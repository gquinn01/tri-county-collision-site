#!/usr/bin/env python3
"""
Turns the twelve manufacturer logos the shop publishes on its own live
homepage into the twelve monochrome marks the brand strip ships, and
prints every number it used.

Built to the precedent of scripts/prepare-repair-photos.py and
scripts/prepare-car-render.py: the irreversible decisions live in a
script that can be re-run and audited, not in somebody's image editor
and memory.

WHERE THE SOURCES COME FROM, AND WHY THAT MATTERS. They are the client's
own published files, read off https://tricountycollision.com/ on
2026-09-17, one per brand:

    logo-subaru.png    Logo-nissan.jpg    Logo-kia.jpg
    Logo-jeep.jpg      Logo-infiniti.jpg  Logo-hyundai.jpg
    Logo-gm.jpg        Logo-ford.jpg      Logo-dodge.jpg
    Logo-chrysler.jpg  logo-acura.png     logo-honda.png

all under /wp-content/uploads/. They are not committed here: this
script takes --src and the twelve files are fetched from those URLs.
AFTER CUTOVER THOSE URLS STOP RESOLVING, and the complete archive of
the WordPress site that CLAUDE.md requires before it goes dark is then
the only copy. If this script ever has to be re-run after that day, the
sources come out of the archive.

The marks themselves are the
manufacturers' trademarks and are used here the way the shop already
uses them: to say which brands it is certified for. That claim is the
owner's and it is in the claims list, not in this script.

TWELVE, NOT THE FOURTEEN THE LIVE STRIP CARRIES. The live carousel shows
fourteen marks, the twelve plus RAM and Fiat, while the live site's own
prose says a dozen and our pages say twelve in four places. The strip
ships what the site claims in words. The discrepancy is an owner
question, recorded in proposed-changes.md; if the shop is certified for
fourteen, the count moves to fourteen everywhere in one commit and
scripts/audit.py's brand-count check is what makes that one commit
rather than four.

WHAT IT DOES, in order, per mark:

1. READS THE PROVENANCE FIRST, through the same reader the audit uses,
   and REFUSES TO PROCESS a file that carries an AI tell. Every asset
   that enters this repo gets its metadata read before it lands, and a
   file that never becomes an output never reaches docs/ to be caught
   later.

2. DECODES the source. PNG here rather than JPEG for the ones that
   arrived as JPEG, because sips converts and this script does not
   carry a JPEG decoder. Palette PNGs are expanded; the Subaru mark is
   one.

3. CONVERTS TO AN ALPHA MASK, which is the whole treatment. The mark's
   luminance becomes opacity: white ground goes fully transparent, the
   darkest ink goes fully opaque, everything between lands in between,
   so a logo's internal tones survive as tones rather than being
   posterised into a silhouette. The Ford script stays legible inside
   its oval because the white script is transparent, not white.

   THE PIXELS ARE BLACK AND THE STYLESHEET OWNS THE TONE. The output is
   a grey+alpha PNG whose grey is 0, so the mark's darkness on the page
   is one opacity value in site.css rather than twelve baked greys in
   twelve files. Changing how dark the strip sits is then a one-number
   change and cannot leave eleven files stale. It is also the palette
   note's own rule: a ground or a tone that must agree in more than one
   place is one value plus a derivation.

   IT IS GROUND-INDEPENDENT ON PURPOSE. Compositing the marks onto
   --silver would have baked the page's ground into twelve files, and
   the palette note records that this exact mistake has already been
   made once on this site with ten rgba() washes.

4. TRIMS to the mark's own bounding box, at an alpha threshold rather
   than a colour one, so JPEG ringing around a logo does not pad the
   box by a few pixels and make one mark visually smaller than its
   neighbours.

5. NORMALISES THE HEIGHT. Every mark ships at the same pixel height and
   whatever width its own proportions give it. Consistent height is the
   live strip's treatment and it is what makes a row of marks read as
   one row rather than as twelve decisions.

6. DOWNSCALES with a box filter, which is the right filter for going
   down and costs nothing to write. Never upscales: a mark smaller than
   the target height ships at its own size rather than being blown up.

7. WRITES no metadata at all. The writer emits IHDR, IDAT and IEND and
   nothing else, so there is nothing to strip afterwards and nothing to
   leak.

8. VERIFIES, and fails rather than shipping: every source clean, every
   output decodable, every output the target height, and the whole
   strip inside its byte budget.
"""

