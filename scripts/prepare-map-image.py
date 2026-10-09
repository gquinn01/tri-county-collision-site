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

THE SCHEMA NOW CARRIES THIS PIN, corrected forward 2026-09-25. When this
script was written (3.54) the coordinates were kept out of the schema, which
had its own owner question (4.7). Greg's ruling of 2026-09-25 (3.56) adopted
the verified pin as the schema's geo, so the pin and geo are now ONE pair of
values: GEO_LAT and GEO_LON in scripts/audit.py, which this script reads.
The map and the schema cannot disagree, because there is nothing to
disagree with.

WHY INLINE SVG. The palette lives in one place, docs/assets/site.css. An SVG
file loaded through <img> cannot read that stylesheet, so every colour would
be a hex typed here. Inline, every mark carries a class (.map-road,
.map-label, .map-pin...) that site.css paints, and the labels are set in the
site's own self-hosted Source Sans 3. No extra request, either.

A TOWN FRAME, added 2026-09-28, proposed-changes.md 3.63. The town-page
template carries a map in its directions section: one drawing that shows
the town and the shop together, made the same way, from the same one
Overpass query, at a wider frame. FRAMES below holds each frame; "contact"
is the original and draws exactly what it always drew. A town frame adds
ONE refusal to the pin's: the town's reference corner must be a node the
two named roads actually share in the data, within max_m of the town's
recorded place point, or nothing is drawn. At a town frame's scale only
the main road classes are drawn, and only the roads the recorded routing
uses are named, because a directions diagram labels the way and not the
county.

USAGE:
    python3 scripts/prepare-map-image.py --data PATH          # draw from a cached response
    python3 scripts/prepare-map-image.py --fetch PATH         # one query, cache it, draw
    ... --frame NAME     which frame, from FRAMES: contact (the default), jamison
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
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "docs", "contact-us", "index.html")

# THE PIN is the schema's geo, read from scripts/audit.py rather than
# typed here: two values that must agree are one value. Google's own place
# point for the shop, verified 2026-09-24 (3.54) and adopted 2026-09-25
# (3.56). It must still fall inside an OSM building footprint for this
# script to draw at all.
_spec = importlib.util.spec_from_file_location("audit", os.path.join(HERE, "audit.py"))
_audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_audit)
PIN_LAT, PIN_LON = _audit.GEO_LAT, _audit.GEO_LON

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
PIN_LABEL = "Tri County Collision Center"
PIN_LABEL_SIZE = 17
MIN_LABEL_RUN = 150          # units of road a name needs to be written along

MAPS_HREF = ("https://www.google.com/maps/search/?api=1&amp;query=Tri%20County%20Collision%20Center"
             "%2C%20995%20Jaymor%20Rd%2C%20Southampton%2C%20PA%2018966")

# THE FRAMES. "contact" repeats the constants above exactly, so choosing it
# changes nothing; a town frame overrides them. Every value is recorded in
# proposed-changes.md with the record that set it.
MAIN_CLASSES = ("motorway", "trunk", "primary", "secondary", "tertiary",
                "motorway_link", "trunk_link", "primary_link", "secondary_link",
                "tertiary_link")
