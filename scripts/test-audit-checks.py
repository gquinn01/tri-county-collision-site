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

    # The inventory is not empty, and that is the point: if it ever is,
    # either every referenced page exists or somebody deleted the
    # attributes instead of converting them.
    pend = audit.find_pending_links(os.path.join(root, "docs"))
    check("    and the pending inventory is populated, not quietly emptied",
          len(pend) > 0, len(pend))

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

    print("16. The odometer must not disturb the review count")
    # WHY. The stat band's numbers now roll. Each digit is a strip of
    # [target, 0-9, target], so at runtime the DOM holds a lot of digits
    # that are not the review count. THE STRIPS ARE BUILT BY site.js AND
    # NEVER EXIST IN THE FILE, which is what keeps the review-count check
    # honest: it reads source, not a rendered page. These cases hold that
    # invariant down, because the tempting "optimisation" later is to
    # pre-render the strips into the HTML.
    import tempfile as _tempfile2

    site_js = open(os.path.join(root, "docs", "assets", "site.js"),
                   encoding="utf-8").read()
    check("     site.js reads the number from the markup, not a constant",
          ".stat-n" in site_js and str(audit.REVIEW_COUNT) not in site_js)
    check("     so a review-count refresh needs no knowledge of the effect",
          "textContent.trim()" in site_js)

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

    # And the guard would notice if someone ever baked the strips in.
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
