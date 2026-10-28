# Design: Jamie B. Smith

Shared design system for the academic website. The source content and metadata remain authoritative.

## System

- Hallmark Riso v2, selected by Jamie on 28 October 2026.
- Editorial, with a long-document structure for the academic record.
- Homepage and About use a split opening: large name beside distinct science-fiction landscapes.
- The Riso draw was `28a026`. The poster suggestion became a split composition to keep the artwork clear and text legible. The existing academic record takes precedence over an agency portfolio anatomy.
- Original artwork and portraits retain their full colour at Jamie's request. No image files are replaced or retouched.
- Home keeps the original mountain-and-planets artwork; About uses the generated sea-and-rock-arches companion in `assets/media/about-scifi-sea.png`. Its prompt and provenance are in `ABOUT_SCIFI_ASSET.md`.
- Jamie's review changes: portraits are now up to 448px on desktop, 292px on tablet and 336px on phones, constrained to the available width, with 896px image renditions. The homepage's main heading reads “Jamie B. Smith”, the Elsewhere heading reads “Elsewhere”, and LOM is removed from the navigation.
- Copy and destinations remain in `content/` and `data/`; design templates render those records.

## Tokens and type

- `static/css/tokens.css` is the palette and spacing source of truth.
- Cabinet Grotesk 800 for display and controls; Literata 400/500 for body and navigation.
- Warm paper, medium blue ink, pink fills. The existing dark-mode control uses a corresponding dark-blue palette.
- Misregistration appears on one word in the opening heading only.
- Academic prose remains 60–70 characters wide with comfortable leading.
- Riso's mobile link wrapping is intentional for long, descriptive academic links; navigation labels stay on one line.

## Controls and motion

- Primary: pink rectangle with deep-blue text, 48px minimum height.
- Links: blue text and pink underline. Focus rings are immediate and visible.
- Mobile navigation, search and the existing appearance control remain functional.
- No decorative movement; reduced-motion preferences are honoured.

## Existing pages

- Homepage and About: new biography layout with the original author data.
- Research, consultancy, publications, external profiles, research influence, institutional ethnography and portrait: shared Riso typography and reading layout.
- The separate `/lom/` and `/us/` static applications remain byte-for-byte unchanged.
- Schema.org identity information, canonical URLs and existing search setup remain intact.

## Exports

`static/css/tokens.css`, `base.css`, `riso.css`, `riso-hero.css`, `riso-fonts.css`.
Local fonts and their sources are in `static/fonts/`.
