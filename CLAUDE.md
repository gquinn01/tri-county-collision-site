# Tri-County Collision

This is a **client build**. The client is Tri-County Collision, a collision
repair shop in Southampton, PA. The site is `https://tricountycollision.com/`.

Corcoran Communications builds and monitors it. The shop owns it.

---

## The four things that govern this repo

### 1. The build spec is `pagemap.md`

**`pagemap.md` at the repo root is the page map of record.** It was
extracted from the Tri-County plan on 2026-09-03 and it, not this file and
not an idea anyone has later, says which pages exist. If a page is not on
it, it does not get built. If the map should change, the map changes first
and the build follows.

The full plan, pricing and client notes stay OUT of this repo, because this
repo is public. `pagemap.md` carries only what the build needs.

What it commits us to, in short:

- **37 indexable pages** (38 if ADAS calibration clears its gate), plus 1
  noindexed utility page, the thank-you page. The old sitemap's 48 entries
  become 37 or 38, all real.
- **Migrate faithfully, do not rewrite for its own sake.** The promise of
  this migration is that rankings survive. Existing slugs are kept wherever
  a page keeps its purpose, because every unnecessary redirect spends a
  little of that.
- **Eleven old URLs redirect**: 8 clones to their canonical targets, 2
  category archives to the blog index, and `/customer-information/` to
  `/contact-us/`. A clone or plumbing URL gets a 301 to the page it copies
  or an honest 404, never a forced mapping to a sales page.
- **Two gates that data decides, not us.** ADAS calibration is built only if
  Keyword Planner shows demand AND the owner confirms calibration happens
  in-house. A town page keeps its page unless Search Console shows no
  impressions over the last 12 months, in which case it folds into the hub
  and its URL 301s there. This is rule 7: town pages earn their existence.
- **No page ships copy from `pagemap.md`.** Facts come from the truth
  inventory, the client-owner is fact-checker of record, and every text
  change is proposed as before/after pairs and approved before it lands.

Small and true beats big and padded. A collision shop needs the pages that
are fact, not a page count.

### 2. The corcoran-site-standards skill governs every page

It lives at `.claude/skills/corcoran-site-standards/SKILL.md`, in this repo,
from the first commit. It is a **byte-identical copy** of the firm's
standards, kept unedited on purpose so it does not fork per client. It is
the law here, not a reference:

- **Facts are sacred.** Never invent a statistic, a date, a certification,
  a year in business, or a result, not even a plausible one, not even as a
  placeholder that "will be fixed later." Placeholders ship.
- **Scope honesty.** The site may only sell what the shop actually does.
  For every "we handle / we repair / we work with" sentence, ask the client
  whether they actually do it.
- **Definition of done**: `python3 scripts/audit.py --strict` passes at
  100/100 and the diff is reviewed before commit. No exceptions, including
  for small changes.
- **Mechanism over memory**: a rule worth keeping becomes a check in
  `scripts/audit.py`. A rule that lives only in a comment gets violated.
- Plain language, no em dashes anywhere including code comments, one H1 per
  page, machine-counted title and description limits, NAP character
  identical everywhere, no price or review markup, real photos only.

Read the skill before writing a line of copy or a line of markup.

### 3. The client is the fact-checker of record

Greg holds that role for corcoranpr.com. **Here it is the shop owner**, and
it is a role, not a courtesy. Every claim on the site passes through them
before it ships. Anything they have not confirmed does not go on a page.

**Confirmed and now enforced** (2026-09-03):

```
name     Tri-County Collision
address  995 Jaymor Rd, Southampton, PA 18966
phone    (215) 322-5350   tel:+12153225350
email    contact@tricountycollision.com          (added 2026-09-05)
```

These are the values published on the shop's live site, read and confirmed
by Greg Quinn of Corcoran Communications, **the vendor**. The standards make
the client-owner the fact-checker of record for a client site, so a vendor
confirmation is a deliberate exception and it is recorded as one, here and
in `scripts/audit.py`. **Owner sign-off on the NAP is still outstanding.**
When it lands, note the date in both places.

