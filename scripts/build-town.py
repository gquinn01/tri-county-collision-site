#!/usr/bin/env python3
"""
Builds the town pages, /areas-served-collision-repair-<key>/, from the
Jamison template. proposed-changes.md 3.81.

THE TEMPLATE IS JAMISON AS SHIPPED (3.62 to 3.76), Greg's ruling opening run
two (3.77): the eleven towns are produced from it, not migrated. This script
is the Jamison builder moved out of scratch space and generalised. Its proof
of faithfulness is that it regenerates Jamison's page identically outside
its HTML comments.

WHAT IS DERIVED, AND FROM WHERE. Every drive figure, road, route number,
turn word and compass word comes from TOWN_ROUTES in scripts/audit.py, the
recorded routing the strategy chat verified (3.78), and the page is gated by
the audit's routing check. Derived here, never typed:
  - the lead's first sentence and its routed minutes;
  - the directions card's intro line, steps and chip;
  - the title, by title_for: the cascade Greg rules on in 3.95 (it was
    ruling 4, 3.80, until the name changed). The title check fails anything
    over 60; this function is what keeps the long towns from regressing;
  - the meta description, the schema, and the page's llms.txt entry;
  - the four nearby towns, by straight line between recorded place points.
Every rounding is half-up (3.78). A step under an eighth of a mile is in feet.

WHAT IS WRITTEN PER TOWN (CONTENT below): the two-paragraph opening, which
ends on its own call-first sentence, and the FAQ. Every sentence of it is a
pair in the record, and its figures are placeholders ({min}, {mi}, {mi1},
{d1}...) filled from the routing, so prose can never carry a stale number.
The variance gate in scripts/audit.py holds every town under 30% shared
phrasing against every other page of the tier.

WHAT IS LIFTED BYTE FOR BYTE: the chrome (from a post one directory deep),
the proof cards (from /collision-repair/'s stat band), Real Repairs and the
promise band (from home). A template change there reaches every town on the
next build.

BUILD ORDER: this page, then scripts/prepare-map-image.py draws its map
between the MAP markers (--frame jamison, or --frame town --town KEY --name
NAME for the rest). Rebuilding empties the markers, and the audit fails a
town page whose map is empty (3.81), so the map is always drawn after.

    python3 scripts/build-town.py bensalem-pa richboro-pa     # build these
    python3 scripts/build-town.py --all                         # every town in CONTENT
"""
import argparse
import html
import json
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit  # noqa: E402

# The noindex tag follows audit.STAGING (3.94), so a rebuild after cutover
# cannot re-noindex a page. sync-chrome's pass, which every page written
# here goes through, settles the visible banner and the favicon links.
ROBOTS_LINE = ("  " + audit.STAGING_ROBOTS_META + "\n") if audit.STAGING else ""

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.join(ROOT, "docs", "deer-season-in-bucks-county-insurance-coverage-next-steps", "index.html")
HOME = os.path.join(ROOT, "docs", "index.html")
COLLISION = os.path.join(ROOT, "docs", "collision-repair", "index.html")
LLMS = os.path.join(ROOT, "docs", "llms.txt")
BASE = "https://tricountycollision.com/"
HUB = BASE + "areas-served/"
MAPS_HREF = ("https://www.google.com/maps/search/?api=1&amp;query=Tri%20County%20Collision%20Center"
             "%2C%20995%20Jaymor%20Rd%2C%20Southampton%2C%20PA%2018966")
PHONE = '<a href="tel:+12153225350">(215) 322-5350</a>'
RIGHT_TO_CHOOSE = '<a href="../your-right-to-choose-a-body-shop/">your right to choose a body shop</a>'
# The same post by its other name: its title is "PA Law: Your Right to Choose
# a Body Shop (Anti-Steering)", so this anchor text is the post's own words.
RIGHT_TO_CHOOSE_TITLE = '<a href="../your-right-to-choose-a-body-shop/">PA Law: Your Right to Choose a Body Shop</a>'
COLLISION_LINK = '<a href="../collision-repair/">collision repair</a>'
COMMERCIAL_LINK = '<a href="../commercial-collision-repair/">commercial collision repair</a>'
PDR_LINK = '<a href="../paintless-dent-repair/">paintless dent repair</a>'
GLASS_LINK = '<a href="../auto-glass-repair-replacement/">auto glass repair</a>'
RIGHT_TO_CHOOSE_STEERING = '<a href="../your-right-to-choose-a-body-shop/">Pennsylvania\'s anti-steering rules</a>'
TITLE_MAX, META_MAX = 60, 160

# ---------------------------------------------------------------------------
# PER-TOWN CONTENT. Prose only: every figure is a placeholder.
#   {min}  the route's minutes, half-up          {mi}  whole miles, half-up
#   {mi1}  miles to one decimal                  {dN}  step N's distance phrase
#   {phone} the tel: link                        {rtc} the right-to-choose post link
# Optional per town: "steps" (a style per step, see step_html), "nbsp" (which
# step parts take a no-break space; default every figure and route number,
# the 3.76 rule), "nearby" (keys; default the four nearest by straight line),
# "alt" (an alternative-route paragraph), "corner_names" (the crossroads as
# the card's intro line names it), "modified" (the page's dateModified).
JAMISON_HEAD = '<!-- ============================================================\n       JAMISON, THE PILOT OF THE TOWN-PAGE TEMPLATE. Built 2026-09-28,\n       proposed-changes.md 3.62, which is the template\'s home: section\n       order, the fact discipline, the schema and the variance gate are\n       defined there, and the eleven migrating towns and the hub follow it\n       once Greg approves this page. AMENDED IN 3.63, on Greg\'s rulings:\n       the service heroes\' chip row, the drawn map of the primary route\n       beside the steps, three of home\'s Real Repairs pairs after the\n       promise band with home\'s own ask, and a centred opening. AMENDED IN\n       3.70: the pairs move directly under the proof cards, on ink, and\n       the directions card goes side by side from 900px.\n\n       BUILD ORDER: this page first, then scripts/prepare-map-image.py\n       --frame jamison, which draws between the MAP markers. Rebuilding the\n       page empties them, so the map is always drawn after.\n\n       A REBUILD, NOT A MIGRATION. pagemap.md\'s row: "Rebuild to the\n       sibling standard: directions, named roads, own FAQ; owner supplies\n       the local facts, never invented." The live page carried no\n       directions, no FAQ and no local fact, so no sentence of it survives;\n       every sentence here is a pair in 3.62, awaiting the owner.\n\n       WHERE EACH FACT COMES FROM. The shop\'s name, address, phone and hours\n       are the constants in scripts/audit.py. The roads, route numbers,\n       distance and drive time are an OSRM routing from OpenStreetMap\'s\n       Jamison village point (40.2548297, -75.0893372, where York Road meets\n       Almshouse Road) to the shop\'s verified pin, recorded in 3.62; the\n       drive time is free-flow and flagged there for the owner. That Jamison\n       is in Warwick Township, Bucks County is OpenStreetMap\'s. The\n       neighbors named are only those the shop\'s own hub already serves.\n       Nothing about Jamison that a map cannot check is on this page, by\n       design: that is the owner\'s to supply, and absent until then.\n\n       NOT IN JAMISON, SAID FIRST. The shop is in Southampton, and the page\n       says so in its lead, its opening section and its first question.\n\n       LINKS FOLLOW THE PAGES. A crumb or nearby link whose page is not\n       built yet waits as a span with data-pending-href; the builder writes\n       a real link the day the page exists, and the pending-link test forces\n       that rebuild. The hub landed in 3.79. The schema\n       keeps the hub\'s absolute production URL, because the schema\n       describes the production site and the tier ships together.\n\n       STAGING, DELIBERATE, AND NOT A DEFECT: noindex below, docs/robots.txt\n       disallows everything, and the canonical is absolute to the\n       production domain. All three come off together at cutover.\n\n       NO PRICE, OFFER, REVIEW OR RATING MARKUP.\n       ============================================================ -->'
JAMISON_OPENING_NOTE = '         "AND THE SURROUNDING AREA" (3.71) names no town, so it needs no hub\n         check; the towns it does name must be hub-served, as 3.62 ruled.\n         "WE ARE NOT IN JAMISON, AND WE WON\'T PRETEND TO BE" IS KEPT ON\n         PURPOSE: the question of cutting it was raised and Greg ruled it\n         stays, 2026-09-29. It is the page\'s protected-voice line, and its\n         honesty is what makes the rest credible. No sweep flattens it.\n'

