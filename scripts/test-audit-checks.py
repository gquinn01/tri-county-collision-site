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

import glob
import html
import json
import os
import re
import subprocess
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
    # drafts/ is included while it exists. It is throwaway design work, but
    # it is throwaway design work that gets copied FROM, and the tracking
    # number has no business travelling out of it either.
    for tree in ("templates", "docs", "drafts"):
        if not os.path.isdir(os.path.join(root, tree)):
            continue
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
    check("    no file under templates/, docs/ or drafts/ carries it", not hits, hits)

    print("12. Links, both directions: nothing dead, nothing forgotten")
    # WHY, DIRECTION ONE. The nav on this site grows as pages land, and
    # the standards say never link to a page that does not exist. That
    # rule is easy to keep on the day you write it and impossible to keep
    # across a thirty-seven page migration, because the tempting move is
    # always to write the whole nav now and build the pages later. It also
    # catches the ordinary migration accident: a stylesheet or a photo
    # whose path is one ../ out.
    #
    # WHY DIRECTION TWO, ADDED 2026-09-10. Enforcing direction one leaves
    # a residue: elements that SHOULD be links and are not yet. The logo,
    # the breadcrumb's "Home", the online-estimate phrases, the paintless
    # dent repair mention, the blog post in FAQ 5. Waiting was the
    # unmechanized half. Nothing recorded what each was waiting for and
    # nothing would notice the day the wait ended, so a page could ship
    # built and unlinked with a span sitting where its link belongs, and
    # direction one would report a clean site the whole time.
    #
    # Each now carries data-pending-href with the URL it becomes, and this
    # fails the moment that URL resolves to a real file. BOTH DIRECTIONS
    # RESOLVE THROUGH audit.resolve_local_link, so they cannot disagree
    # about what "../" means.
    import glob as _glob
    import tempfile as _tempfile

    def dead_links(under):
        out = []
        for page in sorted(_glob.glob(os.path.join(under, "**", "*.html"),
                                      recursive=True)):
            with open(page, encoding="utf-8", errors="replace") as fh:
                html_text = fh.read()
            # Comments are stripped first: a commented-out link is not a
            # link, and this file's own explanations name paths that do
            # not exist.
            html_text = re.sub(r"<!--[\s\S]*?-->", " ", html_text)
            # THE ATTRIBUTE BOUNDARY IS load-BEARING. "href" is a
            # substring of "data-pending-href", so an unanchored pattern
            # reads every pending link as a dead link, which is exactly
            # what it did the first time this ran. A pending link is the
            # opposite of a dead one.
            for ref in re.findall(r'(?:^|\s)(?:href|src)="([^"]+)"', html_text):
                if ref.startswith(("http://", "https://", "tel:", "mailto:",
                                   "#", "data:")):
                    continue
                if not os.path.isfile(audit.resolve_local_link(page, ref)):
                    out.append(f"{os.path.relpath(page, under)} -> {ref}")
        return out

    check("    no relative link points at a missing file",
          not dead_links(os.path.join(root, "docs")), dead_links(os.path.join(root, "docs")))

    live = [x for x in audit.find_pending_links(os.path.join(root, "docs")) if x[4]]
    check("    no data-pending-href points at a page that now exists",
          not live, [f"{os.path.relpath(pth, root)}:{ln} {href}"
                     for pth, ln, href, _t, _r in live])

    # The inventory used to be asserted non-empty: if it ever emptied,
    # either every referenced page existed or somebody had deleted the
    # attributes instead of converting them. 3.82 built the whole areas
    # tier, so it is legitimately empty now, and the check is split into
    # the two things it was protecting (3.82):
    #   the reader still finds a pending link when one exists (a fixture);
    #   every town page is a REAL link from the hub, so an empty inventory
    #   means done, not deleted.
    with _tempfile.TemporaryDirectory() as _ptmp:
        os.makedirs(os.path.join(_ptmp, "a"))
        with open(os.path.join(_ptmp, "a", "index.html"), "w", encoding="utf-8") as fh:
            fh.write('<span data-pending-href="../later/">waiting</span>')
        _found = audit.find_pending_links(_ptmp)
    check("    the pending inventory reader still finds a pending link when one exists",
          len(_found) == 1 and _found[0][2] == "../later/" and not _found[0][4], _found)
    _hub = open(os.path.join(root, "docs", "areas-served", "index.html"), encoding="utf-8").read()
    _unlinked = [k for k in audit.TOWN_ROUTES
                 if f'<a href="../{audit.TOWN_ROUTE_PREFIX}{k}/">' not in _hub]
    check("    and every town page is a real link from the hub: an empty inventory means done, not deleted",
          not _unlinked, _unlinked)

    # --- fixtures, so both directions are proved on inputs we control ---
    with _tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "svc"))
        with open(os.path.join(tmp, "svc", "index.html"), "w", encoding="utf-8") as fh:
            fh.write('<a href="../gone/">dead</a>'
                     '<span data-pending-href="../soon/">waiting</span>'
                     '<!-- <a href="../commented-out/">not a link</a> -->')
        check("     DIRECTION 1: an href with no file behind it fails",
              dead_links(tmp) == ["svc/index.html -> ../gone/"], dead_links(tmp))
        check("     a link inside a comment is not a link",
              not any("commented-out" in x for x in dead_links(tmp)), dead_links(tmp))
        check("     a data-pending-href is NOT read as an href",
              not any("soon" in x for x in dead_links(tmp)), dead_links(tmp))
        check("     DIRECTION 2: a pending href stays quiet while unbuilt",
              [x for x in audit.find_pending_links(tmp) if x[4]] == [])

        # Now build the page it was waiting for. The wait is over, and the
        # span is still a span.
        os.makedirs(os.path.join(tmp, "soon"))
        with open(os.path.join(tmp, "soon", "index.html"), "w", encoding="utf-8") as fh:
            fh.write("<h1>built</h1>")
        now_live = [x for x in audit.find_pending_links(tmp) if x[4]]
        check("     DIRECTION 2: the day its target exists, it FAILS",
              len(now_live) == 1, now_live)
        check("     and it reports the file, the line and the href",
              bool(now_live) and now_live[0][1] == 1
              and now_live[0][2] == "../soon/", now_live)

        # Converting it is what clears the failure, and the converted link
        # then has a real file behind it, so direction one stays quiet.
        pth = os.path.join(tmp, "svc", "index.html")
        body = open(pth, encoding="utf-8").read().replace(
            '<span data-pending-href="../soon/">waiting</span>',
            '<a href="../soon/">waiting</a>')
        open(pth, "w", encoding="utf-8").write(body)
        check("     converting it to a real link clears BOTH directions",
              [x for x in audit.find_pending_links(tmp) if x[4]] == []
              and dead_links(tmp) == ["svc/index.html -> ../gone/"],
              dead_links(tmp))

    # Both halves resolve "../" through the same function, which is the
    # only reason they can be trusted to agree.
    check("     both directions share one resolver",
          "audit.resolve_local_link" in open(
              os.path.abspath(__file__), encoding="utf-8").read())

    print("13. The review count, which is the one number that rots on its own")
    # WHY. A review count is true on the day it is read and quietly wrong
    # every week after, and nothing on the page changes when it goes
    # wrong. On 2026-09-10 the live site's Trustindex widget said 231 and
    # the shop's own Google Business Profile said 274, in the same week.
    # Nobody would have noticed by eye. So both halves are checked: that
    # every visible mention agrees, and that the recorded reading is not
    # stale. These cases are the ones that must never score a pass.
    import tempfile as _tempfile
    from datetime import date as _date, timedelta as _timedelta

    with _tempfile.TemporaryDirectory() as tmp:
        # The real markup shape: the numeral and the words live in two
        # separate spans, so anything matching raw HTML would miss it.
        with open(os.path.join(tmp, "index.html"), "w", encoding="utf-8") as fh:
            fh.write('<!-- It was 231 on 2026-09-05, off the widget. -->\n'
                     '<span class="stat-n">274</span>\n'
                     '<span class="stat-l">Google reviews</span>\n'
                     '<script>var old = "199 reviews";</script>')
        with open(os.path.join(tmp, "llms.txt"), "w", encoding="utf-8") as fh:
            fh.write("Rated 4.9 across 274 Google reviews.\n")

        found = audit.find_review_counts(tmp)
        nums = sorted(n for _p, n, _s in found)
        check("     the numeral and the words in separate spans are still read as one count",
              274 in nums, nums)
        check("     a comment recording the OLD number is not counted as a claim",
              231 not in nums, nums)
        check("     a number inside <script> is not counted either",
              199 not in nums, nums)
        check("     llms.txt is scanned, not just the pages",
              nums == [274, 274], nums)

    def run_review(hits, counted_on, today):
        """One call of the check against fixed inputs. find_review_counts
        is swapped out so the cases are the fixtures, not the repo."""
        real_find, real_date = audit.find_review_counts, audit.REVIEW_COUNTED_ON
        audit.find_review_counts = lambda root=None: hits
        audit.REVIEW_COUNTED_ON = counted_on
        try:
            passes, warns, fails, notes = [], [], [], []
            audit.check_review_count_local(passes, warns, fails, notes, today=today)
            return warns, fails, notes
        finally:
            audit.find_review_counts, audit.REVIEW_COUNTED_ON = real_find, real_date

    TODAY = _date(2026, 9, 10)
    N = audit.REVIEW_COUNT
    agree = [("docs/a/index.html", N, "274 Google reviews")]
    disagree = agree + [("docs/b/index.html", 231, "231 Google reviews")]

    warns, fails, notes = run_review(agree, "2026-09-10", TODAY)
    check("     agreement on the day it was counted is clean", not fails and not warns,
          fails + warns)
    check("     and it reports as a note rather than a pass",
          len(notes) == 1, notes)

    warns, fails, notes = run_review(disagree, "2026-09-10", TODAY)
    check("     TWO PAGES THAT DISAGREE ARE A CRITICAL", len(fails) == 1, fails)
    check("     and the critical names both numbers",
          bool(fails) and "231" in fails[0] and "274" in fails[0], fails)
    check("     and names the files, so it can be fixed without a search",
          bool(fails) and "docs/b/index.html" in fails[0], fails)

    # The recorded constant counts as one of the instances. A single page
    # that drifts from it has nothing else on the site to disagree with,
    # and that is exactly when a wrong number survives longest.
    lone = [("docs/a/index.html", 231, "231 Google reviews")]
    warns, fails, notes = run_review(lone, "2026-09-10", TODAY)
    check("     ONE page disagreeing with REVIEW_COUNT is a critical too",
          len(fails) == 1, fails)

    warns, fails, notes = run_review(agree, str(TODAY - _timedelta(days=35)), TODAY)
    check("     exactly 35 days old is not yet stale", not warns, warns)
    warns, fails, notes = run_review(agree, str(TODAY - _timedelta(days=36)), TODAY)
    check("     36 days old is a WARNING, not a critical",
          len(warns) == 1 and not fails, warns + fails)
    check("     and the warning says how old it is",
          bool(warns) and "36 days old" in warns[0], warns)

    warns, fails, notes = run_review(agree, str(TODAY + _timedelta(days=1)), TODAY)
    check("     a counted-on date in the future is caught", len(warns) == 1, warns)

    warns, fails, notes = run_review([], "2026-09-10", TODAY)
    check("     no mention anywhere is a note, not a failure",
          not fails and not warns and len(notes) == 1, fails + warns + notes)

    # The whole point of a critical is that --strict stops the build.
    src = open(os.path.join(root, "scripts", "audit.py"), encoding="utf-8").read()
    check("     --strict actually exits 1 on a site-wide critical",
          "opts.strict and (below or site_fails)" in src)

    print("14. No review or rating markup anywhere, which is the other half")
    # WHY. The count is published as visible text ON PURPOSE. Google's
    # guidelines rule out self-serving review markup on a business's own
    # site, and the standards allow no review or rating markup unless the
    # data is real and the owner has decided to publish it. The number
    # being true is not the same as the markup being allowed.
    marked = []
    for dirpath, _dirs, files in os.walk(os.path.join(root, "docs")):
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            full = os.path.join(dirpath, name)
            with open(full, encoding="utf-8", errors="replace") as fh:
                body = fh.read()
            for script in re.findall(r"(?is)<script[^>]*ld\+json[^>]*>(.*?)</script>", body):
                if re.search(r'"(aggregateRating|ratingValue|reviewCount|reviewRating)"',
                             script):
                    marked.append(os.path.relpath(full, root))
    check("     no page carries aggregateRating, ratingValue or reviewCount in its schema",
          not marked, marked)

    print("15. The comment convention, which is the blind spot's dressing")
    # WHY. audit.py strips comments before it reads review counts, so a
    # number quoted in a comment can rot with nothing to catch it. On
    # 2026-09-10 the stat band's own comment was found carrying a stale
    # count and a stale order, through two commits, and no check could
    # have seen it. The convention is that comments name REVIEW_COUNT and
    # the band's DOM order instead of quoting either. This is the check
    # that watches for the convention lapsing.
    import inspect as _inspect
    import tempfile as _tempfile

    def comment_hits(body):
        with _tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "p.html"), "w", encoding="utf-8") as fh:
                fh.write(body)
            return audit.find_rotting_comments(tmp)

    check("     a comment quoting a literal count is caught",
          len(comment_hits("<!-- It was 274 reviews on the profile. -->")) == 1)
    check("     the other word order is caught too",
          len(comment_hits("<!-- The reviews stood at 274 that day. -->")) == 1)
    check("     a comment wrapped across lines is still one sentence",
          len(comment_hits("<!-- It was 274\n         Google reviews. -->")) == 1)

    # THE POINT OF THE CONVENTION: the approved spelling is the one the
    # pattern cannot fire on, because the character after "REVIEW" in
    # REVIEW_COUNT is an underscore and an underscore is a word
    # character. The rule is easy to keep rather than easy to resent.
    check("     naming REVIEW_COUNT instead is NOT caught, by construction",
          comment_hits("<!-- The count lives in REVIEW_COUNT, set 2026 in audit.py. -->") == [])
    check("     naming the band's DOM order instead is NOT caught",
          comment_hits("<!-- The order is the band's DOM order. Read the markup. -->") == [])

    check("     one digit beside the word is prose, not a count",
          comment_hits("<!-- Ask for a 5 star review. -->") == [])
    check("     five digits is not a count this shop will have",
          comment_hits("<!-- 12345 reviews someday. -->") == [])
    check("     a number more than a few words away is left alone",
          comment_hits("<!-- 274 is the number of things that are not "
                       "at all related to any reviews here. -->") == [])

    # Structurally incapable of failing: it is not handed anywhere to put
    # a critical. A promise in a docstring is not a mechanism.
    params = list(_inspect.signature(audit.check_comment_convention_local).parameters)
    check("     the check cannot raise a critical, having no fails list",
          params == ["warns", "notes"], params)

    warns, notes = [], []
    audit.check_comment_convention_local(warns, notes)
    check("     and the repo's own comments are clean right now",
          not warns and len(notes) == 1, warns)

    print("16. The counting effect is withdrawn, and the lane still draws once")
    # WHY. From 2026-09-10 the stat band's figures rolled like an odometer
    # on first arrival, and this section proved the roll never disturbed
    # the review count. GREG'S RULING, proposed-changes.md 3.85: the effect
    # leaves the site, the rolling digits and the rolling word both. The
    # figures stand still as the text they are in the markup. This section
    # now proves the absence, and holds the motion law's remaining claims
    # about the lane, the one arrival effect left.
    import re as _re16
    import tempfile as _tempfile2

    site_js = open(os.path.join(root, "docs", "assets", "site.js"),
                   encoding="utf-8").read()
    site_css = open(os.path.join(root, "docs", "assets", "site.css"),
                    encoding="utf-8").read()
    js_code = _re16.sub(r"/\*.*?\*/", "", site_js, flags=_re16.S)
    css_code = _re16.sub(r"/\*.*?\*/", "", site_css, flags=_re16.S)
    check("     site.js builds no odometer, digit or word",
          not _re16.search(r"buildOdometer|buildWordOdometer|ODO_|WORD_TRAVEL|odo-", js_code))
    check("     site.js never touches the stat band or its figures",
          not _re16.search(r"statband|stat-n|fig-n", js_code))
    check("     site.css carries no .odo rule",
          not _re16.search(r"\.odo\b", css_code))
    odo_pages = [os.path.relpath(dp, root) for dp, _dn, fn in os.walk(os.path.join(root, "docs"))
                 for f in fn if f.endswith(".html")
                 and _re16.search(r'class="[^"]*\bodo\b', open(os.path.join(dp, f), encoding="utf-8").read())]
    check("     and no page carries odometer markup", not odo_pages, odo_pages)

    # The lane: once, on first arrival, never under reduced motion, and
    # resting fully drawn when it does not run.
    check("     the lane is still built and armed on its own section",
          "buildLane(steps)" in js_code and "sections.push(steps" in js_code)
    check("     it fires once: the observer unobserves on first arrival",
          "io.unobserve(entry.target)" in js_code)
    guard = js_code.find("if (reduceMQ.matches) { return; }")
    check("     reduced motion returns before anything is armed",
          0 <= guard < js_code.find('classList.add("motion-armed")'))
    rm = _re16.search(r"@media \(prefers-reduced-motion: reduce\) \{\s*\.lane-dash, \.faq-ico \{ transition: none; \}\s*\.lane-dash \{ transform: scaleY\(1\); \}", css_code)
    check("     and under it the lane rests fully drawn in site.css", bool(rm))
    check("     nothing in site.js loops: no interval, no animation frame",
          not _re16.search(r"setInterval|requestAnimationFrame", js_code))

    hits = audit.find_review_counts(os.path.join(root, "docs"))
    # NOT "exactly once". This asserted a count of 1 while docs/ held one
    # page, and a second page stating the same true number failed it on the
    # day the homepage landed. The invariant was never "one mention", it is
    # "every mention agrees with the recorded count".
    check("     every stated count under docs/ is the recorded number",
          bool(hits) and all(h[1] == audit.REVIEW_COUNT for h in hits),
          [(h[0], h[1]) for h in hits])
    check("     and at least one page states it",
          len(hits) >= 1, len(hits))

    # And the review-count check would still notice odometer strips baked
    # into a page, the one way the withdrawn effect could come back as
    # markup rather than script.
    with _tempfile2.TemporaryDirectory() as tmp:
        strip = "".join("<span>%d</span>" % d for d in range(10))
        with open(os.path.join(tmp, "p.html"), "w", encoding="utf-8") as fh:
            fh.write('<span class="stat-n"><span class="odo">'
                     '<span class="odo-d"><span class="odo-strip">'
                     '<span>2</span>' + strip + '<span>4</span>'
                     '</span></span></span></span>'
                     '<span class="stat-l">Google reviews</span>')
        baked = audit.find_review_counts(tmp)
        nums = sorted({n for _p, n, _s in baked})
        check("     a PRE-RENDERED strip would be caught, not silently accepted",
              bool(baked) and nums != [audit.REVIEW_COUNT], nums)

    print("17. Asset provenance: an AI-generated image must never land")
    # WHY THIS EXISTS. Rule 9 bans AI imagery and had no mechanism, so
    # for the whole build it was enforced by somebody choosing to look.
    # On 2026-09-17 two licensed candidates for the We Fix It All render
    # were both AI, and each gave itself away in a DIFFERENT tag: one in
    # the IPTC source type, one in the tool field. Either tell alone
    # would have passed the other file.
    #
    # The fixtures are written here rather than committed, because
    # committing a known-AI image to prove the check catches AI images
    # would put a known-AI image in the repo.
    import tempfile as _tempfile3

    IPTC = "http://cv.iptc.org/newscodes/digitalsourcetype/"

    def prov(xmp: str) -> dict:
        """Writes a fixture carrying `xmp` and reads it back."""
        with _tempfile3.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.jpg")
            with open(path, "wb") as fh:
                fh.write(b"\xff\xd8\xff\xe1" + xmp.encode("utf-8") + b"\xff\xd9")
            return audit.read_asset_provenance(path)

    a = prov(f"<Iptc4xmpExt:DigitalSourceType>{IPTC}trainedAlgorithmicMedia"
             "</Iptc4xmpExt:DigitalSourceType>")
    check("     trainedAlgorithmicMedia as an element is caught",
          bool(a["reasons"]) and "trainedAlgorithmicMedia" in a["source_type"], a)

    a = prov(f'Iptc4xmpExt:DigitalSourceType="{IPTC}trainedAlgorithmicMedia"')
    check("     and as an ATTRIBUTE, which is the other legal spelling",
          bool(a["reasons"]), a)

    a = prov(f"<Iptc4xmpExt:DigitalSourceType>{IPTC}"
             "compositeWithTrainedAlgorithmicMedia</Iptc4xmpExt:DigitalSourceType>")
    check("     a part-generative composite is caught too",
          bool(a["reasons"]), a)

    a = prov("<xmp:CreatorTool>OkiDokiBot AI Art Generator</xmp:CreatorTool>")
    check("     THE SECOND TELL: an AI generator in the tool field, with no "
          "source type at all", bool(a["reasons"]) and not a["source_type"], a)

    a = prov("<xmp:CreatorTool>Midjourney</xmp:CreatorTool>")
    check("     and the other generators by name", bool(a["reasons"]), a)

    # THE CASES THAT MUST KEEP PASSING. Failing these would ban the very
    # asset this check was written to let through: a real 3D ghosted
    # render is a person at a workstation, and its source type says so.
    a = prov(f"<Iptc4xmpExt:DigitalSourceType>{IPTC}digitalCapture"
             "</Iptc4xmpExt:DigitalSourceType>")
    check("     a camera passes", not a["reasons"], a)

    a = prov(f"<Iptc4xmpExt:DigitalSourceType>{IPTC}digitalArt"
             "</Iptc4xmpExt:DigitalSourceType>")
    check("     digitalArt passes, WHICH IS THE POINT: that is a real 3D render",
          not a["reasons"], a)

    a = prov(f"<Iptc4xmpExt:DigitalSourceType>{IPTC}algorithmicMedia"
             "</Iptc4xmpExt:DigitalSourceType>")
    check("     algorithmicMedia passes: procedural is not generative",
          not a["reasons"], a)

    a = prov('dcterms:provenance="https://cai-manifests.adobe.com/manifests/urn-c2pa-x"'
             f'<Iptc4xmpExt:DigitalSourceType>{IPTC}digitalCapture'
             "</Iptc4xmpExt:DigitalSourceType>")
    check("     a C2PA manifest ALONE is not a tell: real stock carries one",
          not a["reasons"] and a["c2pa"], a)

    a = prov("<xmp:CreatorTool>Adobe Photoshop 26.0 (Macintosh)</xmp:CreatorTool>")
    check("     ordinary editing software passes", not a["reasons"], a)

    a = prov("")
    check("     and a file with no metadata passes, because a label is all "
          "this can read", not a["reasons"], a)

    # The wiring, not just the reader: the check has to be able to fail a
    # build. The comment-convention check is deliberately handed no fails
    # list; this one must have one.
    with _tempfile3.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "assets", "img"))
        with open(os.path.join(tmp, "assets", "img", "bad.jpg"), "wb") as fh:
            fh.write(b"\xff\xd8" + (f"<Iptc4xmpExt:DigitalSourceType>{IPTC}"
                                    "trainedAlgorithmicMedia"
                                    "</Iptc4xmpExt:DigitalSourceType>").encode())
        with open(os.path.join(tmp, "assets", "img", "drawn.svg"), "w") as fh:
            fh.write("<svg>midjourney</svg>")
        found = audit.find_assets(tmp)
        check("     find_assets reads rasters and leaves .svg alone, because an "
              "svg here is our own drawing", len(found) == 1, [x["path"] for x in found])

        _sd = audit.SITE_DIR
        audit.SITE_DIR = tmp
        try:
            p2, w2, f2, n2 = [], [], [], []
            audit.check_asset_provenance_local(p2, w2, f2, n2)
        finally:
            audit.SITE_DIR = _sd
        check("     and it raises a CRITICAL, not a warning",
              len(f2) == 1 and not w2, (f2, w2))
        check("     which names the file", "bad.jpg" in f2[0], f2)
        check("     and refuses the shortcut of stripping the label",
              "strip the label" in f2[0], f2)

    real = audit.find_assets(os.path.join(root, "docs"))
    check("     every image in the repo right now is clean",
          bool(real) and all(not a["reasons"] for a in real),
          [a["path"] for a in real if a["reasons"]])

    print("18. The brand count: the marks, the words and the schema agree")
    # WHY. The live site does this wrong RIGHT NOW, which is the whole
    # argument for the check: its carousel shows fourteen marks while its
    # own prose says a dozen. Nobody typed that discrepancy on purpose.
    # A strip is built once in a page builder and the prose is written
    # somewhere else, and after that neither one knows about the other.
    # This build says the number in four kinds of place, so it has four
    # ways to drift and needs a mechanism rather than a memory.

    STRIP = ('<ul class="brandtrack">%s</ul>'
             % "".join('<li><img src="b/%d.png" alt="B%d"></li>' % (i, i)
                       for i in range(12)))
    DUPE = ('<ul class="brandtrack" aria-hidden="true">%s</ul>'
            % "".join('<li><img src="b/%d.png" alt="B%d"></li>' % (i, i)
                      for i in range(12)))

    with _tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "index.html"), "w", encoding="utf-8") as fh:
            fh.write("<!-- we used to say 9 vehicle brands -->\n"
                     + STRIP + DUPE + DUPE
                     + "<p>factory training for a dozen vehicle brands</p>"
                     + "<p>Twelve manufacturers, and the procedures</p>"
                     + "<p>factory-certified for 12+ vehicle brands</p>"
                     + '<script type="application/ld+json">'
                     + '{"text":"a collision center for 12+ vehicle brands"}</script>'
                     + '<script>var old = "7 vehicle brands";</script>')
        found = audit.find_brand_claims(tmp)
        marks = [n for _p, n, _s in found["marks"]]
        text = sorted(n for _p, n, _s in found["text"])
        schema = [n for _p, n, _s in found["schema"]]
        check("     the strip is counted once, not once per duplicate track",
              marks == [12], marks)
        check("     the aria-hidden tracks are not counted as brands",
              sum(marks) == 12, marks)
        check("     \"a dozen\", \"Twelve\" and \"12+\" all read as 12",
              text == [12, 12, 12], text)
        check("     a comment recording an old count is not a claim",
              9 not in text, text)
        check("     a number inside a plain <script> is not a claim either",
              7 not in text, text)
        check("     JSON-LD is read separately from visible text",
              schema == [12], schema)

    def run_brand(found):
        """One call of the check against fixed inputs, with the finder
        swapped out so the cases are the fixtures and not the repo."""
        real_find = audit.find_brand_claims
        audit.find_brand_claims = lambda root=None: found
        try:
            passes, warns, fails, notes = [], [], [], []
            audit.check_brand_count_local(passes, warns, fails, notes)
            return warns, fails, notes
        finally:
            audit.find_brand_claims = real_find

    N = audit.BRAND_COUNT
    agree = {"marks": [("docs/index.html", N, "12 marks in the strip")],
             "text": [("docs/index.html", N, "a dozen vehicle brands")],
             "schema": [("docs/collision-repair/index.html", N, "12+ vehicle brands")]}
    warns, fails, notes = run_brand(agree)
    check("     agreement across marks, text and schema is clean",
          not fails and not warns, fails + warns)
    check("     and it reports as a note rather than a pass",
          len(notes) == 1, notes)

    # THE LIVE SITE'S OWN STATE, as a fixture: fourteen marks over a
    # sentence that says a dozen. This is the case the check exists for.
    live = dict(agree, marks=[("docs/index.html", 14, "14 marks in the strip")])
    warns, fails, notes = run_brand(live)
    check("     FOURTEEN MARKS OVER A DOZEN IN WORDS IS A CRITICAL",
          len(fails) == 1 and not warns, fails + warns)
    check("     and the critical names both numbers",
          bool(fails) and "12" in fails[0] and "14" in fails[0], fails)
    check("     and says which kind of place each came from",
          bool(fails) and "marks in" in fails[0] and "text in" in fails[0], fails)

    schema_drift = dict(agree, schema=[("docs/collision-repair/index.html", 13,
                                        "13 vehicle brands")])
    warns, fails, notes = run_brand(schema_drift)
    check("     schema drifting from the page is a critical too",
          len(fails) == 1, fails)
    check("     and the report names the schema as the odd one out",
          bool(fails) and "schema in" in fails[0], fails)

    # The recorded constant is one of the voices, so one lonely page that
    # drifts has something to disagree with. That is exactly the case a
    # wrong number survives longest in.
    lone = {"marks": [], "schema": [],
            "text": [("docs/index.html", 14, "14 vehicle brands")]}
    warns, fails, notes = run_brand(lone)
    check("     ONE page disagreeing with BRAND_COUNT is a critical too",
          len(fails) == 1, fails)

    empty = {"marks": [], "text": [], "schema": []}
    warns, fails, notes = run_brand(empty)
    check("     no mention anywhere is a note, not a failure",
          not fails and not warns and len(notes) == 1, fails + warns + notes)

    # And the strip as it actually ships, because a fixture that passes
    # while the real page fails is a fixture that lies.
    _sd = audit.SITE_DIR
    try:
        audit.SITE_DIR = os.path.join(root, "docs")
        passes, warns, fails, notes = [], [], [], []
        audit.check_brand_count_local(passes, warns, fails, notes)
    finally:
        audit.SITE_DIR = _sd
    check("     the strip that ships agrees with every page that ships",
          not fails, fails)

    # Greg's ruling of 2026-09-24, proposed-changes.md 3.53: an execution
    # page declares its kind and is exempt from the checks listed against
    # that kind and from nothing else. BOTH DIRECTIONS are held here: the
    # declared page still fails what it should, and a page that does not
    # declare gets no exemption. Same shape as the address check, which
    # needed a mechanism after it scored a wrong address as a pass.
    print("19. The contact kind: exempt from exactly two checks, nothing else")
    check("     the contact kind lists exactly the two ruled checks",
          audit.RUBRIC_EXEMPTIONS.get("contact") == ("faq-schema", "thin-content"),
          audit.RUBRIC_EXEMPTIONS.get("contact"))
    check("     no blanket kind exists, utility above all: exactly the ruled kinds",
          audit.RUBRIC_EXEMPTIONS == {"contact": ("faq-schema", "thin-content"),
                                      "post": ("faq-schema",),
                                      "blog-index": ("faq-schema",),
                                      "town": (),
                                      "hub": ()},
          audit.RUBRIC_EXEMPTIONS)
    # 3.62: a town page is a ruled kind exempt from NOTHING. It has to carry
    # a real FAQ and earn its words, so both checks stay live on it.
    check("     the town kind is declared, and exempts nothing",
          "town" in audit.RUBRIC_EXEMPTIONS and audit.RUBRIC_EXEMPTIONS["town"] == (),
          audit.RUBRIC_EXEMPTIONS.get("town"))

    def run_kind(meta: str, body: str):
        html = PAGE.replace("</head>", meta + "</head>").format(body=body)
        audit.load = lambda _src, _h=html: _h
        passes, warns, fails, notes, kind = audit.audit("fabricated.html", coverage=None)
        return " ".join(passes), " ".join(warns), " ".join(fails), " ".join(notes), kind

    contact_meta = '<meta name="tri-county-page" content="contact">'
    short = '<p>Call <a href="tel:+12153225350">(215) 322-5350</a>.</p>'

    p, w, f, n, kind = run_kind(contact_meta, short)
    check("     a short contact page draws no thin-content warning",
          "Thin content" not in w, w)
    check("     and no FAQPage warning", "no FAQPage schema" not in w, w)
    check("     both exemptions are reported as notes, not silence",
          "not measured against 300" in n and "No FAQPage schema, not measured" in n, n)
    check("     it still reports as a page, not as a special kind", kind == "page", kind)

    p, w, f, n, kind = run_kind(contact_meta, short.replace(
        "</p>", "</p><p>Or call 215.709.9665 today.</p>"))
    check("     a contact page still fails on the CallRail number",
          "CallRail tracking number" in f, f)
    p, w, f, n, kind = run_kind(contact_meta, short + '<p><a href="mailto:info@tricountycollision.com">info@tricountycollision.com</a></p>')
    check("     and on the second email address", "info@tricountycollision.com" in f, f)
    p, w, f, n, kind = run_kind(contact_meta, short + f"<p>995 Jaymor Road, {CITY}</p>")
    check("     and on a wrong street spelling", "street address is spelled" in f, f)
    p, w, f, n, kind = run_kind(contact_meta, "<p>Email contact@tricountycollision.com.</p>")
    check("     and still warns on an untappable contact", "not linked" in w, w)
    html_no_h1 = PAGE.replace("<h1>Collision Repair</h1>", "").replace(
        "</head>", contact_meta + "</head>").format(body=short)
    audit.load = lambda _src, _h=html_no_h1: _h
    _p, _w, _f, _n, _k = audit.audit("fabricated.html", coverage=None)
    check("     and still fails with no H1", any("No H1" in x for x in _f), _f)

    p, w, f, n, kind = run_kind("", short)
    check("     an UNDECLARED short page still draws the thin-content warning",
          "Thin content" in w, w)
    check("     and the FAQPage warning", "no FAQPage schema" in w, w)
    p, w, f, n, kind = run_kind('<meta name="tri-county-page" content="contct">', short)
    check("     a misspelled kind gets no exemption", "Thin content" in w, w)
    p, w, f, n, kind = run_kind('<meta name="tri-county-page" content="utility">', short)
    check("     and neither does utility", "Thin content" in w and "no FAQPage schema" in w, w)

    # The hours, 3.54: the constants beside the NAP, every copy held to
    # them. Same shape as the address tests: the canonical form keeps
    # passing, every way of writing it differently fails, and words that
    # merely look like hours are left alone.
    print("20. The hours: one way to write them, and no Sunday")
    H = "<p>Monday to Friday, 8&nbsp;a.m. to 6&nbsp;p.m.<br>Saturday by appointment only</p>"
    p, w, f = run(H)
    check("     the canonical pair passes, no-break spaces and all",
          "Hours match the constants" in p and "hours are written" not in f, (p, f))
    for label, body in (
            ("the live contact page's own spelling", "<p>Hours: Monday - Friday 8 AM - 6 PM</p>"),
            ("an abbreviated range", "<p>Mon-Fri, 8 a.m. - 6 p.m.</p>"),
            ("the right days at the wrong time", "<p>Monday to Friday, 8 a.m. to 5 p.m.</p>"),
            ("Saturday capitalised the live site's way", "<p>Saturday By Appointment Only</p>"),
            ("a stray clock time beside the canonical pair", H + "<p>Call before 5 p.m.</p>"),
            ("a stray day beside the canonical pair", H + "<p>Closed Tuesday afternoons.</p>")):
        p, w, f = run(body)
        check(f"     caught: {label}", "hours are written a second way" in f, f)
    for body in ("<p>Sunday: Closed</p>", H + "<p>Open Sundays too.</p>"):
        p, w, f = run(body)
        check(f"     Sunday is a critical: {body[-26:]!r}", "Sunday is mentioned" in f, f)
    p, w, f = run("<p>Hundreds of hours of training. Sun damage fades paint. The door was left open.</p>")
    check("     words that only look like hours are left alone",
          "hours are written" not in f and "Sunday" not in f and "Hours match" not in p, (p, f))
    wrong_schema = ('<script type="application/ld+json">{"@type":"AutoBodyShop",'
                    '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification",'
                    '"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],'
                    '"opens":"08:00","closes":"17:00"}]}</script>')
    p, w, f = run(H + wrong_schema)
    check("     a schema that closes at 17:00 is a critical",
          "schema's hours disagree" in f, f)
    n, strays, sundays = audit.hours_findings(
        "- Hours: Monday to Friday, 8 a.m. to 6 p.m. Saturday by appointment only.")
    check("     the llms.txt phrasing is canonical", n == 2 and not strays and not sundays,
          (n, strays, sundays))
    n, strays, sundays = audit.hours_findings("- Hours: Mon-Fri 8-6, Sat by appt.")
    check("     and a shorthand llms.txt line is not", bool(strays), strays)
    _load = audit.load
    audit.load = lambda src: open(src, encoding="utf-8").read()
    try:
        # EVERY SHIPPED PAGE means pages. A redirect stub or the 404 page
        # declares a SPECIAL_KINDS kind and is scored on its own short
        # rubric, with no hours, geo or headings by design; the first stubs
        # landed in 3.62. Only a declared special kind is left out, so a
        # real page that forgot its markup is still swept.
        def _special(path):
            m = re.search(r'<meta name="tri-county-page" content="([^"]*)"',
                          open(path, encoding="utf-8").read())
            return bool(m) and m.group(1).strip().lower() in audit.SPECIAL_KINDS
        shipped = sorted(x for x in glob.glob(os.path.join(root, "docs", "*.html")) +
                         glob.glob(os.path.join(root, "docs", "*", "index.html"))
                         if not _special(x))
        bad = []
        for pg in shipped:
            sp, sw, sf, sn, sk = audit.audit(pg)
            if not any("Hours match the constants" in x for x in sp) or \
                    any("hours" in x.lower() or "Sunday" in x for x in sf):
                bad.append(pg)
    finally:
        audit.load = _load
    check(f"     every shipped page ({len(shipped)}) matches the constants", not bad, bad)

    print("21. An inline SVG's <title> is not the page's title")
    p, w, f = run('<svg role="img"><title>A map of the roads around the shop, drawn from OpenStreetMap data</title></svg>')
    check("     the page title is still measured as the head's alone",
          f"({len('Collision Repair in Southampton, PA | Tri-County Collision')} chars)" in p, p)

    # The blog's kinds, 3.57. A post is a read and an index routes, so each
    # is exempt from faq-schema and nothing else, and thin-content stays
    # live on both. Greg's condition: NOT REQUIRED, NEVER UNMEASURED. A post
    # that shows a visible FAQ is held to the mirror law like any page.
    print("23. The blog kinds: no FAQ required, and an FAQ is still measured")
    long_body = "<p>" + " ".join(["word"] * 320) + "</p>"
    faq_vis = ('<details><summary>Is it free?<span class="faq-ico"></span></summary>'
               '<p>Yes, estimates are free.</p></details>')

    def faq_schema(ans):
        return ('<script type="application/ld+json">{"@type":"FAQPage","mainEntity":[{'
                '"@type":"Question","name":"Is it free?","acceptedAnswer":{"@type":"Answer",'
                f'"text":"{ans}"}}}}]}}</script>')

    for k in ("post", "blog-index"):
        meta = f'<meta name="tri-county-page" content="{k}">'
        p, w, f, n, kind = run_kind(meta, long_body)
        check(f"     a {k} with no FAQ draws no FAQPage warning, and says so in a note",
              "no FAQPage schema" not in w and "not measured here" in n, (w, n))
        check(f"     a {k} still reports as a page", kind == "page", kind)
        p, w, f, n, kind = run_kind(meta, "<p>Too short to be a real post.</p>")
        check(f"     a thin {k} STILL warns: thin-content is live on this kind",
              "Thin content" in w, w)
        p, w, f, n, kind = run_kind(meta, long_body + faq_vis + faq_schema("No, it costs money."))
        check(f"     a {k} WITH a visible FAQ and a mismatched schema FAILS the mirror",
              "FAQ answer does not match its schema" in f, f)
        p, w, f, n, kind = run_kind(meta, long_body + faq_vis)
        check(f"     a {k} with a visible FAQ and NO schema is warned, not excused",
              "no FAQPage schema" in w and "not measured here" not in n, (w, n))
        p, w, f, n, kind = run_kind(meta, long_body + faq_vis + faq_schema("Yes, estimates are free."))
        check(f"     a {k} with a matching FAQ passes the mirror",
              "byte-identical" in p and "FAQ" not in f, (p, f))
    p, w, f, n, kind = run_kind('<meta name="tri-county-page" content="posts">', long_body)
    check("     a misspelled blog kind gets no exemption", "no FAQPage schema" in w, w)
    p, w, f, n, kind = run_kind(contact_meta, long_body + faq_vis + faq_schema("No."))
    check("     and contact, too, is held to the mirror when it shows an FAQ",
          "FAQ answer does not match its schema" in f, f)

    # The shop's coordinates, 3.56: GEO_LAT and GEO_LON, the verified pin.
    # Same shape as the address and hours tests: the right value passes,
    # the known-wrong one fails, and so does every other way to drift.
    print("22. The schema's geo is the verified pin, and only that")

    def biz(geo):
        g = "" if geo is None else f',"geo":{geo}'
        return ('<script type="application/ld+json">{"@context":"https://schema.org",'
                '"@graph":[{"@type":"AutoBodyShop","@id":"https://tricountycollision.com/#business"'
                f'{g}}}]}}</script>')

    def gc(lat, lon):
        return f'{{"@type":"GeoCoordinates","latitude":{lat},"longitude":{lon}}}'

    p, w, f = run(biz(gc(audit.GEO_LAT, audit.GEO_LON)))
    check("     the verified pin passes", "Schema geo is the verified pin" in p
          and "not the shop's verified pin" not in f, (p, f))
    for label, geo in (
            ("the old live-site value, a map URL's centre, 220m west", gc(40.1660232, -75.0538596)),
            ("latitude and longitude swapped", gc(audit.GEO_LON, audit.GEO_LAT)),
            ("one digit off in the seventh place", gc(audit.GEO_LAT, -75.0512848)),
            ("Nominatim's interpolated point", gc(40.1650509, -75.0494633)),
            ("coordinates that are not numbers", gc('"north"', '"west"'))):
        p, w, f = run(biz(geo))
        check(f"     caught: {label}", "not the shop's verified pin" in f, f)
    p, w, f = run(biz(None))
    check("     caught: a business node with no geo at all", "carries no `geo`" in f, f)
    p, w, f = run('<script type="application/ld+json">{"@type":"Place",'
                  f'"geo":{gc(40.0, -75.0)}}}</script>')
    check("     a geo on a node that is not the business is left alone",
          "verified pin" not in f and "verified pin" not in p, (p, f))
    _load = audit.load
    audit.load = lambda src: open(src, encoding="utf-8").read()
    try:
        bad = []
        for pg in shipped:
            sp, sw, sf, sn, sk = audit.audit(pg)
            if not any("Schema geo is the verified pin" in x for x in sp) or \
                    any("verified pin" in x for x in sf):
                bad.append(pg)
    finally:
        audit.load = _load
    check(f"     every shipped page ({len(shipped)}) carries the verified pin", not bad, bad)

    # And the page as it actually ships.
    _load = audit.load
    audit.load = lambda src: open(src, encoding="utf-8").read()
    try:
        cp, cw, cf, cn, ck = audit.audit(os.path.join(root, "docs", "contact-us", "index.html"))
    finally:
        audit.load = _load
    check("     /contact-us/ as it ships: no critical, and sameAs its only warning",
          not cf and len(cw) == 1 and "sameAs" in cw[0], (cf, cw))

    # Empty headings, 3.60. One shipped in 3.58, an <h2></h2> closing a
    # migrated post, and nothing could see it: it has no box to look at and
    # no words to read. Same shape as the address tests: the clean page
    # passes, every way of being empty fails, and headings whose words sit
    # inside other markup are left alone.
    print("24. Empty headings: a heading with no words is a critical")
    p, w, f = run("<h2>What happens next</h2><p>Words.</p>")
    check("     a page whose headings all carry words passes",
          "No empty headings: all 2 h1 to h6 carry words" in p and "Empty heading" not in f, (p, f))
    for label, body in (
            ("the shipped case, an empty h2 closing the prose", "<p>Words.</p><h2></h2>"),
            ("spaces and a line break", "<h3>  \n  </h3>"),
            ("a no-break space, which a reader hears as nothing", "<h2>&nbsp;</h2>"),
            ("an empty strong, WordPress's other leftover", "<h2><strong> </strong></h2>"),
            ("a comment and nothing else", "<h4><!-- a heading went here --></h4>"),
            ("an empty link", '<h2><a href="../contact-us/"></a></h2>'),
            ("the smallest heading", "<h6></h6>"),
            ("an empty second H1 beside the real one", "<h1></h1>")):
        p, w, f = run(body)
        check(f"     caught: {label}", "Empty heading:" in f, f)
    p, w, f = run("<h2></h2><p>Words.</p><h3> </h3>")
    check("     two empty headings are both named, with their tags",
          "<h2> on line" in f and "<h3> on line" in f, f)
    for label, body in (
            ("words inside a link", '<h2><a href="../contact-us/">Contact us</a></h2>'),
            ("words beside an empty icon span", '<h3><span class="faq-ico"></span>Is it free?</h3>'),
            ("a heading that is only a number", "<h3>01</h3>"),
            ("an empty heading inside a script string, which is not markup",
             '<script>var t = "<h2></h2>";</script>')):
        p, w, f = run(body)
        check(f"     left alone: {label}", "Empty heading" not in f, f)
    _load = audit.load
    audit.load = lambda src: open(src, encoding="utf-8").read()
    try:
        bad = []
        for pg in shipped:
            sp, sw, sf, sn, sk = audit.audit(pg)
            if not any("No empty headings" in x for x in sp) or any("Empty heading" in x for x in sf):
                bad.append(pg)
    finally:
        audit.load = _load
    check(f"     every shipped page ({len(shipped)}) has no empty heading", not bad, bad)

    # Town-page variance, 3.62: rule 7's gate for the areas tier. Built with
    # the first town page, so it compares nothing on the shipped site yet;
    # these fixtures are what prove it will stop the second from shipping as
    # a copy of the first. Each one is shaped so that one specific way of
    # breaking the measure turns it red (3.62 records the mutations).
    print("25. Town variance: no shared substantive H2, under 30% shared phrasing")
    # The ceiling is the doctrine's own number, pinned directly: the
    # fixtures below sit far over it (a copy measures 80 percent and more),
    # so without this line a ceiling loosened to 0.8 would pass them all.
    check("     the ceiling is the doctrine's: under 30 percent shared phrasing",
          audit.TOWN_SHARED_MAX == 0.30 and audit.TOWN_SHINGLE == 3,
          (audit.TOWN_SHARED_MAX, audit.TOWN_SHINGLE))

    def town(name, h2s, prose, pattern=""):
        secs = "".join(f"<section><h2>{h}</h2><p>{p}</p></section>" for h, p in zip(h2s, prose))
        return (f'<html><head><meta name="tri-county-page" content="town"></head><body>'
                f'<nav class="crumb"><ol><li>Home</li><li>{pattern}</li></ol></nav><main>'
                f'<section id="why-the-trip"><p>{pattern}</p></section>{secs}'
                f'<section id="start"><h2>We will get you back on the road.</h2><p>{pattern}</p></section>'
                f'<a class="svc-card" href="#"><p>{pattern}</p></a>'
                f'<section id="nearby"><h2>Nearby towns we serve</h2><p>{pattern}</p></section>'
                f'</main></body></html>')

    def vary(pages):
        return audit.town_variance_findings({k: (h, (k,)) for k, h in pages.items()})

    # Two genuinely different pages about the same shop.
    a_text = ("The quickest way in from here is the state road south past the reservoir, then "
              "east at the light where the old mill stood before the fire of the nineties.")
    b_text = ("Most people coming from this side of the county take the pike through the "
              "village center and turn at the diner, which saves the backup on the main road.")
    f = vary({"jamison": town("Jamison", ["Getting here from Jamison"], [a_text]),
              "warminster": town("Warminster", ["Getting here from Warminster"], [b_text])})
    check("     two genuinely different town pages pass both halves",
          not f["shared_h2"] and all(r < audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)

    # A copy with only the name swapped, and dense enough in place names
    # that it reads as different UNLESS the names are masked.
    def dense(n):
        return " ".join(f"{n} drivers call first. {n} cars come in. We fix {n} dents. "
                        f"{n} estimates are free. {n} roads lead here." for _ in range(3))
    f = vary({"jamison": town("Jamison", ["For drivers from Jamison"], [dense("Jamison")]),
              "warminster": town("Warminster", ["For drivers from Warminster"], [dense("Warminster")])})
    over = [r for _a, _b, r in f["pairs"] if r >= audit.TOWN_SHARED_MAX]
    check("     caught: a copy with the town's name swapped, names masked", bool(over), f)
    check("     and its H2s, which differ only by name, are not the H2 half's to catch",
          not f["shared_h2"], f["shared_h2"])

    # A short page wholly inside a long one: containment catches it, and
    # Jaccard would let the long page's extra text dilute it away.
    long_extra = " ".join(f"Paragraph {i} is about something else entirely, word {i} of many."
                          for i in range(60))
    f = vary({"jamison": town("Jamison", ["From Jamison"], [a_text]),
              "hatboro": town("Hatboro", ["From Hatboro"], [a_text + " " + long_extra])})
    check("     caught: a short page contained in a long one",
          any(r >= audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)

    # The same substantive H2 on two pages, with different prose under it.
    f = vary({"jamison": town("Jamison", ["Getting to the shop"], [a_text]),
              "warminster": town("Warminster", ["Getting to the shop"], [b_text])})
    check("     caught: a shared substantive H2, even with different prose",
          [h for _a, _b, h in f["shared_h2"]] == ["getting to the shop"], f["shared_h2"])

    # Everything shared lives in pattern text: the crumb, the trust band,
    # the promise band, the service cards, the nearby links.
    shared = " ".join(["Lifetime warranty on all repair work, reviews on Google, twelve brands."] * 12)
    f = vary({"jamison": town("Jamison", ["Getting here from Jamison"], [a_text], shared),
              "warminster": town("Warminster", ["Getting here from Warminster"], [b_text], shared)})
    check("     left alone: identical pattern text, and the pattern H2s it carries",
          not f["shared_h2"] and all(r < audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)

    # The Real Repairs pairs, 3.63: byte-identical on every town page by
    # design, pattern text by the #real-repairs id. They carry their own
    # "Real Repairs" H2, so only their id keeps it from the H2 half.
    # 3.67: THE CHIP ROW AND THE STAT BAND LEFT THE TOWN TEMPLATE, and their
    # entries left the lists with them, so a chip row or a #proof band on
    # two town pages is now COUNTED, like any other shared text.
    chips = ('<ul class="badges"><li>Free estimates</li><li>Insurance paperwork handled</li>'
             '<li>ASE and I-CAR Gold Class certified</li><li>Detailed after every repair</li></ul>')
    pairs = ('<section id="real-repairs"><h2>Real Repairs</h2><p>Restored to pre-accident condition</p>'
             + "".join(f'<figure class="ba"><figcaption><strong>{car}</strong> {dmg}</figcaption></figure>'
                       for car, dmg in (("Dodge Grand Caravan", "Front-end collision"),
                                        ("Mercedes CLE 300", "Rear-end collision"),
                                        ("Nissan Murano", "Door dents"))) * 6 + '</section>')

    def town_363(name, h2, prose, extra=""):
        return town(name, [h2], [prose]).replace(
            "<main>", f'<main><section id="town-head"><h1>For {name}</h1>{extra}</section>').replace(
            '<section id="nearby">', pairs + '<section id="nearby">')

    f = vary({"jamison": town_363("Jamison", "Getting here from Jamison", a_text),
              "warminster": town_363("Warminster", "Getting here from Warminster", b_text)})
    check("     left alone: identical pairs on two town pages",
          not f["shared_h2"] and all(r < audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)
    f = vary({"jamison": town_363("Jamison", "Getting here from Jamison", a_text),
              "warminster": town_363("Warminster", "Getting here from Warminster", a_text)})
    check("     caught: shared prose OUTSIDE the pairs still reads as a copy",
          any(r >= audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)
    f = vary({"jamison": town_363("Jamison", "Getting here from Jamison", a_text, chips * 4),
              "warminster": town_363("Warminster", "Getting here from Warminster", b_text, chips * 4)})
    check("     3.67: an identical chip row on two town pages is COUNTED, no longer pattern",
          any(r >= audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)
    # The service cards, pattern by class since 3.62, isolated only in 3.67:
    # until then a mutant dropping "svc-card" from the list turned nothing
    # red, because no fixture shared text in the cards alone.
    cards = "".join(f'<a class="svc-card" href="#"><h3>{t}</h3><p>{d}</p></a>' for t, d in (
        ("Collision Repair", "Minor and major collision damage, with a lifetime warranty on the work."),
        ("Commercial Collision Repair", "Work vehicles and fleets, with help on the insurance side."),
        ("Auto Glass Repair", "Windshields, side windows and rear windows."),
        ("Paintless Dent Repair", "Door dings and hail dents, fixed without repainting."))) * 3
    f = vary({"jamison": town_363("Jamison", "Getting here from Jamison", a_text).replace("</main>", cards + "</main>"),
              "warminster": town_363("Warminster", "Getting here from Warminster", b_text).replace("</main>", cards + "</main>")})
    check("     left alone: identical service cards on two town pages",
          all(r < audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)
    proof = ('<section id="proof"><p>' + " ".join(["Lifetime warranty on all repair work, 274 Google "
             "reviews, twelve vehicle brands factory-certified."] * 6) + '</p></section>')
    f = vary({"jamison": town_363("Jamison", "Getting here from Jamison", a_text, proof),
              "warminster": town_363("Warminster", "Getting here from Warminster", b_text, proof)})
    check("     3.67: an identical #proof band on two town pages is COUNTED, no longer pattern",
          any(r >= audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)

    # The case for the trip, 3.64: byte-identical on every town page by
    # design, by the #why-the-trip id. It carries its own H2, so only the id
    # keeps it from the H2 half as well as from the phrase measure.
    band = ('<section id="why-the-trip"><h2>Why drivers pass closer shops</h2>'
            + "<p>A collision repair is two drives: one to drop the car off, one to pick it up. "
              "Everything between them is on us: the estimate, the insurance paperwork, and a "
              "repair done to your manufacturer's own procedures.</p>" * 4 + '</section>')

    def town_364(name, h2, prose):
        return town(name, [h2], [prose]).replace('<section id="start">', band + '<section id="start">')

    f = vary({"jamison": town_364("Jamison", "Getting here from Jamison", a_text),
              "warminster": town_364("Warminster", "Getting here from Warminster", b_text)})
    check("     left alone: an identical case-for-the-trip band on two town pages",
          not f["shared_h2"] and all(r < audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)
    f = vary({"jamison": town_364("Jamison", "Getting here from Jamison", a_text),
              "warminster": town_364("Warminster", "Getting here from Warminster", a_text)})
    check("     caught: shared prose OUTSIDE the band still reads as a copy",
          any(r >= audit.TOWN_SHARED_MAX for _a, _b, r in f["pairs"]), f)

    # An empty H2 on both pages is the empty-heading check's critical.
    f = vary({"jamison": town("Jamison", ["", "From Jamison"], ["", a_text]),
              "warminster": town("Warminster", ["", "From Warminster"], ["", b_text])})
    check("     left alone: an empty H2 on both is not a shared heading", not f["shared_h2"], f)

    # The gate reads the tree: one town and no hub compares nothing, and the
    # hub, when it lands, is compared like a sibling.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        def put(rel, htm):
            os.makedirs(os.path.join(tmp, os.path.dirname(rel)), exist_ok=True)
            open(os.path.join(tmp, rel), "w", encoding="utf-8").write(htm)
        put("areas-served-collision-repair-jamison-pa/index.html",
            town("Jamison", ["For drivers from Jamison"], [dense("Jamison")]))
        tp, tw, tf, tn = [], [], [], []
        audit.check_town_variance_local(tp, tw, tf, tn, root=tmp)
        check("     one town and no hub: nothing to compare, and a note that says so",
              not tf and not tp and any("nothing to compare" in n for n in tn), (tf, tn))
        put("areas-served/index.html",
            town("Hub", ["Every town we serve"], [dense("Jamison")]).replace(
                '<meta name="tri-county-page" content="town">', ""))
        tp, tw, tf, tn = [], [], [], []
        audit.check_town_variance_local(tp, tw, tf, tn, root=tmp)
        check("     caught: a town page that copies its hub, as a critical",
              any("read as copies" in x and "areas-served" in x for x in tf), tf)
        put("areas-served-collision-repair-warminster-pa/index.html",
            town("Warminster", ["For drivers from Jamison"], [b_text]))
        tp, tw, tf, tn = [], [], [], []
        audit.check_town_variance_local(tp, tw, tf, tn, root=tmp)
        check("     caught: a sibling reusing another town's substantive H2, as a critical",
              any("share a substantive H2" in x for x in tf), tf)

    tp, tw, tf, tn = [], [], [], []
    audit.check_town_variance_local(tp, tw, tf, tn)
    check("     the shipped site raises no variance critical", not tf, tf)

    # One routing, every rendering derived, 3.65: Greg's accuracy mandate.
    # Every fixture is the SHIPPED Jamison page with exactly one thing made
    # wrong, so what passes is the real page and what fails differs from it
    # by one fact.
    print("26. One routing: the directions and every drive figure derive from it")
    jam_path = os.path.join(root, "docs", "areas-served-collision-repair-jamison-pa", "index.html")
    jam = open(jam_path, encoding="utf-8").read()
    route = audit.TOWN_ROUTES["jamison-pa"]
    llms = audit.llms_entry_for("https://tricountycollision.com/areas-served-collision-repair-jamison-pa/",
                                os.path.join(root, "docs"))
    got = audit.town_route_findings(jam, route, llms)
    check("     the shipped Jamison page derives from its recorded routing", not got, got)
    check("     and its llms.txt entry was found and read", "15 minutes" in llms, llms)

    def one(old, new, count=1):
        assert jam.count(old) == count, (old, jam.count(old))
        return jam.replace(old, new)

    steps = re.findall(r"(?s)<li><strong>.*?</li>", jam)
    for label, page, llms_x in (
            ("a wrong turn word, step 2 left made right",
             one("<strong>Turn left onto West Bristol Road</strong>", "<strong>Turn right onto West Bristol Road</strong>"), llms),
            ("a wrong compass word, step 1 south made north",
             one("<strong>Head south on York Road (PA&nbsp;263)</strong>", "<strong>Head north on York Road (PA&nbsp;263)</strong>"), llms),
            ("two steps in the wrong order", jam.replace(steps[1], "@@").replace(steps[2], steps[1]).replace("@@", steps[2]), llms),
            ("a step dropped", jam.replace(steps[3], ""), llms),
            ("a wrong route number, behind the nbsp (3.76)", one("(PA&nbsp;263)</strong>", "(PA&nbsp;611)</strong>"), llms),
            ("a stale step distance, 4 miles made 5, behind the nbsp (3.76)", one("follow it for about 4&nbsp;miles", "follow it for about 5&nbsp;miles"), llms),
            ("a stale quarter mile made half a mile", one("about a quarter mile along", "about half a mile along"), llms),
            # These two isolate their checks: nothing else about the step is
            # wrong, and the figure is valid ELSEWHERE on this route.
            ("the wrong road on a step, turn and distance untouched",
             one("<strong>Turn left onto West Bristol Road</strong>", "<strong>Turn left onto Street Road</strong>"), llms),
            ("another step's distance on step 2, 4 miles made 2",
             one("follow it for about 4&nbsp;miles", "follow it for about 2&nbsp;miles"), llms),
            ("a stale minute count in the lead",
             one("about 15 minutes from Jamison. Factory-certified", "about 20 minutes from Jamison. Factory-certified"), llms),
            ("a stale minute count in the chip", one("~15 min from Jamison", "~18 min from Jamison"), llms),
            ("a stale total distance, 8.4 made 9.1",
             jam.replace("about 8.4 miles", "about 9.1 miles"), llms),
            ("a stale meta description",
             re.sub(r'(<meta name="description" content="[^"]*?)about 15 minutes', r"\1about 12 minutes", jam), llms),
            ("a stale figure in the map's alt text",
             jam.replace('aria-label="Map of the drive from Jamison,', 'aria-label="A 25 minutes drive map from Jamison,'), llms),
            ("a stale llms.txt entry", jam, llms.replace("15 minutes", "25 minutes"))):
        f = audit.town_route_findings(page, route, llms_x)
        check(f"     caught: {label}", bool(f) and page != jam or llms_x != llms and bool(f), f)
    p, w, f, n, kind = run_kind('<meta name="tri-county-page" content="town">',
                                "<p>We are about 15 minutes away.</p>")
    check("     caught: a town page printing a drive time with no recorded routing behind it",
          "no recorded routing behind them" in f, f)
    p, w, f, n, kind = run_kind('<meta name="tri-county-page" content="post">',
                                "<p>We are about 15 minutes away.</p>")
    check("     left alone: a page that is not a town page is not held to a routing",
          "recorded routing" not in f, f)

    # The contact embed, 3.65: the verified pin, by coordinates, never a
    # name (a name query brings the Business Profile's card with it).
    good = (f'<iframe src="https://www.google.com/maps?q={audit.GEO_LAT},{audit.GEO_LON}&amp;z=15&amp;output=embed"'
            ' title="Map" loading="lazy"></iframe>')
    p, w, f = run(good)
    check("     the embed centred on the verified pin passes", "centred on the verified pin" in p and
          "embed is wrong" not in f, (p, f))
    for label, frag in (
            ("an embed queried by the business's NAME",
             good.replace(f"q={audit.GEO_LAT},{audit.GEO_LON}", "q=Tri-County+Collision,+995+Jaymor+Rd")),
            ("an embed one digit off the pin", good.replace(str(audit.GEO_LON), "-75.0512848")),
            ("an embed with no title", good.replace(' title="Map"', "")),
            ("an embed that loads eagerly", good.replace(' loading="lazy"', ""))):
        p, w, f = run(frag)
        check(f"     caught: {label}", "embed is wrong" in f, f)

    # THE CRUMB MIRROR, 3.76, closing 3.60's open item 1: the visible
    # breadcrumb and the BreadcrumbList agree in labels and order, both
    # directions. Severity from the FAQ mirror: drift is a critical, a
    # crumb with no schema a warning, schema with no readable crumb a note.
    print("27. The crumb mirror: the visible breadcrumb is the BreadcrumbList")

    def crumb(*labels, pending=None):
        items = []
        for i, x in enumerate(labels):
            if i == 0:
                items.append(f'<li><a href="../">{x}</a></li>')
            elif pending == i:
                items.append(f'<li><span data-pending-href="../hub/">{x}</span></li>')
            else:
                items.append(f"<li>{x}</li>")
        return '<nav class="crumb" aria-label="Breadcrumb"><ol>' + "".join(items) + "</ol></nav>"

    def crumb_schema(*labels, order=None, nested=False):
        els = []
        for i, x in enumerate(labels, 1):
            els.append({"@type": "ListItem", "position": i,
                        "item": {"@id": f"https://tricountycollision.com/{i}/", "name": x}}
                       if nested else {"@type": "ListItem", "position": i, "name": x})
        if order:
            els = [els[k] for k in order]
        return ('<script type="application/ld+json">'
                + json.dumps({"@context": "https://schema.org",
                              "@graph": [{"@type": "BreadcrumbList", "itemListElement": els}]})
                + "</script>")

    three = ("Home", "Areas We Serve", "Jamison")
    p, w, f, n, kind = run_kind("", crumb(*three, pending=1) + crumb_schema(*three))
    check("     a crumb that mirrors its schema passes, a pending span item included",
          "breadcrumb and the BreadcrumbList agree, 3 items" in p and "Breadcrumb" not in f, (p, f))
    p, w, f, n, kind = run_kind("", crumb(*three) + crumb_schema(*three, order=(2, 0, 1)))
    check("     the schema is read by position, not by array order",
          "BreadcrumbList agree" in p and "Breadcrumb" not in f, (p, f))
    p, w, f, n, kind = run_kind("", crumb(*three) + crumb_schema(*three, nested=True))
    check("     a name carried on the item node is read too",
          "BreadcrumbList agree" in p, p)
    curly = ("Home", "Blog", "“Collision Repair Near Me”? Choosing a Southampton Body Shop")
    p, w, f, n, kind = run_kind("", crumb(*curly) + crumb_schema(*curly))
    check("     a post's long curly-quoted title mirrors byte for byte",
          "BreadcrumbList agree" in p, p)
    for label, page, schema, want in (
            ("a label edited on the page only", ("Home", "Areas We Serve", "Jamison, PA"), three,
             "label differs"),
            ("a label edited in the schema only", three, ("Home", "Service Areas", "Jamison"),
             "label differs"),
            ("an item on the page, missing from the schema", three, ("Home", "Jamison"),
             "on the page but not in the BreadcrumbList"),
            ("an item in the schema, missing from the page", ("Home", "Jamison"), three,
             "in the BreadcrumbList but not on the page"),
            ("the same items in a different order", ("Home", "Jamison", "Areas We Serve"), three,
             "order differs")):
        p, w, f, n, kind = run_kind("", crumb(*page) + crumb_schema(*schema))
        check(f"     caught as a critical: {label}", want in f and "BreadcrumbList agree" not in p, (p, f))
    p, w, f, n, kind = run_kind("", crumb(*three))
    check("     a visible crumb with no BreadcrumbList is a warning, not a critical",
          "visible breadcrumb with no BreadcrumbList" in w and "Breadcrumb" not in f, (w, f))
    p, w, f, n, kind = run_kind("", crumb_schema(*three))
    check("     a BreadcrumbList with no readable crumb is a note, never scored",
          "no visible breadcrumb this check can read" in n and "readcrumb" not in f + w, (n, f, w))
    p, w, f, n, kind = run_kind("", '<nav class="crumb"><a href="../">Home</a> / Jamison</nav>'
                                + crumb_schema(*three))
    check("     a crumb nav with no list items reads as unreadable, not as a mismatch",
          "no visible breadcrumb this check can read" in n and "readcrumb" not in f, (n, f))
    p, w, f, n, kind = run_kind("", "<p>No trail here.</p>")
    check("     a page with neither says nothing about breadcrumbs",
          "readcrumb" not in p + w + f + n, (p, w, f, n))
    for page in ("areas-served-collision-repair-jamison-pa", "contact-us",
                 "collision-repair-near-me-in-southampton-how-to-choose-the-right-auto-body-shop"):
        src = os.path.join(root, "docs", page, "index.html")
        audit.load = lambda _s, _h=open(src, encoding="utf-8").read(): _h
        ps, ws, fs, ns, kd = audit.audit(src, coverage=None)
        check(f"     the shipped {page[:40]} crumb mirrors its schema",
              any("BreadcrumbList agree" in x for x in ps) and not any("readcrumb" in x for x in fs),
              [x for x in fs if "readcrumb" in x])

    # THE SHORT-STEP RULE AND THE PER-TOWN RADIUS, 3.78. A step under an
    # eighth of a mile is written in feet, to the nearest hundred, never
    # "0.0 miles"; every rounding is half-up. And every TOWN_ROUTES entry
    # is held to its own corner radius, a widened radius only with a reason.
    print("28. Short steps derive feet; every town's corner holds its own radius")
    for mi, want in ((0.04, "200 feet"), (0.08, "400 feet"), (0.06, "300 feet"), (0.07, "400 feet"),
                     (0.005, "100 feet"), (0.1249, "700 feet"), (0.125, "a quarter mile"),
                     (0.28, "a quarter mile"), (0.375, "half a mile"), (0.5, "1 mile"),
                     (1.92, "2 miles"), (2.5, "3 miles"), (3.5, "4 miles")):
        got = audit.step_miles_phrase(mi)
        check(f"     {mi} mi derives \u201c{want}\u201d", got == want, got)
    sweep = [audit.step_miles_phrase(k / 1000) for k in range(1, 10001)]
    check("     no distance from 0.001 to 10 mi ever derives zero",
          not any(x.startswith(("0 ", "0.0")) or x == "0 feet" for x in sweep),
          [x for x in sweep if x.startswith(("0 ", "0.0"))][:3])
    route = {"miles": 2.2, "minutes": 5.2, "roads_driven": ("Main Road", "Jaymor Road"),
             "steps": (("Main Road", "", "", 90, 2.1), ("Jaymor Road", "", "right", 146, 0.06))}

    def short_page(last, extra=""):
        return ('<main><section id="getting-here"><p>About 5 minutes.' + extra + '</p><ol class="numbered">'
                '<li><strong>Head east on Main Road</strong> for about 2&nbsp;miles.</li>'
                f'<li><strong>Turn right onto Jaymor Rd</strong>, and the shop is {last}.</li>'
                "</ol></section></main>")
    got = audit.town_route_findings(short_page("about 300&nbsp;feet along"), route)
    check("     a 0.06 mi last step written \u201cabout 300 feet\u201d passes", not got, got)
    for label, page in (("the wrong hundred, 400 feet for 0.06 mi", short_page("about 400&nbsp;feet along")),
                        ("the old wrong rendering, 0.0 miles", short_page("about 0.0 miles along")),
                        ("a quarter mile for a 0.06 mi step", short_page("about a quarter mile along")),
                        ("an underived feet figure in the prose", short_page("about 300&nbsp;feet along",
                                                                           " The lot is 600 feet deep."))):
        got = audit.town_route_findings(page, route)
        check(f"     caught: {label}", bool(got), got)
    ne = dict(route, minutes=audit.TOWN_ROUTES["northeast-philadelphia"]["minutes"])
    check("     Northeast Philadelphia's recorded 8.5 minutes reads \u201cabout 9 minutes\u201d, half-up",
          ne["minutes"] == 8.5 and not audit.town_route_findings(short_page("about 300&nbsp;feet along")
                                                                  .replace("About 5 minutes", "About 9 minutes"), ne), None)
    got = audit.town_route_findings(short_page("about 300&nbsp;feet along").replace("About 5 minutes", "About 8 minutes"), ne)
    check("     caught: \u201cabout 8 minutes\u201d for 8.5, the banker's rounding", bool(got), got)
    got = audit.town_route_config_findings()
    check("     every recorded town's corner lies inside its own radius", not got, got)
    check("     Bensalem, Horsham and Huntingdon Valley carry their widened radii with reasons",
          all(audit.TOWN_ROUTES[k]["max_m"] > 60 and audit.TOWN_ROUTES[k].get("max_m_why")
              for k in ("bensalem-pa", "horsham-pa", "huntingdon-valley-pa")), None)
    base = dict(audit.TOWN_ROUTES["bensalem-pa"])
    for label, mut in (("a corner outside its radius (Bensalem held to 60)", dict(base, max_m=60)),
                       ("a widened radius with no reason", {k: v for k, v in dict(base, max_m=70).items()
                                                            if k != "max_m_why"}),
                       ("a corner moved 200m off its place", dict(base, corner=base["corner"][:3]
                                                                   + (base["corner"][3] + 0.0018, base["corner"][4]))),
                       ("an entry with no place recorded", {k: v for k, v in base.items() if k != "place"})):
        got = audit.town_route_config_findings({"x-pa": mut})
        check(f"     caught: {label}", bool(got), got)

    # THE SERVED LIST, 3.79: one list, AREA_SERVED, written into every
    # business node by scripts/sync-area-served.py and checked on every page.
    print("29. The served list: every business node carries AREA_SERVED")
    import importlib.util
    spec = importlib.util.spec_from_file_location("sync_area_served", os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync-area-served.py"))
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)

    def biz_page(area, extra_nodes=()):
        g = {"@context": "https://schema.org", "@graph": [
            {"@type": "AutoBodyShop", "@id": "https://tricountycollision.com/#business",
             "name": "Tri-County Collision", "areaServed": area}] + list(extra_nodes)}
        return ('<script type="application/ld+json">\n' + "\n".join("  " + x for x in json.dumps(g, indent=2, ensure_ascii=False).splitlines())
                + "\n  </script>")
    want = audit.area_served_nodes()
    check("     AREA_SERVED names Jamison, closing the 3.62 open item",
          any(x[1] == "Jamison, Pennsylvania" for x in audit.AREA_SERVED), None)
    p, w, f, n, kind = run_kind("", biz_page(want))
    check("     a business node carrying the list passes", "one served list" in p and "served list" not in f, (p, f))
    no_jamison = [x for x in want if x["name"] != "Jamison, Pennsylvania"]
    for label, area in (("the list without Jamison, the 3.62 defect", no_jamison),
                        ("the list in another order", list(reversed(want))),
                        ("a place the hub does not serve", want + [{"@type": "City", "name": "Newtown, Pennsylvania"}]),
                        ("a place with its county dropped", [dict(x, containedInPlace=None) if x["name"].startswith("Hatboro") else x for x in want])):
        p, w, f, n, kind = run_kind("", biz_page(area))
        check(f"     caught as a critical: {label}", "is not the served list" in f, f)
    town_service = {"@type": "Service", "name": "Collision Repair for Jamison, PA",
                    "areaServed": [{"@type": "City", "name": "Jamison, Pennsylvania"}]}
    out = sync.synced(biz_page(no_jamison, [town_service]))
    got = json.loads(re.search(r'(?s)<script type="application/ld\+json">(.*?)</script>', out).group(1))["@graph"]
    check("     the sync writes the list into the business node", got[0]["areaServed"] == want, got[0]["areaServed"])
    check("     and leaves a Service node's own areaServed alone", got[1]["areaServed"] == town_service["areaServed"], got[1])
    check("     a synced page is a fixed point: syncing again changes nothing", sync.synced(out) == out, None)
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync-area-served.py"), "--check"],
                       capture_output=True, text=True)
    check("     every shipped page is in sync (sync-area-served.py --check exits 0)", r.returncode == 0, r.stdout[-300:])

    # THE HUB IS HELD TO THE ROUTINGS, 3.79 (protocol f).
    print("30. The hub: every town figure and road derives from its routing")

    def hub(*blocks, outside=""):
        return ("<main>" + "".join(f'<article data-town="{k}"><h3>Town</h3><p>{t}</p></article>' for k, t in blocks)
                + f"<p>{outside}</p></main>")
    good = hub(("richboro-pa", "About 8 minutes from 2nd Street Pike and Almshouse Road, straight down Second Street Pike (PA 232)."),
               ("hatboro-pa", "About 8 minutes from York Road and Byberry Road, by Byberry Road, Davisville Road and County Line Road."),
               ("bensalem-pa", "About 15 minutes from Knights Road and Street Road, then Second Street Pike (PA 232)."))
    got = audit.hub_route_findings(good)
    check("     derived figures, corner roads, County Line Road and Second-for-2nd all pass", not got, got)
    for label, page in (
            ("a stale minute count", good.replace("About 8 minutes from 2nd", "About 10 minutes from 2nd")),
            ("a stale figure written in words", good.replace("About 8 minutes from 2nd", "About ten minutes from 2nd")),
            ("the live page's range, in words", good.replace("About 8 minutes from 2nd", "Ten to fifteen minutes from 2nd")),
            ("a range whose upper end is derived", good.replace("About 8 minutes from 2nd", "About 6 to 8 minutes from 2nd")),
            ("a mileage the routing does not derive", good.replace("About 8 minutes from 2nd", "About 6 miles and 8 minutes from 2nd")),
            ("a bearing", good.replace("straight down", "northeast down")),
            ("a hyphenated bearing", good.replace("straight down", "west-southwest, down")),
            ("a road the route does not drive", good.replace("Almshouse Road", "Buck Road")),
            ("a route number the steps do not drive", good.replace("(PA 232).</p></article><article data-town=\"hatboro", "(PA 263).</p></article><article data-town=\"hatboro")),
            ("a step phrase on the hub", good.replace("straight down", "a quarter mile, then down")),
            ("a drive figure outside every town block", hub(("richboro-pa", "About 8 minutes."), outside="Most towns are about 10 minutes out.")),
            ("a figure for a town with no routing", hub(("nowhere-pa", "About 8 minutes out.")))):
        got = audit.hub_route_findings(page)
        check(f"     caught: {label}", bool(got), got)
    check("     four miles in words is read as Richboro's road-derived 4, and passes",
          not audit.hub_route_findings(good.replace("About 8 minutes from 2nd", "About four miles and 8 minutes from 2nd")), None)
    check("     \u201chalf a mile\u201d and \u201ca quarter mile\u201d stay step phrases, never \u201c1 mile\u201d",
          [k for k, _v, _s in audit.route_quantities("half a mile, then a quarter mile")] == ["step", "step"], None)
    check("     a capitalised compass word is a name, not a bearing",
          not audit.hub_route_findings(hub(("northeast-philadelphia", "The Northeast is closer than most people assume."))), None)
    shipped = open(os.path.join(root, "docs", "areas-served", "index.html"), encoding="utf-8").read()
    got = audit.hub_route_findings(shipped)
    check("     the shipped hub derives every figure and road from its routings", not got, got)
    check("     and carries a block for every routed town", all(f'data-town="{k}"' in shipped for k in audit.TOWN_ROUTES), None)
    p, w, f, n, kind = run_kind('<meta name="tri-county-page" content="hub">', hub(("richboro-pa", "About 12 minutes.")))
    check("     a page declared as the hub is checked, and fails on a stale figure", "does not derive" in f, f)
    p, w, f, n, kind = run_kind("", hub(("richboro-pa", "About 12 minutes.")))
    check("     an undeclared page is not read as the hub", "does not derive" not in f, f)

    # BATCH 1, 3.81: the variance gate under Greg's option C, proved in both
    # directions on the shipped pages; the empty-map check; the town
    # script's title rule and derived nearby order.
    print("31. The town tier: option C's gate both ways, an undrawn map, the town script's rules")
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("build_town", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-town.py"))
    bt = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(bt)
    tier = {os.path.basename(os.path.dirname(f)): f for f in glob.glob(os.path.join(root, "docs", "areas-served*", "index.html"))}

    def pair(a_html, b_html, a_key, b_key):
        r = audit.town_variance_findings({"a": (a_html, audit.own_town_names(tier[a_key])),
                                          "b": (b_html, audit.own_town_names(tier[b_key]))})
        return r["pairs"][0][2], r["shared_h2"]
    ben_k, ric_k = "areas-served-collision-repair-bensalem-pa", "areas-served-collision-repair-richboro-pa"
    ben, ric = open(tier[ben_k]).read(), open(tier[ric_k]).read()
    base, _h = pair(ben, ric, ben_k, ric_k)
    allpairs = audit.town_variance_findings({k: (open(f).read(), audit.own_town_names(f)) for k, f in tier.items()})
    worst = max(x[2] for x in allpairs["pairs"])
    check("     the shipped tier clears the gate: every pair under 30%, no shared H2",
          worst < audit.TOWN_SHARED_MAX and not allpairs["shared_h2"], (worst, allpairs["shared_h2"]))
    ben_open = re.search(r'(?s)<section id="for-bensalem">.*?<div class="prose"[^>]*>(.*?)</div>', ben).group(1)
    ric_open = re.search(r'(?s)(<section id="for-richboro">.*?<div class="prose"[^>]*>)(.*?)(</div>)', ric)
    copied = ric.replace(ric_open.group(0), ric_open.group(1) + ben_open + ric_open.group(3))
    v, _h = pair(ben, copied, ben_k, ric_k)
    check("     caught: Bensalem's opening copied into Richboro's page fails the gate",
          v >= audit.TOWN_SHARED_MAX, (base, v))
    ben_ans = re.findall(r"(?s)<details>.*?<p>(.*?)</p>", ben)[3]
    ric_ans = re.findall(r"(?s)<details>.*?<p>(.*?)</p>", ric)
    copied2 = ric
    for x in ric_ans[2:4]:
        copied2 = copied2.replace(f"<p>{x}</p>", f"<p>{ben_ans}</p>", 1)
    v2, _h = pair(ben, copied2, ben_k, ric_k)
    check("     caught: Bensalem FAQ answers copied into Richboro's page fail the gate",
          v2 >= audit.TOWN_SHARED_MAX, (base, v2))
    ben_steps = re.search(r'(?s)<ol class="numbered">.*?</ol>', ben).group(0)
    ric_steps = re.search(r'(?s)<ol class="numbered">.*?</ol>', ric).group(0)
    v3, _h = pair(ben, ric.replace(ric_steps, ben_steps), ben_k, ric_k)
    check("     the derived steps do not count: Bensalem's steps in Richboro's card leave the pair unchanged",
          abs(v3 - base) < 1e-9, (base, v3))
    intro_ben = re.search(r'(?s)<div class="dir-body">\s*<div class="prose">\s*(<p>.*?</p>)', ben).group(1)
    intro_ric = re.search(r'(?s)<div class="dir-body">\s*<div class="prose">\s*(<p>.*?</p>)', ric).group(1)
    v4, _h = pair(ben, ric.replace(intro_ric, intro_ben), ben_k, ric_k)
    check("     the card's intro line does not count either", abs(v4 - base) < 1e-9, (base, v4))
    jam = open(tier["areas-served-collision-repair-jamison-pa"]).read()
    tt = audit._TownText()
    tt.feed(jam)
    words = " ".join(" ".join(tt.words).split())
    check("     Jamison's alternative-route paragraph is prose and still counts",
          "Staying on York Road" in words and "From the crossroads" not in words and "Head south on York" not in words, None)
    town_meta = '<meta name="tri-county-page" content="town">'
    for label, frag, want in (
            ("a town page whose MAP markers are empty", "<!-- MAP:BEGIN, written by x --><!-- MAP:END -->", "map is empty"),
            ("a town page with no MAP markers at all", "<p>No map.</p>", "no MAP markers")):
        p, w, f, n, kind = run_kind(town_meta, frag)
        check(f"     caught as a critical: {label}", want in f, f)
    p, w, f, n, kind = run_kind(town_meta, '<!-- MAP:BEGIN, x --><svg viewBox="0 0 1 1" role="img" aria-label="Map"></svg><!-- MAP:END -->')
    check("     a drawn map passes", "map is drawn" in p and "map is empty" not in f, (p, f))
    for name in bt.TOWN_NAMES.values():
        t = bt.title_for(name)
        full = f"Collision Repair for {name}, PA | Tri-County Collision"
        check(f"     the title for {name} is {len(t)} characters, and the short brand only where needed",
              len(t) <= 60 and (t == full if len(full) <= 60 else t.endswith("| Tri-County")), t)
    check("     Jamison's nearby order derives: Warminster, Richboro, Hatboro, Horsham",
          bt.nearest("jamison-pa") == ["warminster-pa", "richboro-pa", "hatboro-pa", "horsham-pa"], bt.nearest("jamison-pa"))
    check("     build-town.py carries no Jamison nearby exception",
          "nearby" not in bt.CONTENT["jamison-pa"], None)

    # BATCHES 2 AND 3, 3.82: crumbs never wrap, site-wide, on Greg's
    # ruling. Under flex-wrap the last crumb took a line of its own before
    # it could shrink, and on Northeast Philadelphia that line pushed Call
    # under the call bar at 360. The fold is only ever measured by a
    # render, so the rule that protects it is held here, in the stylesheet.
    print("32. Crumbs never wrap: every crumb but the last holds, the last one shrinks")
    css = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "docs", "assets", "site.css"), encoding="utf-8").read()
    css = re.sub(r"(?s)/\*.*?\*/", "", css)
    rules = re.findall(r"([^{}]+)\{([^{}]*)\}", css)

    def decl(selector):
        return " ".join(body for sel, body in rules if selector in [s.strip() for s in sel.split(",")])
    check("     .crumb ol declares flex-wrap: nowrap", re.search(r"flex-wrap:\s*nowrap", decl(".crumb ol")) is not None, decl(".crumb ol"))
    check("     no rule anywhere lets .crumb ol wrap again",
          not any(re.search(r"flex-wrap:\s*wrap", body) for sel, body in rules if ".crumb ol" in sel), None)
    check("     every crumb holds its width", re.search(r"flex-shrink:\s*0", decl(".crumb li")) is not None, decl(".crumb li"))
    last = decl(".crumb li:last-child")
    check("     the last crumb alone shrinks, and clips with an ellipsis",
          all(re.search(p, last) for p in (r"flex-shrink:\s*1", r"min-width:\s*0", r"text-overflow:\s*ellipsis",
                                           r"white-space:\s*nowrap", r"overflow:\s*hidden")), last)

    # THE HEADER-NAV SWEEP, 3.83: the chrome is identical on every real
    # page but for the current-page marking, and every chrome link lands on
    # a real page or a recorded URL. Both checks, both directions, on
    # fixtures built from the generator's own output.
    print("33. The site chrome: identical but for the marking, every link real, stubs bare")
    _spec = _ilu.spec_from_file_location("sync_chrome", os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync-chrome.py"))
    sc = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(sc)

    def pg(page, head=None, foot=None, body="<main><h1>x</h1></main>"):
        h, f = sc.render(page)
        return f"<html><body>\n  {head if head is not None else h}\n{body}\n  {foot if foot is not None else f}\n</body></html>"
    stub = ('<html><head><meta http-equiv="refresh" content="0; url=../collision-repair/"></head>'
            '<body><p>Moved.</p></body></html>')
    # The service pages come from the generator's own SERVICES, not a typed
    # list: a typed list missed /adas-calibration/ the day it landed (3.86).
    good_keys = ["index.html", "contact-us/index.html", "blog/index.html", "areas-served/index.html"] + \
                [f"{t}index.html" for t, _ in sc.SERVICES] + \
                [f"areas-served-collision-repair-{k}/index.html" for k in audit.TOWN_ROUTES]

    def site(**over):
        s = {k: pg("" if k == "index.html" else k[:-len("index.html")]) for k in good_keys}
        s["body-shop-jamison/index.html"] = stub
        s.update(over)
        return s

    def bad(found):
        return [k for k in ("missing", "differs", "marking", "links", "stub_chrome") if found[k]]
    f0 = audit.chrome_findings(site())
    check("     generated chrome on every page, at two depths and each page marked as itself, passes",
          bad(f0) == [] and f0["forms"] == 1, f0)
    ship = {}
    for path in glob.glob(os.path.join(audit.SITE_DIR, "**", "index.html"), recursive=True):
        with open(path, encoding="utf-8") as fh:
            ship[os.path.relpath(path, audit.SITE_DIR)] = fh.read()
    fs = audit.chrome_findings(ship)
    check("     the shipped site passes both checks", bad(fs) == [], {k: fs[k] for k in bad(fs)})
    h, f = sc.render("blog/")
    for label, over, want in (
            ("a page whose nav label drifts", {"blog/index.html": pg("blog/", head=h.replace(">Contact Us<", ">Contact<"))}, "differs"),
            ("a page missing a nav item", {"blog/index.html": pg("blog/", head=re.sub(r'\s*<li class="nav-item"><a href="../contact-us/">Contact Us</a></li>', "", h))}, "differs"),
            ("a page whose footer drifts", {"blog/index.html": pg("blog/", foot=f.replace("Explore", "Pages"))}, "differs"),
            ("a page with no chrome", {"blog/index.html": "<html><body><main>x</main></body></html>"}, "missing"),
            ("a link to itself without aria-current", {"blog/index.html": pg("blog/", head=h.replace(' aria-current="page"', "", 1))}, "marking"),
            ("aria-current on a link that lands elsewhere", {"blog/index.html": pg("blog/", head=h.replace('href="../contact-us/"', 'href="../contact-us/" aria-current="page"', 1))}, "marking"),
            ("a link to a page that does not exist", {"blog/index.html": pg("blog/", head=h.replace("../contact-us/", "../contact/", 1))}, "links"),
            ("a link to a redirect stub", {"blog/index.html": pg("blog/", head=h.replace("../contact-us/", "../body-shop-jamison/", 1))}, "links"),
            ("an unrecorded external URL", {"blog/index.html": pg("blog/", head=h.replace("powerforms.docusign.net", "example.com", 1))}, "links"),
            ("a DocuSign URL one character off", {"blog/index.html": pg("blog/", head=h.replace("env=na4", "env=na3", 1))}, "links"),
            ("a CarWise link back in the chrome, withdrawn in 3.84",
             {"blog/index.html": pg("blog/", head=h.replace('</ul>\n      </nav>', '</ul>\n        <a class="btn btn-sm btn-ghost" href="'
                                                        + html.escape(audit.CARWISE_ESTIMATE_URL) + '" target="_blank" rel="noopener">Get an Estimate</a>\n      </nav>', 1))}, "links"),
            ("a dead # link", {"blog/index.html": pg("blog/", head=h.replace('href="../blog/"', 'href="#"').replace('href="./"', 'href="#"', 1))}, "links"),
            ("a redirect stub wearing chrome", {"body-shop-jamison/index.html": stub.replace("<body>", "<body>" + h)}, "stub_chrome")):
        fx = audit.chrome_findings(site(**over))
        check(f"     caught: {label}", bool(fx[want]), {k: fx[k] for k in bad(fx)})
    check("     the DocuSign link is the live nav's, recorded character for character",
          sc.render("")[0].count(html.escape(audit.DOCUSIGN_URL, quote=True)) == 1, None)
    towns_in_nav = re.findall(r'<a href="areas-served-collision-repair-[^"]+/">([^<]+)</a>',
                              re.search(r'(?s)id="nav-sub-areas".*?</ul>', sc.render("")[0]).group(0))
    check("     the Areas We Serve dropdown lists every routed town, alphabetically",
          towns_in_nav == sorted(towns_in_nav) and len(towns_in_nav) == len(audit.TOWN_ROUTES), towns_in_nav)
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync-chrome.py"), "--check"],
                       capture_output=True, text=True)
    check("     sync-chrome.py --check: every page carries the generator's chrome", r.returncode == 0, r.stdout[-400:])
    # The blog's builder cannot be re-run without its live cache, so its
    # chrome is held to the shipped pages here, byte for byte.
    _spec = _ilu.spec_from_file_location("migrate_blog", os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrate-blog.py"))
    mb = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(mb)
    _assets, _biz, chrome = mb.shell()
    for slug in ("deer-season-in-bucks-county-insurance-coverage-next-steps", "blog"):
        with open(os.path.join(audit.SITE_DIR, slug, "index.html"), encoding="utf-8") as fh:
            shipped = fh.read()
        nav, foot = chrome(f"{slug}/")
        check(f"     migrate-blog.py writes /{slug}/'s chrome exactly as it ships",
              nav + "\n  <main>" in shipped and shipped.endswith(foot), None)

    # THE HERO LAW'S SCOPED EXCEPTION, 3.86: an illustration needs its own
    # ruling. The refusal is held in both directions on the script's own
    # function and FRAMES, so a second illustration cannot arrive the way
    # a photograph does, and the one ruled frame still builds.
    print("34. A hero made in an illustration program needs a frame that declares its ruling")
    _spec = _ilu.spec_from_file_location("prep_hero", os.path.join(os.path.dirname(os.path.abspath(__file__)), "prepare-hero-photo.py"))
    ph = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(ph)
    ill = "Adobe Illustrator CC 2017 (Windows)"
    check("     an undeclared frame refuses an Illustrator source",
          ph.illustration_refusal(ill, ph.FRAMES["glass"]) is not None, None)
    check("     the ruled adas frame accepts it", ph.illustration_refusal(ill, ph.FRAMES["adas"]) is None, None)
    for tool in ("Inkscape 1.2", "CorelDRAW 2021", "Affinity Designer 2"):
        check(f"     {tool} is refused undeclared too", ph.illustration_refusal(tool, {}) is not None, None)
    for tool in ("", "Adobe Photoshop 25.0 (Macintosh)", "Adobe Lightroom Classic"):
        check(f"     a camera or photo tool ({tool or 'none declared'}) is not refused",
              ph.illustration_refusal(tool, {}) is None, None)
    check("     exactly one frame declares an illustration, the one the ruling names",
          [k for k, f in ph.FRAMES.items() if f.get("illustration")] == ["adas"], None)

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
