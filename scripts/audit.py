#!/usr/bin/env python3
"""
SEO + AEO Site Auditor: the "scanning" half of your agent team.

This is a real, working audit script. It checks a page for the on-page
factors that matter most for local businesses, both classic SEO
(ranking in Google) and AEO / answer engine optimization (being the
answer that AI assistants like ChatGPT, Claude, Perplexity, and
Google's AI Overviews give when someone asks "best spa near me").
It then writes a markdown report. In the GitHub workflow, an AI agent
(Claude) reads this report, explains it in plain English, and files it
as a GitHub Issue with recommended fixes.

The site is no longer one page, so this audits EVERY page and scores
each one separately. A single page dragging the site down is visible by
name in the summary table instead of being averaged away.

Usage:
    python3 scripts/audit.py                           # every page under docs/
    python3 scripts/audit.py docs/index.html           # one local file
    python3 scripts/audit.py docs/services/seo/        # a folder
    python3 scripts/audit.py https://example.com/      # a live site, expanded
                                                       # via its sitemap.xml
    python3 scripts/audit.py --strict                  # exit 1 if any page < 100

No external packages needed: pure Python standard library.
"""

import argparse
import glob
import hashlib
import json
import math
import os
import posixpath
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

# The live site's page list comes from its own sitemap. Locally we glob
# the folder that IS the live site.
SITE_DIR = "docs"
SITEMAP_PATH = os.path.join(SITE_DIR, "sitemap.xml")
LLMS_PATH = os.path.join(SITE_DIR, "llms.txt")

# --- The NAP -----------------------------------------------------------
# Name, address, phone. Rule 6: these are character-identical everywhere
# they appear, on the site, in schema, on the Google Business Profile and
# in every directory. One spelling, no variants. This block is the single
# place the canonical spelling lives, so a page and a check can never
# disagree about it.
#
# PROVENANCE, because a fact on a client site is only as good as its
# source. Phone and address below are the values published on the shop's
# live WordPress site, read and confirmed on 2026-09-03 by Greg Quinn of
# Corcoran Communications, the vendor. The standards make the CLIENT-OWNER
# the fact-checker of record for a client site, so the vendor confirming
# is a deliberate exception and it is recorded here rather than blurred:
# owner sign-off on the NAP is still outstanding. Get it, and when you do,
# replace this paragraph with the date the owner confirmed. Until then a
# reader of this file knows exactly whose word these values rest on.
NAP_NAME = "Tri-County Collision"
NAP_STREET = "995 Jaymor Rd"
NAP_LOCALITY = "Southampton"
NAP_REGION = "PA"
NAP_POSTAL = "18966"
NAP_PHONE_DISPLAY = "(215) 322-5350"
NAP_PHONE_TEL = "+12153225350"

# The phone and email, in the formats they could plausibly be typed.
# Every visible mention of either is meant to be tappable: a reader on a
# phone should never have to memorize a number and retype it in the
# dialer. Mentions inside JSON-LD are data, not copy, and are skipped.
#
# The phone regex is deliberately loose about punctuation. It has to be:
# the point of the check is to CATCH a number typed some other way, and a
# pattern that only matched the canonical spelling would sail past
# "215.322.5350" as if it were not a phone number at all.
NAP_PHONE_RE = re.compile(r"\(?215\)?[\s.\-]?322[\s.\-]?5350")

# THE EMAIL CHECK IS ON, as of 2026-09-05. The canonical published
# address is contact@tricountycollision.com.
#
# PROVENANCE, on the same footing as the phone and address above. This is
# a VENDOR decision by Greg Quinn of Corcoran Communications, recorded as
# the same deliberate exception the rest of the NAP is recorded as: the
# standards make the CLIENT-OWNER the fact-checker of record, and owner
# sign-off on the NAP, email included, is still outstanding. When it
# lands, replace this paragraph with the date the owner confirmed.
#
# It is not a guess. contact@tricountycollision.com is the address the
# live site publishes in its AutoBodyShop JSON-LD and in the contact
# block on every service page. The live site ALSO prints
# info@tricountycollision.com in its footer, which is exactly the drift
# this check exists to stop: two addresses for one business read as two
# businesses to entity matching, and one of them is the one customers and
# insurers actually reach. The new site publishes ONE address, and any
# page here that prints the other one now fails.
NAP_EMAIL_RE = re.compile(r"contact@tricountycollision\.com")

# The OTHER address, the one the old site's footer carries. It is not a
# variant spelling to be corrected quietly, it is a second mailbox, and
# whether it forwards, is read, or is dead is the owner's to answer. Until
# then it does not go on a page here, and a page that carries it says so.
NAP_EMAIL_WRONG_RE = re.compile(r"info@tricountycollision\.com", re.I)

# --- The CallRail tracking number -------------------------------------
# (215) 709-9665 is a CallRail tracking number. The old WordPress site
# prints it in the header, and CallRail's own script swaps numbers into
# the page VISUALLY at runtime, which is the supported way to run call
# tracking without breaking NAP consistency.
#
# So the number never belongs in this site's source: not in the HTML, not
# in the schema, not in the template, not in a comment. A tracking number
# baked into the markup is a second phone number for one business, which
# is the Map Pack self-competition rule 6 exists to prevent, and it is
# the number a crawler and an AI assistant would then hand out as the
# shop's. The CallRail snippet gets added at cutover and does its
# swapping at runtime, over a page whose source says (215) 322-5350.
#
# This is a CRITICAL, not a warning. It is the kind of thing that gets
# pasted in during a hurried migration and is invisible by eye.
TRACKING_PHONE_RE = re.compile(r"\(?215\)?[\s.\-]?709[\s.\-]?9665")

# --- The chrome's recorded external links, 3.83 -----------------------
# The header and the footer are written by scripts/sync-chrome.py, and
# every link they carry must land on a real page under docs/ or on one of
# the two in CHROME_EXTERNAL_URLS, character for character: the DocuSign
# link, read off the live site's nav, which is Greg's guide for the nav
# (proposed-changes.md 3.83), and the footer's map link.
#
# The DocuSign PowerForm is the live nav's "Authorization Forms" item,
# carried over exactly. OWNER QUESTION 35: whether it is current. If the
# owner retires it, the item comes out by ruling, not silently.
DOCUSIGN_URL = ("https://powerforms.docusign.net/2919d585-3b16-4977-833f-75a24163bec3"
                "?env=na4&acct=228c4f1e-de2e-4461-9dbe-6a809b101cd4"
                "&accountId=228c4f1e-de2e-4461-9dbe-6a809b101cd4")
# The shop's CarWise estimate and appointment links, exactly as
# /contact-us/ has carried them since Greg's 2026-09-24 decision, owner
# confirmation that CarWise is still in use already on the list. They are
# NOT chrome allowances: the nav carried them in 3.83 and Greg withdrew
# them in 3.84, so they now record the contact page's two links. Holding
# /contact-us/ to them is a recorded option, not a check built today.
CARWISE_ESTIMATE_URL = ("https://www.carwise.com/online-photo-estimate/"
                        "tri-county-collision-center-southampton-pa-18966/481195")
CARWISE_APPOINTMENT_URL = ("https://www.carwise.com/auto-body-shops/book-appointment/"
                           "tri-county-collision-center-southampton-pa-18966/481195")
# The footer's map link, the same maps search the contact page uses.
MAPS_NAP_URL = ("https://www.google.com/maps/search/?api=1&query=Tri-County%20Collision"
                "%2C%20995%20Jaymor%20Rd%2C%20Southampton%2C%20PA%2018966")
CHROME_EXTERNAL_URLS = (DOCUSIGN_URL, MAPS_NAP_URL)

# The contact patterns that are actually live. Built from whichever of the
# two above is set, so turning one on or off changes nothing else.
NAP_CONTACT_RES = [(k, rx) for k, rx in
                   (("phone", NAP_PHONE_RE), ("email", NAP_EMAIL_RE))
                   if rx is not None]

# --- Address consistency ----------------------------------------------
# The street address is the NAP field that drifts, because it is the one
# with abbreviations in it. "Rd" becomes "Road", the ZIP goes missing, the
# comma moves. Each variant is a slightly different business as far as a
# search engine's entity matching is concerned, which is exactly the harm
# rule 6 exists to prevent, and none of it is visible by eye across
# thirty-odd pages.
#
# So: any page that says "Jaymor" at all is claiming to carry the
# address, and gets checked for the canonical spelling of it.
NAP_STREET_CANON = NAP_STREET
NAP_CITYLINE_CANON = f"{NAP_LOCALITY}, {NAP_REGION} {NAP_POSTAL}"
NAP_STREET_MENTION_RE = re.compile(r"Jaymor", re.I)

# --- The hours, defined once ------------------------------------------
# ADDED 2026-09-24, proposed-changes.md 3.54, as the mechanism 3.53
# proposed. The hours were two lines of footer text on six pages, one more
# in /contact-us/'s header, a box beside the map there, llms.txt and every
# page's openingHoursSpecification, with nothing holding them together.
# They are a fact customers act on, so a copy that drifts is a shop that
# answers the phone at the wrong time.
#
# THE VALUES ARE THE LIVE SITE'S, migrated: its schema says Monday to
# Friday 08:00 to 18:00 and carries "Saturday Hours: By appointment only".
# Owner confirmation against the Google Business Profile is outstanding
# (4.7). SUNDAY IS DELIBERATELY ABSENT. The live schema never mentions it,
# open or closed, so the record does not know it, and a page that says
# anything about Sunday is saying something nobody confirmed.
#
# The check, per page and on llms.txt: every day name, every "Mon-Fri"
# style range and every clock time in visible text must sit inside one of
# the two canonical strings below. Anything else is the hours written a
# second way, and it is a critical, same as a second spelling of the
# street. Any Sunday is a critical. The schema must say the same thing.
HOURS_WEEKDAYS = "Monday to Friday, 8 a.m. to 6 p.m."
HOURS_SATURDAY = "Saturday by appointment only"
HOURS_SCHEMA_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
HOURS_SCHEMA_OPENS = "08:00"
HOURS_SCHEMA_CLOSES = "18:00"

# --- The shop's coordinates, defined once ------------------------------
# ADOPTED BY GREG'S RULING OF 2026-09-25, proposed-changes.md 3.56. This is
# Google's own place point for the shop, VERIFIED 2026-09-24 three ways
# (3.54): it is the point Google's data gives for the footer's search; it
# falls inside the OpenStreetMap footprint of the building (way 902318081);
# and the satellite view shows the shop in that building, on the northeast
# side of Jaymor Rd at James Way and Knowles Ave.
#
# A VENDOR-VERIFIED EXCEPTION, recorded like the NAP's: the standards make
# the owner the fact-checker of record, and owner sign-off is outstanding.
# It folds into his NAP sign-off rather than being a separate ask.
#
# WHAT IT REPLACED, so nobody pastes that class of coordinate again: the
# live site's geo, 40.1660232, -75.0538596, about 220m west of the shop. Its
# latitude matched and its longitude did not, because it was a Google Maps
# URL's "@lat,lon", the viewport CENTRE, which Google shifts sideways for
# its side panel. It is not the pin. Take coordinates from the place's
# own data, never from a map URL.
#
# The check: every business node's geo in every page's schema equals these
# exactly. scripts/prepare-map-image.py draws its pin from the same two
# values, so the map and the schema cannot disagree.
GEO_LAT = 40.1660232
GEO_LON = -75.0512847


def geo_findings(nodes: list) -> tuple:
    """(business nodes checked, every way their geo departs from the
    constants). A business node with no geo is a departure: the node
    repeats in full on every page, so a missing value is drift."""
    out, n = [], 0
    for node in nodes:
        t = node.get("@type")
        names = {type_name(x) for x in (t if isinstance(t, list) else [t]) if x}
        if not LOCAL_BUSINESS_TYPES.intersection(names):
            continue
        n += 1
        geo = node.get("geo")
        if not isinstance(geo, dict):
            out.append("the business node carries no `geo`")
            continue
        try:
            lat, lon = float(geo.get("latitude")), float(geo.get("longitude"))
        except (TypeError, ValueError):
            out.append(f"`geo` is not two numbers: {geo!r}")
            continue
        if (lat, lon) != (GEO_LAT, GEO_LON):
            out.append(f"`geo` is {lat}, {lon}; the constants say {GEO_LAT}, {GEO_LON}")
    return n, out
HOURS_DAY_RE = re.compile(
    r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)s?\b"
    r"|\b(?:Mon|Tue|Tues|Wed|Thu|Thur|Thurs|Fri|Sat|Sun)\.?\s*(?:-|\u2013|to|thru|through)\s*"
    r"(?:Mon|Tue|Tues|Wed|Thu|Thur|Thurs|Fri|Sat|Sun)\b", re.I)
HOURS_TIME_RE = re.compile(
    r"\b\d{1,2}(?::\d{2})?\s*(?:a\.m\.|p\.m\.|am\b|pm\b)", re.I)


def hours_findings(text: str):
    """(canonical mentions, stray mentions, sunday mentions) in one run of
    visible text. Entities decoded and no-break spaces flattened first, so
    8&nbsp;a.m. and 8 a.m. are the same string."""
    t = " ".join(unescape(text).replace("\u00a0", " ").split())
    spans = [(m.start(), m.end())
             for canon in (HOURS_WEEKDAYS, HOURS_SATURDAY)
             for m in re.finditer(re.escape(canon), t)]
    inside = lambda m: any(a <= m.start() and m.end() <= b for a, b in spans)
    strays, sundays = [], []
    for rx in (HOURS_DAY_RE, HOURS_TIME_RE):
        for m in rx.finditer(t):
            if re.match(r"(?i)sun", m.group(0)):
                continue
            if not inside(m):
                strays.append(t[max(0, m.start() - 30):m.end() + 30].strip())
    for m in re.finditer(r"(?i)\bsundays?\b", t):
        sundays.append(t[max(0, m.start() - 30):m.end() + 30].strip())
    return len(spans), strays, sundays


def hours_schema_findings(nodes: list) -> list:
    """Every way the business node's openingHoursSpecification departs
    from the constants. An absent specification is not a departure; a
    page with no business node is checked elsewhere."""
    out = []
    for node in nodes:
        specs = node.get("openingHoursSpecification")
        if specs is None:
            continue
        specs = specs if isinstance(specs, list) else [specs]
        want = (sorted(HOURS_SCHEMA_DAYS), HOURS_SCHEMA_OPENS, HOURS_SCHEMA_CLOSES)
        got = []
        for sp in specs:
            days = sp.get("dayOfWeek", [])
            days = days if isinstance(days, list) else [days]
            got.append((sorted(str(d).rsplit("/", 1)[-1] for d in days),
                        str(sp.get("opens", "")), str(sp.get("closes", ""))))
        if got != [want]:
            out.append(f"`openingHoursSpecification` says {got}, the constants say {[want]}")
    return out

# THE TRAILING PERIOD IS A VARIANT. "995 Jaymor Rd." is not "995 Jaymor
# Rd", and character-identical has no rounding.
#
# The first version of this pattern ended each alternative with \b, which
# reads as "a word character has to come next." After "Rd." the next
# character on a real page is a comma or a line break, and neither is a
# word character, so the boundary never matched and
# "995 Jaymor Rd., Southampton, PA 18966" sailed through. Worse, it
# scored as a PASS rather than as a silent skip, because the canonical
# string "995 Jaymor Rd" is a PREFIX of the variant: a plain
# `in` test found it inside "995 Jaymor Rd." and reported the address as
# correctly spelled. A check that says PASS on the thing it exists to
# catch is worse than no check.
#
# So both halves are fixed. "Rd\." is self-terminating and needs no
# boundary; "Road" keeps one. And the canonical test is now a regex with
# a lookahead, so "995 Jaymor Rd" only counts when nothing word-like or a
# period follows it.
NAP_STREET_VARIANT_RE = re.compile(
    r"\b(?:995\s+)?Jaymor\s+(?:Road\b|Rd\.)", re.I)
NAP_STREET_CANON_RE = re.compile(re.escape(NAP_STREET_CANON) + r"(?![.\w])")

# --- Staging ------------------------------------------------------------
# THE SITE IS NOINDEXED ON PURPOSE, AND THIS IS THE SWITCH THAT SAYS SO.
#
# The shop's real site is live on WordPress right now. This build is not it.
# A crawlable staging copy is a second address answering for one business,
# which is the harm rule 6 exists to prevent, so until cutover every page
# carries <meta name="robots" content="noindex, nofollow">, docs/robots.txt
# disallows everything, and the canonicals point at the PRODUCTION domain
# from day one so any signal that does leak lands on the real site.
#
# The audit therefore INVERTS its noindex check while this is True. A page
# with noindex passes; a page WITHOUT it fails. Tolerating the exception
# would have been the easy way and the wrong one: the risk during staging is
# not that a page is noindexed, it is that one page quietly is not, and gets
# indexed at a github.io address while the real site is still live. A
# deliberate exception that the build does not enforce is just a comment,
# and comments get violated.
#
# AT CUTOVER, amended 3.94 after the pre-launch sweep's flip simulation
# passed a site that still said "staging" on 37 pages and in llms.txt:
#   1. set this to False;
#   2. run scripts/sync-chrome.py, which takes the noindex tag and the
#      visible banner off every page, because it writes both from this
#      switch (STAGING_ROBOTS_META and STAGING_BANNER below);
#   3. replace docs/robots.txt with an open one that names the sitemap and
#      blocks no AI crawler;
#   4. rewrite docs/llms.txt's staging paragraph (the one carrying
#      LLMS_STAGING_MARK).
# All four move together, in one commit. With this False, a noindex tag, a
# banner, a disallow-all robots.txt or the llms.txt paragraph left behind is
# a CRITICAL, so a half-done flip fails loudly. The page generators
# (build-town.py, migrate-blog.py, migrate-hub.py) read this same switch,
# so a rebuild after cutover cannot re-stage a page. Record the date here
# and in CLAUDE.md when it happens.
STAGING = True

# The two staging fragments every page carries while STAGING is True, held
# here once so scripts/sync-chrome.py and the generators write the same
# bytes the check below reads. The banner's comment names the switch, not
# a date, so it stays true until the day it is deleted.
STAGING_ROBOTS_META = '<meta name="robots" content="noindex, nofollow">'
STAGING_BANNER = (
    '<!-- Removed at cutover, with the noindex tag and the robots.txt disallow.\n'
    '       A human who opens this page should not have to guess why it is not\n'
    '       indexed. -->\n'
    '  <p class="staging">Staging build. Not the live site. The shop\'s live site '
    'is at tricountycollision.com</p>')
STAGING_BANNER_RE = re.compile(r'<p\s+class="staging"', re.I)
# docs/llms.txt's staging paragraph opens with this. Matched case-blind, and
# so is the word "staging" anywhere in llms.txt once the switch is off.
LLMS_STAGING_MARK = "THIS SITE IS NOT LIVE YET"


def staging_robots_meta() -> str:
    """The robots tag a generated page carries: the noindex while staging,
    nothing after cutover."""
    return STAGING_ROBOTS_META if STAGING else ""


def staging_banner() -> str:
    """The visible banner a generated page carries: present while staging,
    nothing after cutover."""
    return STAGING_BANNER if STAGING else ""


# --- The favicon set, 3.94 ----------------------------------------------
# The shop's own site icon, made by scripts/prepare-favicon.py and linked
# from every real page's head by scripts/sync-chrome.py. Each entry is
# (rel, attributes after rel, path under docs/). A page missing one, or a
# file missing from docs/, fails.
ICON_LINKS = (
    ("icon", 'sizes="any"', "favicon.ico"),
    ("icon", 'type="image/png" sizes="192x192"', "assets/img/icon-192.png"),
    ("apple-touch-icon", "", "assets/img/icon-180.png"),
)

# --- The review count, and the day it was counted ---------------------
# A REVIEW COUNT IS THE ONE NUMBER ON THIS SITE THAT ROTS ON ITS OWN. It
# is true on the day it is read and quietly wrong every week after, and
# nothing on the page changes when it goes wrong. So it is recorded here
# with the day it was counted, and the check below enforces both halves.
#
# 274 reviews and 4.9 stars, read off the shop's own GOOGLE BUSINESS
# PROFILE on 2026-09-10 by Greg Quinn of Corcoran Communications, the
# vendor. The standards make the client-owner the fact-checker of record,
# so this is the same deliberate vendor-confirmation exception the NAP
# block carries, recorded as one. OWNER SIGN-OFF IS STILL OUTSTANDING.
#
# It replaces 231 and "Rated Excellent", which came off the live site's
# Trustindex widget on 2026-09-05. THE WIDGET AND THE PROFILE DISAGREED
# BY 43 REVIEWS IN THE SAME WEEK. See proposed-changes.md 4.4.
#
# NO Review OR AggregateRating MARKUP GOES WITH IT, ever. Google's own
# guidelines rule out self-serving review markup on a business's own
# site, and the standards allow no review or rating markup unless the
# data is real and the owner has decided to publish it. This number
# lives in visible text and nowhere else.
REVIEW_COUNT = 274
REVIEW_RATING = "4.9"
REVIEW_COUNTED_ON = "2026-09-10"

# Past this many days the count is old enough that publishing it without
# re-reading the profile is a guess. A WARNING, not a critical: the number
# is not wrong yet, it is just no longer known to be right.
REVIEW_STALE_DAYS = 35

# "274 Google reviews", "based on 274 reviews", "274 reviews". Matched
# against VISIBLE TEXT, after comments and scripts are stripped, so a
# comment recording what the number used to be is history rather than a
# contradiction. The trade is deliberate: a stale number in a comment
# misleads the next person, but failing a build over a changelog line
# would teach everyone to stop writing them.
#
# HARDENED 3.94. The pattern used to allow only "google" between the number
# and "reviews", so "over 231 verified Google reviews" in a migrated post was
# never read, and this check reported the count as agreeing everywhere while
# a stale number and the retired widget's adjective stood on a page. Up to
# three words may now sit between the two, and a "+" after the number is
# read as the number. Measured against the whole site when it was widened:
# it found the post's 231 and no number that is not a review count.
# A year followed by words is not a count ("In 2019 our customers left
# reviews"), so a 19xx or 20xx with words after it is skipped; a bare
# "2019 reviews" still counts. A comma is read only as a thousands
# separator, so "since 2019, reviews" is not a count either.
REVIEW_COUNT_RE = re.compile(
    r"\b(?!(?:19|20)\d\d\s+[A-Za-z]+\s+(?!reviews?\b))"
    r"(\d{1,3}(?:,\d{3})+|\d{1,7})\+?\s+(?:[A-Za-z][\w'’-]*\s+){0,3}?reviews?\b", re.I)

# --- The brand count: the marks, the words and the schema agree -------
# ADDED 2026-09-17, with the brand strip, and it is the review count's
# check in a second key: one shop has one number of brands, and a
# visitor who meets two has no way to tell which is real.
#
# WHAT MADE IT NECESSARY. The live site's own carousel shows FOURTEEN
# marks, the twelve plus RAM and Fiat, while the same site's prose says
# "a dozen". Nobody wrote that discrepancy on purpose; a strip is built
# once in a page builder and the prose is written somewhere else, and
# after that neither knows about the other. This build now states the
# number in FOUR kinds of place at once: the stat band, the prose, the
# FAQ schema, and twelve pictures in a row. That is four places to drift.
#
# SO THE CHECK COUNTS THE PICTURES. It reads the number of marks in the
# strip, every count claimed in visible text, every count claimed inside
# JSON-LD, and this constant, and a disagreement between any two of them
# is a CRITICAL. If the owner confirms RAM and Fiat, the count moves to
# fourteen everywhere in one commit, because anything less fails here.
#
# THE STRIP'S DUPLICATE TRACKS DO NOT COUNT. The marquee ships the marks
# three times so the drift has no seam, and two of those tracks are
# aria-hidden. Counting them would report thirty-six brands, which is
# why the count is taken from the one track a screen reader is offered.
BRAND_COUNT = 12
BRANDS = ("INFINITI", "Nissan", "Hyundai", "Kia", "Acura", "Honda",
          "GM", "Chrysler", "Ford", "Dodge", "Subaru", "Jeep")

# THE SERVICE FAMILY, 3.87, and since 3.90 THE ONE TABLE OF ITS CARDS. Each
# row is (path, label, line): the page, its one name across the site, and
# its one card line. scripts/sync-chrome.py imports it for the nav dropdown
# and the footer, scripts/build-town.py for the What we fix cards, and
# scripts/sync-service-cards.py for home's router text and the five
# Related Services sections. The enumeration check below holds every page
# to it: every grid carries the family (a service page's own grid, the
# family minus itself), and every card carries its row's label and line,
# so a card cannot drift and a service cannot be half-added. The labels are
# the live nav's words, except ADAS Calibration, which the live site never
# had (3.86). "Glass Repair & Replacement" is the one name on every card
# too, Greg's ruling (3.90); "Auto Glass Repair" retired as a label.
# THE LINES ARE THE TOWNS' (3.90, Greg's ruling). The collision line's "a
# lifetime warranty on the work" is the card-length rendering of the hub's
# "on all repair work": the same claim, held to the same owner confirmation
# (proposed-changes.md 4.1). If it is ever normalised, this is the one place.
SERVICES = (
    ("collision-repair/", "Collision Repair",
     "Minor and major collision damage, with a lifetime warranty on the work."),
    ("commercial-collision-repair/", "Commercial Collision Repair",
     "Work vehicles and fleets, with help on the insurance side."),
    ("auto-glass-repair-replacement/", "Glass Repair & Replacement",
     "Windshields, side windows and rear windows."),
    ("paintless-dent-repair/", "Paintless Dent Repair",
     "Door dings and hail dents, fixed without repainting."),
    ("adas-calibration/", "ADAS Calibration",
     "Cameras and sensors re-aimed to factory spec after repairs."),
)
SERVICE_PATHS = tuple(p for p, _l, _ln in SERVICES)
# RELATED SERVICES LEAVES THESE OUT, 3.91, Greg's ruling. A service page's
# Related Services list is the family minus the page itself minus these,
# ONE rule with no special case: on Commercial's own page minus-self already
# removes it, so that page keeps its four siblings and the other four show
# three. Home's router and the towns' grids are untouched: they carry the
# whole family.
RELATED_LEAVES_OUT = ("commercial-collision-repair/",)
COUNT_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")

