"""Rebuild profile artwork with Pillow and Windows system fonts."""
from pathlib import Path
from collections import deque
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PAPER, INK, MUTED, ACCENT, LINE = '#F1EEE6', '#252820', '#66685D', '#B8422B', '#D1CEC2'

def text(d, xy, value, size=16, fill=INK, face='arial'):
    font = ImageFont.truetype('C:/Windows/Fonts/' + face + '.ttf', size*2)
    d.text((xy[0]*2, xy[1]*2), value, font=font, fill=fill)

def line(d, points, fill=LINE, width=1):
    d.line([(x*2,y*2) for x,y in points], fill=fill, width=width*2)

im = Image.new('RGB', (2160,880), PAPER)
d = ImageDraw.Draw(im)
text(d,(48,30),'JANLEARNS',15,face='arialbd')
text(d,(765,30),'MACHINE LEARNING / AI',14,face='consola')
line(d,[(48,66),(1032,66)],INK)
text(d,(45,99),'Rayzan Fazri',73,face='georgia')
text(d,(45,182),'Ramdany.',73,face='georgia')
text(d,(49,294),'Learning machines. Building things.',23)
line(d,[(48,367),(1032,367)])
text(d,(48,392),'EXPERIMENTS, NOTES & WORK IN PROGRESS',13,MUTED,'consola')
text(d,(905,392),'PROFILE / 01',13,MUTED,'consola')
for x in range(792,1000,32):
    for y in range(116,326,32):
        d.ellipse((x*2,y*2,x*2+3,y*2+3),fill=LINE)
line(d,[(824,310),(824,246),(888,246),(888,150),(984,150)],ACCENT,3)
line(d,[(888,246),(952,246),(952,310)],INK,2)
for x,y in [(824,310),(984,150),(952,310)]:
    d.ellipse(((x-6)*2,(y-6)*2,(x+6)*2,(y+6)*2),fill=ACCENT if x!=952 else INK)
im.save(ROOT/'img/profile-cover.png',optimize=True)

im=Image.new('RGB',(2160,700),INK)
d=ImageDraw.Draw(im)
text(d,(42,31),'01 / PATHFINDING',13,'#C7C8BA','consola')
text(d,(40,91),'A way through.',48,PAPER,'georgia')
text(d,(43,166),'NPC Maze Solver',22,PAPER)
text(d,(43,204),'An experiment in learning by doing.',17,'#C7C8BA')
line(d,[(43,279),(530,279)],'#56594E')
text(d,(43,302),'EXPLORE THE INTERACTIVE DEMO',13,PAPER,'consola')
line(d,[(514,319),(530,303),(516,303)],'#E98C6D',2)
line(d,[(530,303),(530,317)],'#E98C6D',2)
x0,y0,step=684,41,29
walls={(2,0),(4,0),(8,0),(5,1),(7,1),(1,2),(2,2),(4,2),(6,2),(9,2),
       (0,3),(4,3),(6,3),(9,3),(3,4),(4,4),(5,4),(8,4),(0,5),(5,5),
       (3,6),(7,6),(1,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),
       (4,8),(6,8),(1,9),(3,9),(4,9)}
for row in range(10):
    for col in range(10):
        x,y=x0+col*step,y0+row*step
        d.rectangle((x*2,y*2,(x+step-3)*2,(y+step-3)*2),
                    fill='#74776A' if (col,row) in walls else '#34382F')
# Find an actual open route for the conceptual maze illustration.
queue=deque([[(0,0)]])
seen={(0,0)}
while queue:
    route=queue.popleft()
    if route[-1]==(9,9):
        break
    x,y=route[-1]
    for nxt in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
        if 0<=nxt[0]<10 and 0<=nxt[1]<10 and nxt not in walls and nxt not in seen:
            seen.add(nxt)
            queue.append(route+[nxt])
assert route[-1]==(9,9), 'Maze must have a route to the exit'
line(d,[(x0+x*step+13,y0+y*step+13) for x,y in route],'#E98C6D',3)
for col,row in [(0,0),(9,9)]:
    x,y=x0+col*step+13,y0+row*step+13
    d.ellipse(((x-5)*2,(y-5)*2,(x+5)*2,(y+5)*2),fill=PAPER)
im.save(ROOT/'img/maze-study.png',optimize=True)