import argparse
import importlib.util
import os
import struct
import subprocess
import sys
import tempfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = os.path.join(REPO, "docs", "assets", "img", "brands")

# THE TWELVE, in the order the strip prints them, with the source file
# each one comes from. The order is the live strip's own order with RAM
# and Fiat removed, so a reader comparing the two sees the same run.
BRANDS = [
    ("subaru", "logo-subaru.png", "Subaru"),
    ("nissan", "Logo-nissan.jpg", "Nissan"),
    ("kia", "Logo-kia.jpg", "Kia"),
    ("jeep", "Logo-jeep.jpg", "Jeep"),
    ("infiniti", "Logo-infiniti.jpg", "INFINITI"),
    ("hyundai", "Logo-hyundai.jpg", "Hyundai"),
    ("gm", "Logo-gm.jpg", "GM"),
    ("ford", "Logo-ford.jpg", "Ford"),
    ("dodge", "Logo-dodge.jpg", "Dodge"),
    ("chrysler", "Logo-chrysler.jpg", "Chrysler"),
    ("acura", "logo-acura.png", "Acura"),
    ("honda", "logo-honda.png", "Honda"),
]

# ONE SOURCE IS A BADGE RATHER THAN A MARK, and it is cropped to its
# mark. The GM file is the "GM CERTIFIED Collision Repair Center"
# badge: the GM box sits above ten empty rows and then two lines of
# fine print. At the height this strip renders, that print is three
# pixels tall and reads as a grey smudge, which is worse than no text
# at all and worse for GM than for any other brand in the row.
#
# So the mark is taken and the print is left. It removes nothing the
# site claims: "factory-certified for 12 vehicle brands", GM among
# them, is published in words on /collision-repair/ and is in the
# claims list where the owner can confirm it. A claim belongs in text
# that a person and a crawler can both read, not in three pixels.
#
# The box is in TRIMMED coordinates and it was measured off the mask's
# own row profile, not guessed: ink runs to row 91, rows 92 to 101 are
# empty, the print starts at 102.
CROP_AFTER_TRIM = {
    "gm": (0, 0, None, 92),
}

# 2x of the 30px the strip renders at, so the marks are sharp on a
# retina screen and the <img> width and height attributes are half
# these numbers.
TARGET_H = 60

# The knockout. Luminance at or above WHITE_L is ground and goes fully
# transparent; at or below BLACK_L is ink and goes fully opaque. The
# white point is not 1.0 because these arrived as JPEGs and a JPEG's
# white is 252 to 255 rather than 255 flat.
WHITE_L = 0.955
BLACK_L = 0.06

# Below this alpha a pixel is not part of the mark for trimming
# purposes. Eight of 255 is under half a percent and is comfortably
# above JPEG ringing.
TRIM_A = 8

# The whole strip, twelve files. Generous for what these are, and it is
# a ceiling rather than a target: the run below comes in far under it.
BUDGET = 150 * 1024