# A count typed beside "services" ("Four services, one shop", "the four
# services"). It must be the family's own size, spelled as a word.
SERVICE_COUNT_RE = re.compile(r"\b(" + "|".join(COUNT_WORDS[1:]) + r"|\d+)\s+services\b", re.I)

# A BARE-TEXT ENUMERATION: one sentence naming ALL BUT ONE of the family or
# more, in words, with no links for a link-based scan to find. That is the
# half-added shape exactly: a sentence written when the family was one
# smaller. Three of five is NOT the bar, because /blog/'s lead names
# collision repair, dent repair and ADAS calibration among its post TOPICS,
# which is not an enumeration of services (3.87). The business name is
# removed first, because "Tri-County Collision" is not a service.
SERVICE_TEXT_RE = {
    "collision-repair/": re.compile(r"\bcollision (?:repair|work)\b", re.I),
    "commercial-collision-repair/": re.compile(r"\bcommercial\b|\bfleets?\b", re.I),
    "auto-glass-repair-replacement/": re.compile(r"\bauto glass\b|\bglass repair\b|\bwindshields?\b", re.I),
    "paintless-dent-repair/": re.compile(r"\bdent repair\b|\bpaintless\b|\bPDR\b", re.I),
    "adas-calibration/": re.compile(r"\bADAS\b|\bcalibrat\w*", re.I),
}

# "12 vehicle brands", "12+ vehicle brands", "a dozen vehicle brands",
# "Twelve manufacturers". The "+" is READ AS THE NUMBER: "12+" and "12"
# are the same count for agreement purposes, because the claim under it
# is the same claim. Whether the site should say "12" or "12+" at all is
# a claims question and it is in proposed-changes.md 4.1, not here.
BRAND_WORDS = {"ten": 10, "eleven": 11, "twelve": 12, "dozen": 12,
               "thirteen": 13, "fourteen": 14, "fifteen": 15}
BRAND_COUNT_RE = re.compile(
    r"\b(?:(\d{1,3})\s*\+?|(?:a\s+)?(" + "|".join(BRAND_WORDS) + r"))\s+"
    r"(?:vehicle\s+|car\s+|auto\s+|automotive\s+)?"
    r"(?:brands?|manufacturers?|makes?)\b", re.I)

# --- The brand LISTS, 3.94 ------------------------------------------------
# The count check above reads numbers. It could not read a list, and the
# pre-launch sweep found one it had passed: a migrated post saying the shop
# services "Dodge, Ram, Kia, Infiniti, Chrysler, Jeep, GM, Hyundai, Fiat,
# Subaru, Ford, and Nissan", two brands the shop has not confirmed (owner
# question 6b) and two of the twelve missing, beside a site that says twelve.
#
# A BRAND LIST is a run of three or more brand names joined by commas,
# "and", "&" or "/", read in visible text and inside JSON-LD. Matched
# case-blind, so "Infiniti" is INFINITI. Two rules, both CRITICAL:
#
#   1. Every name in a list is one of BRANDS. A name from OTHER_BRANDS is
#      a certification or service claim nobody has confirmed. If the owner
#      confirms one, it moves into BRANDS and the strip in one commit.
#   2. A list naming at least half of BRANDS is an enumeration of the
#      twelve, and must name all of them. A shorter list is examples
#      ("a Honda, Nissan, Ford, or something else") and may name any of
#      them. A long list held short on an OPEN OWNER QUESTION is recorded
#      in BRAND_LISTS_HELD with its question, where the next reader sees
#      it, and is reported as a note instead.
OTHER_BRANDS = ("Toyota", "Lexus", "Scion", "Ram", "Fiat", "Alfa Romeo", "Maserati",
                "Mazda", "Mitsubishi", "BMW", "Mini", "Mercedes-Benz", "Mercedes",
                "Audi", "Volkswagen", "VW", "Porsche", "Volvo", "Tesla", "Genesis",
                "Lincoln", "Mercury", "Chevrolet", "Chevy", "Buick", "Cadillac", "GMC",
                "Land Rover", "Jaguar", "Saturn", "Pontiac", "Rivian", "Polestar",
                "Lucid", "Smart")
_BRAND_TOKEN = "(?:" + "|".join(re.escape(b) for b in sorted(
    set(BRANDS) | set(OTHER_BRANDS), key=len, reverse=True)) + ")"
BRAND_LIST_RE = re.compile(
    r"(?<![\w-])" + _BRAND_TOKEN + r"(?![\w-])"
    r"(?:\s*(?:,\s*(?:and\s+|&\s*)?|\s+and\s+|\s*&\s*|\s*/\s*)"
    r"(?<![\w-])" + _BRAND_TOKEN + r"(?![\w-])){2,}", re.I)
BRAND_LISTS_HELD = {
    "what-do-all-those-lights-mean-in-my-car-understanding-your-vehicles-language/":
        "owner question 28: the live post's 2023 list of eleven, without Subaru "
        "(proposed-changes.md 4.11). Held as migrated until the owner answers.",
}


BRAND_PLUS_RE = re.compile(r"\d\s*\+\s*(?:vehicle\s+|car\s+|auto\s+|automotive\s+)?"
                           r"(?:brands?|manufacturers?|makes?)\b", re.I)

# The one track a screen reader is offered, and the <img> elements in
# it. Deliberately anchored to the class and to the ABSENCE of
# aria-hidden: a fourth duplicate track added later still counts zero,
# and a mark added to the real track counts one.
BRAND_TRACK_RE = re.compile(
    r"<ul[^>]*\bclass=\"[^\"]*\bbrandtrack\b[^\"]*\"(?![^>]*aria-hidden)[^>]*>"
    r"(.*?)</ul>", re.S | re.I)
JSONLD_RE = re.compile(
    r"(?is)<script[^>]+type=\"application/ld\+json\"[^>]*>(.*?)</script>")

# --- Asset provenance: no AI-generated image enters this repo ----------
# ADDED 2026-09-17, after two candidate assets for the We Fix It All
# render were both caught by reading their metadata.
#
# The standards say real photos only, no stock and no AI-generated
# imagery, and the reason is the firm's own argument: a site that tells
# clients real beats stock has to live by it. That rule had no
# mechanism, so it was a rule that depended on somebody remembering to
# look. Twice in one afternoon the thing that caught an AI asset was a
# person deciding to check, which is exactly the shape of rule that
# rule 8 says gets violated.
#
# WHAT THE TWO CANDIDATES CARRIED, both licensed from Adobe Stock and
# both rejected on the client's ruling:
#
#   AdobeStock_1060063701  IPTC DigitalSourceType = trainedAlgorithmicMedia
#   AdobeStock_746591791   xmp:CreatorTool = "OkiDokiBot AI Art Generator"
#
# Two different tells in two different tags, which is why this reads
# both and does not trust either one alone. The first is Adobe's own
# C2PA label, the standard IPTC code for "a generative model made these
# pixels". The second carries no DigitalSourceType at all and names the
# generator in the tool field instead.
#
# THE LIMIT, AND IT IS A REAL ONE. This reads labels. It cannot read
# pixels, so it cannot catch an AI asset whose metadata was stripped,
# and stripping is one command. The check is a floor and not a
# guarantee: it makes the labelled case impossible to ship by accident,
# and the unlabelled case stays a human judgement at purchase time. A
# report that says "no AI marker" is saying the file makes no such
# claim, not that a person made it.
#
# WHAT IS DELIBERATELY NOT A FAIL. digitalCapture is a camera.
# digitalArt and algorithmicMedia are a person at a workstation, which
# is what a real 3D ghosted render is, and failing those would ban the
# asset this check was written to let through.
AI_SOURCE_TYPES = (
    "trainedalgorithmicmedia",
    "compositewithtrainedalgorithmicmedia",
)

# Generator names and phrases that mean the same thing when they turn up
# in a tool field. Deliberately specific: "firefly" alone is a typeface
# and a product name, so it is spelled "adobe firefly", and bare "ai" is
# not here at all because it matches half the software on earth.
AI_TOOL_RE = re.compile(
    r"midjourney|stable\s?diffusion|dall[·.\-\s]?e\b|adobe firefly"
    r"|okidokibot|leonardo\.ai|ideogram|nightcafe|craiyon|starryai"
    r"|ai (?:art|image) generator|text[-\s]to[-\s]image"
    r"|generative (?:fill|expand)|ai[-\s]generated",
    re.I)

# Where the tells live. Both tags appear as an element or as an
# attribute depending on how the XMP was written, so both spellings are
# matched rather than assumed.
SOURCE_TYPE_RE = re.compile(
    r"DigitalSourceType\s*[>=]\s*[\"']?\s*"
    r"(?:http://cv\.iptc\.org/newscodes/digitalsourcetype/)?([A-Za-z]+)")
CREATOR_TOOL_RE = re.compile(r"CreatorTool\s*[>=]\s*[\"']?([^<\"'\r\n]{1,120})")

# Raster formats only. An .svg under docs/ is our own drawing, in the
# repo as text, and it is reviewed as code rather than as an asset.
ASSET_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif")

# --- The convention that keeps comments from rotting ------------------
# COMMENTS NEVER CARRY THE LITERAL REVIEW COUNT OR THE STAT ORDER. They
# name `REVIEW_COUNT` and "the band's DOM order" instead.
#
# WHY THERE IS A CONVENTION AT ALL. The check above strips comments
# before reading review counts, deliberately, so that a comment
# recording history is not read as the page contradicting itself. The
# cost of that choice showed up on 2026-09-10: the stat band's own
# comment had been carrying a stale count AND a stale order through two
# commits, and nothing could have caught it, because the one mechanism
# that reads counts is the one that had been told to look away.
#
# So the convention removes the thing that rots, and this check watches
# for it coming back. A comment that says `REVIEW_COUNT` stays true
# when the number changes; a comment that says the number does not.
#
# THE CONVENTION AND THE CHECK FIT EACH OTHER BY CONSTRUCTION: `\breview\b`
# cannot match inside `REVIEW_COUNT`, because the character after
# "REVIEW" is an underscore and an underscore is a word character. The
# approved way of writing it is exactly the way this pattern cannot fire
# on, which is what makes the rule easy to keep rather than easy to
# resent.
#
# WARN-LEVEL, AND STRUCTURALLY INCAPABLE OF FAILING: the function is not
# handed a `fails` list. A rotting comment misleads the next reader and
# costs nothing to a visitor, so it should never stop a build. It is
# also the kind of thing that turns into a false positive on somebody's
# perfectly reasonable prose, and a false positive that fails a build
# gets the check deleted rather than fixed.
HTML_COMMENT_RE = re.compile(r"(?s)<!--(.*?)-->")

# "a few words" is three. Two to four digits, because a one-digit number
# beside "review" is prose ("a 5 star review") and five digits is not a
# count this shop will have in this decade.
_NEARBY_WORDS = r"(?:[\w'\u2019()\-.,:;/]+ ){0,3}"
COMMENT_REVIEW_NUM_RE = re.compile(
    r"\b\d{2,4}\b " + _NEARBY_WORDS + r"reviews?\b"
    r"|\breviews?\b " + _NEARBY_WORDS + r"\d{2,4}\b", re.I)

# --- Links that are waiting on a page that does not exist yet ---------
# THE SITE NEVER WRITES A LINK TO A PAGE THAT HAS NOT BEEN BUILT. That
# rule is enforced: a relative href with no file behind it fails the
# build. The cost of enforcing it is a set of elements that SHOULD be
# links and are not yet: the logo, the breadcrumb's "Home", the
# online-estimate phrases, the paintless dent repair mention, the blog
# post in FAQ 5.
#
# Waiting was the unmechanized part. Nothing recorded what each one was
# waiting for, and nothing would notice the day the wait ended, so the
# failure mode is a page that ships built and unlinked with a span
# sitting where its link should be.
#
# So each carries data-pending-href with the URL it becomes. The test
# then cuts BOTH ways: a real href to a missing file fails, and a
# pending href to a file that now EXISTS fails until it is converted.
# The second direction is the one that was missing.
PENDING_HREF_RE = re.compile(r'data-pending-href="([^"]+)"')

# The site's own base URL, used to work out what URL a local file will
# serve at. That is how the two checks below know whether a page is in
# sitemap.xml under its OWN address rather than under some other page's.
SITE_BASE = "https://tricountycollision.com/"

# A sitemap is not always a list of pages. It may be a <sitemapindex>,
# a list of OTHER sitemaps, which is what WordPress and Yoast ship by
# default. We follow an index into its children, with two caps so a
# malformed or looping sitemap cannot spin a scan forever: how deep the
# nesting may go, and how many sitemap files one run will fetch at all.
SITEMAP_MAX_DEPTH = 3
SITEMAP_MAX_FILES = 50

# --- LocalBusiness and everything that IS one -------------------------
# The "is this a local business page" check used to hold a hand-written
# list of about twenty types, which meant every schema.org subtype
# nobody had thought to type out was reported as having no
# LocalBusiness schema at all. A real prospect's site was flagged on
# every page for exactly this: it publishes a complete AutoBodyShop
# node, address, telephone, geo and hours included, and AutoBodyShop is
# a LocalBusiness subtype the list happened to omit. The finding was
# false, and it was the kind of false that a prospect can check in a
# minute.
#
# So this is the full set: LocalBusiness plus every class under it in
# the schema.org vocabulary, all 130 of them, derived from
# schemaorg-current-https.jsonld (schema.org v29, read 2026-08-28) by
# walking rdfs:subClassOf down from schema:LocalBusiness. None of them
# is superseded. It is baked in as a literal rather than fetched so the
# audit still runs with no network, which is how it runs against our
# own pages. To refresh it after a schema.org release, walk the
# vocabulary again; do not add names by hand, which is the habit that
# produced the short list.
LOCAL_BUSINESS_TYPES = frozenset({
    "LocalBusiness", "AccountingService", "AdultEntertainment",
    "AmusementPark", "AnimalShelter", "ArchiveOrganization",
    "ArtGallery", "Attorney", "AutoBodyShop", "AutoDealer",
    "AutoPartsStore", "AutoRental", "AutoRepair", "AutoWash",
    "AutomatedTeller", "AutomotiveBusiness", "Bakery",
    "BankOrCreditUnion", "BarOrPub", "BeautySalon", "BedAndBreakfast",
    "BikeStore", "BookStore", "BowlingAlley", "Brewery",
    "CafeOrCoffeeShop", "Campground", "Casino", "ChildCare",
    "ClothingStore", "ComedyClub", "ComputerStore", "ConvenienceStore",
    "CovidTestingFacility", "DaySpa", "Dentist", "DepartmentStore",
    "Distillery", "DryCleaningOrLaundry", "Electrician",
    "ElectronicsStore", "EmergencyService", "EmploymentAgency",
    "EntertainmentBusiness", "ExerciseGym", "FastFoodRestaurant",
    "FinancialService", "FireStation", "Florist", "FoodEstablishment",
    "FurnitureStore", "GardenStore", "GasStation", "GeneralContractor",
    "GolfCourse", "GovernmentOffice", "GroceryStore", "HVACBusiness",
    "HairSalon", "HardwareStore", "HealthAndBeautyBusiness",
    "HealthClub", "HobbyShop", "HomeAndConstructionBusiness",
    "HomeGoodsStore", "Hospital", "Hostel", "Hotel", "HousePainter",
    "IceCreamShop", "IndividualPhysician", "InsuranceAgency",
    "InternetCafe", "JewelryStore", "LegalService", "Library",
    "LiquorStore", "Locksmith", "LodgingBusiness", "MedicalBusiness",
    "MedicalClinic", "MensClothingStore", "MobilePhoneStore", "Motel",
    "MotorcycleDealer", "MotorcycleRepair", "MovieRentalStore",
    "MovieTheater", "MovingCompany", "MusicStore", "NailSalon",
    "NightClub", "Notary", "OfficeEquipmentStore", "Optician",
    "OutletStore", "PawnShop", "PetStore", "Pharmacy", "Physician",
    "PhysiciansOffice", "Plumber", "PoliceStation", "PostOffice",
    "ProfessionalService", "PublicSwimmingPool", "RadioStation",
    "RealEstateAgent", "RecyclingCenter", "Resort", "Restaurant",
    "RoofingContractor", "SelfStorage", "ShoeStore", "ShoppingCenter",
    "SkiResort", "SportingGoodsStore", "SportsActivityLocation",
    "SportsClub", "StadiumOrArena", "Store", "TattooParlor",
    "TelevisionStation", "TennisComplex", "TireShop",
    "TouristInformationCenter", "ToyStore", "TravelAgency",
    "VacationRental", "WholesaleStore", "Winery"
})

# A @type may be written as a bare name, a full URL, or a compact IRI
# ("AutoBodyShop", "https://schema.org/AutoBodyShop", "schema:AutoBodyShop").
# All three are valid JSON-LD and all three appear in the wild, so the
# name is normalized before anything is matched against it. Without
# this, a page using the URL form reads as having no recognized type at
# all, which would fail the FAQPage check the same way.
TYPE_NAME_RE = re.compile(r"^(?:https?://(?:www\.)?schema\.org/|schema:)")


def type_name(raw) -> str:
    """The bare schema.org class name from any of its written forms."""
    if not isinstance(raw, str):
        return ""
    return TYPE_NAME_RE.sub("", raw.strip()).strip("/")


# --- Pages that are not pages -----------------------------------------
# Two kinds of file under docs/ exist for machines rather than readers: a
# redirect stub standing at an old WordPress URL, and the 404 page. Both
# would fail the page rubric for things that are deliberate. A stub has
# no FAQ, no schema and forty words; the 404 page has no canonical,
# because a canonical on an error page would claim the URL is the real
# version of something. Above all, neither belongs in sitemap.xml, and
# "not listed in sitemap.xml" is a critical for a real page.
#
# So each declares itself in the head and gets a short rubric of its own:
#   <meta name="tri-county-page" content="redirect-stub">
#   <meta name="tri-county-page" content="error-404">
# They still score through the same formula and still appear in the
# table, so a malformed stub drops off 100/100 and fails --strict exactly
# like anything else. What changes is WHICH checks apply.
SPECIAL_KINDS = ("redirect-stub", "error-404")

# --- Execution pages: the full rubric, minus checks NAMED per kind ------
# RULED BY GREG 2026-09-24, proposed-changes.md 3.53. EXECUTION PAGES
# MEASURE DIFFERENTLY. Two checks below measure a page whose job is to
# persuade and to answer: the FAQPage check and the 300-word thin-content
# check. /contact-us/ does neither. Its job is to put every way of
# reaching the shop within one tap and the call inside the first screen,
# and the fold probe is what measures that. A check that forced 300 words
# of filler or an invented FAQ onto it would be the check designing the
# page. The check serves the page, never the reverse.
#
# WHY NOT LET IT SCORE 83 AND RECORD IT: a permanent sub-bar score teaches
# the Monday reader to skim past warnings, and the report is worth paying
# for only while a warning means something.
#
# THE LIMITS ARE THE PERMISSION:
#   - A page opts in by declaring it in its own head, where the next
#     reader sees it: <meta name="tri-county-page" content="contact">.
#   - A kind is exempt from exactly the checks listed against it, by
#     name, and from nothing else. Every other check runs as usual, and
#     the page still counts as a page in the report.
#   - KINDS ARE PER-KIND AND EXPLICIT. A new page that trips its own
#     rubric mismatch (privacy is the expected next one) declares ITS OWN
#     kind with its own recorded scope. There is never a blanket pass,
#     and never one for "utility".
#   - An exempt check still reports, as a note naming the exemption, so
#     the report says what was not measured rather than going quiet.
# scripts/test-audit-checks.py holds both directions: a contact-kind page
# still fails what it should, and an undeclared page gets no exemption.
#
# THE BLOG'S TWO KINDS, RULED BY GREG 2026-09-25, proposed-changes.md 3.57.
# A POST IS A READ AND AN INDEX ROUTES: neither page type answers questions,
# so neither is measured for an answer block. Each is exempt from
# faq-schema and NOTHING ELSE. Thin-content stays live on both, on purpose:
# a post under 300 words SHOULD warn, because a thin post is a real
# editorial problem in a way a missing FAQ is not.
#
# THE EXEMPTION MEANS NOT REQUIRED, NEVER UNMEASURED. It applies only to a
# page that shows NO visible FAQ. A post that carries one (an FAQ-rich post
# is a real AEO play) is measured like every other page: no schema warns,
# and the mirror law fails any difference between the visible text and the
# FAQPage node, both directions. That holds for contact too.
#
# A TOWN PAGE IS DECLARED AND EXEMPT FROM NOTHING, Greg's ruling of
# 2026-09-28, proposed-changes.md 3.62. It carries a real FAQ and has to
# earn its words, so faq-schema and thin-content both stay measured. The
# empty tuple is written out rather than left to the .get() default, so the
# kind is a ruled entry like the others and a later edit that adds an
# exemption to it is a visible change to a ruled list, not a new key.
# The tier's own gate is check_town_variance_local, further down.
RUBRIC_EXEMPTIONS = {
    "contact": ("faq-schema", "thin-content"),
    "post": ("faq-schema",),
    "blog-index": ("faq-schema",),
    "town": (),
    # 3.79: the areas hub. It carries FAQs and its own long copy, so it
    # earns no exemption; declared so the hub routing check reads it.
    "hub": (),
}

REFRESH_RE = re.compile(
    r"""<meta[^>]+http-equiv=["']refresh["'][^>]*content=["']\s*\d+\s*;\s*url=([^"']+)["']""",
    re.I)

# --- Cache-busting stamps ---------------------------------------------
# docs/assets/site.css and site.js are referenced as
# `assets/site.css?v=<first 8 hex of the file's SHA-256>`, written by
# scripts/stamp-assets.py. GitHub Pages serves both with
# `cache-control: max-age=600`, so without the stamp a ten-minute-old
# browser cache hands back the OLD stylesheet, which during the build
# twice looked exactly like a CSS bug and got chased as one.
#
# The stamper is a command someone has to run. This check is what makes
# forgetting to run it impossible: a stale or missing stamp is a critical
# against the page, same as a missing sitemap entry.
STAMPED_ASSETS = ("assets/site.css", "assets/site.js")
STAMP_RE = {
    a: re.compile(r'(?:href|src)="(?:\{\{ROOT\}\}|/|(?:\.\./)*)'
                  + re.escape(a) + r'(\?v=([0-9a-f]+))?"')
    for a in STAMPED_ASSETS
}


def current_stamps() -> dict:
    """First 8 hex of each stamped asset's SHA-256. Empty dict if they
    cannot be read, which is the case on a live-URL run, and the check
    then does nothing rather than guessing."""
    out = {}
    for a in STAMPED_ASSETS:
        try:
            with open(os.path.join(SITE_DIR, a), "rb") as f:
                out[a] = hashlib.sha256(f.read()).hexdigest()[:8]
        except OSError:
            return {}
    return out


def page_url(source: str) -> str:
    """The absolute URL a local file will serve at, so a page can be
    looked up in the sitemap under its own address."""
    rel = os.path.relpath(source, SITE_DIR).replace(os.sep, "/")
    if rel == "index.html":
        rel = ""
    elif rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    return SITE_BASE + rel


def check_asset_stamps(html: str, stamps: dict, passes: list, fails: list):
    """Every page that links the shared stylesheet or script must carry
    the CURRENT stamp for it."""
    if not stamps:
        return
    for asset, rx in STAMP_RE.items():
        m = rx.search(html)
        if not m:
            continue                      # this page does not use it
        want = stamps[asset]
        if m.group(2) == want:
            passes.append(f"`{asset}` carries the current cache-busting stamp `?v={want}`.")
        elif m.group(1) is None:
            fails.append(
                f"**`{asset}` is referenced with no `?v=` stamp.** GitHub Pages serves it with "
                f"`max-age=600`, so a browser can hand back a ten-minute-old copy and make a "
                f"shipped change look broken. Run `python3 scripts/stamp-assets.py`.")
        else:
            fails.append(
                f"**`{asset}` carries a stale stamp** (`?v={m.group(2)}`, the file is now "
                f"`?v={want}`). The page will serve a cached older copy of the file. Run "
                f"`python3 scripts/stamp-assets.py`.")


