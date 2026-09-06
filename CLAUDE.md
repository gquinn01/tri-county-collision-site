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
| `scripts/audit.py` | The SEO and AEO scanner. Scores every page separately. Its NAP block is the one place the canonical name, address and phone live. |
| `scripts/test-sitemap-expansion.py` | Tests the sitemap expansion. Run it before touching that code. |
| `scripts/test-audit-checks.py` | Smoke tests for the NAP checks: the address spelling, the CallRail number, the one email. Written after the address check was caught scoring a wrong address as a pass. |
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
| `docs/` | The site. `assets/site.css` is the one place the palette lives, and its header carries the palette table, where each color came from, and the measured contrast ratios. |

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
