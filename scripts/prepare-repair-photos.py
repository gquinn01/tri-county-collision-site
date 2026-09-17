#!/usr/bin/env python3
"""
Turns the shop's own before/after repair photographs into the ten
frames the Real Repairs band ships, and prints every number it used.

Built to the precedent set by scripts/prepare-car-render.py: the
irreversible decisions live in a script that can be re-run and audited,
not in somebody's image editor and memory.

WHAT IT DOES, in order, per frame:

1. RESIZES to the target width. Never upscales: the width is capped at
   the smaller native width of the PAIR, so both frames of a pair ship
   at identical pixel dimensions and the crossfade overlays exactly.

2. CROPS ONLY WHERE A PAIR'S ASPECTS DISAGREE. Four of the five pairs
   already match. job5's before is 4:3 and its after is 16:9, so the
   before is cropped to 16:9. THE CROP IS TAKEN OFF THE TOP AND BOTTOM
   and its offset is recorded here, because the damage sits mid frame
   and what comes off is building above and gravel below. No crop on
   this site hides damage or flatters a repair; the honesty of the pair
   is the only reason the section exists.

3. REDACTS. Every license plate and every windshield sticker carrying
   identifying numbers is destroyed, not softened. All ten frames were
   inspected at magnification before this list was written, and three
   regions were found. The other seven are clean, mostly because
   Pennsylvania issues rear plates only and those frames face forward.

   THE METHOD IS PIXELATE THEN BLUR, in that order, and the order is
   the point. Averaging into large blocks throws the information away;
   blurring afterwards only stops the blocks looking like a deliberate
   mosaic. A Gaussian blur alone can sometimes be partly undone, and a
   plate is not the thing to be clever about.

4. STRIPS METADATA STRUCTURALLY, which re-encoding does NOT do. The
   sources had already lost their EXIF to the platform they came
   through, checked rather than assumed: no GPS and no Exif marker in
   any of the ten. But sips PUTS METADATA BACK when it writes a JPEG.
   Its output carried an APP1 Exif block, an APP1 XMP packet, an APP13
   Photoshop block and an APP2 ICC profile, none of which was in the
   input. So every APP1 through APP15 segment and every comment is
   walked and dropped, leaving APP0 JFIF and the coding markers.

   The check is then structural rather than a text search. Counting the
   string "exif" in a JPEG cannot tell a harmless orientation tag from a
   GPS record, and it false-positives on compressed pixel data: the
   first version of this script reported "gps:1" on a frame whose
   metadata was clean. Walking the marker segments answers exactly.

5. LEAVES A FRAME ALONE WHEN IT NEEDS NOTHING. A frame with no crop, no
   redaction and no resize is copied with its metadata stripped and
   never re-compressed, because re-encoding an already-compressed
   photograph only compounds the loss. Three of the ten take this path.

6. VERIFIES, and fails rather than shipping: no APP1-APP15 or comment
   segment survives, the redaction destroyed local detail, the pair's
   dimensions match exactly, and the file is inside budget.

   NO OUTPUT MAY BE LARGER THAN ITS SOURCE. A re-encode that grows the
   file is adding bits, not detail. The first run inflated a 98KB
   source into a 139KB output at quality 68, which is worse on both
   counts, so the per-frame budget is capped by the source's own size.

THE SOURCES DO NOT LIVE IN THIS REPO AND MUST NOT. They are the
client's originals, they carry unredacted plates, and this repository
is public. SOURCE_DIR points at wherever the client's copies are; only
the redacted, stripped output is committed. That is also why this
script cannot be re-run from a clean checkout, which is a deliberate
trade: the alternative is committing readable plates.

Usage:
    python3 scripts/prepare-repair-photos.py SOURCE_DIR
    python3 scripts/prepare-repair-photos.py SOURCE_DIR --budget 150000
"""

import argparse
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

OUT_DIR = os.path.join("docs", "assets", "img", "repairs")

# The widest a card is ever rendered is 526 CSS px at desktop, so 2x is
# 1052. Capped per pair at the smaller native width, never upscaled.
MAX_WIDTH = 1050

