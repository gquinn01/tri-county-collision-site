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

# The crop every 1440-wide source gets. A frame that needs anything else
# says so with its own "crop" box, below.
LEGACY_W, LEGACY_H = 1440, 960
OUT_W, OUT_H = 1200, 800
# THE HERO CONTRACT. A frame that is not a page hero, the commercial
# page's link-preview crop (3.92c), names its own "out_size"; nothing that
# ships as a hero ever does.
HERO_SIZE = (OUT_W, OUT_H)

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

    # THE SERVICE-PAGE HEROES ADDED 2026-09-24 WERE INTERIM STOCK. Greg
    # licensed them from Adobe Stock with the generative-AI filter
    # excluded; see proposed-changes.md 3.47 to 3.49 and 4.9. The fleet
    # one is replaced by the shop's own photograph (3.92b). The glass and
    # dent ones stay, and since Greg's ruling of 2026-10-06 they are
    # shoot-list items, no longer cutover blockers. The
    # licensed originals stay OUTSIDE this public repo like every other
    # source, and the asset id is recorded here because the shipped file
    # carries no metadata to say where it came from.
    #
    # THESE SOURCES ARE FOUR TO EIGHT THOUSAND PIXELS WIDE, NOT 1440, so
    # each carries an explicit "crop" box (left, top, width, height) in
    # source pixels. Every box is the source trimmed to exact 3:2 and no
    # further: the subject already sits right of centre, which is where
    # the scrim leaves photograph showing, so there is nothing to gain by
    # cropping in and a resolution cost to paying for it. The one resample
    # is still the box downscale to 1200x800.
    #
    # THE SUBJECT EXTENTS WERE MEASURED ON A 1000px WORKING COPY AND SCALED
    # BACK TO SOURCE PIXELS. The working copy exists only to be measured;
    # nothing built here reads it.
    "glass": {
        "asset": "AdobeStock_64691325",
        "out": "hero-windshield-replacement-in-shop.jpg",
        "src": (4255, 2832),
        "crop": (4, 0, 4248, 2832),
        "subject": (877, 2310),      # the suction-cup lifters, rows
        "subject_x": (962, 3544),    # and columns
        "wreck": (877, 2310),
        "wreck_label": "lifters on glass",
        "how": "saturated-red scan: the lifters are the only saturated red "
               "in a teal and grey frame",
        "note": "7 discarded columns, split 4 left and 3 right",
        "cleared": [],
    },
    "dent": {
        "asset": "AdobeStock_1571353580",
        "out": "hero-dent-lifter-on-red-door.jpg",
        "src": (8192, 5464),
        "crop": (1, 2, 8190, 5460),
        # A RED CAR DEFEATS A RED SCAN, so the subject is the tool, found
        # by a gold scan, with the blue glue tab found by a blue one. The
        # glove and rods run below and right of both, to the frame edge.
        "subject": (975, 2785),      # the lifter body and its tab, rows
        "subject_x": (4620, 7463),   # glue tab's left edge to the lifter's right
        "wreck": (1901, 2531),       # the glue tab on the dent
        "wreck_label": "glue tab on dent",
        "how": "gold scan for the lifter, blue scan for the glue tab",
        "note": "2 discarded columns and 4 discarded rows, all red paint",
        "cleared": [],
    },
    # THE COMMERCIAL HERO IS THE SHOP'S OWN PHOTOGRAPH SINCE 2026-10-06,
    # 3.92b. It replaced AdobeStock_430555209, the interim stock work van
    # that shipped 2026-09-24 (3.49), which is retired as replaced: no
    # frame here builds it any more, and its file, hero-wrecked-work-van.jpg,
    # was deleted from docs/ in 3.92c. Git history keeps it. This one is a photograph the shop
    # published of itself on its Facebook page, so it carries no asset id
    # and no metadata, and the provenance reader finding nothing is the
    # expected result, recorded, not a pass by default.
    #
    # THE CROP IS THE FULL WIDTH AND THE TOP 960 ROWS, MEASURED. A
    # saturated-red scan on 20px cells (red over 110 and over 1.8x both
    # green and blue) puts the truck's red bodywork at rows 20..879, so
    # every red pixel of it stays and the 120 discarded rows are the lower
    # bumper chrome, the bottom of the tyre and asphalt.
    #
    # THE TAGUE TRUCK COULD NOT BE CROPPED OUT, AND IS REDACTED INSTEAD.
    # It sits at columns 110..312, and a 3:2 crop that starts right of it
    # is at most 1128 wide, which would mean upscaling to 1200. No
    # upscaling, so Greg's standing rule on another business's livery is
    # met the other way his ruling allows: unrecognizable. See "redact".
    "commercial": {
        "out": "hero-red-rollback.jpg",
        "src": (1440, 1080),
        "crop": (0, 0, 1440, 960),
        "subject": (20, 879),        # the red bodywork, rows
        "subject_x": (105, 1439),    # grille edge to the bed at the frame edge
        "wreck": (20, 879),
        "wreck_label": "red bodywork",
        "how": "saturated-red scan on 20px cells",
        "note": "120 discarded rows are bumper chrome, tyre and asphalt; "
                "no red bodywork is lost",
        "provenance": "the shop's own photograph, via its Facebook page, "
                      "Greg's ruling 3.92",
        # SOURCE PIXELS, each with what it is. Every box is destroyed by
        # the Real Repairs method, pixelate then blur, and held to the
        # same ceiling on the detail that survives.
        "redact": [
            ((110, 252, 312, 452),
             "the Tague Lumber box truck in the background: another "
             "business's livery, name and logo, Greg's standing rule"),
            ((0, 322, 118, 395),
             "two more businesses' lettering beside it: a U-Haul panel and "
             "a moving-and-equipment truck's side"),
            ((882, 280, 924, 312),
             "the windshield registration sticker, which reads 7 and 24 "
             "at full resolution"),
        ],
        # INSPECTED AT MAGNIFICATION 2026-10-06 AND CLEARED.
        "cleared": [
            ((1080, 0, 1320, 240),
             "backlit sky through pine branches, and the top of the truck's "
             "own chrome mirror reflecting it"),
            ((460, 680, 620, 760),
             "the truck's own headlight: chrome reflector cells and the "
             "clear lens, bright and edge-dense, no glyph"),
        ],
    },
    # THE COMMERCIAL PAGE'S LINK-PREVIEW IMAGE, 3.92c, Greg's ruling of
    # 2026-10-06. THE SAME PHOTOGRAPH AS THE HERO, CROPPED A SECOND WAY,
    # because the two have different jobs. The hero must be 1200x800 and
    # covers the left of the frame with the scrim, so the redaction block
    # where the Tague truck was sits under it. og:image serves the WHOLE
    # frame to every link preview, so there the block showed. This crop
    # leaves the truck out instead of covering it.
    #
    # MEASURED: the Tague truck's box ends at column 304, read at 4x on a
    # 10px grid, so the crop starts at 309 and takes everything to the
    # right edge. 1131 is the widest 3:2 width from there (1131x754, a
    # multiple of 3), and it ships at its own size: no resample, so no
    # upscaling. The cost is the grille's left half, which is left of 309.
    # Rows 24..777 keep the fairing's marker lights and the whole
    # headlight. The registration sticker is inside the crop and stays
    # redacted; the other two boxes fall outside it and are skipped.
    #
    # Cleared regions here are in CROP pixels, as for every frame whose
    # plate check runs on the crop: source minus (309, 24).
    "commercial-og": {
        "out": "og-red-rollback.jpg",
        "out_size": (1131, 754),
        "src": (1440, 1080),
        "crop": (309, 24, 1131, 754),
        "subject": (30, 770),        # marker lights to the headlight's lower edge
        "subject_x": (380, 1439),    # the grille's right edge to the bed
        "wreck": (30, 770),
        "wreck_label": "cab and headlight",
        "how": "read off a 60px coordinate grid on the decoded frame",
        "note": "309 columns discarded on the left (the Tague truck, two "
                "businesses' lettering, the grille's left half), 24 rows "
                "at the top and 302 at the foot",
        "provenance": "the shop's own photograph, via its Facebook page, "
                      "Greg's ruling 3.92",
        "redact": [
            # The truck's measured extent, ending at column 304. The
            # hero's box for it runs to 312, a margin this crop would cut.
            ((110, 252, 305, 452), "the Tague Lumber box truck"),
            ((0, 322, 118, 395), "the U-Haul panel and the moving truck's side"),
            ((882, 280, 924, 312),
             "the windshield registration sticker, which reads 7 and 24 "
             "at full resolution"),
        ],
        # The hero frame's two cleared objects, the same pixels, inspected
        # at magnification 2026-10-06, in crop pixels here.
        "cleared": [
            ((771, 0, 1031, 216),
             "backlit sky through pine branches, and the truck's own chrome "
             "mirror reflecting it (source 1080..1340, 24..240)"),
            ((151, 591, 471, 751),
             "the truck's own headlight: chrome reflector cells and the "
             "clear lens, no glyph (source 460..780, 615..775)"),
        ],
    },

    # THE ONE HERO THAT IS NOT A PHOTOGRAPH, ADDED 2026-10-01, and it is
    # here by a scoped amendment to the hero law, not by an exception
    # quietly taken (proposed-changes.md 3.86, CLAUDE.md rule 1). Every
    # hero is text over a photograph, except where the page's subject is
    # invisible to a camera. /adas-calibration/ teaches sensor fields and
    # camera aim, which no photograph can show, and this licensed,
    # human-made illustration shows exactly that. It is NOT interim stock
    # and not a cutover blocker: it is the page's ruled hero.
    #
    # THE CROP IS ANCHORED RIGHT, AND MEASURED. The sensor fields that
    # read red, where another car is close, are the only saturated red in
    # a blue and green frame, so a red scan found them: 136px cells, rows
    # 680..2719, columns 2448..4895. That is right of centre, where the
    # scrim leaves the image showing. The 1613 columns discarded on the
    # left are the merge curve and two green-field cars, which would sit
    # under the scrim.
    #
    # THE TOP 200 ROWS GO BECAUSE THE SCRIM MEASUREMENT SAID SO. Cropped
    # from row 0, the illustration's own bright HUD frame border sat under
    # the breadcrumb at 360x640, and one pixel of the "Home" glyph run
    # measured 6.73 against the 7:1 target. The standard did not move and
    # the type got no shadow; the frame of the image moved, which is this
    # asset's own choice to make. One row is discarded at the foot to make
    # exact 3:2.
    "adas": {
        "asset": "AdobeStock_345981008",
        "out": "hero-adas-sensor-fields-illustration.jpg",
        "src": (5444, 2755),
        "crop": (1613, 200, 3831, 2554),
        "subject": (680, 2719),      # the red sensor fields, rows
        "subject_x": (2448, 4895),   # and columns
        "wreck": (680, 2719),
        "wreck_label": "red sensor fields",
        "how": "saturated-red scan on 136px cells: the red fields are the "
               "only saturated red in a blue and green frame",
        "note": "1613 columns discarded on the left (the merge curve, two "
                "green-field cars), 200 rows at the top (the HUD frame border, "
                "which defeated the scrim under the 360 breadcrumb) and 1 at "
                "the foot",
        "cleared": [],
        # THE DECLARATION THE ILLUSTRATION CHECK BELOW REQUIRES. A second
        # illustration needs its own ruling, and its own entry here saying
        # so; the script refuses one that arrives without it.
        "illustration": "Greg's ruling of 2026-10-01, proposed-changes.md "
                        "3.86: the page's subject, sensor fields and camera "
                        "aim, is invisible to a camera",
    },
}

