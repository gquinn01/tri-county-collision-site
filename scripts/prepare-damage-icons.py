#!/usr/bin/env python3
"""
Turns the licensed "Car Accident" icon set into the eight marks the We Fix
It All band ships, and prints every number it used.

Built to the precedent of scripts/prepare-repair-photos.py,
scripts/prepare-car-render.py and scripts/prepare-brand-logos.py: the
irreversible decisions live in a script that can be re-run and audited,
not in somebody's image editor and memory.

WHERE THE SOURCE COMES FROM, AND WHY IT IS NOT IN HERE. The set is
AdobeStock_1964340052, "Car Accident", 36 editable line icons, licensed by
Greg Quinn on 2026-09-22. It is an Adobe Illustrator file and it stays
OUTSIDE this public repo like every licensed source, so this script takes
the .ai path as an argument. Nothing about the source is committed except
its id, its provenance reading, and the geometry of the eight marks that
ship.

WHAT IT DOES, in order:

1. READS THE PROVENANCE FIRST, through the same reader the audit uses, and
   REFUSES TO PROCESS a file that carries an AI tell. Every asset that
   enters this repo gets its metadata read before it lands. The strategy
   chat pre-checked this file; that is not a substitute for the standing
   step, so the step runs here and prints what it found.

2. PARSES THE .ai AS PDF. An Illustrator file saved with PDF compatibility
   carries the artwork twice: once as a PDF page and once as Illustrator's
   own private data. The PDF page is the readable one. Object 8 is the
   page content stream; it is Flate-compressed and zlib is in the standard
   library, so there is no dependency here.

3. WALKS THE CONTENT STREAM, tracking the CTM through q/Q/cm, and collects
   every painted path. THERE ARE NO STROKES IN THIS FILE: 253 fills, zero
   S operators, no line-width settings anywhere. The marks are filled
   outlines, so `fill: none; stroke: ...` renders them as nothing. This is
   the single most important fact about the set and it is why the band's
   CSS changed.

4. SPLITS THE PAGE ON ITS OWN GRID. The artwork is one full-height cover
   illustration on the left plus a 6x6 grid of marks. The split is by gaps
   in the occupancy histogram, not by hard-coded boxes, so a re-run on a
   re-exported file still lands on the same 36.

5. EMITS THE CHOSEN MARKS AT ONE SCALE, in their natural proportions.

   THE SCALE IS DERIVED, NOT CHOSEN. The set carries ONE stroke weight,
   measured at 9.61 to 10.08 and taken as 9.8 set units. The site's chip
   glyphs are 17px at stroke-width 2.1 on a 24 viewBox, which is 1.4875
   device px. The set matches that at 54.64px per 360 set units; the band
   ships 56px per 360, which is 0.155556 px per set unit and puts the
   set's own stroke at 1.524 device px, 2.5% off the chips.

   A SQUARE BOX WAS TRIED AND REJECTED. Forcing every mark into one square
   makes the wide two-car compositions shrink to fit, which drops their
   stroke to 0.58 and 0.68 of everyone else's. Natural proportions at one
   scale give all eight an identical 1.524px line, which is the whole
   point of a set.

6. BUILDS THE THREE MATCHED REDRAWS the set has no honest mark for, in the
   set's own hand: same 9.8 stroke, same round caps and joins, and for two
   of the three the set's OWN CAR, lifted whole from icon 29. Recorded per
   icon in proposed-changes.md 3.28.

7. PATCHES docs/index.html IN PLACE, replacing only the <svg> in each of
   the eight items and leaving every heading and every line of copy
   exactly as it was.

THE LIMIT OF THE PROVENANCE STEP, STATED PLAINLY. The marks ship as inline
SVG in the HTML. Inline SVG carries no metadata, so there is no derived
file for scripts/audit.py's reader to scan afterwards and a clean audit
says nothing about these eight. The provenance that matters was read on
the source, before a line was built on it, and it is recorded here, in the
section's HTML comment and in proposed-changes.md 3.28. That is the same
arrangement the car render has and it is a floor, not a guarantee.
"""

