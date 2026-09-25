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
                                      "blog-index": ("faq-schema",)},
          audit.RUBRIC_EXEMPTIONS)

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
        shipped = sorted(glob.glob(os.path.join(root, "docs", "*.html")) +
                         glob.glob(os.path.join(root, "docs", "*", "index.html")))
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
