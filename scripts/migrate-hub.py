#!/usr/bin/env python3
"""
Migrates /areas-served/, the areas hub, from the live WordPress page, and
prints every change it makes as a before/after pair. proposed-changes.md 3.79.

THE BLOG'S DISCIPLINE (3.57). The live page is read once and cached OUTSIDE
this public repo, and passed in with --src. Every paragraph migrated here is
quoted from that cache and the build refuses to run unless each quotation is
found in it exactly once, so the pairs are anchored to what the live page
actually says. Nothing is invented; what an edit removes is HELD and printed,
not lost.

WHAT IS THE HUB'S OWN. The live page's own copy is about 1,200 words: the
intro, the town blurbs, "Don't see your town", "What doesn't change" and four
FAQs. Everything after them (the "Get Your Free Estimate Today" heading, the
Minor and Major Collision Repair boilerplate, the testimonials, the contact
block and form) also appears on all eleven live town pages, measured, and is
the site-wide boilerplate Greg's rulings exclude. The pagemap's "~2,500
words" counted it.

GREG'S RULINGS THIS FOLLOWS (3.77):
  Q1  every town figure derives from that town's recorded routing
      (TOWN_ROUTES in scripts/audit.py), and the routing check reads the hub:
      each town's blurb is marked data-town="<key>", and a figure outside
      every blurb is refused.
  Q2  bearings and straight-line distances come off; a road stays only where
      that town's route drives it or its corner names it; the five places
      without pages keep their names and lose their distances.
  Q3  the 52 years and the second generation are held pending 4.5; the
      warranty's "parts and labor" takes the vetted "all repair work";
      "towing assistance" migrates flagged and joins the owner questions;
      everything else migrates with pairs and claims-list entries.

    python3 scripts/migrate-hub.py --src /path/outside/repo/hub.html
"""
import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit  # noqa: E402

# The noindex tag follows audit.STAGING (3.94), so a rebuild after cutover
# cannot re-noindex a page. sync-chrome's pass, which every page written
# here goes through, settles the visible banner and the favicon links.
ROBOTS_LINE = ("  " + audit.STAGING_ROBOTS_META + "\n") if audit.STAGING else ""

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "areas-served", "index.html")
CHROME = os.path.join(ROOT, "docs", "deer-season-in-bucks-county-insurance-coverage-next-steps", "index.html")
HOME = os.path.join(ROOT, "docs", "index.html")
BASE = "https://tricountycollision.com/"
URL = BASE + "areas-served/"
MODIFIED = "2026-10-09"

TITLE = "Serving Bucks & Montgomery | Tri County Collision Center"
META = ("Tri County Collision Center serves Bensalem, Warminster, Willow Grove, Northeast Philly and more "
        "from Southampton. ASE/I-CAR Gold certified, lifetime warranty.")
LIVE_TITLE = "Areas We Serve | Collision Repair Bucks & Montgomery County | Tri County"
LIVE_META = ("Tri County Collision Center serves Bensalem, Warminster, Willow Grove, Northeast Philly, "
             "and more from Southampton, PA. ASE/I-CAR Gold certified; lifetime warranty. Call (215) 322-5350.")

PHONE = '<a href="tel:+12153225350">(215) 322-5350</a>'

