#!/usr/bin/env python3
"""Validate production HTML, metadata, local links and the Pagefind 1.4 index."""
import gzip
from html.parser import HTMLParser
import json
import re
from pathlib import Path
import sys
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicate_ids = []
        self.links = []
        self.canonical = []
        self.descriptions = []
        self.social = {}
        self.h1 = self.main = self.titles = 0
        self.noindex = self.ignore_search = self.in_json = self.in_title = self.in_head = False
        self.json_text = self.title_text = ''
        self.schemas = []
        self.missing_alt = []
        self.citation_meta = {}
        self.body_text = []
        self.downloads = []
        self.in_raw = False
        self.paper_title = ''
        self.in_h1 = False
        self.paper_kinds = []
        self.paper_dois = []
        self.open_elements = []
        self.element_order = 0
        self.regions = {name: [] for name in
                        ('author', 'abstract', 'no_abstract', 'tldr', 'citation')}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.element_order += 1
        hidden = (any(element['hidden'] for element in self.open_elements)
                  or 'hidden' in a or a.get('aria-hidden') == 'true'
                  or bool(re.search(r'(?:display\s*:\s*none|visibility\s*:\s*hidden)',
                                    a.get('style', ''), flags=re.I)))
        element = {'tag': tag, 'hidden': hidden, 'regions': [], 'paragraphs': []}
        markers = {'data-paper-author': 'author', 'data-paper-abstract': 'abstract',
                   'data-no-abstract': 'no_abstract', 'data-paper-tldr': 'tldr'}
        names = [name for marker, name in markers.items() if marker in a]
        if a.get('id') == 'paper-citation':
            names.append('citation')
        for name in names:
            region = {'text': [], 'paragraphs': [], 'ids': set(), 'headings': set(),
                      'order': self.element_order}
            self.regions[name].append(region)
            element['regions'].append(region)
        active = self.open_elements + [element]
        for ancestor in active:
            for region in ancestor['regions']:
                if a.get('id'):
                    region['ids'].add(a['id'])
                    if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and not hidden:
                        region['headings'].add(a['id'])
                if tag == 'p':
                    paragraph = []
                    region['paragraphs'].append(paragraph)
                    element['paragraphs'].append(paragraph)
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                       'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.open_elements.append(element)
        if tag == 'article' and ('data-paper-kind' in a or 'data-publication-doi' in a):
            self.paper_kinds.append(a.get('data-paper-kind', 'journal-article'))
            self.paper_dois.append(a.get('data-publication-doi', ''))
        if a.get('id'):
            if a['id'] in self.ids:
                self.duplicate_ids.append(a['id'])
            self.ids.add(a['id'])
        if tag == 'h1':
            self.h1 += 1
            self.in_h1 = True
        if tag in ('script', 'style'):
            self.in_raw = True
        if tag == 'main':
            self.main += 1
        if tag == 'head':
            self.in_head = True
        if tag == 'title' and self.in_head:
            self.in_title = True
            self.titles += 1
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
            if 'download' in a:
                self.downloads.append(a['href'])
        if tag in ('img', 'script') and a.get('src'):
            self.links.append(a['src'])
        if tag == 'img' and 'alt' not in a:
            self.missing_alt.append(a.get('src', 'unnamed image'))
        if tag == 'link' and a.get('rel') == 'stylesheet':
            self.links.append(a.get('href', ''))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a.get('href', ''))
        if tag == 'meta' and a.get('name', '').startswith('citation_'):
            self.citation_meta.setdefault(a['name'], []).append(a.get('content', ''))
        if tag == 'meta' and a.get('name') == 'description':
            self.descriptions.append(a.get('content', ''))
        if tag == 'meta' and a.get('name') == 'robots':
            self.noindex = self.noindex or 'noindex' in a.get('content', '')
        if tag == 'meta' and a.get('property'):
            self.social[a['property']] = a.get('content', '')
        if tag in ('html', 'body') and a.get('data-pagefind-ignore') == 'all':
            self.ignore_search = True
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.in_json = True
            self.json_text = ''

    def handle_data(self, data):
        if not self.in_head and not self.in_raw:
            self.body_text.append(data)
            if not any(element['hidden'] for element in self.open_elements):
                for element in self.open_elements:
                    for region in element['regions']:
                        region['text'].append(data)
                    for paragraph in element['paragraphs']:
                        paragraph.append(data)
        if self.in_h1:
            self.paper_title += data
        if self.in_title:
            self.title_text += data
        if self.in_json:
            self.json_text += data

    def handle_endtag(self, tag):
        for index in range(len(self.open_elements) - 1, -1, -1):
            if self.open_elements[index]['tag'] == tag:
                del self.open_elements[index:]
                break
        if tag in ('script', 'style'):
            self.in_raw = False
        if tag == 'h1':
            self.in_h1 = False
        if tag == 'head':
            self.in_head = False
        if tag == 'title':
            self.in_title = False
        if tag == 'script' and self.in_json:
            self.schemas.append(json.loads(self.json_text))
            self.in_json = False


