# docs/ is a placeholder

Nothing has been built yet. This folder exists so the repo's shape is right
from the first commit, not because there is a site in it.

**GitHub Pages is deliberately NOT enabled on this repository.** Turning it
on would publish an empty folder at a github.io address while the shop's
real site is still live on WordPress, which is a second address answering
for the same business. Leave it off until cutover.

## What lands here when the build starts

**`pagemap.md` at the repo root is the page map of record.** It is the build
spec: 37 indexable pages, 38 if ADAS calibration clears its gate, plus 2
noindexed utility pages, and 10 old URLs that redirect. Every page it lists
gets built from `templates/service-page-template.html`, and every page is
governed by the `corcoran-site-standards` skill in
`.claude/skills/corcoran-site-standards/`. The standards are not advisory.

Two things the map insists on that are easy to lose during a migration:

- **Slugs are kept wherever a page keeps its purpose.** The promise of this
  migration is that rankings survive, and every unnecessary redirect spends
  a little of that.
- **Content that ranks migrates faithfully**, rather than being rewritten
  for its own sake. Fixing a title over 60 characters is the job. Rewriting
  a 4,100-word page that is working is not.

A page does not exist until all four of these are true:

1. its `<url>` block is in `docs/sitemap.xml` with the real date
2. its line is in `## Key pages` in `docs/llms.txt`
3. it is linked from the navigation `pagemap.md` specifies
4. `python3 scripts/audit.py --strict` passes it at 100/100

Steps 1 and 2 are enforced by the audit, which fails a page that is missing
from either. Step 4 is the definition of done and has no exceptions,
including for small changes.

## Until then

The weekly Site Auditor is pointed at the LIVE WordPress site at
https://tricountycollision.com/ through the `SITE_URL` repo variable. It is
scanning the shop's real site, not this folder. That is what the Monday
report describes, and the report says so on its own face.

## The NAP, which the audit now enforces

```
Tri-County Collision
995 Jaymor Rd, Southampton, PA 18966
(215) 322-5350
```

One spelling, everywhere, character for character. `scripts/audit.py` fails
a page that writes the street any other way. Do not retype it from memory;
the template already carries it.

The **email is still open**: the owner has not designated the one address to
publish, so the audit's email check is off and says so on every page. The
map calls for one email and one phone on Home and on Contact.

## At cutover

Web DNS records only. **Never MX.** The shop's email has to survive the
launch. Archive the old WordPress site completely before it goes dark; that
archive is the last copy of it that will ever exist.

The map's redirect discipline applies here: test the redirect list against
the old site's full URL list, which means the old sitemap, anything Search
Console has ever shown, and the archive's link graph. Every entry names an
equivalent page or is an honest 404.
