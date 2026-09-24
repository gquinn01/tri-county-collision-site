#!/usr/bin/env python3
"""
Draws /contact-us/'s directions map from OpenStreetMap data, writes it into
the page as inline SVG, and prints every number it used.

WHY THIS EXISTS. Greg's ruling of 2026-09-24 (proposed-changes.md 3.54): the
contact page gains a map beside the shop's details, and nothing on this site
makes a third-party request at runtime, so the map is ours and self-hosted.
It is a DIRECTIONS DIAGRAM: the roads a driver knows, their names, their
route numbers where OSM records one, and our pin. Nothing else. A nearby
business in the data does not ship: this is not a neighbourhood guide.

WHY IT IS DRAWN AND NOT STITCHED FROM TILES. The brief said to stitch
tile.openstreetmap.org tiles. The OSMF Tile Usage Policy, section 4, read on
2026-09-24, prohibits "any pre-emptive fetching of tiles other than those a
user is actively viewing" and "offline use", and a static image built from
tiles at build time is both. Greg agreed, and the licence is kept rather than
bent. The OSM editing API was ruled out the same way: its policy says it is
"provided in order to edit the map data, not for read-only purposes". So the
data comes from ONE Overpass API query, within that service's fair use, and
this script draws it. Greg's scope ruling of 2026-09-24: the 2026-09-17
no-third-drawing ruling does not reach cartography (3.22).

THE LICENCE BASIS. OpenStreetMap data is licensed under the Open Data
Commons Open Database License (ODbL) 1.0, openstreetmap.org/copyright, read
2026-09-24. A map image drawn from it is a PRODUCED WORK under ODbL 4.3: it
may be published under any terms, provided it carries a notice that credits
the contributors and says the data is available under the ODbL. The page
carries exactly that, visibly, in the map's figcaption:
    Map data (c) OpenStreetMap contributors, available under the Open
    Database License.
with links to openstreetmap.org/copyright and the ODbL text. Share-alike
attaches to derivative DATABASES, not produced works, and no database
leaves this script: the Overpass response is cached OUTSIDE the repo.

ACCURACY IS THE WHOLE POINT, and a wrong map is worse than none. The pin is
not the geocoder's point. Nominatim returns an interpolated house number
~190m from the shop, and the live schema's geo (still on every page, 4.7)
is ~220m west of it, the classic offset of a Google Maps URL's viewport
centre copied as if it were the pin. The pin is PIN below, and it is
checked against the OSM building footprints: the script prints which
footprint contains it, and refuses to draw if none does.

THE COORDINATES DO NOT ENTER THE SCHEMA. They exist to draw a picture. geo in
the schema is a separate fact with its own owner question (4.7).

WHY INLINE SVG. The palette lives in one place, docs/assets/site.css. An SVG
file loaded through <img> cannot read that stylesheet, so every colour would
be a hex typed here. Inline, every mark carries a class (.map-road,
.map-label, .map-pin...) that site.css paints, and the labels are set in the
site's own self-hosted Source Sans 3. No extra request, either.

USAGE:
    python3 scripts/prepare-map-image.py --data PATH          # draw from a cached response
    python3 scripts/prepare-map-image.py --fetch PATH         # one query, cache it, draw
    ... --out-dir DIR    write map.svg there and do NOT touch docs/

No external packages, pure Python standard library.
"""

import argparse
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "docs", "contact-us", "index.html")

# THE PIN. Google's own place coordinate for "Tri-County Collision" at the
# footer's search URL, read 2026-09-24, and it must fall inside an OSM
# building footprint for this script to draw at all. See 3.54.
PIN_LAT, PIN_LON = 40.1660232, -75.0512847

# THE QUERY, and the only request this script ever makes. The bbox is the
# frame below plus a margin, so roads that cross the edge are whole; the
# buildings are fetched only to verify the pin and are never drawn.
QUERY_BBOX = (40.1570, -75.0680, 40.1750, -75.0345)   # s, w, n, e
ROAD_CLASSES = ("motorway", "trunk", "primary", "secondary", "tertiary",
                "unclassified", "residential", "motorway_link", "trunk_link",
                "primary_link", "secondary_link", "tertiary_link")
