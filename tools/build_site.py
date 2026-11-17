"""Step 1 of 2: build the English pages from the page sources in tools/src/ (into tools/.build/).

Run from the repository root:  python3 tools/build_site.py
Then run:                      python3 tools/i18n.py
"""
import re,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'tools','src')
OUT=os.path.join(ROOT,'tools','.build')  # intermediate English pages; i18n.py turns these into the real site
os.makedirs(OUT,exist_ok=True)
# The page sources refer to images by an id; this maps each id to its file in assets/.
BLOBS={'7f6c0b293b5ca221ab8dca08d463cfec':'brc-crown-white.svg',
'1897d917baed1cc5e56f1da94adf13a1':'brc-crown-red.svg',
'fce67d760db1110f8b0e5fa8aeb48b87':'rug-logo-en.svg',
'0cba844e6d9a8b84517cd7e3c79c796c':'rug-logo-nl.svg',
'ec716513fb7bc26d25947a6621baf027':'client-gasunie.png',
'48fdcd637d872b7afcf65b179f206c40':'client-provincie-groningen.png',
'274f50ed696218f6ca9812fdb565054e':'client-resato.png',
'b75cef0b87ef141ed31e252d08a8f70f':'client-fc-groningen.png',
'f2de1d83775f5bcd829581e15dc62aaf':'linkedin-black.png',
'6636523929c2148818e6bb9ef0cac18e':'linkedin-white.png'}
for n in BLOBS.values(): assert os.path.exists(os.path.join(ROOT,'assets',n)),n
PAGES={'C-TenWeeks.dc.html':'index.html','Submit.dc.html':'submit.html','Product.dc.html':'product.html','Students.dc.html':'students.html'}
def sub1(s,a,b,n=1):
    assert s.count(a)==n,(a[:60],s.count(a)); return s.replace(a,b)
def base(name):
    t=open(SRC+'/'+name).read()
    title=re.search(r'<title>(.*?)</title>',t).group(1)
    helm=re.search(r'<helmet>(.*?)</helmet>',t,re.S).group(1).strip()
    body=t[t.index('</helmet>')+9:t.index('</x-dc>')].strip()
    body=body.replace('{{accent}}','#dc002d')
    for k,n in BLOBS.items(): body=body.replace('/_blob/'+k,'assets/'+n)
    for a,b in PAGES.items(): body=body.replace('href="'+a+'"','href="'+b+'"')
    return title,helm,body
def page(title,helm,body,js=''):
    return '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex, nofollow">\n<title>%s</title>\n%s\n</head>\n<body>\n%s\n%s</body>\n</html>\n'%(title,helm,body,('<script>\n'+js.strip()+'\n</script>\n') if js else '')

# ---------- index
title,helm,b=base('C-TenWeeks.dc.html')
b=sub1(b,'{{typed}}','<span id="typed">Real Consultants.</span>')
b=sub1(b,'aria-pressed="{{isOrg}}" onClick="{{pickOrg}}"','id="btn-org" aria-pressed="true"')
b=sub1(b,'aria-pressed="{{isStudent}}" onClick="{{pickStudent}}"','id="btn-student" aria-pressed="false"')
m=re.search(r'<sc-if value="\{\{isOrg\}\}"[^>]*>\n(.*?)\n</sc-if>',b,re.S); b=b.replace(m.group(0),'<div id="panel-org">\n'+m.group(1)+'\n</div>')
m=re.search(r'<sc-if value="\{\{isStudent\}\}"[^>]*>\n(.*?)\n</sc-if>',b,re.S); b=b.replace(m.group(0),'<div id="panel-student" hidden>\n'+m.group(1)+'\n</div>')
people=[('Drs. Gert Haanstra','Course coordinator',0,'https://www.rug.nl/staff/g.f.haanstra/','https://nl.linkedin.com/in/gerthaanstra'),('Dr. Daniël Speldekamp','External relations',1,'',''),('Alieda Reijinga','Back office',0,'',''),('Drs. Bas Baalmans','Lecturer, supervisor',0,'https://www.rug.nl/staff/b.s.baalmans/',''),('Drs. Mariette Zweers','Lecturer, supervisor',0,'',''),('Ivan Palko, MSc','Lecturer, supervisor',0,'',''),('Dr. Teye Marra','Lecturer, supervisor',1,'',''),('Evelien Wolthuis, MSc','Guest lecturer',0,'',''),('Drs. Roel Stolvoort','Guest lecturer',0,'','')]
m=re.search(r'<sc-for list="\{\{people\}\}"[^>]*>\n(.*?)\n</sc-for>',b,re.S)
tpl=m.group(1);out=[]
for n,r,sch,home,li in people:
    c=tpl
    mi=re.search(r'<sc-if value="\{\{p\.scholar\}\}"[^>]*>\n(.*?)\n</sc-if>',c,re.S)
    c=c.replace(mi.group(0),mi.group(1) if sch else '').replace('\n\n','\n')
    c=c.replace('{{p.name}}',n).replace('{{p.role}}',r).replace('{{p.home}}',home or '#').replace('{{p.li}}',li or '#').replace('href="#scholar-link"','href="#"')
    out.append(c)