The email is the address the live site publishes in its `AutoBodyShop`
JSON-LD and in the contact block on every service page. The live site also
prints `info@tricountycollision.com` in its footer. That second address is
**not** published here, and `scripts/audit.py` now fails any page carrying
it: two addresses for one business read as two businesses to entity
matching, and only one of them is the mailbox the shop actually reads.
Which one that is, and whether the other should forward, is still the
owner's to answer.

They are not advisory. `scripts/audit.py` now fails any page that spells the
street a second way (`Jaymor Road`, `Jaymor Rd.` with the period, a missing
ZIP, a moved comma), because each variant reads as a slightly different
business to Google's entity matching, which is how a shop ends up competing
with itself in the Map Pack. `templates/service-page-template.html` carries
all four as literals, so nobody retypes them.

That check was itself wrong until 2026-09-05, and wrong in the worst
direction: `995 Jaymor Rd., Southampton` scored as a **pass**, because the
pattern demanded a word character after `Rd.` and the canonical string is a
prefix of the variant. `scripts/test-audit-checks.py` now holds that input
and the rest of the wrong addresses, so the mechanism has a mechanism.

### The CallRail number never reaches the source

**(215) 709-9665 is a CallRail tracking number.** The old WordPress header
prints it. It must never appear in this site's HTML, its schema, the
template, or a comment, on any page.

CallRail does its work by **swapping numbers into the rendered page
visually at runtime**, which is the supported way to run call tracking
without breaking NAP consistency. The source says (215) 322-5350 and always
will; the script rewrites what a particular visitor sees. **The CallRail
snippet gets added at cutover**, in the same pass as the GA4 property, and
not before.

A tracking number baked into the markup is a second phone number for one
business, which is the Map Pack self-competition rule 6 exists to prevent,
and it is the number a crawler or an AI assistant would hand out as the
shop's. `scripts/audit.py` scores it as a **critical**, because it is the
kind of thing that gets pasted in during a hurried migration and is
invisible by eye.

**Still unconfirmed, and therefore still off:**

- **Everything else the template still tokenizes**: geo coordinates,
  socials and `sameAs`, area served, GA4 ID, form endpoint, taglines, and
  the proof line. `{{TOKENS}}` with no defaults. Fill them from the client,
  in writing, and check them character for character against the Google
  Business Profile.

### The review count is a fact with a clock on it

**274 Google reviews, 4.9 stars, read off the shop's own Google Business
Profile on 2026-09-10.** Vendor-confirmed, like the NAP, and so the same
deliberate exception: **owner sign-off is outstanding**.

It replaced 231 and "Rated Excellent", which came off the live site's
Trustindex widget on 2026-09-05. **The widget and the profile disagreed by
43 reviews in the same week**, and a shop this size does not take 43 reviews
in five days, so the widget was wrong rather than behind. That is the
argument for not carrying it through cutover, and it is recorded in
`proposed-changes.md` 4.4.

`scripts/audit.py` now holds `REVIEW_COUNT`, `REVIEW_RATING` and
`REVIEW_COUNTED_ON`, reads every visible review-count mention under `docs/`,
**fails as a critical when any two disagree**, and **warns once the reading is
more than 35 days old**. `--strict` exits 1 on a site-wide critical, which it
did not do before, because there had never been one to raise.

**No rating or review markup, ever**, on the strength of this or anything
else. Google's guidelines rule out self-serving review markup on a business's
own site. Visible text only.

### Comments name the constant, never the value

**A comment never carries the literal review count or the stat band's order.
It names `REVIEW_COUNT` and "the band's DOM order" instead.** Decided
2026-09-10, after the stat band's own comment was found carrying a stale
count and a stale order through two commits.

