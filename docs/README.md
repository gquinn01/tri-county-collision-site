# docs/ is a placeholder

Nothing has been built yet. This folder exists so the repo's shape is right
from the first commit, not because there is a site in it.

**GitHub Pages is deliberately NOT enabled on this repository.** Turning it
on would publish an empty folder at a github.io address while the shop's
real site is still live on WordPress, which is a second address answering
for the same business. Leave it off until cutover.

## What lands here when the build starts

The page map in the Tri-County plan is the build spec. Every page it lists
gets built from `templates/service-page-template.html`, and every page is
governed by the `corcoran-site-standards` skill in
`.claude/skills/corcoran-site-standards/`. The standards are not advisory.

A page does not exist until all four of these are true:

1. its `<url>` block is in `docs/sitemap.xml` with the real date
2. its line is in `## Key pages` in `docs/llms.txt`
3. it is linked from the navigation the plan specifies
4. `python3 scripts/audit.py --strict` passes it at 100/100

Steps 1 and 2 are enforced by the audit, which fails a page that is missing
from either. Step 4 is the definition of done and has no exceptions,
including for small changes.

## Until then

The weekly Site Auditor is pointed at the LIVE WordPress site at
https://tricountycollision.com/ through the `SITE_URL` repo variable. It is
scanning the shop's real site, not this folder. That is what the Monday
report describes, and the report says so on its own face.

## At cutover

Web DNS records only. **Never MX.** The shop's email has to survive the
launch. Archive the old WordPress site completely before it goes dark; that
archive is the last copy of it that will ever exist.