b=b.replace(m.group(0),'\n'.join(out))
b=b.replace('href="#case-placeholder"','href="#"')
# client carousel: each row is written once in the source (between REPEAT marks) and repeated 8x here so the loop is seamless, also on very wide screens
assert b.count('<!--REPEAT-->')==2
b=re.sub(r'<!--REPEAT-->\n(.*?)\n<!--/REPEAT-->',lambda m:'\n'.join([m.group(1)]*8),b,flags=re.S)
JS_INDEX='''
(function () {
  var doc = document;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(id) { return doc.getElementById(id); }
  function all(sel, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(sel)); }

  // audience switch (Organisations / Students)
  var sw = $("switch"), bo = $("btn-org"), bs = $("btn-student"), po = $("panel-org"), ps = $("panel-student");
  function pick(org) {
    po.hidden = !org; ps.hidden = org;
    bo.setAttribute("aria-pressed", String(org)); bs.setAttribute("aria-pressed", String(!org));
    sw.classList.toggle("is-student", !org);
    var panel = org ? po : ps;
    all(".card", panel).forEach(function (c, i) { c.style.setProperty("--i", i); c.classList.add("in"); });
    panel.classList.remove("is-swapping"); void panel.offsetWidth; panel.classList.add("is-swapping");
  }
  bo.addEventListener("click", function () { pick(true); });
  bs.addEventListener("click", function () { pick(false); });

  // reveal on scroll: elements with class "rv" fade in once; inside an "rv-group" they follow each other
  all(".rv-group").forEach(function (g) {
    all(".rv", g).forEach(function (el, i) { el.style.setProperty("--i", i); });
  });
  function countUp(el) {
    var end = parseInt(el.getAttribute("data-count"), 10), t0 = null;
    if (reduce || !end) return;
    function tick(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / 900);
      el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(tick);
    }
    el.textContent = "0"; requestAnimationFrame(tick);
  }
  function show(el) {
    if (el.classList.contains("in")) return;
    el.classList.add("in");
    all("[data-count]", el).forEach(countUp);
  }
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { show(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    all(".rv").forEach(function (el) { io.observe(el); });
  } else { all(".rv").forEach(function (el) { el.classList.add("in"); }); }

  // header state, menu highlight and the ten-weeks timeline: all driven by one scroll handler
  var hdr = $("hdr"), tl = $("tl"), items = all("li", tl), wk = $("wk-n");
  var links = all(".nav-link"), secs = links.map(function (a) { return $(a.getAttribute("href").slice(1)); });
  if (!reduce) items.forEach(function (li) { li.classList.remove("on"); });
  function frame() {
    ticking = false;
    var vh = window.innerHeight;
    hdr.classList.toggle("is-stuck", window.scrollY > 8);
    var cur = -1;
    secs.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < vh * 0.4) cur = i; });
    if (cur >= 0 && secs[cur].getBoundingClientRect().bottom < vh * 0.25 && cur === secs.length - 1) cur = -1;
    links.forEach(function (a, i) { if (i === cur) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
    if (reduce) return;
    var r = tl.getBoundingClientRect(), inset = 12;
    var len = items[items.length - 1].getBoundingClientRect().top + 17 - r.top - inset;  // the line ends at the last dot
    tl.style.setProperty("--rail", len + "px");
    var p = Math.max(0, Math.min(1, (vh * 0.62 - r.top - inset) / len));
    tl.style.setProperty("--p", p.toFixed(4));
    var fillY = r.top + inset + p * len, label = items[0].getAttribute("data-wk");
    items.forEach(function (li) {
      var on = li.getBoundingClientRect().top + 17 <= fillY + 1;
      li.classList.toggle("on", on);
      if (on) label = li.getAttribute("data-wk");
    });
    if (wk.textContent !== label) wk.textContent = label;
  }
  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  frame();

  // typewriter headline
  if (reduce) return;
  var phrases = ['Real Consultants.', 'Real Answers.', 'Real Progress.', 'Fresh Perspectives.', 'Ten Weeks.'];
  var el = $("typed"), i = 0, deleting = true;
  function step() {
    var full = phrases[i], cur = el.textContent, wait = 45;
    if (deleting) {
      if (cur.length > 0) { el.textContent = cur.slice(0, -1); wait = 28; }
      else { deleting = false; i = (i + 1) % phrases.length; wait = 250; }
    } else if (cur.length < full.length) { el.textContent = full.slice(0, cur.length + 1); wait = 60; }
    else { deleting = true; wait = 2200; }
    setTimeout(step, wait);
  }
  setTimeout(step, 2200);
})();
'''
open(OUT+'/index.html','w').write(page('Business Research & Consulting · University of Groningen',helm,b,JS_INDEX))

