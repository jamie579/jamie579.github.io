#!/usr/bin/env python3
"""Validate production HTML, metadata, local links and the Pagefind 1.4 index."""
import gzip
from html.parser import HTMLParser
import json
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

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            if a['id'] in self.ids:
                self.duplicate_ids.append(a['id'])
            self.ids.add(a['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'main':
            self.main += 1
        if tag == 'head':
            self.in_head = True
        if tag == 'title' and self.in_head:
            self.in_title = True
            self.titles += 1
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag in ('img', 'script') and a.get('src'):
            self.links.append(a['src'])
        if tag == 'img' and 'alt' not in a:
            self.missing_alt.append(a.get('src', 'unnamed image'))
        if tag == 'link' and a.get('rel') == 'stylesheet':
            self.links.append(a.get('href', ''))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a.get('href', ''))
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
        if self.in_title:
            self.title_text += data
        if self.in_json:
            self.json_text += data

    def handle_endtag(self, tag):
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


root = Path(sys.argv[1] if len(sys.argv) > 1 else 'public').resolve()
origin = 'https://jamiebriansmith.com'
errors = []
pages = {}
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
print(f'PASS: {len(pages)} HTML pages; metadata, JSON-LD, headings, main/skip links, local links/assets, sitemap and {len(search_urls)} search routes; legacy noindex preserved.')
