# tools: how the pages are generated

The eight HTML pages (four English, four Dutch) are generated from the files in this folder. Change the sources here and regenerate; do not edit the generated HTML by hand, or the next run will overwrite it.

## Files

- `src/C-TenWeeks.dc.html`: source of the homepage (`index.html`)
- `src/Submit.dc.html`: source of the assignment form (`submit.html`)
- `src/Product.dc.html`, `src/Students.dc.html`: sources of the two placeholder pages
- `nl.json`: the Dutch translation, as "English text": "Dutch text"
- `build_site.py`: step 1, builds the English pages from `src/`
- `i18n.py`: step 2, adds the language flag and the "Built with Claude Fable 5.2" line, then writes the Dutch pages to `nl/`

The sources are the pages as exported from the design canvas. They contain a few template marks (`{{...}}`, `<sc-if>`, `<sc-for>`) that `build_site.py` turns into plain HTML and JavaScript.

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
| Language flag, AI-disclosure line | `i18n.py` |
| Images | add the file to `assets/`; images referenced by id in `src/` are mapped in `build_site.py` (`BLOBS`) |

## Checks after regenerating

- `i18n.py` prints "untranslated:" followed by English text it found no Dutch for. Names, logos' alt text, "Week 1" and similar are expected there; a full sentence is not.
- Run `git diff` to see exactly what changed in the generated pages.