Nothing could have caught it. The review-count check strips comments before
it reads counts, on purpose, so that a comment recording history is not read
as the page contradicting itself, and the one mechanism that reads counts is
therefore the one told to look away. A comment that names the constant stays
true when the value changes; a comment that spells the value out is a copy
that nothing updates.

`scripts/audit.py` **warns, and can only ever warn**, when an HTML comment
under `docs/` carries a two-to-four digit number within a few words of
"review". It is handed no `fails` list, so it is structurally incapable of
stopping a build: a rotting comment misleads the next reader and costs a
visitor nothing, and a check that can fail a build on somebody's reasonable
prose is a check that gets deleted rather than fixed.

**The convention and the check fit by construction.** `\breview\b` cannot
match inside `REVIEW_COUNT`, because the next character is an underscore and
an underscore is a word character. The approved spelling is exactly the one
the pattern cannot fire on.

The proof line deserves its own warning. Years in business, I-CAR or ASE
certifications, manufacturer approvals, insurer relationships, warranty
terms: every one of those is checkable, and every one of them ships only
after the owner has confirmed it.

### 4. The client owns their accounts

**GA4, Google Business Profile, the domain, and the form endpoint all live
in the client's own accounts, never the agency's.** Analytics goes in the
shop's Google account. The form posts to the shop's endpoint. This is what
makes the exit promise, "you keep everything," easy to keep, and it is
easier to set up right than to unwind later.

---

## The design system

**Decided 2026-09-06, from three complete pages built as drafts and compared
by scrolling. The pick is PHOTOGRAPHIC. Pages 2 through 37 inherit it, and
nobody re-decides it per page.** The losing drafts were deleted rather than
kept around, because a second direction sitting in the repo is a second
direction someone will build from.

The full spec, with the arithmetic, lives in the header of
`docs/assets/site.css`. That file is the one place the palette and the type
are defined. Read it before writing a hex, a `font-family`, or a hero.

**1. The hero is a full-bleed photograph with an opaque panel over it.**
Opaque, not a translucent wash: type over a photograph is
only reliably readable when something solid sits behind it. The photograph is
a real one of this shop, its people or its work.

**The panel's ground is oxblood, decided 2026-09-10.** It was ink until then.
It now carries `.field-ox`, the same ground the two act bands carry, including
the recorded 104 degree gradient, under the palette law's written exception for
section backgrounds. Still opaque: a gradient between two solid stops is not a
wash, and nothing of the photograph shows through.

**It is the same class, not a copy of it.** The act-button rule is keyed to
`.field-ox`, so the hero's Call button became ink-filled with silver text and
the silver hairline **on its own**, and the Email ghost stayed a silver outline,
with nothing written for the hero specifically. One class, one ground, one
button grammar. A hand-copied gradient would have needed its own button rule
and would have drifted from the bands the first time either changed.

**The supporting colours were re-measured against the gradient's lightest
stop**, `--ox`, which is the worst case: h1 and eyebrow 11.04, lead and
breadcrumb 7.34, breadcrumb separator 8.35. Text needs 4.5 and a chip border
needs 3 as a shape. Everything cleared without moving a token. **Only the chip
border's alpha changed**, from .42 to .50, and not to make it stronger: .42
measured 3.85 on ink and only 3.11 on the lighter oxblood ground, so .50 puts
it back to exactly 3.85. Same strength, on a ground that changed under it.

**2. The panel is flush to the left viewport edge.** No gap, no float, no
rounded corner. Its **left padding equals the page grid's left margin**, so
the type inside it lines up with the first character of every band below it.
At wide viewports the panel **grows with the margin instead of detaching from
the edge**: it is welded to the glass, and only the column inside it moves
with the grid. `width = --edge + --col + --pad-r`, and because the width
contains `--edge`, the panel is 792px at 1440 and 1032px at 1920.

