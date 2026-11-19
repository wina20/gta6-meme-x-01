#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme with Pillow.

Scene: a Vice City style sunset beach. The make.fun ghost mascot (white body,
thick black outline, black four-pointed sparkle eyes, one round little hand)
chills on the sand holding its magenta star coin, in no hurry at all --
because unlike everyone waiting on GTA VI since 2013, this agent already got
paid. The name make.fun sits in the bottom caption, inside the picture.

Everything is drawn from scratch here: no stock art, no Rockstar assets.
Rendered at 2x and downscaled so edges stay clean at judge size.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1200 * S, 675 * S   # final picture is 1200 x 675
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MAGENTA = (224, 33, 138)
INK = (12, 6, 24)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_and_ground(img):
    """Vertical sunset gradient, then sea and sand bands."""
    d = ImageDraw.Draw(img)
    stops = [
        (0.00, (38, 10, 74)),     # deep purple up top
        (0.30, (106, 36, 128)),
        (0.48, (199, 62, 133)),   # hot pink
        (0.60, (255, 110, 84)),   # orange at the horizon
        (0.62, (64, 32, 92)),     # sea, dark violet
        (0.78, (64, 32, 92)),
        (0.80, (214, 130, 84)),   # wet sand line
        (1.00, (168, 92, 58)),    # dry sand
    ]
    for y in range(H):
        t = y / (H - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                d.line([(0, y), (W, y)], fill=lerp(c0, c1, (t - t0) / (t1 - t0)))
                break


def sun(img):
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy, r = int(W * 0.335), int(H * 0.615), int(H * 0.30)
    for grow, alpha in ((90, 40), (50, 70)):
        d.ellipse([cx - r - grow, cy - r - grow, cx + r + grow, cy + r + grow],
                  fill=(255, 176, 92, alpha))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 196, 105))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 226, 160), width=4)


def sea_glints(img):
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(2013)
    for _ in range(90):
        x = rng.randint(30, W - 200)
        y = rng.randint(int(H * 0.635), int(H * 0.765))
        n = rng.randint(24, 110)
        d.line([(x, y), (x + n, y)], fill=(255, 170, 120, rng.randint(50, 130)),
               width=rng.choice((3, 4)))


def sparkle(d, cx, cy, tall, wide, waist, fill):
    """A four-pointed sparkle (the ghost's eye shape, and coin glints)."""
    pts = [(cx, cy - tall), (cx + waist, cy - waist), (cx + wide, cy),
           (cx + waist, cy + waist), (cx, cy + tall), (cx - waist, cy + waist),
           (cx - wide, cy), (cx - waist, cy - waist)]
    d.polygon(pts, fill=fill)


def star(d, cx, cy, r_out, r_in, fill):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def palm(d, base_x, base_y, height, lean, flip=1):
    """A palm silhouette: curved trunk plus drooping fronds."""
    col = (18, 7, 34)
    top_x = base_x + lean * flip
    top_y = base_y - height
    pts = []
    for i in range(25):
        t = i / 24
        x = base_x + (top_x - base_x) * t * t
        y = base_y + (top_y - base_y) * t
        pts.append((x, y))
    d.line(pts, fill=col, width=26, joint="curve")
    for ang in (-165, -125, -85, -40, -5, 30):
        a = math.radians(ang if flip > 0 else 180 - ang)
        length = height * 0.42
        frond = []
        for i in range(17):
            t = i / 16
            x = top_x + math.cos(a) * length * t
            y = top_y + math.sin(a) * length * t + 130 * t * t
            frond.append((x, y))
        d.line(frond, fill=col, width=15, joint="curve")


def umbrella(img):
    """A striped beach umbrella planted left of the ghost."""
    d = ImageDraw.Draw(img)
    px, py = int(W * 0.205), int(H * 0.985)      # pole foot in the sand
    tx, ty = int(W * 0.225), int(H * 0.475)      # pole top / canopy centre
    d.line([(px, py), (tx, ty)], fill=(60, 32, 20), width=12)
    r = int(W * 0.155)
    cols = [MAGENTA, (255, 240, 214)]
    for i in range(8):
        d.pieslice([tx - r, ty - r, tx + r, ty + r],
                   start=180 + i * 22.5, end=180 + (i + 1) * 22.5,
                   fill=cols[i % 2], outline=(60, 20, 50))
    d.ellipse([tx - 13, ty - 13, tx + 13, ty + 13], fill=(60, 20, 50))


