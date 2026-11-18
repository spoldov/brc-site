"""Makes the browser-tab icons and the link-preview images in assets/.

Only needed when the headline, the red or the wordmark changes. Unlike the other two scripts this one
needs a browser: it uses Playwright with Chrome (python3 -m pip install playwright).
Run from the repository root:  python3 tools/make_share_images.py [path-to-chrome]
The pictures are re-saved from their pixels only, so they carry no metadata.
"""
import asyncio, io, os, sys
from playwright.async_api import async_playwright
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A=os.path.join(ROOT,'assets')
FONTS='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&family=Inter:wght@400;500;600&display=swap">'
RED='radial-gradient(70rem 36rem at 105% 115%, rgba(60,0,14,.55), transparent 62%), linear-gradient(120deg, #dc002d 0%, #cf002a 45%, #a8001f 100%)'
TEXT={'nl':('Faculteit Economie en Bedrijfskunde · Rijksuniversiteit Groningen','Echte Vragen,','Echte Consultants.','Bedrijfsadvies van begeleide studentconsultants in tien weken.'),
      'en':('Faculty of Economics and Business · University of Groningen','Real Questions,','Real Consultants.','Hire our student consultants for business advice within ten weeks.')}
def share(lang):
    eyebrow,l1,l2,sub=TEXT[lang]
    return '''<!doctype html><html><head><meta charset="utf-8">%s<style>
body{margin:0;width:1200px;height:630px;background:%s;color:#fff;font-family:Inter,Arial,sans-serif;position:relative;overflow:hidden}
body:before{content:"";position:absolute;inset:0;background:radial-gradient(rgba(255,255,255,.2) 1.3px, transparent 1.9px) 0 0/30px 30px;-webkit-mask-image:linear-gradient(100deg, transparent 40%%, #000 100%%)}
.in{position:absolute;inset:0;padding:64px 72px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:20px;font-size:24px;font-weight:600}
.brand b{font-family:Archivo,Arial,sans-serif;font-stretch:115%%;font-weight:800;font-size:46px;letter-spacing:-0.02em;line-height:1}
.eye{margin-top:auto;font-size:19px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
h1{margin:20px 0 26px;font-family:Archivo,Arial,sans-serif;font-stretch:112%%;font-weight:800;font-size:100px;line-height:.98;letter-spacing:-0.03em;white-space:nowrap}
p{margin:0;font-size:29px}
</style></head><body><div class="in"><div class="brand"><b>BRC</b><span>Business Research &amp; Consulting</span></div>
<div class="eye">%s</div><h1>%s<br>%s</h1><p>%s</p></div></body></html>'''%(FONTS,RED,eyebrow,l1,l2,sub)
ICON='''<!doctype html><html><head><meta charset="utf-8">%s<style>
body{margin:0;width:512px;height:512px;background:transparent}
div{width:512px;height:512px;border-radius:%%s;background:linear-gradient(135deg,#dc002d,#b80026);display:flex;align-items:center;justify-content:center;color:#fff;font-family:Archivo,Arial,sans-serif;font-stretch:100%%%%;font-weight:800;font-size:212px;letter-spacing:-0.03em}
</style></head><body><div>BRC</div></body></html>'''%FONTS
def clean(png_bytes,mode):
    im=Image.open(io.BytesIO(png_bytes)).convert(mode); out=Image.new(mode,im.size); out.paste(im); return out
async def main():
    chrome=sys.argv[1] if len(sys.argv)>1 else None
    async with async_playwright() as p:
        b=await p.chromium.launch(**({'executable_path':chrome} if chrome else {}),args=['--no-sandbox'])
        for lang in ('nl','en'):
            pg=await b.new_page(viewport={'width':1200,'height':630}); await pg.set_content(share(lang),wait_until='networkidle'); await pg.wait_for_timeout(400)
            clean(await pg.screenshot(),'RGB').save(os.path.join(A,'share-%s.jpg'%lang),'JPEG',quality=88,optimize=True); await pg.close()
        for radius,sizes in (('112px',(32,192)),('0',(180,))):
            pg=await b.new_page(viewport={'width':512,'height':512}); await pg.set_content(ICON%radius,wait_until='networkidle'); await pg.wait_for_timeout(400)
            im=clean(await pg.screenshot(omit_background=True),'RGBA'); await pg.close()
            for s in sizes: im.resize((s,s),Image.LANCZOS).save(os.path.join(A,'favicon-%d.png'%s),optimize=True)
        await b.close()
asyncio.run(main())
