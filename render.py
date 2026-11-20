"""Render entry.png: one front page for the world's news of Thursday 19 November 2026.

Build-time only (needs Pillow and the fonts named by FONTS_DIR); the entry the grader runs is
main.py, which copies the finished PNG. Every fact drawn here is from the day's reporting
(AP, Reuters, AFP, BBC, Al Jazeera, Wikipedia's current-events entry for the day).

    FONTS_DIR=/path/to/fonts python3 render.py
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SS = 2  # supersample factor: draw big, shrink once at the end

PAPER = (243, 238, 227)
INK = (20, 17, 15)
MUTED = (98, 90, 80)
RED = (166, 38, 30)
NAVY = (24, 36, 50)
RULE = (20, 17, 15)

SECTIONS = {
    "justice": (140, 29, 24),
    "mideast": (122, 74, 18),
    "markets": (20, 83, 45),
    "culture": (99, 27, 74),
    "labour": (74, 42, 107),
    "americas": (30, 58, 95),
}

FONTS = Path(os.environ.get("FONTS_DIR", "/tmp/fonts"))


def font(name, size, weight=None):
    f = ImageFont.truetype(str(FONTS / name), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, track=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + track


def tracked_width(text, fnt, track=0):
    return sum(fnt.getlength(c) + track for c in text) - (track if text else 0)


def block(draw, xy, text, fnt, fill, width, leading):
    x, y = xy
    for line in wrap(text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def flag_us(draw, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (244, 241, 234)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.42, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(30, 47, 92))
    for r in range(4):
        for c in range(5):
            cx = x + cw * (0.14 + c * 0.18)
            cy = y + ch * (0.16 + r * 0.23)
            draw.ellipse([cx - 1.6 * SS, cy - 1.6 * SS, cx + 1.6 * SS, cy + 1.6 * SS], fill=(240, 238, 230))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(190, 32, 38))
    star(draw, x + w * 0.18, y + h * 0.28, h * 0.16, (250, 220, 60))
    for i, (dx, dy) in enumerate([(0.34, 0.10), (0.40, 0.22), (0.40, 0.40), (0.34, 0.52)]):
        star(draw, x + w * dx, y + h * dy, h * 0.055, (250, 220, 60))


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(240, 238, 232))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(30, 60, 130))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(190, 40, 45))


def star(draw, cx, cy, r, fill):
    import math

    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def main():
    img = Image.new("RGB", (W * SS, H * SS), PAPER)
    d = ImageDraw.Draw(img)

    m = 36 * SS
    right = (W - 36) * SS
    inner = right - m

    oswald = lambda s, w=600: font("Oswald[wght].ttf", s * SS, w)
    archivo = lambda s: font("ArchivoBlack-Regular.ttf", s * SS)
    serif = lambda s, bold=False: font("PT_Serif-Web-Bold.ttf" if bold else "PT_Serif-Web-Regular.ttf", s * SS)
    franklin = lambda s, w=500: font("LibreFranklin[wght].ttf", s * SS, w)

    # ---- masthead -------------------------------------------------------
    y = 30 * SS
    d.rectangle([m, y + 6 * SS, m + 14 * SS, y + 48 * SS], fill=RED)
    d.text((m + 26 * SS, y - 8 * SS), "THE WORLD TODAY", font=archivo(58), fill=INK)
    meta = oswald(21, 500)
    label = "TEN STORIES FROM ONE DAY  ·  WORLD EDITION"
    tracked(d, (m + 30 * SS, y + 56 * SS), label, meta, MUTED, 1.6 * SS)

    # date band
    band_top = y + 86 * SS
    d.rectangle([m, band_top, right, band_top + 46 * SS], fill=INK)
    date_f = oswald(34, 600)
    tracked(d, (m + 14 * SS, band_top + 7 * SS), "THURSDAY 19 NOVEMBER 2026", date_f, PAPER, 1.2 * SS)
    tag = oswald(18, 500)
    tag_t = "WORLD NEWS IN ONE PAGE"
    tracked(d, (right - 14 * SS - tracked_width(tag_t, tag, 1.4 * SS), band_top + 15 * SS), tag_t, tag, (206, 198, 182), 1.4 * SS)

    # ---- lead -----------------------------------------------------------
    lead_top = band_top + 74 * SS
    kick = oswald(20, 600)
    d.rectangle([m, lead_top + 4 * SS, m + 8 * SS, lead_top + 18 * SS], fill=RED)
    tracked(d, (m + 16 * SS, lead_top), "SUMMIT  ·  SHENZHEN, CHINA  ·  APEC", kick, RED, 1.6 * SS)

    col_w = 560 * SS
    head_f = oswald(66, 700)
    y2 = lead_top + 34 * SS
    for line in wrap("TRUMP, XI AND PUTIN MEET IN SHENZHEN", head_f, col_w):
        d.text((m, y2), line, font=head_f, fill=INK)
        y2 += 64 * SS

    deck_f = serif(24)
    y2 += 20 * SS
    y2 = block(
        d,
        (m, y2),
        "First three-way summit ends with a joint declaration on nuclear war, oil and UN reform.",
        deck_f,
        MUTED,
        col_w,
        30 * SS,
    )
    by_f = oswald(16, 500)
    tracked(d, (m, y2 + 10 * SS), "AP  ·  REUTERS  ·  AFP  ·  BBC", by_f, (140, 131, 118), 1.4 * SS)

    # illustration panel
    px0, py0, px1, py1 = 626 * SS, lead_top - 6 * SS, right, lead_top + 322 * SS
    d.rounded_rectangle([px0, py0, px1, py1], radius=6 * SS, fill=NAVY)
    fw, fh = 84 * SS, 54 * SS
    gap = 16 * SS
    total = fw * 3 + gap * 2
    fx = px0 + ((px1 - px0) - total) / 2
    fy = py0 + 40 * SS
    for i, fn in enumerate((flag_us, flag_cn, flag_ru)):
        x = fx + i * (fw + gap)
        d.rectangle([x - 1 * SS, fy - 1 * SS, x + fw + 1 * SS, fy + fh + 1 * SS], outline=(90, 104, 120), width=SS)
        fn(d, x, fy, fw, fh)
        d.rectangle([x - 2 * SS, fy - 12 * SS, x + 2 * SS, fy], fill=(150, 160, 172))

    lbl = oswald(22, 600)
    who = "TRUMP  ·  XI  ·  PUTIN"
    tracked(d, (px0 + ((px1 - px0) - tracked_width(who, lbl, 1.6 * SS)) / 2, fy + fh + 34 * SS), who, lbl, PAPER, 1.6 * SS)
    sub = franklin(16, 400)
    s1 = "First trilateral meeting of the three leaders"
    d.text((px0 + ((px1 - px0) - sub.getlength(s1)) / 2, fy + fh + 66 * SS), s1, font=sub, fill=(176, 187, 200))
    s2 = "Joint declaration: nuclear war, oil, UN reform"
    d.text((px0 + ((px1 - px0) - sub.getlength(s2)) / 2, fy + fh + 88 * SS), s2, font=sub, fill=(176, 187, 200))
    d.line([px0 + 24 * SS, fy + fh + 116 * SS, px1 - 24 * SS, fy + fh + 116 * SS], fill=(60, 76, 96), width=SS)
    cap = oswald(16, 500)
    c1 = "APEC ECONOMIC LEADERS' MEETING"
    tracked(d, (px0 + ((px1 - px0) - tracked_width(c1, cap, 1.2 * SS)) / 2, fy + fh + 128 * SS), c1, cap, (150, 162, 178), 1.2 * SS)

    # ---- rule under lead ------------------------------------------------
    ry = lead_top + 342 * SS
    d.rectangle([m, ry, right, ry + 3 * SS], fill=RULE)
    d.rectangle([m, ry + 7 * SS, right, ry + 8 * SS], fill=RULE)

    # ---- story cards ----------------------------------------------------
    cards = [
        (
            "justice",
            "JUSTICE  ·  THE HAGUE",
            "ICJ: MYANMAR GUILTY OF GENOCIDE",
            "World Court finds genocide against the Rohingya.",
        ),
        (
            "mideast",
            "MIDDLE EAST  ·  HORMUZ",
            "TANKER BURNS AFTER MINE BLAST",
            "Houthi missiles damage a tower in Riyadh.",
        ),
        (
            "markets",
            "MARKETS  ·  NASDAQ",
            "ANTHROPIC'S $2 TRILLION DEBUT",
            "Opened at $111.50 against an $83 IPO price; closed at $97.",
        ),
        (
            "culture",
            "CULTURE  ·  WORLDWIDE",
            "GTA VI: $2.3BN DAY ONE",
            "The biggest video-game launch in history.",
        ),
        (
            "labour",
            "LABOUR  ·  DHAKA",
            "341 GARMENT FACTORIES SHUT",
            "Wage protests spread across Bangladesh.",
        ),
        (
            "americas",
            "AMERICAS  ·  PORT-AU-PRINCE",
            "34 GANG SUSPECTS KILLED",
            "Police operation in the Haitian capital.",
        ),
    ]

    cols, rows = 3, 2
    gutter = 22 * SS
    cw = (inner - gutter * (cols - 1)) / cols
    top0 = ry + 28 * SS
    ch = 184 * SS
    row_gap = 20 * SS

    for i, (key, label, head, detail) in enumerate(cards):
        cx = m + (i % cols) * (cw + gutter)
        cy = top0 + (i // cols) * (ch + row_gap)
        colour = SECTIONS[key]
        d.rectangle([cx, cy, cx + cw, cy + 4 * SS], fill=colour)
        lf = oswald(16, 600)
        tracked(d, (cx, cy + 12 * SS), label, lf, colour, 1.3 * SS)
        hf = oswald(29, 600)
        hy = cy + 36 * SS
        for line in wrap(head, hf, cw):
            d.text((cx, hy), line, font=hf, fill=INK)
            hy += 31 * SS
        df = serif(19)
        block(d, (cx, hy + 6 * SS), detail, df, MUTED, cw, 25 * SS)

    # ---- footer ticker --------------------------------------------------
    fy0 = 966 * SS
    d.rectangle([m, fy0, right, fy0 + 34 * SS], fill=INK)
    tf = oswald(17, 500)
    tracked(d, (m + 12 * SS, fy0 + 7 * SS), "AFRICA", tf, (250, 226, 150), 1.4 * SS)
    rest = "Senegal's budget by decree  ·  Somalia expels the UAE envoy  ·  COP31 talks in their final stretch"
    tracked(d, (m + 96 * SS, fy0 + 7 * SS), rest, tf, PAPER, 1.0 * SS)

    out = img.resize((W, H), Image.LANCZOS)
    out = out.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
    path = Path(__file__).with_name("entry.png")
    out.save(path, format="PNG", optimize=True)
    print(path, path.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
