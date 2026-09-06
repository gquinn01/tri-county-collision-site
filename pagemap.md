# Tri-County Collision: Page Map (build spec)

*Extracted 2026-09-03 from the Tri-County plan by the strategy chat, for this repo. This is the page map of record for the build; CLAUDE.md and docs/README.md point here. This repo is public, so the full plan, pricing, and client notes stay out of it; this file carries only what the build needs.*

## Rules that govern every row

Every page ships at 100/100 strict. Content that ranks migrates faithfully rather than being rewritten for its own sake. Existing slugs are kept wherever a page keeps its purpose, because the promise of this migration is that rankings survive, and every unnecessary redirect spends a little of that. A clone or plumbing URL gets a 301 to the page it copies or an honest 404, never a forced mapping to a sales page.

No page ships copy from this file. Facts come from the truth inventory; the client-owner is fact-checker of record; every text change is presented propose-first as before/after pairs and approved before it lands.

**The email, decided 2026-09-05.** Where a row says "one email", that email is `contact@tricountycollision.com`. It is the address the live site publishes in its schema and in the contact block on every service page. The live footer's `info@` address is not published here. This is a vendor decision by Corcoran, recorded as the same deliberate exception the rest of the NAP is recorded as, and owner sign-off is still outstanding. `scripts/audit.py` now enforces both halves: the published address, and a critical on any page carrying the other one.

**The CallRail number never reaches the source.** (215) 709-9665 is a call-tracking number. It does not go in the HTML, the schema, the template or a comment, on any page. CallRail swaps numbers in visually at runtime, so the source says (215) 322-5350 and always will. The snippet is added at cutover. `scripts/audit.py` fails any page that carries the tracking number.

## The map

| New page | Source | Treatment | Old URLs that 301 here |
|---|---|---|---|
| Home | / | Migrate proof and structure; add a real FAQ (5 to 7 questions from the phone log, owner supplies); one email, one phone; footer year | /auto-repair-shop-southampton-pa/, /car-repair-shop-southampton-pa/ |
| Collision repair | /collision-repair/ | Migrate ~4,100 words and 7 FAQs; fix standalone-test answer openers; FAQPage schema mirrored to the visible text | /auto-body-repair/, /body-shop-southampton/ |
| Commercial collision repair | /commercial-collision-repair/ | Migrate ~1,670 words and 6 FAQs; fix answer openers; meta to 160 | /collision-repair-copy-copy/ |
| Auto glass | /auto-glass-repair-replacement/ | Migrate ~1,525 words and 6 FAQs; add the FAQPage schema it lacks | /auto-glass-repair-replacement-copy/ |
| Paintless dent repair | /paintless-dent-repair/ | Migrate ~1,520 words; check for a visible FAQ and mirror it | none |
| ADAS calibration | new, candidate | Build only if Keyword Planner shows demand and the owner confirms calibration is done in-house. Source material: the glass page's in-house statement and the ADAS blog post, which stays a post and links here | none |
| Areas we serve (hub) | /areas-served/ | Migrate ~2,500 words and 4 FAQs; add Jamison to the county lists; title to 60, meta to 160 | none |
| 11 finished town pages | /areas-served-collision-repair-*/ | Migrate each with its own FAQ mirrored; fix the Bensalem drive-time contradiction; two titles trimmed to 60, one meta to 160. Gate: a town keeps its page unless Search Console shows no impressions for it over the last 12 months, in which case it folds into the hub and its URL 301s there | none, slugs kept |
| Jamison | /areas-served-collision-repair-jamison-pa/ | Rebuild to the sibling standard: directions, named roads, own FAQ; owner supplies the local facts, never invented. Same gate as the other towns | /body-shop-jamison/, /paintless-dent-repair-jamison/ |
| Contact | /contact-us/ | Migrate; add the missing meta; one email, one phone; form on an endpoint the client owns. This page is now the only intake form on the site | /customer-information/ |
| Privacy | new | Required from day one; the forms need it | none |
| Blog index | /blog/ | Migrate; add H1 and meta | /category/collision-repair/, /category/news/ |
| 16 posts | existing slugs | Migrate; titles to 60 and metas to 160, machine-counted, promise words kept; alt text; slugs kept | none |
| Customer information form | /customer-information/ | **RETIRED, decided 2026-09-05.** The page carried a third-party intake form the shop does not own. We build our own form, on an endpoint the client owns, and the one place to reach the shop from the web is Contact. The URL 301s to /contact-us/, which is a genuinely equivalent destination: it is where a customer goes to send the shop their details | (this URL redirects out, see the right-hand column of Contact) |
| Thank-you page | /thanks/ | Keep, noindexed, with an H1; it is the GA4 form_submit key event, and the new form's success state is what sends the reader here | none |

## Counts

37 indexable pages without ADAS (home, 4 services, hub, 12 towns, contact, privacy, blog index, 16 posts), 38 with it, plus 1 noindexed utility page, the thank-you page. Eleven old URLs redirect: the 8 clones to their canonical targets, the 2 category archives to the blog index, and /customer-information/ to /contact-us/. The old sitemap's 48 entries become 37 or 38, all real.

The customer-information page moved from the utility column to the redirect column on 2026-09-05, when the intake form was retired. It is the second count these numbers have carried, so the arithmetic is spelled out rather than left to be re-derived: one utility page, eleven redirects.

## Redirect discipline

The map is written before the build starts and tested against the old site's full URL list: the sitemap, anything Search Console has ever shown, and the old-site archive's link graph. Every entry names an equivalent page or is an honest 404. Archive the old WordPress site completely before it goes dark; it is the last copy. At cutover, change web DNS records only, never MX.