**3. A stat band sits directly under the hero, on paper. Three stats.**
Big numeral, label, one supporting line. **Three is the rule, not the
leftover**: a four-across row is the natural shape and there is no fourth
honest number, so the third stat is a word. Inventing a statistic to balance a
layout is the exact failure the prime law exists to stop. **Any number that is
true only on the day it is written carries the date it was true**, in the
supporting line. On the collision page that is the review count.

**4. Type: Archivo Black for display, Source Sans 3 for reading.** Both
self-hosted in `docs/assets/fonts/`, both SIL Open Font License 1.1, both
licence texts sitting beside them unedited. **Nothing reaches a webfont CDN at
runtime**, so there is no third-party request on any page and nothing to break
when someone else's CDN changes. Archivo Black takes `h1`, `h2`, `h3` and the
step numerals and nothing smaller; every label, subhead and run of body copy
is Source Sans 3. **Archivo Black has exactly one weight.** Ask it for 700 and
the browser fakes it, which looks like a mistake because it is one.

**5. Ink sticky header**, with the slim ink staging bar above it until
cutover. The call button keeps its oxblood fill, because oxblood means act,
and carries a silver border: `--ox` on `--ink` measures **1.47**, so without
the border the button is invisible as a shape even though its label reads at
11.04.

**The act button on any dark ground wears the silver hairline.** Decided
2026-09-10, and it is one symmetric rule rather than two exceptions, because
the two failures are **the same number**: `--ox` on `--ink` is 1.47 and
`--ink` on `--ox` is also 1.47. So on the two oxblood bands the act button is
now **ink filled with silver text and the silver hairline**, exactly as the
header's button is oxblood filled with silver text and the silver hairline. The
fill is whichever dark the ground is not; the hairline is what gives the shape
an edge. Labels read at 11.04 and 16.21. **The Email ghost button beside it is
unchanged on either ground** — it is a border and a label already.

**6. The palette is four colours, two text shades and one highlight ground**, and gold is not one of
them any more. Oxblood means act and nothing else: two oxblood bands per page,
each carrying the CTA row. Ink is structural. Solid colours only and no glows.

**White is a ground, not a shade of the ground.** Added 2026-09-10. `--silver`
is the page; `--white` is used on exactly **one band**, the stat band under the
hero, to lift the three proof figures off the run of the page. Every text pair
gets better on it: ink 17.33 against 14.09, oxblood 11.80 against 9.60,
`--ink-2` 9.80 against 7.96, `--ox-tx` 8.95 against 7.27.

**The band separates more than it used to, and that was not the plan.** It
measured 1.07 against the old cream ground, chosen so it would read as the same
page one shade cleaner rather than as a contrast switch. Against the silver it
measures **1.23**. Still nothing like a band change, but the highlight does more
work now than it was asked to.

**The ground is the logo's silver, decided 2026-09-10.** 40,515 opaque hueless
letterform pixels were sampled out of the TRI-COUNTY wordmark, the same method
that produced `--mark`. **The wordmark is chrome, so it is a range, not a
colour**: darkest #676767, median #ABABAB, p75 #CACACA, highlight #E6E8E8.
**Which stop becomes the ground is a judgement and it is recorded as one.** The
median is what the eye calls the silver and it is unusable as a ground:
`--ink-2` measures 4.27 on it and `--ox-tx` 3.90, so secondary and small accent
text both fail. The rule taken was **the lightest stop the wordmark actually
contains** — the highlight where the chrome catches the light — which is
**#E6E8E8**. Sampled, not invented, and every text pair clears on it.

`--rule` came out of the same sample at the wordmark's p75, **#CACACA**. It had
to move: the old warm #DED8D1 measured 1.32 on the cream and only **1.15** on
the silver, which is a hairline nobody can see. #CACACA measures 1.33.

**The temperature change is a brand decision, not a taste one.** #F9F7F4 was a
warm cream, red highest and blue lowest. #E6E8E8 is the logo's own
neutral-to-cool chrome. The page now stands on a colour the mark is actually
made of, which is the same argument that put #691C17 and #E92424 in the table.
**What it costs:** every ratio on the ground drops a little, because the ground
got darker. Nothing dropped below its floor.

