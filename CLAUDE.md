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

- **37 indexable pages** (38 if ADAS calibration clears its gate), plus 2
  noindexed utility pages. The old sitemap's 48 entries become 37 or 38,
  all real.
- **Migrate faithfully, do not rewrite for its own sake.** The promise of
  this migration is that rankings survive. Existing slugs are kept wherever
  a page keeps its purpose, because every unnecessary redirect spends a
  little of that.
- **Ten old URLs redirect**: 8 clones to their canonical targets, 2 category
  archives to the blog index. A clone or plumbing URL gets a 301 to the page
  it copies or an honest 404, never a forced mapping to a sales page.
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
```

These are the values published on the shop's live site, read and confirmed
by Greg Quinn of Corcoran Communications, **the vendor**. The standards make
the client-owner the fact-checker of record for a client site, so a vendor
confirmation is a deliberate exception and it is recorded as one, here and
in `scripts/audit.py`. **Owner sign-off on the NAP is still outstanding.**
When it lands, note the date in both places.

They are not advisory. `scripts/audit.py` now fails any page that spells the
street a second way (`Jaymor Road`, a missing ZIP, a moved comma), because
each variant reads as a slightly different business to Google's entity
matching, which is how a shop ends up competing with itself in the Map Pack.
`templates/service-page-template.html` carries all three as literals, so
nobody retypes them.

**Still unconfirmed, and therefore still off:**

- **The email.** The owner has not designated the one address to publish.
  The page map calls for one email and one phone on both Home and Contact,
  so there is a right answer and it is theirs to give. `NAP_EMAIL_RE` stays
  `None`, the email half of the contact check does not run, and the audit
  says so as a note on every page rather than passing silently. Do not pick
  an address off the old site.
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
| `scripts/stamp-assets.py` | Cache-busting stamps for `docs/assets/site.css` and `site.js`. |
| `scripts/fetch_seo_news.py` | Pulls the headline sweep the Google Watcher reads. |
| `scripts/cascade-analyzer.html` | CSS cascade analyzer. |
| `scripts/mobile-check.md` | The mobile check procedure. |
| `templates/service-page-template.html` | The service and location page template. |
| `agents/site-auditor.md` | The weekly Monday report agent's job description. |
| `agents/google-watcher.md` | The daily algorithm watch agent's job description. |
| `.github/workflows/` | The two agent schedules. |
| `docs/` | Placeholder. The build has not started. |

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
python3 scripts/audit.py --strict             # once docs/ has pages
```

## GitHub Pages

**Off, on purpose.** Turning it on before cutover would publish an empty
folder at a github.io address while the shop's real site is still live,
which is a second address answering for the same business. Leave it off.