CONTENT = {
    "jamison-pa": {
        "name": "Jamison", "county": "bucks", "modified": "2026-10-09",
        "corner_names": ("York Road", "Almshouse Road"),
        "opening": [
            "Tri County Collision Center is a family-owned body shop in Southampton, and we fix cars for drivers "
            "from Jamison, Warminster, Richboro, Ivyland and the surrounding area. We are not in Jamison, "
            "and we won't pretend to be. We are about {mi} miles down the road.",
            "Jamison sits in Warwick Township, where York Road (PA 263) meets Almshouse Road. From that "
            "corner to our shop is about {min} minutes without traffic. If your car has been in an "
            "accident, call before you decide where it goes.",
        ],
        "faq": [
            ("Is Tri County Collision Center actually in Jamison?",
             "Tri County Collision Center is not in Jamison: the shop is at 995 Jaymor Rd, Southampton, PA 18966, "
             "about {mi} miles and {min} minutes from Jamison without traffic. Pennsylvania law protects "
             "your right to choose your own collision shop for repairs. Your insurance company cannot "
             "require you to use their preferred facility or steer you elsewhere. Our post on {rtc} "
             "explains the law."),
            ("How do I get to Tri County Collision Center from Jamison?",
             "The drive from Jamison to Tri County Collision Center is about {mi1} miles and takes about {min} "
             "minutes without traffic: south on York Road (PA 263), left on West Bristol Road, right on "
             "Second Street Pike (PA 232), and right on Jaymor Rd to the shop."),
            ("Does Tri County Collision Center work with my insurance company if I live in Jamison?",
             "Tri County Collision Center works with all major insurance companies, and a Jamison address makes no "
             "difference to that."),
            ("When is Tri County Collision Center open for Jamison drivers?",
             "Tri County Collision Center is open Monday to Friday, 8 a.m. to 6 p.m., and Saturday by appointment "
             "only."),
        ],
        "steps": ("head", "follow", "go", "last"),
        "nbsp": ({"ref"}, {"dist"}, set(), set()),
        "head": JAMISON_HEAD,
        "opening_note": JAMISON_OPENING_NOTE,
        "alt": ("Staying on York Road to County Line Road, then following County Line Road east to "
                "James Way and Jaymor Rd, takes about the same time."),
    },
    "bensalem-pa": {
        "name": "Bensalem", "county": "bucks", "modified": "2026-10-09",
        "opening": [
            "Tri County Collision Center repairs cars for Bensalem drivers, and for their neighbors in "
            "Feasterville-Trevose, Langhorne, Huntingdon Valley and Northeast Philadelphia. The shop is in "
            "Southampton, not Bensalem Township. From Knights Road the drive is about {mi} miles, and "
            "almost all of it is Street Road.",
            "Knights Road crosses Street Road (PA 132) inside Bensalem Township, Bucks County. Leave from that "
            "crossroads and you reach our door in about {min} minutes when the road is clear. Before "
            "your car goes to a shop you didn't pick, pick up the phone and call us.",
        ],
        "faq": [
            ("Is there a Tri County Collision Center location in Bensalem?",
             "Bensalem has no Tri County Collision Center location. The shop is at 995 Jaymor Rd, Southampton, "
             "PA 18966, about {mi} miles and {min} minutes from Knights Road and Street Road on clear "
             "roads. Where your car gets fixed is your decision under Pennsylvania law, not your "
             "insurer's, and our write-up of {rtc_steer} sets out what that means."),
            ("Which roads lead from Bensalem to the shop?",
             "Street Road (PA 132) does almost all the work: stay on it about {d1} from Knights Road, go "
             "left at 2nd Street Pike (PA 232) and drive about {d2}, then make the right onto Jaymor Rd, "
             "where the shop is about {d3} in."),
            ("Does Tri County Collision Center handle the insurance claim for a Bensalem driver?",
             "Tri County Collision Center handles the paperwork and communication with your insurer, so you don't "
             "have to, and it works with all major insurance companies."),
            ("Will Street Road traffic change the drive time?",
             "Street Road traffic can lengthen the drive from Bensalem. The figure of about {min} minutes is a routing on empty roads, measured from where "
             "Knights Road crosses Street Road, so traffic on Street Road adds to it. Allow for the time "
             "of day when you set out."),
            ("How much of the drive from Bensalem is on Street Road?",
             "The drive from Bensalem is nearly all on Street Road. Of the roughly {mi1} miles from Knights Road to Tri County Collision Center, "
             "about {d1} are on Street Road (PA 132). The last stretch is about {d2} on 2nd Street Pike "
             "(PA 232), then about {d3} on Jaymor Rd to the shop."),
        ],
    },
    "feasterville-trevose-pa": {
        "name": "Feasterville-Trevose", "county": "bucks", "modified": "2026-10-09",
        "opening": [
            "Of all the towns on our Areas We Serve page, Feasterville-Trevose is the closest by road. "
            "Even so, the shop is not in Feasterville or Trevose; it is in Southampton, about {mi1} miles "
            "from Buck Road. We also work on cars for drivers from Richboro, Huntingdon Valley, Bensalem "
            "and Northeast Philadelphia.",
            "Buck Road meets Street Road (PA 132) in Lower Southampton Township, Bucks County. That "
            "crossroads is about {min} minutes from our shop in light traffic. When something hits your "
            "car, our number is worth dialing before any other.",
        ],
        "faq": [
            ("How far is Tri County Collision Center from Feasterville-Trevose?",
             "Tri County Collision Center is about {mi1} miles and {min} minutes from Buck Road and Street Road "
             "without traffic, the shortest drive of any town on the shop's Areas We Serve page. It is in Southampton "
             "at 995 Jaymor Rd, Southampton, PA 18966, not in Feasterville-Trevose itself."),
            ("What is the route from Buck Road?",
             "Head along Street Road (PA 132) for about {d1}, turn left onto 2nd Street Pike (PA 232) for "
             "about {d2}, and turn right onto Jaymor Rd; the shop is about {d3} along."),
            ("Is the drive the same from the Trevose side?",
             "The figure on this page starts at Buck Road and Street Road in Feasterville. The Trevose side "
             "of Feasterville-Trevose runs longer, so allow a few more minutes from there."),
            ("Does the trip from Buck Road use the turnpike?",
             "Neither the turnpike nor an interstate. The drive from Buck Road runs on Street Road "
             "(PA 132), then 2nd Street Pike (PA 232), then Jaymor Rd, about {mi1} miles in all, with no "
             "toll road along the way."),
            ("Is Tri County Collision Center part of a chain?",
             "No, Tri County Collision Center is family owned and operated, not a chain or a franchise, and it "
             "works from 995 Jaymor Rd, Southampton, PA 18966, about {min} minutes from Buck Road and "
             "Street Road without traffic."),
        ],
    },
    "langhorne-pa": {
        "name": "Langhorne", "county": "bucks", "modified": "2026-10-09",
        "opening": [
            "Langhorne is one of the longer trips to our door, and we'd rather say so up front. "
            "Tri County Collision Center is in Southampton, about {mi} miles from the middle of the borough. "
            "Drivers from Bensalem, Feasterville-Trevose, Richboro and Northeast Philadelphia bring their "
            "cars to us too.",
            "The borough's center is where Maple Avenue (PA 213) crosses Bellevue Avenue, in Langhorne, "
            "Bucks County. Without traffic the drive from there takes about {min} minutes. After a crash, "
            "a call to us is a good first move.",
        ],
        "faq": [
            ("Isn't Southampton a long way from Langhorne?",
             "Southampton is about {mi} miles and {min} minutes from Maple Avenue and Bellevue Avenue "
             "without traffic, and Tri County Collision Center is there, at 995 Jaymor Rd, Southampton, PA 18966. "
             "It is a longer drive than some, which is why this page shows the route and the shop's case "
             "for making it."),
            ("Does the drive from Langhorne use an interstate?",
             "The recorded route uses no interstate: Maple Avenue (PA 213), Bridgetown Pike, Bustleton "
             "Pike, Street Road (PA 132), 2nd Street Pike (PA 232) and Jaymor Rd, in that order."),
            ("Does an estimate cost anything?",
             "No, at Tri County Collision Center estimates are free and there is no obligation, whichever town "
             "you come from."),
            ("Will my car come back clean?",
             "Yes, at Tri County Collision Center vehicles are detailed inside and out after every repair."),
            ("Is Tri County Collision Center certified for my car's brand?",
             "Tri County Collision Center is factory-certified for 12 brands: INFINITI, Nissan, Hyundai, Kia, "
             "Acura, Honda, GM, Chrysler, Ford, Dodge, Subaru and Jeep. That list is the same whether you "
             "drive in from Langhorne or from next door."),
        ],
        "steps": ("head", "roundabout", "continue", "follow", "follow", "last"),
    },
    "richboro-pa": {
        "name": "Richboro", "county": "bucks", "modified": "2026-10-09",
        "opening": [
            "Richboro drivers have one of the simplest trips to Tri County Collision Center: stay on one road "
            "until the last turn. The shop is in Southampton, about {mi1} miles from the Richboro "
            "crossroads, not in Richboro. We see cars from Feasterville-Trevose, Warminster, "
            "Jamison and Langhorne as well.",
            "Richboro's crossroads is 2nd Street Pike (PA 232) at Almshouse Road, in Northampton Township, "
            "Bucks County. From it the shop is about {min} minutes away with no traffic. Make us your "
            "first call when the damage is done, and decide the rest after.",
        ],
        "faq": [
            ("Does Tri County Collision Center have a shop in Richboro?",
             "Tri County Collision Center has no shop in Richboro. It is at 995 Jaymor Rd, Southampton, PA 18966, "
             "about {mi1} miles and {min} minutes from 2nd Street Pike and Almshouse Road without "
             "traffic."),
            ("Is it really one road from Richboro?",
             "The drive from Richboro is nearly all on 2nd Street Pike. From Almshouse Road, head along 2nd Street Pike (PA 232) for about {d1}, keep right "
             "to stay on it for about {d2}, then turn right onto Jaymor Rd; the shop is about {d3} "
             "along."),
            ("My insurer named a different shop. Do I have to use it?",
             "You do not have to use your insurer's shop. In Pennsylvania the choice of collision shop belongs to you, and an insurer "
             "cannot make you use the one it prefers. Our post on {rtc} goes through the law."),
            ("Are the technicians certified?",
             "Yes, Tri County Collision Center's technicians are ASE and I-CAR Gold Class certified."),
            ("Is Tri County Collision Center in the same county as Richboro?",
             "Yes, Richboro's crossroads is in Northampton Township and the shop is in Upper Southampton "
             "Township, and both townships are in Bucks County. The drive between them is about {mi1} "
             "miles."),
        ],
    },
    "warminster-pa": {
        "name": "Warminster", "county": "bucks", "modified": "2026-10-09",
        "opening": [
            "A Southampton shop on a Warminster page needs explaining, so here it is: Tri County Collision Center "
            "is not in Warminster, and the drive from Warminster's crossroads is about {mi1} miles. We "
            "also repair cars from Hatboro, Horsham, Jamison and Willow Grove.",
            "York Road (PA 263) meets Street Road in Warminster Township, Bucks County, and the drive "
            "time from that junction is about {min} minutes with no traffic. Call us after an accident, "
            "before the car goes anywhere else.",
        ],
        "faq": [
            ("Why is a Southampton shop on a Warminster page?",
             "Because Tri County Collision Center repairs cars for Warminster drivers, and the shop, at 995 "
             "Jaymor Rd, Southampton, PA 18966, is about {mi1} miles and {min} minutes from York Road and "
             "Street Road without traffic. It is not in Warminster, and this page says so."),
            ("Which way do I drive from York Road and Street Road?",
             "Take York Road (PA 263) for about {d1}, turn left onto East County Line Road for about "
             "{d2}, turn left onto James Way for about {d3}, then turn right onto Jaymor Rd; the shop is "
             "about {d4} along."),
            ("Where does the drive time on this page start?",
             "The Warminster drive time starts at the junction of York Road (PA 263) and Street Road in "
             "Warminster Township. Warminster is a big township, so if you start near its edges, expect "
             "the trip to run longer or shorter than that."),
            ("Is the repair work guaranteed?",
             "Tri County Collision Center gives a lifetime warranty on all repair work, for Warminster drivers as "
             "for everyone else."),
            ("Which part of the drive from Warminster is longest?",
             "East County Line Road, at about {d2}. York Road (PA 263) takes up about {d1} before it, "
             "and James Way and Jaymor Rd after it are shorter still."),
        ],
    },
    "hatboro-pa": {
        "name": "Hatboro", "county": "montgomery", "modified": "2026-10-09",
        "opening": [
            "Tri County Collision Center isn't in Hatboro. The borough belongs to Montgomery County, while the "
            "shop sits in Upper Southampton Township, Bucks County, roughly {mi1} miles from York Road. "
            "Drivers from Horsham, Willow Grove, Warminster and Huntingdon Valley come to us too.",
            "York Road meets Byberry Road at the heart of Hatboro borough, and from that corner the shop "
            "is about {min} minutes away with the roads clear. Right after the crash, before anyone else "
            "touches the car, phone us.",
        ],
        "faq": [
            ("Is Tri County Collision Center in Hatboro?",
             "Tri County Collision Center is not in Hatboro itself; it is at 995 Jaymor Rd, Southampton, PA 18966, in "
             "Bucks County, about {mi1} miles and {min} minutes from York Road and Byberry Road without "
             "traffic."),
            ("What is the drive from Hatboro like?",
             "Five short legs: Byberry Road for about {d1}, Davisville Road for about {d2}, East County "
             "Line Road for about {d3}, James Way for about {d4}, and Jaymor Rd for the last {d5} or "
             "so."),
            ("Does it matter that Hatboro is in Montgomery County?",
             "No, crossing from Montgomery County into Bucks County changes nothing about the repair: the "
             "same certified technicians, and the same lifetime warranty on all repair work."),
            ("Can I pick Tri County Collision Center if my insurer prefers another shop?",
             "Yes, under Pennsylvania law the decision about where your car is repaired is yours, "
             "whatever your insurer would prefer; the {rtc_title} post lays out the details."),
            ("Will Tri County Collision Center talk to my insurance company for me?",
             "Yes, dealing with your insurer, paperwork and all, is part of the job at Tri County "
             "Collision Center, and the shop works with all major insurance companies."),
        ],
    },
    "horsham-pa": {
        "name": "Horsham", "county": "montgomery", "modified": "2026-10-09",
        "opening": [
            "From Horsham, Tri County Collision Center is a Bucks County shop across the county boundary in "
            "Southampton, about {mi1} miles from Easton Road. It is not in Horsham, and this page won't "
            "suggest otherwise. Hatboro, Willow Grove, Warminster and Huntingdon Valley are on our list "
            "of towns, too.",
            "Easton Road meets Horsham Road in Horsham Township, Montgomery County, about {min} minutes "
            "from our shop on open roads. So when a crash leaves you with a damaged car, ring us before "
            "you commit it anywhere.",
        ],
        "faq": [
            ("Is there a Tri County Collision Center shop in Horsham?",
             "Tri County Collision Center has no shop in Horsham; its shop is at 995 Jaymor Rd, Southampton, PA 18966, about {mi1} miles and "
             "{min} minutes from Easton Road and Horsham Road without traffic."),
            ("How do I drive from Horsham to the shop?",
             "Most of the trip is West County Line Road, about {d3} of it. You reach it by Horsham Road "
             "and Blair Mill Road, and you leave it for James Way and then Jaymor Rd, where the shop is."),
            ("Can Tri County Collision Center repair a work truck from Horsham?",
             "Yes, alongside cars, Tri County Collision Center takes on work vehicles and fleets; its "
             "{commercial} page explains how."),
            ("What if something isn't right after the repair?",
             "Tri County Collision Center stands behind the work with a lifetime warranty on all repair work: if "
             "anything isn't right, the shop will make it right."),
            ("Is Horsham farther from the shop than Hatboro?",
             "Horsham is a little farther than Hatboro by road; from Horsham's crossroads the drive is "
             "about {mi1} miles and {min} minutes without traffic."),
        ],
    },
    "huntingdon-valley-pa": {
        "name": "Huntingdon Valley", "county": "montgomery", "modified": "2026-10-09",
        "opening": [
            "Huntingdon Valley is a short trip to Tri County Collision Center, but it's still a trip: the shop is "
            "in Southampton, over the Bucks County line, not in Huntingdon Valley. From Wynkoop Avenue it "
            "is about {mi1} miles away. We repair cars for drivers from Northeast Philadelphia, Willow "
            "Grove, Feasterville-Trevose and Jenkintown too.",
            "Huntingdon Pike (PA 232) crosses Wynkoop Avenue in Lower Moreland Township, Montgomery "
            "County, and that crossroads is about {min} minutes from us on empty roads. If you've had an "
            "accident, give us a call first and keep your options open.",
        ],
        "faq": [
            ("Is Tri County Collision Center located in Huntingdon Valley?",
             "Tri County Collision Center is not located in Huntingdon Valley; its address is 995 Jaymor Rd, Southampton, PA 18966, about "
             "{mi1} miles and {min} minutes from Huntingdon Pike and Wynkoop Avenue without traffic."),
            ("What road do I take from Huntingdon Valley?",
             "Huntingdon Pike (PA 232) carries you about {d1} toward Southampton, changing its name to "
             "2nd Street Pike on the way, and a left onto Jaymor Rd leaves about {d2} to the shop."),
            ("Does Tri County Collision Center fix dents without repainting?",
             "Yes, Tri County Collision Center's paintless dent repair fixes door dings and hail dents without repainting, and the "
             "{pdr} page explains when it works."),
            ("Is Huntingdon Valley the closest town to the shop?",
             "Huntingdon Valley is not quite the closest: by road, Feasterville-Trevose is closer. From Huntingdon Pike and Wynkoop Avenue "
             "the drive is still one of the shortest of any town on the shop's Areas We Serve page."),
            ("Do I pay for an estimate?",
             "You don't: Tri County Collision Center's estimates cost nothing and come with no obligation."),
        ],
    },
    "jenkintown-pa": {
        "name": "Jenkintown", "county": "montgomery", "modified": "2026-10-09",
        "opening": [
            "Jenkintown is the longest drive of any Montgomery County town we serve, and we'd rather you "
            "hear it from us. Tri County Collision Center is in Southampton, Bucks County, not Jenkintown, about "
            "{mi1} miles from Old York Road. Willow Grove, Huntingdon Valley, Hatboro and Horsham drivers "
            "make the trip as well.",
            "Old York Road meets West Avenue in Jenkintown borough, Montgomery County. With no traffic, "
            "that corner is about {min} minutes from the shop. Whatever happened to the car, a call to us "
            "before anything else is the right start.",
        ],
        "faq": [
            ("Why would a Jenkintown driver go to Southampton?",
             "Tri County Collision Center is not in Jenkintown; it is about {mi1} miles and {min} minutes away, "
             "without traffic, at 995 Jaymor Rd, Southampton, PA 18966. The drive is longer than a trip "
             "to a closer shop, and the proof section on this page sets out what it buys."),
            ("Is there a straight road from Jenkintown?",
             "No single road runs straight through. The route winds out of Jenkintown on West Avenue, "
             "Newbold Road, Washington Lane and Susquehanna Road, then takes Valley Road for about {d5}, "
             "Welsh Road (PA 63) for about {d6} and Huntingdon Pike (PA 232) for about {d7}, and ends on "
             "Jaymor Rd at the shop."),
            ("Does Tri County Collision Center fix auto glass?",
             "Yes, Tri County Collision Center fixes windshields, side windows and rear windows. The {glass} page has the details."),
            ("Is the drive shorter from other parts of Jenkintown?",
             "The drive from other parts of Jenkintown can be longer or shorter. The time on this page, about {min} minutes without traffic, "
             "starts at Old York Road and West Avenue in the borough."),
            ("Will I have to deal with the insurance company myself?",
             "No, Tri County Collision Center takes on the paperwork and the conversations with your insurer, and "
             "it works with all major insurance companies."),
        ],
    },
    "willow-grove-pa": {
        "name": "Willow Grove", "county": "montgomery", "modified": "2026-10-09",
        "opening": [
            "Willow Grove is in Montgomery County; Tri County Collision Center is a short hop into the next "
            "county, in Southampton, about {mi1} miles from the Easton Road junction. The shop isn't in "
            "Willow Grove, and it has customers in Hatboro, Horsham, Huntingdon Valley and Jenkintown "
            "too.",
            "Easton Road and York Road come together in Upper Moreland Township, and from that junction "
            "the shop is about {min} minutes away on quiet roads. Before a body shop is chosen for you, "
            "choose to call us.",
        ],
        "faq": [
            ("Does Tri County Collision Center have a Willow Grove location?",
             "No, Tri County Collision Center's shop is at 995 Jaymor Rd, Southampton, PA 18966, about {mi1} miles and {min} minutes "
             "from Easton Road and York Road without traffic."),
            ("Which road does most of the work from Willow Grove?",
             "Davisville Road does most of the work from Willow Grove. You spend only about {d1} on York Road (PA 611) before turning onto it, "
             "and it then carries you about {d2}, most of the trip. East County Line Road, James Way and "
             "Jaymor Rd finish it off."),
            ("Does Tri County Collision Center repair major collision damage?",
             "Yes: minor and major damage alike, backed by a lifetime warranty on all repair work. See "
             "the {collision} page for how a repair goes, from the first look to the finished car."),
            ("How long is the drive in traffic?",
             "In traffic the drive from Willow Grove runs longer than about {min} minutes. That figure is a routing on "
             "empty roads from Easton Road and York Road, so rush hour around the junction will stretch "
             "it."),
            ("Who owns Tri County Collision Center?",
             "Tri County Collision Center is family owned and operated, and the business runs from "
             "its shop on Jaymor Rd in Southampton, Bucks County."),
        ],
    },
    "northeast-philadelphia": {
        "name": "Northeast Philadelphia", "origin": "Somerton", "county": "philadelphia",
        "modified": "2026-10-09",
        "opening": [
            "Tri County Collision Center is in Southampton, Bucks County, not in Northeast Philadelphia, and the "
            "Somerton end of the Northeast is close: about {mi1} miles away. The far side of the "
            "Northeast runs longer. We also repair cars for drivers from Feasterville-Trevose, Huntingdon "
            "Valley, Bensalem and Willow Grove.",
            "In Somerton, Bustleton Avenue meets Byberry Road inside the City of Philadelphia, and from "
            "that corner we're about {min} minutes away without traffic. Crashed in the city? Call us, "
            "then decide where the car goes.",
        ],
        "faq": [
            ("Is Tri County Collision Center in Northeast Philadelphia?",
             "No, Tri County Collision Center is in Southampton, Bucks County, at 995 Jaymor Rd, Southampton, PA 18966: about "
             "{mi1} miles and {min} minutes from Bustleton Avenue and Byberry Road in Somerton, without "
             "traffic."),
            ("How do I get from Somerton to the shop?",
             "From Bustleton Avenue, follow Byberry Road for about {d1}, turn right onto Huntingdon Pike "
             "(PA 232) for about {d2}, where it becomes 2nd Street Pike, then turn left onto Jaymor Rd; the "
             "shop is about {d3} along."),
            ("What about the rest of the Northeast?",
             "The drive time for Northeast Philadelphia is measured from Somerton. The far side of the Northeast runs longer, so allow "
             "extra time if you're starting deeper in the city."),
            ("Can a Philadelphia driver choose a shop outside the city?",
             "Yes, Pennsylvania law lets you choose your collision shop, wherever it is, and your insurer "
             "cannot require its own preferred one. Our {rtc_title} post explains it."),
            ("Will my car be cleaned before I pick it up?",
             "Every repaired vehicle at Tri County Collision Center is detailed inside and out before it goes back "
             "to its owner."),
        ],
    },
}
COUNTY = {"bucks": ("Bucks County, PA", "#area-bucks-county"),
          "montgomery": ("Montgomery County, PA", "#area-montgomery-county"),
          "philadelphia": ("Philadelphia, PA", "#area-philadelphia")}