# ---------------------------------------------------------------------------
# THE PAIRS. (id, live text quoted from the cache, new HTML, reason). A new
# value equal to the live one migrates unchanged. A new value of None is
# HELD: removed from the page, printed, kept in the record.
INTRO = [
    ("lead",
     "When your car is damaged, the question isn't which shop is closest. It's who you trust with the "
     "repair and whether that repair will hold up years from now.",
     None, "unchanged; it is the header's lead"),
    ("intro-2",
     "Tri County Collision Center has been answering that question from Southampton since 1974, family "
     "owned and operated, now in its second generation. Our ASE/I-CAR® Gold technicians work on foreign and "
     "domestic vehicles alike. We're a factory-certified collision center for a dozen major brands. We "
     "accept all major forms of insurance. And every repair is backed by a lifetime warranty. We'll handle "
     "your insurer, keep you informed, and push back when they want a shortcut that isn't right for your "
     "car. That last part is why a lot of people end up here.",
     "Tri County Collision Center has been answering that question from Southampton for years, family owned and "
     "operated. Our ASE/I-CAR® Gold technicians work on foreign and domestic vehicles alike. We're a "
     "factory-certified collision center for a dozen major brands. We accept all major forms of insurance. "
     "And there's a lifetime warranty on all repair work. We'll handle your insurer, keep you informed, and "
     "push back when they want a shortcut that isn't right for your car. That last part is why a lot of "
     "people end up here.",
     "the NAP name; \"since 1974\" and \"now in its second generation\" HELD pending 4.5 (Q3), and "
     "\"for years\" is the rendering /collision-repair/ migrated for the same claim (4.5); the warranty "
     "takes its one vetted rendering with its scope attached (Greg's ruling 3 on the hub, 3.80)"),
    ("intro-3",
     "And under Pennsylvania law, the shop is your call, not your insurance company's. Wherever you're "
     "driving from, that choice belongs to you. The communities below are the ones that keep making it. "
     "Here's where they are, how far out they are, and what to expect when you arrive.",
     "And under Pennsylvania law, the shop is your call, not your insurance company's. Wherever you're "
     "driving from, that choice belongs to you. The communities below are the ones that keep making it. "
     "Here's how far out they are by road, and what to expect when you arrive.",
     "\"where they are\" promised the bearings Q2 took off; the distances are now road-derived"),
]

