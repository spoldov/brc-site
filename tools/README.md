# tools: how the pages are generated

The HTML pages (four Dutch at the site root, four English in `en/`, plus four temporary forwarding pages in `nl/`) are generated from the files in this folder. Change the sources here and regenerate; do not edit the generated HTML by hand, or the next run will overwrite it.

## Files

- `src/C-TenWeeks.dc.html`: source of the homepage (`index.html`). Since design v2 this file is maintained by hand: all homepage styling is in the `<style>` block at its top, with the colours and sizes as variables in the first lines.
- `src/Submit.dc.html`: source of the assignment form (`submit.html`)
- `src/Product.dc.html`, `src/Students.dc.html`, `src/Newsletter.dc.html`: sources of the three placeholder pages (`product.html`, `students.html`, `newsletter.html`)
- `nl.json`: the Dutch translation, as "English text": "Dutch text"
- `build_site.py`: step 1, builds the English pages from `src/` into `tools/.build/` (an intermediate folder, not kept in git)
- `i18n.py`: step 2, adds the language switch (EN / NL) and the "Built with Claude Fable 5.2 and Opus 5.5" line, then writes the Dutch pages to the site root and the English pages to `en/`
- `make_illustrations.py`: draws the three temporary homepage illustrations into `assets/` (only needed when they change)
- `make_share_images.py`: makes the browser-tab icons and the link-preview pictures in `assets/` (only needed when the headline, the red or the wordmark changes; needs Playwright and Chrome, see the top of the file)

The sources started as exports from the design canvas; the homepage source no longer matches the canvas. They contain a few template marks (`{{...}}`, `<sc-if>`, `<sc-for>`) that `build_site.py` turns into plain HTML and JavaScript.

## Regenerating

Run both commands from the repository root, in this order. They overwrite the eight HTML files.

`python3 tools/build_site.py`

`python3 tools/i18n.py`

Needs Python 3 only; no packages.

## Where to change what

| To change | Edit |
|---|---|
| Layout, styling or English text | the matching file in `src/` |
| Dutch text | `nl.json` |
| English text that has a Dutch version | the file in `src/` **and** the matching key in `nl.json` (the key must equal the new English text exactly) |
| Rotating headline phrases | `build_site.py` (search for `phrases`), and `nl.json` for Dutch |
| Team members and their links | `build_site.py` (search for `people=`) |
| Price notes and button labels in the form | `build_site.py` (search for `JS_SUBMIT`), and `nl.json` for Dutch |
| Language switch, AI-disclosure line | `i18n.py` |
| Web address used in link previews, preview description text | `i18n.py` (`SITE_URL`, `DESC`). **Change `SITE_URL` when the site moves to its final address.** |
| Footer of the form and placeholder pages | `build_site.py` (search for `SUBFOOT`); its styling is at the end of the `<style>` block in each of the three sub-page sources |
| The red, other colours, page width, text size | the `:root`, `html` and `.wrap` lines at the top of the `<style>` block in `src/C-TenWeeks.dc.html` |
| Homepage motion (scroll reveal, timeline, counters, sticky header) | `build_site.py` (search for `JS_INDEX`) |
| Client logos in the carousel | `src/C-TenWeeks.dc.html`: each row is written once between `<!--REPEAT-->` marks and repeated by `build_site.py`. Since v2.7.0 the boxes are placeholders ("Approvals" / "Pending"). To show a logo once its client has approved: `<div class="client"><img src="assets/client-….png" alt="Name"></div>`; the four earlier logo files are still in `assets/`. Keep an even number of boxes per row so the pattern stays regular |
| BRC wordmark | plain text `<span class="logo"><b>BRC</b></span>` in the header of each source (`.slogo` on the sub-pages). The version with the RUG crown above it is kept as a fallback: the files `assets/brc-crown-white.svg` and `brc-crown-red.svg` are still in the repo, and the full header markup and styling are on branch `archive/v2.6.0` |
| Newsletter link | homepage footer and the newsletter card in "What clients say": `src/C-TenWeeks.dc.html`; footer of the other pages: `SUBFOOT` in `build_site.py`; the page itself: `src/Newsletter.dc.html` |
| Homepage photos | the three pictures are `<div class="photo has-img"><img src="assets/illustration-….svg" alt="…"></div>` in `src/C-TenWeeks.dc.html`. Put the photo in `assets/`, change `src` and `alt` there, and change the matching `alt` key in `nl.json` (Dutch description) |
| Images | add the file to `assets/`; images referenced by id in `src/` are mapped in `build_site.py` (`BLOBS`) |

## Checks after regenerating

- `python3 tools/checks/render_check.py` renders all eight pages at phone, tablet and desktop sizes and reports anything wider than the screen, script errors, broken images, links to missing files and headline phrases that do not fit. Add `--shots` to also save full-page screenshots in `tools/checks/out/` (not kept in git). It needs Playwright and Chrome; see the top of the file.

- `i18n.py` prints "untranslated:" followed by English text it found no Dutch for. Names, logos' alt text, "Week 1" and similar are expected there; a full sentence is not.
- Run `git diff` to see exactly what changed in the generated pages.
