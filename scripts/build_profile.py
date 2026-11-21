"""Generate the profile artwork with Pillow.

Style: white editorial layout, oversized black grotesk type, a few playful
flat shapes. Typeface is Inter Tight (SIL OFL, see scripts/fonts/OFL.txt).
Run: python scripts/build_profile.py
"""
from collections import deque
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = Path(__file__).resolve().parent / 'fonts' / 'InterTight.ttf'

PAPER, INK, GREY, RULE = '#FFFFFF', '#111111', '#8C8C8C', '#E6E6E6'
YELLOW, BLUE, PINK, GREEN, CREAM = '#FFD43B', '#3B5BFF', '#FF9EC4', '#1FC48F', '#F3EFE6'
S = 2  # render at 2x, GitHub scales it down


@lru_cache(None)
def font(size, weight='Bold'):
    f = ImageFont.truetype(str(FONT), int(size * S))
    f.set_variation_by_name(weight)
    return f


def canvas(w, h, bg=PAPER):
    im = Image.new('RGBA', (w * S, h * S), bg)
    return im, ImageDraw.Draw(im)


def sc(*v):
    return tuple(int(x * S) for x in v)


def text(d, x, y, s, size, weight='Bold', fill=INK, anchor='la'):
    d.text(sc(x, y), s, font=font(size, weight), fill=fill, anchor=anchor)


def width(d, s, size, weight='Bold'):
    return d.textlength(s, font=font(size, weight)) / S


def circle(d, x, y, r, fill):
    d.ellipse(sc(x - r, y - r, x + r, y + r), fill=fill)


def rrect(d, box, r, fill, outline=None, w=0):
    d.rounded_rectangle(sc(*box), radius=r * S, fill=fill, outline=outline, width=w * S)


def smiley(d, x, y, r, fill=YELLOW):
    circle(d, x, y, r, fill)
    e = r * 0.32
    circle(d, x - e, y - r * 0.18, r * 0.09, INK)
    circle(d, x + e, y - r * 0.18, r * 0.09, INK)
    d.arc(sc(x - r * 0.45, y - r * 0.35, x + r * 0.45, y + r * 0.5), 20, 160,
          fill=INK, width=int(r * 0.09 * S))


