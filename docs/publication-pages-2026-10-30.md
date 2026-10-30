# Five publication pages — local review, 30 October 2026

Five journal articles now have individual, readable HTML pages under `/publications/`. They are linked from the existing bibliography and relevant research resources. No navigation item was added. This is the first review batch; the remaining papers have not been converted. Nothing was pushed or published.

## Selection and evidence

The selection represents complementary contributions, rather than claiming these are the five most cited papers. All are first-author papers, with complete coauthor bylines retained.

| Page | Why selected | Authoritative abstract and bibliographic evidence | Article licence |
| --- | --- | --- | --- |
| `posthuman-institutional-ethnography` | An empirical application of posthuman institutional ethnography to nursing regulation and everyday work | [Wiley, DOI 10.1111/jan.17077](https://onlinelibrary.wiley.com/doi/full/10.1111/jan.17077), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12810658/), publisher-deposited [Crossref](https://api.crossref.org/works/10.1111/jan.17077) | CC BY 4.0 |
| `vitruvian-nurse-burnout` | A distinctive conceptual account of professional ideals, regulation and burnout | [Wiley, DOI 10.1111/nin.12538](https://onlinelibrary.wiley.com/doi/full/10.1111/nin.12538), [PubMed](https://pubmed.ncbi.nlm.nih.gov/36424518/), publisher-deposited [Crossref](https://api.crossref.org/works/10.1111/nin.12538) | CC BY-NC 4.0 |
| `posthuman-speculative-ethics` | Collaborative work on the assumptions and exclusions of algorithmic healthcare | [Wiley, DOI 10.1111/nup.12447](https://onlinelibrary.wiley.com/doi/full/10.1111/nup.12447), [PubMed](https://pubmed.ncbi.nlm.nih.gov/37357707/), publisher-deposited [Crossref](https://api.crossref.org/works/10.1111/nup.12447) | CC BY-NC 4.0 |
| `nurse-migration` | Evidence synthesis connecting nurses' experiences with workforce policy | [Sage, DOI 10.1177/15271544221102964](https://journals.sagepub.com/doi/10.1177/15271544221102964), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9274786/), publisher-deposited [XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9274786/fullTextXML) | CC BY 4.0 |
| `nursing-stress-measurement` | Recent quantitative and methodological work on what stress scores support | [PMC, DOI 10.1016/j.ijnsa.2026.100689](https://pmc.ncbi.nlm.nih.gov/articles/PMC13653943/), [PubMed](https://pubmed.ncbi.nlm.nih.gov/42861036/), publisher-deposited [XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13653943/fullTextXML) | CC BY-NC-ND 4.0 |

The complete abstracts are preserved as plain text, including their original spelling and punctuation. The stress abstract's literal `[city blinded]` is retained as published. Commentary below each abstract is separate and bounded by the paper's design. Original published author-name variants are used in citations; the site's Person entity connects recognised Jamie Smith variants without changing the journal bylines. No PDFs are rehosted.

Issue and first-online dates remain distinct: JAN February 2026 / 5 June 2025; Vitruvian January 2024 / 24 November 2022; speculative ethics July 2023 / 26 June 2023; migration August 2022 / 23 June 2022; stress December 2026 collection / 25 September 2026 online. Licence start dates are not treated as publication dates.

## Reusable implementation

Each `content/publications/<slug>/index.md` uses JSON front matter, which Hugo reads natively. The `paper` object is the single source for visible citations, ordered authors, complete abstract sections, scholarly metadata and citation exports. Webpage `date` and `lastmod` are separate from the article's dates.

- `type: publication` selects the shared layout. `outputs: [HTML, BIB, RIS]` produces `index.html`, `cite.bib` and `cite.ris` in the same route.
- `paper.title`, `doi`, `journal`, `year`, ordered `authors`, `abstract`, and verified bibliographic locators describe the published article.
- `publication_date` retains the issue date at known precision; `published_online` records the separately verified online date. Highwire citation dates use a complete issue date if available, or the citation year alone.
- `citation_key`, `citation_bibtex` and `citation_ris` identify exports. The Hugo templates generate both files during the normal build, without a separate generator or new dependencies.
- BibTeX uses the standard `pages` field for page ranges or article locators. It does not duplicate locators in `eid`. RIS uses `JF` for the full journal title. Both formats preserve all authors and the DOI.
- `open_access` records real publisher/repository links and versions. `abstract_source_url`, `abstract_license_url` and `abstract_license_label` attribute the abstract. The current five papers have the same licence across each paper's linked versions; if later versions differ, render a distinct label per version.
- Optional `pdf_url` is only for a verified direct PDF. External PDFs may be visible links; `citation_pdf_url` is emitted only for a local sibling file, following [Scholar guidance](https://scholar.google.com/intl/en/scholar/inclusion.html).

The pages share the normal navigation and accessibility landmarks. Their content is the same for visitors and crawlers. They enter the sitemap and Pagefind automatically; no crawler-only text, hidden abstracts or special navigation layer was introduced. Metadata follows the [Google Scholar inclusion guidance](https://scholar.google.com/intl/en/scholar/inclusion.html); this does not establish actual inclusion.

## Verification

- Production build: Hugo 0.155.1 Extended, existing pinned modules and dependencies. No deployment workflow executed.
- Generated-site checker: 18 HTML files, 15 public sitemap/search routes; all titles, descriptions, canonical URLs, scholarly metadata, schema/visible-abstract agreement, authors, internal links, citation file targets and legacy exclusions passed.
- Independent HTML audit: zero findings.
- All five source abstracts and full author arrays matched the evidence records. Their rendered abstract paragraphs matched the complete source text after whitespace normalization.
- All ten BibTeX/RIS files round-tripped through Pandoc to CSL JSON. Titles, DOI, full authors, journal, year, volume, issue and page/article locators matched the source record.
- All five pages checked at 1440 × 1000 and 390 × 844: no horizontal overflow. Desktop, mobile and complete-page captures saved in the review package. Citation anchor and a real RIS download worked; Publications links reach all five pages. Searching `STERN-57` returns the new paper page.

The full review package, evidence JSONs and saved build are in `../review/` and `../previews/` beside this checkout. The gallery is `../paper-preview.html`. Actual Google/AI indexing remains untested because this work is local only.
