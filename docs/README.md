# docs/ is the site

The build has started. One page is in: `/collision-repair/`, migrated from the
shop's live WordPress page on 2026-09-05 and reviewed as the pattern the other
36 follow.

**GitHub Pages is deliberately NOT enabled on this repository.** The shop's
real site is still live on WordPress, and a second address answering for the
same business is the exact harm rule 6 exists to prevent. Leave it off until
cutover.

## Staging: three things are "wrong" on purpose

```
1. <meta name="robots" content="noindex, nofollow">   on every page
2. robots.txt                                         Disallow: /
3. <link rel="canonical">     absolute to https://tricountycollision.com/
```

Do not fix any of them. They come off together at cutover and not before.
`scripts/audit.py` enforces this through its `STAGING` switch: while it is on,
a page **missing** its noindex tag is a critical, because the risk is not that
a page is noindexed, it is that one page quietly is not. CLAUDE.md carries the
full reasoning and the cutover checklist.

Every page also carries a visible staging banner, so a human who opens one does
not have to read the head to find out why.

## What is in here

| Path | What it is |
|---|---|
| `assets/site.css` | **The one place the palette lives.** Its header carries the palette table, where each color was sampled from on the live site, and the measured contrast ratios. Read it before writing a hex anywhere. |
| `assets/site.js` | Almost empty, deliberately. Every page works with JavaScript off. |
| `assets/img/` | Photographs. See the warning below. |
| `collision-repair/` | The pattern page. |
| `robots.txt` | The staging block. |
| `llms.txt` | The AI-agent guide. A page is not done until it is listed here. |
| `sitemap.xml` | **Generated.** Run `python3 scripts/build-sitemap.py`; do not hand-edit. |

## Rules that hold on every page here

- **Never write a link to a page that does not exist.** The nav and the footer
  columns grow as pages land. `scripts/test-audit-checks.py` fails the build on
  a relative link with no file behind it, so this is checked rather than
  remembered. It is why the logo is not yet a link and why the breadcrumb's
  "Home" is plain text: `docs/index.html` has not been built.
- **Every internal link is relative** and never starts with `/`. Absolute URLs
  appear only where the spec demands them: canonical, `og:url`, `og:image` and
  schema `@id`/`url`.
- **The FAQ is mirrored.** Each visible answer is byte-identical to its
  `acceptedAnswer`. Edit one, edit both. The audit scores a mismatch as a
  critical.
- **No price, offer, review or rating markup.** The live site publishes a
  `priceRange` and an offer catalog. Neither is carried, and both are on the
  claims list as an owner decision.
- **No em dashes**, anywhere, code comments included.

A page does not exist until all four of these are true:

1. its `<url>` block is in `sitemap.xml` (run the generator)
2. its line is in `## Key pages` in `llms.txt`
3. it is linked from the nav and the footer column it belongs in
4. `python3 scripts/audit.py --strict` passes it at 100/100

Steps 1, 2 and 3 are all enforced. Step 4 is the definition of done and has no
exceptions, including for small changes.

## The photographs are not cleared yet

`assets/img/` holds three photographs carried over from the live page. **All
three look like stock**, and the live site's blog images are named
`AdobeStock_*.jpeg`, so the site demonstrably uses stock elsewhere. The
standards say real photos only: the owner, the shop, the work.

They are here because the migration is faithful and staging is not public.
`proposed-changes.md` lists this as the one item that should stop a launch.
Confirm each is the shop's own work, or replace it before cutover.

## The NAP, which the audit enforces

```
Tri-County Collision
995 Jaymor Rd, Southampton, PA 18966
(215) 322-5350
contact@tricountycollision.com
```

One spelling, everywhere, character for character. `scripts/audit.py` fails a
page that writes the street any other way, the trailing period in `Jaymor Rd.`
included, and it fails a page carrying the old site's second email address.
Do not retype any of it from memory; the template carries all four.

**The live site spells the street two ways on one page**: `Rd` in its footer,
`Road` in its JSON-LD. This build carries `995 Jaymor Rd` in both places by
construction. See `proposed-changes.md`, section 3.1.

**The CallRail tracking number does not belong in this folder**, which is why
its digits are not printed here. CallRail swaps numbers into the page visually
at runtime, so the source says (215) 322-5350 and nothing else. The snippet is
added at cutover. CLAUDE.md carries the number and the reasoning;
`scripts/audit.py` scores it as a critical on any page, and
`scripts/test-audit-checks.py` fails the build if it appears anywhere under
`templates/` or `docs/`.

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
