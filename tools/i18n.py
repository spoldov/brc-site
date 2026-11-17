"""Step 2 of 2: add the language switch and AI-disclosure line, and write the Dutch pages to nl/.

Run from the repository root, after tools/build_site.py:  python3 tools/i18n.py
Dutch wording lives in tools/nl.json (English text -> Dutch text).
Any English text without a translation is printed under "untranslated".
"""
import re,json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=ROOT
D=json.load(open(os.path.join(ROOT,'tools','nl.json'),encoding='utf-8'))
NLFLAG='<svg aria-hidden="true" width="30" height="20" viewBox="0 0 9 6" style="display: block; border-radius: 3px; box-shadow: 0 0 0 1.5px #ffffff"><rect width="9" height="2" fill="#AE1C28"></rect><rect y="2" width="9" height="2" fill="#ffffff"></rect><rect y="4" width="9" height="2" fill="#21468B"></rect></svg>'
UKFLAG='<svg aria-hidden="true" width="30" height="20" viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" style="display: block; border-radius: 3px; box-shadow: 0 0 0 1.5px #ffffff"><clipPath id="ukclip"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"></path></clipPath><path d="M0,0 v30 h60 v-30 z" fill="#012169"></path><path d="M0,0 L60,30 M60,0 L0,30" stroke="#ffffff" stroke-width="6"></path><path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#ukclip)" stroke="#C8102E" stroke-width="4"></path><path d="M30,0 v30 M0,15 h60" stroke="#ffffff" stroke-width="10"></path><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"></path></svg>'
def flag(href,code,label,svg):
    return '<a href="%s" lang="%s" hreflang="%s" aria-label="%s" title="%s" style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px">%s</a>'%(href,code,code,label,label,svg)
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
