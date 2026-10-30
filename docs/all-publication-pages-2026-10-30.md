# Publication collection and editorial pass — 30 October 2026

Local review only. Nothing pushed, merged, deployed or submitted for indexing.

The existing scholarly bibliography now links to 31 publication pages: the five approved pages plus 26 additions. These include 24 journal papers, two conference abstracts, two chapters, a thesis, a scoping review protocol and a superseded preprint. The three Public Philosophy essays remain external links. No main navigation item was added.

## Reading and citing

Each page opens with three short TL;DR paragraphs: a relatable hook, a design-appropriate account of the research, and a return to the everyday question. These are new website summaries. They distinguish conceptual arguments, observed findings, pilot work and planned trials without inventing anecdotes or results.

Twenty-seven records have complete verified abstracts. Four have explicit explanations instead:

| Publication | Abstract status | Full-text access |
| --- | --- | --- |
| Invisible Yet Indispensable | The editorial has no published abstract | Free to read at Wiley; no open reuse licence verified |
| We All Care, ALL the Time | The commentary has no published abstract | Publisher full text, CC BY-NC-ND 4.0 |
| Making Care Perceptible | Available descriptions are truncated; no complete abstract was verified | Newcastle deposit is embargoed until 1 August 2028 |
| Antimicrobial prescribing protocol | No conventional abstract; the exact stated aim is shown separately | Original and updated public OSF PDFs |

Twenty-eight records have verified free reading routes, including publicly readable conference abstracts and repository manuscripts. This count does not imply that every version has a Creative Commons licence. No free complete copy was verified for *Mattering*, *Making Care Perceptible* or *imagining afFIRMative futures for nursing*. Their pages retain the DOI/source route and describe the access limit. PDFs are linked at their legitimate host, not rehosted.

The March 2026 homogeneity preprint points prominently to the October 2026 PLOS ONE article. The OSF prescribing protocol points to the completed scoping review. These are labelled stages or versions, not presented as additional independent studies.

## Evidence and unresolved source discrepancies

The [source audit](publication-source-audit-2026-10-30.json) records authoritative publisher, Crossref, PubMed/PMC, DataCite, OSF and institutional-repository evidence for each page. Raw retrievals and the independent TL;DR review remain in the adjacent local review folder.

Corrections needed outside this repository, not applied:

- **OJIN / Crossref:** the author ORCIDs for *An Ethics of Artificial Intelligence for Nursing* are swapped. The website preserves the published byline and uses Jamie’s verified site identity; it does not reproduce the swapped identifiers.
- **Making Care Perceptible / Crossref:** the chapter DOI record omits Jamie from its author list. The page and downloads use the four authors confirmed by JSTOR and institutional records: Jamie B. Smith, Eva Willis, Kieran Sheehan and Emily Jones.
- **OSF creator order:** DataCite’s project creator order differs from the protocol PDF byline. The citation follows the document’s ordered byline.
- **Thesis:** the repository’s 2023 issue date and title differ from the PDF cover’s Spring 2021 date and title wording. The page follows the repository citation and explicitly labels the date as repository publication, not a degree award date.
- Exact dates conflict for *Interpreting Posthumanism* and the two chapters. Year-level citation dates are retained where necessary; independently verified online dates remain separate.
- Eva-Maria Willis’s joint-first-author credit on the person-centred-care paper is displayed.

## Editorial decisions

The complete personal-site preview received a plain-language pass after Jamie requested human, concise copy. Redundant Contribution and Using this research sections were removed from publication pages: the TL;DR and published abstract already perform those jobs. Website summaries, access notes and landing-page copy were tightened; audit explanations were kept in this report. Published abstracts, quotations, titles, citation data, identity facts and source links were protected. The [publication editorial check](publication-editorial-check-2026-10-30.md) records identical before/after hashes for every protected field; the [landing-page check](site-editorial-check-2026-10-30.md) records the wider cuts.

The three-part TL;DR structure is intentional and requested. It is not an authorship test. Necessary scientific qualifications remain attached to the findings they qualify.

## Implementation

The JSON front matter in `content/publications/<slug>/index.md` is authoritative. Shared Hugo templates generate the visible record, scholarly metadata, BibTeX and RIS. No new application dependencies were introduced.

- `paper.tldr` contains `hook`, `science` and `so_what`; all are visible HTML immediately below the title.
- `paper.kind` distinguishes `journal-article`, `conference-abstract`, `book-chapter`, `thesis`, `protocol` and `preprint`. Journal-published trial protocols remain journal articles with an explicit study-type label.
- Journal and conference records use ScholarlyArticle; chapters use Chapter; the thesis uses Thesis; the OSF protocol uses CreativeWork. Missing abstracts are omitted from schema rather than replaced by a website summary.
- Citation exports use article/JOUR, incollection/CHAP, phdthesis/THES, techreport/RPRT and unpublished/UNPB as appropriate. Preprint/protocol status is also stated in notes or genre fields. Reader applications vary in how they retain RIS notes and genre labels.
- Titles and book titles are protected against BibTeX case conversion. Special TeX characters are escaped. Page ranges and article locators are not duplicated.
- Issue and first-online dates remain separate. The page’s edit date is never substituted for the publication date.
- All pages are reached from Publications and included in the sitemap and on-site search. Human visitors and crawlers receive the same content. No hidden crawler copy or extra menu tabs were added.

Schema types follow the official [Chapter](https://schema.org/Chapter) and [Thesis](https://schema.org/Thesis) definitions; bibliographic metadata follows [Google Scholar’s inclusion guidance](https://scholar.google.com/intl/en/scholar/inclusion.html). These changes do not establish actual search inclusion or promise citations or a knowledge panel.

## Validation and review files

The production build contains 44 HTML pages, with 41 public sitemap/search routes and 31 scholarly records. The generated-site checker covers titles, canonical URLs, metadata/schema agreement, ordered bylines, complete abstract text or explicit missing-abstract notes, three-part TL;DRs, citation downloads, local links and legacy privacy exclusions. An independent HTML audit found no issues.

All 62 citation exports passed independent Pandoc import and comparison with the source records, with zero failing records. The audit distinguishes real template defects from Pandoc-only smart-quote and genre-label conversion. All 31 publication pages and nine edited landing pages passed desktop and mobile checks at 1440 × 1000 and 390 × 844, with no horizontal overflow or broken images. A real thesis RIS download matched the generated file. Saved captures and browser checks are in the review package.

The build is saved at `../previews/personal`; the offline gallery is `../paper-preview.html`. Local Hugo 0.155.1 Extended was used with the existing dependencies. The exact remote CI environment was not run because this branch was not pushed.
