# docs/ is the site

Brought current 2026-10-09 (`proposed-changes.md` 3.94). **37 indexable pages
are built**: home, five service pages, the areas hub, twelve town pages,
contact, the blog index and sixteen posts, plus two redirect stubs. Privacy is
the 38th and ships with the first analytics tag. `pagemap.md` at the repo root
is the page map of record, and `CLAUDE.md` carries the cutover checklist.

**GitHub Pages is deliberately NOT enabled on this repository.** The shop's
real site is still live on WordPress, and a second address answering for the
same business is the exact harm rule 6 exists to prevent. Leave it off until
cutover.

## Staging: four things are "wrong" on purpose

```
1. <meta name="robots" content="noindex, nofollow">   on every page
2. robots.txt                                         Disallow: /
3. <p class="staging">                                the visible banner
4. llms.txt                                           its staging paragraph
```

The canonicals are absolute to `https://tricountycollision.com/` from day one,
so they need no change at cutover.

Do not fix any of the four. They come off together at cutover and not before.
`scripts/audit.py` enforces this through its `STAGING` switch, in both
directions: while it is on, a page **missing** its noindex tag is a critical
and a page missing its banner warns; once it is off, a noindex tag, a banner,
or staging language left in `llms.txt` is a critical. The page generators
(`scripts/build-town.py`, `migrate-blog.py`, `migrate-hub.py`) read the same
switch, so a rebuild after cutover cannot re-stage a page. CLAUDE.md carries
the full flip procedure.

## What is in here

| Path | What it is |
|---|---|
| `assets/site.css` | **The design system, and the one place the palette lives.** Its header carries the chosen direction, the type pairing, the hero arithmetic, the stat-band rule, the palette table with its provenance, the motion amendments and the measured contrast ratios. Read it before writing a hex, a `font-family` or a hero. |
| `assets/fonts/` | Archivo Black and Source Sans 3, self-hosted, with their unedited SIL OFL 1.1 licence texts. **No webfont CDN is contacted at runtime.** |
| `assets/site.js` | Small, deliberately: the footer year, the nav disclosures, the lane's arrival motion and the Real Repairs pairs. Every page works with JavaScript off. |
| `assets/img/` | Photographs, marks and icons. Every image's provenance is read by `scripts/audit.py`. |
| `favicon.ico`, `assets/img/icon-*.png` | The shop's own site icon, taken from its live site (3.94). |
| `robots.txt` | The staging block. |
| `llms.txt` | The AI-agent guide. A page is not done until it is listed here. |
| `sitemap.xml` | **Generated.** Run `python3 scripts/build-sitemap.py`; do not hand-edit. |

## The design, decided once

The direction was picked on 2026-09-06 and amended since, each amendment dated.
**Nobody re-decides it per page.** Its current state, with every amendment and
the arithmetic behind it, is in the header of `assets/site.css`, and CLAUDE.md
carries the short version. Do not take the design from this file.

## Rules that hold on every page here

- **Never write a link to a page that does not exist.** The audit fails a
  relative link with no file behind it, so this is checked rather than
  remembered.
- **Every internal link is relative** and never starts with `/`. Absolute URLs
  appear only where the spec demands them: canonical, `og:url`, `og:image` and
  schema `@id`/`url`.
- **The FAQ is mirrored.** Each visible answer is byte-identical to its
  `acceptedAnswer`. Edit one, edit both. The audit scores a mismatch as a
  critical.
- **No price, offer, review or rating markup.**
- **No em dashes**, anywhere, code comments included.

A page does not exist until all four of these are true:

1. its `<url>` block is in `sitemap.xml` (run the generator)
2. its line is in `## Key pages` in `llms.txt`
3. it is linked from the nav and the footer column it belongs in
4. `python3 scripts/audit.py --strict` passes it at 100/100

Steps 1, 2 and 3 are all enforced. Step 4 is the definition of done and has no
exceptions, including for small changes.

## The photographs

What is the shop's own, what is licensed stock and what is on the shoot list is
recorded in `proposed-changes.md` 4.9 and section 3. Stock that remains is
there by Greg's launch-placeholder ruling of 2026-10-06, and is a shoot-list
item, not a blocker.

## The NAP, which the audit enforces

```
Tri County Collision Center
995 Jaymor Rd, Southampton, PA 18966
(215) 322-5350
contact@tricountycollision.com
```

One spelling, everywhere, character for character. `scripts/audit.py` fails a
page that writes the street any other way, the trailing period in `Jaymor Rd.`
included, and it fails a page carrying the old site's second email address.
Do not retype any of it from memory.

**The CallRail tracking number does not belong in this folder**, which is why
its digits are not printed here. CallRail swaps numbers into the page visually
at runtime, so the source says (215) 322-5350 and nothing else. The snippet is
added at cutover. CLAUDE.md carries the number and the reasoning;
`scripts/audit.py` scores it as a critical on any page.

## Until cutover

The weekly Site Auditor is pointed at the LIVE WordPress site at
https://tricountycollision.com/ through the `SITE_URL` repo variable. It is
scanning the shop's real site, not this folder, and the Monday report says so
on its own face.

## At cutover

Web DNS records only. **Never MX.** The shop's email has to survive the launch.
Archive the old WordPress site completely before it goes dark; that archive is
the last copy of it that will ever exist.

The map's redirect discipline applies here: test the redirect list against the
old site's full URL list, which means the old sitemap, anything Search Console
has ever shown, and the archive's link graph. Every entry names an equivalent
page or is an honest 404.
