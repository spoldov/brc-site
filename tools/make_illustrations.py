"""Draws the three temporary homepage illustrations (no faces) into assets/.

Run from the repository root:  python3 tools/make_illustrations.py
These stand in for real photos. Replace them with photos of BRC teams (with consent) before launch.
"""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RED='#dc002d'; DEEP='#a8001f'; INK='#17181c'; SLATE='#4f5d6d'; WHITE='#ffffff'
SKIN=['#f2c9b0','#c98f6f','#8d5a44','#e6b08f','#a8714f']
HAIR=[INK,'#5a2d22','#2b2f36','#7d0017','#3a2a24']
def svg(body,bg):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" preserveAspectRatio="xMidYMid slice">'
            '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
            '<rect width="900" height="600" fill="url(#bg)"/>%s</svg>\n')%(bg[0],bg[1],body)
def r(x,y,w,h,f,rx=0,extra=''): return '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" %s/>'%(x,y,w,h,rx,f,extra)
def c(x,y,rad,f,extra=''): return '<circle cx="%g" cy="%g" r="%g" fill="%s" %s/>'%(x,y,rad,f,extra)
def line(pts,col,w): return '<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"/>'%(' '.join('%g,%g'%p for p in pts),col,w)
def head(x,y,i,rad=34,back=False):
    # head with a simple hair shape; no facial features
    if back: return c(x,y,rad,HAIR[i%5])
    return c(x,y,rad,SKIN[i%5])+'<path d="M%g %g a%g %g 0 0 1 %g 0 q-%g -%g -%g 0z" fill="%s"/>'%(x-rad,y-4,rad,rad,2*rad,rad,rad*0.55,2*rad,HAIR[i%5])
def seated(x,table_y,i,col):
    return r(x-58,table_y-104,116,120,col,40)+r(x-9,table_y-118,18,26,SKIN[i%5])+head(x,table_y-142,i)
def standing(x,floor,i,col,legs=INK,arm=None):
    s='<ellipse cx="%g" cy="%g" rx="62" ry="10" fill="%s" opacity=".12"/>'%(x,floor+4,INK)
    s+=r(x-30,floor-150,24,150,legs,10)+r(x+6,floor-150,24,150,legs,10)
    if arm: s+=line([(x+arm[0]*30,floor-262),(x+arm[0]*30+arm[1],floor-262+arm[2])],col,26)+c(x+arm[0]*30+arm[1],floor-262+arm[2],15,SKIN[i%5])
    s+=r(x-46,floor-300,92,170,col,36)+r(x-9,floor-316,18,26,SKIN[i%5])+head(x,floor-338,i,32)
    return s
def bars(x,y,hs,w,gap,cols): return ''.join(r(x+n*(w+gap),y-h,w,h,cols[n%len(cols)],4) for n,h in enumerate(hs))
def text_lines(x,y,ws,col='#d9dce0',h=9,gap=12): return ''.join(r(x,y+n*(h+gap),w,h,col,4) for n,w in enumerate(ws))

# 1. intake at the client: a team and the client around a table
def intake():
    b=c(730,150,210,WHITE,'opacity=".55"')
    b+=r(560,70,250,210,WHITE,18,'opacity=".9"')+r(681,70,8,210,'#f3c6cc')+r(560,171,250,8,'#f3c6cc')        # window
    b+=r(96,300,56,150,DEEP,12)+'<path d="M124 300c-50-40-58-110-34-150 30 30 44 90 34 150zM124 300c40-50 44-120 20-170-30 40-36 110-20 170zM124 300c-10-60 0-130 40-176" fill="%s"/>'%'#7d0017'  # plant
    ty=430
    for n,(x,col) in enumerate([(250,RED),(400,INK),(550,SLATE),(700,DEEP)]): b+=seated(x,ty,n,col)
    b+='<path d="M360 150h150a22 22 0 0 1 22 22v52a22 22 0 0 1-22 22h-86l-30 30v-30h-34a22 22 0 0 1-22-22v-52a22 22 0 0 1 22-22z" fill="%s"/>'%WHITE     # speech bubble
    b+=c(404,198,9,RED)+c(436,198,9,RED)+c(468,198,9,RED)
    b+=r(120,ty,700,30,'#2b2d33',15)+r(170,ty+30,26,170,'#2b2d33')+r(744,ty+30,26,170,'#2b2d33')           # table
    b+=r(352,ty-64,96,60,'#3a3d44',8)+r(336,ty-6,128,8,'#55595f',4)                                        # laptop
    b+=r(196,ty-12,90,10,WHITE,3,'transform="rotate(-4 240 %g)"'%ty)+r(596,ty-12,84,10,WHITE,3)+r(520,ty-34,26,32,WHITE,6)+r(700,ty-34,26,32,RED,6)
    return svg(b,('#fdeef0','#f6cfd6'))

# 2. poster session: two posters, a presenter and two visitors
def posters():
    b=c(160,120,230,WHITE,'opacity=".5"')+r(0,520,900,80,'#f1dcc8')
    for x,title in ((90,RED),(560,INK)):
        b+=r(x+118,420,14,110,'#b9a48f')+r(x+70,524,110,10,'#b9a48f',5)
        b+=r(x,90,250,340,WHITE,16,'stroke="#ead7c4" stroke-width="3"')+r(x+24,114,150,22,title,6)
    b+=bars(118,300,[60,96,130,84],32,14,[RED,INK,RED,DEEP])+text_lines(118,326,[190,150,170])
    b+=c(640,230,56,'#f3c6cc')+'<path d="M640 230V174a56 56 0 0 1 53 74z" fill="%s"/>'%RED+r(716,180,70,12,'#d9dce0',4)+r(716,206,54,12,'#d9dce0',4)+r(716,232,62,12,'#d9dce0',4)+text_lines(584,326,[200,160,180])
    b+=standing(396,540,1,RED,INK,arm=(-1,-58,-34))
    b+=standing(500,540,3,SLATE,'#2b2d33')
    b+=standing(838,540,0,DEEP,INK,arm=(-1,-36,-60))
    return svg(b,('#fdf4ea','#f8e3d0'))

# 3. final presentation: a presenter at a screen, the client's team in front
def presentation():
    b=c(450,210,330,WHITE,'opacity=".5"')
    b+=r(150,60,520,310,WHITE,18,'stroke="#cfd8e2" stroke-width="3"')+r(180,88,190,22,INK,6)+text_lines(180,128,[120,90],'#d9dce0')
    b+=bars(190,330,[40,64,52,90],34,16,['#e3e8ee'])
    b+=line([(410,310),(470,270),(520,286),(580,214),(636,150)],RED,10)+c(636,150,13,RED)
    b+=r(396,366,28,60,'#b7c2ce')+r(330,420,160,12,'#b7c2ce',6)
    b+=standing(760,470,2,RED,INK,arm=(-1,-70,-70))
    for n,(x,col) in enumerate([(120,INK),(290,DEEP),(460,SLATE),(630,INK),(800,'#7d0017')]):
        b+=r(x-74,520,148,120,col,48)+head(x,480,n+1,40,back=True)
    return svg(b,('#eef2f6','#d9e2ec'))

for name,fn in (('intake',intake),('posters',posters),('presentation',presentation)):
    open(os.path.join(ROOT,'assets','illustration-%s.svg'%name),'w').write(fn())
