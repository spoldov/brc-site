# Working on the BRC website

Read the latest handover document in the claude.ai Project "BRC website" and `CHANGELOG.md` before changing anything. The owner's rules there apply; the most important ones are repeated here because they apply to every change.

## Alignment (the owner's standing rule)

The owner wants a calm, simple page that is easy on the eyes. Everything that sits next to or above something else is aligned by default, without being asked:

- Text on one line shares a baseline (header items, the timeline label and its text, side-by-side captions).
- A box, dot, icon or logo next to text is centred on that text: on its first line when the text runs over several lines.
- Stacked items share a left edge (or are all centred, where a block is centred).
- Boxes have equal space left and right of their content, and equal top and bottom where they hold one line. Exception: boxes stacked in a column (like the timeline labels) share one width, the widest content plus equal space, so their right edges line up too; shorter content then gets more space on the right.
- Text with the same role in neighbouring boxes has the same size and weight and starts on the same line; bold text is never level with plain text in a neighbouring box.
- Organic differences are fine only when the content causes them (different text lengths giving different box widths or line counts), never as a side effect of styling.
- Aim for within about half a pixel where the browser allows; do not add complexity to chase sub-pixel differences.
- When adding or changing anything, check its alignment against its neighbours, measure in the browser rather than judge by eye (`tools/checks/design_check.py` covers part of this), and fix it or flag it.

## How to work

- Edit the sources in `tools/`, never the generated HTML; see `tools/README.md`. Regenerate with `python3 tools/build_site.py`, then `python3 tools/i18n.py`.
- Before changing a finished version, push it as branch `archive/vX.Y.Z`; add a `CHANGELOG.md` entry for every version.
- Run `tools/checks/render_check.py` and `tools/checks/design_check.py` once at the end of a change, not after every step.
- Be direct. When the owner has misread an explanation, say so plainly. State what is unverified.