def entities(schema):
    """Include top-level graphs without treating referenced sub-entities as duplicates."""
    if isinstance(schema, list):
        for item in schema:
            yield from entities(item)
    elif isinstance(schema, dict):
        yield schema
        yield from entities(schema.get('@graph', []))


def normalise_text(value):
    return ' '.join(re.findall(r'\w+', value, flags=re.UNICODE)).casefold()


def check_publication(page, rel, canonical):
    """Check visible scholarly records against their type-specific metadata and schema."""
    kinds = {
        'journal-article': ('ScholarlyArticle', 'citation_journal_title'),
        'conference-abstract': ('ScholarlyArticle', 'citation_journal_title'),
        'preprint': ('ScholarlyArticle', 'citation_journal_title'),
        'book-chapter': ('Chapter', 'citation_inbook_title'),
        'thesis': ('Thesis', 'citation_dissertation_institution'),
        'protocol': ('CreativeWork', 'citation_technical_report_institution'),
    }
    issues = []
    if len(page.paper_kinds) != 1:
        issues.append(f'{rel}: expected one marked publication article, found {len(page.paper_kinds)}')
    kind = page.paper_kinds[0] if page.paper_kinds else 'journal-article'
    if kind not in kinds:
        return issues + [f'{rel}: unsupported publication kind {kind!r}']
    schema_type, container_key = kinds[kind]
    scholarly_types = {value[0] for value in kinds.values()}
    found = [item for schema in page.schemas for item in entities(schema)
             if scholarly_types.intersection(item.get('@type', [])
                                             if isinstance(item.get('@type'), list)
                                             else [item.get('@type')])]
    if len(found) != 1:
        return issues + [f'{rel}: expected one {schema_type} for {kind}, found {len(found)} scholarly entities']
    article = found[0]
    if article.get('@type') != schema_type:
        issues.append(f'{rel}: {kind} must use {schema_type}, found {article.get("@type")}')
    meta = page.citation_meta
    for key in ('citation_title', container_key, 'citation_doi',
                'citation_year', 'citation_publication_date'):
        if len(meta.get(key, [])) != 1 or not meta[key][0]:
            issues.append(f'{rel}: missing/duplicate {key}')
    for key in {value[1] for value in kinds.values()} - {container_key}:
        if key in meta:
            issues.append(f'{rel}: {kind} must not use {key}')
    title = meta.get('citation_title', [''])[0]
    if title != article.get('headline') or normalise_text(title) != normalise_text(page.paper_title):
        issues.append(f'{rel}: paper title differs across H1, metadata and schema')
    authors = [author.get('name', '') for author in article.get('author', [])]
    if not authors or any(not author.strip() for author in authors) or authors != meta.get('citation_author', []):
        issues.append(f'{rel}: ordered byline differs between citation metadata and schema')
    visible_authors = [' '.join(''.join(region['text']).split())
                       for region in page.regions['author']]
    if visible_authors != authors:
        issues.append(f'{rel}: visible byline differs from the complete ordered schema byline')
    visible = normalise_text(' '.join(page.body_text))
    for author in authors:
        if normalise_text(author) not in visible:
            issues.append(f'{rel}: schema author absent from visible page: {author}')
    abstracts = page.regions['abstract']
    no_abstract = page.regions['no_abstract']
    if no_abstract:
        if len(no_abstract) != 1 or not ''.join(no_abstract[0]['text']).strip():
            issues.append(f'{rel}: missing/duplicate visible explanation for an unavailable abstract')
        if abstracts or 'abstract' in article:
            issues.append(f'{rel}: unavailable abstract must have no abstract region or schema abstract')
    else:
        abstract = article.get('abstract', '')
        abstract_text = ' '.join(abstracts[0]['text']) if len(abstracts) == 1 else ''
        if (not isinstance(abstract, str) or not abstract.strip()
                or normalise_text(abstract) != normalise_text(abstract_text)):
            issues.append(f'{rel}: complete schema abstract does not match the visible abstract region')
    tldr = page.regions['tldr']
    if len(tldr) != 1:
        issues.append(f'{rel}: expected one visible TL;DR section, found {len(tldr)}')
    else:
        paragraphs = tldr[0]['paragraphs']
        if len(paragraphs) != 3 or any(not ''.join(p).strip() for p in paragraphs):
            issues.append(f'{rel}: TL;DR must contain exactly three nonempty visible paragraphs')
        if 'paper-tldr-heading' not in tldr[0]['headings']:
            issues.append(f'{rel}: TL;DR is missing its paper-tldr-heading heading')
        if any(tldr[0]['order'] >= region['order']
               for region in abstracts + no_abstract + page.regions['citation']):
            issues.append(f'{rel}: TL;DR must precede the abstract and citation')
    doi = meta.get('citation_doi', [''])[0]
    if not re.fullmatch(r'10\.\d{4,9}/\S+', doi, flags=re.I) or article.get('@id') != 'https://doi.org/' + doi:
        issues.append(f'{rel}: incorrect or inconsistent DOI')
    if article.get('mainEntityOfPage', {}).get('@id') != canonical:
        issues.append(f'{rel}: article does not identify its canonical webpage')
    if page.paper_dois != [doi]:
        issues.append(f'{rel}: marked publication DOI differs from citation metadata')
    citations = page.regions['citation']
    citation = normalise_text(' '.join(citations[0]['text'])) if len(citations) == 1 else ''
    if not citation or not citation.startswith(normalise_text(' '.join(authors))):
        issues.append(f'{rel}: visible citation is missing the complete ordered byline')
    for label, value in (('title', title), ('DOI', doi),
                         ('year', meta.get('citation_year', [''])[0])):
        if value and normalise_text(value) not in citation:
            issues.append(f'{rel}: visible citation does not include its bibliographic {label}')
    container_name = meta.get(container_key, [''])[0]
    if container_key in ('citation_journal_title', 'citation_inbook_title'):
        container = article.get('isPartOf', {})
        seen = set()
        while isinstance(container, dict) and container.get('isPartOf'):
            if id(container) in seen:
                break
            seen.add(id(container))
            container = container['isPartOf']
        expected_type = 'Book' if kind == 'book-chapter' else 'Periodical'
        if (not isinstance(container, dict) or container.get('name') != container_name
                or container.get('@type') != expected_type):
            issues.append(f'{rel}: {expected_type} container differs between metadata and schema')
    else:
        institutions = [article.get(key, {}) for key in ('publisher', 'sourceOrganization')]
        if not any(isinstance(item, dict) and item.get('name') == container_name
                   for item in institutions):
            issues.append(f'{rel}: institution differs between metadata and schema')
    if container_name and normalise_text(container_name) not in citation:
        issues.append(f'{rel}: visible citation omits its publication container/institution')
    citation_date = meta.get('citation_publication_date', [''])[0]
    if not re.fullmatch(r'\d{4}(?:/\d{2}/\d{2})?', citation_date):
        issues.append(f'{rel}: citation date must be a full calendar date or known year')
    if citation_date[:4] != meta.get('citation_year', [''])[0]:
        issues.append(f'{rel}: citation date and bibliographic year disagree')
    if not re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?', article.get('datePublished', '')):
        issues.append(f'{rel}: invalid scholarly publication date')
    article_number = next((item.get('value') for item in article.get('identifier', [])
                           if item.get('propertyID') == 'Article number'), '')
    for key, value in (('citation_firstpage', article.get('pageStart') or article_number),
                       ('citation_lastpage', article.get('pageEnd'))):
        if meta.get(key, []) != ([str(value)] if value else []):
            issues.append(f'{rel}: pagination/article locator differs between metadata and schema')
    for pdf in meta.get('citation_pdf_url', []):
        if not pdf.startswith(canonical) or pdf not in page.links:
            issues.append(f'{rel}: citation PDF must be a visible verified sibling of the abstract page')
    for extension in ('.bib', '.ris'):
        if len([url for url in page.downloads if url.endswith(extension)]) != 1:
            issues.append(f'{rel}: missing/duplicate downloadable {extension} citation')
    if '/publications/' not in page.links:
        issues.append(f'{rel}: missing route back to publications')
    return issues