# ---------- submit
title,helm,b=base('Submit.dc.html')
b=sub1(b,'<div style="display: {{formDisplay}};','<div id="form-wrap" style="display: flex;')
for n in '123':
    b=sub1(b,'<li style="border-top: 6px solid {{bar%s}};'%n,'<li id="bar%s" style="border-top: 6px solid %s;'%(n,'#17181c' if n=='1' else '#c9cdd2'))
    b=sub1(b,'<div style="display: {{d%s}};'%n,'<div id="step%s" style="display: %s;'%(n,'flex' if n=='1' else 'none'))
for h,d in (('setSmall','data-set="size:small"'),('setLarge','data-set="size:large"'),('setKnown','data-set="known:yes"'),('setNew','data-set="known:no"')):
    b=sub1(b,'onChange="{{%s}}"'%h,d)
m=re.search(r'<sc-if value="\{\{isKnown\}\}"[^>]*>\n(.*?)\n</sc-if>',b,re.S); b=b.replace(m.group(0),'<div id="via-wrap" hidden>\n'+m.group(1)+'\n</div>')
m=re.search(r'<sc-if value="\{\{submitted\}\}"[^>]*>\n(.*?)\n</sc-if>',b,re.S); b=b.replace(m.group(0),'<div id="confirm" hidden>\n'+m.group(1)+'\n</div>')
b=sub1(b,'onClick="{{back}}"','id="btn-back"'); b=sub1(b,'onClick="{{next}}"','id="btn-next"')
b=sub1(b,'visibility: {{backVis}}','visibility: hidden'); b=sub1(b,'>{{nextLabel}}<','>Next step<')
b=sub1(b,'>{{price}}<',' id="price">€2,000 – €4,000<'); b=sub1(b,'>{{priceNote}}<',' id="price-note">Answer the two questions in step 1 to see your rate.<')
b=b.replace('href="#privacy"','href="#"')
JS_SUBMIT='''
(function () {
  // Mock-up only: nothing is sent anywhere.
  var s = { step: 1, size: null, known: null };
  var $ = function (id) { return document.getElementById(id); };
  function render() {
    for (var n = 1; n <= 3; n++) {
      $('step' + n).style.display = s.step === n ? 'flex' : 'none';
      $('bar' + n).style.borderTopColor = s.step >= n ? '#17181c' : '#c9cdd2';
    }
    $('btn-back').style.visibility = s.step > 1 ? 'visible' : 'hidden';
    $('btn-next').textContent = s.step < 3 ? 'Next step' : 'Send assignment';
    $('via-wrap').hidden = s.known !== 'yes';
    var price = '€2,000 – €4,000', note = 'Answer the two questions in step 1 to see your rate.';
    if (s.size === 'small') { price = '€2,000'; note = 'Rate for start-ups and very small businesses.'; }
    else if (s.known === 'yes') { price = '€3,000'; note = 'Partner rate, for returning clients and organisations in our network.'; }
    else if (s.size === 'large' && s.known === 'no') { price = '€4,000'; note = 'Standard rate.'; }
    $('price').textContent = price; $('price-note').textContent = note;
  }
  document.querySelectorAll('[data-set]').forEach(function (el) {
    el.addEventListener('change', function () { var kv = el.getAttribute('data-set').split(':'); s[kv[0]] = kv[1]; render(); });
  });
  $('btn-back').addEventListener('click', function () { s.step = Math.max(1, s.step - 1); render(); });
  $('btn-next').addEventListener('click', function () {
    if (s.step < 3) { s.step += 1; render(); window.scrollTo({ top: 0 }); }
    else { $('form-wrap').style.display = 'none'; $('confirm').hidden = false; }
  });
  render();
})();
'''
open(OUT+'/submit.html','w').write(page('Submit an assignment · BRC',helm,b,JS_SUBMIT))
for src,dst,t in (('Product.dc.html','product.html','Example assignment · BRC'),('Students.dc.html','students.html','Information for students · BRC')):
    _,helm,b=base(src); open(OUT+'/'+dst,'w').write(page(t,helm,b))
