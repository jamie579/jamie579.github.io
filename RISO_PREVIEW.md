# Riso website preview

Prepared 28 October 2026, in an isolated checkout of `jamie579/jamie579.github.io`.
Source baseline: `a2ddf564080d1c15bf004f516bc0773b100964f5`.
Prepared on branch `design/riso-preview`. Jamie approved publication on 28 October 2026, with a final correction to the editorial roles: Nursing Inquiry editorial-board membership is confirmed by Jamie; the Nursing Philosophy editorial role is TBC. Pushing the approved source commit to `main` runs the repository's build and GitHub Pages deployment workflows.

## Review

- Live local preview: http://localhost:1313/
- Before/after comparison: `.hallmark/compare.html`
- Current desktop and phone images of Home, About and Elsewhere: `.hallmark/revision/`; earlier screenshots of other routes: `.hallmark/final/`.
- Latest enlarged-portrait screenshots for Home and About at desktop, laptop, tablet and phone sizes: `.hallmark/portraits/`. Visual checks passed at all four sizes; short desktop screens use normal document flow.

The preview server is bound to 127.0.0.1. To restart it from this directory:

```sh
hugo --destination .hallmark/site --baseURL http://localhost:1313/
./node_modules/.bin/pagefind --site .hallmark/site
python3 -m http.server 1313 --bind 127.0.0.1 --directory .hallmark/site
```

## Design

- Hallmark Riso: Cabinet Grotesk display type, Literata body, blue ink, pink accents and warm paper.
- Home keeps the existing full-colour sci-fi landscape. About has a distinct generated companion with a turquoise sea, rock arches and a ringed planet. Original files are unchanged; Hugo generates web-sized renditions and CSS supplies a light print texture. See `ABOUT_SCIFI_ASSET.md` for the new asset and its generation prompt.
- Both portraits were enlarged another 40 percent after Jamie's latest review: up to 448px on desktop, 292px on tablet and 336px on phones, constrained to the available column. Hugo serves sharper 896px renditions. The homepage main heading drops “Dr”; Elsewhere's main heading is now “Elsewhere”; the LOM navigation tab is removed.
- Original portraits, author records, body copy and destinations remain. The small decorative hospital emoji was removed.
- The long About biography keeps its portrait/profile column in view on taller desktop screens, with normal document flow on phones, tablets and viewports at most 960px tall.
- Shared article styling covers the nine academic routes; `/lom/` and `/us/` remain byte-identical to the source baseline.
- Fonts are served locally. The design system and font sources are documented in `design.md` and `static/fonts/SOURCES.md`.

## Verified

- Hugo preview and production builds succeed; Pagefind generates its index successfully.
- The nine-page comparison checks the original source baseline against the authorised changes: removal of the nine LOM navigation links/list items, the shorter Elsewhere heading, and the corrected Nursing Inquiry/Nursing Philosophy editorial roles. Other paragraphs/list items, metadata and JSON-LD are preserved. The local verifier records the exact allowed content and menu changes.
- Production canonical URLs and JSON-LD origin pass for all nine pages.
- Hallmark rendered homepage, About, Research and Consultancy at phone, laptop and large desktop sizes. No Floor failures remained. Two article spacing reports are false positives: the following section headings are visible before the fold, so the reported area is not empty. Full details remain in the tool output; this is not a claim of an unqualified clean linter run.
- Mobile menus at 320, 375 and 1024 pixels open with all eight remaining destinations in bounds. Desktop navigation fits at 1280 and 1440 pixels. Revision checks at 375, 768 and 1280 pixels verify the distinct loaded images, increased portrait dimensions, requested headings and absence of horizontal overflow.
- Appearance toggle changes to the dark Riso palette; keyboard focus has a visible three-pixel ring; site search opens and its index returns eight results for “nursing”.
- Publication check found the legacy GitHub Pages root lacked its Pagefind index. The root index is now eligible for the existing build workflow's generated-files commit; `public/` and `static/pagefind/` remain ignored. Verify live search after deployment.
- Independent hero review's mobile word-spacing issue was fixed. Independent finish review's empty About sidebar was addressed with desktop sticky positioning.
- Follow-up artwork review passed on desktop and phone. The latest Hallmark check reports zero hard failures, three spacing reflex findings and three preservation-coverage warnings. The retained hero whitespace and Elsewhere's visible continuation were reviewed; the tool did not accept the spacing waiver. The separate nine-page preservation check passes with the exact authorised changes above. See `.hallmark/revision-lint.txt` and `.hallmark/interaction-revision.jsonl` for the unabridged results.

Reports and reusable checks are under `.hallmark/`, which is ignored by Git. Live publication is verified separately against GitHub Actions and the public website after deployment.