def ghost(img):
    """The make.fun ghost, large and centre stage, holding its coin."""
    d = ImageDraw.Draw(img, "RGBA")
    cx = int(W * 0.545)
    top = int(H * 0.315)
    gw = int(W * 0.295)            # body width
    gh = int(H * 0.545)            # body height
    bottom = top + gh
    dome_cy = top + gw // 2

    # soft shadow on the sand
    d.ellipse([cx - gw * 0.62, bottom - 26, cx + gw * 0.62, bottom + 40],
              fill=(40, 16, 40, 110))

    def body_points(scale):
        pts = []
        for i in range(41):        # dome, left to right over the top
            a = math.pi - i * math.pi / 40
            pts.append((cx + scale * (gw / 2) * math.cos(a),
                        dome_cy - scale * (gw / 2) * math.sin(a)))
        pts.append((cx + scale * gw / 2, bottom - 30))          # right side
        bumps = 4
        for b in range(bumps):     # wavy hem, right to left
            bx = cx + scale * gw / 2 - (b + 0.5) * (gw / bumps)
            for i in range(13):
                a = i * math.pi / 12
                pts.append((bx - (gw / bumps / 2) * math.cos(a) * scale / scale,
                            bottom - 30 + 30 * math.sin(a)))
        pts.append((cx - scale * gw / 2, bottom - 30))          # left side
        return pts

    d.polygon(body_points(1.055), fill=INK)        # thick black outline
    d.polygon(body_points(1.0), fill=(255, 255, 255))

    # sparkle eyes
    ey = dome_cy + int(H * 0.055)
    for ex in (cx - int(gw * 0.19), cx + int(gw * 0.19)):
        sparkle(d, ex, ey, 100, 66, 27, INK)

    # the round little hand, out to the right, holding the coin up
    hx, hy = cx + int(gw * 0.52), int(H * 0.60)
    coin_x, coin_y, coin_r = hx + 105, hy - 88, 126
    d.ellipse([coin_x - coin_r, coin_y - coin_r, coin_x + coin_r, coin_y + coin_r],
              fill=MAGENTA, outline=INK, width=9)
    star(d, coin_x, coin_y, 62, 26, (255, 255, 255))
    d.ellipse([hx - 54, hy - 54, hx + 54, hy + 54],
              fill=(255, 255, 255), outline=INK, width=10)
    sparkle(d, coin_x + 130, coin_y - 120, 44, 30, 12, (255, 255, 255))
    sparkle(d, coin_x - 150, coin_y - 60, 30, 20, 9, (255, 255, 255))


def fit_font(text, max_w, size):
    # leave room for the outline stroke on both sides of the text
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        if f.getlength(text) + 24 <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(FONT, size)


def caption(d, text, y, size, fill, max_w=int(W * 0.94)):
    f = fit_font(text, max_w, size)
    x = (W - f.getlength(text)) / 2
    d.text((x, y), text, font=f, fill=fill, stroke_width=9, stroke_fill=INK)


def main():
    img = Image.new("RGB", (W, H))
    sky_and_ground(img)
    sun(img)
    sea_glints(img)
    d = ImageDraw.Draw(img)
    palm(d, int(W * 0.015), int(H * 0.80), int(H * 0.52), int(W * 0.045), flip=1)
    palm(d, int(W * 0.995), int(H * 0.815), int(H * 0.44), int(W * 0.05), flip=-1)
    umbrella(img)
    ghost(img)

    d = ImageDraw.Draw(img)
    caption(d, "13 YEARS WAITING FOR GTA VI…", int(H * 0.030), 120, (255, 255, 255))
    caption(d, "MY AI AGENT ALREADY GOT PAID", int(H * 0.828), 100, (255, 255, 255))
    caption(d, "ON make.fun", int(H * 0.898), 106, (255, 210, 63))

    img = img.resize((W // S, H // S), Image.LANCZOS)
    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