def special_audit(source: str, html: str, p, kind: str, coverage: dict):
    """The short rubric for a redirect stub or the 404 page.

    Both are scored on what they are actually FOR, and both are checked
    for the thing that matters most about them: that they stayed out of
    sitemap.xml. Neither is checked against llms.txt, which lists pages a
    reader or an assistant would want, and these are not that."""
    passes, warns, fails, notes = [], [], [], []
    own = page_url(source)
    listed = coverage is not None and own in coverage["sitemap_locs"]

    if kind == "redirect-stub":
        sp, sw, sf = staging_page_findings(html, is_stub=True)
        passes += sp
        warns += sw
        fails += sf
        canon = (p.canonical or "").strip()
        if canon.startswith(SITE_BASE):
            passes.append(f"Canonical points at the new page: {canon}")
        else:
            fails.append(
                f"**A redirect stub needs an absolute `rel=canonical` at its target.** "
                f"Found: {canon or 'nothing'}. That tag is what passes the old URL's ranking "
                f"signal to the page that replaced it.")

        m = REFRESH_RE.search(html)
        if not m:
            fails.append(
                "**No `<meta http-equiv=\"refresh\">`.** GitHub Pages cannot issue a real 301, "
                "so the meta refresh is what actually moves a reader. Without it this file is a "
                "dead end with a canonical on it.")
        else:
            raw = m.group(1).strip()
            # Fragments are compared away: the canonical deliberately
            # carries none (Google strips them anyway) while the refresh
            # target keeps its anchor so the reader lands in the right
            # section. Same page, two jobs.
            target = urljoin(own, raw).split("#")[0]
            if target == canon.split("#")[0]:
                passes.append(f"Meta refresh and canonical agree on the destination: {target}")
            else:
                fails.append(
                    f"**The meta refresh and the canonical disagree.** The refresh sends readers "
                    f"to {target} and the canonical sends crawlers to {canon.split('#')[0]}. "
                    f"Pick one destination and use it in both.")
            if re.search(r"<a[^>]+href=\"" + re.escape(raw) + r"\"", html):
                passes.append("A real link to the destination is on the page, for anyone the "
                              "refresh and the script both miss.")
            else:
                warns.append(
                    f"**No visible link to {raw}.** If the refresh is blocked and JavaScript is "
                    f"off, the reader is stranded. Add one sentence with a real link.")
    else:
        t = p.title.strip()
        if not t:
            fails.append("**Missing <title> tag.** The error page is a page a reader lands on; "
                         "give it a name.")
        elif len(t) > 60:
            warns.append(f"**Title is {len(t)} characters** (aim for \u226460): \u201c{t}\u201d")
        else:
            passes.append(f"Title tag present and a good length ({len(t)} chars): \u201c{t}\u201d")

        d = p.meta.get("description", "").strip()
        if not d:
            fails.append("**Missing meta description.**")
        elif len(d) > 160:
            warns.append(f"**Meta description is {len(d)} characters** (aim for \u2264160).")
        else:
            passes.append(f"Meta description present and a good length ({len(d)} chars).")

        h1s = [h.strip() for h in p.h1s if h.strip()]
        if len(h1s) != 1:
            fails.append(f"**{len(h1s)} H1 headings found.** The error page needs exactly one.")
        else:
            passes.append(f"Exactly one H1: \u201c{h1s[0][:80]}\u201d")

        if p.has_viewport:
            passes.append("Mobile viewport tag present.")
        else:
            fails.append("**No viewport meta tag.**")

        missing_alt = [src for src, alt in p.images if alt is None or not alt.strip()]
        if p.images and missing_alt:
            fails.append(f"**{len(missing_alt)} of {len(p.images)} images missing alt text.**")
        elif p.images:
            passes.append(f"All {len(p.images)} images have alt text.")

        check_asset_stamps(html, current_stamps(), passes, fails)

        notes.append("Scored as the error page, not as a page: no canonical is expected on it "
                     "(one would claim this URL is the real version of something), and it is "
                     "deliberately absent from sitemap.xml and llms.txt.")

    if coverage is None:
        pass
    elif listed:
        fails.append(
            f"**Listed in `docs/sitemap.xml` at {own}, and it must not be.** A "
            + ("redirect stub is not a page; listing it asks Google to index a file whose only "
               "job is to point at another one."
               if kind == "redirect-stub" else
               "sitemap is a list of pages worth visiting, and an error page is not one.")
            + " Remove its `<url>` block.")
    else:
        passes.append(f"Correctly absent from `docs/sitemap.xml`: {own}")

    if kind == "redirect-stub":
        notes.append("Scored as a redirect stub, not as a page: no schema, no FAQ, no word count "
                     "and no llms.txt entry are expected on it.")
    return passes, warns, fails, notes




# THE EMPTY-HEADING CHECK, 2026-09-28, proposed-changes.md 3.60. A heading
# with no words is announced by a screen reader as a heading with no name,
# and it is invisible by eye, which is how a WordPress leftover, an empty
# <h2> closing a migrated post, shipped in 3.58 and was found only by a
# layout probe in 3.59. A CRITICAL, on Greg's ruling of 2026-09-28: nobody
# means to ship one. "Empty" is text content that is nothing but
# whitespace, no-break spaces included, which is what a reader hears.
HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")


