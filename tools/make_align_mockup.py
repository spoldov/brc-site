"""TEMPORARY: mock-up of the alignment fixes (bold text never level with plain text in a neighbouring box).

Makes mockups/align.html (Dutch) and mockups/align-en.html (English) from the generated homepages.
The real homepage is not changed. Run from the repository root, after build_site.py and i18n.py:
    python3 tools/make_align_mockup.py
Delete this script and the mockups/ folder once the fixes are accepted (and built into the source) or rejected.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'mockups')
os.makedirs(OUT, exist_ok=True)

CSS = r'''
/* ===== mock-up: alignment fixes ===== */
/* Shared rows (CSS subgrid): boxes side by side share invisible rows, so every heading starts on the same line
   and every plain text starts on the same line, whatever the length of the text. Same technique as the
   "Wat levert het op?" cards. Gaps: the parent's row gap equals the gap inside a box; space between rows of
   boxes comes from a bottom margin on each box. */
@supports (grid-template-rows:subgrid){

  /* 1. "Wat klanten zeggen": quote and newsletter card (two columns above 900 px) */
  @media (min-width:901px){
    .proof{row-gap:1rem}
    .proof > .quote, .page .proof > a.pcard{display:grid; grid-row:span 2; grid-template-rows:subgrid; align-content:start; gap:1rem; padding-top:2.25rem}
    .proof .pcard h3{font-family:Archivo,Arial,sans-serif; font-weight:600; font-size:1.5rem; line-height:1.3}
  }

  /* 2. Example assignments: heading row, text row, link row */
  #products .cards3{row-gap:0.625rem}
  #products .pcard{display:grid; grid-row:span 3; grid-template-rows:subgrid; align-content:start; margin-bottom:0.625rem}
  .pcard-cta{font-weight:600; text-decoration:underline; text-underline-offset:3px; align-self:end}

  /* 2b. Price cards: tier label, price and description each on a shared row (above phone width, where they sit side by side) */
  @media (min-width:721px){
    .costs .cards3{row-gap:0.5rem}
    .costs .price{display:grid; grid-row:span 3; grid-template-rows:subgrid; align-content:start; gap:0.5rem}
  }

  /* 3. Team: name row and role row; icons centred over both (above phone width, where the team is a list) */
  @media (min-width:721px){
    .team{row-gap:0}
    .person{display:grid; grid-row:span 2; grid-template-rows:subgrid; grid-template-columns:1fr auto; column-gap:1rem; row-gap:0; margin-bottom:1rem; align-items:start}
    .person > div:first-child{display:contents}
    .person br{display:none}
    .person > div:first-child > strong{grid-column:1; grid-row:1}
    .person > div:first-child > span{grid-column:1; grid-row:2}
    .person-links{grid-column:2; grid-row:1 / span 2; align-self:center}
  }
  /* tablets (two columns): the icons move under the role, so names have the full card width and do not wrap */
  @media (min-width:721px) and (max-width:1180px){
    .person{grid-row:span 3; grid-template-columns:1fr}
    .person-links{grid-column:1; grid-row:3; align-self:start; margin-top:0.75rem}
  }
}

/* 4. Cost notes: the bold label on its own line above its text */
.covers strong{display:block; margin-bottom:0.25rem}

.mock-badge{position:fixed; left:1rem; bottom:1rem; z-index:99; max-width:calc(100% - 2rem); background:#17181c; color:#fff;
  font:500 0.8125rem/1.5 Inter,system-ui,sans-serif; padding:0.625rem 0.875rem; border-radius:0.75rem; box-shadow:0 8px 24px -8px rgba(0,0,0,.5)}
.mock-badge a{color:#fff; text-decoration:underline; text-underline-offset:2px}
'''

def fix_paths(t, prefix):
    # the mock-ups live in mockups/: links already starting with ../ point to the site root and stay as they are;
    # other relative links get the page's own folder (../ for Dutch, ../en/ for English)
    return re.sub(r'\b(src|href)="(?!https?:|#|mailto:|tel:|/|data:|\.\./)([^"]+)"', lambda m: '%s="%s%s"' % (m.group(1), prefix, m.group(2)), t)

for src, dst, other, label in (('index.html', 'align.html', 'align-en.html', 'English'),
                               (os.path.join('en', 'index.html'), 'align-en.html', 'align.html', 'Nederlands')):
    t = open(os.path.join(ROOT, src), encoding='utf-8').read()
    t = fix_paths(t, '../en/' if src.startswith('en') else '../')
    # dark assignment card: the link moves out of the paragraph onto its own row
    m = re.search(r'(<a class="pcard pcard-dark[^>]*>.*?<p>[^<]*?)\s*<u>([^<]*)</u></p></a>', t, re.S)
    assert m, 'dark card not found'
    t = t.replace(m.group(0), m.group(1) + '</p><span class="pcard-cta">' + m.group(2) + ' →</span></a>')
    cur = '../en/index.html' if src.startswith('en') else '../index.html'
    badge = ('<div class="mock-badge"><b>Mock-up</b>: alignment fixes (quote and newsletter card, example assignments, prices, team, cost notes)<br>'
             '<a href="%s">current site</a> · <a href="%s">%s</a></div>\n' % (cur, other, label))
    assert t.count('</head>') == 1 and t.count('</body>') == 1
    t = t.replace('</head>', '<style>' + CSS + '</style>\n</head>').replace('</body>', badge + '</body>')
    open(os.path.join(OUT, dst), 'w', encoding='utf-8').write(t)
    print('wrote mockups/' + dst)