root = Path(sys.argv[1] if len(sys.argv) > 1 else 'public').resolve()
origin = 'https://jamiebriansmith.com'
errors = []
pages = {}
publication_count = 0
for file in root.rglob('*.html'):
    page = Page()
    try:
        page.feed(file.read_text())
    except (ValueError, UnicodeError) as error:
        errors.append(f'{file.relative_to(root)}: invalid HTML/JSON-LD: {error}')
    pages[file] = page

for file, page in pages.items():
    rel = file.relative_to(root).as_posix()
    if rel in ('us/index.html', 'lom/index.html'):
        if not page.noindex or not page.ignore_search:
            errors.append(f'{rel}: lost noindex or on-site search exclusion')
        continue
    if rel == '404.html':
        continue
    if page.h1 != 1 or page.main != 1:
        errors.append(f'{rel}: expected one h1 and main, found {page.h1}/{page.main}')
    if page.duplicate_ids:
        errors.append(f'{rel}: duplicate IDs {page.duplicate_ids}')
    if page.missing_alt:
        errors.append(f'{rel}: images without alt {page.missing_alt}')
    if '#main-content' not in page.links:
        errors.append(f'{rel}: missing skip link')
    if page.titles != 1 or not page.title_text.strip():
        errors.append(f'{rel}: missing/duplicate title')
    if len(page.descriptions) != 1 or not page.descriptions[0].strip():
        errors.append(f'{rel}: missing/duplicate description')
    route = '/' if rel == 'index.html' else '/' + rel.removesuffix('index.html')
    if page.canonical != [origin + route]:
        errors.append(f'{rel}: unexpected canonical {page.canonical}')
    for field in ('og:title', 'og:description', 'og:image', 'twitter:image', 'og:image:alt'):
        if not page.social.get(field):
            errors.append(f'{rel}: missing social metadata {field}')
    if page.social.get('og:url') != origin + route:
        errors.append(f'{rel}: incorrect social URL')
    if page.social.get('og:locale') != 'en_GB':
        errors.append(f'{rel}: incorrect Open Graph locale')
    for href in page.links + [page.social.get('og:image', '')]:
        url = urlparse(href)
        if url.scheme in ('mailto', 'tel', 'data', 'javascript'):
            continue
        if url.netloc and url.netloc != 'jamiebriansmith.com':
            continue
        target = (root / unquote(url.path).lstrip('/')) if url.path.startswith('/') else file.parent / unquote(url.path)
        if not url.path:
            target = file
        if target.is_dir():
            target = target / 'index.html'
        if not target.exists():
            errors.append(f'{rel}: missing local target {href}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{rel}: missing fragment {href}')
    people = [item for schema in page.schemas for item in entities(schema)
              if 'Person' in (item.get('@type') if isinstance(item.get('@type'), list) else [item.get('@type')])]
    if len(people) != 1:
        errors.append(f'{rel}: expected one Person entity, found {len(people)}')
    elif people[0].get('name') != 'Dr Jamie Brian Smith':
        errors.append(f'{rel}: wrong identity')
    if page.citation_meta or (rel.startswith('publications/') and rel != 'publications/index.html'):
        publication_count += 1
        errors.extend(check_publication(page, rel, origin + route))