**One sanctioned section-background gradient, decided 2026-09-10.** The firm's
palette law allows exactly this one exception, and only as a dated, recorded
decision; this is the record. The two oxblood act bands carry a gradient taken
from **the logo's own swoosh** — the mark's red sweep runs dark, bright, dark
across its length, and the chrome sweep beneath it does the same in grey. At
band scale that reads as light falling across a painted panel.

**It stays inside one hue, which is the point.** The brightest place in the
band is `--ox` exactly and the ends are a deeper oxblood, so **oxblood still
means act from the first pixel**. A version starting in `--ink` was drawn and
rejected for that reason: an act band would have spent its first screen
looking structural. The deep end is **derived, not invented** — `color-mix()`
takes it from `--ox-dk` and `--ink`, both already in the palette, so no fifth
colour is typed into the stylesheet.

Text gets *more* readable toward the ends, not less: 11.04 on `--ox`, 13.02 on
`--ox-dk`, 14.38 at the deep end. **Nothing else on this site gets a
gradient** — not text, not a button, not a card, not an accent.

**7. The lift, adopted 2026-09-10. A mold behaviour: every card on every page
gets it and nobody re-decides it per page.** A `.card`, `.step` or `.svc`
rises 3px under a pointer, an ink shadow comes up beneath it, and the oxblood
rule along its base sharpens from quiet to solid and sweeps to the card's full
width. The lift is generic on purpose, because feedback to a hand should feel
familiar. **The materials are what make it this site's**: the default is a
soft grey glow that belongs to nobody, and this shadow is `--ink`, so a card
casts a shadow the colour of the site's own darkest value. The sweep is the
branded half.

What may move is a short list: **transform, opacity, and the rule's width.**
No colour animates, no shadow animates, no height animates. It is pure CSS,
so it works with JavaScript off. It is hover-only, behind
`@media (hover: hover)`, so a tap never welds a hover state on. Under
`prefers-reduced-motion` the hover **state** still changes, because a reader
who asked for less motion still needs to know the pointer is on something;
what goes is the movement.

Two costs, both paid: the step numeral moved from `.step::before` to
`.step h3::after`, because the lift needs both pseudo-elements, and `.svc`
gave up `overflow: hidden` with the photo's rounding moving onto the image.
**A component that wants the lift needs both of its own pseudo-elements
free.**

Under a pointer the step numeral also goes solid oxblood, on the same clock as
the sweep, so a card answers as one gesture rather than two. **Colour only, no
blur, no glow**, and it is the one property outside transform, opacity and the
rule's width that the stylesheet animates.

**8. Arrival motion, adopted 2026-09-10.** The odometer and the lane, both
from the same sampler.

---

## The motion amendment, 2026-09-10

**Motion used to be zero except the FAQ accordion. It is not zero any more.**
Five candidates were built on a sampler, judged, and the sampler was deleted
once every verdict was in. Two were cut. The reasoning is in the git history
around this date. Four things move now, in two kinds.

**Kind one, which was always allowed: motion that answers a reader.** The FAQ
disclosure and its chevron, the lift under a pointer, the press under a
finger. Unremarkable.

**Kind two, which is the actual amendment: motion may also fire once on a
section's first arrival. A number counts. A word rolls with it. A lane draws.
Never looping, never re-triggering.** The stat band is one event, not three:
all three stats roll on the same drum and the same class, released by the same
observer, so the row arrives as a row. The word's strips hold **the same letter
twice** and travel one cell, so it rolls without ever showing a character that
is not its own.

Both are still evidence rather than costume, which is the only reason they
were allowed in:

- **The number counts because the number is real.** The stat band carries
  checked, dated figures, and an odometer is the one counting instrument that
  belongs to a car. A counter over an invented number would be the prime law's
  exact failure wearing a nice easing curve. **It reads its target from the
  markup**, so the weekly review-count refresh edits one number in the HTML and
  the effect follows. Nobody refreshing a count needs to know it exists.
