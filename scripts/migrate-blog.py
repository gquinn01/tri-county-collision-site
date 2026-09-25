#!/usr/bin/env python3
"""
Migrates the shop's 16 blog posts, and builds /blog/, from the live
WordPress pages, and prints every change it makes as a before/after pair.

WHY A SCRIPT. Sixteen posts take the same dozen transformations, and a
transformation done by hand sixteen times is sixteen chances to do it
differently. Here each one is written once, applied mechanically, counted
per post and printed, so the record's pairs are this script's output rather
than somebody's recollection. proposed-changes.md 3.57 and 3.58.

THE SOURCE. The live posts at https://tricountycollision.com/<slug>/, read
2026-09-25, cached OUTSIDE this public repo (like every supplied original)
and passed in with --src. The live post is the content source of record: no
fact invented, no claim added, none silently dropped. Every edit below is a
pair with its reason; anything a pair removes is recorded as HELD, not lost.

WHAT EVERY POST GETS, mechanically:
  - The business name as the NAP writes it. "Tri County Collision Center",
    "Tri-County Collision Center" and "Tri County Collision" all become
    "Tri-County Collision", the precedent every service page set (3.47-3.49).
  - Links: the shop's own URLs become relative links to pages that exist,
    and pending spans (data-pending-href) to pages that do not yet, so the
    pending-link test forces each one the day its target lands. Google Maps
    and Google search links become the one directions URL the footers use.
    A malformed href is repaired to what its anchor text says.
  - NO IMAGE. Old-site imagery is banned from this repo, because the old
    vendor's licences cannot be verified. Posts ship text-first, and a post
    that leaned on its images is flagged in the record.
  - Markup reduced to the prose the site styles: p, h2, h3, h4, ul, ol, li,
    strong, em, a. WordPress classes, empty paragraphs and no-break spaces go.
  - A visible FAQ in the live post migrates as the site's FAQ, <details> and
    a byte-identical FAQPage node, because Greg's ruling of 2026-09-25 is
    that a post is not REQUIRED to carry an FAQ, never that one goes
    unmeasured. Openers that fail the standalone test are pairs.

DATES ARE FACTS. datePublished and dateModified are the live post's own
article:published_time and article:modified_time, the same instants written
in America/New_York, so their dates read as the live post's visible date.
Nothing is freshened. build-sitemap.py takes lastmod from dateModified.

AUTHORSHIP IS THE SHOP'S. The live posts carry a "Greg Quinn" byline and
author box; neither migrates. The BlogPosting's author and publisher are the
AutoBodyShop node under the shared @id. These are MIGRATED posts, so the
firm's AI-disclosure rule does not bite here; it applies the day a new post
is drafted in this repo.

USAGE:
    python3 scripts/migrate-blog.py --src DIR --posts SLUG [SLUG...] --record 3.57
    python3 scripts/migrate-blog.py --src DIR --index --record 3.57
Posts not built yet stay pending on the index. No external packages.
"""

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
SHELL = os.path.join(DOCS, "contact-us", "index.html")
BASE = "https://tricountycollision.com/"
NY = ZoneInfo("America/New_York")
MAPS = ("https://www.google.com/maps/search/?api=1&amp;query=Tri-County%20Collision"
        "%2C%20995%20Jaymor%20Rd%2C%20Southampton%2C%20PA%2018966")
TITLE_MAX, DESC_MAX = 60, 160

