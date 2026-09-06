#!/usr/bin/env python3
"""
Smoke tests for the NAP checks in audit.py.

WHY THIS FILE EXISTS. Rule 6 says the name, address and phone are
character-identical everywhere. audit.py is the mechanism that makes
that true instead of remembered, and on 2026-09-05 the mechanism was
found to be lying.

The address-variant pattern ended each alternative with \\b, which reads
as "a word character comes next." On a real page the character after
"995 Jaymor Rd." is a comma or a line break, so the boundary never
matched. Worse than a silent skip: the canonical string "995 Jaymor Rd"
is a PREFIX of the variant, so the plain `in` test found it inside
"995 Jaymor Rd." and the page was scored as CORRECTLY SPELLED. A check
that reports a pass on the exact input it exists to catch is worse than
no check, because it also tells everyone downstream to stop looking.

That bug was invisible from the outside: every page anyone had written
happened to spell the street the right way, so the check "worked" on
every input it had ever been given. Only a deliberately wrong page shows
it. So the deliberately wrong pages live here.

The same file covers the other two checks that must never drift back:
the CallRail tracking number, which must never reach the source, and the
one published email address.

No network and no external packages: audit.load is swapped for a
dictionary lookup, so this runs offline in a second.

Usage:
    python3 scripts/test-audit-checks.py     # exits 1 if anything fails
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit  # noqa: E402


FAILURES = []


def check(label: str, passed: bool, detail=""):
    """Records a result instead of raising, so one broken case cannot
    hide the ten after it."""
    print(f"  {'ok  ' if passed else 'FAIL'}  {label}")
    if not passed:
        FAILURES.append(f"{label}{f'  ->  {detail}' if detail != '' else ''}")


PAGE = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Collision Repair in Southampton, PA | Tri-County Collision</title>
<meta name="description" content="A description that is comfortably under one hundred and sixty characters, so the length checks never become the reason a case fails.">
<link rel="canonical" href="https://tricountycollision.com/collision-repair/">
<meta property="og:title" content="Collision Repair"><meta property="og:description" content="Short.">
</head><body><main><h1>Collision Repair</h1>
{body}
</main></body></html>"""


def run(body: str):
    """Audits one fabricated page and returns its three scored buckets as
    one searchable string each."""
    html = PAGE.format(body=body)
    audit.load = lambda _src, _h=html: _h
    passes, warns, fails, notes, kind = audit.audit("fabricated.html", coverage=None)
    return " ".join(passes), " ".join(warns), " ".join(fails)


# The address as it is meant to appear, used as the tail of most cases so
# the city line is never the reason a case fails.
CITY = "Southampton, PA 18966"


