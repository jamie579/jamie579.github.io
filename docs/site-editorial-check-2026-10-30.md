# Personal website editorial pass

30 October 2026. Scope: non-publication landing pages and the public biography in `data/authors/me.yaml`. Publication pages, their index, templates and the Compost site were assigned elsewhere.

Applied the decontamination and academic-writing-jamie skills, using the opening and a body section of *Staying With the Trouble in Nursing 12.5 Hours at a Time* to check the difference between precise, practice-grounded language and generic explanation. The edits address wording and repetition; they make no claim about authorship detection.

## Changes

- **Home:** shortened the contact and talks links. Kept the research question and clinical biography.
- **About:** put the Charité link directly on the appointment and removed the sentence explaining that the profile verifies it. Described the doctorate's use of posthuman institutional ethnography without implying that Jamie originated the method.
- **Research:** removed “documented on my institutional profile”, shortened link labels and cut the repeated job title. Kept the named studies, instrument length and distinctions between workforce research, philosophy and process evaluation.
- **Institutional ethnography:** retained attribution to Dorothy E. Smith, Carol A. Taylor and Nicola Fairchild, while cutting the defensive originality disclaimer. Removed a repeated methods list and collaboration pitch. Kept the difficult-shift example, thesis methods and regulation study.
- **Critical posthumanism:** removed the disclaimer about the page being incomplete, the contribution announcement and the sentence announcing three reading routes. Kept the histories of exclusion, material relations, distinctions between traditions, coauthor credits and reading list.
- **Consultancy:** cut the repeated biography and offer, shortened descriptions of the work, and replaced generic enquiries language with the information needed to discuss a project. Retained the services, experience examples, uncertainty about evidence, agreed scope and fees.
- **Elsewhere:** removed the introductory and closing verification language. Shortened the Burdett award account by removing the celebration venue and anniversary detail; retained Georgia Duffy, the award year, the fourteen projects and the annual-report citation.
- **Portrait:** shortened the licence explanation while retaining the photographer, copyright, reuse conditions, source, attribution example and restriction of the licence to that image.
- **Research influence:** cut the sentence explaining that the examples document citation and discussion. Kept that exact level of claim and all source/page references.

## Protected text and checks

- Publication titles, authors, DOI and other link destinations, dates, roles, publishing aliases, ORCID, source/page references and the portrait credit were preserved.
- The institutional ethnography lineage and the distinction between feminist new materialism and critical posthumanism remain explicit.
- Policy citations remain citations and discussion; they were not rewritten as evidence of policy change or impact.
- The home biography in `data/authors/me.yaml` was reviewed and left unchanged. Its clinically specific wording already served the page. The unrendered CV history, methods abbreviations and award summaries were left alone.
- The non-rendered `content/authors/_index.md` was checked and left unchanged.
- Compared every changed passage with its starting text for scope and meaning. Programmatic comparison found identical link destinations and date fields in all nine edited pages. Ruby's YAML parser accepted their frontmatter and the author data.
- No new facts, anecdotes, quotations, citations or placeholders were added. No builds, commits or publication actions were performed.
