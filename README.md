# Dr Jamie Brian Smith — personal website

Hugo source for [jamiebriansmith.com](https://jamiebriansmith.com/), using the existing Hugo Blox résumé modules and custom Riso styling.

## Source and generated files

Edit `content/` for pages, `data/authors/` for identity and profile data, `config/_default/` for site settings, `layouts/_partials/` for template overrides, and `static/css/` for the custom styles. Artwork is in `assets/media/`.

The HTML, CSS and JavaScript at the repository root are generated publishing output. `public/` is the normal local build output. Do not edit generated HTML in place. `static/us/` and `static/lom/` are standalone legacy pages with deliberate `noindex` metadata; retain those privacy preferences. Their Pagefind exclusions also keep them out of on-site search. `pagefind.yml` limits indexing to routed pages, excluding the standalone 404 page.

## Local build and review

The workflows use Hugo **0.154.5 extended**, Node **22** and pnpm **10.14.0**. The pinned Hugo modules are in `go.mod`; dependencies are in `pnpm-lock.yaml`.

```sh
pnpm install --frozen-lockfile
pnpm run build
python3 scripts/check_site.py public
python3 -m http.server 4173 --bind 127.0.0.1 --directory public
```

A build can also go outside the checkout, for example:

```sh
hugo --minify --destination ../review/personal-build
pnpm exec pagefind --site ../review/personal-build
python3 scripts/check_site.py ../review/personal-build
```

## Deployment boundary

Both `build-and-publish.yml` and `deploy-pages.yml` react to source changes pushed to `main`. The first copies generated output to the repository root and commits it; the second builds and deploys a Pages artifact. A review branch and local build do **not** publish the site. Do not push to `main` or dispatch a deployment workflow during review. The Netlify configuration is also retained; the live hosting path should be confirmed before changing deployment arrangements.

## Content homes

- Home: short introduction and routes into the site.
- About: biography, current roles and publishing-name variants.
- Research: the research programme.
- Institutional ethnography: methodological lineage and Jamie’s nursing studies.
- Critical posthumanism: an introductory resource and reading routes, distinct from the methods page.
- Publications: the manually maintained bibliography and article links.
- Elsewhere: institutional profiles, editorial roles, recognition and speaking.
- Compost Collaborative: collective projects, creative work and events.

Publication records distinguish preprints, protocols, editorials and journal articles. Verify substantive corrections against publishers or institutional repositories. `scripts/sync_orcid_publications.py` is a legacy opt-in importer that expects `ORCID_WORKS` markers; the present bibliography uses `SCHOLAR_WORKS` markers and is not automatically overwritten by that script. Do not replace the curated bibliography by running the importer without reviewing its output.

The current crawler policy permits public crawling. No model-training opt-out has been introduced. Search access and training permissions are separate decisions; `llms.txt` is supplementary documentation, not a condition of search visibility.

Built on [Hugo Blox](https://github.com/HugoBlox/kit), under the existing repository licence.
