# Personal website review — 30 October 2026

Prepared on `codex/discoverability-review-2026-10-30`. Nothing was pushed, merged or published.

## What changed

- Made **Dr Jamie Brian Smith** prominent in the visible identity, page titles, descriptions, social metadata and the existing Person schema. Retained the Jamie B. Smith, Jamie B Smith and Jamie Smith publishing variants.
- Shortened Home, About and Research and gave each a clear purpose. Home directs visitors to the programme, methods, publications, consultancy and speaking; About holds the biography; Research explains the programme. Collective projects and events point to Compost.
- Improved the existing institutional ethnography page. Added a distinct critical-posthumanism resource with an introductory example, wider intellectual lineage and three co-authored reading routes. Institutional ethnography is credited to Dorothy E. Smith; the posthumanist institutional ethnography lineage explicitly includes Carol A. Taylor and Nicola Fairchild. Jamie's contribution is located in nursing.
- Corrected publication records and replaced unresolved placeholders with verified links or explicit output types. Removed duplicate editorial-role content in favour of one home on Elsewhere.
- Kept existing routes, artwork and styles. Fixed the decorative surname's duplicate accessible text. Added a keyboard skip link and main landmark; scoped on-site search to main content; retained the noindex settings on the two standalone legacy pages and excluded both from Pagefind. Existing `/us/` already had this search exclusion; `/lom/` did not.
- Removed the unsupported Website SearchAction: the site uses a client-side search modal, not a working `?q=` results route. Retired an inactive legacy schema hook containing conflicting identity data. Existing active Person/ProfilePage markup is retained.

## Source and deployment

Authoritative sources are `content/`, `data/authors/`, `config/_default/`, `layouts/` and `static/`; root HTML is generated publishing output. The README now documents this, builds and the curated bibliography workflow. The legacy ORCID importer expects different markers and was not run over the manually curated bibliography.

Both `build-and-publish.yml` and `deploy-pages.yml` react to changes on `main`. Deployment files, dependency inputs and generated root publishing files were left unchanged. The live host's actual active deployment route should be confirmed before a later publication decision.

The local override in `layouts/baseof.html` follows pinned Hugo Blox commit `27742d31a056` and adds only the skip link, main landmark and Pagefind boundary. Review this override against upstream when upgrading the theme.

## Verification and factual decisions