- **The lane draws because the section is a road.** Six steps from the phone
  call to the keys, with a dashed centre line down them. A lane and not a
  progress bar on purpose: no track, no state change once painted, constant
  speed.

**The lane's audience is a phone reader, and only a phone reader.** It exists
only below 720px, the one width where `.steps` is a single column and a line
from 01 to 06 is a road rather than a stray rule across a grid. A desktop
reader never sees it. That is a deliberate scope, not an unfinished one.

**Under `prefers-reduced-motion` both do nothing.** The number rests at its
true value, which is what it was showing anyway, and the lane rests fully
drawn. Nothing is hidden and nothing is pending, in that case or with
JavaScript off. The strips are `[target, 0-9, target]`, so the true number is
on screen before the roll, after it, and when no script runs at all.

**The limit of this amendment:** once, on first arrival, then the observer
stops watching. Anything that would move a second time, or move without a
reader having either arrived or acted, is a different decision and needs its
own amendment, dated, here and in the header of `docs/assets/site.css`.

## Staging ships noindexed on purpose

**Three things are deliberately "wrong" on every page in `docs/` until
cutover. None of them is a defect and none of them gets "fixed" before
then.**

```
1. <meta name="robots" content="noindex, nofollow">   on every page
2. docs/robots.txt                                    Disallow: /
3. <link rel="canonical">                             absolute to
                                                      https://tricountycollision.com/
```

The reason is the one that also keeps GitHub Pages switched off: **the
shop's real site is live on WordPress right now**, and a crawlable copy of
it at a second address is a second address answering for one business. That
is the Map Pack self-competition rule 6 exists to prevent, and it is worse
here than on a greenfield build, because the two copies would be near
duplicates of each other.

The three work at different layers on purpose. `robots.txt` stops the fetch.
The meta tag stops the indexing if a URL is reached some other way, which a
`robots.txt` disallow does not by itself guarantee. The canonical means any
signal that does leak lands on the **real** site rather than on a staging
address, and it is absolute from day one so no page has to be edited at
cutover to point somewhere new.

**This is enforced, not remembered.** `scripts/audit.py` carries a `STAGING`
switch, and while it is `True` the noindex check runs **inverted**: a page
carrying the tag passes, and a page **missing** it is a critical. The risk
during staging is not that a page is noindexed, it is that one page quietly
is not. The audit also checks `docs/robots.txt` itself, because tags without
the file is only half the exception. Every scored page carries a note naming
the exception, so nobody reading a report has to wonder.

**At cutover, all three come off in one commit**: set `STAGING = False`,
strip the meta tag from every page, and replace `docs/robots.txt` with an
open one that names the sitemap and blocks no AI crawler (GPTBot,
OAI-SearchBot, ClaudeBot, anthropic-ai, PerplexityBot and Google-Extended
stay welcome). Flipping the switch before the tags come off fails every
page, which is the correct alarm and not a bug. Record the date here when it
happens.

The pages also carry a visible staging banner. A human who opens one should
not have to read the head to find out why it is not indexed.

## Never touch MX records

At cutover, change **web DNS records only**. Never MX.

The shop's email has to survive the launch. An MX change during a website
cutover takes down the address customers and insurers send estimates to,
and mail that bounces during the gap is gone. Web records and mail records
are separate, and there is no reason a site launch should ever touch the
mail ones.

Also at cutover: archive the old WordPress site completely before it goes
dark. That archive is the last copy of it that will ever exist.

---

## What is in here