# Per frame. Ten frames lazy-loading below the fold; the total is
# reported so the page cost is a number rather than a feeling.
SIZE_BUDGET = 150 * 1024

# Never encode a photograph below this. A gallery of repairs is the
# evidence the section exists for, and quality 40 foliage looks like a
# different trade. If a pair cannot meet the budget at this quality it
# loses WIDTH instead, which costs sharpness on a retina screen and
# nothing else. Width steps apply to the PAIR, never to one frame, or
# the crossfade would stop registering.
QUALITY_FLOOR = 52
WIDTH_STEPS = (1.0, 0.90, 0.81, 0.73)

# A redacted region has to lose most of its local detail. Measured as
# mean absolute difference between neighbouring pixels inside the box,
# before and after. Anything under this ratio means the blur did not
# take, which would ship a readable plate.
MAX_DETAIL_REMAINING = 0.25

# (slug, vehicle, before_source, after_source, crop, redactions)
#
# `crop` is (top_fraction, bottom_fraction) taken off a frame, or None.
# `redactions` maps "before"/"after" to a list of (x0, y0, x1, y1) in
# fractions of that frame, AFTER any crop.
#
# THE THREE REDACTIONS, and what each one is:
#   job3 after  the green Pennsylvania inspection sticker on the
#               windshield, which carries characters
#   job4 after  the rear plate at the left edge, readable, with its
#               registration sticker
#   job5 after  the rear plate, in shadow and faint, with a
#               registration sticker still visible
PAIRS = [
    ("job1", "Jeep Grand Cherokee L",
     "494205493_1532755301327952_7153971413320167501_n.jpg",
     "494116256_1532755314661284_6059890045038476746_n (1).jpg",
     {}, {}),
    ("job2", "Dodge Grand Caravan",
     "512110097_23935414566078447_3642043474801073806_n.jpg",
     "510981164_23936370802649490_8284221120494983470_n.jpg",
     {}, {}),
    ("job3", "BMW 5 Series",
     "494062418_1534240677846081_8306642657866217258_n.jpg",
     "494264414_1535430581060424_5573845858472557498_n (1).jpg",
     {}, {"after": [(0.592, 0.230, 0.668, 0.277)]}),
    ("job4", "Nissan Murano",
     "504496869_18272281837285996_4698946999816394701_n.jpg",
     "509946056_1579376289999186_7069959255358919205_n (1).jpg",
     {}, {"after": [(0.000, 0.398, 0.050, 0.558)]}),
    ("job5", "Mercedes CLE 300",
     "520456767_1602717714331710_5557557647920193621_n.jpg",
     "526797785_1615702756366539_5549957451569432077_n.jpg",
     # 4:3 down to 16:9. More comes off the top, which is building and
     # sky, than off the bottom, which still holds the lower bumper.
     {"before": (0.185, 0.065)},
     {"after": [(0.422, 0.596, 0.518, 0.668)]}),
]


def sips(*args):
    subprocess.run(["sips", *args], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def dims(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                         capture_output=True, text=True, check=True).stdout
    w = h = None
    for line in out.splitlines():
        if "pixelWidth" in line:
            w = int(line.split()[-1])
        elif "pixelHeight" in line:
            h = int(line.split()[-1])
    return w, h


def read_png(path):
    """8-bit PNG to (w, h, channels, bytearray). Handles the colour
    types sips emits and raises on anything else rather than guessing."""
    d = open(path, "rb").read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    pos, idat, w, h, bd, ct = 8, b"", None, None, None, None
    while pos < len(d):
        ln = struct.unpack(">I", d[pos:pos + 4])[0]
        typ = d[pos + 4:pos + 8]
        if typ == b"IHDR":
            w, h, bd, ct = struct.unpack(">IIBB", d[pos + 8:pos + 18])
        elif typ == b"IDAT":
            idat += d[pos + 8:pos + 8 + ln]
        elif typ == b"IEND":
            break
        pos += 12 + ln
    if bd != 8 or ct not in (0, 2, 6):
        raise ValueError(f"{path}: bitdepth {bd} colour type {ct} not handled")
    ch = {0: 1, 2: 3, 6: 4}[ct]
    raw = zlib.decompress(idat)
    stride = w * ch
    out = bytearray(w * h * ch)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
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
    return w, h, ch, out


def write_rgb_png(path, w, h, px):
    rows = bytearray()
    for y in range(h):
        rows.append(0)
        rows += px[y * w * 3:(y + 1) * w * 3]
    comp = zlib.compress(bytes(rows), 6)

    def chunk(t, d):
        return (struct.pack(">I", len(d)) + t + d
                + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF))

    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n")
        fh.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)))
        fh.write(chunk(b"IDAT", comp))
        fh.write(chunk(b"IEND", b""))


