# brc-site

Mock-up of the website for Business Research & Consulting (BRC), a course of the Faculty of Economics and Business, University of Groningen.

**Status: mock-up for internal approval. Not the live site.**

## Pages

- `index.html`: homepage (Dutch, the default language)
- `submit.html`: three-step assignment form (mock-up only; nothing is sent)
- `product.html`: placeholder for the example-assignment pages
- `students.html`: placeholder for the information-for-students page
- `en/`: the same four pages in English. "NL / EN" in the header switches language.
- `nl/`: TEMPORARY forwarding pages to the Dutch pages at the root (Dutch used to live here). Delete this folder after approval.

## Versions

See `CHANGELOG.md`. Each finished version is kept as a branch named `archive/vX.Y.Z` that is never changed afterwards.

Plain HTML with inline styles and a little JavaScript. Open `index.html` in a browser to view.

The pages are generated from the sources in `tools/`. To change the site, edit there and regenerate; see `tools/README.md`.

## Assets

- `assets/rug-logo-en.svg`, `assets/rug-logo-nl.svg`: University of Groningen logos, converted from the official EPS files. The Dutch one is kept ready for the Dutch version.
- `assets/brc-crown-*.svg`: the crown from the university logo, used in the BRC wordmark. Use is pending approval.
- `assets/client-*.png`: client logos taken from the clients' own websites.
- `assets/linkedin-*.png`: official LinkedIn icon files.

## Open items before going live

- Text in [SQUARE BRACKETS] is a placeholder.
- The Dutch text is a first translation and needs proofreading.
- Six client logos are still missing (the carousel shows the name instead).
- Team links are placeholders except two homepages and one LinkedIn profile.
- The three homepage pictures (`assets/photo-*.jpg`) are AI-generated and show people who do not exist; replace with real photos or disclose before launch.
- Fonts load from Google Fonts; consider hosting them locally.
- Pages carry a `noindex` tag so search engines skip the mock-up. Remove it at launch.
