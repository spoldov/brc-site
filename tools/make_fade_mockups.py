"""TEMPORARY: three mock-ups of the client carousel fading out where it leaves the content width.

Makes mockups/fade-a.html, fade-b.html and fade-c.html from the generated Dutch homepage (index.html).
The real homepage is not changed. Run from the repository root, after build_site.py and i18n.py:
    python3 tools/make_fade_mockups.py
Delete this script and the mockups/ folder once a variant is chosen (or rejected).
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'mockups')
os.makedirs(OUT, exist_ok=True)
page = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

# The content edge: the homepage content is at most 80rem wide with at least 2rem on each side
# (1.25rem on phones). Everything between the screen edge and this line is "outside the bound".
EDGE = '.brc-car{--edge:max(2rem, (100% - 80rem) / 2)}\n@media (max-width:720px){.brc-car{--edge:1.25rem}}\n'

def mask(stops):
    g = 'linear-gradient(90deg, %s)' % stops
    return '.brc-car{-webkit-mask-image:%s; mask-image:%s}\n' % (g, g)

def linear(f):
    # fully visible inside the content width, fading to nothing over f outside it
    return mask('transparent calc(var(--edge) - {f}), #000 var(--edge), #000 calc(100% - var(--edge)), transparent calc(100% - var(--edge) + {f})'.format(f=f))

def eased(f):
    # same, but with a gentle start and a long tail
    l = ['transparent calc(var(--edge) - {f})', 'rgba(0,0,0,.1) calc(var(--edge) - {f} * .75)',
         'rgba(0,0,0,.35) calc(var(--edge) - {f} * .5)', 'rgba(0,0,0,.75) calc(var(--edge) - {f} * .25)', '#000 var(--edge)']
    r = ['#000 calc(100% - var(--edge))', 'rgba(0,0,0,.75) calc(100% - var(--edge) + {f} * .25)',
         'rgba(0,0,0,.35) calc(100% - var(--edge) + {f} * .5)', 'rgba(0,0,0,.1) calc(100% - var(--edge) + {f} * .75)',
         'transparent calc(100% - var(--edge) + {f})']
    return mask(', '.join(l + r).format(f=f))

VARIANTS = [
    ('a', 'A · soft and quick: fades over 6rem (96 px) outside the content width', linear('6rem')),
    ('b', 'B · tight: fades over 2rem (32 px), almost a clean cut at the content edge', linear('2rem')),
    ('c', 'C · long and gentle: eased fade over 14rem (224 px)', eased('14rem')),
]

def fix_paths(t):
    # the mock-ups live one folder down, so relative links and images need ../
    return re.sub(r'\b(src|href)="(?!https?:|#|mailto:|tel:|/|data:|\.\./)([^"]+)"', r'\1="../\2"', t)

for key, label, css in VARIANTS:
    nav = ' · '.join('<a href="fade-%s.html"%s>%s</a>' % (k, ' aria-current="page"' if k == key else '', k.upper()) for k, _, _ in VARIANTS)
    badge = ('<div class="mock-badge"><b>Mock-up</b> %s<br>%s · <a href="../index.html">current site</a></div>\n' % (label, nav))
    style = ('<style>\n/* mock-up: carousel fade */\n' + EDGE + css +
             '.mock-badge{position:fixed; left:1rem; bottom:1rem; z-index:99; max-width:calc(100% - 2rem); background:#17181c; color:#fff; '
             'font:500 0.8125rem/1.5 Inter,system-ui,sans-serif; padding:0.625rem 0.875rem; border-radius:0.75rem; box-shadow:0 8px 24px -8px rgba(0,0,0,.5)}\n'
             '.mock-badge a{color:#fff; text-decoration:underline; text-underline-offset:2px}\n'
             '.mock-badge a[aria-current]{color:#ff8fa5; font-weight:700}\n</style>\n</head>')
    t = fix_paths(page)
    assert t.count('</head>') == 1 and t.count('</body>') == 1
    t = t.replace('</head>', style).replace('</body>', badge + '</body>')
    open(os.path.join(OUT, 'fade-%s.html' % key), 'w', encoding='utf-8').write(t)
    print('wrote mockups/fade-%s.html' % key)