class PageParser(HTMLParser):
    """Walks the HTML and collects everything the audit needs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        # An inline <svg> may carry its own <title>, which names the graphic,
        # not the page. Without this depth count its text was appended to the
        # page title, so an inline map would have silently lengthened the
        # measured title. Found while building /contact-us/'s map, 3.54.
        self._svg_depth = 0
        self._in_jsonld = False
        self.meta = {}            # name/property -> content
        self.h1s = []
        self._in_h1 = False
        self.jsonld_blocks = []
        self.images = []          # list of (src, alt-or-None)
        self.links_internal = 0
        self.links_external = 0
        self.canonical = None
        self.has_viewport = False
        self.contacts_linked = 0  # phone/email mentions inside tel:/mailto:
        self.contacts_bare = []   # (line, kind) for the ones that are not
        self._href_stack = []     # open <a> hrefs, innermost last
        self._skip_depth = 0      # inside <script>/<style>
        # Visible FAQ items, as (question, answer) of rendered text. The
        # house rule is that each one is byte-identical to its schema
        # twin, so this collects what a reader sees and the FAQ mirror
        # check compares it against the FAQPage node.
        self.faq_visible = []
        self._details_depth = 0
        self._in_summary = False
        self._in_faq_answer = False
        self._faq_q = None
        self._faq_a = None
        self._skip_faq_ico = 0    # the chevron <span>, art with no words
        # Every h1 to h6 as (tag, line, text), for the empty-heading check.
        # A stack rather than a flag, so a heading's text is its own even
        # if markup ever nests one inside another by mistake.
        self.headings = []
        self._heading_stack = []
        # The visible breadcrumb, as the rendered text of each <li> of the
        # first <nav> whose class names a crumb, for the crumb mirror
        # check (3.76). None when the page has no such nav; an empty list
        # when it has one this parser cannot read as a list.
        self.crumb_visible = None
        self._crumb_nav = 0       # depth inside the crumb nav, 0 outside
        self._crumb_done = False  # only the first crumb nav is read
        self._crumb_li = None     # the open item's text, or None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip_depth += 1
        if tag == "svg":
            self._svg_depth += 1
        if tag in HEADING_TAGS:
            self._heading_stack.append([tag, self.getpos()[0], ""])
        if tag == "nav":
            if self._crumb_nav:
                self._crumb_nav += 1
            elif not self._crumb_done and "crumb" in (a.get("class") or "").split():
                self._crumb_nav = 1
                self.crumb_visible = []
        if tag == "li" and self._crumb_nav:
            self._crumb_li = ""
        if tag == "title" and not self._svg_depth:
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
            self.h1s.append("")
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key.lower()] = a.get("content", "")
            if (a.get("name") or "").lower() == "viewport":
                self.has_viewport = True
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld = True
            self.jsonld_blocks.append("")
        elif tag == "img":
            self.images.append((a.get("src", ""), a.get("alt")))
        elif tag == "details":
            self._details_depth += 1
            self._faq_q, self._faq_a = None, None
        elif tag == "summary" and self._details_depth:
            self._in_summary = True
            self._faq_q = ""
        elif tag == "span" and self._in_summary and "faq-ico" in (a.get("class") or ""):
            self._skip_faq_ico += 1
        elif tag == "p" and self._details_depth and self._faq_a is None:
            self._in_faq_answer = True
            self._faq_a = ""
        elif tag == "a":
            href = a.get("href", "")
            self._href_stack.append(href)
            if href.startswith("http"):
                self.links_external += 1
            elif href and not href.startswith(("#", "mailto:", "tel:")):
                self.links_internal += 1

    def handle_endtag(self, tag):
        if tag == "li" and self._crumb_nav and self._crumb_li is not None:
            self.crumb_visible.append(" ".join(self._crumb_li.split()))
            self._crumb_li = None
        if tag == "nav" and self._crumb_nav:
            self._crumb_nav -= 1
            if not self._crumb_nav:
                self._crumb_done = True
        if tag in HEADING_TAGS and self._heading_stack and self._heading_stack[-1][0] == tag:
            self.headings.append(tuple(self._heading_stack.pop()))
        if tag == "svg" and self._svg_depth:
            self._svg_depth -= 1
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "summary":
            self._in_summary = False
        elif tag == "span" and self._skip_faq_ico:
            self._skip_faq_ico -= 1
        elif tag == "p" and self._in_faq_answer:
            self._in_faq_answer = False
        elif tag == "details":
            if self._details_depth:
                self._details_depth -= 1
            if self._faq_q is not None:
                self.faq_visible.append((self._faq_q.strip(), (self._faq_a or "").strip()))
            self._faq_q, self._faq_a = None, None
        elif tag == "a":
            if self._href_stack:
                self._href_stack.pop()
        elif tag == "script":
            self._in_jsonld = False
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1 and self.h1s:
            self.h1s[-1] += data
        if self._in_jsonld and self.jsonld_blocks:
            self.jsonld_blocks[-1] += data
        if self._in_summary and not self._skip_faq_ico and self._faq_q is not None:
            self._faq_q += data
        if self._in_faq_answer and self._faq_a is not None:
            self._faq_a += data
        if self._skip_depth:
            return
        if self._crumb_li is not None and not self._svg_depth:
            self._crumb_li += data
        for h in self._heading_stack:
            h[2] += data
        if not NAP_CONTACT_RES:
            return
        linked = any(h.startswith(("tel:", "mailto:")) for h in self._href_stack)
        for kind, rx in NAP_CONTACT_RES:
            for _ in rx.finditer(data):
                if linked:
                    self.contacts_linked += 1
                else:
                    self.contacts_bare.append((self.getpos()[0], kind))


def load(source: str) -> str:
    if source.startswith(("http://", "https://")):
        req = urllib.request.Request(source, headers={"User-Agent": "SEO-Audit-Agent/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    with open(source, encoding="utf-8") as f:
        return f.read()


def is_url(source: str) -> bool:
    return source.startswith(("http://", "https://"))


def check_ai_access(base_url: str, warns: list, passes: list, notes: list):
    """AEO checks that only make sense against a LIVE site:
    is the site letting AI assistants' crawlers in, and does it offer
    an llms.txt guide for AI agents?

    These are properties of the SITE, not of any one page, so they run
    once per run and are reported in their own section. Running them per
    page would just refetch the same two files five more times."""
    parts = urlparse(base_url)
    root = f"{parts.scheme}://{parts.netloc}"

    # --- robots.txt: are AI crawlers blocked? ---
    # If these bots are blocked, the business is invisible to the AI
    # assistants a growing share of customers ask for recommendations.
    ai_bots = ["GPTBot", "OAI-SearchBot", "ClaudeBot", "anthropic-ai",
               "PerplexityBot", "Google-Extended"]
    try:
        robots = load(root + "/robots.txt")
        blocked = []
        current_agents = []
        for line in robots.splitlines():
            line = line.split("#")[0].strip()
            if line.lower().startswith("user-agent:"):
                current_agents.append(line.split(":", 1)[1].strip())
            elif line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path == "/":
                    for agent in current_agents:
                        for bot in ai_bots:
                            if bot.lower() == agent.lower():
                                blocked.append(bot)
            elif not line:
                current_agents = []
        if blocked:
            warns.append(f"**robots.txt blocks AI crawlers: {', '.join(sorted(set(blocked)))}.** "
                         "Blocked bots can't read the site, so AI assistants are less likely to "
                         "recommend this business. Unblock them unless the client explicitly wants out.")
        else:
            passes.append("AEO: robots.txt does not block the major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.).")
    except Exception:
        notes.append("Could not fetch robots.txt. If the site truly has none, crawlers default to full access (fine), but add one to be explicit.")

    # --- llms.txt: a curated guide for AI agents ---
    # Honest status (2026): Google says it ignores llms.txt, but Anthropic
    # recommends it, OpenAI publishes them, and Perplexity has been seen
    # reading them. It costs 20 minutes: cheap insurance, not a magic bullet.
    try:
        llms = load(root + "/llms.txt")
        if llms.strip():
            passes.append("AEO: llms.txt present, so AI agents get a curated guide to the business.")
    except Exception:
        notes.append("No llms.txt found. Optional (Google ignores it) but Anthropic/OpenAI agent "
                     "tooling reads it: a 20-minute add for extra AI visibility.")


def check_staging_local(passes: list, warns: list, notes: list, fails: list = None,
                        root: str = None):
    """The half of the staging exception that is a property of the SITE
    rather than of any page: docs/robots.txt and docs/llms.txt. The per-page
    half (the noindex tag and the visible banner) is in staging_page_findings.

    BOTH DIRECTIONS, 3.94. While STAGING is True, robots.txt must disallow
    everything and llms.txt must say the site is not live. Once it is False,
    either one left behind is a CRITICAL: the pre-launch sweep simulated the
    flip and this check passed a site whose llms.txt still told assistants
    to read the old WordPress site, because it only ever looked one way.

    SITE_DIR is resolved when this is CALLED, so the tests can point it at a
    temporary directory."""
    fails = fails if fails is not None else warns
    root = root or SITE_DIR
    path = os.path.join(root, "robots.txt")
    try:
        with open(path, encoding="utf-8") as f:
            body = "\n".join(line.split("#")[0] for line in f.read().splitlines())
    except OSError:
        body = None
        (warns if STAGING else notes).append(
            f"**No `{path}`.** While the build is staging this file is what stops a crawler "
            f"fetching the pages at all; the meta tags are the second line, not the first.")
    if body is not None:
        blocks_all = re.search(r"(?im)^\s*disallow:\s*/\s*$", body) is not None
        if STAGING and blocks_all:
            passes.append("`docs/robots.txt` disallows everything, which is correct while the "
                          "shop's real site is still live. It comes off at cutover, together with "
                          "the pages' noindex tags.")
        elif STAGING:
            warns.append("**`docs/robots.txt` does not disallow everything and the build is still "
                         "staging.** The pages are noindexed but nothing is stopping a crawler "
                         "reading them. Add `Disallow: /` under `User-agent: *`.")
        elif blocks_all:
            fails.append("**`docs/robots.txt` still disallows everything and `STAGING` is off.** "
                         "The site is live and invisible. This is the staging file; replace it with "
                         "the open one that names the sitemap and blocks no AI crawler.")
        elif not re.search(r"(?im)^\s*sitemap:\s*https://tricountycollision\.com/sitemap\.xml\s*$",
                           body):
            warns.append("**`docs/robots.txt` is open but does not name the sitemap.** Add "
                         "`Sitemap: https://tricountycollision.com/sitemap.xml`.")
        else:
            passes.append("`docs/robots.txt` is open and names the sitemap, so crawlers and AI "
                          "agents can read the site.")

    lpath = os.path.join(root, "llms.txt")
    try:
        with open(lpath, encoding="utf-8") as f:
            llms = f.read()
    except OSError:
        return
    marked = LLMS_STAGING_MARK.lower() in llms.lower()
    if STAGING and marked:
        passes.append("`docs/llms.txt` tells assistants this build is not live yet, which is "
                      "true until cutover.")
    elif STAGING:
        warns.append(f"**`docs/llms.txt` has lost its staging paragraph** (\"{LLMS_STAGING_MARK}\") "
                     "while the build is still staging. An assistant reading it would take this "
                     "build for the shop's live site.")
    elif marked or re.search(r"\bstaging\b", llms, re.I):
        fails.append("**`docs/llms.txt` still carries staging language and `STAGING` is off.** "
                     "It tells every assistant that reads it that this site is not the shop's "
                     "live site. Rewrite the staging paragraph as part of the cutover commit.")
    else:
        passes.append("`docs/llms.txt` carries no staging language.")


def staging_page_findings(html_text: str, is_stub: bool = False) -> tuple:
    """(passes, warns, fails) for one page's visible staging banner and, on
    a redirect stub, its noindex tag. A real page's noindex is scored in
    audit() itself, which has always run both ways.

    While STAGING is True a real page MISSING the banner warns: a human who
    opens a noindexed page should be told why. Once it is False, a banner is
    a CRITICAL, and so is a noindex left on a stub. Comments are stripped
    first, so a comment that mentions the banner is not the banner."""
    passes, warns, fails = [], [], []
    bare = re.sub(r"(?s)<!--.*?-->", " ", html_text)
    has_banner = STAGING_BANNER_RE.search(bare) is not None
    if is_stub:
        noindex = re.search(r'<meta\s+name="robots"[^>]*noindex', bare, re.I) is not None
        if not STAGING and noindex:
            fails.append("**This redirect stub is still noindexed and `STAGING` is off.** The "
                         "stub's noindex comes off with every page's at cutover. Run "
                         "`scripts/sync-chrome.py`.")
        if has_banner:
            fails.append("**A redirect stub carries the staging banner.** A stub stays bare.")
        return passes, warns, fails
    if STAGING and has_banner:
        passes.append("Carries the visible staging banner, so a human who opens it knows why "
                      "it is not indexed.")
    elif STAGING:
        warns.append("**No visible staging banner, and the build is still staging.** Run "
                     "`scripts/sync-chrome.py`, which writes it from `STAGING`.")
    elif has_banner:
        fails.append("**The staging banner is still on this page and `STAGING` is off.** Every "
                     "visitor to the live site is told it is not the live site. Run "
                     "`scripts/sync-chrome.py`, which removes it.")
    else:
        passes.append("No staging banner: `STAGING` is off and the page says nothing about it.")
    return passes, warns, fails


def icon_findings(html_text: str, page_rel: str, site_dir: str = None) -> tuple:
    """(passes, fails) for one real page's favicon links, 3.94. Every
    ICON_LINKS entry must be linked from the head at the page's own relative
    path, and its file must exist under docs/. The sweep found none on any
    page while the live site has one, so cutover would have dropped the mark
    Google shows beside every result."""
    site_dir = site_dir or SITE_DIR
    head = html_text.split("</head>", 1)[0]
    prefix = "../" * page_rel.count("/")
    missing = []
    for rel, attrs, path in ICON_LINKS:
        want = f'<link rel="{rel}"' + (f" {attrs}" if attrs else "") + f' href="{prefix}{path}">'
        if want not in head:
            missing.append(want)
        elif not os.path.isfile(os.path.join(site_dir, path)):
            missing.append(f"the file docs/{path}")
    if missing:
        return [], [f"**Favicon set incomplete: missing {'; '.join(f'`{m}`' for m in missing)}.** "
                    "Run `scripts/sync-chrome.py`; the files come from "
                    "`scripts/prepare-favicon.py`."]
    return [f"Links the shop's favicon set: {len(ICON_LINKS)} icon links, every file present."], []


def visible_text(html: str) -> str:
    """What a reader actually sees: comments, scripts and styles removed,
    tags stripped, entities decoded, whitespace collapsed. Comments come
    out FIRST and on purpose, so an explanatory comment that records an
    old number is not read as the page claiming it."""
    s = re.sub(r"(?s)<!--.*?-->", " ", html)
    s = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1\s*>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", unescape(s)).strip()


def find_review_counts(root: str = SITE_DIR) -> list:
    """Every visible review-count mention under docs/, as
    (path, count, snippet). Walks .html and .txt, because llms.txt is
    read by the same assistants the pages are written for and a number
    that disagrees there disagrees just as loudly."""
    hits = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith((".html", ".txt")):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as f:
                    raw = f.read()
            except OSError:
                continue
            text = visible_text(raw) if name.endswith(".html") else raw
            for m in REVIEW_COUNT_RE.finditer(text):
                hits.append((path, int(m.group(1).replace(",", "")),
                             text[max(0, m.start() - 40):m.end() + 24].strip()))
    return hits


def find_rotting_comments(root: str = SITE_DIR) -> list:
    """Every HTML comment under docs/ that carries a number near the word
    "review", as (path, line, snippet). Whitespace is collapsed first, so
    a comment wrapped across five lines reads as one sentence and the
    "few words" window means what it says."""
    hits = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as f:
                    raw = f.read()
            except OSError:
                continue
            for m in HTML_COMMENT_RE.finditer(raw):
                body = re.sub(r"\s+", " ", m.group(1)).strip()
                for hit in COMMENT_REVIEW_NUM_RE.finditer(body):
                    hits.append((path, raw.count("\n", 0, m.start()) + 1,
                                 hit.group(0).strip()))
    return hits


def check_comment_convention_local(warns: list, notes: list):
    """THE CONVENTION: a comment names `REVIEW_COUNT` and "the band's DOM
    order", never the literal count and never the literal order.

    NO `fails` LIST, ON PURPOSE. This check cannot raise a critical
    because it was never handed anywhere to put one. A rotting comment
    misleads the next person to read the file and costs a visitor
    nothing, so it must never stop a build, and a check that can only
    warn is one nobody has a reason to delete.
    """
    hits = find_rotting_comments()
    if not hits:
        notes.append(
            "**No HTML comment under `docs/` carries a literal review count.** The "
            "convention is that comments name `REVIEW_COUNT` and the band's DOM order "
            "rather than quoting either, so they stay true when the values change. "
            "`\\breview\\b` cannot match inside `REVIEW_COUNT`, so the approved "
            "spelling is the one this check cannot fire on.")
        return
    where = "; ".join(f"`{pth}` line {ln} (\"{snip}\")" for pth, ln, snip in hits[:6])
    more = "" if len(hits) <= 6 else f", and {len(hits) - 6} more"
    warns.append(
        f"**{len(hits)} HTML comment{'' if len(hits) == 1 else 's'} under `{SITE_DIR}/` "
        f"carr{'ies' if len(hits) == 1 else 'y'} a number next to the word \"review\": "
        f"{where}{more}.** The review-count check strips comments before it reads counts, "
        "so a number quoted in one can go stale with nothing to catch it, which is exactly "
        "what happened on 2026-09-10. Rewrite it to name `REVIEW_COUNT` instead of quoting "
        "a value. This is a warning and it will never fail a build.")


def resolve_local_link(page_path: str, ref: str) -> str:
    """The file a relative reference points at, from the page holding it.
    A directory and an extensionless path both mean that folder's
    index.html, which is how this site's URLs work.

    SHARED ON PURPOSE. audit.py's pending-link inventory and
    test-audit-checks.py's no-dead-links test both call this, so the two
    directions of the same rule cannot drift apart by one resolving
    "../" differently from the other."""
    target = os.path.normpath(os.path.join(os.path.dirname(page_path),
                                           ref.split("?")[0].split("#")[0]))
    if os.path.isdir(target) or not os.path.splitext(target)[1]:
        target = os.path.join(target, "index.html")
    return target


def find_pending_links(root: str = SITE_DIR) -> list:
    """Every data-pending-href under docs/, as
    (path, line, href, target, ready). `ready` is True when the target
    file now exists, which means the wait is over and the element should
    have become a real link."""
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as f:
                    raw = f.read()
            except OSError:
                continue
            # COMMENTS COME OUT FIRST, the same way the dead-link scan
            # drops them. A pending attribute QUOTED IN A COMMENT is not a
            # pending attribute, it is an explanation of one, and on
            # 2026-09-10 an explanation of the mechanism tripped the
            # mechanism. The two halves of the link rule now agree about
            # what a comment is.
            raw = re.sub(r"(?s)<!--.*?-->", " ", raw)
            for m in PENDING_HREF_RE.finditer(raw):
                href = m.group(1)
                target = resolve_local_link(path, href)
                out.append((path, raw.count("\n", 0, m.start()) + 1, href,
                            target, os.path.isfile(target)))
    return out


def check_pending_links_local(warns: list, notes: list):
    """THE INVENTORY OF WHAT IS WAITING, in every Monday report.

    A note, not a warning, while everything is genuinely still waiting:
    an unbuilt page is the plan working, not a defect. The gate is
    test-audit-checks.py, which fails the build the day a target exists
    and its element is still a span.
    """
    pend = find_pending_links()
    if not pend:
        notes.append(
            "**Nothing is waiting to become a link.** No element under "
            f"`{SITE_DIR}/` carries `data-pending-href`, so either every page "
            "this site references exists, or nothing references one that does not.")
        return

    ready = [x for x in pend if x[4]]
    by_href = {}
    for _path, _line, href, _target, is_ready in pend:
        by_href.setdefault(href, {"n": 0, "ready": is_ready})
        by_href[href]["n"] += 1

    lines = []
    for href in sorted(by_href):
        info = by_href[href]
        mark = " **<- BUILT, convert these to real links**" if info["ready"] else ""
        lines.append(f"  - `{href}`, {info['n']} element"
                     f"{'' if info['n'] == 1 else 's'}{mark}")
    body = "\n".join(lines)

    head = (f"**{len(pend)} element{'' if len(pend) == 1 else 's'} waiting to become "
            f"link{'' if len(pend) == 1 else 's'}**, across "
            f"{len({x[3] for x in pend})} target page"
            f"{'' if len({x[3] for x in pend}) == 1 else 's'}:")
    why = ("\n\nEach carries `data-pending-href` with the URL it becomes. They are "
           "not links yet because this site never writes a link to a page that has "
           "not been built, and each target above is still unbuilt. This is the plan "
           "working, not a defect. `scripts/test-audit-checks.py` fails the build "
           "from the day a target exists, so none of them can be forgotten.")
    if ready:
        why = ("\n\n**" + str(len(ready)) + " of them are ready now**: the target file "
               "exists, so the element should already be a real link. The link test is "
               "failing on this and will keep failing until it is converted." + why)
    notes.append(head + "\n" + body + why)


def find_brand_claims(root: str = None) -> dict:
    """Every place under docs/ that states how many brands, as
    {kind: [(path, count, snippet)]}.

    Three kinds, because they fail in different ways and a report that
    says which one drifted is a report somebody can act on:

      marks   the pictures in the strip, counted from the one track that
              is not aria-hidden
      text    what a reader sees, comments and scripts stripped first
      schema  what a crawler and an assistant read, inside JSON-LD

    SITE_DIR is resolved when this is CALLED, like find_assets, because
    the tests point the check at a temporary directory.
    """
    root = root or SITE_DIR
    out = {"marks": [], "text": [], "schema": []}
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith((".html", ".txt")):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as f:
                    raw = f.read()
            except OSError:
                continue
            if name.endswith(".html"):
                for m in BRAND_TRACK_RE.finditer(raw):
                    n = len(re.findall(r"<img\b", m.group(1), re.I))
                    out["marks"].append((path, n, f"{n} marks in the strip"))
                for m in JSONLD_RE.finditer(raw):
                    for hit in BRAND_COUNT_RE.finditer(m.group(1)):
                        out["schema"].append(
                            (path, brand_number(hit), hit.group(0).strip()))
                text = visible_text(raw)
            else:
                text = raw
            for hit in BRAND_COUNT_RE.finditer(text):
                out["text"].append((path, brand_number(hit),
                                    text[max(0, hit.start() - 40):hit.end() + 16].strip()))
    return out


def brand_number(m) -> int:
    """The count a match states, whether it is written 12, 12+ or twelve."""
    if m.group(1):
        return int(m.group(1))
    return BRAND_WORDS[m.group(2).lower()]


def check_brand_count_local(passes: list, warns: list, fails: list,
                            notes: list):
    """THE BRAND COUNT, ENFORCED RATHER THAN REMEMBERED.

    DISAGREEMENT IS A CRITICAL, and this is the review count's argument
    in a second key. One shop is certified for one number of brands. A
    strip of fourteen marks over a sentence that says a dozen is the
    live site's own state today, and it is the kind of thing that
    survives for years because the picture and the prose are edited in
    different rooms.

    The recorded BRAND_COUNT counts as one of the voices, so a single
    page that drifts from the constant fails on its own.

    Local runs only, like the review count and the asset provenance: it
    reads files under docs/, and a live run is auditing WordPress.
    """
    found = find_brand_claims()
    seen = {}
    for kind in ("marks", "text", "schema"):
        for path, n, snip in found[kind]:
            seen.setdefault(n, []).append((kind, path, snip))
    seen.setdefault(BRAND_COUNT, []).append(
        ("constant", "scripts/audit.py", f"BRAND_COUNT = {BRAND_COUNT}"))

    distinct = sorted(seen)
    total = sum(len(found[k]) for k in found)

    # "12+" IS RULED OUT, 3.94. It reads as the same count above, because it
    # is the same claim, but Greg ruled the site says 12: a "+" beside a list
    # of exactly twelve promises brands nobody has named.
    plus = sorted({f"`{pth}` ({kind})" for kind in ("text", "schema")
                   for pth, _n, snip in found[kind] if BRAND_PLUS_RE.search(snip)})
    if plus:
        fails.append(f"**A brand count carries a \"+\":** {', '.join(plus)}. The site says "
                     f"{BRAND_COUNT}, by Greg's ruling of 2026-10-09 (proposed-changes.md 3.94).")

    if len(distinct) > 1:
        where = "; ".join(
            "**{}** from {}".format(
                n, ", ".join(sorted({f"{kind} in `{pth}`" for kind, pth, _ in seen[n]})))
            for n in distinct)
        fails.append(
            f"**The site states {len(distinct)} different brand counts: {where}.** "
            "The marks in the strip, the number claimed in text and the number in the "
            "schema have to be the same number, because they are the same claim said "
            "three ways. Confirm the list with the owner, then move `BRAND_COUNT`, the "
            "strip and every page in one commit.")
    elif not total:
        notes.append(
            f"**No page states a brand count.** `BRAND_COUNT` is {BRAND_COUNT} and "
            "nothing publishes it yet. Nothing to disagree.")
    else:
        notes.append(
            f"**Brand count agrees everywhere: {BRAND_COUNT}.** "
            f"{len(found['marks'])} strip{'' if len(found['marks']) == 1 else 's'} of marks, "
            f"{len(found['text'])} mention{'' if len(found['text']) == 1 else 's'} in visible "
            f"text and {len(found['schema'])} in JSON-LD, all saying {BRAND_COUNT}. "
            "The live site's own carousel shows fourteen against its prose's dozen; this "
            "is the check that keeps that from happening here.")


def find_brand_lists(root: str = None) -> list:
    """Every brand list under docs/, as (page_rel, kind, names, snippet),
    kind "text" or "schema". Comments and scripts are stripped from the
    visible text first, as everywhere else."""
    root = root or SITE_DIR
    canon = {b.lower(): b for b in BRANDS}
    other = {b.lower(): b for b in OTHER_BRANDS}
    tok = re.compile(r"(?<![\w-])" + _BRAND_TOKEN + r"(?![\w-])", re.I)
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith((".html", ".txt")):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as f:
                    raw = f.read()
            except OSError:
                continue
            rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
            rel = "" if rel == "." else rel + "/"
            sources = []
            if name.endswith(".html"):
                sources.append(("text", visible_text(raw)))
                sources += [("schema", m.group(1)) for m in JSONLD_RE.finditer(raw)]
            else:
                sources.append(("text", raw))
            for kind, text in sources:
                for m in BRAND_LIST_RE.finditer(text):
                    names = [canon.get(t.lower()) or other.get(t.lower()) or t
                             for t in tok.findall(m.group(0))]
                    out.append((rel if name == "index.html" else rel + name, kind, names,
                                m.group(0)))
    return out


def brand_list_findings(lists: list) -> tuple:
    """(fails, notes, n_checked) for the lists find_brand_lists returns."""
    fails, notes = [], []
    half = (len(BRANDS) + 1) // 2
    for page, kind, names, snip in lists:
        outside = sorted({n for n in names if n not in BRANDS})
        named = {n for n in names if n in BRANDS}
        where = f"`{page or '/'}` ({kind})"
        if outside:
            fails.append(
                f"**A brand list names {', '.join(outside)}, which BRANDS does not carry,** in "
                f"{where}: \u201c{snip}\u201d. The site claims only the {len(BRANDS)} in BRANDS "
                f"until the owner confirms another (proposed-changes.md question 6b).")
        elif len(named) >= half and len(named) < len(BRANDS):
            missing = [b for b in BRANDS if b not in named]
            if page in BRAND_LISTS_HELD:
                notes.append(f"**A short brand list is held, not passed,** in {where}: missing "
                             f"{', '.join(missing)}. {BRAND_LISTS_HELD[page]}")
            else:
                fails.append(
                    f"**A list of {len(named)} brands leaves out {', '.join(missing)},** in "
                    f"{where}: \u201c{snip}\u201d. A list naming half or more of BRANDS is the "
                    f"list, and names all {len(BRANDS)}; a few examples are fine.")
    return fails, notes, len(lists)


def check_brand_lists_local(passes: list, fails: list, notes: list, root: str = None):
    """THE BRAND LISTS, READ RATHER THAN COUNTED, 3.94. See BRAND_LIST_RE."""
    f, n, count = brand_list_findings(find_brand_lists(root))
    fails += f
    notes += n
    if not f:
        passes.append(f"Every brand list on the site names only the {len(BRANDS)} in BRANDS, "
                      f"and every list long enough to be the list names all of them "
                      f"({count} list{'' if count == 1 else 's'} read"
                      f"{', ' + str(len(n)) + ' held on an owner question' if n else ''}).")


# --- Town-page variance, the areas tier's gate (3.62) -------------------
# The doctrine's rule 7: a town page exists only with verified variance
# against its hub and every sibling, under 30 percent shared vocabulary and
# no shared substantive H2. Built with the first town page, 2026-09-28, so
# the second cannot ship a lookalike. With one town it compares nothing,
# and says so.
#
# THE MEASURE, proposed in proposed-changes.md 3.62 and calibrated there:
# THREE-WORD SHINGLES, CONTAINMENT, PLACE NAMES MASKED. Each page's
# substantive text is lowercased and every place name in TOWN_PLACE_NAMES,
# plus the page's own town from its slug, becomes one token; the text is
# cut into every run of three consecutive words; and a pair's figure is
# the phrases they share over the phrases of the SMALLER page. A pair at
# or over TOWN_SHARED_MAX fails.
#
# WHY NOT SINGLE WORDS: two honest pages about one shop share "collision",
# "insurance" and "estimate" by necessity. Single-word overlap between our
# own four service pages is 46 to 65 percent, and they are not lookalikes.
# The doorway problem is shared PHRASING, and three-word phrases separate
# it cleanly: 7 to 10 percent between the service pages, 1 to 3 between
# posts, 56 to 65 between the shop's eleven live town pages, which differ
# by little more than the town's name. Measured by these functions, not a
# prototype of them, 2026-09-28. WHY MASKED: a copy with the name
# swapped must read as the copy it is. WHY CONTAINMENT, NOT JACCARD: a
# short page tucked inside a long one is a lookalike, and Jaccard would
# let the long one's extra text dilute it away.
#
# PATTERN TEXT IS DEFINED HERE, NEVER IN MARKUP. What the template repeats
# on every town page by design is left out of both measures: anything in
# a <nav> (the crumb), the sections whose ids are in TOWN_PATTERN_SECTIONS
# (the promise band, the nearby-towns links, the Real Repairs pairs from
# 3.63, and "Why drivers pass closer shops", which from 3.67 carries the
# figures and the chips' claims as cards, byte-identical on every town page
# because the reasons do not change by town), and the .svc-card links to
# the four service pages. A page cannot mark its own
# shared prose as pattern to escape the measure, because the list is not
# the page's to write. Everything else, the FAQ included, is compared.
#
# THE H2 HALF compares substantive H2s literally, case and spacing aside,
# with no masking: the template puts the town's name in every substantive
# H2 on purpose (Greg's brief, 3.62), and the phrase measure above is what
# catches a page that only swapped the name.
# --- One routing per town, every rendering derived (3.65) ---------------
# Greg's accuracy mandate, 2026-09-28: ACCURACY IS A GATE, NOT A GOAL. A
# town page's drive time, distance and directions are the RECORDED ROUTING
# below and derivations of it, and nothing else. Two values that must agree
# are one value plus a derivation. town_route_findings, run on every town
# page by audit(), fails any rendering that disagrees, and
# prepare-map-image.py refuses to draw from a routing file that disagrees
# with these figures, or to label a road the drive does not use.
#
# THE SHAPE. Keyed by the page's slug after "areas-served-collision-repair-".
#   miles, minutes   the whole primary route, as OSRM measured it, free-flow
#   steps            (road, ref, modifier, bearing, miles), one per NUMBERED
#                    STEP on the page, in driving order. The depart step is
#                    left out when it is under 0.02 mi (the page starts at
#                    the town's corner), the unnamed final metres into the
#                    lot are left out, and a "new name" maneuver is not a
#                    turn: its miles fold into the step before it. Since
#                    3.77 a roundabout and its exit are one step on the
#                    exit road, and a "continue" WITH a turn (Richboro's
#                    keep-right) stays its own step.
#   place, corner,   the OSM place node the corner is measured from; the
#   max_m            corner's two roads, its node and coordinates (the
#                    routing's origin); and the refusal radius, 60m unless
#                    Greg widened it for one town with a recorded
#                    max_m_why (3.78)
#   roads_driven     every OSM road name the route's ways carry, which is a
#                    superset of the step names (3.65, Greg's ruling: West
#                    Bristol Road is "East Bristol Road" in OSM for half its
#                    length, a driver mid-leg sees that name, and the map may
#                    label it). The map's labels must be a subset of this.
#
# THE DERIVATIONS, and the only renderings the check accepts:
#   minutes          minutes rounded half-up: "about 15 minutes", "~15 min"
#   route miles      whole miles half-up, or to one decimal: "about 8",
#                    "about 8.4"
#   step miles       under an eighth of a mile, feet to the nearest hundred,
#                    never under 100 ("about 200 feet", 3.78); under half a
#                    mile, the nearest quarter ("a quarter mile"); otherwise
#                    whole miles half-up: "about 2 miles"
#   EVERY ROUNDING IS HALF-UP (3.78): Python's round() is banker's, and sent
#                    an eighth of a mile, half a mile, 8.5 and 10.5 minutes
#                    the wrong way.
#   turn words       "left" and "right" against the step's maneuver modifier
#   compass words    against the maneuver's bearing, on eight points; OSRM
#                    has no compass modifier, and step 1 begins at the
#                    corner facing the way (Greg, 3.65: approved as read)
TOWN_ROUTE_PREFIX = "areas-served-collision-repair-"
TOWN_ROUTES = {
    # OSRM driving, router.project-osrm.org, fetched 2026-09-28, from
    # OpenStreetMap node 158375416 (Jamison, place=village, at York Road and
    # Almshouse Road) to GEO_LAT, GEO_LON. proposed-changes.md 3.62 and 3.65.
    "jamison-pa": {
        "recorded": "2026-09-28",
        "miles": 8.42,
        "minutes": 14.8,
        "place": (158375416, 40.2548297, -75.0893372),
        "corner": ("York Road", "Almshouse Road", 158375416, 40.2548297, -75.0893372),
        "max_m": 60,
        "steps": (
            ("York Road", "PA 263", "right", 194, 1.92),
            ("West Bristol Road", "", "left", 126, 4.09),
            ("Second Street Pike", "PA 232", "right", 177, 2.10),   # 1.37 + 0.73 as "2nd Street Pike"
            ("Jaymor Road", "", "right", 281, 0.28),
        ),
        "roads_driven": ("York Road", "West Bristol Road", "East Bristol Road",
                         "Second Street Pike", "2nd Street Pike", "Jaymor Road"),
    },
    # RUN TWO'S ROUTINGS, 3.77 and 3.78. Every town routed before any hub
    # copy leans on it, so the strategy chat double-checks the whole table
    # once. "place" is the OSM place node the corner is measured from;
    # "corner" is the two named roads, the OSM node the routing starts from
    # and its coordinates, which are the routing's origin; "max_m" is the
    # refusal radius, 60 unless Greg widened it for one town, and a widened
    # one carries "max_m_why". test-audit-checks.py holds every entry to its
    # own radius, and refuses a widened radius with no reason.
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 111019889,
    # Knights Road at Street Road, 62m from place node 158863395, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.78. Steps condensed by the rules recorded in 3.77.
    "bensalem-pa": {
        "recorded": "2026-09-29",
        "miles": 8.14,
        "minutes": 14.8,
        "place": (158863395, 40.1045549, -74.951279),
        "corner": ("Knights Road", "Street Road", 111019889, 40.104902, -74.950713),
        "max_m": 65,
        "max_m_why": "Knights Road at Street Road is Bensalem's main crossroads, 61.6m from the township's label point; the only junction inside 60m is a residential side street (Greg, 3.78)",
        "steps": (
            ("Street Road", "PA 132", "", 340, 7.12),
            ("2nd Street Pike", "PA 232", "left", 189, 0.73),
            ("Jaymor Road", "", "right", 281, 0.28),
        ),
        "roads_driven": ("Street Road", "2nd Street Pike", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 111017981,
    # Buck Road at Street Road, 16m from place node 157558047, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.78. Steps condensed by the rules recorded in 3.77.
    "feasterville-trevose-pa": {
        "recorded": "2026-09-29",
        "miles": 2.92,
        "minutes": 6.0,
        "place": (157558047, 40.1581651, -75.0151696),
        "corner": ("Buck Road", "Street Road", 111017981, 40.158159, -75.014985),
        "max_m": 60,
        "steps": (
            ("Street Road", "PA 132", "", 307, 1.90),
            ("2nd Street Pike", "PA 232", "left", 189, 0.73),
            ("Jaymor Road", "", "right", 281, 0.28),
        ),
        "roads_driven": ("Street Road", "2nd Street Pike", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 110966333,
    # Bellevue Avenue at West Maple Avenue, 3m from place node 158846519, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.77. Steps condensed by the rules recorded in 3.77.
    "langhorne-pa": {
        "recorded": "2026-09-29",
        "miles": 8.78,
        "minutes": 16.0,
        "place": (158846519, 40.1761812, -74.9202481),
        "corner": ("Bellevue Avenue", "West Maple Avenue", 110966333, 40.176161, -74.9202792),
        "max_m": 60,
        "steps": (
            ("West Maple Avenue", "PA 213", "", 258, 2.53),
            ("Bridgetown Pike", "PA 213", "straight", 209, 2.29),
            ("Bustleton Pike", "PA 532", "straight", 198, 0.20),
            ("Street Road", "PA 132", "right", 227, 2.73),
            ("2nd Street Pike", "PA 232", "left", 189, 0.73),
            ("Jaymor Road", "", "right", 281, 0.28),
        ),
        "roads_driven": ("West Maple Avenue", "Bridgetown Pike", "Bustleton Pike", "Street Road", "2nd Street Pike", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 111455644,
    # 2nd Street Pike at Almshouse Road, 29m from place node 158624917, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.77. Steps condensed by the rules recorded in 3.77.
    "richboro-pa": {
        "recorded": "2026-09-29",
        "miles": 4.48,
        "minutes": 8.0,
        "place": (158624917, 40.2151086, -75.0107245),
        "corner": ("2nd Street Pike", "Almshouse Road", 111455644, 40.215324, -75.010532),
        "max_m": 60,
        "steps": (
            ("2nd Street Pike", "PA 232", "", 183, 0.29),
            ("2nd Street Pike", "PA 232", "right", 227, 3.89),
            ("Jaymor Road", "", "right", 281, 0.28),
        ),
        "roads_driven": ("2nd Street Pike", "North 2nd Street Pike", "Second Street Pike", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 111018891,
    # Street Road at York Road, 12m from place node 158566218, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.77. Steps condensed by the rules recorded in 3.77.
    "warminster-pa": {
        "recorded": "2026-09-29",
        "miles": 4.61,
        "minutes": 9.2,
        "place": (158566218, 40.2067751, -75.0996159),
        "corner": ("Street Road", "York Road", 111018891, 40.2067688, -75.0997553),
        "max_m": 60,
        "steps": (
            ("York Road", "PA 263", "sharp left", 189, 1.17),
            ("East County Line Road", "", "left", 125, 2.96),
            ("James Way", "", "left", 40, 0.40),
            ("Jaymor Road", "", "right", 146, 0.06),
        ),
        "roads_driven": ("Street Road", "York Road", "East County Line Road", "West County Line Road", "James Way", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 112228579,
    # South York Road at Byberry Road, 6m from place node 158588118, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.77. Steps condensed by the rules recorded in 3.77.
    "hatboro-pa": {
        "recorded": "2026-09-29",
        "miles": 3.58,
        "minutes": 7.9,
        "place": (158588118, 40.1746252, -75.106825),
        "corner": ("South York Road", "Byberry Road", 112228579, 40.1745959, -75.1068825),
        "max_m": 60,
        "steps": (
            ("Byberry Road", "", "", 90, 1.30),
            ("Davisville Road", "", "left", 64, 0.85),
            ("East County Line Road", "", "right", 126, 0.96),
            ("James Way", "", "left", 40, 0.40),
            ("Jaymor Road", "", "right", 146, 0.06),
        ),
        "roads_driven": ("Byberry Road", "Davisville Road", "East County Line Road", "James Way", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 601720529,
    # Easton Road at Horsham Road, 92m from place node 158401563, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.78. Steps condensed by the rules recorded in 3.77.
    "horsham-pa": {
        "recorded": "2026-09-29",
        "miles": 5.39,
        "minutes": 11.3,
        "place": (158401563, 40.1784422, -75.1285061),
        "corner": ("Easton Road", "Horsham Road", 601720529, 40.1776137, -75.1283706),
        "max_m": 95,
        "max_m_why": "a township's place point is not a village centre; Easton Road at Horsham Road, 92.3m, is the self-evident reference corner (Greg, 3.78)",
        "steps": (
            ("Horsham Road", "", "", 89, 0.30),
            ("Blair Mill Road", "", "left", 36, 1.41),
            ("West County Line Road", "", "right", 126, 3.21),
            ("James Way", "", "left", 40, 0.40),
            ("Jaymor Road", "", "right", 146, 0.06),
        ),
        "roads_driven": ("Horsham Road", "Blair Mill Road", "West County Line Road", "East County Line Road", "James Way", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 5549211250,
    # Huntingdon Pike at Wynkoop Avenue, 61m from place node 158228562, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.78. Steps condensed by the rules recorded in 3.77.
    "huntingdon-valley-pa": {
        "recorded": "2026-09-29",
        "miles": 3.39,
        "minutes": 7.8,
        "place": (158228562, 40.1226101, -75.0635049),
        "corner": ("Huntingdon Pike", "Wynkoop Avenue", 5549211250, 40.1229069, -75.0641086),
        "max_m": 65,
        "max_m_why": "Huntingdon Pike at Wynkoop Avenue, 61.0m, is the main crossroads by the place point; same reasoning as Bensalem (Greg, 3.78)",
        "steps": (
            ("Huntingdon Pike", "PA 232", "", 34, 3.10),
            ("Jaymor Road", "", "left", 281, 0.28),
        ),
        "roads_driven": ("Huntingdon Pike", "2nd Street Pike", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 2125917445,
    # Old York Road at West Avenue, 16m from place node 158472613, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.77. Steps condensed by the rules recorded in 3.77.
    "jenkintown-pa": {
        "recorded": "2026-09-29",
        "miles": 7.77,
        "minutes": 17.1,
        "place": (158472613, 40.0959539, -75.125651),
        "corner": ("Old York Road", "West Avenue", 2125917445, 40.0958613, -75.1257942),
        "max_m": 60,
        "steps": (
            ("West Avenue", "", "", 88, 0.20),
            ("Newbold Road", "", "right", 133, 0.04),
            ("Washington Lane", "", "left", 36, 0.98),
            ("Susquehanna Road", "", "left", 343, 0.08),
            ("Valley Road", "", "right", 343, 2.06),
            ("Welsh Road", "PA 63", "right", 127, 0.71),
            ("Huntingdon Pike", "PA 232", "left", 119, 3.40),
            ("Jaymor Road", "", "left", 281, 0.28),
        ),
        "roads_driven": ("West Avenue", "Newbold Road", "Washington Lane", "Susquehanna Road", "Valley Road", "Welsh Road", "Huntingdon Pike", "2nd Street Pike", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 601352294,
    # Easton Road at York Road, 38m from place node 158472698, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.77. Steps condensed by the rules recorded in 3.77.
    "willow-grove-pa": {
        "recorded": "2026-09-29",
        "miles": 4.59,
        "minutes": 10.5,
        "place": (158472698, 40.1439985, -75.1157286),
        "corner": ("Easton Road", "York Road", 601352294, 40.143664, -75.1156279),
        "max_m": 60,
        "steps": (
            ("York Road", "PA 611", "", 124, 0.07),
            ("Davisville Road", "", "left", 36, 3.08),
            ("East County Line Road", "", "right", 126, 0.96),
            ("James Way", "", "left", 40, 0.40),
            ("Jaymor Road", "", "right", 146, 0.06),
        ),
        "roads_driven": ("York Road", "Davisville Road", "East County Line Road", "James Way", "Jaymor Road"),
    },
    # OSRM driving, router.project-osrm.org, fetched 2026-09-29, from OSM node 110154627,
    # Bustleton Avenue at Byberry Road, 45m from place node 158530515, to GEO_LAT, GEO_LON.
    # proposed-changes.md 3.78. Steps condensed by the rules recorded in 3.77.
    "northeast-philadelphia": {
        "recorded": "2026-09-29",
        "miles": 4.39,
        "minutes": 8.5,
        "place": (158530515, 40.1234434, -75.0148921),
        "corner": ("Bustleton Avenue", "Byberry Road", 110154627, 40.123599, -75.015384),
        "max_m": 60,
        "steps": (
            ("Byberry Road", "", "", 307, 2.87),
            ("Huntingdon Pike", "PA 232", "right", 45, 1.22),
            ("Jaymor Road", "", "left", 281, 0.28),
        ),
        "roads_driven": ("Byberry Road", "Huntingdon Pike", "2nd Street Pike", "Jaymor Road"),
    },
}
# THE SERVED LIST, 3.79: ONE LIST, NOT TYPED PER PAGE. The shared business
# node's areaServed on every page is written from this by
# scripts/sync-area-served.py, and the audit fails any page whose node
# says otherwise. It closes 3.62's open item: Jamison had a page and was
# missing from the list every page carried. Order is the hub's: the three
# areas, the shop's own town, then Bucks, Montgomery and Philadelphia as
# the hub lists them, Jamison closing the Bucks group. Only places the hub
# serves by name; the five it names without pages are not here.
AREA_SERVED_BASE = "https://tricountycollision.com/"
AREA_SERVED = (
    ("AdministrativeArea", "Bucks County, Pennsylvania", "#area-bucks-county"),
    ("AdministrativeArea", "Montgomery County, Pennsylvania", "#area-montgomery-county"),
    ("AdministrativeArea", "Philadelphia, Pennsylvania", "#area-philadelphia"),
    ("City", "Southampton, Pennsylvania", "#area-bucks-county"),
    ("City", "Feasterville-Trevose, Pennsylvania", "#area-bucks-county"),
    ("City", "Richboro, Pennsylvania", "#area-bucks-county"),
    ("City", "Warminster, Pennsylvania", "#area-bucks-county"),
    ("City", "Langhorne, Pennsylvania", "#area-bucks-county"),
    ("City", "Bensalem, Pennsylvania", "#area-bucks-county"),
    ("City", "Jamison, Pennsylvania", "#area-bucks-county"),
    ("City", "Huntingdon Valley, Pennsylvania", "#area-montgomery-county"),
    ("City", "Hatboro, Pennsylvania", "#area-montgomery-county"),
    ("City", "Willow Grove, Pennsylvania", "#area-montgomery-county"),
    ("City", "Horsham, Pennsylvania", "#area-montgomery-county"),
    ("City", "Jenkintown, Pennsylvania", "#area-montgomery-county"),
    ("Place", "Northeast Philadelphia, Pennsylvania", "#area-philadelphia"),
)


def area_served_nodes() -> list:
    """The areaServed array every business node carries, in the exact shape
    the pages have used since 3.47: the three areas carry their @id, every
    place names the area it sits in."""
    out = []
    for kind, name, ref in AREA_SERVED:
        if kind == "AdministrativeArea":
            out.append({"@type": kind, "@id": AREA_SERVED_BASE + ref, "name": name})
        else:
            out.append({"@type": kind, "name": name,
                        "containedInPlace": {"@id": AREA_SERVED_BASE + ref}})
    return out


COMPASS_8 = ("north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest")


def compass_of(bearing: float) -> str:
    return COMPASS_8[int(((bearing + 22.5) % 360) // 45)]


def step_miles_phrase(mi: float) -> str:
    """The one way a step's distance is written, derived.

    UNDER AN EIGHTH OF A MILE, FEET (3.78, Greg's ruling): rounded half-up
    to the nearest hundred and never under 100, so 0.04 mi derives
    "200 feet" and 0.08 derives "400 feet"; the page writes it with the
    house qualifier, "about 200 feet", as it writes "about 2 miles". It
    never derives "0.0 miles", which the quarter-mile rounding used to for
    any step this short. Rounding is half-up throughout the short range:
    Python's round() is banker's, which sent exactly an eighth (0.125 mi)
    to "0.0 miles" as well."""
    if mi < 0.125:
        return f"{max(100, int(mi * 5280 / 100 + 0.5) * 100)} feet"
    if mi < 0.5:
        q = int(mi * 4 + 0.5) / 4
        return {0.25: "a quarter mile", 0.5: "half a mile"}.get(q, f"{q} miles")
    # Half-up here too, found while testing the short-step rule: round() sent
    # exactly half a mile to "0 miles", and 2.5 to 2 while 3.5 went to 4.
    n = int(mi + 0.5)
    return f"{n} mile" if n == 1 else f"{n} miles"


ROUTE_QTY_RE = re.compile(
    r"(?:~\s*|about\s+|roughly\s+|around\s+)?(\d+(?:\.\d+)?)\s*(miles?|minutes?|mins?)\b"
    r"|\b(a quarter mile|half a mile)\b"
    r"|\b(\d{2,5})\s*feet\b", re.I)
_USPS = {"road": "rd", "avenue": "ave", "street": "st", "drive": "dr", "lane": "ln",
         "boulevard": "blvd", "pike": "pike", "turnpike": "tpke", "highway": "hwy"}


def road_key(name: str) -> str:
    """A road name compared by its words, suffix and direction abbreviated
    the USPS way, so "Jaymor Road" and "Jaymor Rd" are one road."""
    w = re.findall(r"[a-z0-9]+", name.lower())
    w = [{"west": "w", "east": "e", "north": "n", "south": "s"}.get(x, x) if i == 0 and len(w) > 2 else x
         for i, x in enumerate(w)]
    if w and w[-1] in _USPS:
        w[-1] = _USPS[w[-1]]
    return " ".join(w)


_NUM_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split())}
_NUM_WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "a": 1, "an": 1})
_NUM_WORD_RE = re.compile(
    r"(?<!half )(?<!half\u00a0)\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
    r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|an?)"
    r"(?:-(one|two|three|four|five|six|seven|eight|nine))?(\s+and\s+a\s+half)?"
    r"(\s+(?:miles?|minutes?|mins?)\b)", re.I)


def _digits_for_words(text: str) -> str:
    """Number words before a unit become digits, so "about four miles" and
    "ten to fifteen minutes" are read like "about 4 miles" (3.79: the live
    hub wrote every figure in words, and a check that reads only digits is
    blind to them). "A quarter mile" and "half a mile" are left alone: they
    are step phrases, read as such."""
    def one(m):
        n = _NUM_WORDS[m.group(1).lower()] + (_NUM_WORDS[m.group(2).lower()] if m.group(2) else 0)
        v = n + 0.5 if m.group(3) else n
        return (f"{v:g}") + m.group(4)
    text = _NUM_WORD_RE.sub(one, text)
    # Then every remaining number word, unit or not, so the low end of a
    # spelled-out range ("Ten to 15 minutes") is a number the range reader
    # sees. "A" and "an" are not in this pass: "a quarter mile" stays a
    # step phrase. A number word with no unit near it is read as nothing.
    text = _BARE_NUM_RE.sub(lambda m: str(_NUM_WORDS[m.group(1).lower()]
                                         + (_NUM_WORDS[m.group(2).lower()] if m.group(2) else 0)), text)
    # A RANGE STATES BOTH ENDS, and both are read: "10 to 15 minutes" becomes
    # "10 minutes to 15 minutes". Before this only the upper end was seen, so
    # a range whose upper end happened to be derived passed with any lower.
    return _RANGE_RE.sub(lambda m: m.group(1) + m.group(4) + m.group(2) + m.group(3) + m.group(4), text)


_BARE_NUM_RE = re.compile(
    r"(?<!half )\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
    r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty)"
    r"(?:-(one|two|three|four|five|six|seven|eight|nine))?\b", re.I)
_RANGE_RE = re.compile(r"\b(\d+(?:\.\d+)?)(\s*(?:to|or|-|\u2013)\s*)(\d+(?:\.\d+)?)(\s+(?:miles?|minutes?|mins?)\b)",
                       re.I)


def route_quantities(text: str) -> list:
    """Every drive-time and distance rendering in a text, as (kind, value, snippet)."""
    out = []
    text = _digits_for_words(text)
    for m in ROUTE_QTY_RE.finditer(text):
        snip = text[max(0, m.start() - 30):m.end() + 10].strip()
        if m.group(3):
            out.append(("step", m.group(3).lower(), snip))
        elif m.group(4):
            out.append(("step", f"{int(m.group(4))} feet", snip))
        elif m.group(2).lower().startswith("mi") and not m.group(2).lower().startswith("min"):
            out.append(("miles", float(m.group(1)), snip))
        else:
            out.append(("minutes", float(m.group(1)), snip))
    return out


class _StepParser(HTMLParser):
    """The numbered steps inside #getting-here: each li's <strong> text and
    its whole text, in order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0          # inside #getting-here
        self.ol = 0
        self.items = []
        self._strong = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and a.get("id") == "getting-here":
            self.depth = 1
        elif self.depth and tag == "section":
            self.depth += 1
        if self.depth and tag == "ol" and "numbered" in (a.get("class") or ""):
            self.ol += 1
        if self.ol and tag == "li":
            self.items.append({"strong": "", "text": ""})
        if self.ol and tag == "strong":
            self._strong = True

    def handle_endtag(self, tag):
        if tag == "section" and self.depth:
            self.depth -= 1
        if tag == "ol" and self.ol:
            self.ol -= 1
        if tag == "strong":
            self._strong = False

    def handle_data(self, data):
        if self.ol and self.items:
            self.items[-1]["text"] += data
            if self._strong:
                self.items[-1]["strong"] += data


def town_route_findings(html_text: str, route: dict, llms_entry: str = "") -> list:
    """Every disagreement between a town page and its recorded routing, as
    human-readable strings. Empty means the page derives from the routing."""
    bad = []
    # Half-up (3.78): round() is banker's, and derived 10 from Willow Grove's
    # 10.5 minutes and 8 from Northeast Philadelphia's 8.5.
    minutes = int(route["minutes"] + 0.5)
    # Half-up, as step_miles_phrase is (3.78): the whole-mile figure a page
    # may state must be the one the phrase derivation would give.
    miles_ok = {float(int(route["miles"] + 0.5)), round(route["miles"], 1)}
    steps = route["steps"]
    step_phrases = {step_miles_phrase(s[4]) for s in steps}
    miles_ok |= {float(int(s[4] + 0.5)) for s in steps if s[4] >= 0.5}
    # 1. Every rendering: the visible page, the meta description, the
    # JSON-LD (the FAQ's schema twin), every aria-label (the map's alt text)
    # and the page's llms.txt entry.
    p = PageParser()
    p.feed(html_text)
    texts = [("the page", visible_text(html_text)),
             ("the meta description", p.meta.get("description", "")),
             ("the JSON-LD", " ".join(p.jsonld_blocks)),
             ("an aria-label", " ".join(unescape(x) for x in re.findall(r'aria-label="([^"]*)"', html_text))),
             ("llms.txt", llms_entry)]
    for where, t in texts:
        for kind, val, snip in route_quantities(t or ""):
            if kind == "minutes" and val != minutes:
                bad.append(f"{where} says {val:g} minutes (“{snip}”); the recorded routing derives {minutes}")
            elif kind == "miles" and val not in miles_ok:
                bad.append(f"{where} says {val:g} miles (“{snip}”); the recorded routing derives "
                           f"{' or '.join(f'{m:g}' for m in sorted(miles_ok))}")
            elif kind == "step" and val not in step_phrases:
                bad.append(f"{where} says “{val}” (“{snip}”); no recorded step derives it")
    # 2. The numbered steps: one per recorded step, in order, each with the
    # routing's road, route number, turn word, compass word and distance.
    sp = _StepParser()
    sp.feed(html_text)
    items = sp.items
    if len(items) != len(steps):
        bad.append(f"the page has {len(items)} numbered steps; the recorded routing has {len(steps)}")
    for i, (it, (road, ref, mod, bearing, mi)) in enumerate(zip(items, steps), 1):
        strong, text = " ".join(it["strong"].split()), " ".join(it["text"].split())
        m = re.search(r"\b(?:onto|on)\s+(.+?)(?:\s*\(|$)", strong)
        page_road = m.group(1) if m else ""
        if road_key(page_road) != road_key(road):
            bad.append(f"step {i} names “{page_road or strong}”; the routing's step {i} is {road}")
        r = re.search(r"\(([^)]*)\)", strong)
        if r and r.group(1) != ref:
            bad.append(f"step {i} gives route number {r.group(1)}; the routing's is {ref or 'none'}")
        # A direction that is part of a road's NAME ("West Bristol Road") is
        # not a direction: every road name in the routing is taken out of the
        # step's text before its turn and compass words are read.
        bare = text
        for nm in sorted(set(route["roads_driven"]) | {s[0] for s in steps} | {page_road}, key=len, reverse=True):
            if nm:
                bare = re.sub(re.escape(nm), " ", bare, flags=re.I)
        bare = re.sub(r"\b\d+\s+Jaymor\s+Rd\b|\b[A-Z][a-z]+ Rd\b", " ", bare)
        for t in re.findall(r"\b(left|right)\b", bare, re.I):
            if t.lower() not in mod:
                bad.append(f"step {i} says turn {t.lower()}; the routing's maneuver is {mod}")
        for c in re.findall(r"\b(north|south|east|west|northeast|northwest|southeast|southwest)\b", bare, re.I):
            if c.lower() != compass_of(bearing):
                bad.append(f"step {i} says {c.lower()}; the routing's bearing {bearing} is {compass_of(bearing)}")
        for kind, val, snip in route_quantities(text):
            if kind == "minutes":
                continue
            said = val if kind == "step" else (f"{val:g} mile" if val == 1 else f"{val:g} miles")
            if said != step_miles_phrase(mi):
                bad.append(f"step {i} says “{snip}”; its recorded {mi} miles derives "
                           f"“{step_miles_phrase(mi)}”")
    return bad


def town_route_config_findings(routes: dict = None) -> list:
    """Every TOWN_ROUTES entry whose recorded corner is not its town's
    corner by its own rule (3.78): the corner more than max_m from the place
    point, a radius widened past 60m with no recorded reason, or a field
    missing. Empty means every entry is held to its own tolerance."""
    bad = []
    for key, r in (TOWN_ROUTES if routes is None else routes).items():
        try:
            _pn, plat, plon = r["place"]
            _ra, _rb, _cn, clat, clon = r["corner"]
            max_m = r["max_m"]
        except (KeyError, ValueError, TypeError):
            bad.append(f"{key}: place, corner or max_m is missing or malformed")
            continue
        d = math.hypot((clat - plat) * 110574.0,
                       (clon - plon) * 111320.0 * math.cos(math.radians(plat)))
        if d > max_m:
            bad.append(f"{key}: the corner is {d:.1f}m from the place point, over its {max_m}m")
        if max_m > 60 and not str(r.get("max_m_why", "")).strip():
            bad.append(f"{key}: max_m is widened to {max_m}m with no max_m_why recorded")
    return bad


# THE HUB IS HELD TO THE ROUTINGS TOO, 3.79 (protocol f, Greg's Q2 ruling).
# Each town's blurb on /areas-served/ is an element carrying
# data-town="<TOWN_ROUTES key>". Inside it every drive figure must derive
# from that town's routing, no compass word may appear (bearings came off
# the hub), and every road it names must be one the route drives or one of
# its corner's two roads; every route number must be one of its steps'.
# A drive figure OUTSIDE every town block is refused: nothing on the hub may
# state a distance or a time that no routing attributes. COMPASS WORDS ARE
# READ LOWERCASE ONLY, so "Northeast Philadelphia" and "East County Line
# Road" are names, not bearings; a sentence that opens with a bare compass
# word is the known gap, recorded in 3.79.
HUB_KIND = "hub"
HUB_ROAD_RE = re.compile(
    r"\b(?:[A-Z0-9][\w'-]*\s+){1,4}(?:Road|Rd|Pike|Avenue|Ave|Street|St|Lane|Ln|Way|"
    r"Boulevard|Blvd|Drive|Dr|Highway|Hwy|Turnpike)\b")
HUB_REF_RE = re.compile(r"\b(PA|US|I|Route)[- \u00a0]?(\d{1,3})\b")
HUB_COMPASS_RE = re.compile(r"\b(?:north|south|east|west)(?:east|west)?\b")


def hub_road_key(name: str) -> str:
    """road_key with any leading direction dropped and "second" read as
    "2nd", so "County Line Road" is East County Line Road's road and
    "Second Street Pike" is 2nd Street Pike's."""
    k = road_key(name).split()
    k = ["2nd" if w == "second" else w for w in k]
    if len(k) > 2 and k[0] in ("n", "s", "e", "w", "north", "south", "east", "west"):
        k = k[1:]
    return " ".join(k)


class _HubParser(HTMLParser):
    """The text of every data-town element inside <main>, by key, and the
    text of <main> outside all of them."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.main = 0
        self.stack = []        # open tags, with the data-town key they opened, if any
        self.blocks = {}
        self.outside = []
        self._skip = 0

    def _key(self):
        for _tag, key in reversed(self.stack):
            if key:
                return key
        return None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.main += 1
        if tag in ("script", "style"):
            self._skip += 1
        if tag in _VOID:
            return
        self.stack.append((tag, a.get("data-town")))

    def handle_endtag(self, tag):
        if tag == "main" and self.main:
            self.main -= 1
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self.main or self._skip:
            return
        k = self._key()
        if k:
            self.blocks[k] = self.blocks.get(k, "") + " " + data
        else:
            self.outside.append(data)


def hub_route_findings(html_text: str, routes: dict = None) -> list:
    """Every disagreement between the hub and the recorded routings."""
    routes = TOWN_ROUTES if routes is None else routes
    p = _HubParser()
    p.feed(html_text)
    bad = []
    for key, raw in p.blocks.items():
        text = " ".join(raw.split())
        r = routes.get(key)
        if r is None:
            if route_quantities(text):
                bad.append(f"{key}: states a drive figure, and {key} has no recorded routing")
            if HUB_ROAD_RE.search(text) or HUB_REF_RE.search(text):
                bad.append(f"{key}: names a road, and {key} has no recorded routing to check it against")
            continue
        minutes = int(r["minutes"] + 0.5)
        miles_ok = {float(int(r["miles"] + 0.5)), round(r["miles"], 1)}
        for kind, val, snip in route_quantities(text):
            if kind == "minutes" and val != minutes:
                bad.append(f"{key}: says {val:g} minutes (\u201c{snip}\u201d); its routing derives {minutes}")
            elif kind == "miles" and val not in miles_ok:
                bad.append(f"{key}: says {val:g} miles (\u201c{snip}\u201d); its routing derives "
                           f"{' or '.join(f'{m:g}' for m in sorted(miles_ok))}")
            elif kind == "step":
                bad.append(f"{key}: says \u201c{val}\u201d; the hub states whole-route figures only")
        for c in HUB_COMPASS_RE.findall(text):
            bad.append(f"{key}: says \u201c{c}\u201d; bearings came off the hub (Q2)")
        allowed = {hub_road_key(n) for n in r["roads_driven"]} | {hub_road_key(n) for n in r["corner"][:2]}
        for m in HUB_ROAD_RE.finditer(text):
            words = m.group(0).split()
            tails = {hub_road_key(" ".join(words[i:])) for i in range(len(words) - 1)}
            if not tails & allowed:
                bad.append(f"{key}: names \u201c{m.group(0)}\u201d, a road its routing does not drive")
        refs = {" ".join(x[1].split()) for x in r["steps"] if x[1]}
        for m in HUB_REF_RE.finditer(text):
            ref = f"{m.group(1)} {m.group(2)}"
            if ref not in refs:
                bad.append(f"{key}: names {m.group(0)}, a route number its steps do not drive")
    for kind, val, snip in route_quantities(" ".join(" ".join(p.outside).split())):
        bad.append(f"a drive figure outside every town block (\u201c{snip}\u201d): nothing attributes it to a town")
    return bad


def llms_entry_for(url: str, root: str = None) -> str:
    """The llms.txt entry for one URL: its line and the indented lines under it."""
    try:
        with open(os.path.join(root or SITE_DIR, "llms.txt"), encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return ""
    out, on = [], False
    for ln in lines:
        if ln.startswith("- "):
            on = url in ln
        if on:
            out.append(ln)
    return " ".join(out)


TOWN_KIND = "town"
TOWN_HUB_PATH = os.path.join("areas-served", "index.html")
# 3.67: THE LISTS FOLLOW THE TEMPLATE. The town page's stat band ("proof")
# and its header chip row (".badges") merged into #why-the-trip, so both
# entries left: a list naming what no town page carries would excuse text
# the template no longer ships. What ships is listed; what died, died.
# 3.81, GREG'S OPTION C: THE GATE STOPS COUNTING FIXED LAYOUT AND DERIVED
# DIRECTIONS. Each exclusion and its reason:
#   #fix          What we fix: the same four cards and one sentence on every
#                 town page, layout, not copy.
#   .map-credit   the ODbL credit under every map, required and identical.
#   .dir-utils    the getaway kit: Open in Google Maps, the chip, the address.
#   .numbered     the numbered steps, and
#   the intro     the first paragraph of the directions card's prose ("From
#                 the crossroads of ...").
# The last two are DERIVED DATA, policed word for word by the routing check
# (town_route_findings), and two towns that arrive on the same roads will
# rightly share them: every route ends on 2nd Street Pike or James Way into
# Jaymor Rd. Counting them would force filler written only to dilute a
# metric, which is the doorway-page disease inverted. THE HEADER, THE
# OPENINGS AND THE FAQS STAY COUNTED: option D, which excluded the header,
# was put to Greg and declined, because it would reverse 3.71's
# first-sentence pressure. A Jamison-style alternative-route paragraph in
# the card is prose, not derived, and stays counted too.
TOWN_PATTERN_SECTIONS = ("start", "nearby", "real-repairs", "why-the-trip", "fix")
TOWN_PATTERN_CLASSES = ("svc-card", "map-credit", "dir-utils", "numbered")
# The card's intro line has no class of its own, and giving it one would
# change shipped markup to suit a metric; it is found by position instead:
# the first <p> directly inside the .prose of a .dir-body.
TOWN_PATTERN_INTRO = ("dir-body", "prose")
TOWN_SHINGLE = 3
TOWN_SHARED_MAX = 0.30
TOWN_PLACE_NAMES = (
    "feasterville-trevose", "feasterville", "trevose", "huntingdon valley",
    "northeast philadelphia", "willow grove", "bryn athyn", "bensalem",
    "hatboro", "horsham", "jamison", "jenkintown", "langhorne", "richboro",
    "warminster", "ivyland", "churchville", "holland", "newtown",
    "northampton", "southampton", "warwick", "warrington", "hartsville",
    "philadelphia", "bucks", "montgomery",
)
_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
         "meta", "source", "track", "wbr"}


class _TownText(HTMLParser):
    """The substantive text and H2s inside <main>, pattern text left out."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []           # [tag, skipping, classes, first <p> seen] per open element
        self.main = 0
        self.words = []
        self.h2s = []
        self._h2 = None

    def _skipping(self):
        return bool(self.stack) and self.stack[-1][1]

    def _is_card_intro(self, tag):
        """The directions card's intro line: a <p> whose parent is the
        .prose of a .dir-body, and the first <p> that .prose opens (3.81)."""
        if tag != "p" or len(self.stack) < 2:
            return False
        parent, grand = self.stack[-1], self.stack[-2]
        outer, inner = TOWN_PATTERN_INTRO
        if inner not in parent[2] or outer not in grand[2]:
            return False
        if parent[3]:
            return False
        parent[3] = True          # this .prose has opened its first <p>
        return True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.main += 1
        if tag in _VOID:
            return
        classes = (a.get("class") or "").split()
        skip = (self._skipping() or tag in ("nav", "script", "style")
                or (tag == "section" and a.get("id") in TOWN_PATTERN_SECTIONS)
                or any(c in TOWN_PATTERN_CLASSES for c in classes)
                or self._is_card_intro(tag))
        self.stack.append([tag, skip, classes, False])
        if tag == "h2" and not skip:
            self._h2 = ""

    def handle_endtag(self, tag):
        if tag == "main" and self.main:
            self.main -= 1
        if tag == "h2" and self._h2 is not None:
            # An empty H2 is the empty-heading check's critical, not a
            # heading two pages can share.
            if self._h2.strip():
                self.h2s.append(" ".join(self._h2.split()))
            self._h2 = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self.main or self._skipping():
            return
        self.words.append(data)
        if self._h2 is not None:
            self._h2 += data


def town_place_mask(text: str, own: tuple = ()) -> list:
    """Lowercased words with every place name, and the page's own town,
    reduced to one token, so a renamed copy reads as a copy."""
    t = text.lower().replace("’", "'")
    for name in sorted(set(TOWN_PLACE_NAMES) | set(own), key=len, reverse=True):
        t = re.sub(r"\b" + re.escape(name) + r"\b", " zzplace ", t)
    return re.findall(r"[a-z0-9']+", t)


def town_shingles(html_text: str, own: tuple = ()) -> tuple:
    p = _TownText()
    p.feed(html_text)
    w = town_place_mask(" ".join(p.words), own)
    grams = {" ".join(w[i:i + TOWN_SHINGLE]) for i in range(len(w) - TOWN_SHINGLE + 1)}
    return grams, p.h2s


def town_variance_findings(pages: dict) -> dict:
    """pages is {label: (html, own_names)}. Every pair is compared, the hub
    included when it is among them. Returns the shared substantive H2s and
    every pair's shared-phrase figure."""
    data = {k: town_shingles(h, own) for k, (h, own) in pages.items()}
    shared_h2, pairs = [], []
    keys = sorted(data)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            ga, ha = data[a]
            gb, hb = data[b]
            common = {x.lower() for x in ha} & {x.lower() for x in hb}
            shared_h2 += [(a, b, h) for h in sorted(common)]
            small = min(len(ga), len(gb))
            pairs.append((a, b, len(ga & gb) / small if small else 1.0))
    return {"shared_h2": shared_h2, "pairs": pairs}


def own_town_names(path: str) -> tuple:
    """The town a town page is about, read off its slug:
    areas-served-collision-repair-jamison-pa -> ("jamison",)."""
    slug = os.path.basename(os.path.dirname(path))
    m = re.match(r"areas-served-collision-repair-(.+?)(?:-pa)?$", slug)
    return (m.group(1).replace("-", " "),) if m else ()


def check_town_variance_local(passes: list, warns: list, fails: list, notes: list,
                              root: str = None):
    """Rule 7's variance, measured across every declared town page and the
    hub. A shared substantive H2 and a pair over the ceiling are criticals:
    this is the gate that stops the second town page shipping as a copy of
    the first."""
    root = root or SITE_DIR
    towns = {}
    for dirpath, _dirs, files in os.walk(root):
        if "index.html" not in files:
            continue
        path = os.path.join(dirpath, "index.html")
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        m = re.search(r'<meta name="tri-county-page" content="([^"]*)"', raw)
        if m and m.group(1).strip().lower() == TOWN_KIND:
            towns[os.path.relpath(path, root)] = (raw, own_town_names(path))
    hub = os.path.join(root, TOWN_HUB_PATH)
    compared = dict(towns)
    if os.path.isfile(hub):
        with open(hub, encoding="utf-8") as f:
            compared[TOWN_HUB_PATH] = (f.read(), ())
    if len(compared) < 2:
        notes.append(
            f"**Town variance: {len(towns)} town page{'' if len(towns) == 1 else 's'}"
            f"{', no hub yet' if not os.path.isfile(hub) else ''}, so nothing to compare.** "
            f"The gate arms the day a second town page or the hub lands: no shared "
            f"substantive H2, and under {TOWN_SHARED_MAX:.0%} shared three-word phrases "
            f"between any two (proposed-changes.md 3.62).")
        return
    found = town_variance_findings(compared)
    for a, b, h in found["shared_h2"]:
        fails.append(f"**Town pages share a substantive H2:** `{a}` and `{b}` both carry "
                     f"“{h}”. Rule 7 forbids it; give each section its own heading.")
    over = [(a, b, r) for a, b, r in found["pairs"] if r >= TOWN_SHARED_MAX]
    for a, b, r in over:
        fails.append(f"**Town pages read as copies:** `{a}` and `{b}` share {r:.0%} of their "
                     f"three-word phrases, place names masked, against a ceiling under "
                     f"{TOWN_SHARED_MAX:.0%}. Rewrite one of them; the doctrine calls a page "
                     f"like this a doorway.")
    if not found["shared_h2"] and not over:
        worst = max(r for _a, _b, r in found["pairs"])
        passes.append(f"Town variance holds across {len(compared)} pages: no shared substantive "
                      f"H2, and the closest pair shares {worst:.0%} of its three-word phrases "
                      f"(ceiling under {TOWN_SHARED_MAX:.0%}).")


# --- The site chrome, 3.83 --------------------------------------------
# The header and the footer are written by scripts/sync-chrome.py. Two
# checks hold them, across every real page:
#
#   IDENTITY. The chrome is the same on every page, compared with every
#   href and src resolved to the site path it lands on and the current-page
#   marking set aside. The marking is the ONE permitted difference, and it
#   is itself checked: a chrome link that lands on the page it sits on
#   carries aria-current="page", and no other link does.
#
#   RESOLUTION. Every chrome link lands on a real page under docs/ (not a
#   redirect stub), or is the shop's own phone or mailbox, or is one of
#   CHROME_EXTERNAL_URLS character for character.
#
# A redirect stub stays bare: chrome on a stub is a failure too.
CHROME_HEAD_RE = re.compile(r'(?s)<header class="nav">.*?</header>')
CHROME_FOOT_RE = re.compile(r'(?s)<footer class="site">.*?</footer>')
CHROME_TEL = "tel:+12153225350"
CHROME_MAILTO = "mailto:contact@tricountycollision.com"


def _chrome_page_url(rel_path: str) -> str:
    d = os.path.dirname(rel_path).replace(os.sep, "/")
    return "/" if d in ("", ".") else f"/{d}/"


def chrome_findings(pages: dict) -> dict:
    """pages maps a docs-relative path ("index.html", "blog/index.html") to
    its HTML. Returns {"missing": [...], "marking": [...], "differs": [...],
    "links": [...], "stub_chrome": [...], "forms": int}."""
    from urllib.parse import urljoin
    from html import escape as _esc
    out = {"missing": [], "marking": [], "differs": [], "links": [], "stub_chrome": [], "forms": 0}
    real = {}
    for rel, raw in pages.items():
        if REFRESH_RE.search(raw):
            if CHROME_HEAD_RE.search(raw) or CHROME_FOOT_RE.search(raw) or 'class="nav"' in raw:
                out["stub_chrome"].append(rel)
            continue
        real[rel] = raw
    live = {_chrome_page_url(r) for r in real}
    forms = {}
    for rel, raw in sorted(real.items()):
        h, f = CHROME_HEAD_RE.findall(raw), CHROME_FOOT_RE.findall(raw)
        if len(h) != 1 or len(f) != 1:
            out["missing"].append(rel)
            continue
        here = _chrome_page_url(rel)
        chrome = re.sub(r"(?s)<!--.*?-->", "", h[0] + f[0])
        for m in re.finditer(r"<a\b[^>]*>", chrome):
            tag = m.group(0)
            hm = re.search(r'\bhref="([^"]*)"', tag)
            href = unescape(hm.group(1)) if hm else ""
            current = 'aria-current="page"' in tag
            if href.startswith(("http://", "https://")):
                if href not in CHROME_EXTERNAL_URLS:
                    out["links"].append((rel, href))
                if current:
                    out["marking"].append((rel, href, "an external link marked as the current page"))
                continue
            if href in (CHROME_TEL, CHROME_MAILTO):
                continue
            if not href or href.startswith(("#", "javascript:", "tel:", "mailto:")):
                out["links"].append((rel, href or "(no href)"))
                continue
            target = urljoin(here, href)
            if target not in live:
                out["links"].append((rel, href))
            if (target == here) != current:
                out["marking"].append((rel, href, "lands on this page without aria-current" if not current
                                       else "carries aria-current but lands elsewhere"))

        def norm_attr(m):
            v = unescape(m.group(2))
            if not v.startswith(("http://", "https://", "tel:", "mailto:", "#")):
                v = urljoin(here, v)
            return f'{m.group(1)}="{_esc(v, quote=True)}"'
        norm = re.sub(r'\b(href|src)="([^"]*)"', norm_attr, chrome)
        norm = re.sub(r'\s+aria-current="page"', "", norm)
        norm = re.sub(r"\s+", " ", norm).strip()
        forms.setdefault(norm, []).append(rel)
    out["forms"] = len(forms)
    if len(forms) > 1:
        major = max(forms.values(), key=len)
        for pgs in forms.values():
            if pgs is not major:
                out["differs"].extend(pgs)
    return out


def check_chrome_local(passes: list, fails: list, root: str = None):
    root = root or SITE_DIR
    pages = {}
    for dirpath, _dirs, files in os.walk(root):
        if "index.html" in files:
            path = os.path.join(dirpath, "index.html")
            with open(path, encoding="utf-8") as f:
                pages[os.path.relpath(path, root)] = f.read()
    if not pages:
        return
    found = chrome_findings(pages)
    for rel in found["missing"]:
        fails.append(f"**`{rel}` carries no site chrome,** or more than one header or footer. "
                     f"Run `scripts/sync-chrome.py` (proposed-changes.md 3.83).")
    for rel in found["differs"]:
        fails.append(f"**`{rel}`'s header or footer differs from every other page's.** The chrome "
                     f"is identical on every page but for the current-page marking; run "
                     f"`scripts/sync-chrome.py` rather than editing a page's chrome by hand.")
    for rel, href, why in found["marking"]:
        fails.append(f"**`{rel}`: the chrome link `{href}` {why}.** The current page is the one "
                     f"thing the chrome may mark, and it must mark it exactly.")
    for rel, href in found["links"]:
        fails.append(f"**`{rel}`: the chrome link `{href}` lands nowhere real.** Every nav and "
                     f"footer link must reach a page under docs/ or a recorded URL "
                     f"(`CHROME_EXTERNAL_URLS`), character for character.")
    for rel in found["stub_chrome"]:
        fails.append(f"**`{rel}` is a redirect stub carrying site chrome.** A stub stays bare.")
    if not any(found[k] for k in ("missing", "differs", "marking", "links", "stub_chrome")):
        n = sum(1 for r in pages.values() if not REFRESH_RE.search(r))
        passes.append(f"The site chrome is identical on all {n} pages but for the current-page "
                      f"marking, which is exact, and every nav and footer link lands on a real "
                      f"page or a recorded URL.")


class _CardGroups(HTMLParser):
    """Every service card inside <main>, grouped by the element that holds
    it. A card is anything whose class names svc-card and whose href or
    data-pending-href lands on a service page. Each card's first h3 and
    first p are read too, so its words answer to SERVICES (3.90)."""
    VOID = {"img", "br", "hr", "input", "meta", "link", "source", "wbr", "area", "col", "embed", "track"}

    def __init__(self, page_rel: str):
        super().__init__(convert_charrefs=True)
        self.page_rel, self.stack, self.n, self.inmain = page_rel, [], 0, False
        self.groups = {}
        self.cards = []          # [target, h3 text, p text]
        self.card_depth = None   # stack depth of the open card
        self.field = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.inmain = True
        cls = (a.get("class") or "").split()
        href = a.get("href") if a.get("href") is not None else a.get("data-pending-href")
        if self.inmain and "svc-card" in cls and href is not None and self.stack:
            target = self.page_rel if href == "./" else \
                posixpath.normpath(posixpath.join("/" + self.page_rel, href)).strip("/") + "/"
            if target in SERVICE_PATHS:
                parent = self.stack[-1]
                self.groups.setdefault(parent, []).append(target)
                self.cards.append([target, None, None])
                self.card_depth = len(self.stack)
        if self.card_depth is not None and tag in ("h3", "p"):
            i = 1 if tag == "h3" else 2
            if self.cards[-1][i] is None:
                self.cards[-1][i] = ""
                self.field = i
        if tag not in self.VOID:
            self.n += 1
            self.stack.append((self.n, tag, a.get("id") or "", " ".join(cls)))

    def handle_data(self, data):
        if self.field is not None:
            self.cards[-1][self.field] += data

    def handle_endtag(self, tag):
        if tag == "main":
            self.inmain = False
        if tag in ("h3", "p"):
            self.field = None
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][1] == tag:
                del self.stack[k:]
                if self.card_depth is not None and k <= self.card_depth:
                    self.card_depth = None
                break


