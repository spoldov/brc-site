"""Step 2 of 2: add the language switch and AI-disclosure line, and write the Dutch pages to nl/.

Run from the repository root, after tools/build_site.py:  python3 tools/i18n.py
Dutch wording lives in tools/nl.json (English text -> Dutch text).
Any English text without a translation is printed under "untranslated".
"""
import re,json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=ROOT
D=json.load(open(os.path.join(ROOT,'tools','nl.json'),encoding='utf-8'))
def flag(href,code,label,svg):
    # Language switch as text: the current language in plain text, the other one as a link.
    cur,other=svg
    return '<span style="display: inline-flex; align-items: center; gap: 0.4em; font-size: 14px; font-weight: 600; letter-spacing: 0.04em"><span>%s</span><span aria-hidden="true" style="opacity: 0.5">/</span><a href="%s" lang="%s" hreflang="%s" aria-label="%s" title="%s" style="color: inherit; opacity: 0.8; text-decoration: underline; text-underline-offset: 3px; padding: 10px 0">%s</a></span>'%(cur,href,code,code,label,label,other)
NLFLAG=('EN','NL')  # shown on the English pages
UKFLAG=('NL','EN')  # shown on the Dutch pages
FLAGMARK='<!--LANGSWITCH-->'
def sub1(s,a,b):
    assert s.count(a)==1,(a[:70],s.count(a)); return s.replace(a,b)
def prep(name,t):
    # language switch slot
    if name=='index.html':
        i=t.index('</nav>'); t=t[:i]+FLAGMARK+'\n'+t[i:]
        t=sub1(t,'is not part of rug.nl.</span>','is not part of rug.nl.<span style="display: block; margin-top: 6px">Built with Claude Fable 5.2</span></span>')
    else:
        m=re.search(r'<a href="index\.html" style="color: #ffffff; font-weight: 600; font-size: 16px; padding: 12px 0">[^<]*</a>',t)
        t=t.replace(m.group(0),'<div style="display: flex; align-items: center; gap: 20px">'+m.group(0)+FLAGMARK+'</div>')
    return t
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
        elif v.startswith('Clients include '): v='Onze klanten zijn onder andere '+v[16:]
        elif re.search(r'[a-z]{3}',v) and v not in ('Nederlands','English'): miss.add('@'+v)
        return '%s="%s"'%(k,v)
    return re.sub(r'\b(aria-label|title|alt)="([^"]*)"',f,t)
def tr_js(js):
    def f(m):
        v=m.group(1)
        return "'"+D[v].replace("'","\\'")+"'" if v in D else m.group(0)
    return re.sub(r"'([^'\n]*)'",f,js)
os.makedirs(OUT+'/nl',exist_ok=True)
miss=set()
for name in ['index.html','submit.html','product.html','students.html']:
    t=prep(name,open(OUT+'/'+name).read())
    alt='<link rel="alternate" hreflang="en" href="%s">\n<link rel="alternate" hreflang="nl" href="%s">\n</head>'
    en=t.replace(FLAGMARK,flag('nl/'+name,'nl','Nederlands',NLFLAG))
    en=sub1(en,'</head>',alt%(name,'nl/'+name))
    # Dutch
    parts=re.split(r'(<script>.*?</script>|<style>.*?</style>)',t,flags=re.S)
    for i,p in enumerate(parts):
        if p.startswith('<script>'): parts[i]=tr_js(p)
        elif p.startswith('<style>'): pass
        else: parts[i]=tr_attr(tr_text(p,miss),miss)
    nl=''.join(parts)
    nl=nl.replace(FLAGMARK,flag('../'+name,'en','English',UKFLAG))
    nl=sub1(nl,'<html lang="en">','<html lang="nl">')
    nl=nl.replace('"assets/','"../assets/').replace('rug-logo-en.svg','rug-logo-nl.svg')
    nl=re.sub(r'€(\d),(\d{3})',r'€ \1.\2',nl)
    nl=sub1(nl,'</head>',alt%('../'+name,name))
    open(OUT+'/'+name,'w').write(en); open(OUT+'/nl/'+name,'w').write(nl)
print('untranslated:');[print('  ',m) for m in sorted(miss)]