FRAMES = {
    # THE CONTACT FRAME NO LONGER PATCHES A PAGE, from 3.65: /contact-us/
    # carries a Google Maps embed on Greg's ruling. Its drawing is kept as
    # scripts/fixtures/contact-map-reference.svg, and redrawing it with
    # --check-against that file is the proof the town frames never disturb
    # it. It draws to --out-dir only.
    "contact": {"PAGE": None},
    # 3.63. The corner is where the 3.62 routing starts: OSM node 158375416,
    # Jamison, place=village, 40.2548297 -75.0893372, which sits at York Road
    # and Almshouse Road. The frame is portrait because the two points lie
    # nearly north and south; 24 m a unit reaches both routes the record
    # names, the one by Bristol Road and Second Street Pike and the one by
    # County Line Road. Only the roads those routes use are named.
    "jamison": {
        "PAGE": os.path.join(ROOT, "docs", "areas-served-collision-repair-jamison-pa", "index.html"),
        "VB_W": 360, "VB_H": 480, "M_PER_UNIT": 24.0,
        "FRAME_CX_LAT": 40.2104, "FRAME_CX_LON": -75.0703,
        "QUERY_BBOX": (40.1520, -75.1300, 40.2690, -75.0100),
        "ROAD_CLASSES": MAIN_CLASSES,
        "LABEL_NEAR_M": 0,
        # THE ROUTE DECIDES WHAT IS NAMED, not a list typed here. OSM renames
        # a road as it goes (West Bristol Road becomes East Bristol Road,
        # York Road has North and South pieces), so a typed list is wrong in
        # exactly the places a driver turns. The recorded OSRM routing is
        # drawn as the way through; its ways' own names and route numbers
        # are the labels and shields; everything else is context.
        "ROUTE_REQUIRED": True,
        # THE PRIMARY ROUTE ONLY, Greg's ruling of 2026-09-28 and the town
        # template's rule (3.63). The map is a directions DIAGRAM: it draws
        # exactly what the page's numbered steps say, and the alternative
        # lives in the page's prose. Drawn with both, the alternative's
        # County Line Road could not be named at this scale, and a road
        # drawn as the way through but unnamed fails the diagram's standard.
        "PRIMARY_ONLY": True,
        # The recorded routing this frame must agree with: TOWN_ROUTES in
        # scripts/audit.py (3.65). The routing file's figures must match it,
        # and every label drawn must be a road it drives.
        "ROUTE_KEY": "jamison-pa",
        # Minor roads are fetched only near the two ends, where the first
        # and last turns are: the shop's corner is the same for every town.
        "MINOR_NEAR_M": 450,
        "WIDTH_SCALE": 0.42,
        "JOIN_TOL": 2.0,
        # TYPE SCALED TO THE FRAME, so it renders at the contact map's size:
        # this viewBox is 360 units wide against contact's 480 and sits in
        # a column of about the same width, so 11 units read as the contact
        # map's 16 do, about 16px at 1440 and 11px on a phone.
        "LABEL_SIZE": 11, "SHIELD_SIZE": 10, "PIN_LABEL_SIZE": 12.5,
        "CORNER": {"label": "Jamison", "roads": ("York Road", "Almshouse Road"),
                   "place": (40.2548297, -75.0893372), "max_m": 60},
        "TOWN": "Jamison",
    },
}


def town_frame(key: str, name: str, route: dict) -> dict:
    """A town frame DERIVED, not typed (3.81): from TOWN_ROUTES[key] (the
    corner, its place point, its radius) and the recorded routing's own
    geometry. The width is Jamison's 360 units with Jamison's 11-unit
    labels, which is what holds the 10.5px label floor on a phone: the card
    draws the map about 348px wide at 390, so a label renders at
    11 x 348 / 360 = 10.6px. The height follows the route's shape, 240 to 480
    units, and the scale is whatever fits the route, the corner and the pin
    with a quarter of the frame to spare."""
    rec = _audit.TOWN_ROUTES[key]
    pts = [(lat, lon) for lon, lat in route["routes"][0]["geometry"]["coordinates"]]
    pts += [(rec["corner"][3], rec["corner"][4]), (PIN_LAT, PIN_LON)]
    s_, n_ = min(p[0] for p in pts), max(p[0] for p in pts)
    w_, e_ = min(p[1] for p in pts), max(p[1] for p in pts)
    clat, clon = (s_ + n_) / 2, (w_ + e_) / 2
    h_m = (n_ - s_) * 110574.0
    w_m = (e_ - w_) * 111320.0 * math.cos(math.radians(clat))
    vb_w = 360
    vb_h = int(max(240, min(480, round(vb_w * h_m / max(w_m, 1) / 10) * 10)))
    mpu = math.ceil(max(w_m * 1.25 / vb_w, h_m * 1.25 / vb_h) * 2) / 2
    half_h = vb_h / 2 * mpu * 1.15 / 110574.0
    half_w = vb_w / 2 * mpu * 1.15 / (111320.0 * math.cos(math.radians(clat)))
    return {
        "PAGE": os.path.join(ROOT, "docs", _audit.TOWN_ROUTE_PREFIX + key, "index.html"),
        "VB_W": vb_w, "VB_H": vb_h, "M_PER_UNIT": mpu,
        "FRAME_CX_LAT": round(clat, 4), "FRAME_CX_LON": round(clon, 4),
        "QUERY_BBOX": (round(clat - half_h, 4), round(clon - half_w, 4),
                       round(clat + half_h, 4), round(clon + half_w, 4)),
        "ROAD_CLASSES": MAIN_CLASSES, "LABEL_NEAR_M": 0,
        "ROUTE_REQUIRED": True, "PRIMARY_ONLY": True, "ROUTE_KEY": key,
        "MINOR_NEAR_M": 450, "WIDTH_SCALE": 0.42,
        # Jamison's join tolerance, 2 units at 24 m a unit, held at the same
        # ground distance, 48m, whatever this frame's scale.
        "JOIN_TOL": round(48.0 / mpu, 2),
        "LABEL_SIZE": 11, "SHIELD_SIZE": 10, "PIN_LABEL_SIZE": 12.5,
        "CORNER": {"label": name, "roads": tuple(rec["corner"][:2]),
                   "place": (rec["place"][1], rec["place"][2]), "max_m": rec["max_m"]},
        "TOWN": name,
    }


