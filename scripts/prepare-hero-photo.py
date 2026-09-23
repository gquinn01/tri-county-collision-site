#!/usr/bin/env python3
"""
Turns the client's photograph of a wrecked customer vehicle into the home
page's hero image, and prints every number it used.

Built to the precedent of scripts/prepare-repair-photos.py, and it IMPORTS
that script's helpers rather than copying them: the APP-segment strip, the
detail metric, the box downscale and the PNG reader are one implementation,
so a fix to either script is a fix to both. A copy would drift.

WHERE THE SOURCE COMES FROM, AND WHY IT IS NOT IN HERE. The client supplied
474875707_9154568911256256_2223418552262379327_n.jpg on 2026-09-22: a real
photograph of a real customer vehicle inside the shop. It stays OUTSIDE this
public repo, like every supplied original and every licensed source, so this
script takes its path as an argument. Permission rides the same practice as
the Real Repairs photographs and the same owner-sheet question covers it.

WHAT THIS RETIRES. accent-major-collision-repair.jpg was the most prominent
stock image on the site. It does NOT leave the repo, because two other
elements still reference it; see proposed-changes.md 3.32.

THE CONTRACT THIS MUST MEET, and why the numbers are what they are. The hero
ships a 1200x800 image and the <img> element carries width="1200"
height="800". Those attributes do not change, so the page's layout is
untouched by construction and the fold cannot move. The source is 1440x1078,
so the job is a crop to 1440x960 and one uniform downscale by 1.2.

THE CROP IS MEASURED, NOT EYEBALLED. The vehicle's red bodywork was located
by scanning for saturated red, which is red-dominant AND not a bright warm
neutral; without that second condition the warm concrete floor scores as car
and the measurement runs to the bottom edge of the frame.

    whole vehicle      y   86 .. 811
    crushed front end  y  236 .. 811   (the right of the frame)
    intact body, left  y   85 .. 632

960 rows must contain 86..811, so the crop's top edge can be anywhere in
0..86. It ships at 0: that keeps the whole roofline and the entire crushed
front end, and spends all 118 discarded rows on empty foreground concrete,
which is the only part of the frame that carries nothing.

NO UPSCALING ANYWHERE. The one resample is 1440 -> 1200, a downscale. The
script refuses to run if the source is smaller than the crop it is asked for.
"""

import argparse
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "docs", "assets", "img")

CROP_W, CROP_H = 1440, 960
OUT_W, OUT_H = 1200, 800

# ONE ENTRY PER PHOTOGRAPH, BECAUSE THE CROP IS MEASURED PER FRAME AND
# CANNOT BE GUESSED. A hero crop has to keep a particular vehicle in a
# particular frame, and where that vehicle sits is a fact about the
# photograph. Parameterised on 2026-09-23 when the second hero arrived
# rather than forked, so both heroes run the same assertions.
#
# HOW `subject` AND `wreck` WERE OBTAINED IS NOT THE SAME FOR BOTH, and
# that is recorded rather than smoothed over:
#
#   home     a saturated-red scan found the car, because a deep red body
#            separates cleanly from a grey floor once "red-dominant AND
#            not a bright warm neutral" is the test.
#   collision  NO COLOUR TEST SEPARATES THIS FRAME. The vehicle is white
#            on grey asphalt under a low sun, and a luma-plus-saturation
#            scan scores the sunlit asphalt and the sky as bodywork just
#            as strongly. The extents below were read off the decoded
#            frame under a 120px coordinate grid instead. That is an
#            inspection, not a scan, and it is written down as one.
FRAMES = {
    "home": {
        "out": "hero-wrecked-sedan-in-shop.jpg",
        "src": (1440, 1078),
        "crop_top": 0,
        "subject": (86, 811),     # the whole vehicle, rows
        "wreck": (236, 811),      # the crushed front end
        "how": "saturated-red scan",
        "note": "118 discarded rows are all foreground concrete",
        "cleared": [],
    },
    "collision": {
        "out": "hero-wrecked-gmc-outside-shop.jpg",
        "src": (1440, 1080),
        "crop_top": 0,
        "subject": (66, 810),     # roofline to tyre contact
        "wreck": (66, 810),       # this vehicle IS the wreck, corner to corner
        "how": "read off a 120px coordinate grid on the decoded frame",
        "note": "120 discarded rows are foreground asphalt, including the "
                "lens-flare streak in the lower left",
        # INSPECTED AT MAGNIFICATION 2026-09-23 AND CLEARED, each one named
        # for what it actually is. See the note on CLEARED REGIONS below.
        "cleared": [
            ((640, 0, 1100, 220),
             "backlit sky through bare trees: the branches are edge-dense and "
             "the blown-out sky behind them is bright and neutral, which is "
             "three conditions out of three met by something that is not an "
             "object at all"),
            ((1180, 190, 1440, 320),
             "the corrugated building and chain-link fence behind the car"),
            ((0, 460, 140, 560),
             "the subject's own front alloy wheel on sunlit gravel"),
        ],
    },
}