# Every town's display name, so a nearby card can name a town whose page
# is not built yet. The same names as the hub's.
TOWN_NAMES = {
    "jamison-pa": "Jamison", "bensalem-pa": "Bensalem", "feasterville-trevose-pa": "Feasterville-Trevose",
    "langhorne-pa": "Langhorne", "richboro-pa": "Richboro", "warminster-pa": "Warminster",
    "hatboro-pa": "Hatboro", "horsham-pa": "Horsham", "huntingdon-valley-pa": "Huntingdon Valley",
    "jenkintown-pa": "Jenkintown", "willow-grove-pa": "Willow Grove",
    "northeast-philadelphia": "Northeast Philadelphia"}


# ---------------------------------------------------------------------------
# DERIVATIONS
def mins(r):
    return int(r["minutes"] + 0.5)


def miles_whole(r):
    return int(r["miles"] + 0.5)


def title_for(name: str) -> str:
    """The town title, as a cascade: Greg's ruling of 2026-10-09 (3.95), the
    rule of record. It replaces ruling 4 of 3.80, whose short brand
    "| Tri-County" is now a name variant. The Jamison pattern first, which
    no town fits with the full name; then the town and the service before
    the name; then the Jamison pattern without the name. The title law's
    tiebreak: when the brand does not fit, the brand drops, never the
    service or the city."""
    t = f"Collision Repair for {name}, PA | {audit.NAP_NAME}"
    if len(t) > TITLE_MAX:
        t = f"{name} Collision Repair | {audit.NAP_NAME}"
    if len(t) > TITLE_MAX:
        t = f"Collision Repair for {name}, PA"
    if len(t) > TITLE_MAX:
        raise SystemExit(f"FAILED: no title pattern fits 60 for {name}: {t!r} is {len(t)}")
    return t


