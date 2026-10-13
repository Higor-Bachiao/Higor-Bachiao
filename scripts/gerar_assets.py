"""Gera os SVGs animados (tema arcade 8-bit) do README de perfil."""
import os
import random
import sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

BG = "#0b0b1e"
FRAME = "#2d2d6b"
YELLOW = "#ffe14d"
CYAN = "#3df2ff"
PINK = "#ff2e88"
WHITE = "#f4f4ff"
LILAC = "#9aa0ff"
GREEN = "#5dff8f"
W = 840
FA = 'class="fa"'
FB = 'class="fb"'

FONT = {
    "A": ".###. #...# #...# ##### #...# #...# #...#",
    "B": "####. #...# #...# ####. #...# #...# ####.",
    "C": ".###. #...# #.... #.... #.... #...# .###.",
    "D": "####. #...# #...# #...# #...# #...# ####.",
    "E": "##### #.... #.... ####. #.... #.... #####",
    "F": "##### #.... #.... ####. #.... #.... #....",
    "G": ".###. #...# #.... #.### #...# #...# .###.",
    "H": "#...# #...# #...# ##### #...# #...# #...#",
    "I": "##### ..#.. ..#.. ..#.. ..#.. ..#.. #####",
    "J": "..### ...#. ...#. ...#. ...#. #..#. .##..",
    "K": "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    "L": "#.... #.... #.... #.... #.... #.... #####",
    "M": "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    "N": "#...# ##..# #.#.# #..## #...# #...# #...#",
    "O": ".###. #...# #...# #...# #...# #...# .###.",
    "P": "####. #...# #...# ####. #.... #.... #....",
    "Q": ".###. #...# #...# #...# #.#.# #..#. .##.#",
    "R": "####. #...# #...# ####. #.#.. #..#. #...#",
    "S": ".#### #.... #.... .###. ....# ....# ####.",
    "T": "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    "U": "#...# #...# #...# #...# #...# #...# .###.",
    "V": "#...# #...# #...# #...# #...# .#.#. ..#..",
    "W": "#...# #...# #...# #.#.# #.#.# ##.## #...#",
    "X": "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    "Y": "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    "Z": "##### ....# ...#. ..#.. .#... #.... #####",
    "0": ".###. #...# #..## #.#.# ##..# #...# .###.",
    "1": "..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.",
    "2": ".###. #...# ....# ...#. ..#.. .#... #####",
    "3": "####. ....# ....# .###. ....# ....# ####.",
    "4": "...#. ..##. .#.#. #..#. ##### ...#. ...#.",
    "5": "##### #.... ####. ....# ....# #...# .###.",
    "6": ".###. #.... #.... ####. #...# #...# .###.",
    "7": "##### ....# ...#. ..#.. .#... .#... .#...",
    "8": ".###. #...# #...# .###. #...# #...# .###.",
    "9": ".###. #...# #...# .#### ....# ....# .###.",
    " ": "..... ..... ..... ..... ..... ..... .....",
    ".": "..... ..... ..... ..... ..... ..... ..#..",
    "-": "..... ..... ..... .###. ..... ..... .....",
    ":": "..... ..#.. ..... ..... ..... ..#.. .....",
    "?": ".###. #...# ....# ...#. ..#.. ..... ..#..",
    "!": "..#.. ..#.. ..#.. ..#.. ..#.. ..... ..#..",
    "/": "....# ....# ...#. ..#.. .#... #.... #....",
    ">": "#.... .#... ..#.. ...#. ..#.. .#... #....",
    "<": "....# ...#. ..#.. .#... ..#.. ...#. ....#",
    "+": "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
    # til: duas linhas extras acima do A (desenhadas acima da linha de topo)
    "Ã": ".##.# #.##. ..... .###. #...# #...# ##### #...# #...# #...#",
}

INVADER_A = [
    "..#.....#..", "...#...#...", "..#######..", ".##.###.##.",
    "###########", "#.#######.#", "#.#.....#.#", "...##.##...",
]
INVADER_B = [
    "..#.....#..", "#..#...#..#", "#.#######.#", "###.###.###",
    "###########", ".#########.", "..#.....#..", ".#.......#.",
]
SHIP = [
    "......#......", ".....###.....", ".....###.....", ".###########.",
    "#############", "#############", "#############",
]