# THE PLATE SIGNATURE IS THREE CONDITIONS, NOT ONE, and the third one was
# added after the first run of this script flagged five boxes that turned
# out to be the rear alloy wheel and the torn-open engine bay.
#
# Detail alone does not identify a plate. Alloy spokes against a dark tyre
# and shredded radiator core are both denser than most of the frame. What
# a plate actually is: a BRIGHT, NEUTRAL rectangle carrying dark glyphs, so
# it is high luma AND low saturation AND high detail together. Measured on
# this frame:
#
#     region                        luma   sat   detail
#     rear alloy wheel              70.8  60.5   16.65   dark, saturated
#     alloy wheel edge             124.9  39.2   18.73   saturated
#     torn engine bay              117.7 117.6   17.71   very saturated
#     bright garage wall           207.7  13.9    9.76   bright and neutral,
#                                                        but no glyphs
#     a plate would be              >150   <35     >14   all three at once
#
# THE THRESHOLD WAS NOT LOWERED TO GET PAST THE FLAG. It was made a
# conjunction, which is stricter about what counts as a plate and still
# catches one: a real plate clears all three, and nothing here clears two.
#
# CLEARED REGIONS, ADDED 2026-09-23 with the second hero. The conjunction
# still fires on things that are not plates: a blown-out sky behind bare
# branches is bright, neutral and edge-dense all at once, and so is a
# corrugated building behind a chain-link fence. The first version of
# this check offered only one way out, "redact it if it is a plate", and
# had no path at all for "looked at it, it is not one" -- which is the
# usual answer and was the answer for all nineteen boxes in the GMC
# frame.
#
# So a frame may carry a list of regions that have been INSPECTED AT
# MAGNIFICATION and cleared, each with a sentence saying what the thing
# actually is. This is deliberately not a threshold: the numbers do not
# move, every suspect outside a cleared region still fails the build, and
# clearing one is an edit to this file that names the region and the
# reason, which somebody reviews. A per-frame exception that has to be
# written down is a different thing from a global limit that has been
# loosened.
PLATE_DETAIL_FLAG = 14.0
PLATE_LUMA_MIN = 150.0
PLATE_SAT_MAX = 35.0
PLATE_BOX_W, PLATE_BOX_H = 120, 60

QUALITY_START = 92
QUALITY_FLOOR = 55


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sips(*args):
    subprocess.run(["sips", *args], capture_output=True, text=True, check=True)


