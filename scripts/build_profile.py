"""Generate the profile's original arcade / engineering artwork with Pillow."""
from pathlib import Path
from collections import deque
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, EDGE = '#101820', '#19252F', '#334450'
WHITE, MUTED, LIME, BLUE, ORANGE = '#F3F1E7', '#ACBBC5', '#D5F56A', '#89C9F0', '#FF936B'
S = 2

def new(h):
    im = Image.new('RGB', (1080*S,h*S), BG)
    return im, ImageDraw.Draw(im)

def box(d, coords, fill, outline=None, width=1):
    d.rectangle(tuple(int(v*S) for v in coords),fill=fill,outline=outline,width=width*S)

def line(d, pts, color=EDGE, width=1):
    d.line([(int(x*S),int(y*S)) for x,y in pts],fill=color,width=width*S)

def txt(d,x,y,s,size=16,color=WHITE,face='consola'):
    f=ImageFont.truetype('C:/Windows/Fonts/'+face+'.ttf',size*S)
    d.text((x*S,y*S),s,font=f,fill=color)

def dot(d,x,y,r,color):
    d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=color)

def chip(d,x,y,label,color=LIME):
    w=len(label)*9+24
    box(d,(x,y,x+w,y+30),color)
    txt(d,x+12,y+6,label,14,BG,'consolab')
    return w

def grid(d,w,h):
    for x in range(0,w,30): line(d,[(x,0),(x,h)],'#192630')
    for y in range(0,h,30): line(d,[(0,y),(w,y)],'#192630')

im,d=new(560)
grid(d,1080,560)
box(d,(24,24,1056,62),LIME)
txt(d,38,33,'JANLEARNS / PERSONAL LAB',15,BG,'consolab')
txt(d,761,33,'BUILD. BREAK. LEARN. REPEAT.',14,BG,'consolab')
# Oversized handle makes the profile recognisable at a glance.
txt(d,33,77,'JAN',125,WHITE,'impact')
txt(d,29,207,'LEARNS',125,LIME,'impact')
box(d,(40,365,90,371),ORANGE)
txt(d,40,393,'Rayzan Fazri Ramdany',25,WHITE,'arialbd')
txt(d,40,435,'Aspiring ML & AI engineer.',18,MUTED)
chip(d,40,478,'PYTHON')
chip(d,132,478,'DEEP LEARNING',BLUE)
chip(d,287,478,'AGENTS',ORANGE)
# Workstation window with a small, explicitly illustrative neural graph.
box(d,(611,91,1036,435),PANEL,EDGE)
box(d,(611,91,1036,129),'#243440')
for x,c in [(628,ORANGE),(645,LIME),(662,BLUE)]: dot(d,x,110,4,c)
txt(d,690,101,'experiment_01.py',13,MUTED)
txt(d,632,147,'> while curious:',17,LIME)
txt(d,652,177,'learn()',17,WHITE)
txt(d,652,207,'build()',17,WHITE)
txt(d,652,237,'try_again()',17,BLUE)
xs=[666,763,860,985]
ys=[[304,344,384],[292,322,352,382],[307,347,387],[326,366]]
for i in range(3):
    for y1 in ys[i]:
        for y2 in ys[i+1]: line(d,[(xs[i],y1),(xs[i+1],y2)],'#3A505D')
for i,x in enumerate(xs):
    for y in ys[i]:
        dot(d,x,y,7,BG)
        dot(d,x,y,4,LIME if i in (0,3) else BLUE)
box(d,(611,451,1036,509),BLUE)
txt(d,628,461,'CURRENT EXPLORATIONS /',15,BG,'consolab')
txt(d,628,482,'VISION, LANGUAGE & AGENTS',15,BG,'consolab')
line(d,[(24,536),(1056,536)],EDGE)
im.save(ROOT/'img/profile-cover.png',optimize=True)