def _main_text_units(html_text: str) -> list:
    """<main>'s visible text one block at a time, so a heading or a list
    item never runs into its neighbour and forms a sentence nobody wrote."""
    m = re.search(r"(?is)<main\b[^>]*>(.*)</main>", html_text)
    body = m.group(1) if m else ""
    body = re.sub(r"(?s)<!--.*?-->", " ", body)
    body = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1\s*>", " ", body)
    body = re.sub(r"(?i)</?(p|li|h[1-6]|summary|figcaption|td|th|dt|dd|div|section|article|ul|ol|a)\b[^>]*>", "\n", body)
    out = []
    for block in visible_text_blocks(body):
        out += [s for s in re.split(r"(?<=[.!?])\s+", block) if s]
    return out


def visible_text_blocks(body: str) -> list:
    return [re.sub(r"\s+", " ", unescape(re.sub(r"(?s)<[^>]+>", " ", b))).strip()
            for b in body.split("\n") if re.sub(r"(?s)<[^>]+>", "", b).strip()]


def service_enumeration_findings(html_text: str, page_rel: str, meta: str = "") -> tuple:
    """(enumerations found, problems). Three shapes, each held to the full
    family in SERVICES (3.87): a group of service cards under one parent,
    a count typed beside "services", and one sentence naming all but one of
    the family or more, in words. The chrome is not read here; check_chrome_local
    holds it, and it is generated from the same list."""
    found, problems = 0, []
    want = len(SERVICES)
    p = _CardGroups(page_rel)
    p.feed(html_text)
    # A SERVICE PAGE'S OWN GRID IS ITS RELATED SERVICES: the family minus
    # itself (3.90) minus RELATED_LEAVES_OUT (3.91). Anywhere else a grid is
    # the whole family.
    on_service = page_rel in SERVICE_PATHS
    expect = [x for x in SERVICE_PATHS
              if not on_service or (x != page_rel and x not in RELATED_LEAVES_OUT)]
    label = {x: lbl for x, lbl, _ln in SERVICES}
    for (_n, tag, gid, gcls), targets in p.groups.items():
        if len(set(targets)) < 2:
            continue
        found += 1
        missing = [label[x] for x in expect if x not in targets]
        where = f"<{tag}{' id=' + gid if gid else ''}{' class=' + gcls if gcls else ''}>"
        if missing:
            problems.append(f"the service cards in {where} lack {', '.join(missing)}")
        if page_rel in targets:
            problems.append(f"the service cards in {where} carry {label[page_rel]}, the page they sit on; "
                            f"a service page's grid is the family minus itself")
        left_out = [label[x] for x in RELATED_LEAVES_OUT if on_service and x != page_rel and x in targets]
        if left_out:
            problems.append(f"the service cards in {where} carry {', '.join(left_out)}, which the Related "
                            f"Services list leaves out (RELATED_LEAVES_OUT, 3.91)")
        dup = sorted({x for x in targets if targets.count(x) > 1})
        if dup:
            problems.append(f"the service cards in {where} repeat {', '.join(dup)}")
    # EVERY CARD SAYS WHAT ITS ROW SAYS, 3.90: one rendering per service.
    for target, h3, para in p.cards:
        row = next(r for r in SERVICES if r[0] == target)
        got = (" ".join((h3 or "").split()), " ".join((para or "").split()))
        if got != (row[1], row[2]):
            problems.append(f"the card for {target} reads \u201c{got[0]}\u201d / \u201c{got[1]}\u201d; "
                            f"SERVICES says \u201c{row[1]}\u201d / \u201c{row[2]}\u201d")
    units = _main_text_units(html_text) + ([meta] if meta else [])
    for u in units:
        for m in SERVICE_COUNT_RE.finditer(u):
            found += 1
            w = m.group(1).lower()
            n = int(w) if w.isdigit() else COUNT_WORDS.index(w)
            if n != want:
                problems.append(f"\u201c{m.group(0)}\u201d counts {n} services; the family is {COUNT_WORDS[want]}")
        s = u.replace("Tri-County Collision", "")
        named = [path for path, rx in SERVICE_TEXT_RE.items() if rx.search(s)]
        if len(named) >= len(SERVICES) - 1:
            found += 1
            missing = [lbl for path, lbl, _ln in SERVICES if path not in named]
            if missing:
                problems.append(f"\u201c{u[:110]}\u201d names {len(named)} services in words and not "
                                f"{', '.join(missing)}")
    return found, problems