# ---------------------------------------------------------------------------
# PER POST: the title and meta (both trimmed from the live post's, machine
# counted), and the edits beyond the mechanical ones. Every edit is
# (before, after, reason) and must match exactly once or the run stops.
POSTS = {
    "what-do-all-those-lights-mean-in-my-car-understanding-your-vehicles-language": dict(
        title="What do all those lights mean in my car?",
        meta=("What your car's warning lights mean, from engine temperature and oil "
              "pressure to tire pressure and traction control, and what to check when one "
              "comes on."),
        flags=["NO-IMAGE: the live post pairs each of its 21 warning lights with a "
               "screenshot of the symbol, and a reader matches a light by its symbol. The "
               "text names and explains every light and stands, but the post is weaker "
               "without them. Shipped text-first; a licensed or owner-supplied symbol set "
               "would restore it."],
        edits=[
            ("such as\u2014the anti-lock", "such as the anti-lock",
             "no em dashes; the dash only introduced the list"),
            ("995 Jaymor Road, Southampton, PA 18966", "995 Jaymor Rd, Southampton, PA 18966",
             "the NAP's street spelling, character for character (and one space before the ZIP)"),
            ("215.322.5350", "(215) 322-5350", "the NAP's phone display"),
            ("shop hours are Monday-Friday 8am-6pm, and Saturday by appointment<strong>.</strong>",
             "shop hours are Monday to Friday, 8 a.m. to 6 p.m., and Saturday by appointment only.",
             "the hours as HOURS_WEEKDAYS and HOURS_SATURDAY write them; the audit fails any "
             "other spelling (3.54)"),
        ]),
    "the-ultimate-guide-to-collision-repair-services-what-to-expect-and-how-to-choose-the-best-provider": dict(
        title="The Ultimate Guide to Collision Repair Services",
        meta=("The ultimate guide to collision repair services: what to expect during the "
              "process and expert tips on choosing the best provider for your vehicle."),
        edits=[]),
    "the-importance-of-oem-parts-in-collision-repair-ensuring-quality-and-safety-for-your-vehicle": dict(
        title="The Importance of OEM Parts in Collision Repair",
        meta=("Learn why Tri-County Collision prioritizes OEM parts in collision repair and "
              "how they ensure quality, safety, and value for your vehicle."),
        edits=[]),
    "the-art-of-paintless-dent-repair": dict(
        title="The Art of Paintless Dent Repair: A Cost-Effective Solution",
        meta=("The art of paintless dent repair at Tri-County Collision: a cost-effective, "
              "efficient fix for minor collisions that preserves your vehicle's original finish."),
        edits=[]),
    "assessing-collision-damage": dict(
        title="Assessing Collision Damage: Fender Benders to Major Crashes",
        meta=("Discover how Tri-County Collision accurately assesses collision damage "
              "severity, from minor fender benders to major crashes"),
        edits=[]),
    "preserving-value-how-tri-county-collision-center-impacts-the-resale-value-of-your-car-through-collision-repair": dict(
        title="Preserving Value: How Collision Repair Impacts Resale Value",
        meta=("Protect your car's resale value with Tri-County Collision's expert collision "
              "repair, restoring your vehicle to its pre-collision condition and appeal."),
        edits=[]),
    "unveiling-the-hidden-benefits-of-paintless-dent-repair-in-collision-restoration": dict(
        title="Unveiling the Hidden Benefits of Paintless Dent Repair",
        meta=("The hidden benefits of paintless dent repair at Tri-County Collision: your "
              "original factory finish preserved, money saved, and back on the road faster."),
        edits=[]),
    "collision-repair-near-me-in-southampton-how-to-choose-the-right-auto-body-shop": dict(
        title="“Collision Repair Near Me”? Choosing a Southampton Body Shop",
        meta=("Searching \"collision repair near me\" in Southampton? Our guide helps you "
              "choose the RIGHT auto body shop with expert tips. Make a confident choice!"),
        edits=[
            ("the Tri County Difference", "the Tri-County Difference",
             "the name as the NAP writes it; the mechanical rule only catches the full name"),
        ]),
    "critical-questions-to-ask-any-collision-center-in-bucks-county-before-handing-over-your-keys": dict(
        title="Critical Questions to Ask a Bucks County Collision Center",
        meta=("Stressed about collision repair in Bucks County? Ask these 7 crucial "
              "questions to find a trusted collision repair center & ensure quality work. "
              "Read now!"),
        edits=[
            ("(like ADAS – Advanced Driver-Assistance Systems)",
             "(like ADAS, Advanced Driver-Assistance Systems)",
             "a spaced dash is an em dash by another glyph; no em dashes"),
            ("(Original Equipment Manufacturer – parts made by",
             "(Original Equipment Manufacturer: parts made by",
             "a spaced dash is an em dash by another glyph; no em dashes"),
            ("communication or updates – a simple",
             "communication or updates: a simple",
             "a spaced dash is an em dash by another glyph; no em dashes"),
        ]),
    "is-my-car-totaled-expert-insights-from-your-southampton-collision-repair-specialists": dict(
        title="Is My Car Totaled? Expert Insights from Southampton",
        meta=("Wondering if your car is totaled? Southampton's collision repair specialists "
              "explain what ‘totaled’ really means and offer a free professional "
              "assessment."),
        edits=[
            ("close to\u2014or exceeds\u2014its market value", "close to, or exceeds, its market value",
             "no em dashes; commas carry the aside"),
        ]),
    "after-the-unthinkable-your-first-steps-following-a-car-accident-in-bucks-county-before-calling-a-collision-shop": dict(
        title="Your First Steps Following a Car Accident in Bucks County",
        meta=("Just had a car accident in Bucks County? A step-by-step guide to what to do "
              "before choosing a collision shop, from Southampton's trusted repair experts."),
        edits=[]),
    "misconceptions-about-collision-repair": dict(
        title="Top 5 Misconceptions About Collision Repair",
        meta=("Confused after a collision? We debunk 5 common repair myths to help you save "
              "money and make a safer choice. Get the expert facts from Tri-County Collision."),
        edits=[]),
    "the-risks-of-driving-a-damaged-vehicle-in-the-southampton-area": dict(
        title="Don’t Delay Repairs! The Risks of Driving a Damaged Vehicle",
        meta=("Driving a damaged car in Southampton? Don't risk it. Learn the hidden safety "
              "and financial dangers of delaying your collision repair."),
        edits=[]),
    "deer-season-in-bucks-county-insurance-coverage-next-steps": dict(
        title="Deer Season in Bucks County: Insurance Coverage & Next Steps",
        meta=("Navigate deer season smart: safety and documentation tips, how claims work, "
              "and expert repairs from Tri-County Collision to restore your vehicle."),
        edits=[
            ("How Tri County handles", "How Tri-County handles",
             "the name as the NAP writes it; the mechanical rule only catches the full name"),
        ],
        faq_edits=[
            ("Yes, if you carry comprehensive coverage.",
             "Hitting a deer is covered by your insurance if you carry comprehensive coverage.",
             "standalone test: \"Yes, if...\" carries no subject when lifted"),
            ("Only if it’s truly safe:",
             "You can drive home after hitting a deer only if it’s truly safe:",
             "standalone test: \"Only if\" carries no subject when lifted"),
        ]),
    "your-right-to-choose-a-body-shop": dict(
        title="PA Law: Your Right to Choose a Body Shop (Anti-Steering)",
        meta=("In Pennsylvania, the repair shop is your choice, not the insurer's. How "
              "anti-steering rules work and how to document your choice with Tri-County Collision."),
        edits=[
            ("(Honda, Toyota, Subaru, Ford, GM, and more)", "(Honda, Subaru, Ford, GM, and more)",
             "HELD: Toyota is not among the twelve factory certifications the site checks "
             "and publishes (BRANDS in audit.py). An unconfirmed certification does not "
             "ship; the owner question asks whether it is true"),
        ],
        faq_edits=[
            ("No. In Pennsylvania, you choose where to repair your vehicle.",
             "No, in Pennsylvania you choose where to repair your vehicle.",
             "standalone test: a bare \"No.\" comma-merges into the sentence after it"),
            ("It shouldn’t be.",
             "No, your claim shouldn’t be delayed if you use a different shop.",
             "standalone test: \"It shouldn't be.\" says nothing when lifted"),
            ("It’s not required by the PA Insurance Department’s guidance;",
             "Multiple estimates are not required by the PA Insurance Department’s guidance;",
             "standalone test: \"It's\" has no antecedent when lifted"),
        ]),
    "adas-calibrations-after-a-crash": dict(
        title="ADAS Calibrations After a Crash: The Hidden Step",
        meta=("ADAS calibrations after a crash restore lane, brake, and blind-spot tech "
              "after repairs. Our Bucks County team handles testing, documentation, and "
              "peace of mind."),
        spaced_dash_to_colon=True,
        edits=[
            ("How Tri County coordinates", "How Tri-County coordinates",
             "the name as the NAP writes it; the mechanical rule only catches the full name"),
            ('<a href="../auto-glass-repair-replacement/">', '<a href="../auto-glass-repair-replacement/#adas">',
             "the brief's ruling: the ADAS post stays a post and links to the glass page's ADAS "
             "section today, and to an ADAS page only if that page ever clears its gate"),
        ]),
}

