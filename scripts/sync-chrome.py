#!/usr/bin/env python3
"""
Writes the site chrome, the header and the footer, into every real page
under docs/. proposed-changes.md 3.83.

WHY A SCRIPT. The chrome repeats in full on every page, and a menu typed
into 36 pages is 36 chances for one of them to drift. Here the chrome is
defined once, this writes it everywhere, and scripts/audit.py fails any page
whose chrome differs from every other page's in anything but the
current-page marking.

WHAT THE NAV IS, AND WHERE IT CAME FROM. Greg's ruling: the nav follows the
LIVE SITE'S navigation as the guide, minus Home, because the logo is the way
home. The items and their labels are the live site's own words, read off
its main menu on 2026-09-29:

    Collision Services      a dropdown: Collision Repair, Commercial
                            Collision Repair, Glass Repair & Replacement,
                            Paintless Dent Repair, and ADAS Calibration,
                            which the live nav does not carry because the
                            live site has no ADAS page. It slots in last,
                            under its page's own H1 words, as 3.83 ruled
                            it would (3.86)
    Areas We Serve          the parent links to the hub; the dropdown lists
                            every routed town, alphabetically
    Authorization Forms     the live nav's DocuSign PowerForm, new tab
    Contact Us, Blog        plain links

The nav carries no CarWise buttons: Greg withdrew them at his
click-through review (3.84), and /contact-us/ keeps both CarWise links.
"Menu" is the live site's own label for its phone toggle. "Explore", the footer column's heading, is the one chrome word not
migrated from the live site: a chrome label is furniture, not a claim.

WHAT IT TOUCHES. On every page that is not a redirect stub: everything from
the CHROME:HEAD marker to the end of the <header>, and the <footer
class="site"> element. Nothing else. A redirect stub stays bare.

THE CURRENT PAGE is the one thing allowed to differ between pages: every
chrome link that lands on the page itself is written "./" and carries
aria-current="page".

    python3 scripts/sync-chrome.py           # write every page
    python3 scripts/sync-chrome.py --check   # exit 1 if any page is out of date
"""
import glob
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
PHONE_TEL = "tel:+12153225350"
PHONE_TEXT = "(215) 322-5350"
EMAIL = "contact@tricountycollision.com"

# The service family is audit.SERVICES, the one list (3.87): the nav, the
# footer and every body enumeration take it from there, and the audit fails
# any enumeration that is not the whole family.
SERVICES = audit.SERVICES
HUB = ("areas-served/", "Areas We Serve")
CONTACT = ("contact-us/", "Contact Us")
BLOG = ("blog/", "Blog")