QUERY = ('[out:json][timeout:50];('
         'way["highway"~"^(' + "|".join(ROAD_CLASSES) + ')$"]'
         '({0},{1},{2},{3});'
         'way["building"](around:120,{4},{5}););out geom tags;').format(
             *QUERY_BBOX, PIN_LAT, PIN_LON)
ENDPOINTS = ("https://overpass-api.de/api/interpreter",
             "https://lz4.overpass-api.de/api/interpreter",
             "https://z.overpass-api.de/api/interpreter")
USER_AGENT = "TriCountyCollisionSiteBuild/1.0 (greg@corcoranpr.com)"

# THE FRAME. A viewBox in drawing units, and how many metres one unit is.
# 480x360 so the labels, at 15 units, land near 16px in the 1440 column and
# near 11px on a phone. The metres are chosen so the frame reaches the roads
# a driver steers by, and are printed.
VB_W, VB_H = 480, 360
M_PER_UNIT = 3.4
FRAME_CX_LAT, FRAME_CX_LON = PIN_LAT, PIN_LON   # recentred below if needed

# How each class is drawn: casing width, road width, "major" casing.
STYLE = {
    "motorway": (13, 10, True), "trunk": (13, 10, True),
    "primary": (12, 9, True), "secondary": (11, 8, True), "tertiary": (10, 7, True),
    "unclassified": (8, 5.5, False), "residential": (7, 4.5, False),
}
for _k in ("motorway", "trunk", "primary", "secondary", "tertiary"):
    STYLE[_k + "_link"] = (7, 4.5, True)
DRAW_ORDER = ["residential", "unclassified", "tertiary_link", "secondary_link",
              "primary_link", "trunk_link", "motorway_link", "tertiary",
              "secondary", "primary", "trunk", "motorway"]
# Which roads get their NAME written. Every major road in frame, plus the
# pin's own street, whatever its class: it is the one a driver looks for.
LABEL_CLASSES = ("motorway", "trunk", "primary", "secondary", "tertiary")
PIN_STREET = "Jaymor Road"
# And every named road that passes this close to the pin, whatever its
# class: the streets that meet at the shop's own corner are the last turn
# a driver makes, and Google labels them too. In frame today that is Jaymor
# Road, James Way and Knowles Avenue.
LABEL_NEAR_M = 160
# Where along a road a label or a route number may sit, tried in order until
# one clears everything already placed.
TRY_AT = (0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8, 0.12, 0.88)
# A name may only sit where the road turns less than this under its letters.
# Past it, text on a path folds over itself at the bend, which is what
# happened to "James Way" at its junction on the first draw.
MAX_TURN_DEG = 25
LABEL_SIZE = 16
SHIELD_SIZE = 13.5
PIN_LABEL = "Tri-County Collision"
PIN_LABEL_SIZE = 17
MIN_LABEL_RUN = 150          # units of road a name needs to be written along

MAPS_HREF = ("https://www.google.com/maps/search/?api=1&amp;query=Tri-County%20Collision"
             "%2C%20995%20Jaymor%20Rd%2C%20Southampton%2C%20PA%2018966")


# ----------------------------------------------------------------------
def fetch(cache_path: str) -> dict:
    """One query. Tries the endpoints in order and stops at the first that
    answers; it never retries in a loop, because fair use is the terms."""
    body = urllib.parse.urlencode({"data": QUERY}).encode()
    for ep in ENDPOINTS:
        try:
            req = urllib.request.Request(ep, data=body, headers={"User-Agent": USER_AGENT})
            raw = urllib.request.urlopen(req, timeout=70).read()
            data = json.loads(raw)
            with open(cache_path, "wb") as f:
                f.write(raw)
            print(f"fetched  {ep}  {len(raw)} bytes  -> {cache_path}")
            return data
        except Exception as e:  # noqa: BLE001, every failure is reported and the next tried
            print(f"fetch    {ep}  FAILED  {e}")
    raise SystemExit("FAILED: no Overpass endpoint answered. Nothing was drawn.")