import argparse
import json
import os
import re
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "docs", "index.html")

ASSET_ID = "AdobeStock_1964340052"
ASSET_TITLE = "Car Accident"
SET_COUNT = 36

# The set's own stroke, recovered from three marks by measuring dark-run
# widths in a large render and dividing by each mark's normalising scale:
# icon 19 gave 10.08, icon 07 gave 9.61, icon 25 gave 9.61.
SET_STROKE = 9.8

# Derived in note 5 above. 56 rendered px per 360 set units.
SCALE = 56.0 / 360.0

# Half a stroke of padding, so a round cap at the edge is not clipped.
PAD = SET_STROKE / 2

CHIP_STROKE_PX = 2.1 * 17 / 24          # the site's established icon weight

# The icon box the eight sit in, bottom-aligned so the cars share a ground
# line and the headings below them stay level. It has to clear the tallest
# mark, and this script fails if it stops doing so.
ICO_BOX = 46


# --------------------------------------------------------------- the file

def pdf_stream(raw: bytes, num: int) -> bytes:
    """One Flate-compressed PDF object, inflated."""
    m = re.search(rb"(?<![0-9])" + str(num).encode() + rb"\s+0\s+obj", raw)
    if not m:
        raise ValueError(f"object {num} is not in this file")
    s = raw.find(b"stream", m.end())
    if s < 0:
        raise ValueError(f"object {num} carries no stream")
    start = s + 6
    if raw[start:start + 2] == b"\r\n":
        start += 2
    elif raw[start:start + 1] in (b"\n", b"\r"):
        start += 1
    end = raw.find(b"endstream", start)
    return zlib.decompress(raw[start:end])


def page_content(raw: bytes) -> bytes:
    """The page's content stream, found through the page tree."""
    if not raw.startswith(b"%PDF"):
        raise ValueError("this .ai was not saved with PDF compatibility, so "
                         "there is no PDF page to read. Re-save it from "
                         "Illustrator with 'Create PDF Compatible File' on.")
    m = re.search(rb"/Contents\s+(\d+)\s+0\s+R", raw)
    if not m:
        raise ValueError("no /Contents reference on the page")
    return pdf_stream(raw, int(m.group(1)))


# ----------------------------------------------------------- the operators

TOKEN = re.compile(rb"/[^\s/\[\]<>()]+|\[|\]|<<|>>|[^\s\[\]/<>]+")


def _mul(a, b):
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