def bitmap(rows, x, y, px):
    """Converte linhas de '#'/'.' em comandos de path (um retângulo por sequência)."""
    d = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] == "#":
                s = c
                while c < len(row) and row[c] == "#":
                    c += 1
                d.append(f"M{x + s * px} {y + r * px}h{(c - s) * px}v{px}h-{(c - s) * px}z")
            else:
                c += 1
    return "".join(d)


def text_w(s, px):
    return len(s) * 6 * px - px


def text(s, x, y, px, fill, attrs=""):
    d = []
    for i, ch in enumerate(s):
        rows = FONT[ch].split()
        top = y - (len(rows) - 7) * px  # glifos com acento sobem acima do topo
        d.append(bitmap(rows, x + i * 6 * px, top, px))
    return f'<path d="{"".join(d)}" fill="{fill}" {attrs}/>'


def ctext(s, y, px, fill, attrs="", width=W):
    return text(s, (width - text_w(s, px)) // 2, y, px, fill, attrs)


def sprite(rows, x, y, px, fill, attrs=""):
    return f'<path d="{bitmap(rows, x, y, px)}" fill="{fill}" {attrs}/>'


def stars(h, n, seed):
    rnd = random.Random(seed)
    out = []
    for cls, count, size, color in (("s1", n, 2, "#5b5ba8"), ("s2", n // 2, 3, "#c9c9ff")):
        pts = [(rnd.randrange(0, W, 4), rnd.randrange(0, h, 4)) for _ in range(count)]
        d = "".join(f"M{x} {y + o}h{size}v{size}h-{size}z" for x, y in pts for o in (0, -h))
        out.append(f'<path class="{cls}" d="{d}" fill="{color}"/>')
    return "".join(out)


def svg(h, body, css="", star_n=40, seed=1):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" shape-rendering="crispEdges">
<defs>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern>
<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".55"/></radialGradient>
</defs>
<style>
@keyframes fall{{from{{transform:translateY(0)}}to{{transform:translateY({h}px)}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.s1{{animation:fall 14s linear infinite}}
.s2{{animation:fall 7s linear infinite}}
.blink{{animation:blink 1s steps(1) infinite}}
{css}
</style>
<rect width="{W}" height="{h}" fill="{BG}"/>
{stars(h, star_n, seed)}
{body}
<rect width="{W}" height="{h}" fill="url(#scan)"/>
<rect width="{W}" height="{h}" fill="url(#vig)"/>
<rect x="2" y="2" width="{W - 4}" height="{h - 4}" fill="none" stroke="{FRAME}" stroke-width="4"/>
</svg>
'''


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name}: {len(content) / 1024:.1f} KB")


# ---------------------------------------------------------------- header
def header():
    h = 320
    title = "HIGOR BACHIÃO"
    px = 8
    tx = (W - text_w(title, px)) // 2
    ty = 92
    css = f'''
@keyframes shine{{0%,88%{{fill:{YELLOW}}}90%,94%{{fill:{WHITE}}}96%,100%{{fill:{YELLOW}}}}}
@keyframes glitch{{0%,86%{{transform:translate(0,0)}}88%{{transform:translate(-8px,0)}}92%{{transform:translate(8px,-4px)}}96%,100%{{transform:translate(0,0)}}}}
@keyframes march{{0%{{transform:translateX(0)}}25%{{transform:translateX(12px)}}50%{{transform:translateX(24px)}}75%{{transform:translateX(12px)}}100%{{transform:translateX(0)}}}}
@keyframes fa{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes fb{{0%,49%{{opacity:0}}50%,100%{{opacity:1}}}}
@keyframes fly{{0%{{transform:translateX(-260px)}}50%{{transform:translateX(260px)}}100%{{transform:translateX(-260px)}}}}
@keyframes shot{{0%{{transform:translateY(0);opacity:1}}80%{{transform:translateY(-60px);opacity:1}}81%,100%{{transform:translateY(-60px);opacity:0}}}}
.title{{animation:shine 5s steps(1) infinite}}
.shadow{{animation:glitch 5s steps(1) infinite}}
.march{{animation:march 2s steps(1) infinite}}
.fa{{animation:fa .8s steps(1) infinite}}
.fb{{animation:fb .8s steps(1) infinite}}
.ship{{animation:fly 9s ease-in-out infinite}}
.shot{{animation:shot .9s linear infinite}}
'''
    body = []
    body.append(text("1UP 004200", 28, 22, 2, PINK))
    body.append(ctext("HI-SCORE 999990", 22, 2, WHITE))
    stage = "STAGE 01"
    body.append(text(stage, W - 28 - text_w(stage, 2), 22, 2, CYAN))
    body.append(text(title, tx + 6, ty + 6, px, PINK, 'class="shadow"'))
    body.append(text(title, tx, ty, px, YELLOW, 'class="title"'))
    body.append(ctext("FULL STACK DEVELOPER", 172, 3, CYAN))
    body.append(ctext("COMPUTER SCIENCE - UNIFEG", 206, 2, LILAC))
    for ix, color in ((70, GREEN), (W - 70 - 44 - 24, PINK)):
        body.append(f'<g class="march">{sprite(INVADER_A, ix, 172, 4, color, FA)}'
                    f'{sprite(INVADER_B, ix, 172, 4, color, FB)}</g>')
    body.append(ctext("> PRESS START <", 244, 3, WHITE, 'class="blink"'))
    sx = (W - 13 * 3) // 2
    body.append(f'<g class="ship">{sprite(SHIP, sx, 284, 3, CYAN)}'
                f'<rect class="shot" x="{sx + 18}" y="270" width="3" height="10" fill="{YELLOW}"/></g>')
    body.append(f'<path d="M24 310h{W - 48}v2h-{W - 48}z" fill="{FRAME}"/>')
    write("header.svg", svg(h, "\n".join(body), css, star_n=70, seed=7))


# ---------------------------------------------------------------- section banners
def section(name, label, idx, total, color):
    h = 56
    px = 4
    lx = 68
    lw = text_w(label, px)
    tag = f"STAGE {idx}/{total}"
    tagx = W - 24 - text_w(tag, 2)
    d0, d1 = lx + lw + 28, tagx - 24
    dots = "".join(f"M{x} 26h4v4h-4z" for x in range(d0, d1, 16))
    travel = d1 - d0 - 22
    css = f'''
@keyframes run{{from{{transform:translateX(0)}}to{{transform:translateX({travel}px)}}}}
@keyframes fa{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes fb{{0%,49%{{opacity:0}}50%,100%{{opacity:1}}}}
.run{{animation:run 6s linear infinite alternate}}
.fa{{animation:fa .6s steps(1) infinite}}
.fb{{animation:fb .6s steps(1) infinite}}
'''
    body = [
        text(">", 24, 14, px, color, 'class="blink"'),
        text(label, lx, 14, px, YELLOW),
        f'<path d="{dots}" fill="{FRAME}"/>',
        f'<g class="run">{sprite(INVADER_A, d0, 20, 2, color, FA)}'
        f'{sprite(INVADER_B, d0, 20, 2, color, FB)}</g>',
        text(tag, tagx, 21, 2, CYAN),
    ]
    write(name, svg(h, "\n".join(body), css, star_n=10, seed=idx))


# ---------------------------------------------------------------- inventory
def inventory():
    groups = [
        ("FRONT-END", ["TYPESCRIPT", "JAVASCRIPT", "REACT", "NEXT.JS", "ANGULAR", "TAILWIND"]),
        ("BACK-END", ["NODE.JS", "EXPRESS", "PRISMA", "POSTGRES", "SUPABASE", "MYSQL",
                      "FIREBASE", "PHP", "PYTHON"]),
        ("TOOLS", ["GIT", "DOCKER", "VERCEL", "POSTMAN"]),
    ]
    px, pad, sh, gap, left = 2, 12, 38, 10, 28
    slots = []
    body = []
    y = 26
    for title, items in groups:
        body.append(text(title, left, y, 2, CYAN))
        y += 26
        x = left
        for it in items:
            sw = text_w(it, px) + 2 * pad
            if x + sw > W - left:
                x = left
                y += sh + gap
            slots.append((it, x, y, sw))
            x += sw + gap
        y += sh + 26
    n = len(slots)
    step = 0.45
    cycle = n * step
    on = 100 / n
    css = f'''
@keyframes sel{{0%{{stroke:{YELLOW};fill:#2a2a12}}{on:.2f}%{{stroke:{FRAME};fill:#14143a}}100%{{stroke:{FRAME};fill:#14143a}}}}
@keyframes lbl{{0%{{fill:{YELLOW}}}{on:.2f}%{{fill:{WHITE}}}100%{{fill:{WHITE}}}}}
.slot{{stroke:{FRAME};fill:#14143a;stroke-width:3;animation:sel {cycle:.2f}s steps(1) infinite}}
.lbl{{animation:lbl {cycle:.2f}s steps(1) infinite}}
'''
    for i, (it, x, sy, sw) in enumerate(slots):
        delay = f'style="animation-delay:{i * step:.2f}s"'
        body.append(f'<rect class="slot" {delay} x="{x}" y="{sy}" width="{sw}" height="{sh}"/>')
        body.append(text(it, x + pad, sy + (sh - 7 * px) // 2, px, WHITE, f'class="lbl" {delay}'))
    h = y - 6
    write("inventory.svg", svg(h, "\n".join(body), css, star_n=30, seed=21))


# ---------------------------------------------------------------- footer
def footer():
    h = 170
    css = '''
@keyframes digit{0%{opacity:1}10%,100%{opacity:0}}
@keyframes march{0%{transform:translateX(0)}25%{transform:translateX(12px)}50%{transform:translateX(24px)}75%{transform:translateX(12px)}100%{transform:translateX(0)}}
@keyframes fa{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes fb{0%,49%{opacity:0}50%,100%{opacity:1}}
.digit{opacity:0;animation:digit 10s steps(1) infinite}
.march{animation:march 2s steps(1) infinite}
.fa{animation:fa .8s steps(1) infinite}
.fb{animation:fb .8s steps(1) infinite}
'''
    body = [ctext("THANKS FOR PLAYING!", 30, 4, YELLOW)]
    line = "CONTINUE?   YES   NO"
    lx = (W - text_w(line, 3)) // 2 - 30
    body.append(text(line, lx, 84, 3, WHITE))
    body.append(text(">", lx + 10 * 18, 84, 3, GREEN, 'class="blink"'))
    dx = lx + text_w(line, 3) + 40
    for i in range(10):
        body.append(text(str(9 - i), dx, 76, 5, PINK, f'class="digit" style="animation-delay:{i}s"'))
    colors = [GREEN, CYAN, PINK, YELLOW, LILAC, GREEN, CYAN, PINK, YELLOW, LILAC]
    x0 = (W - (10 * 33 + 9 * 30)) // 2 - 12
    inv = []
    for i, c in enumerate(colors):
        ix = x0 + i * 63
        inv.append(sprite(INVADER_A, ix, 128, 3, c, 'class="fa"'))
        inv.append(sprite(INVADER_B, ix, 128, 3, c, 'class="fb"'))
    body.append(f'<g class="march">{"".join(inv)}</g>')
    write("footer.svg", svg(h, "\n".join(body), css, star_n=40, seed=99))


header()
sections = [
    ("section-player.svg", "PLAYER INFO", GREEN),
    ("section-inventory.svg", "INVENTORY", PINK),
    ("section-quests.svg", "QUESTS", GREEN),
    ("section-stats.svg", "STATS", PINK),
    ("section-contact.svg", "CONTACT", GREEN),
]
for i, (fname, label, color) in enumerate(sections, 1):
    section(fname, label, i, len(sections), color)
inventory()
footer()
