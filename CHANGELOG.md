# Changelog

Each finished version is kept as a branch named `archive/vX.Y.Z`. Archive branches are never changed afterwards.
To look at an old version on GitHub: open the repository, click the branch button (top left, above the file list) and choose the archive branch.

## v2.9.0 (19 November 2026): larger BRC logo, centred on the header text

- BRC in the header is larger (26 px, was 23; phones and tablets 22 px, was 20) and centred on the header text: the middle of its capitals is level with the middle of the name's capitals (within the 0.5 px the browser can place it). The rest of the header still shares one baseline. Set by `--logo-drop` on `.logo b` / `.slogo b`, measured from rendered pixels.
- Phones: the header never wraps. Below 381 px only BRC and the menu button are shown (the name was hidden below 351 px before). **Correction:** at 360 px the header already wrapped onto two lines since v2.7.0, hiding BRC above the bar; this was missed because that width was not in the header check.
- New check script `tools/checks/design_check.py` for the owner's layout rules (see `tools/README.md`).
- Version v2.8.0 is archived as branch `archive/v2.8.0`.

## v2.8.0 (19 November 2026): bold never level with plain text; carousel ends at the content edge

- **Rule applied across the homepage:** bold text is never level with plain text in a neighbouring box. Measured at 11 widths (390 to 3440 px) in Dutch and English: 0 cases (v2.7.0 had 26). Done with shared rows (CSS subgrid), in one block at the end of the homepage `<style>`:
  - "Wat klanten zeggen": quote and newsletter card share rows; the card heading now has the quote's type (Archivo 24 px, semi-bold);
  - example assignments: heading, text and link rows; in the dark card "Opdracht indienen →" is on its own row instead of inside the paragraph;
  - price cards: tier label, price and description rows;
  - team: name and role rows; on tablets (721 to 1180 px) the icons sit under the role so names do not wrap;
  - cost notes: each bold label on its own line above its text.
- **Client carousel:** back to fully invisible at the content edge, fading in over 6rem inside the column (as v2.6.0). The centred fade of v2.7.0 showed logos up to 3rem outside the column. Pixel check: nothing is drawn outside the column.
- **Example assignments:** the intro sentence ("Onze opdrachten eindigen met …") is removed; the heading uses the same heading block as the other sections. Unused styles `.lead`, `.sec-intro` and the old link style removed.
- The alignment mock-up (`mockups/`, `tools/make_align_mockup.py`) is removed.
- Version v2.7.0 is archived as branch `archive/v2.7.0`.

## Mock-up (19 November 2026, no change to the site)

- **Temporary:** `mockups/align.html` (Dutch) and `mockups/align-en.html` (English) show alignment fixes so that bold text is never level with plain text in a neighbouring box: shared rows (CSS subgrid) for the quote and newsletter card, the example assignments (the "Opdracht indienen" link on its own row), the price cards and the team (icons under the role on tablets); cost-note labels on their own line. Made by `tools/make_align_mockup.py` from the homepages. Delete both once the fixes are accepted or rejected.

## v2.7.0 (18 November 2026): plain BRC wordmark, aligned header, client placeholders, newsletter

- **Header:** the wordmark is plain "BRC" text, without the crown. Every text item in the header (BRC, the name, the menu links, the label of the contact button, NL / EN) now sits on one baseline, on every page and screen size; measured in the browser. Before, the form and placeholder pages had four different baselines. The crown version is kept as a fallback (files in `assets/`, full header on branch `archive/v2.6.0`).
- **Phones, form and placeholder pages:** the "Back to the homepage" link is hidden (BRC links home), so the header fits on one line instead of two. NL and EN in the language switch are now the same size there (EN was 1 px larger).
- **Client carousel:** the fade is centred on the content edge (half visible on the line, 3rem out, 3rem in), so the strip looks exactly as wide as the boxes. The logos are replaced by placeholders reading "Approvals" / "Pending" (Dutch: "Goedkeuring" / "In afwachting"), six per row, until each client has renewed permission and the selection is made. The four logo files stay in `assets/`. Animation slowed to 168 s so the speed is unchanged.
- **Newsletter:**
  - new placeholder page `newsletter.html` (English `en/newsletter.html`);
  - footer of every page: "Blijf op de hoogte: meld u aan voor onze nieuwsbrief" / "Stay up to date: sign up for our newsletter";
  - in "Wat klanten zeggen", the case-description box is replaced by a card "Lees onze nieuwsbrieven voor meer testimonials" with "Laatste nieuws: [PLACEHOLDER]", linking to the newsletter page.