LABEL_ONLY = None
CORNER = None
TOWN = None
ROUTE_ROADS = None          # set in draw() from the route, never typed
SHIELD_REFS = None
ROUTE_REQUIRED = False
PRIMARY_ONLY = False
ROUTE_KEY = None
ROUTE_STEPS = []            # the drawn route's roads in driving order, set in draw()
MINOR_NEAR_M = 0
WIDTH_SCALE = 1.0
ROUTE_ON_M = 25             # a way is on the route when its points lie this close to it
# Two runs of one road join when their ends meet within this many units.
# 0.5 is the contact frame's value, 1.7m on the ground; a wider frame holds
# the ground distance about the same by scaling it, so a road that OSM
# splits at every intersection still reads as one road (3.63).
JOIN_TOL = 0.5
ROUTE_ALIGN_DEG = 30        # ...and runs along it: a segment counts only when it is within
                            # this angle of the route segment it lies on, so a road that
                            # CROSSES the route counts for nothing however close it passes
ROUTE_MIN_M = 15            # the aligned length a way needs; OSM splits roads into short ways
OSRM = "https://router.project-osrm.org/route/v1/driving/"


def use_frame(name: str):
    """Sets the module's frame constants from FRAMES[name] and rebuilds the
    query from them. The contact frame sets nothing and so is unchanged."""
    g = globals()
    for k, v in FRAMES[name].items():
        g[k] = v
    g["QUERY"] = ('[out:json][timeout:50];('
                  'way["highway"~"^(' + "|".join(g["ROAD_CLASSES"]) + ')$"]'
                  '({0},{1},{2},{3});'
                  'way["building"](around:120,{4},{5}););out geom tags;').format(
                      *g["QUERY_BBOX"], PIN_LAT, PIN_LON)
    if g["ROUTE_REQUIRED"]:
        # 3.81: a town frame's data carries each way's node list, so the
        # route's ways are found by OSM node, as roads_driven was.
        g["QUERY"] = g["QUERY"].replace("out geom tags;", "out geom;")
    if g["MINOR_NEAR_M"]:
        ends = [(PIN_LAT, PIN_LON)] + ([g["CORNER"]["place"]] if g["CORNER"] else [])
        g["QUERY"] = g["QUERY"].replace('way["building"]', "".join(
            'way["highway"~"^(unclassified|residential)$"](around:{0},{1},{2});'.format(
                g["MINOR_NEAR_M"], la, lo) for la, lo in ends) + 'way["building"]')


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