# (key, name, county group, live blurb, new blurb, reason). The key is the
# TOWN_ROUTES key and the page slug's tail. Jamison's blurb is NEW: the
# pagemap's "add Jamison to the county lists".
TOWNS = [
    ("feasterville-trevose-pa", "Feasterville-Trevose", "bucks",
     "Our nearest neighbor at roughly three miles east of the shop, and a short run back west along the "
     "Street Road corridor. Most Feasterville and Trevose customers are here in under ten minutes. Close "
     "enough that a drop-off costs you a coffee break rather than a morning.",
     "Our nearest neighbor by road: about 6 minutes from Buck Road and Street Road, most of it along the "
     "Street Road corridor. Close enough that a drop-off costs you a coffee break rather than a morning.",
     "bearing and straight-line distance off (Q2); \"under ten minutes\" is true from Buck and Street and "
     "false from the Trevose side (11.0 min, 3.77), so the figure is the routing's own; \"nearest neighbor\" "
     "holds by road, the table's shortest in miles and minutes; Street Road is 1.90 of the 2.92 miles"),
    ("richboro-pa", "Richboro", "bucks",
     "About four miles northeast of us, straight down Second Street Pike (PA-232). One of the few genuinely "
     "direct shots on this list. Ten to fifteen minutes from most of Northampton Township, whether you're "
     "near Council Rock, off Buck Road, or out toward Almshouse Road.",
     "About 8 minutes from 2nd Street Pike and Almshouse Road, straight down Second Street Pike (PA 232). "
     "One of the few genuinely direct shots on this list.",
     "bearing and straight-line distance off (Q2); the range becomes the routing's 8 minutes; Buck Road is "
     "not driven and comes off with its sentence (Q2); the route is PA 232 to the last turn"),
    ("warminster-pa", "Warminster", "bucks",
     "Roughly four miles northwest, which puts most of Warminster Township ten to fifteen minutes out "
     "heading southeast toward us. County Line Road, Jacksonville Road, and York Road (PA-263) all feed "
     "this direction depending on where in the township you start.",
     "About 9 minutes from York Road and Street Road, by York Road (PA 263) and County Line Road.",
     "bearings and straight-line distance off (Q2); the range becomes the routing's 9 minutes; "
     "Jacksonville Road is not driven (Q2)"),
    ("langhorne-pa", "Langhorne", "bucks",
     "About seven miles due east, with Street Road (PA-132) running west from the borough more or less to "
     "our door. Figure fifteen to twenty minutes. Langhorne absorbs a lot of through-traffic between the "
     "Route 1 corridor, the I-95 interchanges, and everyone headed to Sesame Place, which means Langhorne "
     "drivers see more than their share of collisions they didn't cause.",
     "About 16 minutes from Maple Avenue and Bellevue Avenue, by Bridgetown Pike and then Street Road "
     "(PA 132). Langhorne absorbs a lot of through-traffic, including everyone headed to Sesame Place, "
     "which means Langhorne drivers see more than their share of collisions they didn't cause.",
     "bearing and straight-line distance off (Q2); \"Street Road running from the borough more or less to "
     "our door\" is wrong by the routing (2.73 of 8.78 miles); Route 1 and I-95 are not driven (Q2)"),
    ("bensalem-pa", "Bensalem", "bucks",
     "Bucks County's largest township, about eight miles southeast of us. Street Road (PA-132) runs "
     "northwest from Bensalem toward Southampton and handles most of that traffic. Typically fifteen to "
     "twenty minutes depending on where in the township you're starting and how Street Road is behaving "
     "that day.",
     "Bucks County's largest township. About 15 minutes from Knights Road and Street Road, nearly all of it "
     "on Street Road (PA 132), depending on where in the township you're starting and how Street Road is "
     "behaving that day.",
     "bearing and straight-line distance off (Q2); the old Bensalem contradiction (the live Bensalem page "
     "says both 10 to 15 and 15 to 20) dies by derivation: 15; Street Road is 7.12 of the 8.14 miles"),
    ("jamison-pa", "Jamison", "bucks", None,
     "About 15 minutes from York Road and Almshouse Road, by York Road (PA 263), Bristol Road and Second "
     "Street Pike (PA 232).",
     "NEW, the pagemap's \"add Jamison to the county lists\"; every figure and road from its routing"),
    ("huntingdon-valley-pa", "Huntingdon Valley", "montgomery",
     "The shortest drive on this entire page. Barely two miles southwest of us, meaning most of Lower "
     "Moreland Township is heading northeast for about ten minutes. You cross the county line into Bucks "
     "and you're essentially here. Closer than a lot of Huntingdon Valley residents realize.",
     "About 8 minutes from Huntingdon Pike and Wynkoop Avenue, straight along Huntingdon Pike (PA 232). "
     "You cross the county line into Bucks and you're essentially here. Closer than a lot of Huntingdon "
     "Valley residents realize.",
     "\"the shortest drive on this entire page\" is false by the routings (Feasterville-Trevose, 6.0 min "
     "against 7.8); bearings and straight-line distance off (Q2); the figure is the routing's 8"),
    ("hatboro-pa", "Hatboro", "montgomery",
     "Three miles due west, so Hatboro drivers head east along the County Line Road corridor to reach us. "
     "About ten minutes from the middle of the borough. Between York Road and County Line Road, Hatboro "
     "fits a remarkable number of intersections into a small footprint.",
     "About 8 minutes from York Road and Byberry Road, by Byberry Road, Davisville Road and County Line "
     "Road. Between York Road and County Line Road, Hatboro fits a remarkable number of intersections into "
     "a small footprint.",
     "bearings and straight-line distance off (Q2); \"about ten minutes\" becomes the routing's 8"),
    ("willow-grove-pa", "Willow Grove", "montgomery",
     "Under four miles west-southwest, roughly ten to fifteen minutes heading east-northeast. Willow Grove "
     "straddles Abington and Upper Moreland and functions as a real transportation hub, with PA-611, Old "
     "Welsh Road, and Moreland Road all converging in a tight space. We repair a lot of what that produces.",
     "About 11 minutes from Easton Road and York Road, most of it along Davisville Road. Willow Grove "
     "straddles Abington and Upper Moreland and functions as a real transportation hub, with several busy "
     "roads converging in a tight space. We repair a lot of what that produces.",
     "bearings and straight-line distance off (Q2); the range becomes the routing's 11 (10.5, half-up, "
     "3.78); Old Welsh Road and Moreland Road are not driven (Q2), so the roads go unnamed; Davisville "
     "Road is 3.08 of the 4.59 miles"),
    ("horsham-pa", "Horsham", "montgomery",
     "About four miles west-northwest of the shop. Most of Horsham Township is ten to fifteen minutes "
     "east-southeast of here. Horsham's mix of commuter traffic, commercial corridors, and everything from "
     "compacts to work trucks is a good match for a shop that handles both retail and commercial collision "
     "repair.",
     "About 11 minutes from Easton Road and Horsham Road, by Blair Mill Road and County Line Road. "
     "Horsham's mix of commuter traffic, commercial corridors, and everything from compacts to work trucks "
     "is a good match for a shop that handles both retail and commercial collision repair.",
     "bearings and straight-line distance off (Q2); the range becomes the routing's 11"),
    ("jenkintown-pa", "Jenkintown", "montgomery",
     "About six miles southwest, and the longest drive of our Montgomery County communities. Plan on "
     "twenty minutes or so heading northeast, since there's no single straight road between us. Jenkintown "
     "is a walkable borough where people notice whether work was done properly. That suits us.",
     "About 17 minutes from Old York Road and West Avenue, and the longest drive of our Montgomery County "
     "communities, since there's no single straight road between us. Jenkintown is a walkable borough "
     "where people notice whether work was done properly. That suits us.",
     "bearings and straight-line distance off (Q2); \"twenty minutes or so\" becomes the routing's 17; "
     "\"the longest drive of our Montgomery County communities\" holds by the routings (17.1 against "
     "Horsham's 11.3)"),
    ("northeast-philadelphia", "Northeast Philadelphia", "philadelphia",
     "We're straight north of the Northeast, and closer than most people assume. Somerton is about three "
     "and a half miles out. Bustleton is under five. Torresdale, Byberry, and the neighborhoods around "
     "Pennypack Park run a bit farther. Bustleton Avenue and Red Lion Road carry most of that traffic north "
     "across the county line. Plenty of Northeast Philly residents already cross into Bucks to shop; "
     "crossing it for collision repair gets you out of the queue at an overloaded city shop.",
     "The Northeast is closer than most people assume. Somerton is about 9 minutes from Bustleton Avenue "
     "and Byberry Road, by Byberry Road and Huntingdon Pike. Torresdale, Byberry, and the neighborhoods "
     "around Pennypack Park run a bit farther. Plenty of Northeast Philly residents already cross into "
     "Bucks to shop; crossing it for collision repair gets you out of the queue at an overloaded city shop.",
     "\"straight north\" is a bearing (Q2); Somerton's straight-line figure becomes its routing's 9 (8.5, "
     "half-up, 3.78), from the corner Greg ruled (3.78); Bustleton's straight-line figure off; the far side "
     "stays numberless, as ruled; Red Lion Road is not driven, and its sentence was also a bearing"),
]
GROUPS = [("bucks", "Bucks County Communities We Serve"),
          ("montgomery", "Montgomery County Communities We Serve"),
          ("philadelphia", "Philadelphia Neighborhoods We Serve")]