def meta_for(name: str, r, origin: str = None) -> str:
    away = f"minutes from {origin}" if origin else "minutes away"
    m = (f"Tri County Collision Center in Southampton repairs cars for {name}, PA drivers, about {mins(r)} "
         f"{away}. Directions from {name}, free estimates, (215) 322-5350.")
    if len(m) > META_MAX:
        m = (f"Tri County Collision Center in Southampton repairs cars for {name}, PA drivers, about {mins(r)} "
             f"{away}. Directions, free estimates, (215) 322-5350.")
    if len(m) > META_MAX:
        # 3.82: a long name with an origin (Northeast Philadelphia, from
        # Somerton) overflows even that; the next step drops "Directions,"
        # and keeps the estimates line and the phone.
        m = (f"Tri County Collision Center in Southampton repairs cars for {name}, PA drivers, about {mins(r)} "
             f"{away}. Free estimates, (215) 322-5350.")
    if len(m) > META_MAX:
        raise SystemExit(f"FAILED: no meta pattern fits 160 for {name}")
    return m


def haversine_mi(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371008.8 * math.asin(math.sqrt(d)) / 1609.344


def nearest(key, n=4):
    p = audit.TOWN_ROUTES[key]["place"][1:]
    return [k for _d, k in sorted((haversine_mi(p, v["place"][1:]), k)
                                  for k, v in audit.TOWN_ROUTES.items() if k != key)[:n]]


def display_road(name: str) -> str:
    """Jaymor Road is written the NAP's way, always."""
    return "Jaymor Rd" if name == "Jaymor Road" else name


def step_html(i, step, style, nbsp, last_i):
    road, ref, mod, bearing, mi = step
    sp_ref = "&nbsp;" if "ref" in nbsp else " "
    sp_dist = "&nbsp;" if "dist" in nbsp else " "
    refs = f" ({ref.replace(' ', sp_ref)})" if ref else ""
    rname = display_road(road)
    phrase = audit.step_miles_phrase(mi)
    dist = phrase.replace(" ", sp_dist, 1) if phrase[0].isdigit() else phrase
    turn = mod.replace("slight ", "").replace("sharp ", "")
    if style == "head":
        return f"<strong>Head {audit.compass_of(bearing)} on {rname}{refs}</strong> for about {dist}."
    if style == "follow":
        verb = "Make a sharp " + turn if mod.startswith("sharp") else "Turn " + turn
        return f"<strong>{verb} onto {rname}{refs}</strong> and follow it for about {dist}."
    if style == "go":
        return (f"<strong>Turn {turn} onto {rname}{refs}</strong> and go {audit.compass_of(bearing)} "
                f"for about {dist}.")
    if style == "roundabout":
        return f"<strong>At the roundabout, continue onto {rname}{refs}</strong> for about {dist}."
    if style == "continue":
        return f"<strong>Continue onto {rname}{refs}</strong> for about {dist}."
    if style == "keep":
        return f"<strong>Keep {turn} to stay on {rname}{refs}</strong> for about {dist}."
    if style == "last":
        return (f"<strong>Turn {turn} onto {rname}</strong>, and the shop is about {dist} along, "
                f"at 995 Jaymor Rd, Southampton, PA 18966.")
    raise SystemExit(f"FAILED: unknown step style {style!r}")


def default_styles(steps):
    out = []
    for i, s in enumerate(steps):
        if i == len(steps) - 1:
            out.append("last")
        elif i == 0:
            # Step 1 begins AT the corner, facing the way (3.65, approved as
            # read): OSRM's first maneuver is a turn only because its route
            # starts a few metres along a cross street, and "turn" means
            # nothing to a driver standing at the crossroads.
            out.append("head")
        elif s[2] == "straight":
            out.append("continue")
        elif i and s[0] == steps[i - 1][0]:
            out.append("keep")
        else:
            out.append("follow")
    return tuple(out)


def fmt_ctx(r):
    ctx = {"min": mins(r), "mi": miles_whole(r), "mi1": f"{round(r['miles'], 1):g}",
           "phone": PHONE, "rtc": RIGHT_TO_CHOOSE, "rtc_steer": RIGHT_TO_CHOOSE_STEERING,
           "rtc_title": RIGHT_TO_CHOOSE_TITLE, "collision": COLLISION_LINK, "commercial": COMMERCIAL_LINK,
           "pdr": PDR_LINK, "glass": GLASS_LINK}
    for i, s in enumerate(r["steps"], 1):
        ctx[f"d{i}"] = audit.step_miles_phrase(s[4])
    return ctx


def text_of(h):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", h)).split())


def details(q, a):
    return (f'        <details>\n          <summary>{html.escape(q, quote=False)}<span class="faq-ico" aria-hidden="true"></span></summary>\n'
            f'          <p>{a}</p>\n        </details>')


# WHAT WE FIX, one card per service, in the family's order (3.87). The
# label, link and line all come from audit.SERVICES, the one table (3.90):
# home's router, this grid and the service pages' Related Services sections
# carry one rendering per service, and the audit fails a card that drifts.


def llms_entry(key, name, r, n_faq, origin=None):
    words = dict(enumerate(audit.COUNT_WORDS))
    away = f"from {origin}" if origin else "away"
    body = (f"Collision repair for drivers from {name}, PA. The shop is not in {name}; it is in "
            f"Southampton, about {miles_whole(r)} miles and {mins(r)} minutes {away} without traffic. "
            f"Driving directions from {name} by road and route number, the "
            f"{words[len(audit.SERVICES)]} services, and "
            f"{words[n_faq]} questions {name} drivers ask.")
    lines = textwrap.wrap(body, width=74)   # 76 with the two-space indent, as the file wraps
    return f"- {BASE}{audit.TOWN_ROUTE_PREFIX}{key}/ :\n" + "\n".join("  " + l for l in lines)


def write_llms(entries: dict):
    """Each built town's entry, replaced in place or added after the hub's."""
    s = open(LLMS, encoding="utf-8").read()
    for key, entry in entries.items():
        url = f"{BASE}{audit.TOWN_ROUTE_PREFIX}{key}/"
        m = re.search(r"(?m)^- " + re.escape(url) + r" :\n(?:  .*\n)*", s)
        if m:
            s = s[:m.start()] + entry + "\n" + s[m.end():]
        else:
            hub = re.search(r"(?m)^- " + re.escape(HUB) + r" :\n(?:  .*\n)*", s)
            at = hub.end() if hub else s.index("## Blog posts")
            s = s[:at] + entry + "\n" + s[at:]
    with open(LLMS, "w", encoding="utf-8") as f:
        f.write(s)


# ---------------------------------------------------------------------------
def build(key: str) -> tuple:
    c = CONTENT[key]
    r = audit.TOWN_ROUTES[key]
    name = c["name"]
    slug = audit.TOWN_ROUTE_PREFIX + key
    out = os.path.join(ROOT, "docs", slug, "index.html")
    url = BASE + slug + "/"
    title, meta = title_for(name), meta_for(name, r, c.get("origin"))
    ctx = fmt_ctx(r)
    eyebrow, area_ref = COUNTY[c["county"]]
    area_place = next(x for x in audit.AREA_SERVED if x[1].startswith(name + ","))

    def built(href):
        return os.path.exists(os.path.normpath(os.path.join(os.path.dirname(out), href, "index.html")))

    def card(href, ttl, line=None):
        body = (f"            <div class=\"svc-card-body\">\n              <h3>{ttl}</h3>\n"
                + (f"              <p>{line}</p>\n" if line else "") + "            </div>\n")
        if not built(href):
            return f'          <div class="svc-card" data-pending-href="{href}">\n{body}          </div>'
        return f'          <a class="svc-card" href="{href}">\n{body}          </a>'

    fix_cards = "\n".join(card(f"../{path}", html.escape(lbl, quote=False), html.escape(ln, quote=False))
                          for path, lbl, ln in audit.SERVICES)

    chrome = open(CHROME, encoding="utf-8").read()
    head_assets = chrome[chrome.index("  <!-- No analytics tag yet."):chrome.index("  <!-- One @graph.")]
    body_top = chrome[chrome.index("<body>"):chrome.index("  <main>")]
    body_end = chrome[chrome.index("  </main>") + len("  </main>\n"):]
    graph = json.loads(re.search(r'(?s)<script type="application/ld\+json">(.*?)</script>', chrome).group(1))["@graph"]
    biz = next(n for n in graph if n["@type"] == "AutoBodyShop")

    home = open(HOME, encoding="utf-8").read()
    figs = re.findall(r'(?s)          <figure class="ba">.*?</figure>\n', home)
    pick = [f for f in figs if any(j in f for j in ("job2-", "job5-", "job4-"))]
    assert len(figs) == 5 and len(pick) == 3, (len(figs), len(pick))
    ask = re.search(r'(?s)(        <!-- THE ASK, JOINED TO THE PROOF MOMENT.*?</div>\n)      </div>\n    </section>',
                    re.search(r'(?s)id="real-repairs".*?</section>', home).group(0)).group(1)
    rhead = re.search(r'(?s)(        <div class="sec-head">\n          <h2 class="sec-title">Real Repairs</h2>.*?<div class="repairs-grid">\n)', home).group(1)
    promise = re.search(r'(?s)    <section class="dark field-ox" id="start">.*?</section>\n', home).group(0)
    coll = open(COLLISION, encoding="utf-8").read()
    stats = re.findall(r'(?s)          <div class="stat">\n(.*?)          </div>\n',
                       re.search(r'(?s)<section class="statband" id="proof".*?</section>', coll).group(0))
    assert len(stats) == 3, len(stats)
    figure_cards = "".join('          <article class="card card-figure">\n' + st + '          </article>\n'
                           for st in stats)

    faq = [(q, a.format(**ctx)) for q, a in c["faq"]]
    opening = [p.format(**ctx) for p in c["opening"]]
    origin = c.get("origin", name)
    # An origin page names only the origin here: the H1 directly above names
    # the place, and ", in {name}" wrapped the lead to six lines at 360 and
    # pushed Call under the call bar (proposed-changes.md 3.82).
    lead = (f"Tri County Collision Center is a family-owned body shop in Southampton, about {mins(r)} minutes from "
            f"{origin}. Factory-certified for 12 brands, with a lifetime warranty on all repair work.")
    corner = c.get("corner_names", tuple(r["corner"][:2]))
    intro = ((f"From {origin}, at the crossroads of " if origin != name else "From the crossroads of ")
             + f"{corner[0]} and {corner[1]}, the drive is about "
             f"{round(r['miles'], 1):g} miles and takes about {mins(r)} minutes without traffic.")
    styles = c.get("steps", default_styles(r["steps"]))
    nb = c.get("nbsp", tuple({"ref", "dist"} for _ in r["steps"]))
    assert len(styles) == len(r["steps"]) == len(nb), (key, len(styles), len(r["steps"]), len(nb))
    steps = "\n".join(f"                <li>{step_html(i, s, st, n, len(r['steps']) - 1)}</li>"
                      for i, (s, st, n) in enumerate(zip(r["steps"], styles, nb)))
    alt = f"\n              <p>{c['alt']}</p>" if c.get("alt") else ""
    near = c.get("nearby", tuple(nearest(key)))
    sec_id = "for-" + (key[:-3] if key.endswith("-pa") else key)

    nodes = [
        biz,
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": meta,
         "inLanguage": "en-US", "dateModified": c["modified"],
         "isPartOf": {"@id": BASE + "#business"}, "about": {"@id": url + "#service"},
         "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "Service", "@id": url + "#service", "name": f"Collision Repair for {name}, PA",
         "serviceType": "Collision Repair", "url": url, "provider": {"@id": BASE + "#business"},
         "areaServed": [{"@type": area_place[0], "name": area_place[1],
                         "containedInPlace": {"@id": BASE + area_ref}}]},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Areas We Serve", "item": HUB},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": text_of(a)}}
            for q, a in faq]},
    ]
    jsonld = "\n".join("  " + l for l in json.dumps({"@context": "https://schema.org", "@graph": nodes},
                                                     indent=2, ensure_ascii=False).splitlines())
    frame = ("--frame jamison" if key == "jamison-pa"
             else f'--frame town --town {key} --name "{c.get("origin", name)}"')
    head_comment = c.get("head") or f"""<!-- ============================================================
       {name.upper()}, A TOWN PAGE OF THE AREAS TIER, built by
       scripts/build-town.py from the Jamison template (3.62 to 3.76) in run
       two (3.77 onward), proposed-changes.md, which holds every per-town
       sentence as a pair. Every drive figure, road, turn and compass word
       is TOWN_ROUTES[{key!r}] in scripts/audit.py, the routing the strategy
       chat verified independently (3.78), and the audit's routing check
       gates the page. The township, county and crossroads are
       OpenStreetMap's (3.81). Nothing about {name} that a map cannot check
       is on this page.

       BUILD ORDER: this page first, then scripts/prepare-map-image.py
       {frame}, which draws between the MAP markers. Rebuilding the page
       empties them, and the audit fails a town page with an empty map.

       STAGING, DELIBERATE, AND NOT A DEFECT: noindex below, docs/robots.txt
       disallows everything, and the canonical is absolute to the
       production domain. All three come off together at cutover.

       NO PRICE, OFFER, REVIEW OR RATING MARKUP.
       ============================================================ -->"""
    opening_note = c.get("opening_note", "")
    repairs = ('''    <!-- 3. REAL REPAIRS, a template amendment (3.63): THREE of home's five
         pairs, byte for byte, captions as vetted, the prints treatment by
         the same #real-repairs id and classes. Chosen for variety: a
         minivan's front end, a coupe's rear end, an SUV's door dents. The
         cars are the shop's own work; nothing here says they came from the
         town. Pattern text for the variance gate, by this id, in code.
         DIRECTLY UNDER THE PROOF CARDS, ON INK, by Greg's rulings of
         2026-09-29 (3.70): claims first, the photographs proving them
         second. The ground is /collision-repair/'s own treatment of this
         section, dark field-ink, so the dark print shadow, the .dark
         caption tones and the ink ground's buttons are that page's
         existing rules, reused. It closes on home's own Call/Email row. -->
    <section id="real-repairs" class="dark field-ink">
      <div class="wrap">
''' + rhead + "".join(f.replace('src="assets/', 'src="../assets/') for f in pick) + '''        </div>
''' + ask + '''      </div>
    </section>
''')
    crumb_hub = ('<a href="../areas-served/">Areas We Serve</a>' if built("../areas-served/")
                 else '<span data-pending-href="../areas-served/">Areas We Serve</span>')
    nearby_cards = "\n".join(card(f"../{audit.TOWN_ROUTE_PREFIX}{k}/",
                                  f"{TOWN_NAMES[k]}, PA") for k in near)

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  {head_comment}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Ink. The palette lives in assets/site.css; a meta tag cannot read a
       custom property, which is why this one hex is duplicated. -->
  <meta name="theme-color" content="#121B27">

  <title>{html.escape(title, quote=False)}</title>
  <meta name="description" content="{html.escape(meta)}">

  <link rel="canonical" href="{url}">
{ROBOTS_LINE}  <!-- A TOWN PAGE, declared, and exempt from nothing: Greg's ruling of
       2026-09-28, proposed-changes.md 3.62. It carries a real FAQ and has
       to earn its words. The tier's gate is the variance check in
       scripts/audit.py, which compares every town page with its siblings
       and the hub. -->
  <meta name="tri-county-page" content="town">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(meta)}">
  <meta property="og:url" content="{url}">
  <!-- NO IMAGE ON THIS PAGE, SO ITS SHARE CARD FOLLOWS HOME'S, byte for
       byte, as /contact-us/'s does. It moves to a real shop photograph
       after the shoot. -->
  <meta property="og:image" content="https://tricountycollision.com/assets/img/hero-wrecked-sedan-in-shop.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="800">
  <meta property="og:image:alt" content="A red sedan with its front end crushed and the bumper torn loose, in the shop before repair.">
  <meta name="twitter:card" content="summary_large_image">