| Item | Decision and evidence |
| --- | --- |
| Appointments | [Charité institutional profile](https://gender.charite.de/en/metas/person/person/address_detail/msc_jamie_b_smith/) supports the current Charité, Edinburgh Napier and honorary NHS Lothian roles. The honorary qualification is visible. |
| SHORTER | [Official team](https://www.shortertrial.com/our-team) identifies Jamie as Senior Research Fellow (Process Evaluation), with Gosha Colquhoun as Process Evaluation Lead. Removed wording that Jamie leads the process evaluation. |
| Editorial board | Charité identifies **Nursing Philosophy**. Corrected the previous Nursing Inquiry board claim; guest-editing roles remain separate. |
| Doctoral work | [Edinburgh thesis record](https://era.ed.ac.uk/items/351c3676-c09d-42e0-b8a1-98a09eb19475) establishes the thesis identity, 2023 repository record and methods. Its discussion credits posthumanist IE in education to [Taylor & Fairchild (2020)](https://doi.org/10.1080/17457823.2020.1735469). A repository date is not treated as proof of the degree-award date. |
| Intellectual lineage | Linked primary publisher entries for Dorothy E. Smith's 2005 book, Braidotti's *The Posthuman*, Haraway's *Staying with the Trouble* and Barad's *Meeting the Universe Halfway*. Distinguishes adjacent theoretical traditions and collective contributions. |
| Clinical research nursing editorial | Verified [10.1111/jocn.70140](https://doi.org/10.1111/jocn.70140), JCN 35(2), 499–501, and labelled it editorial. |
| SHORTER protocol | Verified [10.1136/bmjopen-2026-117142](https://doi.org/10.1136/bmjopen-2026-117142), BMJ Open 16(3), e117142. |
| Antimicrobial prescribing review | Replaced the incomplete 2025 review entry with the published [2026 scoping review](https://doi.org/10.1016/j.sapharm.2026.08.001). Kept the [2025 OSF protocol](https://doi.org/10.17605/OSF.IO/F9M2K) as a separate, explicitly labelled output. |
| Homogeneity paper | [PLOS publisher](https://doi.org/10.1371/journal.pone.0345194) and PubMed 42949904 confirm publication on 28 October 2026. Added the journal article and labelled the medRxiv version as superseded. |
| Other bibliography repairs | Added verified details for Camp of Reason, Beyond Heroic Individualism, the JAN PIE article, DARTT, the imposter-syndrome conference abstract and both book chapters. Corrected the year of We all care, ALL the time; the Witness title; the missing Emmanuel Christian Tedjasukmana byline in Mattering; and the simulation essay's author order. Replaced general Polyphony-homepage links with the individual articles. |
| Identity links | ORCID and institutional sources support the identity. Wikidata Q136215075 links the exact ORCID and personal homepage; ResearchGate Jamie-Smith-44 has matching Charité affiliation and authored work. X's handle is supported by Edinburgh/Wikidata links, but the account content was unreadable. The Charité research database returned a JavaScript shell, so its deep profile remains access-limited. |

This was a targeted factual audit of discrepancies and links, not certification of every historical CV claim or every field in every bibliographic entry. Some Crossref requests were rate-limited; substantive changed records were checked against publisher, PubMed or institutional records where available. The GMS DOI was confirmed through the official publisher despite a Crossref 404.

## External changes proposed, not performed

1. **University of Edinburgh profile:** update the stale PhD-candidate/expected-summer-2020 biography to reflect the completed thesis and current career, or make its historical status explicit. The personal site now labels it a historical profile.
2. **ORCID, Scholar, LinkedIn and institutional profiles:** where editing access is available, use the full preferred identity **Dr Jamie Brian Smith** and retain recognised publishing variants; ensure the canonical personal homepage is `https://jamiebriansmith.com/`. This is a consistency proposal, not a claim that every account currently lacks these details. Wikidata already contains the Jamie Brian Smith alias and correct homepage/ORCID.
3. **Scilit, SciProfiles and Semantic Scholar:** check the exact identity records and merge/correct duplicates if necessary. Their unverified links were removed from the visible profile list and `sameAs`; no external records were changed.
4. **Publication indexes:** reconcile the newly published PLOS article and scoping review with their preprint/protocol records, and verify corrected DOI/byline information in any manually maintained external list. Automated import should not create duplicate scholarly works.

## Technical validation

- Frozen pnpm lockfile installation completed; no dependency or lockfile changes.
- Production Hugo build passed with local Hugo 0.155.1 extended, pnpm 10.14.0 and Node 24.13.0. CI remains pinned to Hugo 0.154.5 and Node 22; that exact CI combination was not executed locally.
- Pagefind 1.4.0 built one en-GB index with exactly **10 public routes**, matching the sitemap. The two noindex legacy pages, 404 and hidden modal text are excluded. Old intermediate Pagefind fragments were moved outside the final output before regeneration.
- `python3 scripts/check_site.py ../review/personal-build` passed across **13 HTML files**: titles, descriptions, canonicals, social metadata, valid JSON-LD, one Person entity per public page, one H1 and main, duplicate IDs, skip links, image alt attributes, local assets/links/fragments, sitemap and search routes. It checks the pinned Pagefind fragment format.
- `git diff --check` passed. Generated root HTML, the deployment branches and lockfiles remain unchanged.
- Root review performs the desktop/mobile screenshots, keyboard interaction and live search checks against the production output. See the shared review package for those results.

Production output is `../review/personal-build`. Standard build commands are in the README. On this machine, x64 Hugo caused the universal Node binary to start as x64 despite arm64-installed optional packages. A review-only `../review/bin/node` shim forces `/usr/bin/arch -arm64 /usr/local/bin/node`; the verified command was:

```sh
PATH="$PWD/../review/bin:$PATH" hugo --minify --destination ../review/personal-build
pnpm exec pagefind --site ../review/personal-build
python3 scripts/check_site.py ../review/personal-build
```

## Crawler access

The existing permissive `robots.txt` is unchanged. No training opt-out was present, and none was invented. Search retrieval and model-training permissions are separate policy decisions. The existing supplementary `llms.txt` gains the new resource route and shorter description; it is not treated as a search requirement. Pagefind exclusions follow its [official indexing documentation](https://pagefind.app/docs/indexing/) and [CLI configuration](https://pagefind.app/docs/config-options/).

These changes improve the site's information and implementation; they do not promise rankings, AI citations or a knowledge panel.