ELSEWHERE = (
    "These are the communities we hear from most, not the limits of who we'll help. Some of our closest "
    "neighbors don't have a page of their own: Bryn Athyn is about two and a half miles out, Ivyland "
    "roughly three, Churchville under four, Holland about five, Newtown around eight. We also repair "
    "vehicles for people who were simply passing through when it happened, and we handle vehicles "
    "registered and insured out of state. If you can get here \u2014 or if your vehicle can. Call "
    "(215) 322-5350 and we'll sort it out.",
    "These are the communities we hear from most, not the limits of who we'll help. Some of our neighbors "
    "don't have a page of their own: Bryn Athyn, Ivyland, Churchville, Holland and Newtown. We also repair "
    "vehicles for people who were simply passing through when it happened, and we handle vehicles "
    "registered and insured out of state. If you can get here, or if your vehicle can, call " + PHONE
    + " and we'll sort it out.",
    "the five places keep their names and lose their distances (Q2), and without distances \"closest\" "
    "is a claim nothing checks, so it goes; the em dash goes (house rule); the phone is a link")

UNCHANGED_1 = (
    "The town on your registration doesn't change how we work. Every vehicle gets our ASE/I-CAR® Gold "
    "technicians and a free, no-obligation estimate that explains what's wrong and why it matters. We're a "
    "factory-certified collision center for INFINITI, Nissan, Hyundai, Kia, Acura, Honda, GM, Chrysler, "
    "Ford, Dodge, Subaru, and Jeep. We accept all major forms of insurance and coordinate directly with your "
    "adjuster (including arguing your case when an insurer's estimate doesn't cover what your vehicle "
    "actually needs).")