def fetch_route(cache_path: str) -> dict:
    """ONE OSRM request for a town frame: from the town's recorded place
    point to the pin, with alternatives, full geometry. Cached outside the
    repo like the Overpass response, and never retried in a loop."""
    (la, lo) = CORNER["place"]
    url = (f"{OSRM}{lo},{la};{PIN_LON},{PIN_LAT}"
           "?alternatives=true&overview=full&geometries=geojson&steps=true")
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}),
                                 timeout=70).read()
    data = json.loads(raw)
    if data.get("code") != "Ok":
        raise SystemExit(f"FAILED: OSRM answered {data.get('code')}. Nothing was drawn.")
    with open(cache_path, "wb") as f:
        f.write(raw)
    print(f"fetched  {url.split('?')[0]}  {len(raw)} bytes  -> {cache_path}")
    return data


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
                if math.dist(a[-1], b[0]) < JOIN_TOL and continues(a, b):
                    runs[i] = a + b[1:]
                elif math.dist(a[-1], b[-1]) < JOIN_TOL and continues(a, b[::-1]):
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
def draw(data: dict, route: dict = None):
    global ROUTE_ROADS, SHIELD_REFS, LABEL_ONLY, ROUTE_STEPS
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

    # 1b. A TOWN FRAME'S CORNER must be a point the two named roads share in
    # the data, within max_m of the town's recorded place point, or nothing
    # is drawn: the same rule as the pin, for the other end of the route.
    corner = None
    if CORNER:
        ra, rb = CORNER["roads"]
        pa = {(g["lat"], g["lon"]) for e in els if e.get("tags", {}).get("name") == ra
              and e.get("tags", {}).get("highway") for g in e.get("geometry", [])}
        pb = {(g["lat"], g["lon"]) for e in els if e.get("tags", {}).get("name") == rb
              and e.get("tags", {}).get("highway") for g in e.get("geometry", [])}
        shared = pa & pb
        plat, plon = CORNER["place"]
        def metres(q):
            return math.hypot((q[0] - plat) * 110574.0,
                              (q[1] - plon) * 111320.0 * math.cos(math.radians(plat)))
        if not shared:
            raise SystemExit(f"FAILED: {ra} and {rb} share no point in the data. Nothing was drawn.")
        corner = min(shared, key=metres)
        if metres(corner) > CORNER["max_m"]:
            raise SystemExit(f"FAILED: the nearest {ra}/{rb} junction is {metres(corner):.0f}m from "
                             f"{CORNER['label']}'s recorded point, over {CORNER['max_m']}m. Nothing was drawn.")
        print(f"corner   {ra} meets {rb} at {corner[0]}, {corner[1]}, "
              f"{metres(corner):.0f}m from {CORNER['label']}'s recorded point {plat}, {plon}")

    # 1c. A TOWN FRAME'S ROUTE, from the recorded routing. Every route must
    # start at the corner and end at the pin, or nothing is drawn. A way is
    # on the route when most of its points lie within ROUTE_ON_M of one.
    on_route = set()
    if ROUTE_REQUIRED:
        if not route:
            raise SystemExit("FAILED: this frame draws its route and was given none. Nothing was drawn.")
        k = math.cos(math.radians(PIN_LAT))
        def m(a, b):
            return math.hypot((a[0] - b[0]) * 110574.0, (a[1] - b[1]) * 111320.0 * k)
        lines = []
        drawn_routes = route["routes"][:1] if PRIMARY_ONLY else route["routes"]
        # 3.65: ONE ROUTING. The file drawn from must BE the recorded routing,
        # to the figures the pages print from, or nothing is drawn.
        rec = _audit.TOWN_ROUTES[ROUTE_KEY] if ROUTE_KEY else None
        if rec:
            got_mi = round(drawn_routes[0]["distance"] / 1609.344, 2)
            got_min = round(drawn_routes[0]["duration"] / 60, 1)
            if (got_mi, got_min) != (rec["miles"], rec["minutes"]):
                raise SystemExit(f"FAILED: this routing file measures {got_mi} mi, {got_min} min; the "
                                 f"recorded routing (TOWN_ROUTES[{ROUTE_KEY!r}]) is {rec['miles']} mi, "
                                 f"{rec['minutes']} min. Re-record it or use the recorded file. Nothing was drawn.")
            print(f"route    agrees with TOWN_ROUTES[{ROUTE_KEY!r}]: {got_mi} mi, {got_min} min")
        # The alt text reads the primary route as a driver drives it: each
        # road once, in order, with its route number; a road that only
        # changes its name under the same number is not a new turn.
        ROUTE_STEPS = []
        for st in drawn_routes[0]["legs"][0]["steps"]:
            nm, rf = st.get("name", ""), st.get("ref", "")
            if not nm or st["maneuver"]["type"] in ("depart", "arrive"):
                continue
            if ROUTE_STEPS and (ROUTE_STEPS[-1][0] == nm or (rf and ROUTE_STEPS[-1][1] == rf)):
                continue
            ROUTE_STEPS.append((nm, rf))
        for i, rt in enumerate(drawn_routes):
            pts = [(la, lo) for lo, la in rt["geometry"]["coordinates"]]
            s_m, e_m = m(pts[0], corner), m(pts[-1], (PIN_LAT, PIN_LON))
            if s_m > CORNER["max_m"] or e_m > 60:
                raise SystemExit(f"FAILED: route {i} starts {s_m:.0f}m from the corner or ends "
                                 f"{e_m:.0f}m from the pin. Nothing was drawn.")
            lines.append(pts)
            print(f"route    {i}: {rt['distance'] / 1609.344:.2f} mi, {rt['duration'] / 60:.1f} min "
                  f"free-flow, {len(pts)} points, starts {s_m:.0f}m from the corner, ends {e_m:.0f}m from the pin")
        # Segments bucketed by ~200m cells, so the test is quick.
        cell = 0.002
        grid = {}
        for pts in lines:
            for a, b in zip(pts, pts[1:]):
                for la in (a[0], b[0]):
                    for lo in (a[1], b[1]):
                        grid.setdefault((round(la / cell), round(lo / cell)), set()).add((a, b))
        def near_route(q):
            """The route segment's bearing, in degrees mod 180, if q lies
            within ROUTE_ON_M of it; None otherwise."""
            key = (round(q[0] / cell), round(q[1] / cell))
            for dla in (-1, 0, 1):
                for dlo in (-1, 0, 1):
                    for a, b in grid.get((key[0] + dla, key[1] + dlo), ()):
                        ax, ay = 0.0, 0.0
                        bx, by = (b[1] - a[1]) * 111320.0 * k, (b[0] - a[0]) * 110574.0
                        qx, qy = (q[1] - a[1]) * 111320.0 * k, (q[0] - a[0]) * 110574.0
                        L = bx * bx + by * by
                        t = 0.0 if not L else max(0.0, min(1.0, (qx * bx + qy * by) / L))
                        if L and math.hypot(qx - t * bx, qy - t * by) <= ROUTE_ON_M:
                            return math.degrees(math.atan2(by, bx)) % 180
            return None
        for e in els:
            t = e.get("tags", {})
            if t.get("highway") and e.get("geometry"):
                g = [(p["lat"], p["lon"]) for p in e["geometry"]]
                near = [near_route(q) for q in g]
                along = 0.0
                for (a, na), (b, nb) in zip(zip(g, near), zip(g[1:], near[1:])):
                    if na is None or nb is None:
                        continue
                    seg = math.degrees(math.atan2((b[0] - a[0]) * 110574.0,
                                                  (b[1] - a[1]) * 111320.0 * k)) % 180
                    off = min(abs(seg - na), 180 - abs(seg - na))
                    if off <= ROUTE_ALIGN_DEG:
                        along += m(a, b)
                way_len = sum(m(a, b) for a, b in zip(g, g[1:]))
                # A way counts when enough of it runs along the route: at
                # least ROUTE_MIN_M, and either half the way or 150m of it,
                # so a side road that only touches the route at a junction
                # does not come along whole.
                if along >= ROUTE_MIN_M and (along >= 0.5 * way_len or along >= 150):
                    on_route.add(e["id"])
        # 3.81: ON THE ROUTE BY OSM NODE, when the data allows it. The
        # geometric test above read a Turnpike bridge crossing Street Road
        # (Bensalem) and North York Road, collinear past the corner
        # (Warminster), as driven; the routing's own node record disproves
        # both. When the routing file carries OSRM's node list and the map
        # data carries each way's nodes, a way is on the route exactly when
        # the route traverses its edges for ROUTE_MIN_M or more: the method
        # that built roads_driven, one source of truth. The geometric test
        # stays only as the fallback for older caches without node lists,
        # which is what keeps Jamison's map and the contact reference
        # byte-identical.
        route_nodes = [rt["legs"][0].get("annotation", {}).get("nodes") for rt in drawn_routes]
        way_nodes = [e for e in els if e.get("tags", {}).get("highway") and e.get("nodes") and e.get("geometry")]
        if all(route_nodes) and way_nodes:
            edges = {frozenset(pr) for ns in route_nodes for pr in zip(ns, ns[1:])}
            by_node = set()
            for e in way_nodes:
                g = [(p["lat"], p["lon"]) for p in e["geometry"]]
                along = sum(m(g[i], g[i + 1]) for i, pr in enumerate(zip(e["nodes"], e["nodes"][1:]))
                            if frozenset(pr) in edges)
                if along >= ROUTE_MIN_M:
                    by_node.add(e["id"])
            def _names(ids):
                return {e["tags"].get("name") for e in els if e["id"] in ids and e.get("tags", {}).get("name")}
            dropped = sorted(_names(on_route) - _names(by_node))
            print(f"route    on the route by OSM node identity (3.81): {len(by_node)} ways"
                  + (f"; the geometric test's {dropped} are not driven" if dropped else ""))
            on_route = by_node
        else:
            print("route    no node lists in this data: on the route by the geometric test (fallback)")
        ROUTE_ROADS = True
        names_on = sorted({e["tags"].get("name") for e in els if e["id"] in on_route and e["tags"].get("name")})
        refs_on = sorted({e["tags"].get("ref") for e in els if e["id"] in on_route and e["tags"].get("ref")})
        LABEL_ONLY, SHIELD_REFS = tuple(names_on), tuple(refs_on)
        print(f"route    {len(on_route)} OSM ways lie on it; named {names_on}; numbered {refs_on}")
        if rec:
            stray = sorted(set(names_on) - set(rec["roads_driven"]))
            if stray:
                raise SystemExit(f"FAILED: the route's OSM ways carry {stray}, which the recorded "
                                 f"routing's roads_driven does not. Re-record the routing. Nothing was drawn.")

    # 2. Roads, clipped to the frame, by class.
    roads = []
    for e in els:
        t = e.get("tags", {})
        hw = t.get("highway")
        if hw not in STYLE or not e.get("geometry"):
            continue
        pts = [project(g["lat"], g["lon"]) for g in e["geometry"]]
        for run in clip_polyline(pts):
            roads.append((hw, t.get("name", ""), t.get("ref", ""), run, e["id"] in on_route))
    by_class = {}
    for hw, *_ in roads:
        by_class[hw] = by_class.get(hw, 0) + 1
    if ROUTE_ROADS:
        # A context road far from both ends is drawn only if it is a main
        # road; the minor ones were fetched for the ends' last turns.
        roads = [r for r in roads if r[4] or r[0] in MAIN_CLASSES]
    print(f"roads    {len(roads)} runs in frame: " +
          ", ".join(f"{k} {v}" for k, v in sorted(by_class.items())))

    out = [f'<rect class="map-ground" width="{VB_W}" height="{VB_H}"/>']
    if ROUTE_ROADS is not None:
        # A TOWN FRAME'S HIERARCHY IS THE ROUTE. Every road is scaled to the
        # frame; the context roads take the quiet casing, the route's roads
        # the major one and a wider line. No new colour: the pin stays the
        # map's one oxblood mark.
        route = [r for r in roads if r[4]]
        ctx = [r for r in roads if not r[4]]
        roads = ctx + route
        for group, major, scale in ((ctx, False, 0.8), (route, True, 1.35)):
            for layer in ("case", "road"):
                for cls in DRAW_ORDER:
                    runs = [r for r in group if r[0] == cls]
                    if not runs:
                        continue
                    case_w, road_w, _m = STYLE[cls]
                    w = (case_w if layer == "case" else road_w) * WIDTH_SCALE * scale
                    klass = (("map-case map-case--major" if major else "map-case")
                             if layer == "case" else "map-road")
                    out.append(f'<path class="{klass}" stroke-width="{fmt(w)}" '
                               f'd="{" ".join(d_of(r[3]) for r in runs)}"/>')
    for layer in (() if ROUTE_ROADS is not None else ("case", "road")):
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
    for hw, name, ref, run, _on in roads:
        if not name:
            continue
        if LABEL_ONLY is not None:
            # A town frame names only the roads its recorded route uses.
            if _on and name in LABEL_ONLY:
                names.setdefault(name, []).append(run)
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
    if LABEL_ONLY is not None:
        # Every road a town frame names is a road the route uses, so each
        # ranks as a through road.
        cls_of.update({n: "tertiary" for n in names if cls_of.get(n) not in LABEL_CLASSES})
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
        for hw, _n, rref, run, _on in roads:
            major = _on if ROUTE_ROADS else hw in LABEL_CLASSES
            if major and rref != ref:
                for a_, b_ in zip(run, run[1:]):
                    steps = max(1, int(math.dist(a_, b_) / 3))
                    pts.extend((a_[0] + (b_[0] - a_[0]) * k / steps,
                                a_[1] + (b_[1] - a_[1]) * k / steps) for k in range(steps + 1))
        return pts

    shield_c = []
    for ref in sorted({r[2] for r in roads if r[2]
                       and (SHIELD_REFS is None or r[2] in SHIELD_REFS)}):
        shown = ref_text(ref)
        vis = visible(max(join_runs([r[3] for r in roads if r[2] == ref
                                     and (r[4] or not ROUTE_ROADS)]), key=length), 16)
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

    corner_opts = [(None, [])]
    if corner:
        cx, cy = project(*corner)
        cw = text_w(CORNER["label"], PIN_LABEL_SIZE)
        corner_opts = [(side, [box]) for side, box in (
            ("right", (cx - 10, cy - 14, cx + 18 + cw, cy + 14)),
            ("left", (cx - 18 - cw, cy - 14, cx + 10, cy + 14)))
            if box[0] >= 2 and box[2] <= VB_W - 2]
        if not corner_opts:
            raise SystemExit("FAILED: the corner's name fits on neither side. Nothing was drawn.")
    chosen = None
    for side, pbox in pin_opts:
        for cside, cbox in corner_opts:
            best["score"], best["pick"] = None, None
            search(0, list(pbox) + list(cbox), [], [])
            if chosen is None or best["score"] > chosen[0]:
                chosen = (best["score"], best["pick"], side, pbox, cside)
    _, pick, pin_side, pin_box, corner_side = chosen
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
    if corner:
        report.append(f"  corner {CORNER['label']!r} set {corner_side} of the corner")
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
    if corner:
        cx, cy = project(*corner)
        pin += (f'<circle class="map-corner" cx="{fmt(cx)}" cy="{fmt(cy)}" r="7"/>'
                f'<text class="map-pin-label" font-size="{PIN_LABEL_SIZE}" '
                + (f'x="{fmt(cx + 14)}" y="{fmt(cy + 6)}">' if corner_side == "right" else
                   f'x="{fmt(cx - 14)}" y="{fmt(cy + 6)}" text-anchor="end">')
                + f'{CORNER["label"]}</text>')
        print(f"corner   drawn at ({cx:.1f}, {cy:.1f})")
    print(f"pin      drawn at ({px:.1f}, {py:.1f}) of {VB_W}x{VB_H}; "
          f"frame {VB_W * M_PER_UNIT:.0f}m x {VB_H * M_PER_UNIT:.0f}m at {M_PER_UNIT} m/unit")

    drawn = [n for n, _ in order if any(r.startswith(f"  label  {n!r}") for r in report)]
    # 3.65: NOTHING LABELLED THAT THE DRIVE DOES NOT USE. Judged against the
    # roads driven, not the step names alone (Greg's ruling): West Bristol
    # Road is "East Bristol Road" in OSM for half its length.
    if ROUTE_KEY:
        allowed = set(_audit.TOWN_ROUTES[ROUTE_KEY]["roads_driven"])
        off = [n for n in drawn if n not in allowed]
        if off:
            raise SystemExit(f"FAILED: the map would label {off}, which the recorded routing does "
                             f"not drive. Nothing was drawn.")
        print(f"labels   all {len(drawn)} named roads are roads the recorded routing drives: {drawn}")
    return out, defs, labels, shields, pin, drawn, stamp


