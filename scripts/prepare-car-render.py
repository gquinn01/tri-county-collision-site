#!/usr/bin/env python3
"""
Turns the licensed wireframe car render into the two assets the
We Fix It All band uses, and records the arithmetic while it does it.

WHY THIS IS A SCRIPT AND NOT A SESSION IN AN IMAGE EDITOR. Three
numbers decide whether the render is readable on the ink ground: the
crop box, the gamma, and the resulting median line luminance. Done by
hand they live in somebody's memory and cannot be checked or redone. Run
from here they are printed every time, and re-exporting the asset after
the ground changes is one command instead of an afternoon of clicking.

WHAT IT DOES, in order:

1. CROPS THE DEAD MARGIN. 43% of the licensed canvas is black nothing.
   The content sits at x 143..4980, y 596..2353 of 5123x2928, which is
   horizontally centred already and 10px off centre vertically, so a
   centred crop is within a pixel of the true bounding box and sips can
   do it without an offset crop it does not support.

2. PULLS THE BLACK POINT, which is the correction this asset actually
   needed. Its "black" background is not black: 54% of the licensed
   pixels are v=12 of 255, uniform across every corner and edge. Screen
   blended onto --ink that ground becomes rgb(29,38,49) against
   rgb(18,27,39), a 1.13:1 rectangle, so the render would have shown as
   a faintly lighter box sitting on the band. The black point is
   measured from the image rather than typed: the modal value plus a
   small margin for its own noise, which takes 74% of the pixels to
   exactly zero and makes the screen blend invisible.

   It pays for itself twice. A ground of uniform zero also compresses,
   where a ground dithering between 8 and 16 does not.

3. DOES NOT LIFT THE MIDTONES, and that is a measurement rather than an
   omission. The requirement is that the median line weight clears the
   3:1 a non-text graphic needs on ink. It already does, at both export
   sizes: the median line is 172 at 2160px and 105 at 1080px, which
   screen to 8.42:1 and 4.03:1. A gamma lift was written first, and
   then the numbers said the asset did not need one, so the code keeps
   the mechanism and applies it only if a future size or ground pushes
   the median under the floor. Applying a curve the image does not need
   would flatten the wireframe's tonal structure for nothing.

   THE ORDER STILL MATTERS. Downscaling averages a bright line against
   the black beside it, so lines get dimmer as the image gets smaller:
   the median is 172 at 2160px and 105 at 1080px, from the same source.
   Every measurement is therefore taken on the export, not the master.

4. PICKS THE JPEG QUALITY BY SEARCH, against the 250KB budget. PNG was
   tried first and lost: 479KB for the 2x even with a clean ground,
   because a dense wireframe is high-entropy data, and quantising to 16
   grey levels to fit banded the lines visibly. The JPEG objection was
   ringing reading as a glow around the lines, which is banned, so it
   was measured instead of argued: at the chosen quality the ground
   around a line sits at v=4 for 95% of it, which screens to 1.04:1
   against ink. That is not a glow, it is arithmetic below the
   threshold of sight.

5. MEASURES THE RESULT ON THE GROUND IT WILL SIT ON. The render is
   composited with `mix-blend-mode: screen` over --ink, so the contrast
   that decides readability is the screen composite against --ink, not
   the raw pixel value. Every number this prints is the composite.

THE GROUND IS BLACK AND THAT IS LOAD-BEARING. Screen blending leaves
the ink untouched wherever the asset is 0,0,0 and lightens only where
the lines are, so the asset needs no alpha channel, no background
removal, and stays a flat opaque file. If the band's ground ever stops
being dark, this stops working and the asset needs re-exporting with a
real alpha channel instead.

macOS only: crop and resize are `sips`. The level lift is pure Python
so that no image library is a dependency of this repo.

Usage:
    python3 scripts/prepare-car-render.py SOURCE.jpeg
    python3 scripts/prepare-car-render.py SOURCE.jpeg --target-median 120
"""

import argparse
import os
import struct
import subprocess
import sys
import tempfile
import zlib

# The ink ground the render is composited onto. Kept in step with --ink
# in docs/assets/site.css by hand, because this runs once per asset and
# a stale value here would show up in its own report.
INK = (18, 27, 39)

# The band is one .wrap wide: --wrap is 1120px and .wrap carries 20px of
# side padding, so the content column is 1080. The 2x file doubles it.
CSS_WIDTH = 1080
WIDTHS = (2160, 1080)

# Where the licensed canvas's content actually is, measured: content at
# x 143..4980, y 596..2353 of 5123x2928. Horizontally centred already and
# 10px off centre vertically, so a centred crop is within a pixel of the
# true box and sips needs no offset crop, which it does not support.
CROP_W, CROP_H = 4860, 1790

# A pixel this far above the measured ground is line rather than ground.
# Used only to pick the population whose median is reported.
LINE_FLOOR = 28