BEYOND = (
    "Beyond collision work, we handle commercial and fleet repair, auto glass repair and replacement, "
    "paintless dent repair, towing assistance, rental coordination, and more. Every repair carries our "
    "lifetime warranty on parts and labor. Every vehicle leaves detailed. And we use environmentally "
    "responsible products throughout the shop.",
    "Beyond collision work, we handle commercial and fleet repair, auto glass repair and replacement, "
    "paintless dent repair, ADAS calibration, towing assistance, rental coordination, and more. Every "
    "repair carries our lifetime warranty on all repair work. Every vehicle leaves detailed. And we use "
    "environmentally responsible products throughout the shop.",
    "the warranty takes its one vetted rendering, \"lifetime warranty on all repair work\" (Q3's "
    "amendment); \"towing assistance\" migrates flagged and joins the owner questions (Q3); ADAS "
    "calibration joins the services named, after the four, on Greg's ruling that ADAS appears wherever "
    "the site enumerates its services (3.87)")
HELD_PITCH = ("Fifty-two years in one location, second generation, still family run. That's the whole pitch.",
              "HELD pending 4.5 (Q3): the 52 years and the second generation are the unconfirmed 1974 "
              "claim; without them the paragraph has nothing left to say")

FAQ = [
    ("Do I have to live in one of these towns to bring you my car?",
     "No. These are the areas we hear from most, so we know their roads well, but we repair vehicles for "
     "anyone who can reach us. Where you live has no bearing on the estimate, the warranty, or the work.",
     "No, you don't have to live in one of these towns. These are the areas we hear from most, so we know "
     "their roads well, but we repair vehicles for anyone who can reach us. Where you live has no bearing on "
     "the estimate, the warranty, or the work.",
     "the opener passes the standalone test"),
    ("Which county are you actually in?",
     "Bucks. We're at 995 Jaymor Road, Southampton, PA 18966, close to the Montgomery County line, which is "
     "why customers from Hatboro and Huntingdon Valley get here about as fast as customers from Feasterville.",
     "Tri County Collision Center is in Bucks County, at 995 Jaymor Rd, Southampton, PA 18966, close to the "
     "Montgomery County line, which is why Hatboro and Huntingdon Valley are among our shortest drives.",
     "the opener passes the standalone test; the address takes the NAP's one spelling; \"about as fast as "
     "Feasterville\" is 8 minutes against 6 by the routings, so it becomes what they show: Huntingdon Valley "
     "and Hatboro are the second and third shortest"),
    ("There are closer body shops. Why drive past them?",
     "Because a few extra minutes buy you ASE/I-CAR® Gold technicians, factory-approved repair procedures, "
     "a lifetime warranty, and a shop that will push back on your insurer rather than quietly trimming the "
     "repair to fit their estimate. You'll make that drive once or twice. You'll drive the car for years.",
     "A few extra minutes buy you ASE/I-CAR® Gold technicians, factory-approved repair procedures, a "
     "lifetime warranty on all repair work, and a shop that will push back on your insurer rather than "
     "quietly trimming the repair to fit their estimate. You'll make that drive once or twice. You'll drive "
     "the car for years.",
     "the opener passes the standalone test; the warranty takes its vetted scope (3.80), in the visible "
     "answer and the FAQPage node together, both generated from this one string"),
    ("My vehicle isn't drivable. What now?",
     "Call us at (215) 322-5350 before you make other arrangements. We offer towing assistance and will "
     "coordinate with your insurance company.",
     "If your vehicle isn't drivable, call Tri County Collision Center at " + PHONE + " before you make other "
     "arrangements. We offer towing assistance and will coordinate with your insurance company.",
     "the opener passes the standalone test; the phone is a link; \"towing assistance\" is flagged and "
     "joins the owner questions (Q3)"),
]
HELD_BLOCKS = [
    ("Get Your Free Estimate Today / Wherever you're coming from, Tri County Collision Center is ready to "
     "help. Call us at (215) 322-5350 or visit us at 995 Jaymor Road, Southampton, PA 18966. We're open "
     "Monday through Friday from 8am to 6pm, and by appointment on Saturdays.",
     "HELD: its heading is on all eleven live town pages (site boilerplate, excluded by ruling); its "
     "paragraph restates the NAP and hours the header and footer carry, spells the street a way the audit "
     "fails, and would add an estimate-channel line while 3.69's question is open. The page closes on the "
     "template's promise band instead"),
]