def project(lat: float, lon: float) -> tuple:
    """Local equirectangular metres from the frame centre, then drawing
    units. At this latitude and a frame under 2km, the difference from Web
    Mercator is under a tenth of a unit, which is printed below."""
    k = math.cos(math.radians(FRAME_CX_LAT))
    x = (lon - FRAME_CX_LON) * 111320.0 * k / M_PER_UNIT + VB_W / 2
    y = -(lat - FRAME_CX_LAT) * 110574.0 / M_PER_UNIT + VB_H / 2
    return x, y


def clip_segment(p, q, xmin, ymin, xmax, ymax):
    """Liang-Barsky. The part of p-q inside the box, or None."""
    x0, y0 = p
    dx, dy = q[0] - x0, q[1] - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)):
        if pp == 0:
            if qq < 0:
                return None
            continue
        r = qq / pp
        if pp < 0:
            if r > t1:
                return None
            t0 = max(t0, r)
        else:
            if r < t0:
                return None
            t1 = min(t1, r)
    return (x0 + t0 * dx, y0 + t0 * dy), (x0 + t1 * dx, y0 + t1 * dy)


def clip_polyline(pts, pad=20):
    """Runs of the polyline inside the frame plus a margin, so a road's
    round cap never shows at the edge. Returns a list of point lists."""
    xmin, ymin, xmax, ymax = -pad, -pad, VB_W + pad, VB_H + pad
    runs, cur = [], []
    for a, b in zip(pts, pts[1:]):
        c = clip_segment(a, b, xmin, ymin, xmax, ymax)
        if c is None:
            if cur:
                runs.append(cur)
                cur = []
            continue
        s, e = c
        if not cur:
            cur = [s]
        elif math.dist(cur[-1], s) > 0.01:
            runs.append(cur)
            cur = [s]
        cur.append(e)
        if math.dist(e, b) > 0.01:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) >= 2]


def fmt(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def d_of(pts) -> str:
    return "M" + " L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)


def length(pts) -> float:
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def heading(p, q) -> float:
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def continues(a, b) -> bool:
    """True when run b carries on from the end of run a in roughly the same
    direction. A DUAL CARRIAGEWAY is two OSM ways that meet end to end at
    each junction, running opposite ways; chaining them without this test
    folds the road into a U, and a name written along a U is unreadable.
    Found on the first draws, where PA 232 and County Line Road lost their
    names to it."""
    d = abs((heading(a[-2], a[-1]) - heading(b[0], b[1]) + 180) % 360 - 180)
    return d < 60


def join_runs(runs):
    """Chains runs that share an endpoint AND continue one another, so a
    road split into several OSM ways is labelled once, along its longest
    continuous stretch."""
    runs = [list(r) for r in runs]
    merged = True
    while merged:
        merged = False
        for i in range(len(runs)):
            for j in range(len(runs)):
                if i == j:
                    continue
                a, b = runs[i], runs[j]
                if math.dist(a[-1], b[0]) < 0.5 and continues(a, b):
                    runs[i] = a + b[1:]
                elif math.dist(a[-1], b[-1]) < 0.5 and continues(a, b[::-1]):
                    runs[i] = a + b[::-1][1:]
                else:
                    continue
                del runs[j]
                merged = True
                break
            if merged:
                break
    return runs


def inside(pt, poly) -> bool:
    x, y = pt
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def point_at(pts, dist):
    """The point `dist` units along a polyline."""
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        if dist <= seg and seg:
            t = dist / seg
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        dist -= seg
    return pts[-1]


def span_boxes(pts, centre, w, pad):
    """What a label of width w, centred `centre` units along the road,
    actually covers: a chain of small boxes that follows the letters. One
    axis-aligned box around a diagonal label blocks a triangle of empty
    map twice its size, which is how the first draws lost two names."""
    out = []
    for i in range(9):
        x, y = point_at(pts, max(0.0, centre - w / 2 + w * i / 8))
        out.append((x - pad, y - pad, x + pad, y + pad))
    return out


def turn_deg(pts, centre, w) -> float:
    """How far the road turns, in degrees, across the span a label of width
    w centred `centre` units along it would cover."""
    heads = []
    for i in range(9):
        a = point_at(pts, max(0.0, centre - w / 2 + w * i / 8))
        b = point_at(pts, max(0.0, centre - w / 2 + w * i / 8) + 2.0)
        heads.append(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))
    worst = 0.0
    for h in heads[1:]:
        d = abs((h - heads[0] + 180) % 360 - 180)
        worst = max(worst, d)
    return worst