def towns():
    """Every routed town, ALPHABETICALLY: the one recorded order rule, no
    hand-curated ordering. The labels are the live nav's town names."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_town", os.path.join(ROOT, "scripts", "build-town.py"))
    bt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bt)
    return sorted(((f"areas-served-collision-repair-{k}/", bt.TOWN_NAMES[k]) for k in audit.TOWN_ROUTES),
                  key=lambda t: t[1])


def esc(s: str) -> str:
    return html.escape(s, quote=True)


CHEVRON = ('<svg class="nav-chev" viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
           '<path d="M2.5 4.5 6 8l3.5-3.5"/></svg>')


def render(page: str) -> tuple:
    """(head, foot) for the page at docs/<page>, where page is "" for home
    and "slug/" for every other page."""
    p = "" if page == "" else "../"

    def link(target, label, cls="", extra=""):
        here = target == page
        href = "./" if here else f"{p}{target}"
        c = f' class="{cls}"' if cls else ""
        cur = ' aria-current="page"' if here else ""
        return f'<a{c} href="{esc(href)}"{cur}{extra}>{label}</a>'

    def ext(url, label, cls=""):
        c = f' class="{cls}"' if cls else ""
        return f'<a{c} href="{esc(url)}" target="_blank" rel="noopener">{label}</a>'

    svc = "\n".join(f"              <li>{link(t, esc(l))}</li>" for t, l, _ln in SERVICES)
    twn = "\n".join(f"              <li>{link(t, esc(l))}</li>" for t, l in towns())
    home = link("", f'<img src="{p}logo.png" alt="Tri-County Collision" width="1332" height="530">',
                "nav-home", ' aria-label="Tri-County Collision, home"')

    head = f'''<!-- CHROME:HEAD, written by scripts/sync-chrome.py (proposed-changes.md 3.83).
       Edit the script, never this block: it is rewritten on every page, and
       scripts/audit.py fails a page whose chrome differs from the others in
       anything but the current-page marking.

       THE LOGO IS THE WAY HOME, so the nav carries no Home item. It has
       been a link since 2026-09-10: until then it was a span carrying
       data-pending-href="../" because docs/index.html did not exist. The
       homepage was built, the link test demanded the conversion by
       failing, and that was the conversion, the mechanism in 3.10 working
       end to end rather than being described. -->
  <header class="nav">
    <div class="wrap inner">
      {home}
      <nav class="nav-main" id="navmenu" aria-label="Main">
        <ul class="nav-list">
          <li class="nav-item has-sub">
            <button class="nav-sub-toggle" type="button" aria-expanded="false" aria-controls="nav-sub-services">Collision Services{CHEVRON}</button>
            <ul class="nav-sub" id="nav-sub-services">
{svc}
            </ul>
          </li>
          <li class="nav-item has-sub">
            {link(*HUB)}<button class="nav-sub-toggle nav-sub-icon" type="button" aria-expanded="false" aria-controls="nav-sub-areas" aria-label="Toggle submenu for Areas We Serve">{CHEVRON}</button>
            <ul class="nav-sub nav-sub-towns" id="nav-sub-areas">
{twn}
            </ul>
          </li>
          <li class="nav-item">{ext(audit.DOCUSIGN_URL, "Authorization Forms")}</li>
          <li class="nav-item">{link(*CONTACT)}</li>
          <li class="nav-item">{link(*BLOG)}</li>
        </ul>
      </nav>
      <a class="btn btn-sm nav-call" href="{PHONE_TEL}">Call {PHONE_TEXT}</a>
      <button class="navtoggle" type="button" aria-expanded="false" aria-controls="navmenu">
        <svg class="ico-open" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        <svg class="ico-close" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>
        <span>Menu</span>
      </button>
    </div>
  </header>'''

    maps = esc(audit.MAPS_NAP_URL)
    explore = [link(t, esc(l).replace("Commercial Collision Repair", "Commercial Collision&nbsp;Repair"))
               for t, l, _ln in SERVICES] + [link(*BLOG), link(*CONTACT)]
    exp = "\n".join(f"            <li>{x}</li>" for x in explore)
    areas = [link(t, esc(l)) for t, l in towns()] + [link(HUB[0], "Every town we serve")]
    are = "\n".join(f"            <li>{x}</li>" for x in areas)
    foot = f'''<footer class="site">
    <div class="wrap">
      <div class="foot-grid">
        <div class="foot-id">
          {link("", f'<img src="{p}logo.png" alt="Tri-County Collision" width="1332" height="530">', "foot-home", ' aria-label="Tri-County Collision, home"')}
          <p class="foot-tag">Family owned collision repair in Southampton, PA, serving Bucks County, Montgomery County and Northeast Philadelphia.</p>
          <p class="foot-nap">
            Tri-County Collision<br>
            <a href="{maps}" target="_blank" rel="noopener">995 Jaymor Rd<br>
            Southampton, PA 18966</a><br>
            <a href="{PHONE_TEL}">{PHONE_TEXT}</a><br>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
          </p>
        </div>
        <div class="foot-hours">
          <h2 class="foot-head">Hours</h2>
          <p>Monday to Friday, 8&nbsp;a.m. to 6&nbsp;p.m.<br>
          Saturday by appointment only</p>
        </div>
        <div class="foot-start">
          <h2 class="foot-head">Get Started</h2>
          <ul class="foot-links">
            <li><a href="{PHONE_TEL}">Call {PHONE_TEXT}</a></li>
            <li><a href="mailto:{EMAIL}">Email the shop</a></li>
            <li>{link(*CONTACT[:1], "Send us your details online")}</li>
          </ul>
        </div>
        <div class="foot-explore">
          <!-- These columns list only pages that exist. They grow as pages
               land, and never before. EXPLORE AND AREAS WE SERVE ARE THE
               FULL MAP (3.83, 3.89): every service page, the blog and
               contact here, every town and the hub in the next column, so
               no page is a dead end from its foot. Privacy joins Explore
               when it ships. The labels are the nav's, so each destination
               has ONE name across the chrome. -->
          <h2 class="foot-head">Explore</h2>
          <ul class="foot-links">
{exp}
          </ul>
        </div>
        <div class="foot-areas">
          <!-- AREAS WE SERVE, its own column since 3.89, Greg's ruling. The
               towns are TOWN_ROUTES, alphabetical, never typed; the column
               ends at the hub, in the site's own phrase. -->
          <h2 class="foot-head">Areas We Serve</h2>
          <ul class="foot-links foot-towns">
{are}
          </ul>
        </div>
      </div>
      <div class="foot-bottom">
        <!-- The year is written into the markup so it is right with
             JavaScript off, and assets/site.js updates it so it is right
             next January. A hard-coded year is a stale-clock claim. -->
        <p>&copy; <span data-year>2026</span> Tri-County Collision &middot; <a href="{maps}" target="_blank" rel="noopener">995 Jaymor Rd, Southampton, PA 18966</a> &middot; <a href="{PHONE_TEL}">{PHONE_TEXT}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </footer>'''
    return head, foot


HEAD_RE = re.compile(r"(?s)(?:<!-- CHROME:HEAD.*?-->\s*)?<header class=\"nav\">.*?</header>")
FOOT_RE = re.compile(r'(?s)<footer class="site">.*?</footer>')


def page_of(path: str) -> str:
    rel = os.path.relpath(os.path.dirname(path), DOCS)
    return "" if rel == "." else rel.replace(os.sep, "/") + "/"


def is_stub(text: str) -> bool:
    return re.search(r'http-equiv=["\']refresh', text, re.I) is not None


def synced(path: str, text: str) -> str:
    head, foot = render(page_of(path))
    if len(HEAD_RE.findall(text)) != 1 or len(FOOT_RE.findall(text)) != 1:
        raise SystemExit(f"FAILED: {os.path.relpath(path, ROOT)} does not carry exactly one header "
                         f"and one footer to replace. Nothing written.")
    text = HEAD_RE.sub(lambda m: head, text)
    return FOOT_RE.sub(lambda m: foot, text)


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for path in sorted(glob.glob(os.path.join(DOCS, "**", "index.html"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if is_stub(text):
            continue
        new = synced(path, text)
        if new != text:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    if check:
        if stale:
            print(f"{len(stale)} page(s) carry chrome that is not the generator's:")
            for p in stale:
                print(f"  {p}")
            print("Run scripts/sync-chrome.py.")
            return 1
        print("Every page carries the generated chrome.")
        return 0
    print(f"wrote {len(stale)} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
