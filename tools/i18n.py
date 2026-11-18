"""Step 2 of 2: add the language switch and AI-disclosure line; write the Dutch pages to the site root
(Dutch is the default language) and the English pages to en/.

Run from the repository root, after tools/build_site.py:  python3 tools/i18n.py
Dutch wording lives in tools/nl.json (English text -> Dutch text).
Any English text without a translation is printed under "untranslated".
"""
import re,json,os,html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=ROOT
D=json.load(open(os.path.join(ROOT,'tools','nl.json'),encoding='utf-8'))
def langswitch(href,code,label,pair):
    # Language switch as text: the current language in plain text, the other one as a link.
    cur,other=pair
    return '<span style="display: inline-flex; align-items: baseline; gap: 0.4em; font-size: 14px; font-weight: 600; letter-spacing: 0.04em"><span>%s</span><span aria-hidden="true" style="opacity: 0.5">/</span><a href="%s" lang="%s" hreflang="%s" aria-label="%s" title="%s" style="color: inherit; opacity: 0.8; text-decoration: underline; text-underline-offset: 3px; padding: 10px 0">%s</a></span>'%(cur,href,code,code,label,label,other)
SWITCH_ON_EN=('EN','NL')  # shown on the English pages
SWITCH_ON_NL=('NL','EN')  # shown on the Dutch pages
SWITCHMARK='<!--LANGSWITCH-->'
def sub1(s,a,b):
    assert s.count(a)==1,(a[:70],s.count(a)); return s.replace(a,b)
def prep(name,t):
    # language switch slot
    if name=='index.html':
        i=t.index('</nav>'); t=t[:i]+SWITCHMARK+'\n'+t[i:]
    else:
        m=re.search(r'<a href="index\.html" style="color: #ffffff; font-weight: 600; font-size: 16px; padding: 12px 0">[^<]*</a>',t)
        t=t.replace(m.group(0),'<div style="display: flex; align-items: baseline; gap: 20px">'+m.group(0)+SWITCHMARK+'</div>')
    # AI-disclosure line in the footer of every page
    t=sub1(t,'is not part of rug.nl.</span>','is not part of rug.nl.<span style="display: block; margin-top: 6px">Built with Claude Fable 5.2 and Opus 5.5</span></span>')
    return t
# ---- browser-tab icon and link preview (what LinkedIn, WhatsApp, Teams show when the link is shared)
# Link previews need a full web address. CHANGE THIS when the site moves to its final address.
SITE_URL='https://spoldov.github.io/brc-site/'
DESC={'en':'Hire our student consultants for business advice within ten weeks. A course of the Faculty of Economics and Business, University of Groningen.',
      'nl':'Bedrijfsadvies van begeleide studentconsultants in tien weken. Een vak van de Faculteit Economie en Bedrijfskunde, Rijksuniversiteit Groningen.'}
def head_tags(page_html,lang,path):
    title=html.escape(html.unescape(re.search(r'<title>(.*?)</title>',page_html,re.S).group(1)),quote=True)
    d=html.escape(DESC[lang],quote=True); url=SITE_URL+('' if path.endswith('index.html') and '/' not in path else path)
    if path=='en/index.html': url=SITE_URL+'en/'
    return '\n'.join(['<meta name="description" content="%s">'%d,
      '<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">',
      '<link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192.png">',
      '<link rel="apple-touch-icon" href="assets/favicon-180.png">',
      '<meta property="og:type" content="website">',
      '<meta property="og:site_name" content="BRC · Business Research &amp; Consulting">',
      '<meta property="og:title" content="%s">'%title,
      '<meta property="og:description" content="%s">'%d,
      '<meta property="og:url" content="%s">'%url,
      '<meta property="og:image" content="%sassets/share-%s.jpg">'%(SITE_URL,lang),
      '<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">',
      '<meta property="og:locale" content="%s">'%('nl_NL' if lang=='nl' else 'en_GB'),
      '<meta name="twitter:card" content="summary_large_image">'])+'\n</head>'
