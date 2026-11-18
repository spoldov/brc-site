"""Checks the owner's layout rules in a real browser, on the generated pages.

  1. Bold never level with plain text: in every row of side-by-side boxes on the homepages, no bold line
     overlaps a plain (non-bold) line in a neighbouring box. (Bold and plain within one box are fine.)
  2. Header baseline: every text item in the header (name, menu links, contact-button label, NL / EN,
     back link) sits on one shared baseline.
  3. BRC logo centred: the middle of the BRC capitals is level with the middle of the name's capitals
     (or, where the name is hidden, of the other header text) within 1 px, measured from rendered pixels.
  4. Header on one line: on phones and tablets the header never wraps, BRC and the menu button stay inside
     the bar and the name never runs into the menu button.

Needs Playwright, Pillow and Chrome, like render_check.py. Run from the repository root, after build_site.py and i18n.py:

  python3 tools/checks/design_check.py                  all checks, Dutch and English, at 11 widths
  python3 tools/checks/design_check.py --chrome PATH    use the Chrome at PATH instead of Playwright's own browser

Prints each problem found and ends with exit code 1 if there was one.
"""
import io, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOMES = ['index.html', 'en/index.html']
SUBS = ['submit.html', 'product.html', 'students.html', 'newsletter.html',
        'en/submit.html', 'en/product.html', 'en/students.html', 'en/newsletter.html']
WIDTHS = [360, 390, 721, 768, 900, 1024, 1180, 1220, 1280, 1920, 3440]

# 1. bold/plain clashes between neighbouring boxes
JS_CLASH = r"""() => {
 const found = [];
 document.querySelectorAll('.proof,.cards3,.cards4,.team,.stats,.covers').forEach(c => {
  if (!c.offsetParent) return;
  const rows = {};
  [...c.children].filter(k => k.offsetParent && k.getBoundingClientRect().height > 0)
    .forEach(k => { const t = Math.round(k.getBoundingClientRect().top); (rows[t] = rows[t] || []).push(k); });
  Object.values(rows).forEach(group => {
   if (group.length < 2) return;
   const lines = group.map(k => { const out = []; const w = document.createTreeWalker(k, NodeFilter.SHOW_TEXT); let n;
     while (n = w.nextNode()) { if (!n.textContent.trim() || !n.parentElement.offsetParent) continue;
       const bold = parseInt(getComputedStyle(n.parentElement).fontWeight) >= 600;
       const r = document.createRange(); r.selectNodeContents(n);
       for (const q of r.getClientRects()) if (q.height > 0) out.push({bold, top: q.top, bot: q.bottom, t: n.textContent.trim().slice(0, 30)}); }
     return out; });
   for (let i = 0; i < lines.length; i++) for (let j = 0; j < lines.length; j++) if (i !== j)
     for (const a of lines[i]) if (a.bold) for (const b of lines[j]) if (!b.bold && Math.min(a.bot, b.bot) - Math.max(a.top, b.top) > 2)
       found.push(c.className.split(' ')[0] + ': "' + a.t + '" level with "' + b.t + '"');
  });
 });
 return [...new Set(found)];
}"""

# 2. baselines: a zero-height inline box placed after the last text of an item sits on its baseline
JS_BASELINES = r"""() => {
 const hdr = document.querySelector('.hdr, .shdr'), out = [];
 const probe = (el, label) => {
  if (!el || el.getBoundingClientRect().width === 0) return;
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let t = null, n;
  while (n = w.nextNode()) if (n.textContent.trim()) t = n;
  if (!t) return;
  const s = document.createElement('span'); s.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
  const wr = document.createElement('span'); t.parentNode.insertBefore(wr, t); wr.appendChild(t); wr.appendChild(s);
  out.push([label, Math.round(s.getBoundingClientRect().top * 10) / 10]);
  wr.parentNode.insertBefore(t, wr); wr.remove();
 };
 hdr.querySelectorAll('.brand-name, .sname, .nav-link, .nav-cta, a[hreflang], header > div > a:not([hreflang])').forEach(e => probe(e, e.textContent.trim().slice(0, 20)));
 hdr.querySelectorAll('a[hreflang]').forEach(a => probe(a.parentElement.firstElementChild, 'current language'));
 return out;
}"""