NAME_RE = re.compile(r"Tri[ \-]County Collision Center|Tri County Collision")
KEEP = {"p", "h2", "h3", "h4", "ul", "ol", "li", "strong", "em", "a", "br"}
PAIRS = []


def pair(slug, where, before, after, why):
    PAIRS.append((slug, where, before, after, why))


# ---------------------------------------------------------------------------
def subtree(s, marker):
    """The inner HTML of the first fl-module-content div after `marker`."""
    i = s.find(marker)
    j = s.find('<div class="fl-module-content', i)
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", s[j:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return s[s.find(">", j) + 1:j + m.start()]
    raise SystemExit(f"FAILED: no balanced {marker} block")


class Clean(HTMLParser):
    """Rebuilds the post body with only the tags the site styles. Text is
    decoded and re-escaped, no-break spaces become spaces, attributes go
    except an anchor's href, and images and figures go entirely."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("figure", "img", "script", "style", "iframe"):
            if tag not in ("img",):
                self.skip += 1
            return
        if self.skip or tag not in KEEP:
            return
        if tag == "a":
            self.out.append(f'<a href="{html.escape(dict(attrs).get("href", ""), quote=True)}">')
        else:
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in ("figure", "script", "style", "iframe"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in KEEP or tag == "br":
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data.replace(" ", " "), quote=False))


def clean(body):
    c = Clean()
    c.feed(body)
    h = "".join(c.out)
    h = re.sub(r"[ \t\r\n]+", " ", h)
    h = re.sub(r"\s*(</?(?:p|h2|h3|h4|ul|ol|li)>)\s*", r"\1", h)
    h = re.sub(r"<p>\s*</p>", "", h)
    h = re.sub(r"<(strong|em)>\s*</\1>", "", h)
    h = re.sub(r"(\S) +(</(?:strong|em|a)>)", r"\1\2 ", h)
    h = re.sub(r"  +", " ", h)
    return h


def text_of(h):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


def exists(path):
    return os.path.isfile(os.path.join(DOCS, path, "index.html")) if path else True


def map_links(slug, h, landing):
    """Every anchor to its destination on this site, printed as pairs."""
    def one(m):
        href, inner = html.unescape(m.group(1)), m.group(2)
        label = text_of(inner)
        if href.startswith(BASE):
            path = href[len(BASE):].strip("/")
            if path and not (exists(path) or path in landing):
                pair(slug, "link", href, f'pending span -> ../{path}/', f'"{label}": target not built yet')
                return f'<span data-pending-href="../{path}/">{inner}</span>'
            return f'<a href="../{path + "/" if path else ""}">{inner}</a>'
        if "google.com/maps" in href or "google.com/search" in href:
            pair(slug, "link", href[:70] + "...", "the footers' directions URL",
                 f'"{label}": one Google destination, no tracking parameters')
            return f'<a href="{MAPS}" target="_blank" rel="noopener">{inner}</a>'
        if href.startswith("http://ASE"):
            pair(slug, "link", href, "../contact-us/",
                 f'"{label}": a malformed href; the anchor says Contact Us')
            return f'<a href="../contact-us/">{inner}</a>'
        if href == "tel:12153225350":
            pair(slug, "link", href, "tel:+12153225350", "the NAP's tel: form")
            return f'<a href="tel:+12153225350">{inner}</a>'
        if href.startswith(("mailto:", "tel:")):
            return m.group(0)
        pair(slug, "link", href, href, f'"{label}": external, now opens in a new tab')
        return f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener">{inner}</a>'
    return re.sub(r'<a href="([^"]*)">(.*?)</a>', one, h, flags=re.S)


def apply_edits(slug, h, edits, where):
    # LITERAL against the cleaned HTML, markup included, so an edit can
    # reach a stray tag; the cleaned text carries no &, < or > of its own
    # in any edit's reach, which the exactly-once rule below would catch.
    for before, after, why in edits:
        b, a = before, after
        n = h.count(b)
        if n != 1:
            raise SystemExit(f"FAILED: {slug} {where} edit matched {n} times: {before!r}")
        h = h.replace(b, a)
        pair(slug, where, before, after, why)
    return h


def et(iso):
    return datetime.fromisoformat(iso).astimezone(NY)


def human(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def first_sentence(h):
    m = re.search(r"<p>(.*?)</p>", h, re.S)
    t = text_of(m.group(1)) if m else ""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"])", t)
    out = parts[0]
    if len(out) < 60 and len(parts) > 1:
        out += " " + parts[1]
    return out


# ---------------------------------------------------------------------------
def load_post(src, slug):
    s = open(os.path.join(src, f"p-{slug}.html"), encoding="utf-8").read()
    g = lambda rx: re.search(rx, s, re.S).group(1)
    return dict(
        h1=text_of(g(r"<h1[^>]*>(.*?)</h1>")),
        title=html.unescape(g(r"<title>(.*?)</title>")),
        meta=html.unescape(g(r'<meta name="description" content="([^"]*)"')),
        published=g(r'article:published_time" content="([^"]*)"'),
        modified=g(r'article:modified_time" content="([^"]*)"'),
        body=subtree(s, "fl-module-fl-post-content"))


def build_post(src, slug, landing, record):
    cfg = POSTS[slug]
    live = load_post(src, slug)
    h = clean(live["body"])

    n_names = len(NAME_RE.findall(text_of(h)))
    h = NAME_RE.sub("Tri-County Collision", h)
    if n_names:
        pair(slug, "name", f"{n_names} x Tri County Collision Center (and variants)",
             "Tri-County Collision", "the NAP's name, the service pages' precedent")
    h1 = NAME_RE.sub("Tri-County Collision", live["h1"])
    if h1 != live["h1"]:
        pair(slug, "H1", live["h1"], h1, "the NAP's name")

    h = map_links(slug, h, landing)
    h = apply_edits(slug, h, cfg.get("edits", []), "body")
    if cfg.get("spaced_dash_to_colon"):
        n = h.count(" – ")
        h = h.replace(" – ", ": ")
        pair(slug, "body", f"{n} x 'Label – Text' in the step list", "'Label: Text'",
             "a spaced dash is an em dash by another glyph; no em dashes")

    faq = []
    if "<h2>FAQs</h2>" in h:
        h, tail = h.split("<h2>FAQs</h2>", 1)
        for q, a in re.findall(r"<h3>(.*?)</h3><p>(.*?)</p>", tail, re.S):
            faq.append([q, a])
        rest = re.sub(r"<h3>.*?</h3><p>.*?</p>", "", tail, flags=re.S).strip()
        if rest:
            raise SystemExit(f"FAILED: {slug} FAQ has content this script does not place: {rest[:120]}")
        for before, after, why in cfg.get("faq_edits", []):
            hits = [x for x in faq if x[1].startswith(html.escape(before, quote=False))]
            if len(hits) != 1:
                raise SystemExit(f"FAILED: {slug} FAQ opener matched {len(hits)}: {before!r}")
            hits[0][1] = html.escape(after, quote=False) + hits[0][1][len(html.escape(before, quote=False)):]
            pair(slug, "FAQ opener", before, after, why)

    title, meta = cfg["title"], cfg["meta"]
    if len(title) > TITLE_MAX or len(meta) > DESC_MAX:
        raise SystemExit(f"FAILED: {slug} title {len(title)} / meta {len(meta)} over the limit")
    pair(slug, "title", live["title"], title, f"{len(title)} characters, machine-counted")
    if meta != live["meta"]:
        pair(slug, "meta", live["meta"], meta, f"{len(meta)} characters, machine-counted")

    pub, mod = et(live["published"]), et(live["modified"])
    return dict(slug=slug, title=title, meta=meta, h1=h1, body=h, faq=faq,
                pub=pub, mod=mod, excerpt=first_sentence(h), flags=cfg.get("flags", []),
                words=len(text_of(h).split()) + sum(len(text_of(q + " " + a).split()) for q, a in faq),
                record=record)


# ---------------------------------------------------------------------------
def shell():
    s = open(SHELL, encoding="utf-8").read()
    head_assets = "\n".join(l for l in s.split("\n") if "site.css?v=" in l or "site.js?v=" in l)
    graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
    biz = [n for n in graph["@graph"] if n.get("@type") == "AutoBodyShop"][0]
    nav = re.search(r'  <header class="nav">.*?</header>\n', s, re.S).group(0)
    foot = s[s.index("  <footer class=\"site\">"):]
    foot = foot.replace('<li><a href="./">Send us your details online</a></li>',
                        '<li><a href="../contact-us/">Send us your details online</a></li>')
    assert 'href="./"' not in foot
    return head_assets, biz, nav, foot


def jsonld(graph):
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2).replace("\n", "\n  ")


HEAD_COMMON = '''  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Ink. The palette lives in assets/site.css; a meta tag cannot read a
       custom property, which is why this one hex is duplicated. -->
  <meta name="theme-color" content="#121B27">
'''
OG_IMAGE = '''  <!-- NO IMAGE ON THIS PAGE, SO ITS SHARE CARD FOLLOWS HOME'S, byte for
       byte, as /contact-us/'s does. Old-site imagery is banned from this
       repo; this moves to a real shop photograph after the shoot. -->
  <meta property="og:image" content="https://tricountycollision.com/assets/img/hero-wrecked-sedan-in-shop.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="800">
  <meta property="og:image:alt" content="A red sedan with its front end crushed and the bumper torn loose, in the shop before repair.">
  <meta name="twitter:card" content="summary_large_image">
'''
HEAD_TAIL = '''
  <!-- No analytics tag yet. GA4 goes in the CLIENT'S OWN Google account at
       cutover, and the CallRail snippet goes in beside it. Neither is here,
       because a measurement ID nobody has given us is a fact nobody has
       confirmed. docs/privacy/ ships in the same commit as the first tag. -->

  <!-- Both faces are self-hosted and both are needed above the fold, so they
       are preloaded rather than discovered inside the stylesheet. They are
       SIL OFL 1.1 and their licence texts sit beside them in assets/fonts/. -->
  <link rel="preload" href="../assets/fonts/ArchivoBlack-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../assets/fonts/SourceSans3-var.woff2" as="font" type="font/woff2" crossorigin>
'''
SCHEMA_NOTE = '''  <!-- One @graph. The AutoBodyShop node repeats in full on every page under
       the SAME @id, so the whole site resolves to one business entity, and
       here it is the author and the publisher: authorship is the shop's.
       geo IS THE SHOP'S VERIFIED PIN, GEO_LAT and GEO_LON in scripts/audit.py,
       adopted by Greg's ruling of 2026-09-25 (proposed-changes.md 3.56). It is
       never a map URL's @lat,lon, which is the viewport centre, not the pin.
       sameAs IS DELIBERATELY ABSENT until the client's verified list lands.
       No image in the BlogPosting: this page has none. -->
'''
STAGING = '''
  <!-- Removed at cutover, with the noindex tag and the robots.txt disallow.
       A human who opens this page should not have to guess why it is not
       indexed. -->
  <p class="staging">Staging build. Not the live site. The shop's live site is at tricountycollision.com</p>

'''
CTA = '''<div class="cta-row">
          <a class="btn" href="tel:+12153225350">Call (215) 322-5350</a>
          <a class="btn btn-ghost" href="mailto:contact@tricountycollision.com">Email the shop</a>
        </div>'''


def date_line(p):
    s = f'Published <time datetime="{p["pub"].date().isoformat()}">{human(p["pub"])}</time>'
    if p["mod"].date() != p["pub"].date():
        s += f' &middot; Updated <time datetime="{p["mod"].date().isoformat()}">{human(p["mod"])}</time>'
    return s


def render_post(p, assets, biz, nav, foot):
    url = f"{BASE}{p['slug']}/"
    e = lambda x: html.escape(x, quote=True)
    faq_nodes, faq_html = [], ""
    if p["faq"]:
        items = []
        for q, a in p["faq"]:
            items.append(f'''        <details>
          <summary>{q}<span class="faq-ico" aria-hidden="true"></span></summary>
          <p>{a}</p>
        </details>''')
        faq_nodes = [{"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": text_of(q),
             "acceptedAnswer": {"@type": "Answer", "text": text_of(a)}} for q, a in p["faq"]]}]
        faq_html = f'''
    <!-- THE LIVE POST'S OWN FAQ, migrated into the site's FAQ grammar. Each
         visible answer is byte-identical to its acceptedAnswer: edit one,
         edit both. A post is not required to carry an FAQ; one that does is
         held to the mirror law like any page (Greg, 2026-09-25, 3.57). -->
    <section id="faq" class="band-panel">
      <div class="wrap" style="max-width:880px">
        <div class="sec-head">
          <h2 class="sec-title">FAQs</h2>
        </div>
{chr(10).join(items)}
        {CTA}
      </div>
    </section>
'''
    graph = [biz,
             {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"],
              "description": p["meta"], "inLanguage": "en-US",
              "dateModified": p["mod"].isoformat(),
              "isPartOf": {"@id": BASE + "#business"},
              "breadcrumb": {"@id": url + "#breadcrumb"},
              "mainEntity": {"@id": url + "#article"}},
             {"@type": "BlogPosting", "@id": url + "#article", "headline": p["h1"],
              "description": p["meta"], "inLanguage": "en-US",
              "datePublished": p["pub"].isoformat(), "dateModified": p["mod"].isoformat(),
              "author": {"@id": BASE + "#business"}, "publisher": {"@id": BASE + "#business"},
              "mainEntityOfPage": {"@id": url + "#webpage"},
              "isPartOf": {"@id": BASE + "blog/#blog"}},
             {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                 {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "blog/"},
                 {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}
             ] + faq_nodes
    body_cta = "" if p["faq"] else "\n        " + CTA
    flags = "".join(f"\n\n       FLAGGED: {f}" for f in p["flags"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- ============================================================
       A MIGRATED POST, built by scripts/migrate-blog.py from the shop's
       live post at {url}, read 2026-09-25. The live post is the content
       source of record; every change is a before/after pair in
       proposed-changes.md {p["record"]}, printed by the script. Do not edit
       copy here without adding the pair there.

       THE POST SHAPE, built once and used sixteen times: breadcrumb, H1, a
       quiet date line, the prose at the site's reading width, ONE ask at
       the foot (a CTA row in the mold, not the promise band: a post is a
       read, not a service argument), and the four-service footer.

       DATES ARE THE LIVE POST'S OWN: datePublished and dateModified are its
       published and modified times, in Eastern time. Nothing is freshened.

       NO IMAGE MIGRATES: old-site imagery is banned from this repo.{flags}

       STAGING, DELIBERATE, AND NOT A DEFECT: noindex below, docs/robots.txt
       disallows everything, and the canonical is absolute to the
       production domain. All three come off together at cutover.
       ============================================================ -->
{HEAD_COMMON}
  <title>{e(p["title"])}</title>
  <meta name="description" content="{e(p["meta"])}">

  <link rel="canonical" href="{url}">
  <meta name="robots" content="noindex, nofollow">
  <!-- A POST IS A READ, declared. Greg's ruling of 2026-09-25,
       proposed-changes.md 3.57: scripts/audit.py does not require an FAQ
       of it, and measures every other check, thin content included. -->
  <meta name="tri-county-page" content="post">

  <meta property="og:type" content="article">
  <meta property="og:title" content="{e(p["title"])}">
  <meta property="og:description" content="{e(p["meta"])}">
  <meta property="og:url" content="{url}">
  <meta property="article:published_time" content="{p["pub"].isoformat()}">
  <meta property="article:modified_time" content="{p["mod"].isoformat()}">
{OG_IMAGE}{HEAD_TAIL}{assets}

{SCHEMA_NOTE}  <script type="application/ld+json">
  {jsonld(graph)}
  </script>
</head>
<body>
{STAGING}{nav}
  <main>

    <section class="hero band-panel" id="post-head">
      <div class="wrap">
        <!-- Mirrors the BreadcrumbList, same labels and same order. -->
        <nav class="crumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="../">Home</a></li>
            <li><a href="../blog/">Blog</a></li>
            <li>{e(p["title"])}</li>
          </ol>
        </nav>
        <h1>{e(p["h1"])}</h1>
        <p>{date_line(p)}</p>
      </div>
    </section>

    <section id="post">
      <div class="wrap">
        <div class="prose">
          {p["body"]}
        </div>{body_cta}
      </div>
    </section>
{faq_html}
  </main>

{foot}'''


def render_index(posts, record, assets, biz, nav, foot):
    url = BASE + "blog/"
    title = "Collision Repair Tips & Advice | Tri-County Collision"
    meta = ("Collision repair tips and advice from Tri-County Collision in Southampton, PA: "
            "insurance claims, your right to choose a shop, dent repair, ADAS and more.")
    assert len(title) <= TITLE_MAX and len(meta) <= DESC_MAX, (len(title), len(meta))
    e = lambda x: html.escape(x, quote=True)
    cards, refs = [], []
    for p in posts:
        inner = f'''            <div class="svc-card-body">
              <h3>{e(p["h1"])}</h3>
              <p>{date_line(p)}</p>
              <p>{e(p["excerpt"])}</p>
            </div>'''
        if p["built"]:
            cards.append(f'          <a class="svc-card" href="../{p["slug"]}/">\n{inner}\n          </a>')
            refs.append({"@id": f"{BASE}{p['slug']}/#article"})
        else:
            cards.append(f'          <div class="svc-card" data-pending-href="../{p["slug"]}/">\n{inner}\n          </div>')
    graph = [biz,
             {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title,
              "description": meta, "inLanguage": "en-US", "dateModified": "2026-09-25",
              "isPartOf": {"@id": BASE + "#business"}, "breadcrumb": {"@id": url + "#breadcrumb"},
              "mainEntity": {"@id": url + "#blog"}},
             {"@type": "Blog", "@id": url + "#blog", "name": "Collision Repair Tips & Advice",
              "url": url, "publisher": {"@id": BASE + "#business"}, "blogPost": refs},
             {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                 {"@type": "ListItem", "position": 2, "name": "Blog", "item": url}]}]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- ============================================================
       THE BLOG INDEX, built by scripts/migrate-blog.py, proposed-changes.md
       {record}. pagemap.md's row: migrate, and add the H1 and the meta the
       live index lacks. The H1 is the live index's own title, "Collision
       Repair Tips & Advice"; the meta is new, a pair in the record.

       AN INDEX ROUTES. Sixteen posts as cards in the site's whole-card
       grammar (a.svc-card, so the lift comes with it), newest first, each
       with its title, its date and one line from its own opening. A card
       whose post has not landed yet is a div with data-pending-href and no
       lift, the home router's precedent; the pending-link test turns each
       into a link the day its post exists.

       THE TOP IS COMPACT AND WHITE, not ox: this band routes rather than
       asks, and the palette law keeps oxblood for asking. The argument is
       in the record.

       NOTHING IN NAV OR FOOTER LINKS HERE YET, deliberately: the
       header-nav sweep is its own queued sitting and the footer has no
       honest seat for it. The sitemap and llms.txt carry it today.

       STAGING, DELIBERATE, AND NOT A DEFECT: noindex, robots.txt, and an
       absolute canonical. All three come off together at cutover.
       ============================================================ -->
{HEAD_COMMON}
  <title>{e(title)}</title>
  <meta name="description" content="{e(meta)}">

  <link rel="canonical" href="{url}">
  <meta name="robots" content="noindex, nofollow">
  <!-- AN INDEX ROUTES, declared. Greg's ruling of 2026-09-25,
       proposed-changes.md 3.57: scripts/audit.py does not require an FAQ
       of it, and measures every other check, thin content included. -->
  <meta name="tri-county-page" content="blog-index">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(meta)}">
  <meta property="og:url" content="{url}">
{OG_IMAGE}{HEAD_TAIL}{assets}

{SCHEMA_NOTE.replace("and here it is the author and the publisher: authorship is the shop's", "and here it is the blog's publisher").replace("       No image in the BlogPosting: this page has none. -->", "       blogPost lists only posts that exist; each is a bare @id to its page. -->")}  <script type="application/ld+json">
  {jsonld(graph)}
  </script>
</head>
<body>
{STAGING}{nav}
  <main>

    <section class="hero band-panel" id="blog-head">
      <div class="wrap">
        <!-- Mirrors the BreadcrumbList, same labels and same order. -->
        <nav class="crumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="../">Home</a></li>
            <li>Blog</li>
          </ol>
        </nav>
        <p class="eyebrow">Southampton, PA</p>
        <h1>Collision Repair Tips &amp; Advice</h1>
        <!-- The meta description, word for word, so the index adds no copy
             beyond the one recorded pair. It also closes the header on a
             paragraph, whose last-child margin is 0: ending on the H1 put
             its .5em bottom margin into the seam, 208 at 1440 against the
             177 baseline (3.57). -->
        <p class="lead">{e(meta)}</p>
      </div>
    </section>

    <section id="posts">
      <div class="wrap">
        <h2 class="sr-only">All posts, newest first</h2>
        <div class="grid2">
{chr(10).join(cards)}
        </div>
      </div>
    </section>

  </main>

{foot}'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="the cached live posts, outside the repo")
    ap.add_argument("--posts", nargs="*", default=[])
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--record", required=True)
    a = ap.parse_args()
    if os.path.abspath(a.src).startswith(ROOT + os.sep):
        raise SystemExit("FAILED: the live cache stays outside the repo")
    for s in a.posts:
        if s not in POSTS:
            raise SystemExit(f"FAILED: unknown slug {s}")
    assets, biz, nav, foot = shell()
    landing = set(a.posts)
    built = []
    for slug in a.posts:
        p = build_post(a.src, slug, landing, a.record)
        out = os.path.join(DOCS, slug, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(render_post(p, assets, biz, nav, foot))
        built.append(p)
        print(f"built    {slug}  ({p['words']} words, {len(p['faq'])} FAQ, "
              f"published {p['pub'].date()}, modified {p['mod'].date()})")
    if a.index:
        # Every post is read for its title, date and opening line; only the
        # pairs of posts built in THIS run are printed, once.
        kept = list(PAIRS)
        allp = []
        for slug in POSTS:
            p = build_post(a.src, slug, landing, a.record)
            p["built"] = exists(slug) or slug in landing
            allp.append(p)
        PAIRS[:] = kept
        allp.sort(key=lambda p: p["pub"], reverse=True)
        os.makedirs(os.path.join(DOCS, "blog"), exist_ok=True)
        with open(os.path.join(DOCS, "blog", "index.html"), "w", encoding="utf-8") as f:
            f.write(render_index(allp, a.record, assets, biz, nav, foot))
        print(f"built    blog/  ({sum(p['built'] for p in allp)} linked, "
              f"{sum(not p['built'] for p in allp)} pending)")
    print("\nPAIRS")
    for slug, where, before, after, why in PAIRS:
        print(f"  [{slug[:40]}] {where}\n     BEFORE {before}\n     AFTER  {after}\n     WHY    {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
