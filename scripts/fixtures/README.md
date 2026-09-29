# Fixtures

## contact-map-reference.svg

The directions map `/contact-us/` shipped from 3.54 to 3.65, drawn by
`scripts/prepare-map-image.py` (the "contact" frame) from one Overpass query,
OpenStreetMap base timestamp 2026-09-24T20:08:04Z. From 3.65 the contact page
carries a Google Maps embed instead, and this file is kept so the script's
non-regression proof survives the page no longer shipping it: redrawn from its
own cached data, the contact frame must match this file byte for byte, which
proves that the town frames never disturbed it.

    python3 scripts/prepare-map-image.py --data CONTACT_CACHE \
        --out-dir DIR --check-against scripts/fixtures/contact-map-reference.svg

The cache is a derivative database and stays outside the repo, as every
Overpass response does.

**Map data (c) OpenStreetMap contributors, available under the Open Database
License** (https://www.openstreetmap.org/copyright,
https://opendatacommons.org/licenses/odbl/). The drawing is a produced work
under ODbL 4.3, and this notice is the credit it carries.

Nothing in this folder is served: it is outside `docs/`.