# Tool shelf: labels, not invented scores or proficiency bars.
im,d=new(288)
txt(d,28,20,'01 / TOOLKIT',18,LIME,'consolab')
txt(d,718,23,'THE THINGS ON MY WORKBENCH',14,MUTED)
for x,num,title,items,color in [
    (28,'A','DATA',['Python / pandas','NumPy','Preprocessing'],LIME),
    (376,'B','MODELS',['PyTorch / TensorFlow','Keras / scikit-learn','Model evaluation'],BLUE),
    (724,'C','EXPERIMENTS',['Computer vision / NLP','Autonomous agents','Git / iteration'],ORANGE)]:
    box(d,(x,63,x+328,262),PANEL,EDGE)
    box(d,(x,63,x+5,262),color)
    txt(d,x+20,80,num,15,color,'consolab')
    txt(d,x+54,77,title,23,WHITE,'arialbd')
    line(d,[(x+20,118),(x+308,118)])
    for i,item in enumerate(items): txt(d,x+20,138+i*34,item,17,MUTED)
im.save(ROOT/'img/toolkit.png',optimize=True)

# Maze study, animated locally; no remote image service is required.
walls={(2,0),(4,0),(8,0),(5,1),(7,1),(1,2),(2,2),(4,2),(6,2),(9,2),
       (0,3),(4,3),(6,3),(9,3),(3,4),(4,4),(5,4),(8,4),(0,5),(5,5),
       (3,6),(7,6),(1,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),
       (4,8),(6,8),(1,9),(3,9),(4,9)}
queue=deque([[(0,0)]])
seen={(0,0)}
while queue:
    route=queue.popleft()
    if route[-1]==(9,9): break
    x,y=route[-1]
    for p in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
        if 0<=p[0]<10 and 0<=p[1]<10 and p not in walls and p not in seen:
            seen.add(p)
            queue.append(route+[p])
assert route[-1]==(9,9)
im,d=new(410)
box(d,(24,20,1056,58),ORANGE)
txt(d,38,29,'02 / PROJECT SPOTLIGHT',15,BG,'consolab')
txt(d,819,29,'PATHFINDING LAB',15,BG,'consolab')
txt(d,37,84,'NPC MAZE',62,WHITE,'impact')
txt(d,37,153,'SOLVER',62,BLUE,'impact')
txt(d,40,237,'A small maze. A learning agent.',18,MUTED)
txt(d,40,266,'One experiment at a time.',18,MUTED)
chip(d,40,317,'OPEN THE DEMO >',LIME)
txt(d,40,375,'PATHFINDING / AGENTS / EXPERIMENTS',13,MUTED)
x0,y0,step=711,86,28
for row in range(10):
    for col in range(10):
        x,y=x0+col*step,y0+row*step
        box(d,(x,y,x+25,y+25), '#527386' if (col,row) in walls else PANEL)
txt(d,711,378,'ILLUSTRATED ROUTE / 10 x 10',12,MUTED)
frames=[]
for n in range(1,len(route)+1):
    frame=im.copy(); fd=ImageDraw.Draw(frame)
    pts=[(x0+x*step+12,y0+y*step+12) for x,y in route[:n]]
    if len(pts)>1: line(fd,pts,LIME,4)
    x,y=pts[-1]
    box(fd,(x-6,y-6,x+6,y+6),LIME)
    dot(fd,x0+9*step+12,y0+9*step+12,4,ORANGE)
    frames.append(frame.resize((1080,410),Image.Resampling.LANCZOS))
frames[-1].save(ROOT/'img/maze-study.png',optimize=True)
frames[0].save(ROOT/'img/maze-study.gif',save_all=True,append_images=frames[1:],
               duration=[90]*(len(frames)-1)+[1800],loop=0,optimize=True,disposal=2)

im,d=new(100)
box(d,(24,15,1056,85),LIME)
txt(d,42,31,'GOT AN IDEA?',30,BG,'impact')
txt(d,287,40,"LET'S BUILD SOMETHING TOGETHER.",19,BG,'consolab')
txt(d,932,38,'SAY HI >',16,BG,'consolab')
im.save(ROOT/'img/contact.png',optimize=True)