def _apply(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def painted_paths(data: bytes) -> tuple:
    """Every painted path in the content stream, in page space.

    Returns (paths, counts). Each path is {'subs': [...]}, each subpath
    {'start': (x, y), 'segs': [('L', p) | ('C', a, b, c)]}.
    """
    toks = TOKEN.findall(data)
    st, ctm, stack = [], [1, 0, 0, 1, 0, 0], []
    cur, sub, cp = [], None, None
    out, counts = [], {}
    for t in toks:
        try:
            st.append(float(t))
            continue
        except ValueError:
            pass
        op = t.decode("latin-1", "replace")
        counts[op] = counts.get(op, 0) + 1
        if op == "q":
            stack.append(list(ctm))
        elif op == "Q":
            if stack:
                ctm = stack.pop()
        elif op == "cm" and len(st) >= 6:
            ctm = _mul(st[-6:], ctm)
        elif op == "m" and len(st) >= 2:
            cp = _apply(ctm, st[-2], st[-1])
            sub = {"start": cp, "segs": []}
            cur.append(sub)
        elif op == "l" and len(st) >= 2:
            cp = _apply(ctm, st[-2], st[-1])
            if sub is None:
                sub = {"start": cp, "segs": []}
                cur.append(sub)
            else:
                sub["segs"].append(("L", cp))
        elif op == "c" and len(st) >= 6:
            a = _apply(ctm, st[-6], st[-5])
            b = _apply(ctm, st[-4], st[-3])
            cp = _apply(ctm, st[-2], st[-1])
            if sub is not None:
                sub["segs"].append(("C", a, b, cp))
        elif op == "v" and len(st) >= 4:
            b = _apply(ctm, st[-4], st[-3])
            p = _apply(ctm, st[-2], st[-1])
            if sub is not None:
                sub["segs"].append(("C", cp, b, p))
            cp = p
        elif op == "y" and len(st) >= 4:
            a = _apply(ctm, st[-4], st[-3])
            p = _apply(ctm, st[-2], st[-1])
            if sub is not None:
                sub["segs"].append(("C", a, p, p))
            cp = p
        elif op == "re" and len(st) >= 4:
            x, y, w, h = st[-4:]
            pts = [_apply(ctm, x, y), _apply(ctm, x + w, y),
                   _apply(ctm, x + w, y + h), _apply(ctm, x, y + h)]
            sub = {"start": pts[0],
                   "segs": [("L", pts[1]), ("L", pts[2]), ("L", pts[3])]}
            cur.append(sub)
            cp = pts[0]
        elif op in ("f", "F", "f*", "B", "B*", "b", "b*", "S", "s", "n"):
            if cur and op != "n":
                out.append({"subs": cur})
            cur, sub = [], None
        st = []
    return out, counts


def bbox_of(path) -> tuple:
    xs, ys = [], []
    for s in path["subs"]:
        xs.append(s["start"][0])
        ys.append(s["start"][1])
        for seg in s["segs"]:
            for pt in seg[1:]:
                xs.append(pt[0])
                ys.append(pt[1])
    return min(xs), min(ys), max(xs), max(ys)


# ---------------------------------------------------------------- the grid

def gaps(spans, axis_max, minsize):
    occ = [False] * (int(axis_max) + 2)
    for lo, hi in spans:
        for k in range(int(lo), int(hi) + 1):
            occ[k] = True
    out, s = [], None
    for k, o in enumerate(occ):
        if not o and s is None:
            s = k
        if o and s is not None:
            if k - s >= minsize:
                out.append((s, k))
            s = None
    return out


def split_grid(paths, cover_x=1100.0):
    """The 36 marks, numbered left to right and top to bottom.

    The cover illustration down the left of the page is excluded by its
    x centre. The row gap between the bottom two rows is only 26 units,
    so the y threshold has to be below that; 18 is used and it is the
    reason a re-run does not collapse rows 1 and 2 into one.
    """
    marks = [p for p in paths if (p["bbox"][0] + p["bbox"][2]) / 2 > cover_x]
    cover = len(paths) - len(marks)
    xg = gaps([(p["bbox"][0], p["bbox"][2]) for p in marks], 4790, 18)
    yg = gaps([(p["bbox"][1], p["bbox"][3]) for p in marks], 2270, 18)
    xcuts = [0] + [(a + b) // 2 for a, b in xg] + [10 ** 5]
    ycuts = [0] + [(a + b) // 2 for a, b in yg] + [10 ** 5]
    cells = {}
    for p in marks:
        cx = (p["bbox"][0] + p["bbox"][2]) / 2
        cy = (p["bbox"][1] + p["bbox"][3]) / 2
        ci = max(i for i in range(len(xcuts) - 1) if cx >= xcuts[i])
        ri = max(i for i in range(len(ycuts) - 1) if cy >= ycuts[i])
        cells.setdefault((ri, ci), []).append(p)
    rows = sorted({r for r, _ in cells}, reverse=True)
    cols = sorted({c for _, c in cells})
    icons, n = [], 0
    for r in rows:
        for c in cols:
            if (r, c) not in cells:
                continue
            n += 1
            ps = cells[(r, c)]
            bs = [p["bbox"] for p in ps]
            icons.append({
                "n": n,
                "paths": ps,
                "bbox": (min(b[0] for b in bs), min(b[1] for b in bs),
                         max(b[2] for b in bs), max(b[3] for b in bs)),
            })
    return icons, cover, len(xcuts) - 1, len(ycuts) - 1


# ------------------------------------------------------------- the emitter

def fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def path_d(icon, dy=0.0, pad=None) -> tuple:
    """One mark's fill path, in a viewBox of its own natural proportions."""
    pad = PAD if pad is None else pad
    x0, y0, x1, y1 = icon["bbox"]
    w, h = (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad
    d = []
    for p in icon["paths"]:
        for s in p["subs"]:
            def T(pt):
                return (pt[0] - x0 + pad, y1 - pt[1] + pad + dy)
            X, Y = T(s["start"])
            d.append(f"M{fmt(X)} {fmt(Y)}")
            for seg in s["segs"]:
                if seg[0] == "L":
                    X, Y = T(seg[1])
                    d.append(f"L{fmt(X)} {fmt(Y)}")
                else:
                    a, b, c = T(seg[1]), T(seg[2]), T(seg[3])
                    d.append(f"C{fmt(a[0])} {fmt(a[1])} {fmt(b[0])} {fmt(b[1])} "
                             f"{fmt(c[0])} {fmt(c[1])}")
            d.append("Z")
    return "".join(d), w, h


# ------------------------------------------------------------ the redraws
# Authored in the SET'S units: stroke 9.8, round caps and joins, the set's
# corner radii. Two of the three are built on the set's OWN car, lifted
# whole from icon 29, so one hand appears across all eight by construction
# rather than by anybody's eye.
#
# Every placement is measured. The donor car's panel between the wheels was
# probed row by row: solid beltline at y 69..75, free from y 78..132 apart
# from the door-gap line, solid sill at y 135..141. Everything added to the
# donor sits inside 78..132.

GLASS_W, GLASS_H = 300.0, 268.0
GLASS_STROKE = [
    "M52 236V128L74 70A16 16 0 0 1 90 58H236A18 18 0 0 1 254 76V236"
    "A14 14 0 0 1 240 250H66A14 14 0 0 1 52 236Z",
    "M92 80H232A12 12 0 0 1 244 92V148H70V106Z",
    "M52 150H30A12 12 0 0 0 18 162V174A12 12 0 0 0 30 186H52",
    "M186 190H238",
    "M152 112L96 92", "M152 112L104 140", "M152 112L146 146",
    "M152 112L214 88", "M152 112L228 126", "M152 112L178 140",
    "M118 100L108 84", "M186 98L204 90", "M150 130L138 142",
]

PAINT_STROKE = ["M108 114L138 102L168 114L198 102L228 112"]
PAINT_FLAKES = ["M118 90L128 82L134 92L122 96Z",
                "M200 88L210 80L216 90L204 94Z"]

HAIL_DROP = 78.0
HAIL_DISCS = [(58, 62, 11), (118, 38, 9), (178, 66, 11),
              (238, 42, 10), (298, 70, 11), (338, 44, 9)]
HAIL_STROKE = ["M44 30L52 42", "M104 8L112 20", "M164 34L172 46",
               "M224 10L232 22", "M284 38L292 50", "M324 12L332 24"]

DONOR_ICON, DONOR_PATH = 29, 0
# The donor is built with ITS OWN padding, and it is not the set's PAD. The
# free band above was probed in a space padded by 12, so the redraw marks
# are written in that space and the donor has to keep it or they slide off
# the panel they were measured onto.
DONOR_PAD = 12.0


# ------------------------------------------------------------- the mapping
# heading -> (source, note). A source of ("set", n) is the licensed mark n.
# A source of ("redraw", key) is a matched redraw, recorded as one.
MAPPING = [
    ("Minor collisions",            ("set", 8),
     "two cars nose to nose, light impact ticks and no burst"),
    ("Major collisions",            ("set", 6),
     "head-on, both fronts crushed, large impact burst"),
    ("Cracked windshields",         ("set", 1),
     "front view, spider crack across the windshield"),
    ("Broken side and rear glass",  ("redraw", "glass"),
     "door with wing mirror, window shattered"),
    ("Door dings and dents",        ("set", 20),
     "three-quarter car, localised side impact with shake lines"),
    ("Bumper damage",               ("set", 26),
     "two front ends meeting close up, impact burst between them"),
    ("Scratched and chipped paint", ("redraw", "paint"),
     "donor car, zigzag scratch and two lifted flakes"),
    ("Hail damage",                 ("redraw", "hail"),
     "donor car, stones falling on slanted travel lines"),
]

# Alternatives that validated but were not shipped, kept for the record and
# printed on every run so the choice stays visible.
ALTERNATIVES = {
    "Minor collisions": (7, "same pair with a burst between them; 08 ships "
                            "because it is the lighter drawing and it leaves "
                            "the burst to Major, which sits beside it"),
    "Major collisions": (21, "abstracted head-on, fewer lines, cleaner at any "
                             "size; 06 ships because it shows actual crush, "
                             "which is what the line under it claims"),
    "Door dings and dents": (25, "car from above with the burst on the near "
                                 "side; 20 ships on the client's pick from the "
                                 "numbered sheet, 2026-09-22"),
    "Bumper damage":    (4,  "front view with the burst below the front "
                             "bumper; 26 ships on the client's pick from the "
                             "numbered sheet, 2026-09-22. Icon 31, the side "
                             "view with the burst under the body, reads as "
                             "undercarriage and was never in front"),
}


def svg_for(key, icons_by_n):
    """(inner markup, viewBox w, viewBox h) for one shipped mark."""
    kind, which = key
    if kind == "set":
        d, w, h = path_d(icons_by_n[which])
        return f'<path class="f" d="{d}"/>', w, h
    donor = icons_by_n[DONOR_ICON]
    # The donor is ONE path out of icon 29, so it gets that path's own
    # bbox. Icon 29's bbox spans its speech bubbles too, and using it put
    # 134 units of empty air above the car.
    body = donor["paths"][DONOR_PATH]
    car = {"n": DONOR_ICON, "bbox": bbox_of(body), "paths": [body]}
    if which == "glass":
        inner = "".join(f'<path class="s" d="{d}"/>' for d in GLASS_STROKE)
        return inner, GLASS_W, GLASS_H
    if which == "paint":
        d, w, h = path_d(car, pad=DONOR_PAD)
        inner = f'<path class="f" d="{d}"/>'
        inner += "".join(f'<path class="f" d="{p}"/>' for p in PAINT_FLAKES)
        inner += "".join(f'<path class="s" d="{p}"/>' for p in PAINT_STROKE)
        return inner, w, h
    if which == "hail":
        d, w, h = path_d(car, dy=HAIL_DROP, pad=DONOR_PAD)
        inner = f'<path class="f" d="{d}"/>'
        inner += "".join(f'<circle class="f" cx="{cx}" cy="{cy}" r="{r}"/>'
                         for cx, cy, r in HAIL_DISCS)
        inner += "".join(f'<path class="s" d="{p}"/>' for p in HAIL_STROKE)
        return inner, w, h + HAIL_DROP
    raise ValueError(which)


# ----------------------------------------------------------------- the page

def patch_page(page_html: str, built: dict) -> tuple:
    """Replace only the <svg> in each of the eight items.

    ITEM BY ITEM, and that is the whole point of this function's shape. A
    single regex reaching from `<li class="fix">` to a named <h3> spans
    every item in between, because `.*?` stops at the first match of what
    FOLLOWS it and not at the item boundary. Written that way once, it ate
    seven of the eight items and left the page with one. So the page is cut
    into items first, each item is patched inside its own bounds, and the
    result is counted before a byte is written.
    """
    item_re = re.compile(r'<li class="fix">.*?</li>', re.S)
    svg_re = re.compile(r'(?:<span class="ico">)?<svg\b.*?</svg>(?:</span>)?', re.S)
    head_re = re.compile(r"<h3>([^<]*)</h3>")

    seen = []

    def one(m):
        block = m.group(0)
        h = head_re.search(block)
        if not h:
            return block
        heading = h.group(1)
        if heading not in built:
            return block
        inner, w, hh, pw, ph = built[heading]
        svg = (f'<svg viewBox="0 0 {fmt(w)} {fmt(hh)}" width="{fmt(pw)}" '
               f'height="{fmt(ph)}" aria-hidden="true" focusable="false">'
               f"{inner}</svg>")
        block2, n = svg_re.subn(lambda _: '<span class="ico">' + svg + "</span>",
                                block, count=1)
        if n != 1:
            raise SystemExit(f"FAILED: '{heading}' carries {n} svg elements, "
                             f"wanted exactly 1")
        seen.append(heading)
        return block2

    out = item_re.sub(one, page_html)

    # Guards. This function rewrites a live page, so it proves what it did
    # before main() is allowed to write the file.
    wanted = [h for h, _s, _n in MAPPING]
    missing = [h for h in wanted if h not in seen]
    if missing:
        raise SystemExit("FAILED: never reached " + ", ".join(missing))
    before = len(item_re.findall(page_html))
    after = len(item_re.findall(out))
    if before != after:
        raise SystemExit(f"FAILED: {before} items went in and {after} came "
                         f"out. Nothing written.")
    for h in wanted:
        if out.count(f"<h3>{h}</h3>") != 1:
            raise SystemExit(f"FAILED: '{h}' appears "
                             f"{out.count(f'<h3>{h}</h3>')} times after the "
                             f"patch. Nothing written.")
    return out, len(seen)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build the eight We Fix It All damage marks from the "
                    "licensed set, and patch docs/index.html.")
    ap.add_argument("source", help="path to the licensed .ai, which lives "
                                   "OUTSIDE this repo")
    ap.add_argument("--check", action="store_true",
                    help="Report without writing anything; exit 1 if stale.")
    opts = ap.parse_args()

    if not os.path.isfile(opts.source):
        print(f"FAILED: no such file: {opts.source}")
        return 1

    # 1 -------------------------------------------------- provenance first
    sys.path.insert(0, HERE)
    import audit
    r = audit.read_asset_provenance(opts.source)
    print("PROVENANCE, read before anything was built on it")
    print(f"  file               {os.path.basename(opts.source)}")
    print(f"  asset              {ASSET_ID}  \"{ASSET_TITLE}\"")
    print(f"  bytes              {r['bytes']}")
    print(f"  DigitalSourceType  {r['source_type'] or '(none declared)'}")
    print(f"  CreatorTool        {r['tool'] or '(none declared)'}")
    print(f"  C2PA referenced    {r['c2pa']}")
    if r["reasons"]:
        print("  VERDICT            AI: " + "; ".join(r["reasons"]))
        print("\nFAILED before processing. Rule 9 bans AI imagery and the "
              "label is not the thing to remove; the provenance is the fact.")
        return 1
    print("  VERDICT            clean, no AI tell")
    print("  LIMIT              the eight ship as INLINE SVG, which carries "
          "no metadata.\n                     No derived file exists for the "
          "audit's reader to scan, so a\n                     clean audit "
          "says nothing about them. This reading is the floor.")

    # 2, 3 ------------------------------------------------------- the file
    raw = open(opts.source, "rb").read()
    content = page_content(raw)
    paths, counts = painted_paths(content)
    for p in paths:
        p["bbox"] = bbox_of(p)
    strokes = sum(counts.get(op, 0) for op in ("S", "s", "B", "B*", "b", "b*"))
    print(f"\nTHE FILE   content stream {len(content)} bytes inflated")
    print(f"  painted paths      {len(paths)}")
    print(f"  fill operators     {counts.get('f', 0)}")
    print(f"  STROKE operators   {strokes}   <- the marks are FILLED "
          f"OUTLINES, not strokes")
    print(f"  line-width sets    {counts.get('w', 0)}")

    # 4 -------------------------------------------------------- the grid
    icons, cover, ncols, nrows = split_grid(paths)
    print(f"\nTHE GRID   {ncols} columns x {nrows} rows")
    print(f"  cover-art paths excluded   {cover}")
    print(f"  marks found                {len(icons)}")
    if len(icons) != SET_COUNT:
        print(f"\nFAILED: the licence says {SET_COUNT} marks and the split "
              f"found {len(icons)}.")
        return 1
    by_n = {i["n"]: i for i in icons}

    # 5 ------------------------------------------------------- the scale
    print(f"\nTHE SCALE, derived and not chosen")
    print(f"  set's own stroke           {SET_STROKE} set units")
    print(f"  site's chip glyphs         17px at stroke-width 2.1 on a 24 "
          f"viewBox = {CHIP_STROKE_PX:.4f} device px")
    print(f"  match at                   {CHIP_STROKE_PX * 360 / SET_STROKE:.2f}px "
          f"per 360 set units")
    print(f"  shipped                    56px per 360 = {SCALE:.6f} px per "
          f"set unit")
    print(f"  every mark's stroke        {SET_STROKE * SCALE:.4f} device px  "
          f"({100 * (SET_STROKE * SCALE / CHIP_STROKE_PX - 1):+.1f}% vs the chips)")
    print(f"  the band's old glyphs      30px at stroke-width 2 on a 24 "
          f"viewBox = {2 * 30 / 24:.4f} device px, the site's outlier")

    # 6, 7 --------------------------------------------------- the marks
    print(f"\nTHE EIGHT")
    print(f"  {'heading':<28} {'source':<12} {'viewBox':>15} {'rendered px':>15}")
    built, maxh = {}, 0.0
    for heading, src, note in MAPPING:
        inner, w, h = svg_for(src, by_n)
        pw, ph = w * SCALE, h * SCALE
        built[heading] = (inner, w, h, pw, ph)
        maxh = max(maxh, ph)
        label = f"icon {src[1]:02d}" if src[0] == "set" else "REDRAW"
        print(f"  {heading:<28} {label:<12} {w:>7.1f}x{h:<7.1f} "
              f"{pw:>7.1f}x{ph:<7.1f}")
        print(f"  {'':<28} {note}")
    print(f"\n  tallest mark {maxh:.1f}px -> .fix .ico is {ICO_BOX}px")
    if maxh > ICO_BOX:
        print(f"\nFAILED: the tallest mark is {maxh:.1f}px and .fix .ico is "
              f"{ICO_BOX}px, so it would be clipped. Raise ICO_BOX here and "
              f"in site.css together.")
        return 1
    print(f"  widest mark  {max(b[3] for b in built.values()):.1f}px, and the "
          f"4-across column at 1440 is 269px")

    print(f"\nALTERNATIVES that validated and were not shipped")
    for heading, (n, why) in ALTERNATIVES.items():
        print(f"  {heading:<28} icon {n:02d}  {why}")

    print(f"\nTHE REDRAWS, matched to the set rather than mixed with it")
    print(f"  glass  own drawing, {len(GLASS_STROKE)} stroked paths at "
          f"{SET_STROKE} units. A DOOR and not the donor car: the donor's rear")
    print(f"         side window is 65x32 set units = "
          f"{65 * SCALE:.1f}x{32 * SCALE:.1f} device px and no crack survives "
          f"that. It also has")
    print(f"         to read apart from icon 01, which is a cracked windshield "
          f"in the same row.")
    print(f"  paint  the set's OWN car, icon {DONOR_ICON} path {DONOR_PATH}, "
          f"plus 1 scratch and 2 filled flakes.")
    print(f"         The scratch is a zigzag because at one stroke weight a "
          f"straight line reads as a")
    print(f"         body crease, which the set's cars already carry. All of "
          f"it inside the measured")
    print(f"         free band y 78..132.")
    print(f"  hail   the same car dropped {HAIL_DROP:.0f} units, "
          f"{len(HAIL_DISCS)} filled stones and {len(HAIL_STROKE)} slanted "
          f"travel lines.")
    print(f"         Stones are filled because an 18-unit ring at {SET_STROKE} "
          f"of stroke has no hole left.")

    page = open(PAGE, encoding="utf-8").read()
    new, changed = patch_page(page, built)
    if new == page:
        print(f"\nPAGE   {changed} items already current, nothing written")
        return 0
    if opts.check:
        print(f"\nPAGE   {changed} items are STALE. Re-run without --check.")
        return 1
    open(PAGE, "w", encoding="utf-8").write(new)
    print(f"\nPAGE   {changed} items rewritten in docs/index.html")
    print(f"       headings and copy untouched: the patch is keyed on the "
          f"<h3> and replaces only the <svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
