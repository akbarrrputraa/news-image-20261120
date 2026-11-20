"""news-image-20261120 — one image summing up Friday 20 November 2026.

Pure standard library. Draws a 1024x1024 broadsheet front page with the
day's verified world news and writes it to $MAKEFUN_OUTPUT_DIR/entry.png
(or /output/entry.png). Deterministic: the same bytes on every run.

Stories verified 20 Nov 2026 against WSJ, Barron's, BBC, Reuters, AP and
The Hindu BusinessLine. Events are those that happened, or were first
reported, on 20 November 2026 in some time zone.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import Canvas, text_width  # noqa: E402

W, H = 1024, 1024

# Palette: newsprint paper, navy ink, red accent.
PAPER = bytes([247, 243, 234])
INK = bytes([20, 33, 61])
NAVY = bytes([20, 33, 61])
RED = bytes([178, 34, 34])
GREY = bytes([90, 90, 86])
LGREY = bytes([226, 221, 210])
BLUE = bytes([52, 96, 140])
GOLD = bytes([176, 141, 60])
GREEN = bytes([34, 120, 70])
PANEL = bytes([232, 236, 242])
WHITE = bytes([255, 255, 255])
BLACK = bytes([18, 18, 18])


def draw_scales(c, cx, top, s, color):
    """Scales of justice, drawn from lines and triangles."""
    c.vline(cx, top, 150 * s // 10, color, 4)
    c.hline(cx - 62 * s // 10, top + 12 * s // 10, 124 * s // 10, color, 4)
    c.circle(cx, top - 4 * s // 10, 6 * s // 10, color)
    for side in (-1, 1):
        px = cx + side * 56 * s // 10
        c.line(px, top + 12 * s // 10, px - 26 * s // 10,
               top + 62 * s // 10, color, 3)
        c.line(px, top + 12 * s // 10, px + 26 * s // 10,
               top + 62 * s // 10, color, 3)
        c.line(px - 26 * s // 10, top + 62 * s // 10,
               px + 26 * s // 10, top + 62 * s // 10, color, 3)
        c.triangle(px - 26 * s // 10, top + 62 * s // 10,
                   px + 26 * s // 10, top + 62 * s // 10,
                   px, top + 88 * s // 10, color)
    c.hline(cx - 30 * s // 10, top + 150 * s // 10, 60 * s // 10, color, 5)
    c.hline(cx - 20 * s // 10, top + 140 * s // 10, 40 * s // 10, color, 4)


def draw_chart(c, x, y, w, h, color):
    """Rising market chart with arrow."""
    c.hline(x, y + h, w, GREY, 2)
    c.vline(x, y, h, GREY, 2)
    pts = [(x + 6, y + h - 12), (x + w // 4, y + h - 34),
           (x + w // 2, y + h - 26), (x + 3 * w // 4, y + h - 58),
           (x + w - 8, y + 14)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.line(ax, ay, bx, by, color, 4)
    ex, ey = pts[-1]
    c.line(ex, ey, ex - 14, ey + 2, color, 4)
    c.line(ex, ey, ex - 4, ey + 14, color, 4)


def draw_flags(c, x, y):
    """Three small flags: USA, China, Russia."""
    # USA: red/white stripes + blue canton
    for i in range(7):
        c.rect(x, y + i * 5, 74, 5, RED if i % 2 == 0 else WHITE)
    c.rect(x, y, 30, 20, NAVY)
    for r in range(3):
        for col in range(4):
            c.rect(x + 3 + col * 7, y + 3 + r * 6, 3, 3, WHITE)
    # China: red field, gold stars
    c.rect(x + 86, y, 74, 35, RED)
    c.circle(x + 98, y + 10, 4, GOLD)
    for sx, sy in ((112, 6), (120, 10), (120, 18), (112, 22)):
        c.circle(x + sx, y + sy, 2, GOLD)
    # Russia: white / blue / red tricolour
    c.rect(x + 172, y, 74, 12, WHITE)
    c.rect(x + 172, y + 12, 74, 11, BLUE)
    c.rect(x + 172, y + 23, 74, 12, RED)


def draw_tanker(c, x, y, w):
    """Oil tanker with a flame above the bow."""
    c.rect(x, y + 34, w, 26, NAVY)
    c.triangle(x + w, y + 34, x + w + 26, y + 60, x + w, y + 60, NAVY)
    c.rect(x + 12, y + 12, 22, 22, RED)
    c.rect(x + 40, y + 18, 30, 16, GOLD)
    c.rect(x + 76, y + 12, 22, 22, BLUE)
    c.vline(x + w - 40, y + 6, 28, GREY, 3)
    fx = x + w + 8
    c.triangle(fx - 10, y + 22, fx + 10, y + 22, fx, y - 6, RED)
    c.triangle(fx - 5, y + 22, fx + 5, y + 22, fx, y + 6, GOLD)
    c.rect(x - 6, y + 62, w + 44, 4, BLUE)


def draw_bridge(c, x, y, w):
    """Suspension bridge with a blast star above it."""
    c.hline(x, y + 44, w, INK, 4)
    for px in (x + 12, x + w // 2, x + w - 16):
        c.vline(px, y + 10, 34, INK, 3)
    c.line(x + 12, y + 10, x + w // 2, y + 26, INK, 3)
    c.line(x + w // 2, y + 26, x + w - 16, y + 10, INK, 3)
    bx, by = x + w // 2, y + 10
    for dx, dy in ((-8, -4), (0, -9), (8, -4), (-9, 3), (9, 3),
                   (-4, 7), (4, 7), (0, 9)):
        c.line(bx, by, bx + dx, by + dy, RED, 3)
    c.circle(bx, by, 4, RED)


def draw_globe(c, cx, cy, r):
    c.circle(cx, cy, r, BLUE, fill=False)
    c.circle(cx, cy, r - 3, BLUE, fill=False)
    for dx in (-r // 2, 0, r // 2):
        c.line(cx + dx, cy - r + 6, cx + dx, cy + r - 6, BLUE, 2)
    c.hline(cx - r + 4, cy, 2 * r - 8, BLUE, 2)
    c.hline(cx - r + 8, cy - r // 2, 2 * r - 16, BLUE, 2)
    c.hline(cx - r + 8, cy + r // 2, 2 * r - 16, BLUE, 2)


def story(c, x, y, w, kicker, headline, body, icon=None, hscale=3):
    """One story block. Returns y below the block."""
    c.text(x, y, kicker, 2, RED)
    y += 22
    y = c.para(x, y, headline, hscale, INK, w, leading=7 * hscale + 5)
    y += 4
    y = c.para(x, y, body, 2, BLACK, w, leading=18)
    if icon:
        icon(c, x, y + 6, w)
        y += 78
    return y + 6


def build():
    c = Canvas(W, H, PAPER)

    # ---- masthead ------------------------------------------------------
    c.rect(0, 0, W, 118, NAVY)
    c.rect(0, 118, W, 6, RED)
    c.text(28, 22, "THE WORLD", 9, WHITE)
    c.text_right(W - 28, 30, "IN ONE PAGE", 4, GOLD)
    c.text(28, 84, "FRIDAY, 20 NOVEMBER 2026", 3, WHITE)
    c.text_right(W - 28, 86, "THE DAY'S NEWS  -  ONE IMAGE", 2, WHITE)

    # ---- lead story: ICJ genocide ruling -------------------------------
    y = 138
    c.text(28, y, "THE HAGUE  •  JUSTICE", 2, RED)
    y += 24
    y = c.para(28, y, "WORLD COURT: MYANMAR", 5, INK, 620, leading=40)
    y = c.para(28, y, "COMMITTED GENOCIDE", 5, INK, 620, leading=40)
    y += 2
    y = c.para(28, y,
               "The International Court of Justice ruled 9-6 that Myanmar "
               "committed genocide against the Rohingya in its 2017 "
               "campaign - the first time the UN court has ever found a "
               "state guilty of genocide. About 10,000 were killed; the "
               "court ordered compensation and the safe return of refugees.",
               2, BLACK, 620, leading=18)
    # lead illustration panel
    px, py, pw, ph = 692, 138, 304, 266
    c.rect(px, py, pw, ph, PANEL)
    c.rect(px, py, pw, 4, RED)
    draw_scales(c, px + pw // 2, py + 34, 10, NAVY)
    c.text_center(px + pw // 2, py + 196, "9 - 6", 6, RED)
    c.text_center(px + pw // 2, py + 240, "FIRST VERDICT OF ITS KIND", 2, INK)

    # ---- row 2: three stories ------------------------------------------
    y0 = 420
    c.hline(28, y0, W - 56, INK, 3)
    colw = 304
    xs = [28, 360, 692]
    # A: Anthropic IPO
    y = y0 + 14
    c.text(xs[0], y, "NEW YORK  •  MARKETS", 2, RED)
    y += 22
    y = c.para(xs[0], y, "AI LAB SOARS", 3, INK, colw, leading=26)
    y = c.para(xs[0], y, "ON DEBUT", 3, INK, colw, leading=26)
    y += 4
    y = c.para(xs[0], y,
               "Anthropic closed up 17% at $97.17 in the biggest IPO ever "
               "- $81.3bn raised - as stocks fell 2%.",
               2, BLACK, colw, leading=18)
    draw_chart(c, xs[0] + 8, y + 8, colw - 40, 44, GREEN)
    # B: Shenzhen summit
    y = y0 + 14
    c.text(xs[1], y, "SHENZHEN  •  DIPLOMACY", 2, RED)
    y += 22
    y = c.para(xs[1], y, "FIRST THREE-WAY", 3, INK, colw, leading=26)
    y = c.para(xs[1], y, "SUMMIT", 3, INK, colw, leading=26)
    y += 4
    y = c.para(xs[1], y,
               "The three leaders met in China and issued a four-point "
               "peace declaration.",
               2, BLACK, colw, leading=18)
    draw_flags(c, xs[1] + 8, y + 10)
    # C: Gulf attacks
    y = y0 + 14
    c.text(xs[2], y, "THE GULF  •  CONFLICT", 2, RED)
    y += 22
    y = c.para(xs[2], y, "TANKER ABLAZE,", 3, INK, colw, leading=26)
    y = c.para(xs[2], y, "RIYADH HIT", 3, INK, colw, leading=26)
    y += 4
    y = c.para(xs[2], y,
               "A tanker caught fire after hitting a mine near Hormuz; "
               "a Houthi missile hit Riyadh.",
               2, BLACK, colw, leading=18)
    draw_tanker(c, xs[2] + 8, y + 4, 200)

    # ---- row 3: three stories ------------------------------------------
    y0 = 660
    c.hline(28, y0, W - 56, INK, 3)
    # D: Ukraine
    y = y0 + 14
    c.text(xs[0], y, "KYIV  •  WAR", 2, RED)
    y += 22
    y = c.para(xs[0], y, "BRIDGE HIT AGAIN;", 3, INK, colw, leading=26)
    y = c.para(xs[0], y, "KYIV STRUCK", 3, INK, colw, leading=26)
    y += 4
    y = c.para(xs[0], y,
               "Ukraine hit the Crimean Bridge a third time in four days; "
               "four ballistic missiles struck Kyiv.",
               2, BLACK, colw, leading=18)
    draw_bridge(c, xs[0] + 8, y + 2, 240)
    # E: Berlin talks
    y = y0 + 14
    c.text(xs[1], y, "BERLIN  •  EUROPE", 2, RED)
    y += 22
    y = c.para(xs[1], y, "EUROPE READY FOR", 3, INK, colw, leading=26)
    y = c.para(xs[1], y, "RUSSIA TALKS", 3, INK, colw, leading=26)
    y += 4
    y = c.para(xs[1], y,
               "Ukraine's allies, meeting in Berlin, said they are ready "
               "to negotiate with Russia to end the war.",
               2, BLACK, colw, leading=18)
    draw_globe(c, xs[1] + colw // 2, y + 26, 22)
    # F: Washington
    y = y0 + 14
    c.text(xs[2], y, "WASHINGTON  •  POLITICS", 2, RED)
    y += 22
    y = c.para(xs[2], y, "SENATE BLOCKS WAR", 3, INK, colw, leading=26)
    y = c.para(xs[2], y, "POWERS VOTE", 3, INK, colw, leading=26)
    y += 4
    y = c.para(xs[2], y,
               "The Senate rejected an Iran war-powers vote. Trump "
               "pardoned Pete Rose.",
               2, BLACK, colw, leading=18)
    c.text(xs[2] + 8, y + 8, "51-48", 4, RED)
    c.text(xs[2] + 190, y + 16, "VOTE TO", 2, INK)
    c.text(xs[2] + 190, y + 34, "LIMIT WAR", 2, INK)

    # ---- briefs ---------------------------------------------------------
    y0 = 880
    c.rect(0, y0, W, 4, RED)
    c.text(28, y0 + 12, "ALSO TODAY", 2, RED)
    briefs = ("Genoa airport halts flights after drones spotted  •  "
              "India evacuates 80,000 as Storm Dana nears  •  "
              "Fiona the hippo dies  •  "
              "COP31 draft drops fossil-fuel wording")
    c.para(28, y0 + 36, briefs, 2, BLACK, W - 56, leading=18)

    # ---- markets strip ---------------------------------------------------
    y0 = 956
    c.rect(0, y0, W, 36, NAVY)
    c.text(28, y0 + 11, "MARKETS", 2, GOLD)
    c.text(150, y0 + 11,
           "S&P -2.02% • Dow -2.19% • Nasdaq -2.25% • ANT +17% • NVDA -3%",
           2, WHITE)

    # ---- footer ----------------------------------------------------------
    c.text(28, 1000, "All stories reported 20 Nov 2026.", 2, GREY)
    c.text_right(W - 28, 1000,
                 "Sources: WSJ, Barron's, BBC, Reuters, AP", 2, GREY)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = build().png_bytes()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