def to_rgb(w, h, ch, px):
    """Normalises whatever sips gave us to three channels."""
    if ch == 3:
        return bytearray(px)
    out = bytearray(w * h * 3)
    for i in range(w * h):
        if ch == 1:
            v = px[i]
            out[i * 3] = out[i * 3 + 1] = out[i * 3 + 2] = v
        else:
            out[i * 3:i * 3 + 3] = px[i * ch:i * ch + 3]
    return out


def crop_rows(w, h, px, top_f, bottom_f):
    y0 = int(h * top_f)
    y1 = h - int(h * bottom_f)
    return w, y1 - y0, bytearray(px[y0 * w * 3:y1 * w * 3])


def detail(px, w, box):
    """Mean absolute difference between neighbouring pixels in a box.
    A proxy for how much readable structure is in there."""
    x0, y0, x1, y1 = box
    total = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1 - 1):
            a = (y * w + x) * 3
            b = a + 3
            total += abs(px[a] - px[b]) + abs(px[a + 1] - px[b + 1]) + abs(px[a + 2] - px[b + 2])
            n += 3
    return (total / n) if n else 0.0


def redact(px, w, h, frac_box):
    """Pixelate into big blocks, then blur the blocks. Returns the pixel
    box that was treated and the detail measured before and after."""
    x0 = max(0, int(frac_box[0] * w)); y0 = max(0, int(frac_box[1] * h))
    x1 = min(w, int(frac_box[2] * w)); y1 = min(h, int(frac_box[3] * h))
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"empty redaction box {frac_box}")
    box = (x0, y0, x1, y1)
    before = detail(px, w, box)

    # Blocks sized to the region, floored so a small box still loses its
    # characters: a plate's glyph is a few percent of its width.
    bw = max(6, (x1 - x0) // 6)
    bh = max(6, (y1 - y0) // 4)
    for by in range(y0, y1, bh):
        for bx in range(x0, x1, bw):
            ex, ey = min(bx + bw, x1), min(by + bh, y1)
            rs = gs = bs = cnt = 0
            for y in range(by, ey):
                base = (y * w + bx) * 3
                for i in range(0, (ex - bx) * 3, 3):
                    rs += px[base + i]; gs += px[base + i + 1]; bs += px[base + i + 2]
                    cnt += 1
            r, g, b = rs // cnt, gs // cnt, bs // cnt
            for y in range(by, ey):
                base = (y * w + bx) * 3
                for i in range(0, (ex - bx) * 3, 3):
                    px[base + i] = r; px[base + i + 1] = g; px[base + i + 2] = b

    # Three box-blur passes over the same region, which is enough to
    # take the block edges off without recovering anything.
    rad = 3
    for _ in range(3):
        snap = bytearray(px)
        for y in range(y0, y1):
            for x in range(x0, x1):
                rs = gs = bs = cnt = 0
                for dy in range(-rad, rad + 1):
                    yy = min(y1 - 1, max(y0, y + dy))
                    for dx in range(-rad, rad + 1):
                        xx = min(x1 - 1, max(x0, x + dx))
                        o = (yy * w + xx) * 3
                        rs += snap[o]; gs += snap[o + 1]; bs += snap[o + 2]
                        cnt += 1
                o = (y * w + x) * 3
                px[o] = rs // cnt; px[o + 1] = gs // cnt; px[o + 2] = bs // cnt

    return box, before, detail(px, w, box)


def strip_app_segments(src, dst):
    """Rewrites a JPEG keeping APP0 JFIF and the coding markers, and
    dropping every APP1-APP15 segment and every comment.

    This is what actually removes metadata. Re-encoding does not: sips
    writes its own Exif, XMP, Photoshop and ICC blocks into the output
    regardless of what the input carried.
    """
    d = open(src, "rb").read()
    out = bytearray(d[:2])
    i, dropped = 2, []
    while i < len(d) - 1:
        if d[i] != 0xFF:
            out += d[i:]
            break
        m = d[i + 1]
        if m == 0xDA:              # start of scan, the rest is image
            out += d[i:]
            break
        if m == 0xD9:
            out += d[i:]
            break
        ln = int.from_bytes(d[i + 2:i + 4], "big")
        seg = d[i:i + 2 + ln]
        is_app = 0xE0 <= m <= 0xEF
        is_jfif = m == 0xE0 and d[i + 4:i + 8] == b"JFIF"
        if (is_app and not is_jfif) or m == 0xFE:
            tag = d[i + 4:i + 14].split(b"\x00")[0].decode("latin-1", "replace")
            dropped.append((f"APP{m - 0xE0}" if is_app else "COM", ln, tag))
        else:
            out += seg
        i += 2 + ln
    open(dst, "wb").write(bytes(out))
    return dropped


def app_segments(path):
    """Every metadata segment left in a finished file.

    APP0 JFIF is NOT metadata and is not reported: it is the density
    and thumbnail header every baseline JPEG carries, it identifies
    nobody, and the stripper keeps it on purpose. The first version of
    this check counted it and failed all ten frames, which is a check
    calling its own correct output a defect.
    """
    d = open(path, "rb").read()
    i, found = 2, []
    while i < len(d) - 1:
        if d[i] != 0xFF:
            break
        m = d[i + 1]
        if m in (0xDA, 0xD9):
            break
        ln = int.from_bytes(d[i + 2:i + 4], "big")
        is_jfif = m == 0xE0 and d[i + 4:i + 8] == b"JFIF"
        if (0xE0 <= m <= 0xEF and not is_jfif) or m == 0xFE:
            tag = d[i + 4:i + 14].split(b"\x00")[0].decode("latin-1", "replace")
            found.append((f"APP{m - 0xE0}" if m != 0xFE else "COM", ln, tag))
        i += 2 + ln
    return found


def downscale(px, w, h, neww):
    """Box-average downscale. Used to step a PAIR down in width when it
    cannot meet the budget at the quality floor, working on the already
    decoded and redacted pixels so nothing is re-read or re-blurred."""
    if neww >= w:
        return w, h, px
    newh = max(1, round(h * neww / w))
    out = bytearray(neww * newh * 3)
    for y in range(newh):
        sy0 = y * h // newh
        sy1 = max(sy0 + 1, (y + 1) * h // newh)
        for x in range(neww):
            sx0 = x * w // neww
            sx1 = max(sx0 + 1, (x + 1) * w // neww)
            r = g = b = n = 0
            for yy in range(sy0, sy1):
                base = (yy * w + sx0) * 3
                for i in range(0, (sx1 - sx0) * 3, 3):
                    r += px[base + i]; g += px[base + i + 1]; b += px[base + i + 2]
                    n += 1
            o = (y * neww + x) * 3
            out[o] = r // n; out[o + 1] = g // n; out[o + 2] = b // n
    return neww, newh, out


def metadata_markers(path):
    """What identifying metadata the finished file still carries."""
    raw = open(path, "rb").read()
    low = raw.lower()
    return {
        "Exif": low.count(b"exif"),
        "GPS": low.count(b"gps"),
        "XMP": low.count(b"<x:xmpmeta"),
        "ICC": raw.count(b"ICC_PROFILE"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_dir")
    ap.add_argument("--budget", type=int, default=SIZE_BUDGET)
    opts = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="repairphotos-")
    total = 0
    failures = []
    manifest = []

    for slug, vehicle, bsrc, asrc, crops, reds in PAIRS:
        print(f"\n{slug}  {vehicle}")
        paths = {"before": os.path.join(opts.source_dir, bsrc),
                 "after": os.path.join(opts.source_dir, asrc)}
        for role, pth in paths.items():
            if not os.path.isfile(pth):
                print(f"  MISSING {role}: {pth}", file=sys.stderr)
                return 1

        native = {r: dims(pth) for r, pth in paths.items()}
        srcsize = {r: os.path.getsize(pth) for r, pth in paths.items()}
        width = min(MAX_WIDTH, native["before"][0], native["after"][0])
        print(f"  native      before {native['before'][0]}x{native['before'][1]} "
              f"({srcsize['before'] // 1024}KB), after {native['after'][0]}x"
              f"{native['after'][1]} ({srcsize['after'] // 1024}KB)")

        # A frame that needs nothing done to it is not re-compressed.
        untouched = {
            r: (r not in crops and not reds.get(r) and native[r][0] == width)
            for r in ("before", "after")
        }

        frames = {}
        for role in ("before", "after"):
            if untouched[role]:
                print(f"  {role:6s}    no crop, no redaction, no resize: copied and "
                      f"stripped, never re-compressed")
                frames[role] = None
                continue
            stage = os.path.join(tmp, f"{slug}-{role}.jpg")
            sips("-Z", str(width), paths[role], "--out", stage)
            spng = os.path.join(tmp, f"{slug}-{role}.png")
            sips("-s", "format", "png", stage, "--out", spng)
            w, h, ch, raw = read_png(spng)
            px = to_rgb(w, h, ch, raw)

            if role in crops:
                t, b = crops[role]
                w, h, px = crop_rows(w, h, px, t, b)
                print(f"  {role:6s}    cropped {t * 100:.1f}% off the top and "
                      f"{b * 100:.1f}% off the bottom  ->  {w}x{h}  "
                      f"(building above, gravel below, no damage)")

            for fb in reds.get(role, []):
                box, d0, d1 = redact(px, w, h, fb)
                ratio = (d1 / d0) if d0 else 0.0
                ok = ratio <= MAX_DETAIL_REMAINING
                print(f"  {role:6s}    REDACTED {box[2] - box[0]}x{box[3] - box[1]}px at "
                      f"({box[0]},{box[1]})   local detail {d0:.1f} -> {d1:.1f}, "
                      f"{ratio * 100:.1f}% left   "
                      f"{'ok, destroyed' if ok else 'FAIL, still legible'}")
                if not ok:
                    failures.append(f"{slug}-{role}: redaction left {ratio * 100:.0f}% detail")

            frames[role] = (w, h, px)

        # Both frames of a pair must be pixel-identical in size or the
        # crossfade drifts. Rounding alone put job5 one row apart.
        live = {r: f for r, f in frames.items() if f}
        if len(live) == 2:
            hb, ha = live["before"][1], live["after"][1]
            if hb != ha:
                keep = min(hb, ha)
                for r in ("before", "after"):
                    w, h, px = frames[r]
                    if h != keep:
                        frames[r] = (w, keep, bytearray(px[:w * keep * 3]))
                        print(f"  pair        {r} trimmed {h - keep} row(s) off the bottom "
                              f"so both frames are {w}x{keep}")

        # One width for the pair, stepped down only if the budget cannot
        # be met at the quality floor.
        chosen_w = None
        for step in WIDTH_STEPS:
            attempt = {}
            target_w = max(1, int(round(width * step)))
            okall = True
            for role in ("before", "after"):
                cap = min(opts.budget, srcsize[role])
                if frames[role] is None:
                    attempt[role] = ("copy", None, None)
                    continue
                w, h, px = frames[role]
                if target_w < w:
                    w2, h2, px2 = downscale(px, w, h, target_w)
                else:
                    w2, h2, px2 = w, h, px
                cpng = os.path.join(tmp, f"{slug}-{role}-{target_w}.png")
                write_rgb_png(cpng, w2, h2, px2)
                best = None
                for q in range(88, QUALITY_FLOOR - 1, -1):
                    cand = os.path.join(tmp, f"{slug}-{role}-{target_w}-{q}.jpg")
                    sips("-s", "format", "jpeg", "-s", "formatOptions", str(q),
                         cpng, "--out", cand)
                    stripped = cand + ".s.jpg"
                    strip_app_segments(cand, stripped)
                    sz = os.path.getsize(stripped)
                    if sz <= cap:
                        best = (stripped, q, sz, w2, h2)
                        break
                if best is None:
                    okall = False
                    break
                attempt[role] = best
            if okall:
                chosen_w = target_w
                break

        if chosen_w is None:
            failures.append(f"{slug}: cannot meet {opts.budget // 1024}KB at quality "
                            f"{QUALITY_FLOOR} at any width")
            print(f"  FAILED to fit the budget at quality {QUALITY_FLOOR}", file=sys.stderr)
            continue
        if chosen_w != width:
            print(f"  pair        width stepped {width} -> {chosen_w} to hold quality "
                  f"{QUALITY_FLOOR} inside the budget")

        final_dims = {}
        for role in ("before", "after"):
            name = f"{slug}-{role}.jpg"
            dest = os.path.join(OUT_DIR, name)
            if attempt[role][0] == "copy":
                dropped = strip_app_segments(paths[role], dest)
                sz = os.path.getsize(dest)
                fw, fh = native[role]
                print(f"  {role:6s}    {name}  {fw}x{fh}  {sz:,} bytes ({sz / 1024:.0f} KB)"
                      f"  source was {srcsize[role]:,}, dropped "
                      + (", ".join(f"{t}({n}b)" for t, n, _g in dropped) or "nothing"))
            else:
                stripped, q, sz, fw, fh = attempt[role]
                shutil.copyfile(stripped, dest)
                print(f"  {role:6s}    {name}  {fw}x{fh}  {sz:,} bytes ({sz / 1024:.0f} KB) "
                      f"at quality {q}   cap was "
                      f"{min(opts.budget, srcsize[role]) // 1024}KB")
            left = app_segments(dest)
            clean = not left
            print(f"  {role:6s}    metadata  "
                  + (f"{len(left)} segment(s) left: {left}" if left
                     else "no APP1-APP15, no comment, nothing identifying")
                  + f"   {'ok' if clean else 'FAIL'}")
            if not clean:
                failures.append(f"{name}: {len(left)} metadata segment(s) survived")
            total += os.path.getsize(dest)
            final_dims[role] = (fw, fh)

        match = final_dims["before"] == final_dims["after"]
        print(f"  pair        {final_dims['before'][0]}x{final_dims['before'][1]} vs "
              f"{final_dims['after'][0]}x{final_dims['after'][1]}   "
              f"{'ok, identical so the crossfade registers' if match else 'FAIL, mismatched'}")
        if not match:
            failures.append(f"{slug}: pair dimensions differ")
        manifest.append((slug, vehicle, final_dims["before"]))

    print(f"\ntotal shipped   {total:,} bytes ({total / 1024:.0f} KB) across "
          f"{len(PAIRS) * 2} frames, every one lazy-loaded below the fold")
    print(f"per-frame cap   {opts.budget // 1024}KB, or the source's own size, "
          f"whichever is smaller")
    print("\naspect ratios for the markup:")
    for slug, vehicle, (w, h) in manifest:
        from math import gcd
        g = gcd(w, h)
        print(f"  {slug}  {w}x{h}  ->  {w // g}/{h // g}   {vehicle}")
    if failures:
        print(f"\n{len(failures)} failure(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("\nall frames redacted, stripped, sized and paired")
    return 0


if __name__ == "__main__":
    sys.exit(main())