| Path | What it is |
|---|---|
| `pagemap.md` | **The build spec.** The page map of record. |
| `.claude/skills/corcoran-site-standards/` | The law. Unedited copy of the firm's standards. |
| `scripts/audit.py` | The SEO and AEO scanner. Scores every page separately. Its NAP block is the one place the canonical name, address and phone live, and its review block is the one place the review count, the rating and the day they were counted live. |
| `scripts/test-sitemap-expansion.py` | Tests the sitemap expansion. Run it before touching that code. |
| `scripts/test-audit-checks.py` | Smoke tests for the checks that must never drift back: the address spelling, the CallRail number, the one email, and the review count. Written after the address check was caught scoring a wrong address as a pass. |
| `proposed-changes.md` | Every text change made during the migration, as before/after pairs, plus the claims the pages carry. Awaiting the owner's fact-check. |
| `scripts/build-sitemap.py` | Generates `docs/sitemap.xml` from the pages themselves. `lastmod` comes from each page's own schema `dateModified`, never from a file mtime and never from today. |
| `scripts/stamp-assets.py` | Cache-busting stamps for `docs/assets/site.css` and `site.js`. |
| `scripts/fetch_seo_news.py` | Pulls the headline sweep the Google Watcher reads. |
| `scripts/cascade-analyzer.html` | CSS cascade analyzer. |
| `scripts/mobile-check.md` | The mobile check procedure. |
| `templates/service-page-template.html` | The service and location page template. |
| `agents/site-auditor.md` | The weekly Monday report agent's job description. |
| `agents/google-watcher.md` | The daily algorithm watch agent's job description. |
| `.github/workflows/` | The two agent schedules. |
| `docs/` | The site. |
| `docs/assets/site.css` | **The design system.** The one place the palette and the type are defined. Its header carries the chosen direction, the type pairing, the flush-left hero arithmetic, the stat-band rule, the palette table with its provenance, and the measured contrast ratios. |
| `docs/assets/fonts/` | Archivo Black and Source Sans 3, self-hosted, with their unedited SIL OFL 1.1 licence texts. No webfont CDN is contacted at runtime. |

## The two agents

- **Site Auditor**, Mondays 12:00 UTC. Scans the site, files the weekly
  report as a GitHub Issue labeled `audit-report`. That report is the
  monitoring product the retainer buys, so it ships every week.
- **Google Watcher**, daily 11:00 UTC. Reads the SEO news sweep and files
  an Issue labeled `google-update` only when something actually matters to
  this shop. Most days it files nothing, and silence is a feature.

Both need the `ANTHROPIC_API_KEY` secret. **The client repo's owner adds it
through the GitHub website.** Do not add, print, echo, or otherwise handle
secrets from a terminal.

## The audit target, and when it changes

The `SITE_URL` repo variable is set to `https://tricountycollision.com/`,
so **the weekly scan runs against the shop's LIVE WordPress site**. That is
correct until cutover, because `docs/` is empty and a local run over an
empty folder would report a clean site that does not exist.

The live sitemap is WordPress's, which ships a `<sitemapindex>` rather than
a `<urlset>`. `scripts/audit.py` follows the index into its children.
`scripts/test-sitemap-expansion.py` is the test that keeps it doing so, and
it matters more here than it ever did on a hand-built site.

**At cutover**, decide explicitly whether to clear `SITE_URL` and scan
`docs/` locally or leave it set and keep scanning the live domain, and
record the decision here. Do not let it drift.

## Before you commit

```
python3 scripts/test-sitemap-expansion.py     # exits 1 if anything fails
python3 scripts/test-audit-checks.py          # exits 1 if anything fails
python3 scripts/stamp-assets.py               # after touching site.css or site.js
python3 scripts/build-sitemap.py              # after adding or removing a page
python3 scripts/audit.py --strict             # every page at 100/100
```

The two middle commands take `--check`, which exits 1 instead of rewriting.
Neither is a thing to remember: the audit fails a page whose asset stamp is
stale or whose `<url>` block is missing.

## GitHub Pages

**Off, on purpose.** Turning it on before cutover would publish an empty
folder at a github.io address while the shop's real site is still live,
which is a second address answering for the same business. Leave it off.