- Removed with the case box: its style (`.meta`) and four Dutch translations. `tools/checks/render_check.py` now also checks the newsletter pages.
- Version v2.6.0 is archived as branch `archive/v2.6.0`.

## v2.6.0 (18 November 2026): client carousel fades at the content edge

- The client carousel ("Onze klanten" / "Clients include") is now masked to the content column: logos are fully invisible at the left and right edge of the content (the same line as the headings and boxes) and fully visible 6rem (96 px) further in; on phones the fade is 3rem. Before, the carousel ran the full screen width and only faded at the screen edges. Based on mock-up A, with the fade moved inside the column at the owner's request.
- Settings: `--edge` and `--fade` on `.brc-car` in `tools/src/C-TenWeeks.dc.html` (phone values in the 720 px block).
- The temporary mock-ups (`mockups/`, `tools/make_fade_mockups.py`) are removed.
- To go back to the full-width carousel: restore the `.brc-car` rule from branch `archive/v2.5.2`.
- Version v2.5.2 is archived as branch `archive/v2.5.2`.

## v2.5.2 (18 November 2026): footer line, clean-up, carousel fade mock-ups

- AI-disclosure line in every footer: "Built with Claude Fable 5.2 and Opus 5.5" (Dutch: "Gemaakt met Claude Fable 5.2 en Opus 5.5").
- Clean-up of leftovers from earlier versions; the pages look exactly the same (checked by comparing the generated pages before and after):
  - removed the unused colour variable `--red-ink` from the homepage styling;
  - removed four Dutch translations of text that is no longer on the site (the three `[PHOTO: …]` placeholders replaced by the illustrations, and "Read the case");
  - `tools/i18n.py`: the language-switch code still used names from when the switch was a flag (`flag`, `NLFLAG`, `UKFLAG`, `FLAGMARK`); renamed, output unchanged;
  - `tools/README.md`: the instructions for inserting a homepage photo described the old placeholder markup; updated.
  - Checked and kept: all 18 files in `assets/`, every CSS class, id and animation (all in use), and the placeholders (`[LOGO]` client boxes, empty profile links, case box, form privacy link).
- **Temporary:** three mock-ups of the client carousel fading out where it leaves the content width, in `mockups/fade-a.html`, `fade-b.html` and `fade-c.html` (made by `tools/make_fade_mockups.py` from the Dutch homepage; the real homepage is unchanged). Delete the folder and the script once a variant is chosen or rejected.
- Version v2.5.1 is archived as branch `archive/v2.5.1`.

## v2.5.1 (18 November 2026): "What is in it for you?" cards

- The cards now line up line by line: in every row of cards, all headings start at the same height and all texts start at the same height, on every screen size, in both languages and for both Organisations and Students. Made with CSS subgrid (in `.cards4`); browsers without subgrid show the previous layout.
- Organisations, fourth card: "International reach" is now "Excellent students" with the text "Both Dutch and international students are carefully selected." (Dutch: "Excellente studenten" / "Nederlandse én internationale studenten worden zorgvuldig geselecteerd."). The globe icon is replaced by a star.
- Dutch, "Professionele begeleiding": "advieservaring" is now "consultancy ervaring", at the owner's request (standard spelling would be "consultancy-ervaring").
- Version v2.5.0 is archived as branch `archive/v2.5.0`.

## Tools (18 November 2026, no change to the site)

- Added `tools/checks/render_check.py`: renders every page at phone, tablet and desktop sizes and checks for overflow, script errors, broken images and dead links. See `tools/README.md`.

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
