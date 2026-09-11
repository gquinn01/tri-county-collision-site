#!/usr/bin/env python3
"""
SEO + AEO Site Auditor — the "scanning" half of your agent team.

This is a real, working audit script. It checks a page for the on-page
factors that matter most for local businesses — both classic SEO
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

No external packages needed — pure Python standard library.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys
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
# AT CUTOVER: set this to False, take the meta tag off every page, and
# replace docs/robots.txt with an open one that names the sitemap and blocks
# no AI crawler. All three move together. Flipping this to False before the
# tags come off will fail every page, which is the correct alarm and not a
# bug. Record the date here and in CLAUDE.md when it happens.
STAGING = True

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
REVIEW_COUNT_RE = re.compile(r"\b(\d[\d,]{0,6})\s+(?:google\s+)?reviews?\b", re.I)

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
# vocabulary again — do not add names by hand, which is the habit that
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
            fails.append(f"**{len(h1s)} H1 headings found** \u2014 the error page needs exactly one.")
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




class PageParser(HTMLParser):
    """Walks the HTML and collects everything the audit needs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
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

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip_depth += 1
        if tag == "title":
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
        notes.append("Could not fetch robots.txt — if the site truly has none, crawlers default to full access (fine), but add one to be explicit.")

    # --- llms.txt: a curated guide for AI agents ---
    # Honest status (2026): Google says it ignores llms.txt, but Anthropic
    # recommends it, OpenAI publishes them, and Perplexity has been seen
    # reading them. It costs 20 minutes — cheap insurance, not a magic bullet.
    try:
        llms = load(root + "/llms.txt")
        if llms.strip():
            passes.append("AEO: llms.txt present — AI agents get a curated guide to the business.")
    except Exception:
        notes.append("No llms.txt found. Optional (Google ignores it) but Anthropic/OpenAI agent "
                     "tooling reads it — a 20-minute add for extra AI visibility.")


def check_staging_local(passes: list, warns: list, notes: list):
    """The half of the staging exception that is a property of the SITE
    rather than of any page: docs/robots.txt. The per-page half is in
    audit(). Both have to be true or the exception is not actually in
    force, and checking only the tags would have missed the file."""
    path = os.path.join(SITE_DIR, "robots.txt")
    try:
        with open(path, encoding="utf-8") as f:
            body = "\n".join(line.split("#")[0] for line in f.read().splitlines())
    except OSError:
        (warns if STAGING else notes).append(
            f"**No `{path}`.** While the build is staging this file is what stops a crawler "
            f"fetching the pages at all; the meta tags are the second line, not the first.")
        return
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
        warns.append("**`docs/robots.txt` still disallows everything and `STAGING` is off.** "
                     "The site is live and invisible. This is the staging file; replace it with "
                     "the open one that names the sitemap and blocks no AI crawler.")
    else:
        passes.append("`docs/robots.txt` is open, so crawlers and AI agents can read the site.")


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
        warns.append(f"**{len(h1s)} H1 headings found** — use exactly one; demote the rest to H2.")
    else:
        passes.append(f"Exactly one H1: “{h1s[0][:80]}”")

    # --- Structured data (JSON-LD) ---
    types = []
    faq_nodes = []            # every FAQPage node found, for the mirror check
    business_same_as = False  # sameAs found ON the business node, not just anywhere
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
                    # sameAs is only an entity signal where it sits on
                    # the BUSINESS. See the check further down for the
                    # false pass this exists to prevent.
                    if LOCAL_BUSINESS_TYPES.intersection(names) and item.get("sameAs"):
                        business_same_as = True
        except (json.JSONDecodeError, AttributeError):
            warns.append("**A JSON-LD block failed to parse** — broken structured data is invisible to Google. Validate at validator.schema.org.")
    if types:
        passes.append(f"Structured data found: {', '.join(types)}.")
        if not LOCAL_BUSINESS_TYPES.intersection(types):
            warns.append("**No LocalBusiness-type schema detected.** For a local business this is the #1 upgrade — add name, address, phone, hours, and geo as JSON-LD.")
    else:
        fails.append("**No structured data (JSON-LD) at all.** This is how you speak directly to Google's machines and AI search. Most competitors are missing it — easy win.")

    # --- AEO: is the page built to BE the answer? ---
    # AI assistants and Google's AI Overviews lift answers from pages that
    # ask the question and answer it directly. FAQPage schema + real Q&A
    # text is the closest thing to raising your hand.
    if "FAQPage" in types:
        passes.append("AEO: FAQPage schema present — the page offers ready-made Q&As for AI answers and rich results.")
    else:
        warns.append("**AEO gap: no FAQPage schema.** Add a real FAQ section (the questions customers "
                     "actually call to ask) marked up as FAQPage — it's the closest thing to raising "
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
        warns.append("**Missing Open Graph tags** (og:title / og:description) — shared links will look broken or bare on Facebook/LinkedIn.")
    else:
        passes.append(f"Open Graph tags present ({len(og_d)}-char og:description) — the site will look right when shared on social.")
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
        fails.append("**No viewport meta tag** — Google indexes mobile-first; this is a must-fix.")

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
        fails.append("**Page is set to NOINDEX** — it is telling Google to ignore it entirely. Fix immediately unless intentional.")

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

    # --- Word count (thin content check) ---
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", html)
    words = len(text.split())
    if words < 300:
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
        # is written, and the weekly agent has nothing to read — which is
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
        check_staging_local(site_passes, site_warns, site_notes)
        check_review_count_local(site_passes, site_warns, site_fails, site_notes)
        check_comment_convention_local(site_warns, site_notes)
        check_pending_links_local(site_warns, site_notes)
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
        f"**Site score: {site_score}/100** — {len(perfect)} of {len(results)} "
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
        lines += section("🔴 Critical — fix these first", site_fails)
        lines += section("🟡 Warnings — worth fixing", site_warns)
        lines += section("🟢 Passing", site_passes)
        lines += section("ℹ️ Notes (optional improvements)", site_notes)

    for r in results:
        lines += [f"## Page: `{r['source']}` — {r['score']}/100", ""]
        lines += section("🔴 Critical — fix these first", r["fails"])
        lines += section("🟡 Warnings — worth fixing", r["warns"])
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