def load_audit():
    spec = importlib.util.spec_from_file_location(
        "audit", os.path.join(HERE, "audit.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def to_png(src: str, tmp: str) -> str:
    """Anything sips can read becomes an 8-bit PNG this script can."""
    if src.lower().endswith(".png"):
        return src
    out = os.path.join(tmp, os.path.basename(src) + ".png")
    subprocess.run(["sips", "-s", "format", "png", src, "--out", out],
                   check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    return out


def read_png(path: str):
    """8-bit PNG to (w, h, channels, bytearray).

    Handles greyscale, RGB, RGBA and PALETTE, because the Subaru mark
    arrived as a palette PNG and a reader that raises on one colour
    type would have sent somebody to an image editor.
    """
    d = open(path, "rb").read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    pos, idat, plte, trns = 8, b"", b"", b""
    w = h = bd = ct = None
    while pos < len(d):
        ln = struct.unpack(">I", d[pos:pos + 4])[0]
        typ = d[pos + 4:pos + 8]
        if typ == b"IHDR":
            w, h, bd, ct = struct.unpack(">IIBB", d[pos + 8:pos + 18])
            interlace = d[pos + 20]
            if interlace:
                raise ValueError(f"{path}: interlaced PNG not handled")
        elif typ == b"PLTE":
            plte = d[pos + 8:pos + 8 + ln]
        elif typ == b"tRNS":
            trns = d[pos + 8:pos + 8 + ln]
        elif typ == b"IDAT":
            idat += d[pos + 8:pos + 8 + ln]
        elif typ == b"IEND":
            break
        pos += 12 + ln
    if bd != 8 or ct not in (0, 2, 3, 4, 6):
        raise ValueError(f"{path}: bitdepth {bd} colour type {ct} not handled")
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct]
    raw = zlib.decompress(idat)
    stride = w * ch
    out = bytearray(w * h * ch)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if f == 1:
            for i in range(ch, stride):
                line[i] = (line[i] + line[i - ch]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i - ch] if i >= ch else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - ch] if i >= ch else 0
                c = prev[i - ch] if i >= ch else 0
                b = prev[i]
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        elif f != 0:
            raise ValueError(f"unknown PNG filter {f}")
        out[y * stride:(y + 1) * stride] = line
        prev = line
    if ct == 3:
        rgba = bytearray(w * h * 4)
        for i in range(w * h):
            idx = out[i]
            rgba[i * 4:i * 4 + 3] = plte[idx * 3:idx * 3 + 3]
            rgba[i * 4 + 3] = trns[idx] if idx < len(trns) else 255
        return w, h, 4, rgba
    return w, h, ch, out


def lin(c: int) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_alpha(w: int, h: int, ch: int, px: bytearray) -> bytearray:
    """Luminance becomes opacity, over white.

    A source pixel that is already transparent is ground: the Subaru
    and Acura files carry alpha, and a transparent pixel there means
    the same thing a white one means in the JPEGs.
    """
    lut = [lin(v) for v in range(256)]
    a = bytearray(w * h)
    for i in range(w * h):
        o = i * ch
        if ch == 1:
            r = g = b = px[o]
            al = 255
        elif ch == 2:
            r = g = b = px[o]
            al = px[o + 1]
        elif ch == 3:
            r, g, b = px[o], px[o + 1], px[o + 2]
            al = 255
        else:
            r, g, b = px[o], px[o + 1], px[o + 2]
            al = px[o + 3]
        lum = 0.2126 * lut[r] + 0.7152 * lut[g] + 0.0722 * lut[b]
        # an alpha of its own composites the pixel over white first
        if al != 255:
            lum = lum * (al / 255.0) + (1.0 - al / 255.0)
        t = (WHITE_L - lum) / (WHITE_L - BLACK_L)
        t = 0.0 if t < 0 else (1.0 if t > 1 else t)
        a[i] = int(round(t * 255))
    return a


def trim(w: int, h: int, a: bytearray):
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        row = y * w
        for x in range(w):
            if a[row + x] >= TRIM_A:
                if x < x0:
                    x0 = x
                if x > x1:
                    x1 = x
                if y < y0:
                    y0 = y
                if y > y1:
                    y1 = y
    if x1 < 0:
        raise ValueError("the mask is empty: nothing survived the knockout")
    nw, nh = x1 - x0 + 1, y1 - y0 + 1
    out = bytearray(nw * nh)
    for y in range(nh):
        out[y * nw:(y + 1) * nw] = a[(y + y0) * w + x0:(y + y0) * w + x0 + nw]
    return nw, nh, out


def box_scale(w: int, h: int, a: bytearray, nw: int, nh: int):
    """Area-average downscale. Never called to go up."""
    out = bytearray(nw * nh)
    for y in range(nh):
        sy0, sy1 = y * h // nh, max(y * h // nh + 1, (y + 1) * h // nh)
        for x in range(nw):
            sx0, sx1 = x * w // nw, max(x * w // nw + 1, (x + 1) * w // nw)
            tot = n = 0
            for sy in range(sy0, sy1):
                base = sy * w
                for sx in range(sx0, sx1):
                    tot += a[base + sx]
                    n += 1
            out[y * nw + x] = (tot + n // 2) // n
    return out


def write_gray_alpha_png(path: str, w: int, h: int, a: bytearray):
    """Colour type 4: grey plus alpha, grey pinned at 0.

    Rows are written with the Up filter, which on a mask of mostly
    identical rows compresses far better than no filter and costs two
    lines to implement.
    """
    stride = w * 2
    raw = bytearray()
    prev = bytearray(stride)
    for y in range(h):
        line = bytearray(stride)
        for x in range(w):
            line[x * 2] = 0
            line[x * 2 + 1] = a[y * w + x]
        raw.append(2)
        raw.extend(bytes((line[i] - prev[i]) & 255 for i in range(stride)))
        prev = line
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 4, 0, 0, 0)))
        f.write(chunk(b"IDAT", comp))
        f.write(chunk(b"IEND", b""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True,
                    help="directory holding the twelve files fetched from "
                         "the live site")
    ap.add_argument("--out", default=OUT_DIR)
    args = ap.parse_args()

    audit = load_audit()
    failures = []
    os.makedirs(args.out, exist_ok=True)

    print("PROVENANCE, read before anything is done to any file")
    print(f"  {'file':<22} {'bytes':>7}  {'DigitalSourceType':<20} "
          f"{'CreatorTool':<28} verdict")
    srcs = {}
    for slug, fname, _label in BRANDS:
        p = os.path.join(args.src, fname)
        if not os.path.exists(p):
            failures.append(f"{slug}: source {fname} is missing")
            continue
        r = audit.read_asset_provenance(p)
        verdict = "AI: " + "; ".join(r["reasons"]) if r["reasons"] else "clean"
        print(f"  {fname:<22} {r['bytes']:>7}  {(r['source_type'] or '-'):<20} "
              f"{(r['tool'] or '-')[:28]:<28} {verdict}")
        if r["reasons"]:
            failures.append(f"{slug}: {verdict}")
        srcs[slug] = p
    if failures:
        print("\nFAILED before processing:")
        for f in failures:
            print("  " + f)
        return 1

    print(f"\nMARKS, normalised to {TARGET_H}px tall "
          f"({TARGET_H // 2}px on the page at 2x)")
    print(f"  {'brand':<10} {'source':<12} {'trimmed':<12} {'shipped':<12} "
          f"{'bytes':>7}  note")
    total = 0
    with tempfile.TemporaryDirectory() as tmp:
        for slug, fname, label in BRANDS:
            w, h, ch, px = read_png(to_png(srcs[slug], tmp))
            a = to_alpha(w, h, ch, px)
            tw, th, ta = trim(w, h, a)
            cropped = ""
            if slug in CROP_AFTER_TRIM:
                x0, y0, x1, y1 = CROP_AFTER_TRIM[slug]
                x1 = tw if x1 is None else x1
                y1 = th if y1 is None else y1
                cut = bytearray((x1 - x0) * (y1 - y0))
                for y in range(y0, y1):
                    cut[(y - y0) * (x1 - x0):(y - y0 + 1) * (x1 - x0)] = \
                        ta[y * tw + x0:y * tw + x1]
                tw, th, ta = trim(x1 - x0, y1 - y0, cut)
                cropped = "badge cropped to its mark, "
            if th > TARGET_H:
                nh = TARGET_H
                nw = max(1, int(round(tw * TARGET_H / th)))
                ta = box_scale(tw, th, ta, nw, nh)
                note = cropped + f"scaled {th}->{nh}"
            else:
                nw, nh = tw, th
                note = cropped + "smaller than target, NOT upscaled"
            out = os.path.join(args.out, f"{slug}.png")
            write_gray_alpha_png(out, nw, nh, ta)
            size = os.path.getsize(out)
            total += size
            # verify: it decodes, it is the height asked for, it has ink
            vw, vh, vch, vpx = read_png(out)
            if (vw, vh, vch) != (nw, nh, 2):
                failures.append(f"{slug}: output did not decode as written")
            if th > TARGET_H and vh != TARGET_H:
                failures.append(f"{slug}: output is {vh}px tall, not {TARGET_H}")
            if max(vpx[1::2]) < 200:
                failures.append(f"{slug}: no pixel is near opaque, the mask is "
                                f"too faint to be a mark")
            print(f"  {label:<10} {f'{w}x{h}':<12} {f'{tw}x{th}':<12} "
                  f"{f'{nw}x{nh}':<12} {size:>7}  {note}")

    print(f"\n  {'TOTAL':<10} {'':<12} {'':<12} {'':<12} {total:>7}  "
          f"budget {BUDGET}, "
          f"{'ok' if total <= BUDGET else 'OVER'}")
    if total > BUDGET:
        failures.append(f"the strip is {total} bytes against a {BUDGET} budget")

    if failures:
        print("\nFAILED:")
        for f in failures:
            print("  " + f)
        return 1
    print("\nAll twelve marks written and verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