# A HOME SERVICE CARD PREVIEWS ITS PAGE, 3.93, Greg's ruling, refined on
# the relay the same day. A card that carries a photograph carries THE
# IMAGE ITS TARGET PAGE PRESENTS AS ITS OWN PREVIEW: the page's og:image,
# with og:image:width, og:image:height and og:image:alt, verbatim. That is
# the hero everywhere except where a page deliberately carries a clean
# preview crop (Commercial's, 3.92c), and that exception is the point: the
# redaction block ruled out of link previews stays off the home router too.
# One rule, no per-card forks. scripts/sync-service-cards.py writes it from
# preview_of(); this holds it. A card with no image (the towns', Related
# Services) is not read.
_ATTR_RE = re.compile(r'([a-zA-Z-]+)="([^"]*)"')
_OG_RE = re.compile(r'<meta property="og:image(|:width|:height|:alt)" content="([^"]*)">')
_CARD_IMG_RE = re.compile(r'(?s)<a class="svc-card" href="([^"]+)">\s*(<img\b[^>]*>)')


def preview_of(page_rel: str, site_dir: str = None):
    """A page's own preview image, from its og:image tags, as {src
    (docs-relative), alt (raw, as written), width, height}, or None if the
    page carries no og:image."""
    path = os.path.join(site_dir or SITE_DIR, page_rel, "index.html")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return None
    og = dict(_OG_RE.findall(text))
    if not og.get(""):
        return None
    src = urllib.parse.urlparse(og[""]).path.lstrip("/")
    return {"src": src, "alt": og.get(":alt"), "width": og.get(":width"), "height": og.get(":height")}


def card_image_findings(html_text: str, page_rel: str, site_dir: str = None) -> tuple:
    """(cards with an image, problems). Every such card's image must be its
    target service page's own preview: file, width, height and alt."""
    m = re.search(r"(?s)<main\b.*?</main>", html_text)
    n, problems = 0, []
    for href, tag in _CARD_IMG_RE.findall(m.group(0) if m else ""):
        target = posixpath.normpath(posixpath.join("/" + page_rel, href)).strip("/") + "/"
        if target not in SERVICE_PATHS:
            continue
        n += 1
        want = preview_of(target, site_dir)
        if want is None:
            problems.append(f"the card for {target} carries an image, and {target} has no og:image to preview")
            continue
        a = dict(_ATTR_RE.findall(tag))
        src = posixpath.normpath(posixpath.join("/" + page_rel, a.get("src", ""))).lstrip("/")
        for k, got, exp in (("image", src, want["src"]), ("alt", a.get("alt"), want["alt"]),
                            ("width", a.get("width"), want["width"]), ("height", a.get("height"), want["height"])):
            if got != exp:
                problems.append(f"the card for {target} has {k} \u201c{got}\u201d; its page's og:image has "
                                f"\u201c{exp}\u201d")
    return n, problems


def check_service_count_llms_local(passes: list, fails: list, root: str = None):
    """llms.txt tells AI agents how many services a page shows. The count
    word answers to the family, the same as on a page (3.87)."""
    path = os.path.join(root or SITE_DIR, "llms.txt")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return
    text = re.sub(r"\s+", " ", text)
    bad, n = [], 0
    for m in SERVICE_COUNT_RE.finditer(text):
        n += 1
        w = m.group(1).lower()
        if (int(w) if w.isdigit() else COUNT_WORDS.index(w)) != len(SERVICES):
            bad.append(m.group(0))
    for x in sorted(set(bad)):
        fails.append(f"**`llms.txt` says \u201c{x}\u201d {bad.count(x)} time(s); the family in SERVICES is "
                     f"{COUNT_WORDS[len(SERVICES)]}.** Derive the word from the list (3.87).")
    if n and not bad:
        passes.append(f"`llms.txt` counts the services as the family does, {COUNT_WORDS[len(SERVICES)]}, "
                      f"in all {n} mentions.")