{head_assets}  <!-- One @graph. The AutoBodyShop node repeats in full on every page under
       the SAME @id, so the whole site resolves to one business entity.
       geo IS THE SHOP'S VERIFIED PIN, GEO_LAT and GEO_LON in scripts/audit.py,
       and there is no per-town geo: {name} is where the reader is, not
       where the shop is. The town is named once, as the areaServed of this
       page's own Service node. sameAs IS DELIBERATELY ABSENT until the
       client's verified list lands. The FAQPage node is generated from the
       same strings as the visible questions, so the two cannot differ. -->
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
{body_top}  <main>

    <!-- 1. THE COMPACT OX HEADER, the page-header identity, extended to the
         areas tier by Greg's ruling of 2026-09-28 (3.61, amended in 3.62).
         It carries the call, like /contact-us/'s.
         THE LEAD IS TWO SENTENCES, a template rule (3.71, Greg's ruling of
         2026-09-29). The FIRST is per-town: name, place, routed minutes,
         which the routing check reads. The SECOND is the same two claims
         on every town page BY DESIGN, the brand count (BRAND_COUNT, which
         the brand-count check reads here) and the lifetime warranty, both
         the proof cards' own: true claims do not vary by town, and a
         paraphrase per town would be fake variance. This header is not a
         pattern section, so that sentence counts in the town-to-town
         measure, and 3.71 records what it adds to every pair. -->
    <section class="hero dark field-ox" id="town-head">
      <div class="wrap">
        <!-- Mirrors the BreadcrumbList, same labels and same order. -->
        <nav class="crumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="../">Home</a></li>
            <li>{crumb_hub}</li>
            <li>{html.escape(name)}</li>
          </ol>
        </nav>
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h1>Collision Repair for {html.escape(name)}, PA</h1>
          <p class="lead">{html.escape(lead, quote=False)}</p>
          <div class="cta-row">
            <a class="btn" href="tel:+12153225350">Call (215) 322-5350</a>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. WHY DRIVERS PASS CLOSER SHOPS, ONE PROOF SECTION, as cards: a
         template amendment (3.67, Greg's rulings of 2026-09-29). It replaces
         three stacked proof moments: the header's chip row (3.63), the stat
         band (3.62) and the ox argument band (3.64, 3.66). Each of those
         records stands; this is the supersession. It is the one white band
         under the ox header.
         EVERY LINE WAS ALREADY VETTED; NOTHING HERE IS NEWLY WRITTEN:
         - the lead is 3.64's first paragraph cut at "on us.", the new
           sentence boundary approved by Greg in the 3.67 brief;
         - the three figure cards are the stat band's own lines, lifted
           from /collision-repair/ by this builder so they cannot drift,
           and the review count, rating and date are the constants the
           audit reads (REVIEW_COUNT, REVIEW_RATING, REVIEW_COUNTED_ON);
         - the right-to-choose and free-estimates cards are 3.64's
           sentences, and "Insurance paperwork handled" is the vetted chip,
           a headline card with no support line, by ruling.
         IT KEEPS THE .statband CLASS, which gives it the band's white
         ground. The figures stand still, as the markup has them (3.85).
         BYTE-IDENTICAL ON EVERY TOWN PAGE BY DESIGN: pattern text for the
         variance gate, by this id, in code. It closes on its Call/Email
         row, the section's ask. -->
    <section class="statband" id="why-the-trip">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">Why drivers pass closer shops</h2>
          <p>A collision repair is two drives: one to drop the car off, one to pick it up. Everything between them is on us.</p>
        </div>
        <div class="grid3">
{figure_cards}          <!-- ROW TWO WEARS ROW ONE'S GRAMMAR (3.68, Greg's rulings of
               2026-09-29): each card a vetted chip claim SPLIT into a big ox
               word and a bold label, never reworded. Its big word is .fig-n,
               which shares .stat-n's look. It was split off so the counting
               effect stayed on the three figures, and that effect is now
               withdrawn (3.85). Cards 5 and 6 carry support lines quoted byte for byte from /collision-repair/, which ships both sentences. -->
          <article class="card card-figure">
            <span class="fig-n">Free</span>
            <span class="stat-l">Estimates</span>
            <span class="stat-s">Estimates are free and there is no obligation.</span>
          </article>
          <article class="card card-figure">
            <span class="fig-n">Handled</span>
            <span class="stat-l">Insurance paperwork</span>
            <span class="stat-s">We handle the paperwork and communication so you don't have to.</span>
          </article>
          <article class="card card-figure">
            <span class="fig-n">Detailed</span>
            <span class="stat-l">After every repair</span>
            <span class="stat-s">Vehicles detailed inside and out after every repair.</span>
          </article>
        </div>
        <div class="cta-row">
          <a class="btn" href="tel:+12153225350">Call (215) 322-5350</a>
          <a class="btn btn-ghost" href="mailto:contact@tricountycollision.com">Email the shop</a>
        </div>
      </div>
    </section>