# How far above the modal ground value the black point goes, to swallow
# the ground's own dither. The licensed file's ground is v=12 with values
# from 8 to 16 around it, so 4 takes all of it to zero.
GROUND_MARGIN = 4

# What a non-text graphic needs. The render is a graphic, not text.
GRAPHIC_FLOOR = 3.0

# The asset budget, and the reason the quality is searched rather than set.
SIZE_BUDGET = 250 * 1024

OUT_DIR = os.path.join("docs", "assets", "img")
OUT_STEM = "car-xray-top"


def sips(*args):
    subprocess.run(["sips", *args], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def read_gray_png(path: str):
    """Decodes an 8-bit greyscale PNG to (width, height, bytearray).

    Only the colour type sips emits for this asset is handled, and
    anything else raises rather than guessing, because a silent misparse
    would produce a plausible-looking wrong asset.
    """
    d = open(path, "rb").read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    pos, idat, w, h = 8, b"", None, None
    while pos < len(d):
        ln = struct.unpack(">I", d[pos:pos + 4])[0]
        typ = d[pos + 4:pos + 8]
        if typ == b"IHDR":
            w, h, bd, ct = struct.unpack(">IIBB", d[pos + 8:pos + 18])
            if (bd, ct) != (8, 0):
                raise ValueError(f"expected 8-bit greyscale, got bitdepth {bd} type {ct}")
        elif typ == b"IDAT":
            idat += d[pos + 8:pos + 8 + ln]
        elif typ == b"IEND":
            break
        pos += 12 + ln
    raw = zlib.decompress(idat)
    out = bytearray(w * h)
    prev = bytearray(w)
    p = 0
    for y in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p + w]); p += w
        if f == 1:
            for i in range(1, w):
                line[i] = (line[i] + line[i - 1]) & 255
        elif f == 2:
            for i in range(w):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(w):
                a = line[i - 1] if i else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(w):
                a = line[i - 1] if i else 0
                c = prev[i - 1] if i else 0
                b = prev[i]
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        elif f != 0:
            raise ValueError(f"unknown PNG filter {f}")
        out[y * w:(y + 1) * w] = line
        prev = line
    return w, h, out


def write_gray_png(path: str, w: int, h: int, px: bytearray):
    """Re-encodes greyscale with per-row adaptive filtering. Only an
    intermediate: sips turns it into the JPEG that ships."""
    rows = bytearray()
    prev = bytearray(w)
    for y in range(h):
        line = px[y * w:(y + 1) * w]
        best = None
        for f in (0, 1, 2):
            if f == 0:
                d = bytes(line)
            elif f == 1:
                d = bytes([line[0]] + [(line[i] - line[i - 1]) & 255 for i in range(1, w)])
            else:
                d = bytes([(line[i] - prev[i]) & 255 for i in range(w)])
            cost = sum(min(x, 256 - x) for x in d)
            if best is None or cost < best[0]:
                best = (cost, f, d)
        rows.append(best[1])
        rows += best[2]
        prev = line
    comp = zlib.compress(bytes(rows), 9)

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n")
        fh.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0)))
        fh.write(chunk(b"IDAT", comp))
        fh.write(chunk(b"IEND", b""))


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def screen(v, ground=INK):
    """What `mix-blend-mode: screen` puts on the page for a grey of
    value v sitting on `ground`."""
    return tuple(round(255 - (255 - g) * (255 - v) / 255) for g in ground)


def modal_ground(px) -> int:
    """The value the background actually is. Taken as the mode because
    the ground is over half the pixels in a render like this, and read
    rather than assumed because assuming it was 0 is the mistake that
    would have shipped a grey box."""
    counts = [0] * 256
    for v in px:
        counts[v] += 1
    return counts.index(max(counts))


def levels_lut(black: int, gamma: float = 1.0):
    """Black point, then an optional gamma. 255 stays 255 and `black`
    and below go to 0, so nothing clips at the top and the ground is
    exactly the ground."""
    span = 255.0 - black
    inv = 1.0 / gamma
    out = bytearray(256)
    for v in range(256):
        x = max(0.0, (v - black) / span)
        out[v] = min(255, round(255 * (x ** inv)))
    return bytes(out)


def percentile(sorted_vals, pc):
    return sorted_vals[min(len(sorted_vals) - 1, int(len(sorted_vals) * pc))]