def tr_text(t,miss):
    def f(m):
        raw=m.group(1);s=raw.strip()
        if not s: return m.group(0)
        if s in D: return '>'+raw.replace(s,D[s])+'<'
        k=s.replace('&','&amp;')
        if '&amp;' not in s and k in D: return '>'+raw.replace(s,D[k])+'<'
        if re.search(r'[A-Za-z]{3}',s): miss.add(s)
        return m.group(0)
    return re.sub(r'>([^<>]+)<',f,t)
def tr_attr(t,miss):
    def f(m):
        k,v=m.group(1),m.group(2)
        if v in D: v=D[v]
        elif v.startswith('Homepage of '): v='Homepage van '+v[12:]
        elif v.startswith('LinkedIn profile of '): v='LinkedIn-profiel van '+v[20:]
        elif v.startswith('Google Scholar profile of '): v='Google Scholar-profiel van '+v[26:]
        elif re.search(r'[a-z]{3}',v) and v not in ('Nederlands','English'): miss.add('@'+v)
        return '%s="%s"'%(k,v)
    return re.sub(r'\b(aria-label|title|alt)="([^"]*)"',f,t)
def tr_js(js):
    def f(m):
        v=m.group(1)
        return "'"+D[v].replace("'","\\'")+"'" if v in D else m.group(0)
    return re.sub(r"'([^'\n]*)'",f,js)
BUILD=os.path.join(ROOT,'tools','.build')   # English pages written by build_site.py
os.makedirs(OUT+'/en',exist_ok=True); os.makedirs(OUT+'/nl',exist_ok=True)
# TEMPORARY forwarding pages: Dutch used to live in nl/. Delete the nl/ folder (and STUB below) once the site is approved.
STUB='<!doctype html>\n<!-- TEMPORARY forwarding page. Delete the whole nl/ folder after approval. -->\n<html lang="nl">\n<head>\n<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">\n<title>BRC</title>\n<link rel="canonical" href="../%s">\n<meta http-equiv="refresh" content="0; url=../%s">\n</head>\n<body>\n<p><a href="../%s">Deze pagina is verhuisd. Klik hier als u niet automatisch wordt doorgestuurd.</a></p>\n</body>\n</html>\n'
miss=set()
for name in ['index.html','submit.html','product.html','students.html','newsletter.html']:
    t=prep(name,open(BUILD+'/'+name).read())
    alt='<link rel="alternate" hreflang="nl" href="%s">\n<link rel="alternate" hreflang="en" href="%s">\n<link rel="alternate" hreflang="x-default" href="%s">\n</head>'
    # English: in en/
    en=t.replace(SWITCHMARK,langswitch('../'+name,'nl','Nederlands',SWITCH_ON_EN))
    en=sub1(en,'</head>',head_tags(en,'en','en/'+name))
    en=en.replace('"assets/','"../assets/')
    en=sub1(en,'</head>',alt%('../'+name,name,'../'+name))
    # Dutch: the default, at the site root
    parts=re.split(r'(<script>.*?</script>|<style>.*?</style>)',t,flags=re.S)
    for i,p in enumerate(parts):
        if p.startswith('<script>'): parts[i]=tr_js(p)
        elif p.startswith('<style>'): pass
        else: parts[i]=tr_attr(tr_text(p,miss),miss)
    nl=''.join(parts)
    nl=nl.replace(SWITCHMARK,langswitch('en/'+name,'en','English',SWITCH_ON_NL))
    nl=sub1(nl,'<html lang="en">','<html lang="nl">')
    nl=nl.replace('rug-logo-en.svg','rug-logo-nl.svg')
    nl=sub1(nl,'</head>',head_tags(nl,'nl',name))
    nl=re.sub(r'€(\d),(\d{3})',r'€ \1.\2',nl)
    nl=sub1(nl,'</head>',alt%(name,'en/'+name,name))
    open(OUT+'/'+name,'w').write(nl); open(OUT+'/en/'+name,'w').write(en)
    if name!='newsletter.html': open(OUT+'/nl/'+name,'w').write(STUB%(name,name,name))  # newsletter never lived in nl/
print('untranslated:');[print('  ',m) for m in sorted(miss)]