# AN ILLUSTRATION NEEDS ITS OWN RULING, AND THIS IS THE MECHANISM, 3.86.
# Every hero is a photograph unless a frame above carries an "illustration"
# declaration naming its ruling. A source whose CreatorTool names a vector
# illustration program is refused unless its frame declares one, so the
# second illustration cannot arrive the way a photograph does. The limit is
# the provenance reader's: a raster illustration with no tool declared
# passes this, and the judgement at purchase time is still the control.
VECTOR_TOOLS = ("illustrator", "inkscape", "coreldraw", "affinity designer",
                "sketch", "figma", "vectorworks")


def illustration_refusal(tool: str, frame: dict):
    """None if this source may be built for this frame, else the reason."""
    if any(v in (tool or "").lower() for v in VECTOR_TOOLS) and not frame.get("illustration"):
        return (f"the source was made in {tool}, an illustration program, and "
                f"this frame declares no illustration ruling. Every hero is a "
                f"photograph unless a ruling says otherwise (3.86).")
    return None


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


def plate_scan(rp, px, w, h, box_w=PLATE_BOX_W, box_h=PLATE_BOX_H):
    """Every plate-sized box on a grid, reported by detail.

    RUN EVEN THOUGH NO PLATE IS VISIBLE, and that is the point. The front
    of this car is torn open and its plate area is gone, so the expected
    result is that nothing scores like a plate. A check that only runs when
    somebody already believes there is a plate is a check that catches
    nothing, which is the failure rule 8 exists to stop.
    """
    hits = []
    for y in range(0, h - box_h, box_h // 2):
        for x in range(0, w - box_w, box_w // 2):
            box = (x, y, x + box_w, y + box_h)
            lum = sat = n = 0
            for yy in range(y, y + box_h, 2):
                for xx in range(x, x + box_w, 2):
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
        description="Build a hero image from a supplied or licensed photograph.")
    ap.add_argument("source", help="the supplied photograph, which lives "
                                   "OUTSIDE this repo")
    ap.add_argument("--frame", required=True, choices=sorted(FRAMES),
                    help="which hero this photograph is, and therefore which "
                         "measured crop applies. There is no default: a crop "
                         "guessed for the wrong frame clips a vehicle.")
    ap.add_argument("--out-dir", default=OUT_DIR,
                    help="where the finished file lands. Defaults to "
                         "docs/assets/img; point it at a temp directory to "
                         "re-prove a shipped asset byte for byte without "
                         "touching it.")
    opts = ap.parse_args()
    if not os.path.isfile(opts.source):
        print(f"FAILED: no such file: {opts.source}")
        return 1
    F = FRAMES[opts.frame]
    OUT_W, OUT_H = F.get("out_size", HERO_SIZE)
    SRC_W, SRC_H = F["src"]
    # A frame without an explicit box is one of the two 1440-wide sources,
    # and gets exactly the crop it always had.
    CROP_LEFT, CROP_TOP, CROP_W, CROP_H = F.get(
        "crop", (0, F.get("crop_top", 0), LEGACY_W, LEGACY_H))
    CAR_TOP, CAR_BOTTOM = F["subject"]
    CAR_LEFT, CAR_RIGHT = F.get("subject_x", (CROP_LEFT, CROP_LEFT + CROP_W - 1))
    WRECK_LABEL = F.get("wreck_label", "crushed front")
    WRECK_TOP, WRECK_BOTTOM = F["wreck"]
    OUT_NAME = F["out"]
    print(f"FRAME  {opts.frame}  ->  {OUT_NAME}")
    print(f"  subject rows {CAR_TOP}..{CAR_BOTTOM}, located by {F['how']}")
    if F.get("asset"):
        print(f"  licensed asset     {F['asset']}  "
              f"{'(the ruled illustration, not interim stock)' if F.get('illustration') else '(interim stock, a shoot-list item)'}")
    print(f"  {F['note']}")
    if F.get("provenance"):
        print(f"  provenance         {F['provenance']}")

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
    refusal = illustration_refusal(r["tool"], F)
    if refusal:
        print(f"\nFAILED before processing: {refusal}")
        return 1
    if F.get("illustration"):
        print(f"  ILLUSTRATION       declared: {F['illustration']}")

    print("\nWHAT THE SOURCE CARRIES, by marker walk")
    for tag, ln, who in rp.app_segments(opts.source):
        print(f"  {tag:<6} len {ln:>6}  {who}")

    w, h = rp.dims(opts.source)
    print(f"\nSOURCE  {w}x{h}")
    if (w, h) != (SRC_W, SRC_H):
        print(f"FAILED: this script's crop is measured against {SRC_W}x{SRC_H}. "
              f"A different source needs the scan re-run, not a fudged offset.")
        return 1
    if CROP_W * OUT_H != CROP_H * OUT_W:
        print(f"FAILED: the crop box {CROP_W}x{CROP_H} is not exactly "
              f"{OUT_W}:{OUT_H}, so the one downscale would distort it.")
        return 1
    if CROP_LEFT + CROP_W > w or CROP_TOP + CROP_H > h or w < CROP_W or h < CROP_H:
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
        col_lo, col_hi = CROP_LEFT, CROP_LEFT + CROP_W - 1
        print(f"\nCROP    rows {keep_lo}..{keep_hi}, columns {col_lo}..{col_hi}  "
              f"->  {CROP_W}x{CROP_H}  (discarding {ph - CROP_H} rows and "
              f"{pw - CROP_W} columns)")
        inside_y = keep_lo <= CAR_TOP and keep_hi >= CAR_BOTTOM
        inside_x = col_lo <= CAR_LEFT and col_hi >= CAR_RIGHT
        print(f"  subject          y {CAR_TOP}..{CAR_BOTTOM}, x {CAR_LEFT}..{CAR_RIGHT}   "
              f"{'INSIDE' if inside_y and inside_x else 'CLIPPED'}")
        print(f"  {WRECK_LABEL:<16} y {WRECK_TOP}..{WRECK_BOTTOM}   "
              f"{'INSIDE' if keep_lo <= WRECK_TOP and keep_hi >= WRECK_BOTTOM else 'CLIPPED'}")
        if not (inside_y and inside_x):
            print("FAILED: the crop clips the subject.")
            return 1
        cropped = bytearray()
        for y in range(keep_lo, keep_hi + 1):
            a = (y * pw + col_lo) * 3
            cropped += px[a:a + CROP_W * 3]
        del px
        cw, chh = CROP_W, CROP_H

        # 3b ------------------------------------------------- redact
        # THE REAL REPAIRS METHOD, IMPORTED, NOT COPIED: pixelate then
        # blur, and fail if more than MAX_DETAIL_REMAINING of the local
        # detail survives. Boxes are in source pixels and land on the
        # crop before the plate check, so nothing redacted is scanned
        # as if it were still there.
        if F.get("redact"):
            print(f"\nREDACT, {len(F['redact'])} region(s), pixelate then blur")
        for (rx0, ry0, rx1, ry1), why in F.get("redact", []):
            # A BOX THE CROP LEAVES OUT IS REPORTED AND SKIPPED; A BOX THE
            # CROP CUTS THROUGH FAILS, because half a logo is still a logo
            # and the redaction would be measured on the wrong pixels.
            if rx1 <= col_lo or rx0 > col_hi or ry1 <= keep_lo or ry0 > keep_hi:
                print(f"  ({rx0},{ry0})..({rx1},{ry1}) source px is outside "
                      f"the crop, nothing to redact: {why}")
                continue
            if rx0 < col_lo or rx1 > col_hi + 1 or ry0 < keep_lo or ry1 > keep_hi + 1:
                print(f"FAILED: the crop cuts through a redaction box "
                      f"({rx0},{ry0})..({rx1},{ry1}): {why}")
                return 1
            fb = ((rx0 - col_lo) / cw, (ry0 - keep_lo) / chh,
                  (rx1 - col_lo) / cw, (ry1 - keep_lo) / chh)
            box, d0, d1 = rp.redact(cropped, cw, chh, fb)
            ratio = (d1 / d0) if d0 else 0.0
            print(f"  {box[2] - box[0]}x{box[3] - box[1]}px at ({box[0]},{box[1]})  "
                  f"detail {d0:.1f} -> {d1:.1f}, {ratio * 100:.1f}% left   {why}")
            if ratio > rp.MAX_DETAIL_REMAINING:
                print(f"FAILED: the redaction left {ratio * 100:.0f}% of the "
                      f"local detail, over {rp.MAX_DETAIL_REMAINING * 100:.0f}%.")
                return 1

        # WHERE THE PLATE CHECK RUNS. The plate box is sized for a
        # 1440-wide frame, where a plate is roughly 120x60. A frame cropped
        # wider than that is scanned AFTER the downscale, at 1200 wide,
        # with the box scaled by the same 1200/1440, so a plate is the same
        # fraction of the box in every frame. Scanning an 8190px crop with
        # a 120px box would be looking for a plate a sixth of plate size.
        # Cleared regions for such a frame are in OUTPUT pixels.
        scan_output = CROP_W > LEGACY_W
        if scan_output:
            nw, nh, small = rp.downscale(cropped, cw, chh, OUT_W)
            print(f"\nDOWNSCALE {cw}x{chh} -> {nw}x{nh}   factor {cw / nw:.4f}  "
                  f"(box average, the one resample, run before the plate "
                  f"check because this crop is wider than {LEGACY_W})")
            del cropped
            scan_px, scan_w, scan_h = small, nw, nh
            box_w = round(PLATE_BOX_W * OUT_W / LEGACY_W)
            box_h = round(PLATE_BOX_H * OUT_W / LEGACY_W)
        else:
            scan_px, scan_w, scan_h = cropped, cw, chh
            box_w, box_h = PLATE_BOX_W, PLATE_BOX_H

        # 4 -------------------------------------------- the plate check
        print(f"\nPLATE CHECK, run although no plate is visible")
        hits = plate_scan(rp, scan_px, scan_w, scan_h, box_w, box_h)
        print(f"  {len(hits)} plate-sized boxes ({box_w}x{box_h}) scanned "
              f"on the {scan_w}x{scan_h} {'output' if scan_output else 'crop'}")
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
                if cx0 <= x and y >= cy0 and x + box_w <= cx1 \
                        and y + box_h <= cy1:
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
        if not scan_output:
            nw, nh, small = rp.downscale(cropped, cw, chh, OUT_W)
            if nw == cw:
                print(f"\nNO RESAMPLE: the crop is already {cw}x{chh}, the "
                      f"frame's output size")
            else:
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
        out = os.path.join(opts.out_dir, OUT_NAME)
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
    print(f"\nSHIPPED  {os.path.relpath(out, ROOT)}")
    print(f"  {OUT_W}x{OUT_H} at q{q}, {final} bytes")
    print(f"  source was {src_bytes} bytes, so the output is "
          f"{src_bytes - final} bytes smaller ({100 * final / src_bytes:.1f}% of it)")
    if final > src_bytes:
        print("FAILED: output is larger than the source.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