def main():
    print("1. The canonical spelling, which must keep passing")
    p, w, f = run(f"<p>995 Jaymor Rd, {CITY}</p>")
    check("   scored as the canonical spelling", "canonical spelling" in p, p)
    check("   no critical raised", "street address is spelled" not in f, f)

    print("2. THE REGRESSION: a trailing period, the case that scored a PASS")
    p, w, f = run(f"<p>995 Jaymor Rd., {CITY}</p>")
    check("   the period is caught as a variant", "995 Jaymor Rd." in f, f)
    check("   and it is NOT reported as the canonical spelling",
          "canonical spelling" not in p, p)

    print("3. Rd. at the end of a line, with nothing after it at all")
    p, w, f = run(f"<p>995 Jaymor Rd.<br>{CITY}</p>")
    check("   still caught", "street address is spelled" in f, f)

    print("4. Road spelled out")
    p, w, f = run(f"<p>995 Jaymor Road, {CITY}</p>")
    check("   caught as a variant", "995 Jaymor Road" in f, f)

    print("5. Both spellings on one page, which is what the live site does")
    p, w, f = run(f'<p>995 Jaymor Rd, {CITY}</p><p>Mail to 995 Jaymor Road, {CITY}</p>')
    check("   the variant fails even though the canonical is also present",
          "street address is spelled" in f, f)
    check("   and the page is not also credited with a pass",
          "canonical spelling" not in p, p)

    print("6. The street line with no city, state and ZIP")
    p, w, f = run("<p>995 Jaymor Rd</p>")
    check("   warned, not failed", "is not" in w and "street address is spelled" not in f, (w, f))

    print("7. Jaymor named with no address at all")
    p, w, f = run("<p>We are the shop on Jaymor.</p>")
    check("   failed for naming the street without the canonical address",
          "names Jaymor" in f, f)

    print("8. A page that never mentions the street")
    p, w, f = run("<p>We repair cars in Southampton.</p>")
    check("   the address check stays out of it entirely",
          "Jaymor" not in f and "canonical spelling" not in p, (p, f))

    print("9. The CallRail tracking number")
    p, w, f = run('<p>Call <a href="tel:+12157099665">(215) 709-9665</a></p>')
    check("   caught as a critical", "CallRail tracking number" in f, f)
    p, w, f = run('<p>Call <a href="tel:+12153225350">(215) 322-5350</a></p>')
    check("   the canonical phone is not mistaken for it",
          "CallRail tracking number" not in f, f)
    p, w, f = run("<p>Reach the shop on 215.709.9665 today.</p>")
    check("   caught when punctuated some other way", "CallRail tracking number" in f, f)

    print("10. The one published email address")
    check("    the email half of the contact check is ON",
          audit.NAP_EMAIL_RE is not None, audit.NAP_EMAIL_RE)
    p, w, f = run('<p><a href="mailto:info@tricountycollision.com">info@tricountycollision.com</a></p>')
    check("    the second mailbox is a critical", "info@tricountycollision.com" in f, f)
    p, w, f = run('<p><a href="mailto:contact@tricountycollision.com">contact@tricountycollision.com</a></p>')
    check("    the published address is not flagged",
          "info@tricountycollision.com" not in f, f)
    check("    and it is counted as a tappable contact",
          "tappable" in p, p)
    p, w, f = run("<p>Email contact@tricountycollision.com and we will reply.</p>")
    check("    a bare, untappable address is caught now that the check runs",
          "not linked" in w, w)

    print("11. The tracking number, swept across the files that BECOME pages")
    # audit.py scores built pages. It never sees templates/, and it never
    # sees a partial or an asset. The number is most likely to arrive in
    # exactly those places, pasted from the old site's header into a mold
    # that is then copied thirty-seven times. So this walks the two trees
    # that turn into the site and greps them directly.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hits = []
    for tree in ("templates", "docs"):
        for dirpath, dirnames, filenames in os.walk(os.path.join(root, tree)):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                try:
                    with open(full, encoding="utf-8", errors="replace") as fh:
                        text = fh.read()
                except OSError:
                    continue
                if audit.TRACKING_PHONE_RE.search(text):
                    hits.append(os.path.relpath(full, root))
    check("    no file under templates/ or docs/ carries it", not hits, hits)

    print("12. Every relative link under docs/ has a file behind it")
    # WHY. The nav on this site grows as pages land, and the standards say
    # never link to a page that does not exist. That rule is easy to keep
    # on the day you write it and impossible to keep across a
    # thirty-seven page migration, because the tempting move is always to
    # write the whole nav now and build the pages later. So it is checked
    # rather than remembered. It also catches the ordinary migration
    # accident: a stylesheet or a photo whose path is one ../ out.
    import glob as _glob
    bad = []
    for page in sorted(_glob.glob(os.path.join(root, "docs", "**", "*.html"),
                                  recursive=True)):
        with open(page, encoding="utf-8", errors="replace") as fh:
            html_text = fh.read()
        # Comments are stripped first: a commented-out link is not a link,
        # and this file's own explanations name paths that do not exist.
        html_text = re.sub(r"<!--[\s\S]*?-->", " ", html_text)
        here = os.path.dirname(page)
        for ref in re.findall(r'(?:href|src)="([^"]+)"', html_text):
            if ref.startswith(("http://", "https://", "tel:", "mailto:", "#", "data:")):
                continue
            target = os.path.normpath(os.path.join(here, ref.split("?")[0].split("#")[0]))
            if os.path.isdir(target):
                target = os.path.join(target, "index.html")
            elif not os.path.splitext(target)[1]:
                target = os.path.join(target, "index.html")
            if not os.path.isfile(target):
                bad.append(f"{os.path.relpath(page, root)} -> {ref}")
    check("    no relative link points at a missing file", not bad, bad)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) failed:")
        for x in FAILURES:
            print(f"  - {x}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