def text_of(h: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", h)).split())


def live_texts(path: str) -> list:
    s = open(path, encoding="utf-8").read()
    body = re.sub(r"(?s)<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", "",
                  s[s.find("<body"):])
    return [" ".join(html.unescape(re.sub(r"<[^>]+>", " ", inner)).split())
            for _tag, inner in re.findall(r"(?s)<(h[1-6]|p|li|summary)\b[^>]*>(.*?)</\1>", body)]


def town_link(key: str, name: str) -> str:
    slug = audit.TOWN_ROUTE_PREFIX + key
    href = f"../{slug}/"
    if os.path.exists(os.path.join(ROOT, "docs", slug, "index.html")):
        return f'<a href="{href}">{html.escape(name)}</a>'
    return f'<span data-pending-href="{href}">{html.escape(name)}</span>'


def details(q: str, a: str) -> str:
    return (f'        <details>\n          <summary>{html.escape(q, quote=False)}'
            f'<span class="faq-ico" aria-hidden="true"></span></summary>\n'
            f'          <p>{a}</p>\n        </details>')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="the cached live hub page, outside the repo")
    a = ap.parse_args()
    src = os.path.abspath(a.src)
    if src.startswith(ROOT + os.sep):
        raise SystemExit("FAILED: the live cache stays outside the repo")
    live = live_texts(src)

    def anchored(t: str):
        n = live.count(t)
        if n != 1:
            raise SystemExit(f"FAILED: a quotation is found {n} times in the cached live page, not once: "
                             f"“{t[:80]}…”. Nothing was written.")

    for _id, old, _new, _why in INTRO:
        anchored(old)
    for t in TOWNS:
        if t[3] is not None:
            anchored(t[3])
    for t in (ELSEWHERE[0], UNCHANGED_1, BEYOND[0], HELD_PITCH[0]):
        anchored(t)
    for q, old, _new, _why in FAQ:
        anchored(q)
        anchored(old)
    assert len(TITLE) <= 60 and len(META) <= 160, (len(TITLE), len(META))
    for key, *_ in TOWNS:
        assert key in audit.TOWN_ROUTES, f"{key} has no recorded routing"

    # PAIRS, printed for the record.
    pairs = [("title", LIVE_TITLE, TITLE, f"to 60 ({len(TITLE)}), the NAP name"),
             ("meta", LIVE_META, META, f"to 160 ({len(META)}), the NAP name; the phone is in the page")]
    for _id, old, new, why in INTRO:
        pairs.append((_id, old, old if new is None else new, why))
    for key, name, _g, old, new, why in TOWNS:
        pairs.append((f"town {name}", old or "(none: Jamison had no blurb)", new, why))
    pairs.append(("elsewhere", ELSEWHERE[0], text_of(ELSEWHERE[1]), ELSEWHERE[2]))
    pairs.append(("beyond", BEYOND[0], BEYOND[1], BEYOND[2]))
    pairs.append(("pitch", HELD_PITCH[0], "HELD", HELD_PITCH[1]))
    for q, old, new, why in FAQ:
        pairs.append((f"faq {q}", old, text_of(new), why))
    for old, why in HELD_BLOCKS:
        pairs.append(("closing", old, "HELD", why))
    for pid, old, new, why in pairs:
        mark = "UNCHANGED" if old == new else "CHANGED"
        print(f"--- {pid} [{mark}]\n    before: {old}\n    after:  {new}\n    why:    {why}")

    # THE PAGE.
    chrome = open(CHROME, encoding="utf-8").read()
    head_assets = chrome[chrome.index("  <!-- No analytics tag yet."):chrome.index("  <!-- One @graph.")]
    body_top = chrome[chrome.index("<body>"):chrome.index("  <main>")]
    body_end = chrome[chrome.index("  </main>") + len("  </main>\n"):]
    graph = json.loads(re.search(r'(?s)<script type="application/ld\+json">(.*?)</script>',
                                 chrome).group(1))["@graph"]
    biz = next(n for n in graph if n["@type"] == "AutoBodyShop")
    home = open(HOME, encoding="utf-8").read()
    promise = re.search(r'(?s)    <section class="dark field-ox" id="start">.*?</section>\n', home).group(0)

    nodes = [
        biz,
        {"@type": "CollectionPage", "@id": URL + "#webpage", "url": URL, "name": TITLE,
         "description": META, "inLanguage": "en-US", "dateModified": MODIFIED,
         "isPartOf": {"@id": BASE + "#business"}, "breadcrumb": {"@id": URL + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Areas We Serve", "item": URL}]},
        {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": text_of(new)}}
            for q, _old, new, _why in FAQ]},
    ]
    jsonld = "\n".join("  " + line for line in
                       json.dumps({"@context": "https://schema.org", "@graph": nodes},
                                  indent=2, ensure_ascii=False).splitlines())

    def group(gid, title, band, ask=False):
        cards = []
        for key, name, g, _old, new, _why in TOWNS:
            if g != gid:
                continue
            cards.append(f'          <article class="card" data-town="{key}">\n'
                         f'            <h3>{town_link(key, name)}</h3>\n'
                         f'            <p>{html.escape(new, quote=False)}</p>\n'
                         f'          </article>')
        cls = ' class="band-panel"' if band else ""
        row = ('        <div class="cta-row">\n'
               '          <a class="btn" href="tel:+12153225350">Call (215) 322-5350</a>\n'
               '          <a class="btn btn-ghost" href="mailto:contact@tricountycollision.com">Email the shop</a>\n'
               '        </div>\n') if ask else ""
        return (f'    <section id="{gid}"{cls}>\n      <div class="wrap">\n        <div class="sec-head">\n'
                f'          <h2 class="sec-title">{html.escape(title, quote=False)}</h2>\n        </div>\n'
                f'        <div class="grid3">\n' + "\n".join(cards) + '\n        </div>\n' + row + '      </div>\n'
                f'    </section>\n')

    lead = INTRO[0][1]
    intro2, intro3 = INTRO[1][2], INTRO[2][2]
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- ============================================================
       /areas-served/, THE AREAS HUB. Migrated 2026-09-29 by
       scripts/migrate-hub.py from the cached live page, proposed-changes.md
       3.79, which holds every pair. Rebuild it with that script, never by
       hand: its town names become links as their pages land, and the
       pending-link test forces the rebuild.

       EVERY TOWN FIGURE IS DERIVED. Each blurb is marked data-town with its
       TOWN_ROUTES key, and scripts/audit.py's hub check fails the page if a
       figure disagrees with that town's routing, if a bearing appears, if a
       road is named that the route does not drive, or if a drive figure
       stands outside every blurb (Greg's Q1 and Q2 rulings, 3.77).

       STAGING, DELIBERATE, AND NOT A DEFECT: noindex below, docs/robots.txt
       disallows everything, and the canonical is absolute to the
       production domain. All three come off together at cutover.

       NO PRICE, OFFER, REVIEW OR RATING MARKUP.
       ============================================================ -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Ink. The palette lives in assets/site.css; a meta tag cannot read a
       custom property, which is why this one hex is duplicated. -->
  <meta name="theme-color" content="#121B27">

  <title>{html.escape(TITLE, quote=False)}</title>
  <meta name="description" content="{html.escape(META)}">

  <link rel="canonical" href="{URL}">
{ROBOTS_LINE}  <!-- THE AREAS HUB, declared, and exempt from nothing: it carries FAQs and
       its own long copy (3.79). The declaration is what makes the hub
       routing check read it. -->
  <meta name="tri-county-page" content="hub">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(TITLE)}">
  <meta property="og:description" content="{html.escape(META)}">
  <meta property="og:url" content="{URL}">
  <!-- NO IMAGE ON THIS PAGE, SO ITS SHARE CARD FOLLOWS HOME'S, byte for
       byte, as the town pages' do. -->
  <meta property="og:image" content="https://tricountycollision.com/assets/img/hero-wrecked-sedan-in-shop.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="800">
  <meta property="og:image:alt" content="A red sedan with its front end crushed and the bumper torn loose, in the shop before repair.">
  <meta name="twitter:card" content="summary_large_image">

{head_assets}  <!-- One @graph. The AutoBodyShop node repeats in full on every page under
       the SAME @id, and its areaServed is AREA_SERVED, written by
       scripts/sync-area-served.py. The FAQPage node is generated from the
       same strings as the visible questions, so the two cannot differ. -->
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
{body_top}  <main>

    <!-- 1. THE COMPACT OX HEADER, the page-header identity, extended to the
         areas tier by Greg's ruling (3.61, 3.62). It carries the call. -->
    <section class="hero dark field-ox" id="hub-head">
      <div class="wrap">
        <!-- Mirrors the BreadcrumbList, same labels and same order. -->
        <nav class="crumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="../">Home</a></li>
            <li>Areas We Serve</li>
          </ol>
        </nav>
        <div>
          <h1>Areas We Serve</h1>
          <p class="lead">{html.escape(lead, quote=False)}</p>
          <div class="cta-row">
            <a class="btn" href="tel:+12153225350">Call (215) 322-5350</a>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. THE CASE, the live page's own opening, migrated. -->
    <section id="intro">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">Collision Repair Across Bucks County, Montgomery County &amp; Northeast Philadelphia</h2>
        </div>
        <div class="prose">
          <p>{html.escape(intro2, quote=False)}</p>
          <p>{html.escape(intro3, quote=False)}</p>
        </div>
      </div>
    </section>

    <!-- 3 to 5. THE TOWNS, by county, as the live page groups them. Each blurb
         is a data-town block the hub routing check reads; every figure in it
         is its town's recorded routing, from its named corner.
         TWO SECTION ASKS, BY THE RHYTHM (3.79). Stacked on a phone the town
         lists ran 4,820px between the header's Call and the next call, past
         the 2,684 ceiling. One ask closing Bucks cleared it at 390 (2,608)
         and not at 360 (2,742); asks closing Bucks and Philadelphia clear it
         at every width measured, 360 to 1440, with the two 2,214 apart at
         390, over the 1,634 floor. The grammar is the siblings': Call and
         Email, centred at the section's foot. -->
{group("bucks", GROUPS[0][1], True, ask=True)}
{group("montgomery", GROUPS[1][1], False)}
{group("philadelphia", GROUPS[2][1], True, ask=True)}
    <!-- 6. THE PLACES WITHOUT PAGES, named without distances (Q2). OPTION
         FOR LATER, recorded not built: their own routings, so this could
         state derived times for them. -->
    <section id="elsewhere">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">Don't See Your Town Listed?</h2>
        </div>
        <div class="prose">
          <p>{ELSEWHERE[1]}</p>
        </div>
      </div>
    </section>

    <!-- 7. WHAT DOESN'T CHANGE. Every claim here is in the claims list for the
         owner. "Towing assistance" is flagged and is an owner question. -->
    <section id="constant" class="band-panel">
      <div class="wrap">
        <div class="sec-head">
          <h2 class="sec-title">What Doesn't Change, No Matter Where You Drive In From</h2>
        </div>
        <div class="prose">
          <p>{html.escape(UNCHANGED_1, quote=False)}</p>
          <p>{html.escape(BEYOND[1], quote=False)}</p>
        </div>
      </div>
    </section>

    <!-- 8. THE FAQ, the live page's four, openers made to stand alone. -->
    <section id="faq">
      <div class="wrap" style="max-width:880px">
        <div class="sec-head">
          <h2 class="sec-title">Frequently Asked Questions</h2>
        </div>
{chr(10).join(details(q, new) for q, _old, new, _why in FAQ)}
      </div>
    </section>

    <!-- 9. THE PROMISE BAND, home's #start byte for byte, as the town pages
         close: the approved promise, not a new one. -->
{promise}
  </main>
{body_end}'''
    # THE CHROME IS THE GENERATOR'S (3.83): the lifted chrome is re-rendered
    # for this page, so the page is marked as the current page in its nav
    # and footer, as every page is.
    import importlib.util
    _spec = importlib.util.spec_from_file_location("sync_chrome", os.path.join(ROOT, "scripts", "sync-chrome.py"))
    _sc = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_sc)
    page = _sc.synced(OUT, page)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {os.path.relpath(OUT, ROOT)} {len(page)} bytes; title {len(TITLE)}, meta {len(META)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