urls = [item.text for item in ET.parse(root / 'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
for route in ('/', '/about/', '/research/', '/institutional-ethnography/', '/critical-posthumanism/', '/publications/'):
    if origin + route not in urls:
        errors.append(f'sitemap: missing {route}')
for route in ('/us/', '/lom/'):
    if origin + route in urls:
        errors.append(f'sitemap: noindex legacy URL {route}')

# Pagefind 1.4 stores gzip JSON fragments after this format marker.
search_urls = set()
for fragment in (root / 'pagefind' / 'fragment').glob('*.pf_fragment'):
    payload = gzip.decompress(fragment.read_bytes()).removeprefix(b'pagefind_dcd')
    record = json.loads(payload)
    search_urls.add(record['url'])
    if 'ESC All Results Searching' in record.get('content', ''):
        errors.append(f'Pagefind: search modal indexed in {record["url"]}')
expected_urls = {url.removeprefix(origin) for url in urls}
if search_urls != expected_urls:
    errors.append(f'Pagefind routes differ from sitemap: missing {expected_urls - search_urls}; extra {search_urls - expected_urls}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(pages)} HTML pages and {publication_count} scholarly records; metadata, JSON-LD, full bylines/abstracts, TL;DRs, headings, main/skip links, local links/assets, sitemap and {len(search_urls)} search routes; legacy noindex preserved.')