def alt_text(drawn: list) -> str:
    if CORNER:
        a, b = (as_signed(r) for r in CORNER["roads"])
        # THE SENTENCE ENDS ON THE SHOP, NEVER ON A ROAD. The route's last
        # road is the shop's own street, and "Jaymor Rd." with the period is
        # a spelling scripts/audit.py fails as a second address, which is
        # how the first draft of this line was caught (3.63).
        way = [as_signed(n) + (f" ({ref_text(r)})" if r else "") for n, r in ROUTE_STEPS]
        return (f"Map of the drive from {CORNER['label']}, at {a} and {b}, "
                + ("by " + ", ".join(way[:-1]) + (" and " if len(way) > 1 else "") + way[-1] + " "
                   if way else "")
                + "to Tri County Collision Center in Southampton. Opens directions in Google Maps.")
    near = [as_signed(n) for n in drawn if n != PIN_STREET]
    tail = ""
    if near:
        tail = (", near " + ", ".join(near[:-1]) + (" and " if len(near) > 1 else "") + near[-1])
    return (f"Map of the roads around Tri County Collision Center, marked on {as_signed(PIN_STREET)} in "
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
    ap.add_argument("--check-against", help="compare the drawing to this reference SVG, byte for "
                    "byte, and exit 1 if it differs (the contact frame's non-regression proof)")
    ap.add_argument("--route", help="a town frame's cached OSRM routing to draw")
    ap.add_argument("--fetch-route", help="make the one OSRM request and cache it here (outside the repo)")
    ap.add_argument("--frame", default="contact", choices=sorted(FRAMES) + ["town"],
                    help="which frame to draw, from FRAMES (default: contact), or \"town\" "
                         "with --town and --name for a frame derived from TOWN_ROUTES")
    ap.add_argument("--town", help="with --frame town: the TOWN_ROUTES key")
    ap.add_argument("--name", help="with --frame town: the town's name as the corner label")
    a = ap.parse_args()
    if a.frame == "town":
        if not (a.town and a.name and a.route):
            raise SystemExit("FAILED: --frame town needs --town, --name and the recorded --route.")
        with open(a.route, encoding="utf-8") as f:
            FRAMES["town"] = town_frame(a.town, a.name, json.load(f))
        print(f"label    {FRAMES['town']['LABEL_SIZE']} units in {FRAMES['town']['VB_W']}: about "
              f"{FRAMES['town']['LABEL_SIZE'] * 348 / FRAMES['town']['VB_W']:.1f}px on a 390 phone "
              f"(floor 10.5)")
    use_frame(a.frame)
    print(f"frame    {a.frame}: {VB_W}x{VB_H} at {M_PER_UNIT} m/unit, centre "
          f"{FRAME_CX_LAT}, {FRAME_CX_LON}, page "
          f"{os.path.relpath(PAGE, ROOT) if PAGE else 'none (out-dir only)'}")

    if a.fetch:
        if os.path.abspath(a.fetch).startswith(ROOT + os.sep):
            raise SystemExit("FAILED: the cache is a derivative database and stays outside the repo")
        data = fetch(a.fetch)
    else:
        with open(a.data, encoding="utf-8") as f:
            data = json.load(f)

    route = None
    if a.fetch_route:
        if os.path.abspath(a.fetch_route).startswith(ROOT + os.sep):
            raise SystemExit("FAILED: the routing cache stays outside the repo")
        route = fetch_route(a.fetch_route)
    elif a.route:
        with open(a.route, encoding="utf-8") as f:
            route = json.load(f)
    svg, alt, stamp = build_svg(draw(data, route))
    print(f"alt      {alt}")
    print(f"size     {len(svg.encode())} bytes of inline SVG")

    if a.check_against:
        with open(a.check_against, encoding="utf-8") as f:
            ref = f.read()
        if svg != ref:
            print(f"DIFFERS  from {a.check_against}: {len(svg.encode())} bytes against {len(ref.encode())}")
            return 1
        print(f"matches  {a.check_against}, byte for byte ({len(svg.encode())} bytes)")
    if PAGE is None and not a.out_dir:
        raise SystemExit("FAILED: this frame patches no page; give --out-dir (and --check-against).")
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