def clear(boxes, placed) -> bool:
    return all(b[2] < q[0] or b[0] > q[2] or b[3] < q[1] or b[1] > q[3]
               for b in boxes for q in placed)


def ref_text(ref: str) -> str:
    """A route number as it is signed. OSM's ref may list several networks
    separated by ';' ("I 276;PATP"): the first is the route. An Interstate
    is written with a hyphen, I-276, the way the signs and every US map
    write it; state routes keep OSM's form, "PA 232"."""
    r = ref.split(";")[0].strip()
    return re.sub(r"^I (\d+)$", r"I-\1", r)


# THE NAMES ARE WRITTEN THE WAY THE SIGNS AND THE ADDRESS WRITE THEM. OSM
# spells suffixes out ("Jaymor Road"); the shop's NAP is "995 Jaymor Rd",
# and scripts/audit.py fails any page that spells the street a second way,
# which is right, because a page carrying both reads as two addresses. So
# every label takes the USPS Publication 28 standard abbreviation for a
# trailing street suffix and a leading direction, the same convention
# Google's own map uses on the link this map opens. That abbreviates what
# the data says and adds nothing to it. Found by the audit on the first
# patched build, 3.54.
USPS_SUFFIX = {"Road": "Rd", "Avenue": "Ave", "Street": "St", "Drive": "Dr",
               "Lane": "Ln", "Boulevard": "Blvd", "Turnpike": "Tpke",
               "Court": "Ct", "Circle": "Cir", "Place": "Pl", "Parkway": "Pkwy",
               "Highway": "Hwy"}
USPS_DIRECTION = {"North": "N", "South": "S", "East": "E", "West": "W"}


def as_signed(name: str) -> str:
    words = name.split()
    if len(words) > 1 and words[-1] in USPS_SUFFIX:
        words[-1] = USPS_SUFFIX[words[-1]]
    if len(words) > 2 and words[0] in USPS_DIRECTION:
        words[0] = USPS_DIRECTION[words[0]]
    return " ".join(words)


def text_w(s: str, size: float) -> float:
    """Source Sans 3 at 600 averages close to half an em per character;
    the estimate only has to keep labels off each other."""
    return len(s) * size * 0.52