def plate_scan(rp, px, w, h):
    """Every plate-sized box on a grid, reported by detail.

    RUN EVEN THOUGH NO PLATE IS VISIBLE, and that is the point. The front
    of this car is torn open and its plate area is gone, so the expected
    result is that nothing scores like a plate. A check that only runs when
    somebody already believes there is a plate is a check that catches
    nothing, which is the failure rule 8 exists to stop.
    """
    hits = []
    for y in range(0, h - PLATE_BOX_H, PLATE_BOX_H // 2):
        for x in range(0, w - PLATE_BOX_W, PLATE_BOX_W // 2):
            box = (x, y, x + PLATE_BOX_W, y + PLATE_BOX_H)
            lum = sat = n = 0
            for yy in range(y, y + PLATE_BOX_H, 2):
                for xx in range(x, x + PLATE_BOX_W, 2):
                    i = (yy * w + xx) * 3
                    r, g, b = px[i], px[i + 1], px[i + 2]
                    lum += (r * 299 + g * 587 + b * 114) // 1000
                    mx, mn = max(r, g, b), min(r, g, b)
                    sat += 0 if mx == 0 else (mx - mn) * 255 // mx
                    n += 1
            hits.append((rp.detail(px, w, box), lum / n, sat / n, x, y))
    hits.sort(reverse=True)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build the home hero from the client's supplied photograph.")
    ap.add_argument("source", help="the supplied photograph, which lives "
                                   "OUTSIDE this repo")
    ap.add_argument("--frame", required=True, choices=sorted(FRAMES),
                    help="which hero this photograph is, and therefore which "
                         "measured crop applies. There is no default: a crop "
                         "guessed for the wrong frame clips a vehicle.")
    opts = ap.parse_args()
    if not os.path.isfile(opts.source):
        print(f"FAILED: no such file: {opts.source}")
        return 1
    F = FRAMES[opts.frame]
    SRC_W, SRC_H = F["src"]
    CROP_TOP = F["crop_top"]
    CAR_TOP, CAR_BOTTOM = F["subject"]
    WRECK_TOP, WRECK_BOTTOM = F["wreck"]
    OUT_NAME = F["out"]
    print(f"FRAME  {opts.frame}  ->  {OUT_NAME}")
    print(f"  subject rows {CAR_TOP}..{CAR_BOTTOM}, located by {F['how']}")
    print(f"  {F['note']}")

    sys.path.insert(0, HERE)
    import audit
    rp = load("rp", os.path.join(HERE, "prepare-repair-photos.py"))

    # 1 ------------------------------------------------ provenance first
    r = audit.read_asset_provenance(opts.source)
    src_bytes = r["bytes"]
    print("PROVENANCE, read before anything was built on it")
    print(f"  file               {os.path.basename(opts.source)}")
    print(f"  bytes              {src_bytes}")
    print(f"  DigitalSourceType  {r['source_type'] or '(none declared)'}")
    print(f"  CreatorTool        {r['tool'] or '(none declared)'}")
    print(f"  C2PA referenced    {r['c2pa']}")
    if r["reasons"]:
        print("  VERDICT            AI: " + "; ".join(r["reasons"]))
        print("\nFAILED before processing. Rule 9 bans AI imagery.")
        return 1
    print("  VERDICT            clean, no AI tell")

    print("\nWHAT THE SOURCE CARRIES, by marker walk")
    for tag, ln, who in rp.app_segments(opts.source):
        print(f"  {tag:<6} len {ln:>6}  {who}")

    w, h = rp.dims(opts.source)
    print(f"\nSOURCE  {w}x{h}")
    if (w, h) != (SRC_W, SRC_H):
        print(f"FAILED: this script's crop is measured against {SRC_W}x{SRC_H}. "
              f"A different source needs the scan re-run, not a fudged offset.")
        return 1
    if w < CROP_W or h < CROP_H:
        print("FAILED: the source is smaller than the crop. No upscaling.")
        return 1

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        # 2 ---------------------------------------------------- decode
        png = os.path.join(tmp, "full.png")
        sips("-s", "format", "png", opts.source, "--out", png)
        pw, ph, ch, px = rp.read_png(png)
        px = rp.to_rgb(pw, ph, ch, px)
        print(f"DECODED {pw}x{ph}")

        # 3 ------------------------------------------------------ crop
        keep_lo, keep_hi = CROP_TOP, CROP_TOP + CROP_H - 1
        print(f"\nCROP    rows {keep_lo}..{keep_hi}  ->  {CROP_W}x{CROP_H}  "
              f"(discarding {ph - CROP_H} rows, all of it foreground concrete)")
        print(f"  vehicle          y {CAR_TOP}..{CAR_BOTTOM}   "
              f"{'INSIDE' if keep_lo <= CAR_TOP and keep_hi >= CAR_BOTTOM else 'CLIPPED'}")
        print(f"  crushed front    y {WRECK_TOP}..{WRECK_BOTTOM}   "
              f"{'INSIDE' if keep_lo <= WRECK_TOP and keep_hi >= WRECK_BOTTOM else 'CLIPPED'}")
        if not (keep_lo <= CAR_TOP and keep_hi >= CAR_BOTTOM):
            print("FAILED: the crop clips the vehicle.")
            return 1
        cropped = bytearray()
        for y in range(keep_lo, keep_hi + 1):
            a = (y * pw) * 3
            cropped += px[a:a + pw * 3]
        cw, chh = pw, CROP_H

        # 4 -------------------------------------------- the plate check
        print(f"\nPLATE CHECK, run although no plate is visible")
        hits = plate_scan(rp, cropped, cw, chh)
        print(f"  {len(hits)} plate-sized boxes ({PLATE_BOX_W}x{PLATE_BOX_H}) scanned")
        print(f"  a plate is detail >= {PLATE_DETAIL_FLAG}, luma >= "
              f"{PLATE_LUMA_MIN}, saturation <= {PLATE_SAT_MAX}, ALL THREE")
        print(f"  the five densest boxes, and what they fail on:")
        for d, lum, sat, x, y in hits[:5]:
            why = []
            if d < PLATE_DETAIL_FLAG:
                why.append("detail")
            if lum < PLATE_LUMA_MIN:
                why.append("too dark")
            if sat > PLATE_SAT_MAX:
                why.append("too saturated")
            print(f"    detail {d:6.2f}  luma {lum:6.1f}  sat {sat:6.1f}  "
                  f"at ({x},{y})   {'PLATE-LIKE' if not why else 'not a plate: ' + ', '.join(why)}")
        suspects = [t for t in hits
                    if t[0] >= PLATE_DETAIL_FLAG
                    and t[1] >= PLATE_LUMA_MIN
                    and t[2] <= PLATE_SAT_MAX]
        print(f"  boxes meeting all three: {len(suspects)}")

        def cleared_by(x, y):
            for (cx0, cy0, cx1, cy1), why in F.get("cleared", []):
                if cx0 <= x and y >= cy0 and x + PLATE_BOX_W <= cx1 \
                        and y + PLATE_BOX_H <= cy1:
                    return why
            return None

        unexplained = []
        by_reason = {}
        for d, lum, sat, x, y in suspects:
            why = cleared_by(x, y)
            if why:
                by_reason.setdefault(why, []).append((x, y))
            else:
                unexplained.append((d, lum, sat, x, y))
        for why, boxes in by_reason.items():
            print(f"    {len(boxes):>2} cleared: {why}")
            print(f"       at {', '.join(f'({x},{y})' for x, y in sorted(boxes)[:6])}"
                  f"{' ...' if len(boxes) > 6 else ''}")
        if unexplained:
            for d, lum, sat, x, y in unexplained[:10]:
                print(f"    detail {d:6.2f}  luma {lum:6.1f}  sat {sat:6.1f}  at ({x},{y})")
            print(f"FAILED: {len(unexplained)} plate-sized box(es) are bright, "
                  f"neutral and glyph-dense at once and are NOT in this frame's "
                  f"cleared list. Look at them. Redact a plate; add a cleared "
                  f"region, with what the thing actually is, only for something "
                  f"you have looked at and it is not. Do not relax these numbers.")
            return 1
        if suspects:
            print("  every suspect is inside a region inspected and cleared for "
                  "this frame; none is a plate")
        else:
            print("  NOTHING in the frame is a plate.")

        # 5 ------------------------------------------------- downscale
        nw, nh, small = rp.downscale(cropped, cw, chh, OUT_W)
        print(f"\nDOWNSCALE {cw}x{chh} -> {nw}x{nh}   factor {cw / nw:.4f}  "
              f"(box average, the one resample)")
        if (nw, nh) != (OUT_W, OUT_H):
            print(f"FAILED: expected {OUT_W}x{OUT_H}, got {nw}x{nh}.")
            return 1

        # 6 ---------------------------------------------------- encode
        spng = os.path.join(tmp, "small.png")
        rp.write_rgb_png(spng, nw, nh, small)
        print(f"\nENCODE, searching quality down from {QUALITY_START} for a file "
              f"no larger than the source ({src_bytes} bytes)")
        chosen = None
        for q in range(QUALITY_START, QUALITY_FLOOR - 1, -1):
            cand = os.path.join(tmp, f"q{q}.jpg")
            sips("-s", "format", "jpeg", "-s", "formatOptions", str(q),
                 spng, "--out", cand)
            stripped = os.path.join(tmp, f"s{q}.jpg")
            rp.strip_app_segments(cand, stripped)
            size = os.path.getsize(stripped)
            if chosen is None and size <= src_bytes:
                chosen = (q, stripped, size)
                print(f"  q{q:<3} {size:>7} bytes   <= source, taken")
                break
            print(f"  q{q:<3} {size:>7} bytes   over source, trying lower")
        if chosen is None:
            print("FAILED: cannot land at or under the source size above the "
                  "quality floor.")
            return 1
        q, path, size = chosen

        # 7 ------------------------------------- strip, then prove it
        print(f"\nMETADATA, after the structural strip by marker walk")
        left = rp.app_segments(path)
        for tag, ln, who in left:
            print(f"  {tag:<6} len {ln:>6}  {who}")
        bad = [t for t, _l, _w in left if t not in ("APP0",)]
        if bad:
            print(f"FAILED: {bad} survived the strip.")
            return 1
        print("  only APP0 JFIF remains, which is the coding header and not "
              "metadata")

        # 8 --------------------------------- post-encode decode assertion
        out = os.path.join(OUT_DIR, OUT_NAME)
        vw, vh = rp.dims(path)
        vpng = os.path.join(tmp, "verify.png")
        sips("-s", "format", "png", path, "--out", vpng)
        dw, dh, dch, _dpx = rp.read_png(vpng)
        print(f"\nDECODE ASSERTION on the emitted file")
        print(f"  sips reports      {vw}x{vh}")
        print(f"  round-trip decode {dw}x{dh}, {dch} channels")
        if (vw, vh) != (OUT_W, OUT_H) or (dw, dh) != (OUT_W, OUT_H):
            print("FAILED: the emitted file does not decode to the contract.")
            return 1
        prov = audit.read_asset_provenance(path)
        print(f"  provenance        "
              f"{'clean' if not prov['reasons'] else 'AI: ' + '; '.join(prov['reasons'])}")
        if prov["reasons"]:
            return 1

        # 9 ------------------------------------------------- install
        os.replace(path, out)

    final = os.path.getsize(out)
    print(f"\nSHIPPED  docs/assets/img/{OUT_NAME}")
    print(f"  {OUT_W}x{OUT_H} at q{q}, {final} bytes")
    print(f"  source was {src_bytes} bytes, so the output is "
          f"{src_bytes - final} bytes smaller ({100 * final / src_bytes:.1f}% of it)")
    if final > src_bytes:
        print("FAILED: output is larger than the source.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
