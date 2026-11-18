# Changelog

Each finished version is kept as a branch named `archive/vX.Y.Z`. Archive branches are never changed afterwards.
To look at an old version on GitHub: open the repository, click the branch button (top left, above the file list) and choose the archive branch.

## v2.5.0 (18 November 2026): headline, testimonial section, tab icon, link preview, footers

- Headline: "Real Clients," is now "Real Questions," (Dutch: "Echte Klanten," is now "Echte Vragen,").
- The testimonial and the case box moved out of "Our team" into their own section "What clients say" / "Wat klanten zeggen", directly after the example assignments.
- "What is in it for you?": the icons are red inside the round outline.
- New browser-tab icon (`assets/favicon-*.png`) and link preview (title, description and picture `assets/share-nl.jpg` / `share-en.jpg`) on every page. Both use the letters BRC without the crown. Made by `tools/make_share_images.py`.
- **The link preview contains the full web address of the site** (`SITE_URL` in `tools/i18n.py`, now the GitHub preview address). Change it when the site moves, and run `tools/make_share_images.py` again if the headline changes, because the headline is in the picture.
- The form and placeholder pages have a footer: contact line, RUG logo, the "not part of rug.nl" text, the AI-disclosure line and the address.
- Phones only: the four "What is in it for you?" cards are two by two, and the team is one plain list instead of nine cards.

## v2.4.1 (18 November 2026): pictures back to the illustrations

- The three homepage pictures are the drawn illustrations again (`assets/illustration-*.svg`).
- v2.4.0 had replaced them with three AI-generated photos; the owner withdrew those because they looked too obviously AI-generated. The photo files are removed from the current version. They remain only in the history and in branch `archive/v2.4.0` (the files carry no metadata).

## v2.3.0 (18 November 2026): centred key figures, picture dots, phone alignment

- Key figures: number and label are centred inside each box, on all screen sizes.
- Phones: one picture at a time at full width, with three dots underneath that show which picture is in view (tap a dot to jump).
- Phones: short stand-alone blocks are centred (hero, section headings, key figures, "What is in it for you?" cards, price cards, footer headline and button). Lists and longer text stay left-aligned (example assignments, timeline, team, cost notes, testimonial, case box, footer small print).

## v2.2.0 (18 November 2026): phone and tablet versions, alignment fixes

- **Phones and tablets are now designed.** Up to 1180 px wide the menu collapses into a button that opens a panel; up to 720 px everything is one column, the three pictures become a strip to swipe sideways, and the key figures are two by two.
- "What is in it for you?" cards: content centred; icons are round outlined buttons, the same style as in "Our team".
- "Our team": the Google Scholar icon comes first, so the homepage and LinkedIn icons are in the same place on every card.
- Form and placeholder pages: same content width (1280 px), header style and page background as the homepage. They were 80 px narrower before (1200 px).
- Fixed on phones: long words no longer push cards wider than the screen; the price in the form no longer breaks over two lines.

## v2.1.0 (18 November 2026): Dutch as default, softer background, illustrations

- **Dutch is the default language.** The Dutch pages are at the site root, the English pages in `en/`.
- **Temporary:** `nl/` now only holds four forwarding pages to the new Dutch addresses, so links shared earlier keep working. **Delete the `nl/` folder (and the `STUB` lines in `tools/i18n.py`) after approval.**
- Page background is a soft grey (`#f7f8f9`) instead of pure white; cards on it are white with a hairline.
- "Clients include" / "Onze klanten" has the same heading style as the other sections.
- The three photo placeholders are replaced by temporary illustrations without faces (`assets/illustration-*.svg`, drawn by `tools/make_illustrations.py`). To be replaced by real photos before launch.
- `tools/build_site.py` now writes its intermediate English pages to `tools/.build/` (not kept in git).

## v2.0.2 (17 November 2026): wording

- Key figure: "10 weeks from intake to final advice" is now "10 weeks from assignment start to final advice" (Dutch: "weken van start opdracht tot eindadvies").

## v2.0.1 (17 November 2026): fixes

- The page no longer grows on wide screens. One size for all desktop screens: the content column is at most 1280 px wide and centred; wider screens get more margin.
- The ten weeks: all red week labels have the same width, text aligned left.

## v2.0.0 (17 November 2026): design update, homepage

Designed for desktop screens of 1920 x 1080 and larger, including ultrawide and 4K. Phones and tablets followed in v2.2.0.

- Header: one line (BRC wordmark, name, menu, contact button, EN / NL). It stays at the top while scrolling and turns light after the first scroll. The faculty and university line moved to just above the headline.
- Language switch: text "EN / NL" instead of flags, on all pages.
- Hero: red runs from the current red to a deeper red, with a fine dot pattern. Headline on two lines; the second line types.
- New row of key figures under the photos (4 students, 10 weeks, 4 starts a year, from EUR 2,000), counting up once.
- Client logos moved up, directly under the key figures.
- "What is in it for you?": icons on the cards, sliding switch between Organisations and Students.
- Example assignments: arrow on each clickable card; "Something else?" is the dark card.
- The ten weeks: timeline that fills while scrolling, with a large week number.
- Costs: grey band with white price cards; no black outline (outline now means "clickable" only).
- Team: compact rows.
- Sections fade in once when they enter the screen. All motion is off for visitors who have "reduce motion" set, and the page works without JavaScript.
- Fixed: "Clients include" heading was 32 px out of line.

## v1.0.0 (17 November 2026): first version

Variant C "Ten weeks", English and Dutch, as described in the handover document of 17 November 2026. Kept in branch `archive/v1.0.0` (commit `b8175fa`).