{repairs}
    <!-- 4. THE OPENING, centred, the service pages' intro shape (Greg's
         3.52 ruling). The PROSE is per-town (3.63): run two writes each
         town's own opening to this pattern and never reuses these
         sentences; the variance gate holds them apart. The neighbors are
         only places the shop's own hub already serves.
         NO ASK OF ITS OWN SINCE 3.64, on Greg's ruling: the ask 3.62 put
         here was scaffolding for one askless run, and the proof section
         above now closes on an ask its own copy argues for.
{opening_note}         TWO PARAGRAPHS, a template rule (3.72, Greg's ruling of
         2026-09-29): the second ends on the call-first sentence, so the
         paragraph ends on the ask. The ask is in words only: 3.64's ruling
         still holds, and the section carries no Call button of its own. -->
    <section id="{sec_id}">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">For drivers from {html.escape(name)}</h2>
        </div>
        <div class="prose" style="text-align:center">
          <p>{opening[0]}</p>
          <p>{opening[1]}</p>
        </div>
      </div>
    </section>

    <!-- 5. THE DIRECTIONS CARD, a template amendment (3.65, Greg's ruling):
         the map, then the body in the order 3.75 ruled (Greg, 2026-09-29,
         superseding 3.74's chip at the top): the steps and the alternative
         route, which are the content, open the body; then the Call, the
         primary ask; and last the getaway kit, "Open in Google Maps" and
         the drive-time chip sharing one row, the address beneath. Open in
         Google Maps is an EXIT action, so it may not outrank the conversion
         action: content, then the ask, then the utilities.
         EVERY ROUTE FACT HERE IS THE RECORDED ROUTING, TOWN_ROUTES in
         scripts/audit.py, and its town_route_findings fails the page if a turn
         word, a road, a step's distance or a minute count disagrees with it.
         THE CHIP'S TILDE IS THE QUALIFIER'S FIRST HALF: "~15 min" hedges
         the number, and the intro sentence ABOVE it in this same card, at
         the head of the steps, carries the full "about 15 minutes without
         traffic" (the chip sits in the kit since 3.75). Together they
         satisfy the qualifier rule, so a future sitting must not strip the
         chip for lacking it.
         The street is always "Jaymor Rd", no period, and the number only in
         the full canonical address, which scripts/audit.py enforces.
         NON-BREAKING SPACES IN THE STEPS, a template rule (3.76): a figure
         and its unit ("about 4&nbsp;miles") and a route number's two halves
         ("(PA&nbsp;263)") are joined by &nbsp; wherever a wrap split them,
         and run two's builder does the same for every town's steps. The
         routing check reads straight through them (test section 26). -->
    <section id="getting-here" class="band-panel">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">Getting to the shop from {html.escape(name)}</h2>
        </div>
        <div class="dir-card">
          <!-- THE MAP DRAWS THE PRIMARY ROUTE ONLY, Greg's ruling of
               2026-09-28 (3.63): it shows exactly what the steps below say.
               Drawn by scripts/prepare-map-image.py {frame} from one
               Overpass query and the recorded routing; rebuilt after this
               page, never by hand. -->
          <figure class="map-box dir-map">
            <!-- MAP:BEGIN, written by scripts/prepare-map-image.py -->
            <!-- MAP:END -->
            <figcaption class="map-credit">Map data &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors</a>, available under the <a href="https://opendatacommons.org/licenses/odbl/" target="_blank" rel="noopener">Open Database License</a>.</figcaption>
          </figure>
          <div class="dir-body">
            <div class="prose">
              <p>{intro}</p>
              <ol class="numbered">
{steps}
              </ol>{alt}
            </div>
            <div class="cta-row">
              <a class="btn" href="tel:+12153225350">Call (215) 322-5350</a>
            </div>
            <div class="dir-utils">
              <div class="dir-top">
                <a class="btn btn-ghost btn-sm" href="{MAPS_HREF}" target="_blank" rel="noopener">Open in Google Maps</a>
                <span class="dir-chip"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>~{mins(r)} min from {html.escape(origin)}</span>
              </div>
              <p class="dir-address"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg><a href="{MAPS_HREF}" target="_blank" rel="noopener">995 Jaymor Rd, Southampton, PA 18966</a></p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. WHAT WE FIX. Each card restates only what its own page's meta
         description already says. No demand claim: nothing here says which
         repair {name} drivers ask for most, because nobody knows. -->
    <section id="fix">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">What we fix for {html.escape(name)} drivers</h2>
          <p>Pick the one that fits what happened. Each page explains how the repair works.</p>
        </div>
        <div class="grid2">
{fix_cards}
        </div>
      </div>
    </section>

    <!-- 7. THE PROMISE BAND, home's #start byte for byte, by Greg's ruling
         of 2026-09-28: the approved promise, not a new one. It carries the
         call, so the band test is met. -->
{promise}
    <!-- 8. THE FAQ, unique to the town, and the geographic objection first,
         answered in its opening sentence. -->
    <section id="faq">
      <div class="wrap" style="max-width:880px">
        <div class="sec-head">
          <h2 class="sec-title">Questions from {html.escape(name)} drivers</h2>
        </div>
{chr(10).join(details(q, a) for q, a in faq)}
      </div>
    </section>

    <!-- 9. NEARBY TOWNS: the four sibling pages nearest {name} by straight
         line between recorded place points (3.81), and the hub. Each is a link
         once its page is built and a pending span until then. -->
    <section id="nearby" class="band-panel">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">Nearby towns we serve</h2>
        </div>
        <div class="grid2">
{nearby_cards}
{card("../areas-served/", "Every town we serve")}
        </div>
      </div>
    </section>

  </main>
{body_end}'''
    # THE CHROME IS THE GENERATOR'S (3.83): the lifted chrome is re-rendered
    # for this page, so the page is marked as the current page in its nav
    # and footer, as every page is.
    import importlib.util
    _spec = importlib.util.spec_from_file_location("sync_chrome", os.path.join(ROOT, "scripts", "sync-chrome.py"))
    _sc = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_sc)
    page = _sc.synced(out, page)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {os.path.relpath(out, ROOT)} {len(page)} bytes; title {len(title)} ({title!r}), "
          f"meta {len(meta)}")
    return llms_entry(key, name, r, len(faq), c.get("origin"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    keys = list(CONTENT) if a.all else a.keys
    for k in keys:
        if k not in CONTENT or k not in audit.TOWN_ROUTES:
            raise SystemExit(f"FAILED: {k} needs both CONTENT here and TOWN_ROUTES in audit.py")
    entries = {k: build(k) for k in keys}
    write_llms(entries)
    return 0


if __name__ == "__main__":
    sys.exit(main())