def check_hours_llms_local(passes: list, fails: list):
    """docs/llms.txt states the hours to AI agents, so it answers to the
    same constants as every page. Same test, same severity."""
    try:
        with open(LLMS_PATH, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return
    n_ok, strays, sundays = hours_findings(text)
    for x in strays:
        fails.append(f"**`{LLMS_PATH}` writes the hours a second way:** \u201c{x}\u201d. "
                     f"It must say `{HOURS_WEEKDAYS}` and `{HOURS_SATURDAY}` exactly.")
    for x in sundays:
        fails.append(f"**`{LLMS_PATH}` mentions Sunday:** \u201c{x}\u201d. The record has "
                     f"no Sunday hours.")
    if n_ok and not strays and not sundays:
        passes.append(f"`{LLMS_PATH}` states the hours exactly as the constants do.")


def check_review_count_local(passes: list, warns: list, fails: list,
                             notes: list, today: date = None):
    """THE REVIEW COUNT, ENFORCED RATHER THAN REMEMBERED.

    Two failures, and they are different in kind:

    DISAGREEMENT IS A CRITICAL. Two different review counts on one site
    is one of them being wrong, and a visitor cannot tell which. The
    recorded REVIEW_COUNT counts as one of the instances, so a page that
    drifts from the constant fails even when it is the only page saying
    anything.

    AGE IS A WARNING. Past REVIEW_STALE_DAYS the number is not known to be
    wrong, it is only no longer known to be right, and the fix is to read
    the profile again rather than to edit the page.

    Local runs only. It reads files under docs/, and on a live run the
    target is the shop's WordPress site, where these files are not what
    is being audited.
    """
    today = today or date.today()
    hits = find_review_counts()

    counts = {}
    for path, n, snip in hits:
        counts.setdefault(n, []).append((path, snip))

    try:
        counted_on = date.fromisoformat(REVIEW_COUNTED_ON)
    except ValueError:
        fails.append(f"**`REVIEW_COUNTED_ON` is not a date** (`{REVIEW_COUNTED_ON}`). "
                     "It has to be ISO `YYYY-MM-DD`, because the staleness check "
                     "subtracts it from today.")
        return

    seen = dict(counts)
    seen.setdefault(REVIEW_COUNT, []).append(("scripts/audit.py", f"REVIEW_COUNT = {REVIEW_COUNT}"))
    distinct = sorted(seen)

    if len(distinct) > 1:
        where = "; ".join(
            f"**{n}** in " + ", ".join(sorted({f"`{pth}`" for pth, _ in seen[n]}))
            for n in distinct)
        fails.append(
            f"**The site states {len(distinct)} different review counts: {where}.** "
            "One business has one review count, and a visitor who spots two has no way "
            "to tell which is the real one. Read the Google Business Profile, then "
            "update `REVIEW_COUNT`, `REVIEW_COUNTED_ON` and every page in one commit.")
    elif not hits:
        notes.append(
            f"**No page states a review count.** `REVIEW_COUNT` is {REVIEW_COUNT}, recorded "
            f"{REVIEW_COUNTED_ON}, and nothing publishes it yet. Nothing to disagree.")

    age = (today - counted_on).days
    if age < 0:
        warns.append(
            f"**`REVIEW_COUNTED_ON` is in the future** ({REVIEW_COUNTED_ON}, {-age} day"
            f"{'' if -age == 1 else 's'} from now). One of the date and the clock is wrong.")
    elif age > REVIEW_STALE_DAYS:
        warns.append(
            f"**The review count is {age} days old.** {REVIEW_COUNT} reviews and "
            f"{REVIEW_RATING} stars were counted on {REVIEW_COUNTED_ON}, and anything past "
            f"{REVIEW_STALE_DAYS} days is a guess rather than a reading. Open the Google "
            "Business Profile, read the current count, and update the constants and the "
            "pages together. This is a warning, not a critical: the number is not known "
            "to be wrong, it is no longer known to be right.")
    elif hits:
        notes.append(
            f"**Review count agrees everywhere and is {age} day{'' if age == 1 else 's'} old.** "
            f"{REVIEW_COUNT} reviews and {REVIEW_RATING} stars, counted {REVIEW_COUNTED_ON}, "
            f"stated identically in {len(hits)} place{'' if len(hits) == 1 else 's'} under "
            f"`{SITE_DIR}/`. Visible text only: there is no review or rating markup on this "
            "site, deliberately.")


def read_asset_provenance(path: str) -> dict:
    """What one image file says about where it came from.

    Returns the DigitalSourceType, the CreatorTool and whether a C2PA
    manifest is referenced, plus a verdict. A C2PA manifest on its own
    is not a tell: legitimate stock carries one too, and it is the
    assertion inside the label that matters, not the presence of a
    label.

    The whole file is scanned as latin-1 rather than only its metadata
    segments. Parsing JPEG APP markers, PNG chunks, WebP RIFF and AVIF
    boxes correctly is four parsers and a dependency, and the strings
    being matched are long enough that compressed pixel data producing
    one by chance is not a thing that happens. The failure direction is
    also the safe one: a false positive stops a build and gets read by
    a person, a false negative ships an AI asset.
    """
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("latin-1", "replace")

    source_type = ""
    for m in SOURCE_TYPE_RE.finditer(text):
        val = m.group(1).strip()
        if val:
            source_type = val
            if val.lower() in AI_SOURCE_TYPES:
                break

    tool = ""
    for m in CREATOR_TOOL_RE.finditer(text):
        val = m.group(1).strip()
        if val:
            tool = val
            if AI_TOOL_RE.search(val):
                break

    reasons = []
    if source_type.lower() in AI_SOURCE_TYPES:
        reasons.append(f"IPTC DigitalSourceType is `{source_type}`")
    if tool and AI_TOOL_RE.search(tool):
        reasons.append(f"CreatorTool is `{tool}`")
    # A generator named anywhere else in the metadata counts too. The
    # side-view candidate hid in the tool field; the next one may not.
    if not reasons:
        loose = AI_TOOL_RE.search(text)
        if loose:
            reasons.append(f"the file carries the string `{loose.group(0)}`")

    return {
        "path": path,
        "bytes": len(raw),
        "source_type": source_type,
        "tool": tool,
        "c2pa": "cai-manifests.adobe.com" in text or "c2pa" in text.lower(),
        "reasons": reasons,
    }


def find_assets(root: str = None) -> list:
    """Every raster image under docs/, with its provenance read.

    SITE_DIR is resolved when this is CALLED and not when it is
    defined, because a default argument binds once at import and the
    tests point the check at a temporary directory.
    """
    root = root or SITE_DIR
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if name.lower().endswith(ASSET_EXTS):
                try:
                    out.append(read_asset_provenance(os.path.join(dirpath, name)))
                except OSError:
                    continue
    return sorted(out, key=lambda a: a["path"])


def check_asset_provenance_local(passes: list, warns: list, fails: list,
                                 notes: list):
    """AN AI-GENERATED IMAGE IS A CRITICAL, not a warning.

    Rule 9 bans AI imagery outright, and the client reaffirmed it on
    2026-09-17 against two assets he had already licensed, so the
    threshold here is not a judgement call this script gets to make.
    It is also the cheapest possible thing to get wrong: the metadata
    that gives an asset away is invisible in every image viewer, a
    C2PA manifest is readable by anyone who opens the published file,
    and the shop's own argument is that real beats stock.

    Local runs only, like the rest of these. On a live run the target
    is the WordPress site and there are no files to read.
    """
    assets = find_assets()
    if not assets:
        notes.append(
            f"**No raster images under `{SITE_DIR}/`.** Nothing to check yet. Every "
            "licensed asset gets its metadata read before it lands, and this is what "
            "reads it.")
        return

    bad = [a for a in assets if a["reasons"]]
    if bad:
        for a in bad:
            fails.append(
                f"**`{a['path']}` is AI-generated: " + "; ".join(a["reasons"]) + ".** "
                "Rule 9 allows no AI imagery, reaffirmed 2026-09-17. Do not strip the "
                "label to make it pass: the provenance is the fact, the label is only "
                "where it is written down, and removing it is a lie about the asset "
                "plus a licence breach. Replace the file with one whose source is a "
                "camera or a person at a workstation.")

    clean = [a for a in assets if not a["reasons"]]
    if clean:
        labelled = [a for a in clean if a["source_type"]]
        detail = ""
        if labelled:
            kinds = sorted({a["source_type"] for a in labelled})
            detail = (f" {len(labelled)} carr{'ies' if len(labelled) == 1 else 'y'} an "
                      f"explicit source type ({', '.join(kinds)}).")
        passes.append(
            f"No AI-generation marker on {len(clean)} of {len(assets)} image"
            f"{'' if len(assets) == 1 else 's'} under `{SITE_DIR}/`.{detail}")

    notes.append(
        "**What the asset check can and cannot do.** It reads the labels a file carries: "
        "the IPTC `DigitalSourceType`, the XMP `CreatorTool`, and any generator named "
        "elsewhere in the metadata. It cannot read pixels, so an AI image whose metadata "
        "was stripped passes it. Treat a clean result as 'the file makes no AI claim', "
        "not as 'a person made this'. The judgement at purchase time is still the "
        "control that matters, and this is the floor under it.")


# --- The FAQ standalone test, as a check, 3.94 ---------------------------
# The standards' FAQ law: every answer's opening sentence must survive being
# lifted without its question, because that is exactly what an assistant
# does with it. The pre-launch sweep found 27 town answers opening "No.",
# "It can.", "A little." and the like, none of which says anything alone.
# An opener FAILS when it:
#   - is under FAQ_OPENER_MIN_WORDS words ("No.", "Horsham has none.");
#   - opens on a pronoun whose antecedent is in the question ("It does:
#     windshields...", "This page times the drive...");
#   - opens on a comparative fragment ("Longer than the figure...",
#     "Nearly.", "Not quite.", "A little.").
# A bare particle comma- or colon-merged into a full sentence passes ("No,
# PDR will not damage your paint."), which is what the standards prescribe.
FAQ_OPENER_MIN_WORDS = 6
FAQ_OPENER_PRONOUN_RE = re.compile(r"^(?:it|they|this|that|these|those)\b", re.I)
FAQ_OPENER_FRAGMENT_RE = re.compile(
    r"^(?:longer|shorter|nearly|mostly|partly|not quite|a little|somewhat)\b", re.I)


def faq_opener(answer: str) -> str:
    """The answer's first sentence, as an assistant would lift it."""
    return re.split(r"(?<=[.!?])\s+", unescape(re.sub(r"<[^>]+>", "", answer)).strip(), maxsplit=1)[0]


def faq_opener_findings(qas) -> list:
    """[(question, opener, why)] for every answer whose opener fails."""
    bad = []
    for q, a in qas:
        first = faq_opener(a)
        n = len(re.findall(r"[\w\u2019'-]+", first))
        if n < FAQ_OPENER_MIN_WORDS:
            bad.append((q, first, f"{n} word{'' if n == 1 else 's'}"))
        elif FAQ_OPENER_PRONOUN_RE.match(first):
            bad.append((q, first, "it opens on a pronoun"))
        elif FAQ_OPENER_FRAGMENT_RE.match(first):
            bad.append((q, first, "it opens on a fragment"))
    return bad


def audit(source: str, coverage: dict = None):
    """Scores one page. `coverage` carries the parsed sitemap.xml and
    llms.txt for local runs, so a page that was built but never published
    into either file gets caught here rather than by a customer."""
    html = load(source)
    p = PageParser()
    p.feed(html)

    # A redirect stub or the 404 page declares itself in the head and is
    # scored against its own short rubric instead of this one. See
    # SPECIAL_KINDS at the top of the file for why.
    kind = (p.meta.get("tri-county-page") or "").strip().lower()
    if kind in SPECIAL_KINDS:
        return special_audit(source, html, p, kind, coverage) + (kind,)
    # A declared execution kind keeps this whole rubric and loses only the
    # checks RUBRIC_EXEMPTIONS names for it. It still reports as a page.
    exempt = RUBRIC_EXEMPTIONS.get(kind, ())
    exempt_why = {
        "contact": (f"Declared `tri-county-page` kind `contact`, an execution page: "
                    f"exempt by Greg's ruling of 2026-09-24, proposed-changes.md 3.53."),
        "post": (f"Declared `tri-county-page` kind `post`: a post is a read, not an "
                 f"answer block. Exempt by Greg's ruling of 2026-09-25, "
                 f"proposed-changes.md 3.57."),
        "blog-index": (f"Declared `tri-county-page` kind `blog-index`: an index routes, "
                       f"it does not answer. Exempt by Greg's ruling of 2026-09-25, "
                       f"proposed-changes.md 3.57."),
    }.get(kind, "")
    declared_kind = kind
    kind = "page"

    passes, warns, fails, notes = [], [], [], []

    # --- Title tag ---
    t = p.title.strip()
    if not t:
        fails.append("**Missing <title> tag.** This is the strongest on-page ranking signal. Add one: `Business | Service | Town, ST`.")
    elif len(t) > 60:
        warns.append(f"**Title is {len(t)} characters** (aim for ≤60 so Google doesn't cut it off): “{t}”")
    else:
        passes.append(f"Title tag present and a good length ({len(t)} chars): “{t}”")

    # --- Meta description ---
    d = p.meta.get("description", "").strip()
    if not d:
        fails.append("**Missing meta description.** It's your free ad copy on the Google results page. Add one under 160 characters with a clear offer.")
    elif len(d) > 160:
        warns.append(f"**Meta description is {len(d)} characters** (aim for ≤160): “{d[:80]}…”")
    else:
        passes.append(f"Meta description present and a good length ({len(d)} chars).")

    # --- H1 ---
    h1s = [h.strip() for h in p.h1s if h.strip()]
    if len(h1s) == 0:
        fails.append("**No H1 heading.** Every page needs exactly one H1 containing the main service + location.")
    elif len(h1s) > 1:
        warns.append(f"**{len(h1s)} H1 headings found.** Use exactly one; demote the rest to H2.")
    else:
        passes.append(f"Exactly one H1: “{h1s[0][:80]}”")

    # --- Empty headings (3.60) ---
    empty = [(tag, line) for tag, line, text in p.headings if not text.strip()]
    if empty:
        where = ", ".join(f"<{tag}> on line {line}" for tag, line in empty)
        fails.append(f"**Empty heading: {where}.** A heading with no words is announced by a "
                     f"screen reader as a heading with no name, and nobody sees it by eye. "
                     f"Delete the element; do not fill it with filler.")
    else:
        passes.append(f"No empty headings: all {len(p.headings)} h1 to h6 carry words.")

    # --- Every service enumeration carries the whole family, in its words (3.87, 3.90) ---
    if not is_url(source):
        _rel = os.path.relpath(os.path.dirname(os.path.abspath(source)),
                               os.path.abspath(SITE_DIR)).replace(os.sep, "/")
        _rel = "" if _rel == "." or _rel.startswith("..") else _rel + "/"
        n_enum, enum_problems = service_enumeration_findings(html, _rel, d)
        for x in enum_problems:
            fails.append(f"**A service enumeration does not answer to SERVICES:** {x}. Every place the "
                         f"site lists its services carries all {len(SERVICES)} in SERVICES (a service "
                         f"page's own grid, the family minus itself and RELATED_LEAVES_OUT), and every card carries its row's "
                         f"label and line, so a service cannot be half-added and a card cannot drift "
                         f"(3.87, 3.90, 3.91). Run scripts/sync-service-cards.py.")
        if n_enum and not enum_problems:
            passes.append(f"All {n_enum} service enumeration(s) on the page carry the family of "
                          f"{len(SERVICES)}, and every card its row's label and line.")

    # --- A home service card's image is its page's own preview, 3.93 ---
    if not is_url(source):
        n_ci, ci_problems = card_image_findings(html, _rel)
        for x in ci_problems:
            fails.append(f"**A service card does not preview its page:** {x}. A card that carries a "
                         f"photograph carries the image its target page presents as its own preview, "
                         f"its og:image, the same file, size and alt (3.93). Run "
                         f"scripts/sync-service-cards.py.")
        if n_ci and not ci_problems:
            passes.append(f"All {n_ci} photographed service card(s) carry their page's own preview "
                          f"image, file, size and alt.")

    # --- A Google Maps embed is the verified pin, by coordinates (3.65) ---
    # Greg's ruling of 2026-09-28: /contact-us/ embeds Google's map CENTRED
    # ON GEO_LAT, GEO_LON, never on the business's name. A name query renders
    # the Business Profile's card, today carrying a second name and an
    # unconfirmed phone number, onto the page from Google's side, where no
    # other check of ours can see it. So any Google Maps iframe must query
    # exactly the pin, carry a title, and load lazily.
    for tag in re.findall(r"<iframe\b[^>]*>", html, re.I):
        src = unescape((re.search(r'\bsrc="([^"]*)"', tag) or [None, ""])[1])
        if "google." not in src or "/maps" not in src:
            continue
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(src).query).get("q", [""])[0]
        want = f"{GEO_LAT},{GEO_LON}"
        problems = []
        if q != want:
            problems.append(f"it queries “{q}”, not the verified pin {want}"
                            + (" (a NAME query brings the Business Profile's card with it)"
                               if re.search(r"[A-Za-z]", q) else ""))
        if not re.search(r'\btitle="[^"]+"', tag):
            problems.append("it has no title, so a screen reader announces an unnamed frame")
        if 'loading="lazy"' not in tag:
            problems.append("it does not load lazily, so its weight lands on every visit")
        if problems:
            fails.append("**The Google Maps embed is wrong:** " + "; ".join(problems) + ".")
        else:
            passes.append(f"The Google Maps embed is centred on the verified pin, {want}, "
                          f"by coordinates, titled, and lazy-loaded.")

    # --- The map is drawn (3.81), town pages only ---
    # build-town.py writes the MAP markers empty and prepare-map-image.py
    # draws between them afterwards. A page built and never drawn would ship
    # a blank map box, and nothing else would notice: a critical, by Greg's
    # ruling that an undrawn map never ships silently.
    if declared_kind == TOWN_KIND:
        mm = re.search(r"(?s)<!-- MAP:BEGIN[^>]*-->(.*?)<!-- MAP:END -->", html)
        if not mm:
            fails.append("**This town page has no MAP markers, so no map can be drawn into it.** "
                         "Rebuild it with scripts/build-town.py.")
        elif not re.search(r"<svg\b[^>]*\brole=\"img\"", mm.group(1)):
            fails.append("**This town page's map is empty: the MAP markers hold no drawing.** Run "
                         "scripts/prepare-map-image.py for this town after building the page.")
        else:
            passes.append("The page's map is drawn between its MAP markers.")

    # --- One routing, every rendering derived (3.65), town pages only ---
    if declared_kind == TOWN_KIND:
        slug = os.path.basename(os.path.dirname(os.path.abspath(source)))
        key = slug[len(TOWN_ROUTE_PREFIX):] if slug.startswith(TOWN_ROUTE_PREFIX) else slug
        route = TOWN_ROUTES.get(key)
        own = page_url(source) if not is_url(source) else source
        if route is None:
            if route_quantities(visible_text(html)):
                fails.append(f"**This town page prints drive times or distances with no recorded "
                             f"routing behind them.** Add `{key}` to TOWN_ROUTES in scripts/audit.py "
                             f"from an actual routing, or take the figures off the page.")
        else:
            found = town_route_findings(html, route, llms_entry_for(own) if not is_url(source) else "")
            if found:
                fails.append("**The page's directions disagree with its recorded routing** "
                             f"(TOWN_ROUTES[{key!r}], {route['recorded']}): " + "; ".join(found)
                             + ". A wrong turn word or a stale minute is a build failure, not a proofread.")
            else:
                passes.append(f"Directions derive from the recorded routing ({route['recorded']}): "
                              f"{len(route['steps'])} steps in order with their turns, roads and "
                              f"distances, and every drive time and distance rendering agrees.")

    # --- The hub is held to the routings too (3.79, protocol f) ---
    if declared_kind == HUB_KIND:
        found = hub_route_findings(html)
        n_blocks = len(re.findall(r'\bdata-town="', html))
        if found:
            fails.append("**The hub states something about a town that its recorded routing does "
                         "not derive:** " + "; ".join(found) + ".")
        else:
            passes.append(f"Every drive figure and road on the hub derives from its town's recorded "
                          f"routing: {n_blocks} town blocks read, no bearing, no figure outside a block.")

    # --- Structured data (JSON-LD) ---
    types = []
    faq_nodes = []            # every FAQPage node found, for the mirror check
    crumb_nodes = []          # every BreadcrumbList node, for the crumb mirror
    business_same_as = False  # sameAs found ON the business node, not just anywhere
    business_nodes = []       # the business node(s), for the served-list check
    for block in p.jsonld_blocks:
        try:
            data = json.loads(block)
            items = data if isinstance(data, list) else [data]
            # A page that describes several things at once (a business, a
            # service, a breadcrumb, an FAQ) puts them in an @graph so they
            # can reference each other by @id. Unwrap it, or every node
            # inside is invisible and the page looks like it has no schema
            # at all. Most modern CMS sites emit one, so this matters when
            # auditing a prospect's site too.
            unwrapped = []
            for item in items:
                graph = item.get("@graph") if isinstance(item, dict) else None
                if graph:
                    unwrapped.extend(graph if isinstance(graph, list) else [graph])
                else:
                    unwrapped.append(item)
            for item in unwrapped:
                t2 = item.get("@type")
                if t2:
                    names = [type_name(t) for t in
                             (t2 if isinstance(t2, list) else [t2])]
                    names = [n for n in names if n]
                    types.extend(names)
                    if "FAQPage" in names:
                        faq_nodes.append(item)
                    if "BreadcrumbList" in names:
                        crumb_nodes.append(item)
                    # sameAs is only an entity signal where it sits on
                    # the BUSINESS. See the check further down for the
                    # false pass this exists to prevent.
                    if LOCAL_BUSINESS_TYPES.intersection(names) and item.get("sameAs"):
                        business_same_as = True
                    if LOCAL_BUSINESS_TYPES.intersection(names):
                        business_nodes.append(item)
        except (json.JSONDecodeError, AttributeError):
            warns.append("**A JSON-LD block failed to parse.** Broken structured data is invisible to Google. Validate at validator.schema.org.")
    if types:
        passes.append(f"Structured data found: {', '.join(types)}.")
        if not LOCAL_BUSINESS_TYPES.intersection(types):
            warns.append("**No LocalBusiness-type schema detected.** For a local business this is the #1 upgrade: add name, address, phone, hours, and geo as JSON-LD.")
    else:
        fails.append("**No structured data (JSON-LD) at all.** This is how you speak directly to Google's machines and AI search. Most competitors are missing it, so it is an easy win.")

    # --- AEO: is the page built to BE the answer? ---
    # AI assistants and Google's AI Overviews lift answers from pages that
    # ask the question and answer it directly. FAQPage schema + real Q&A
    # text is the closest thing to raising your hand.
    if "FAQPage" in types:
        passes.append("AEO: FAQPage schema present: the page offers ready-made Q&As for AI answers and rich results.")
    elif "faq-schema" in exempt and not p.faq_visible:
        # Not required, never unmeasured: a page of an exempt kind that DOES
        # show a visible FAQ falls through to the warning below and to the
        # mirror law, exactly like every other page (3.57).
        notes.append(f"**No FAQPage schema, not measured here.** {exempt_why}")
    else:
        warns.append("**AEO gap: no FAQPage schema.** Add a real FAQ section (the questions customers "
                     "actually call to ask) marked up as FAQPage; it's the closest thing to raising "
                     "your hand when an AI assembles an answer.")

    # --- FAQ mirror: does the schema say what the page says? ---
    # Assistants and rich results quote acceptedAnswer, not the visible
    # copy, so the two drifting apart means the machines are handing out a
    # sentence the reader never sees. The house rule is that each visible
    # question and answer is byte-identical to its schema twin: edit one,
    # edit both. Runs on parsed page text, so it works the same against a
    # local file or a fetched live URL.
    schema_faq = []
    for node in faq_nodes:
        entities = node.get("mainEntity") or []
        for q in entities if isinstance(entities, list) else [entities]:
            if not isinstance(q, dict):
                continue
            ans = q.get("acceptedAnswer") or {}
            schema_faq.append((str(q.get("name", "")).strip(),
                               str(ans.get("text", "")).strip() if isinstance(ans, dict) else ""))
    if schema_faq and not p.faq_visible:
        # Schema but nothing this check can read. On our pages that means
        # the FAQ section is gone; on a prospect's it usually means their
        # FAQ is built from divs we do not recognize. Not worth scoring a
        # stranger's site down for markup we simply cannot see, so it says
        # so and stops.
        notes.append(f"{len(schema_faq)} FAQ question(s) in FAQPage schema, but no visible "
                     f"<details>/<summary> FAQ was found to compare them against. Either the "
                     f"page's FAQ is missing, or it is built with markup this check does not read.")
    elif p.faq_visible and not schema_faq:
        # The AEO check above already warns that FAQPage schema is absent,
        # and that warning is itself a scoring defect. Saying it again per
        # question would punish one mistake several times over.
        pass
    elif schema_faq or p.faq_visible:
        by_schema = dict(schema_faq)
        by_page = dict(p.faq_visible)
        only_schema = [q for q in by_schema if q not in by_page]
        only_page = [q for q in by_page if q not in by_schema]
        mismatched = [q for q in by_schema if q in by_page and by_schema[q] != by_page[q]]

        # One on each side is almost always the same item with its
        # question edited in one place only. Say that, rather than
        # reporting it twice as two unrelated absences.
        if len(only_schema) == 1 and len(only_page) == 1:
            fails.append(
                f"**FAQ question text differs between the page and its schema.** "
                f"Schema asks “{only_schema[0][:90]}”, the page asks “{only_page[0][:90]}”. "
                f"Each question must be byte-identical in both: edit one, edit both.")
            only_schema, only_page = [], []
        for q in only_schema:
            fails.append(f"**FAQ in schema but not on the page: “{q[:90]}”.** "
                         f"Schema promising an answer the reader never sees is the kind of thing "
                         f"Google penalizes as mismatched structured data. Add it or drop it.")
        for q in only_page:
            fails.append(f"**FAQ on the page but not in schema: “{q[:90]}”.** "
                         f"It cannot be quoted by AI answers or rich results until it is in the "
                         f"FAQPage node.")
        for q in mismatched:
            fails.append(f"**FAQ answer does not match its schema: “{q[:70]}”.** "
                         f"The page says “{by_page[q][:80]}…” and the schema says "
                         f"“{by_schema[q][:80]}…”. Assistants quote the schema, so this is the "
                         f"sentence being handed out instead of yours. Edit one, edit both.")
        if not (only_schema or only_page or mismatched) and schema_faq:
            passes.append(f"All {len(schema_faq)} FAQ questions and answers are byte-identical "
                          f"between the visible page and the FAQPage schema.")

    # --- FAQ standalone openers, 3.94 ---
    # An assistant lifts the first sentence of an answer without its
    # question. See FAQ_OPENER_* for the rule.
    opener_qas = schema_faq or list(p.faq_visible or [])
    if opener_qas:
        bad = faq_opener_findings(opener_qas)
        for q, first, why in bad:
            fails.append(f"**An FAQ answer's first sentence does not stand alone ({why}):** "
                         f"\u201c{q[:70]}\u201d opens \u201c{first[:80]}\u201d. Assistants lift "
                         f"the opener without its question, so it has to carry its own subject. "
                         f"Comma-merge a bare particle into the sentence after it (\u201cNo, "
                         f"...\u201d), or name the subject.")
        if not bad:
            passes.append(f"All {len(opener_qas)} FAQ answers open on a sentence that stands "
                          f"alone without its question.")

    # --- Crumb mirror: does the BreadcrumbList say what the crumb says? ---
    # 3.76, closing 3.60's open item 1. The FAQ mirror's law applied to the
    # breadcrumb: Google shows the BreadcrumbList's names as the result's
    # path, so a crumb edited on the page and not in the schema hands out a
    # trail the reader never sees. Labels and order must be byte-identical,
    # both directions. SEVERITY ARGUED FROM THE FAQ MIRROR, case by case:
    #   both present, any difference ...... a CRITICAL, as FAQ drift is;
    #   a visible crumb, no BreadcrumbList . a WARNING, as a visible FAQ
    #                                        with no FAQPage schema is;
    #   a BreadcrumbList, no readable crumb  a NOTE, as FAQ schema with no
    #                                        readable FAQ is: the weekly scan
    #                                        reads the live WordPress site,
    #                                        whose crumb markup this parser
    #                                        may not recognise, and a stranger's
    #                                        markup is not scored down.
    # A crumb nav whose items are not <li>s reads as unreadable, not empty.
    schema_crumb = []
    for node in crumb_nodes[:1]:
        elements = node.get("itemListElement") or []
        elements = [e for e in (elements if isinstance(elements, list) else [elements])
                    if isinstance(e, dict)]
        def _pos(e):
            try:
                return float(e.get("position"))
            except (TypeError, ValueError):
                return float("inf")
        for e in sorted(elements, key=_pos):
            name = e.get("name")
            if name is None and isinstance(e.get("item"), dict):
                name = e["item"].get("name")
            schema_crumb.append(" ".join(str(name or "").split()))
    page_crumb = p.crumb_visible or []
    if page_crumb and schema_crumb:
        if page_crumb == schema_crumb:
            passes.append(f"The visible breadcrumb and the BreadcrumbList agree, "
                          f"{len(page_crumb)} items in the same order: "
                          + " / ".join(page_crumb) + ".")
        else:
            only_page = [x for x in page_crumb if x not in schema_crumb]
            only_schema = [x for x in schema_crumb if x not in page_crumb]
            if len(only_page) == 1 and len(only_schema) == 1 and len(page_crumb) == len(schema_crumb):
                fails.append(f"**Breadcrumb label differs between the page and its schema.** The page "
                             f"says “{only_page[0][:80]}”, the BreadcrumbList says "
                             f"“{only_schema[0][:80]}”. Each label must be byte-identical in both: "
                             f"edit one, edit both.")
            else:
                for x in only_page:
                    fails.append(f"**Breadcrumb item on the page but not in the BreadcrumbList: "
                                 f"“{x[:80]}”.** Search results show the schema's trail, so this "
                                 f"step is missing from it.")
                for x in only_schema:
                    fails.append(f"**Breadcrumb item in the BreadcrumbList but not on the page: "
                                 f"“{x[:80]}”.** The schema is handing out a step the reader "
                                 f"never sees.")
                if not only_page and not only_schema:
                    fails.append("**Breadcrumb order differs between the page and its schema.** "
                                 "The page reads " + " / ".join(page_crumb) + "; the BreadcrumbList "
                                 "reads " + " / ".join(schema_crumb) + ". Same items, same order.")
    elif page_crumb:
        warns.append("**A visible breadcrumb with no BreadcrumbList schema.** Search results cannot "
                     "show the trail " + " / ".join(page_crumb) + " until it is marked up; add a "
                     "BreadcrumbList with the same labels in the same order.")
    elif schema_crumb:
        notes.append(f"A BreadcrumbList of {len(schema_crumb)} items, but no visible breadcrumb this "
                     f"check can read to compare it against: either the page shows none, or it is "
                     f"built with markup this check does not read.")

    # --- The served list: every business node carries AREA_SERVED (3.79) ---
    # One list, written by scripts/sync-area-served.py. A page whose node
    # names a different set, order or shape is a critical: two pages that
    # serve different towns describe two businesses. Local files only: the
    # live WordPress site's schema is not ours until cutover, and scoring
    # it against this list would fill every Monday report with criticals
    # that describe the old site, not this one.
    if business_nodes and not is_url(source):
        want = area_served_nodes()
        if all(n.get("areaServed") == want for n in business_nodes):
            passes.append(f"The business node's areaServed is the one served list, AREA_SERVED "
                          f"({len(want)} places).")
        else:
            got = [a.get("name") for a in (business_nodes[0].get("areaServed") or []) if isinstance(a, dict)]
            missing = [x[1] for x in AREA_SERVED if x[1] not in got]
            extra = [x for x in got if x not in [y[1] for y in AREA_SERVED]]
            fails.append("**The business node's areaServed is not the served list.** "
                         + (f"Missing: {', '.join(missing)}. " if missing else "")
                         + (f"Not in AREA_SERVED: {', '.join(extra)}. " if extra else "")
                         + "Every page carries one list, AREA_SERVED in scripts/audit.py; run "
                           "scripts/sync-area-served.py rather than editing a page's schema.")

    # Entity clarity: sameAs links tie the business to its profiles
    # (Google Business Profile, Yelp, Instagram...), which is how AI
    # systems confirm the business is real and reviewed.
    # THIS USED TO BE A SUBSTRING SEARCH over the whole JSON-LD, and a
    # substring search finds sameAs anywhere: on an areaServed entry
    # pointing at a Wikipedia article for the county, for instance, which
    # is a perfectly ordinary thing to publish and says nothing at all
    # about whether the BUSINESS has verified profiles. The page then
    # scored a pass on an entity signal it did not have. A check that can
    # be satisfied by the wrong node is the same class of defect as the
    # address check that was satisfied by a prefix, so it is fixed the
    # same way: look at the node that has to carry it.
    if business_same_as:
        passes.append("AEO: the business node carries sameAs profile links, a strong entity signal for AI systems.")
    else:
        warns.append("**AEO gap: no `sameAs` links on the business node.** Add links to the Google "
                     "Business Profile, Yelp, and social profiles so AI systems can verify the entity "
                     "and its reviews. A sameAs elsewhere in the graph, on an areaServed place for "
                     "example, does not count: it says nothing about this business.")

    # --- Social sharing ---
    # The 160-character ceiling on og:description is a HOUSE RULE, not a
    # standard. Open Graph itself sets no limit, and the networks all cut
    # at different points (and move the goalposts), so nobody can tell you
    # the "correct" length. What we can do is keep one number in the head
    # of every page: the meta description is capped at 160 above, and the
    # two descriptions are usually near-copies of each other, so letting
    # og: run longer just means the pair drifts apart. A NOTE, not a
    # warning and never a critical: notes are the one bucket score_of()
    # does not count, which is right for a rule we invented. An over-long
    # og:description still shares fine, so it should never be the reason
    # a page drops off 100. The missing-tags case below stays a warning,
    # because that one is a real defect.
    og_d = p.meta.get("og:description", "").strip()
    if not (p.meta.get("og:title") and og_d):
        warns.append("**Missing Open Graph tags** (og:title / og:description), so shared links will look broken or bare on Facebook/LinkedIn.")
    else:
        passes.append(f"Open Graph tags present ({len(og_d)}-char og:description), so the site will look right when shared on social.")
        if len(og_d) > 160:
            notes.append(f"og:description is {len(og_d)} characters, past the 160 the meta description keeps. House consistency rule, not a spec: trim it when convenient, preserving the promises over the connectives. “{og_d[:80]}…”")

    # --- Technical basics ---
    if p.canonical:
        passes.append(f"Canonical URL set: {p.canonical}")
    else:
        warns.append("**No canonical URL.** Add `<link rel=\"canonical\" ...>` to avoid duplicate-content confusion.")

    if p.has_viewport:
        passes.append("Mobile viewport tag present (site is mobile-friendly at the HTML level).")
    else:
        fails.append("**No viewport meta tag.** Google indexes mobile-first; this is a must-fix.")

    # See STAGING at the top of this file for why this check is inverted
    # while the build is not live.
    robots = p.meta.get("robots", "")
    if STAGING:
        if "noindex" in robots:
            passes.append("Correctly noindexed for staging: the real site is still live on "
                          "WordPress, and this build must not answer for the same business.")
            notes.append("**Recorded staging exception.** This page carries `noindex, nofollow`, "
                         "`docs/robots.txt` disallows everything, and the canonical points at "
                         "the production domain. All three are deliberate, all three come off "
                         "together at cutover, and none of them is a defect to be fixed before "
                         "then. `STAGING` in `scripts/audit.py` is the switch. On a live site "
                         "this check runs the other way and a noindexed page is a critical.")
        else:
            fails.append("**This page is NOT noindexed and the build is still staging.** Every "
                         "page carries `<meta name=\"robots\" content=\"noindex, nofollow\">` "
                         "until cutover, because the shop's real site is live right now and a "
                         "crawlable second copy is a second address answering for one business. "
                         "Add the tag, or set `STAGING = False` if this really is cutover day.")
    elif "noindex" in robots:
        fails.append("**Page is set to NOINDEX.** It is telling Google to ignore it entirely. Fix immediately unless intentional.")

    # --- The staging banner and the favicon set, 3.94 ---
    # Only for a file that lives under docs/: a fabricated test page is
    # not a page of this site and carries neither.
    if not is_url(source):
        _in = os.path.relpath(os.path.dirname(os.path.abspath(source)),
                              os.path.abspath(SITE_DIR)).replace(os.sep, "/")
        if not _in.startswith(".."):
            sp, sw, sf = staging_page_findings(html)
            passes += sp
            warns += sw
            fails += sf
            ip, ifl = icon_findings(html, "" if _in == "." else _in + "/")
            passes += ip
            fails += ifl

    # --- Images ---
    missing_alt = [src for src, alt in p.images if alt is None or not alt.strip()]
    if p.images and missing_alt:
        warns.append(f"**{len(missing_alt)} of {len(p.images)} images missing alt text.** Alt text helps image search and accessibility.")
    elif p.images:
        passes.append(f"All {len(p.images)} images have alt text.")

    # --- Tappable phone and email ---
    # A bare number in body copy is a number the reader has to memorize
    # and retype. Every visible mention should be a tel:/mailto: link, so
    # a phone reader taps once. Silent regression is the real risk here:
    # this is the kind of thing that gets missed when a new FAQ answer or
    # card is written, which is exactly why it is checked on every page.
    if p.contacts_bare:
        where = ", ".join(f"line {ln} ({kind})" for ln, kind in p.contacts_bare[:5])
        warns.append(f"**{len(p.contacts_bare)} phone/email mention(s) not linked** ({where}). "
                     f"Wrap each one so it is tappable on a phone: "
                     f"`<a href=\"tel:{NAP_PHONE_TEL}\">{NAP_PHONE_DISPLAY}</a>`.")
    elif p.contacts_linked:
        passes.append(f"All {p.contacts_linked} phone/email mentions are tappable tel:/mailto: links.")

    # The second mailbox. See NAP_EMAIL_WRONG_RE for why this is a
    # critical and not a tidy-up.
    if NAP_EMAIL_WRONG_RE.search(html):
        fails.append(
            "**This page prints `info@tricountycollision.com`.** The one address this site "
            "publishes is `contact@tricountycollision.com`. The old WordPress footer carries "
            "the other one, so it travels during a migration without anyone typing it. Two "
            "addresses for one business read as two businesses to entity matching, and only "
            "one of them is the mailbox the shop actually reads.")

    # The CallRail number. See TRACKING_PHONE_RE.
    if TRACKING_PHONE_RE.search(html):
        fails.append(
            "**This page contains the CallRail tracking number (215) 709-9665.** It must never "
            "appear in this site's source, schema or templates. CallRail swaps numbers into the "
            "page visually at runtime; a tracking number written into the markup is a second "
            "phone number for one business, and it is the number crawlers and AI assistants "
            f"will hand out. Use `{NAP_PHONE_DISPLAY}` and let the snippet do its job.")

    # --- The street address, spelled one way ---
    if NAP_STREET_MENTION_RE.search(html):
        has_street = NAP_STREET_CANON_RE.search(html) is not None
        has_cityline = NAP_CITYLINE_CANON in html
        variant = NAP_STREET_VARIANT_RE.search(html)
        # A variant fails even when the canonical spelling is ALSO on the
        # page, which the old `and not has_street` guard let through. That
        # is not a hypothetical: the live WordPress site prints
        # "995 Jaymor Rd" in its footer and "995 Jaymor Road" in its
        # JSON-LD, on the same page. One page, two businesses.
        if variant:
            fails.append(
                f"**The street address is spelled `{variant.group(0)}` here, not "
                f"`{NAP_STREET_CANON}`.** NAP is character-identical everywhere or it is "
                f"nothing: each variant reads as a slightly different business to "
                f"Google's entity matching, which is how a shop ends up competing with "
                f"itself in the Map Pack. A trailing period counts, and so does a variant "
                f"that sits alongside the correct spelling somewhere else on the page. "
                f"Use `{NAP_STREET_CANON}`.")
        elif not has_street:
            fails.append(
                f"**This page names Jaymor but not `{NAP_STREET_CANON}`.** If the page "
                f"carries the address it carries the canonical spelling. If it should "
                f"not carry the address at all, take the mention out.")
        elif not has_cityline:
            warns.append(
                f"**The street line is here but `{NAP_CITYLINE_CANON}` is not.** A street "
                f"address without its city, state and ZIP is not a NAP match. Add the "
                f"full line.")
        else:
            passes.append(f"NAP address is the canonical spelling: "
                          f"{NAP_STREET_CANON}, {NAP_CITYLINE_CANON}.")

    # --- The hours: every copy says the constants, and nothing else ---
    vis = re.sub(r"(?s)<!--.*?-->|<script.*?</script>|<style.*?</style>", " ", html)
    vis = re.sub(r"<[^>]+>", " ", vis)
    n_ok, strays, sundays = hours_findings(vis)
    biz_nodes = []
    for block in p.jsonld_blocks:
        try:
            data = json.loads(block)
        except (json.JSONDecodeError, ValueError):
            continue
        for item in (data if isinstance(data, list) else [data]):
            if isinstance(item, dict):
                g = item.get("@graph")
                biz_nodes.extend(x for x in (g if isinstance(g, list) else [item])
                                 if isinstance(x, dict) and "openingHoursSpecification" in x)
    schema_off = hours_schema_findings(biz_nodes)
    for x in strays:
        fails.append(f"**The hours are written a second way:** \u201c{x}\u201d. Every copy "
                     f"says `{HOURS_WEEKDAYS}` and `{HOURS_SATURDAY}`, character for "
                     f"character (HOURS_* in scripts/audit.py), because a customer acts "
                     f"on the hours and two versions of them is one wrong.")
    for x in sundays:
        fails.append(f"**Sunday is mentioned:** \u201c{x}\u201d. The record has no Sunday "
                     f"hours, open or closed; the live schema never says. It is an owner "
                     f"question (proposed-changes.md section 5), not a fact to publish.")
    for x in schema_off:
        fails.append(f"**The schema's hours disagree with the constants:** {x}.")
    if n_ok and not strays and not sundays and not schema_off:
        passes.append(f"Hours match the constants in all {n_ok} visible mention"
                      f"{'' if n_ok == 1 else 's'}"
                      f"{' and the schema' if biz_nodes else ''}.")

    # --- The shop's coordinates: every business node says the constants ---
    all_nodes = []
    for block in p.jsonld_blocks:
        try:
            data = json.loads(block)
        except (json.JSONDecodeError, ValueError):
            continue
        for item in (data if isinstance(data, list) else [data]):
            if isinstance(item, dict):
                g = item.get("@graph")
                all_nodes.extend(x for x in (g if isinstance(g, list) else [item])
                                 if isinstance(x, dict))
    n_geo, geo_off = geo_findings(all_nodes)
    for x in geo_off:
        fails.append(f"**The schema's geo is not the shop's verified pin:** {x}. "
                     f"GEO_LAT and GEO_LON in scripts/audit.py are the one place it "
                     f"lives (proposed-changes.md 3.56). Never take coordinates from a "
                     f"map URL: its @lat,lon is the viewport centre, not the pin.")
    if n_geo and not geo_off:
        passes.append(f"Schema geo is the verified pin, {GEO_LAT}, {GEO_LON}.")

    # --- Word count (thin content check) ---
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", html)
    words = len(text.split())
    if words < 300 and "thin-content" in exempt:
        notes.append(f"**~{words} words, not measured against 300 here.** {exempt_why}")
    elif words < 300:
        warns.append(f"**Thin content: ~{words} words.** Local pages generally need 300+ words of real, useful text to rank.")
    else:
        passes.append(f"Healthy content depth: ~{words} words on the page.")

    # --- Cache-busting stamps on the shared assets ---
    check_asset_stamps(html, current_stamps() if not is_url(source) else {}, passes, fails)

    # --- Published where crawlers can find it ---
    # A page that exists but is in neither sitemap.xml nor llms.txt is a
    # page Google and the AI assistants may never discover. On a live run
    # this is moot: the page list came FROM the sitemap.
    if coverage is not None and p.canonical:
        canon = p.canonical.strip()
        if canon in coverage["sitemap_locs"]:
            passes.append(f"Listed in sitemap.xml, so crawlers get pointed at it: {canon}")
        else:
            fails.append(f"**Not listed in `docs/sitemap.xml`.** The page is live at {canon} but "
                         "the sitemap never mentions it, so Google has to stumble on it. Add a "
                         "`<url>` block with today's date.")
        # Word-boundary match: without it, the homepage's canonical would
        # match any deeper URL that starts with it and always "pass".
        if re.search(re.escape(canon) + r"(?![\w/.\-])", coverage["llms_text"]):
            passes.append("AEO: listed in llms.txt, so AI agents get a guided route to the page.")
        else:
            warns.append(f"**Not listed in `docs/llms.txt`.** Add {canon} under `## Key pages` so "
                         "AI assistants reading the guide know this page exists.")

    return passes, warns, fails, notes, kind