# ----------------------------------------------------------------------
def draw(data: dict):
    els = data.get("elements", [])
    stamp = data.get("osm3s", {}).get("timestamp_osm_base", "unknown")
    print(f"data     OSM base timestamp {stamp}, {len(els)} elements")

    # 1. The pin must sit inside a building, or nothing is drawn.
    pin_bldg = None
    for e in els:
        t = e.get("tags", {})
        if "building" in t and e.get("geometry"):
            poly = [(g["lon"], g["lat"]) for g in e["geometry"]]
            if inside((PIN_LON, PIN_LAT), poly):
                pin_bldg = e
    if not pin_bldg:
        raise SystemExit("FAILED: the pin is inside no OSM building footprint. "
                         "Nothing was drawn; re-verify PIN against Google.")
    bt = pin_bldg.get("tags", {})
    print(f"pin      {PIN_LAT}, {PIN_LON} lies inside building way {pin_bldg['id']} "
          f"(building={bt.get('building')}, name={bt.get('name', '-')!r}, "
          f"addr={bt.get('addr:housenumber', '-')} {bt.get('addr:street', '-')})")

    # 2. Roads, clipped to the frame, by class.
    roads = []
    for e in els:
        t = e.get("tags", {})
        hw = t.get("highway")
        if hw not in STYLE or not e.get("geometry"):
            continue
        pts = [project(g["lat"], g["lon"]) for g in e["geometry"]]
        for run in clip_polyline(pts):
            roads.append((hw, t.get("name", ""), t.get("ref", ""), run))
    by_class = {}
    for hw, *_ in roads:
        by_class[hw] = by_class.get(hw, 0) + 1
    print(f"roads    {len(roads)} runs in frame: " +
          ", ".join(f"{k} {v}" for k, v in sorted(by_class.items())))

    out = [f'<rect class="map-ground" width="{VB_W}" height="{VB_H}"/>']
    for layer in ("case", "road"):
        for cls in DRAW_ORDER:
            runs = [r for r in roads if r[0] == cls]
            if not runs:
                continue
            case_w, road_w, major = STYLE[cls]
            w = case_w if layer == "case" else road_w
            klass = ("map-case map-case--major" if major else "map-case") if layer == "case" else "map-road"
            d = " ".join(d_of(r[3]) for r in runs)
            out.append(f'<path class="{klass}" stroke-width="{fmt(w)}" d="{d}"/>')

    # 3. Names, along the longest continuous stretch of each named road:
    # every major road in frame, and every named road near the pin.
    px, py = project(PIN_LAT, PIN_LON)
    near_u = LABEL_NEAR_M / M_PER_UNIT
    defs, labels, shields, report = [], [], [], []
    names = {}
    for hw, name, ref, run in roads:
        if not name:
            continue
        near = min(math.dist((px, py), q) for q in run) <= near_u
        if hw in LABEL_CLASSES or name == PIN_STREET or near:
            names.setdefault(name, []).append(run)

    def visible(run, m=4):
        return [q for q in run if m <= q[0] <= VB_W - m and m <= q[1] <= VB_H - m]

    # THE ORDER IS THE PRIORITY: the pin's own street, then the through
    # roads a driver steers by, then the streets at the shop's corner,
    # longest first within each, measured JOINED, because a road split
    # into many OSM ways is still one road.
    cls_of = {r[1]: r[0] for r in roads if r[1]}
    order = sorted(names.items(), key=lambda kv: (
        kv[0] != PIN_STREET, cls_of.get(kv[0]) not in LABEL_CLASSES,
        -max(length(j) for j in join_runs(kv[1]))))

    # Every place each name could go: straight enough, inside its stretch.
    pad = LABEL_SIZE * 0.5
    names_c, corner_c = [], []
    for name, runs in order:
        vis = visible(max(join_runs(runs), key=length))
        ln = length(vis) if len(vis) >= 2 else 0
        w = text_w(as_signed(name), LABEL_SIZE)
        if len(vis) >= 2 and vis[-1][0] < vis[0][0]:
            vis = vis[::-1]
        opts = []
        for frac in TRY_AT:
            c = frac * ln
            if ln < w + 24 or c - w / 2 < 6 or c + w / 2 > ln - 6:
                continue
            if turn_deg(vis, c, w) > MAX_TURN_DEG:
                continue
            opts.append((frac, span_boxes(vis, c, w, pad)))
        entry = {"kind": "name", "key": name, "vis": vis, "ln": ln, "opts": opts}
        major = name == PIN_STREET or cls_of.get(name) in LABEL_CLASSES
        (names_c if major else corner_c).append(entry)

    # Every place each route number could go. A driver steers by a route
    # number as much as by a name, so they rank with the through roads and
    # ahead of the corner streets, and they are in the same search: placed
    # after it, the I-276 box once found every place already taken.
    # A ROUTE NUMBER NEVER SITS WHERE ANOTHER MAJOR ROAD CROSSES ITS ROUTE.
    # The first draw that placed both boxes put "PA 232" on the Turnpike
    # crossing, where it read as the Turnpike's number. So a box is refused
    # anywhere a major road carrying a different number passes under it.
    def other_major_points(ref):
        pts = []
        for hw, _n, rref, run in roads:
            if hw in LABEL_CLASSES and rref != ref:
                for a_, b_ in zip(run, run[1:]):
                    steps = max(1, int(math.dist(a_, b_) / 3))
                    pts.extend((a_[0] + (b_[0] - a_[0]) * k / steps,
                                a_[1] + (b_[1] - a_[1]) * k / steps) for k in range(steps + 1))
        return pts

    shield_c = []
    for ref in sorted({r[2] for r in roads if r[2]}):
        shown = ref_text(ref)
        vis = visible(max(join_runs([r[3] for r in roads if r[2] == ref]), key=length), 16)
        ln = length(vis) if len(vis) >= 2 else 0
        w = text_w(shown, SHIELD_SIZE) + 14
        others = other_major_points(ref)
        opts = []
        for frac in TRY_AT:
            if not ln:
                break
            at = point_at(vis, frac * ln)
            box = (at[0] - w / 2 - 3, at[1] - 14, at[0] + w / 2 + 3, at[1] + 14)
            if any(box[0] - 6 <= x <= box[2] + 6 and box[1] - 6 <= y <= box[3] + 6 for x, y in others):
                continue
            opts.append((frac, [box]))
        shield_c.append({"kind": "shield", "key": ref, "shown": shown, "vis": vis,
                         "ln": ln, "w": w, "opts": opts})
    cands = names_c + shield_c + corner_c

    # The pin's name goes right of the pin or left of it, whichever lets
    # more be written.
    lw = text_w(PIN_LABEL, PIN_LABEL_SIZE)
    pin_opts = [("right", [(px - 14, py - 38, px + 20 + lw, py + 4)]),
                ("left", [(px - 20 - lw, py - 38, px + 14, py + 4)])]
    pin_opts = [o for o in pin_opts if o[1][0][0] >= 2 and o[1][0][2] <= VB_W - 2]

    # EXHAUSTIVE, AND SMALL: under ten items with up to nine places each.
    # The best layout writes the most items in priority order: the pin's
    # street, the through roads, the route numbers, the corner streets. A
    # greedy pass cannot see that its first choice blocks a later, more
    # useful one.
    best = {"score": None, "pick": None}

    def search(i, placed, pick, score):
        if best["score"] is not None:
            ceiling = score + [1] * (len(cands) - i)
            if ceiling < best["score"]:
                return
        if i == len(cands):
            if best["score"] is None or score > best["score"]:
                best["score"], best["pick"] = list(score), list(pick)
            return
        for frac, boxes in cands[i]["opts"]:
            if clear(boxes, placed):
                search(i + 1, placed + boxes, pick + [(frac, boxes)], score + [1])
        search(i + 1, placed, pick + [None], score + [0])

    chosen = None
    for side, pbox in pin_opts:
        best["score"], best["pick"] = None, None
        search(0, list(pbox), [], [])
        if chosen is None or best["score"] > chosen[0]:
            chosen = (best["score"], best["pick"], side, pbox)
    _, pick, pin_side, pin_box = chosen
    for i, (c, got) in enumerate(zip(cands, pick)):
        if got is None:
            why = ("no stretch long and straight enough" if not c["opts"]
                   else "every place collides with a higher-priority item")
            report.append(f"  skip   {c['kind']} {c['key']!r}: {why}")
            continue
        frac, boxes = got
        if c["kind"] == "name":
            pid = f"map-r{i}"
            defs.append(f'<path id="{pid}" d="{d_of(c["vis"])}"/>')
            labels.append(f'<text class="map-label" font-size="{LABEL_SIZE}" dy="5">'
                          f'<textPath href="#{pid}" startOffset="{frac * 100:.0f}%" '
                          f'text-anchor="middle">{as_signed(c["key"])}</textPath></text>')
            report.append(f"  label  {c['key']!r} written {as_signed(c['key'])!r}, "
                          f"at {frac:.0%} of a {c['ln']:.0f}-unit stretch")
        else:
            at = point_at(c["vis"], frac * c["ln"])
            w = c["w"]
            shields.append(f'<rect class="map-shield" x="{fmt(at[0] - w / 2)}" y="{fmt(at[1] - 11)}" '
                           f'width="{fmt(w)}" height="22" rx="3"/>'
                           f'<text class="map-shield-text" font-size="{SHIELD_SIZE}" '
                           f'x="{fmt(at[0])}" y="{fmt(at[1] + 4.5)}" text-anchor="middle">{c["shown"]}</text>')
            report.append(f"  shield {c['shown']!r} (OSM ref {c['key']!r}) at {frac:.0%} of its stretch")
    report.append(f"  pin    name set {pin_side} of the pin")
    print("labels")
    print("\n".join(report))

    # 5. The pin: the one oxblood mark, and its name.
    pin = (f'<path class="map-pin" d="M{fmt(px)} {fmt(py)} c-3 -9 -12 -13 -12 -21 '
           f'a12 12 0 1 1 24 0 c0 8 -9 12 -12 21z"/>'
           f'<circle class="map-pin-dot" cx="{fmt(px)}" cy="{fmt(py - 21)}" r="4.5"/>'
           f'<text class="map-pin-label" font-size="{PIN_LABEL_SIZE}" '
           + (f'x="{fmt(px + 16)}" y="{fmt(py - 16)}">' if pin_side == "right" else
              f'x="{fmt(px - 16)}" y="{fmt(py - 16)}" text-anchor="end">')
           + f'{PIN_LABEL}</text>')
    print(f"pin      drawn at ({px:.1f}, {py:.1f}) of {VB_W}x{VB_H}; "
          f"frame {VB_W * M_PER_UNIT:.0f}m x {VB_H * M_PER_UNIT:.0f}m at {M_PER_UNIT} m/unit")

    drawn = [n for n, _ in order if any(r.startswith(f"  label  {n!r}") for r in report)]
    return out, defs, labels, shields, pin, drawn, stamp