# 3. first-letter boxes for the pixel measurement of capital heights
JS_FIRST = r"""(sel) => { const el = document.querySelector(sel); if (!el || el.getBoundingClientRect().width === 0) return null;
 const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n = w.nextNode(); while (n && !n.textContent.trim()) n = w.nextNode();
 const i = n.textContent.search(/\S/); const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1);
 const q = r.getBoundingClientRect(); return [q.left, q.top, q.right, q.bottom]; }"""

# 4. header fits on one line
JS_FIT = r"""() => { const h = document.querySelector('.hdr').getBoundingClientRect(), l = document.querySelector('.logo b').getBoundingClientRect(),
 m = document.querySelector('.menu-btn').getBoundingClientRect(), n = document.querySelector('.brand-name').getBoundingClientRect();
 return {inBar: l.top >= h.top && l.bottom <= h.bottom && (m.width === 0 || (m.top >= h.top && m.bottom <= h.bottom)),
         overlap: n.width > 0 && m.width > 0 && n.right > m.left}; }"""

def cap_centre(img, box, scale):
    """Vertical middle of the letter pixels inside box (white or near-black text on any background)."""
    x0, y0, x1, y1 = [int(v * scale) for v in box]
    ys = [y for y in range(max(0, y0 - 4), y1 + 4)
          if any(min(img.getpixel((x, y))) > 215 or max(img.getpixel((x, y))) < 90 for x in range(x0, x1))]
    return (min(ys) + max(ys)) / 2 / scale if ys else None

def main():
    chrome = sys.argv[sys.argv.index('--chrome') + 1] if '--chrome' in sys.argv else None
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch(**({'executable_path': chrome} if chrome else {}), args=['--no-sandbox'])
        for page_path in HOMES + SUBS:
            url = 'file://' + os.path.join(ROOT, page_path)
            for w in WIDTHS:
                page = browser.new_page(viewport={'width': w, 'height': 900}, device_scale_factor=3)
                page.goto(url); page.wait_for_timeout(400)
                where = '%s at %d px' % (page_path, w)
                # header checks
                bl = page.evaluate(JS_BASELINES)
                vals = [v for _, v in bl]
                if vals and max(vals) - min(vals) > 0.6:
                    problems.append('%s: header text not on one baseline: %s' % (where, bl))
                img = Image.open(io.BytesIO(page.screenshot(clip={'x': 0, 'y': 0, 'width': w, 'height': 80}))).convert('RGB')
                logo = page.evaluate(JS_FIRST, '.logo b, .slogo b')
                ref = page.evaluate(JS_FIRST, '.brand-name, .sname') or page.evaluate(JS_FIRST, 'header a[hreflang]')
                if logo and ref:
                    a, b = cap_centre(img, logo, 3), cap_centre(img, ref, 3)
                    if a is not None and b is not None and abs(a - b) > 1:
                        problems.append('%s: BRC not centred on the header text (%.1f px off)' % (where, a - b))
                if page_path in HOMES:
                    if w <= 1180:
                        fit = page.evaluate(JS_FIT)
                        if not fit['inBar'] or fit['overlap']:
                            problems.append('%s: header does not fit on one line' % where)
                    # bold/plain rule, both audiences
                    for k in (0, 1):
                        page.locator('#switch button').nth(k).click(); page.wait_for_timeout(300)
                        for c in page.evaluate(JS_CLASH):
                            problems.append('%s (%s): %s' % (where, ('organisations', 'students')[k], c))
                page.close()
        browser.close()
    for pr in sorted(set(problems)):
        print(pr)
    print('No problems found.' if not problems else '%d problem(s).' % len(set(problems)))
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