def score_of(n_pass: int, n_warn: int, n_fail: int) -> int:
    """Unchanged formula: the share of checks that passed. Notes are free."""
    return round(100 * n_pass / max(1, n_pass + n_warn + n_fail))


def is_xml_url(url: str) -> bool:
    """True for a URL that points at an XML file. Those are sitemaps and
    feeds, never pages. Scoring one against the HTML rubric produces a
    page-shaped verdict about a file no reader will ever open."""
    return urlparse(url).path.lower().endswith(".xml")


def new_sitemap_stats() -> dict:
    """What one expansion learned about the sitemaps it read, so the
    report can say what was followed and what was skipped."""
    return {"files": 0, "indexes": 0, "unreadable": [], "capped": False}


def collect_sitemap_pages(sitemap_url: str, depth: int = 0, seen: set = None,
                          stats: dict = None) -> list:
    """Returns the page URLs one sitemap lists, following an index.

    A <urlset> lists pages. A <sitemapindex> lists other sitemaps, and
    its <loc> entries are those sitemaps' own addresses. Both use the
    same <loc> tag, so the wrapper tag is the only thing that says which
    kind of list you are holding. Reading an index as if it were a
    urlset is what put category-sitemap.xml, page-sitemap.xml and
    post-sitemap.xml through the page rubric on the first prospect scan.

    Anything ending in .xml is dropped here whatever the wrapper said,
    so a sitemap that is mislabeled, or an index nested deeper than we
    follow, still cannot put a sitemap into the page list."""
    if seen is None:
        seen = set()
    if stats is None:
        stats = new_sitemap_stats()
    # Three ways to stop: already been here (an index can point at
    # itself), too deep, or too many files fetched for one run. The last
    # two mean we may be leaving real pages unread, so they get recorded
    # and reported. Revisiting a sitemap we already read costs nothing.
    if sitemap_url in seen:
        return []
    if depth > SITEMAP_MAX_DEPTH or stats["files"] >= SITEMAP_MAX_FILES:
        stats["capped"] = True
        return []
    seen.add(sitemap_url)
    stats["files"] += 1

    xml = load(sitemap_url)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if re.search(r"<\s*sitemapindex[\s>]", xml):
        stats["indexes"] += 1
        pages = []
        for child in locs:
            # One dead child sitemap must not cost us the others.
            try:
                pages.extend(collect_sitemap_pages(child, depth + 1, seen, stats))
            except Exception:
                stats["unreadable"].append(child)
        return pages
    return [u for u in locs if not is_xml_url(u)]


def expand_sitemap(url: str):
    """A live site's page list comes from its own sitemap. If that can't
    be read we still audit the URL we were given, and say why."""
    parts = urlparse(url)
    root = f"{parts.scheme}://{parts.netloc}"
    # Pointing the script straight at a sitemap means audit what THAT
    # file lists, not what /sitemap.xml lists.
    entry = url if is_xml_url(url) else root + "/sitemap.xml"
    fallback = [] if is_xml_url(url) else [url]
    stats = new_sitemap_stats()
    try:
        locs = collect_sitemap_pages(entry, stats=stats)
    except Exception:
        return fallback, (f"Could not read {entry}, so only the page you named was "
                          "audited. Add a sitemap so every page gets scanned.")

    followed = []
    if stats["indexes"]:
        n = stats["files"] - 1
        followed.append(f"{entry} is a sitemap index, so the {n} sitemap"
                        f"{'' if n == 1 else 's'} under it "
                        f"{'was' if n == 1 else 'were'} read instead of being scored as pages.")
    if stats["capped"]:
        followed.append(f"That index nests deeper than {SITEMAP_MAX_DEPTH} levels or lists more "
                        f"than {SITEMAP_MAX_FILES} sitemaps, so the scan stopped following it "
                        "and some pages may be missing from this report.")
    if stats["unreadable"]:
        followed.append("These child sitemaps could not be read: "
                        + ", ".join(stats["unreadable"]) + ".")
    if not locs:
        followed.append(f"{entry} lists no pages, so only the page you named was audited.")
        return fallback, " ".join(followed)
    return sorted(set(locs)), (" ".join(followed) if followed else None)


def resolve_targets(args):
    """No arguments audits the whole site. Paths, folders and URLs all work."""
    if not args:
        return sorted(glob.glob(os.path.join(SITE_DIR, "**", "*.html"), recursive=True)), None
    if len(args) == 1 and is_url(args[0]):
        return expand_sitemap(args[0])
    targets = []
    for a in args:
        if is_url(a) or os.path.isfile(a):
            targets.append(a)
        elif os.path.isdir(a):
            targets.extend(sorted(glob.glob(os.path.join(a, "**", "*.html"), recursive=True)))
        else:
            targets.append(a)   # let it fail loudly with a real filename
    return targets, None


def local_coverage():
    """Reads sitemap.xml and llms.txt once, for the two publish checks."""
    try:
        with open(SITEMAP_PATH, encoding="utf-8") as f:
            sitemap = f.read()
        with open(LLMS_PATH, encoding="utf-8") as f:
            llms = f.read()
    except OSError:
        return None
    return {
        "sitemap_locs": set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap)),
        "llms_text": llms,
    }


def section(title: str, items: list, level: str = "###") -> list:
    return [f"{level} {title}", ""] + [f"- {x}" for x in items] + [""] if items else []


def main():
    ap = argparse.ArgumentParser(
        description="Audit every page of the site for SEO and AEO, scoring each one.")
    ap.add_argument("targets", nargs="*",
                    help="Files, folders or a live URL. Default: every .html under docs/")
    ap.add_argument("--strict", action="store_true",
                    help="Exit 1 if any page scores under 100. Use it in a build gate.")
    opts = ap.parse_args()

    targets, expand_note = resolve_targets(opts.targets)
    if not targets:
        # A live run that found nothing has a reason, and the note is it.
        print(expand_note or f"No HTML pages found under {SITE_DIR}/.", file=sys.stderr)
        return 1

    live = [t for t in targets if is_url(t)]
    coverage = None if live else local_coverage()

    results = []
    for t in targets:
        # One unreadable page must never take the whole run down with it.
        # load() reaches the network for a live URL, and every network
        # error is an exception: DNS, TLS, timeout, 500, a redirect loop.
        # Uncaught, that ends the process with a traceback, no report file
        # is written, and the weekly agent has nothing to read, which is
        # exactly how the 2026-08-17 scheduled run died on a transient DNS
        # failure at the runner. A page we cannot read is a finding, so
        # record it as a critical against that page and keep going.
        try:
            passes, warns, fails, notes, kind = audit(t, coverage=None if is_url(t) else coverage)
        except Exception as e:
            passes, warns, notes, kind = [], [], [], "page"
            fails = [f"**Could not read this page** ({type(e).__name__}: {e}). "
                     "For a live URL that usually means the site or the network was "
                     "unreachable when the scan ran, not that the page is broken. "
                     "Re-run before acting on it."]
        results.append({"source": t, "passes": passes, "warns": warns,
                        "fails": fails, "notes": notes, "kind": kind,
                        "score": score_of(len(passes), len(warns), len(fails))})

    # Site-wide AEO checks run once, against the live site only.
    site_passes, site_warns, site_notes, site_fails = [], [], [], []
    if live:
        check_ai_access(live[0], site_warns, site_passes, site_notes)
    else:
        check_staging_local(site_passes, site_warns, site_notes, site_fails)
        check_review_count_local(site_passes, site_warns, site_fails, site_notes)
        check_brand_count_local(site_passes, site_warns, site_fails, site_notes)
        check_brand_lists_local(site_passes, site_fails, site_notes)
        check_town_variance_local(site_passes, site_warns, site_fails, site_notes)
        check_chrome_local(site_passes, site_fails)
        check_asset_provenance_local(site_passes, site_warns, site_fails, site_notes)
        check_comment_convention_local(site_warns, site_notes)
        check_pending_links_local(site_warns, site_notes)
        check_hours_llms_local(site_passes, site_fails)
        check_service_count_llms_local(site_passes, site_fails)
    if expand_note:
        site_notes.append(expand_note)

    total_pass = sum(len(r["passes"]) for r in results) + len(site_passes)
    total_warn = sum(len(r["warns"]) for r in results) + len(site_warns)
    total_fail = sum(len(r["fails"]) for r in results) + len(site_fails)
    site_score = score_of(total_pass, total_warn, total_fail)
    perfect = [r for r in results if r["score"] == 100]

    # The audited set is no longer all one thing: real pages, redirect
    # stubs standing at old WordPress URLs, and the 404 page. Spelling out
    # the mix keeps the headline count from reading as a page count.
    def _n(kind):
        return sum(1 for r in results if r.get("kind") == kind)

    parts = []
    if _n("page"):
        parts.append(f"{_n('page')} page{'' if _n('page') == 1 else 's'}")
    if _n("redirect-stub"):
        parts.append(f"{_n('redirect-stub')} redirect stub{'' if _n('redirect-stub') == 1 else 's'}")
    if _n("error-404"):
        parts.append(f"{_n('error-404')} error page")
    mix = f" ({', '.join(parts)})" if len(parts) > 1 else ""

    lines = [
        "# SEO + AEO Audit Report", "",
        f"**Site score: {site_score}/100**: {len(perfect)} of {len(results)} "
        f"{'page' if len(results) == 1 else 'pages'} at 100/100{mix}",
        f"**{total_pass} passing · {total_warn} warnings · {total_fail} critical** across the site",
        "",
        "| Page | Score | Passing | Warnings | Critical |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        flag = "" if r["score"] == 100 else " ⚠️"
        lines.append(f"| `{r['source']}` | {r['score']}/100{flag} | {len(r['passes'])} | "
                     f"{len(r['warns'])} | {len(r['fails'])} |")
    lines.append("")

    if site_passes or site_warns or site_notes or site_fails:
        lines += ["## Site-wide", ""]
        lines += section("🔴 Critical: fix these first", site_fails)
        lines += section("🟡 Warnings: worth fixing", site_warns)
        lines += section("🟢 Passing", site_passes)
        lines += section("ℹ️ Notes (optional improvements)", site_notes)

    for r in results:
        lines += [f"## Page: `{r['source']}`: {r['score']}/100", ""]
        lines += section("🔴 Critical: fix these first", r["fails"])
        lines += section("🟡 Warnings: worth fixing", r["warns"])
        lines += section("🟢 Passing", r["passes"])
        lines += section("ℹ️ Notes (optional improvements)", r["notes"])

    report = "\n".join(lines)
    print(report)
    with open("audit-report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("\n(Report saved to audit-report.md)", file=sys.stderr)

    below = [r for r in results if r["score"] < 100]
    if below:
        print(f"{len(below)} page(s) under 100/100: "
              + ", ".join(r["source"] for r in below), file=sys.stderr)
    # A SITE-WIDE CRITICAL HAS TO TRIP --strict TOO. Before the review-count
    # check there were none, so strict only ever read per-page scores, and a
    # site-wide critical would have printed a red heading and exited 0.
    if site_fails:
        print(f"{len(site_fails)} site-wide critical(s).", file=sys.stderr)
    return 1 if (opts.strict and (below or site_fails)) else 0


if __name__ == "__main__":
    sys.exit(main())