def solve_gamma(px, line_idx, black, target_contrast):
    """Bisects for the gamma whose median LINE pixel clears
    `target_contrast` on ink.

    The line population is fixed from the ORIGINAL pixels and carried
    through. Re-selecting it after the curve is applied was a real bug:
    a lift pushes hundreds of thousands of near-black antialiasing
    pixels above any fixed floor, they join the population, and the
    median falls instead of rising. It reported a lift as a darkening
    and it looked entirely plausible.
    """
    lo, hi = 1.0, 8.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lut = levels_lut(black, mid)
        med = percentile(sorted(lut[px[i]] for i in line_idx), 0.5)
        if contrast(screen(med), INK) < target_contrast:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--budget", type=int, default=SIZE_BUDGET)
    opts = ap.parse_args()

    if not os.path.isfile(opts.source):
        print(f"No such file: {opts.source}", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)

    tmp = tempfile.mkdtemp(prefix="carrender-")
    crop = os.path.join(tmp, "crop.jpeg")
    print(f"source          {opts.source}  ({os.path.getsize(opts.source):,} bytes)")
    sips("-c", str(CROP_H), str(CROP_W), opts.source, "--out", crop)
    print(f"cropped         {CROP_W} x {CROP_H}, the measured content box\n")

    results = []
    for width in WIDTHS:
        stage = os.path.join(tmp, f"{width}.jpeg")
        stage_png = os.path.join(tmp, f"{width}.png")
        sips("-Z", str(width), crop, "--out", stage)
        sips("-s", "format", "png", stage, "--out", stage_png)
        w, h, px = read_gray_png(stage_png)

        black = modal_ground(px) + GROUND_MARGIN
        line_idx = [i for i, v in enumerate(px) if v > black + LINE_FLOOR]
        med_before = percentile(sorted(px[i] for i in line_idx), 0.5)

        gamma = 1.0
        lut = levels_lut(black, gamma)
        med = percentile(sorted(lut[px[i]] for i in line_idx), 0.5)
        if contrast(screen(med), INK) < GRAPHIC_FLOOR:
            gamma = solve_gamma(px, line_idx, black, GRAPHIC_FLOOR * 1.3)
            lut = levels_lut(black, gamma)
            med = percentile(sorted(lut[px[i]] for i in line_idx), 0.5)

        corrected = bytearray(px).translate(lut)
        zeros = 100.0 * corrected.count(0) / len(corrected)
        ground_idx = [i for i, v in enumerate(corrected) if v == 0]

        corr_png = os.path.join(tmp, f"{width}-corr.png")
        write_gray_png(corr_png, w, h, corrected)

        name = f"{OUT_STEM}{'@2x' if width != CSS_WIDTH else ''}.jpg"
        out = os.path.join(OUT_DIR, name)
        chosen_q, size = None, None
        for q in range(85, 24, -5):
            sips("-s", "format", "jpeg", "-s", "formatOptions", str(q),
                 corr_png, "--out", out)
            size = os.path.getsize(out)
            if size <= opts.budget:
                chosen_q = q
                break
        # What the JPEG did to the ground, which is the only objection
        # to using one here. Measured on the pixels that were zero.
        check = os.path.join(tmp, f"{width}-check.png")
        sips("-s", "format", "png", out, "--out", check)
        _cw, _ch, done = read_gray_png(check)
        halo = sorted(done[i] for i in ground_idx)
        h95, hmax = percentile(halo, 0.95), halo[-1]
        med_final = percentile(sorted(done[i] for i in line_idx), 0.5)

        c_med = contrast(screen(med_final), INK)
        print(f"{name}")
        print(f"  {w} x {h}   {size:,} bytes ({size / 1024:.0f} KB) at quality {chosen_q}")
        print(f"  ground          modal v={black - GROUND_MARGIN}, black point {black}"
              f"  ->  {zeros:.1f}% of pixels exactly 0")
        print(f"  gamma           {gamma:.3f}"
              f"{'  (none needed, the median already clears)' if gamma == 1.0 else ''}")
        print(f"  median line     {med_before} -> {med_final}"
              f"   screened on ink {c_med:.2f}:1   (floor {GRAPHIC_FLOOR}:1)")
        print(f"  ground halo     p95 v={h95}, max v={hmax}"
              f"   screened {contrast(screen(h95), INK):.2f}:1   "
              f"(1.0 = invisible, a glow would show here)\n")
        results.append((name, size, c_med, chosen_q, contrast(screen(h95), INK)))

    worst = min(r[2] for r in results)
    biggest = max(r[1] for r in results)
    over = [r[0] for r in results if r[3] is None]
    halo_worst = max(r[4] for r in results)
    print(f"worst line contrast   {worst:.2f}:1   "
          f"{'ok' if worst >= GRAPHIC_FLOOR else 'UNDER THE FLOOR'}")
    print(f"largest file          {biggest / 1024:.0f} KB   "
          f"{'ok' if not over else 'OVER BUDGET: ' + ', '.join(over)}")
    print(f"worst ground halo     {halo_worst:.2f}:1   "
          f"{'ok, no visible glow' if halo_worst < 1.1 else 'VISIBLE, reconsider format'}")
    return 0 if (worst >= GRAPHIC_FLOOR and not over and halo_worst < 1.1) else 1


if __name__ == "__main__":
    sys.exit(main())