def alt_text(drawn: list) -> str:
    near = [as_signed(n) for n in drawn if n != PIN_STREET]
    tail = ""
    if near:
        tail = (", near " + ", ".join(near[:-1]) + (" and " if len(near) > 1 else "") + near[-1])
    return (f"Map of the roads around Tri-County Collision, marked on {as_signed(PIN_STREET)} in "
            f"Southampton{tail}. Opens directions in Google Maps.")


def build_svg(parts) -> tuple:
    out, defs, labels, shields, pin, drawn, stamp = parts
    alt = alt_text(drawn)
    svg = (f'<a href="{MAPS_HREF}" target="_blank" rel="noopener">'
           f'<svg viewBox="0 0 {VB_W} {VB_H}" role="img" aria-label="{alt}">'
           f'<defs>{"".join(defs)}</defs>{"".join(out)}{"".join(labels)}'
           f'{"".join(shields)}{pin}</svg></a>')
    return svg, alt, stamp


MARK_RE = re.compile(r"(<!-- MAP:BEGIN[^>]*-->)(.*?)(\n\s*<!-- MAP:END -->)", re.S)


def patch_page(html: str, svg: str, stamp: str) -> str:
    """Writes the drawing between the two markers and nowhere else, and
    proves it before main() writes a byte: exactly one marker pair, and
    exactly one map in the result."""
    if len(MARK_RE.findall(html)) != 1:
        raise SystemExit("FAILED: the page must carry exactly one MAP:BEGIN/MAP:END pair")
    indent = "            "
    body = (f"\n{indent}<!-- Drawn from OpenStreetMap data, base timestamp {stamp}. "
            f"Do not edit by hand. -->\n{indent}{svg}")
    out = MARK_RE.sub(lambda m: m.group(1) + body + m.group(3), html)
    if out.count('<svg viewBox="0 0 %d %d" role="img"' % (VB_W, VB_H)) != 1:
        raise SystemExit("FAILED: the patched page does not carry exactly one map")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--data", help="a cached Overpass response to draw from")
    src.add_argument("--fetch", help="make the one query and cache it here (outside the repo)")
    ap.add_argument("--out-dir", help="write map.svg here and leave docs/ alone")
    a = ap.parse_args()

    if a.fetch:
        if os.path.abspath(a.fetch).startswith(ROOT + os.sep):
            raise SystemExit("FAILED: the cache is a derivative database and stays outside the repo")
        data = fetch(a.fetch)
    else:
        with open(a.data, encoding="utf-8") as f:
            data = json.load(f)

    svg, alt, stamp = build_svg(draw(data))
    print(f"alt      {alt}")
    print(f"size     {len(svg.encode())} bytes of inline SVG")

    if a.out_dir:
        os.makedirs(a.out_dir, exist_ok=True)
        with open(os.path.join(a.out_dir, "map.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote    {os.path.join(a.out_dir, 'map.svg')} (docs/ untouched)")
        return 0
    with open(PAGE, encoding="utf-8") as f:
        html = f.read()
    new = patch_page(html, svg, stamp)
    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"patched  {os.path.relpath(PAGE, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