def pill(im, cx, cy, w, h, angle, fill):
    """Rotated capsule pasted onto im."""
    layer = Image.new('RGBA', (int(w * S), int(h * S)), (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle((0, 0, w * S - 1, h * S - 1), radius=h * S / 2, fill=fill)
    layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(layer, (int(cx * S - layer.width / 2), int(cy * S - layer.height / 2)))


def save(im, name, radius=28):
    """Round the corners so the white cards also sit well on GitHub dark mode."""
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=radius * S, fill=255)
    im.putalpha(mask)
    im.save(ROOT / 'img' / name, optimize=True)


# ---------------------------------------------------------------- cover
im, d = canvas(1080, 600)
text(d, 48, 44, 'Janlearns', 24)
text(d, 1032, 47, 'Rayzan Fazri Ramdany  —  Cimahi, Indonesia', 17, 'Medium', GREY, 'ra')
for i, line in enumerate(['Teaching machines', 'to read Indonesian', '(and to reason a bit).']):
    text(d, 44, 118 + i * 92, line, 86, 'Bold')
# playful corner: a sun that watches, a capsule, a dot
pill(im, 770, 500, 210, 70, 28, BLUE)
smiley(d, 962, 448, 84)
circle(d, 990, 128, 20, PINK)
d.line(sc(48, 512, 600, 512), fill=RULE, width=2 * S)
text(d, 48, 536, 'Machine learning  ·  NLP  ·  LLM fine-tuning  ·  RAG', 20, 'Regular', GREY)
save(im, 'profile-cover.png')


# ---------------------------------------------------------------- toolkit
im, d = canvas(1080, 470)
text(d, 48, 40, 'Toolkit', 20, 'SemiBold', GREY)
text(d, 1032, 40, 'What I reach for, not a skill meter', 17, 'Regular', GREY, 'ra')
rows = [('Data', 'Python, pandas, NumPy  ·  Preprocessing, EDA  ·  OCR, PDF ingestion', YELLOW),
        ('Models', 'PyTorch, TensorFlow  ·  HF Transformers, BERT  ·  LoRA / QLoRA', BLUE),
        ('Apps', 'RAG, LangChain, Ollama  ·  Streamlit, desktop  ·  GitHub Actions', PINK)]
for i, (label, items, c) in enumerate(rows):
    y = 92 + i * 122
    d.line(sc(48, y, 1032, y), fill=RULE, width=2 * S)
    text(d, 48, y + 26, f'0{i + 1}', 16, 'Medium', GREY)
    text(d, 104, y + 14, label, 62, 'Bold')
    circle(d, 104 + width(d, label, 62) + 22, y + 66, 10, c)
    text(d, 1032, y + 52, items, 19, 'Regular', INK, 'ra')
d.line(sc(48, 458, 1032, 458), fill=RULE, width=2 * S)
save(im, 'toolkit.png')


# ---------------------------------------------------------------- project cards
CW, CH, TH = 860, 720, 560  # card width/height, thumbnail height


def card(name, title, tags, bg, draw_art):
    im, d = canvas(CW, CH)
    rrect(d, (0, 0, CW, TH), 28, bg)
    draw_art(im, d)
    text(d, 8, TH + 40, title, 50, 'Bold')
    text(d, 8, TH + 116, tags, 26, 'Regular', GREY)
    save(im, name)


def art_cekfakta(im, d):
    # a claim card being checked by a magnifier
    rrect(d, (150, 120, 610, 440), 24, PAPER)
    for i, w in enumerate([360, 300, 380, 220]):
        rrect(d, (195, 170 + i * 58, 195 + w, 196 + i * 58), 13, RULE)
    rrect(d, (195, 228, 495, 254), 13, INK)
    circle(d, 620, 330, 118, INK)
    circle(d, 620, 330, 88, YELLOW)
    d.line(sc(705, 415, 790, 500), fill=INK, width=34 * S)
    d.line(sc(578, 334, 610, 366, 668, 296), fill=INK, width=16 * S, joint='curve')


def art_contextflow(im, d):
    # a stack of documents flowing into a small model
    for i in range(3):
        rrect(d, (120 + i * 26, 130 + i * 26, 360 + i * 26, 430 + i * 26), 20,
              PAPER, INK, 4)
    for i in range(4):
        rrect(d, (200, 230 + i * 44, 360, 250 + i * 44), 10, RULE)
    for k in range(4):
        circle(d, 460 + k * 42, 300, 8 + k * 2, INK)
    smiley(d, 700, 300, 92, YELLOW)


def art_ner(im, d):
    # a sentence where some words carry entity tags
    words = [('Rayzan', 'PER', YELLOW), ('kuliah', None, None), ('di', None, None),
             ('Cimahi', 'LOC', GREEN), ('sejak', None, None), ('2022', 'TIME', PAPER)]
    x, y = 80, 200
    for w, tag, c in words:
        ww = width(d, w, 46, 'SemiBold') + 52
        if x + ww > CW - 80:
            x, y = 80, y + 150
        rrect(d, (x, y, x + ww, y + 80), 40, c or '#FFC2DA', INK if c else None, 4 if c else 0)
        text(d, x + ww / 2, y + 40, w, 46, 'SemiBold', INK, 'mm')
        if tag:
            text(d, x + 10, y - 40, tag, 22, 'Bold', INK)
        x += ww + 22


def art_rag(im, d):
    # papers on the left, a cited answer bubble on the right
    for i in range(3):
        rrect(d, (90 + i * 30, 150 + i * 28, 280 + i * 30, 400 + i * 28), 14, PAPER, INK, 4)
    for i, w in enumerate([120, 90, 130, 70]):
        rrect(d, (175, 250 + i * 34, 175 + w, 264 + i * 34), 7, RULE)
    rrect(d, (175, 284, 275, 298), 7, YELLOW)
    for k in range(3):
        circle(d, 372 + k * 30, 290, 7, INK)
    d.polygon([sc(500, 374), sc(480, 450), sc(596, 374)], fill=PAPER, outline=INK, width=4 * S)
    rrect(d, (460, 150, 790, 380), 34, PAPER, INK, 4)
    d.line(sc(505, 378, 580, 378), fill=PAPER, width=5 * S)
    for i, w in enumerate([250, 210, 140]):
        rrect(d, (500, 195 + i * 50, 500 + w, 217 + i * 50), 11, RULE)
    rrect(d, (660, 295, 750, 327), 16, YELLOW)
    text(d, 705, 311, '[1]', 20, 'Bold', INK, 'mm')


card('work-cekfakta.png', 'CekFakta', 'NLP  ·  OCR  ·  Browser extension', YELLOW, art_cekfakta)
card('work-contextflow.png', 'ContextFlow AI', 'LLM fine-tuning  ·  LoRA  ·  Supabase', BLUE, art_contextflow)
card('work-ner.png', 'NER for Indonesian', 'Token classification  ·  BERT', PINK, art_ner)
card('work-rag.png', 'Poverty RAG Chatbot', 'RAG  ·  Vector DB  ·  LLM', GREEN, art_rag)


# ---------------------------------------------------------------- maze study
walls = {(2, 0), (4, 0), (8, 0), (5, 1), (7, 1), (1, 2), (2, 2), (4, 2), (6, 2), (9, 2),
         (0, 3), (4, 3), (6, 3), (9, 3), (3, 4), (4, 4), (5, 4), (8, 4), (0, 5), (5, 5),
         (3, 6), (7, 6), (1, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7),
         (4, 8), (6, 8), (1, 9), (3, 9), (4, 9)}
queue, seen = deque([[(0, 0)]]), {(0, 0)}
while queue:
    route = queue.popleft()
    if route[-1] == (9, 9):
        break
    x, y = route[-1]
    for p in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:
        if 0 <= p[0] < 10 and 0 <= p[1] < 10 and p not in walls and p not in seen:
            seen.add(p)
            queue.append(route + [p])
assert route[-1] == (9, 9)

im, d = canvas(1080, 440, CREAM)
text(d, 48, 44, 'Lab', 20, 'SemiBold', GREY)
text(d, 44, 92, 'NPC Maze', 78)
text(d, 44, 178, 'Solver', 78)
text(d, 48, 286, 'A small maze, a learning agent,', 21, 'Regular')
text(d, 48, 316, 'and a lot of attempts.', 21, 'Regular')
rrect(d, (48, 362, 268, 410), 24, INK)
text(d, 158, 386, 'Open the demo  →', 19, 'SemiBold', PAPER, 'mm')
x0, y0, step = 660, 40, 36
for row in range(10):
    for col in range(10):
        x, y = x0 + col * step, y0 + row * step
        rrect(d, (x + 2, y + 2, x + step - 2, y + step - 2), 7,
              INK if (col, row) in walls else PAPER)
frames = []
for n in range(1, len(route) + 1):
    f = im.copy()
    fd = ImageDraw.Draw(f)
    pts = [sc(x0 + x * step + step / 2, y0 + y * step + step / 2) for x, y in route[:n]]
    if len(pts) > 1:
        fd.line(pts, fill=BLUE, width=8 * S, joint='curve')
    gx, gy = x0 + 9 * step + step / 2, y0 + 9 * step + step / 2
    circle(fd, gx, gy, 9, PINK)
    ax, ay = route[n - 1]
    smiley(fd, x0 + ax * step + step / 2, y0 + ay * step + step / 2, 15)
    frames.append(f.resize((1080, 440), Image.Resampling.LANCZOS).convert('RGB'))
frames[-1].save(ROOT / 'img/maze-study.png', optimize=True)
frames[0].save(ROOT / 'img/maze-study.gif', save_all=True, append_images=frames[1:],
               duration=[90] * (len(frames) - 1) + [1800], loop=0, optimize=True, disposal=2)


# ---------------------------------------------------------------- contact
im, d = canvas(1080, 330)
text(d, 48, 48, 'Want to collaborate?', 26, 'Medium', GREY)
text(d, 44, 92, 'rayzanfazri@gmail.com', 72)
d.line(sc(48, 190, 48 + width(d, 'rayzanfazri@gmail.com', 72), 190), fill=INK, width=5 * S)
text(d, 48, 248, 'Want to say hi?  LinkedIn  ·  Instagram  ·  GitHub', 21, 'Regular', GREY)
smiley(d, 960, 230, 62)
pill(im, 1010, 96, 110, 40, -30, PINK)
save(im, 'contact.png')
