"""Renders every page at phone, tablet and desktop sizes and checks for layout problems.

What it checks on each page and size:
  - nothing is wider than the screen (no sideways scrolling)
  - no script errors
  - no broken images
  - no links to pages or files that do not exist in the repo
  - on the two homepages: every typed headline phrase fits on one line, and the headline does not change height

Needs Playwright and Chrome (python3 -m pip install playwright). Nothing else in tools/ needs these.
Run from the repository root, after build_site.py and i18n.py:

  python3 tools/checks/render_check.py                  check only, prints one line per page and size
  python3 tools/checks/render_check.py --shots          also saves full-page screenshots in tools/checks/out/
  python3 tools/checks/render_check.py --chrome PATH    use the Chrome at PATH instead of Playwright's own browser

The screenshots folder is not kept in git. The script ends with exit code 1 when it found a problem.
"""
import asyncio, os, re, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'tools', 'checks', 'out')
PAGES = ['index.html', 'submit.html', 'product.html', 'students.html', 'newsletter.html',
         'en/index.html', 'en/submit.html', 'en/product.html', 'en/students.html', 'en/newsletter.html']
# (name, width, height). Phones and the small tablet are rendered as touch devices.
SIZES = [('phone-360', 360, 740), ('phone-390', 390, 844), ('phone-430', 430, 932),
         ('tablet-768', 768, 1024), ('tablet-1024', 1024, 768),
         ('laptop-1366', 1366, 768), ('desktop-1920', 1920, 1080), ('wide-3440', 3440, 1440)]

TOO_WIDE = """() => {
  const w = document.documentElement.clientWidth;
  const sideways = document.documentElement.scrollWidth - w;
  // elements that stick out on the right; the logo carousel and the picture strip scroll on purpose
  const out = [...document.querySelectorAll('body *')].filter(e =>
      !e.closest('.brc-car,.photos') && getComputedStyle(e).position !== 'fixed' &&
      e.getBoundingClientRect().right > w + 1).slice(0, 3).map(e => e.className || e.tagName);
  return [sideways, out];
}"""
HEADLINE = """(phrases) => {
  const t = document.getElementById('typed'), line = t.parentElement, h1 = document.querySelector('h1');
  const first = t.textContent, bad = [], heights = new Set();
  for (const p of phrases.concat([''])) {
    t.textContent = p;
    if (line.scrollWidth > line.clientWidth) bad.push(p);
    heights.add(Math.round(h1.getBoundingClientRect().height));
  }
  t.textContent = first;
  return [bad, [...heights]];
}"""

def phrases_in(page_html):
    m = re.search(r"var phrases = \[(.*?)\];", page_html)
    return re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(1)) if m else []

async def main():
    shots = '--shots' in sys.argv
    chrome = sys.argv[sys.argv.index('--chrome') + 1] if '--chrome' in sys.argv else None
    if shots: os.makedirs(OUT, exist_ok=True)
    problems = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(**({'executable_path': chrome} if chrome else {}), args=['--no-sandbox'])
        for page_path in PAGES:
            file_path = os.path.join(ROOT, page_path)
            source = open(file_path, encoding='utf-8').read()
            for name, w, h in SIZES:
                touch = w < 1000
                ctx = await browser.new_context(viewport={'width': w, 'height': h}, has_touch=touch, is_mobile=touch)
                pg = await ctx.new_page(); errors = []
                pg.on('pageerror', lambda e: errors.append(str(e)))
                await pg.goto('file://' + file_path, wait_until='networkidle'); await pg.wait_for_timeout(400)
                # scroll through the page once so everything that fades in on scroll is visible
                height = await pg.evaluate('document.documentElement.scrollHeight')
                for y in range(0, height, 350):
                    await pg.evaluate('window.scrollTo(0, %d)' % y); await pg.wait_for_timeout(40)
                await pg.evaluate('window.scrollTo(0, 0)'); await pg.wait_for_timeout(400)
                found = []
                sideways, sticking_out = await pg.evaluate(TOO_WIDE)
                if sideways > 0 or sticking_out: found.append('wider than the screen by %d px: %s' % (sideways, sticking_out))
                if errors: found.append('script errors: %s' % errors[:2])
                broken = await pg.evaluate("[...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src'))")
                if broken: found.append('broken images: %s' % broken)
                links = await pg.evaluate("[...document.querySelectorAll('a[href],link[rel~=icon],link[rel=apple-touch-icon]')].map(a => a.getAttribute('href'))")
                base = os.path.dirname(file_path)
                dead = sorted({l for l in links if not re.match(r'^(https?:|mailto:|#)', l)
                               and not os.path.exists(os.path.normpath(os.path.join(base, l.split('#')[0])))})
                if dead: found.append('links to missing files: %s' % dead)
                if page_path.endswith('index.html') and phrases_in(source):
                    too_long, heights = await pg.evaluate(HEADLINE, phrases_in(source))
                    if too_long: found.append('headline phrases that do not fit: %s' % too_long)
                    if len(heights) > 1: found.append('headline changes height while typing: %s' % heights)
                if shots:
                    await pg.screenshot(path=os.path.join(OUT, '%s--%s.png' % (page_path.replace('/', '_').replace('.html', ''), name)), full_page=True)
                problems += len(found)
                print('%-18s %-13s %s' % (page_path, name, 'ok' if not found else 'PROBLEM: ' + '; '.join(found)))
                await ctx.close()
        await browser.close()
    print('\n%d problem(s) found.' % problems if problems else '\nNo problems found.')
    if shots: print('Screenshots are in tools/checks/out/')
    sys.exit(1 if problems else 0)

asyncio.run(main())
