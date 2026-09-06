# Proposed changes, awaiting the owner's fact-check

Every text change made during the migration, as before/after pairs, plus every
claim the migrated pages carry. Nothing in here is settled. The standards make
the **client-owner the fact-checker of record**, and this file is how that role
gets exercised: read it, say yes or no to each line, and anything that gets a
no comes off the page.

**Status: 1 page migrated.** `/collision-repair/`, built 2026-09-05 from
`https://tricountycollision.com/collision-repair/` read the same day.

The rule this migration ran on: the live page is the content source of record,
no fact was invented, and the new page claims nothing the old page does not
already claim. Where wording changed, it is below.

---

## 1. Before and after

### 1.1 The business name, 5 changes on this page

| | |
|---|---|
| **Before** | Tri County Collision Center |
| **After** | Tri-County Collision |

Changed in the page title, the hero lead, step 8 of the accident checklist,
the "Why Choose" heading, and FAQ 5. `CLAUDE.md` records `Tri-County Collision`
as the canonical name and `scripts/audit.py` holds it in its NAP block.

**This one needs a decision before anything else, because three spellings are
in play right now:**

- `Tri-County Collision` is on the logo and in this repo's NAP block.
- `Tri County Collision Center` is the `name` in the live site's schema, its
  `og:site_name`, and most of its body copy.
- `Tri County Collision` is the live page title's suffix.

Rule 6 says the name is character-identical everywhere, site, schema, Google
Business Profile and every directory, and that the name field takes the real
business name with nothing appended. **Whatever the Google Business Profile
says is the answer**, and the site follows it rather than the other way round.
If GBP says "Tri County Collision Center", this repo's NAP block changes and
these five edits are reverted. Check it before the second page is built, because
every page after this one inherits the answer.

### 1.2 FAQ 1, opening sentence

| | |
|---|---|
| **Before** | The timeline depends on the severity of the damage. |
| **After** | How long collision repair takes depends on the severity of the damage. |

The FAQ law's standalone test: an assistant lifts the opening sentence without
the question. "The timeline" then has no antecedent. Echoing the question's own
words fixes it and strengthens the match. Nothing after this sentence changed.

### 1.3 FAQ 2, opening sentences

| | |
|---|---|
| **Before** | Absolutely. That's our standard. |
| **After** | Yes, your car will look the same after collision repair, and that is our standard. |

A bare "Absolutely." fails the standalone test outright, and "That's our
standard" carries an ambiguous antecedent once the question is gone. The two
sentences are comma-merged into one that is true when lifted alone. Nothing
after this changed.

### 1.4 FAQ 5, opening sentences

| | |
|---|---|
| **Before** | Yes, absolutely. Pennsylvania law protects your right to choose your own collision shop for repairs. |
| **After** | Yes, Pennsylvania law protects your right to choose your own collision shop for repairs. |

Same rule, smallest possible fix: "absolutely." is deleted and the "Yes" is
merged into the sentence that already carried the whole answer.

### 1.5 The opening paragraph, split, no words changed

The live page's first paragraph runs about 200 words. Its first two sentences
are now the hero lead and the rest is the paragraph under the H2. Every
sentence survives, in its original order and wording. Split only.

### 1.6 A typo

| | |
|---|---|
| **Before** | paintless dent repair (PDR) , which removes minor dings |
| **After** | paintless dent repair (PDR), which removes minor dings |

A space before the comma, left behind when the live page's link was closed.

### 1.7 The contact heading

| | |
|---|---|
| **Before** | Contact Us for Your Free Consultation |
| **After** | Contact Us for Your Free Estimate |

Everywhere else on the page, including the FAQ, the offer is a free estimate.
"Consultation" is the only place it is called something else, and a shop that
offers one thing should call it one thing. **If the shop does offer a
consultation that is distinct from an estimate, say so and this reverts.**

### 1.8 Alt text, 3 changes

| Image | Before | After |
|---|---|---|
| Major collision repair | `accent-major-collision-repair` | Technician grinding metal beside a vehicle with its front bumper and headlight assembly removed for major collision repair. |
| Minor collision repair | Final collision repair touch-ups being completed on a **grey** automobile. | Final collision repair touch-ups being completed on a **black** automobile. |
| Logo | `Tri-County-Collision-Logo-Horizontal-new` | Tri-County Collision |

Two of these were filenames rather than descriptions, which is what a screen
reader would have read aloud. The third describes a grey car; the car in the
photograph is black.

### 1.9 Button labels

| | |
|---|---|
| **Before** | Call Now for a Free Quote |
| **After** | Call (215) 322-5350 |

The number is now visible on the button and tappable, which is the point of
the button. **"Get an Estimate Online" is dropped from every CTA row for now**
and replaced with "Email the shop", because the form it pointed at does not
exist yet. It comes back when `/contact-us/` ships with the shop's own form
endpoint. See 3.2.

### 1.10 The footer year

| | |
|---|---|
| **Before** | © 2023 Tri County Collision Center. All Rights Reserved. |
| **After** | © 2026 Tri-County Collision (updated by script each January) |

A copyright line three years stale is a stale-clock signal to a reader deciding
whether anyone still runs this business. The markup carries a real year so it
is right with JavaScript off, and the script keeps it right after that.

### 1.11 Typographic normalization, no words changed

Curly apostrophes and quotes are straight ASCII throughout, on the page and in
the schema. The live page used curly in its visible copy and straight in its
JSON-LD, which alone would break the mirror law: the FAQ answers have to be
byte-identical in both places, and a curly apostrophe is a different byte.

---

## 2. What the live page carries that this page does not

None of these is a wording change. Each is a thing deliberately not carried,
and each is reversible.

| Not carried | Why |
|---|---|
| The CallRail number, (215) 709-9665, in the header | It is a tracking number. CallRail swaps numbers in visually at runtime, so the source keeps one phone number. The snippet is added at cutover. `scripts/audit.py` fails any page carrying it. |
| `info@tricountycollision.com` in the footer | The live page prints two email addresses, `contact@` in its schema and contact block and `info@` in its footer. One business publishes one mailbox. **Which one the shop actually reads, and whether the other should forward, is an open question for the owner.** |
| `priceRange: "$$"` in the schema | The standards allow no price, offer, review or rating markup unless the data is real and the owner has decided to publish it. `$$` is a claim about what the shop costs. **Owner decision: publish it or not.** |
| `hasOfferCatalog` with two `Offer` nodes | Same rule. The two services it lists, minor and major collision repair, are on the page as prose instead. |
| The blog feed, ten posts with excerpts | It belongs on `/blog/`, per the page map. |
| The testimonials carousel | Four named testimonials. Reviews are a ranking engine and these are real, but they are a site-wide module and they need a decision about where they live. **Owner decision.** |
| The Trustindex review widget | A third-party script. The rating it displays is carried as one line of visible text instead. See 4.4. |
| The link on "paintless dent repair (PDR)" | `/paintless-dent-repair/` has not been built. This site never writes a link to a page that does not exist, and `scripts/test-audit-checks.py` fails the build on one. It goes back when the page lands. |
| The link in FAQ 5 to the anti-steering blog post | Same reason. The sentence stays; only the link waits. |
| The rollover image pair | The live page's "Major Collision Repair" photo is a hover swap between two files. One image, shown always. |
| The duplicate navigation | WordPress rendered the whole nav twice, once for desktop and once for mobile. |
| `foundingDate: 1974`, `slogan`, `naics`, `alternateName`, `knowsAbout`, the `additionalProperty` block | Real claims from the live schema, none of them needed on a service page's business node. **Several are strong and should probably go on the homepage**: see 4.6. |

---

## 3. Migration notes

### 3.1 The address is spelled two ways on the live page, right now

The live `/collision-repair/` page prints **`995 Jaymor Rd`** in its footer and
in its body copy, and **`995 Jaymor Road`** in its `PostalAddress` JSON-LD. Same
page, same business, two spellings.

That is not cosmetic. Each variant reads as a slightly different business to
Google's entity matching, which is how a shop ends up competing with itself in
the Map Pack. **The new site carries `995 Jaymor Rd` in both places by
construction**: `scripts/audit.py` fails any page that spells it another way,
the trailing period in `Rd.` included, and `scripts/test-audit-checks.py` holds
the same-page case, canonical spelling and variant together on one page, as a
permanent test.

**Check the Google Business Profile.** Whichever spelling GBP uses is the one
the site should use, and if GBP says "Road" then this repo's NAP block changes
rather than the profile.

### 3.2 Two sentences depend on a form that does not exist yet

The migrated copy says "You can request an estimate online" (FAQ 4), "or get
started online" (the opening paragraph), and "or request a free estimate
online" (Minor Collision Repair). All three are true of the business today,
because the live site has that form.

**They stop being true if `/contact-us/` ships without one.** The old intake
form is retired and the new one posts to an endpoint in the shop's own account.
Either the form ships at cutover or these three sentences come out.

### 3.3 The page map's word count is about 40% high

`pagemap.md` says this page is "~4,100 words". The page's own content, H1
through the last FAQ answer, is **2,437 words**. The difference is WordPress
chrome counted as content: the navigation rendered twice, the ten-post blog
feed with excerpts, the testimonials carousel and the review widget.

The migrated page is 2,623 words including its own headings, nav and footer, so
**nothing is missing**. The map's number should be corrected before it is used
to judge whether the other pages migrated completely, because "~1,670 words" and
"~1,525 words" on the sibling rows were almost certainly measured the same way.

### 3.4 Section order, and the one section that moved

The migrated page keeps the live page's section order exactly: intro, process,
minor, major, what to do after a crash, insurance claims, factory certification,
why choose us, service area. **One block moved.** The FAQ is now the last thing
before the footer, and the contact band sits above it, which is the house
structure every page on this site uses. On the live page the FAQ is followed by
the blog feed, the testimonials carousel and then the contact block, and the
first two of those are not carried at all.

No words changed and no section was added or dropped in the reorder.

### 3.5 sameAs is deliberately absent, pending the verified list

The business node ships with no `sameAs`, so the audit reports one warning and
the page scores 95/100 rather than 100. That is honest and it is the only gap.

The live site publishes five, listed here so the verification has somewhere to
start. A `sameAs` claims "this profile is us", so **only profiles the shop
actually controls belong in it**:

```
https://share.google/OPqWctAlZ4ik95HVj                 (Google Business Profile)
https://www.facebook.com/p/Tri-County-Collision-Center-100037804906604/
https://www.yelp.com/biz/tri-county-collision-center-southampton
https://www.linkedin.com/company/tri-county-collision-center/
https://www.carwise.com/auto-body-shops/tri-county-collision-center-southampton-pa-18966/481195
```

The last two are the ones to look at hardest: directory profiles are often
auto-generated and unclaimed, and a wrong existing listing is a worse problem
than a missing one.

---

## 4. The claims list

Every claim the migrated page carries. All of them come from the live site, so
none is new. That is not the same as being verified, and the prime law says an
unverified claim does not ship. **Confirm each one.**

### 4.1 Certification and warranty

- **ASE and I-CAR Gold Class certified technicians.** Stated four times on the
  page and in the hero badge strip. Certifications lapse. Confirm current.
- **Lifetime warranty on all repair work.** In the hero badges, the Major
  Collision Repair copy, the Why Choose list and FAQ 2. **Lifetime of what,
  covering what, transferable to a new owner or not?** This is the single most
  load-bearing claim on the page.
- **Factory-certified for 12 vehicle brands**: INFINITI, Nissan, Hyundai, Kia,
  Acura, Honda, GM, Chrysler, Ford, Dodge, Subaru, Jeep. The page also says
  "12+" in two places while the list has exactly 12. Confirm the number and the
  list, and pick one of "12" or "12+".

### 4.2 Scope of work

Rule 2, scope honesty. For each of these the question is not "is it plausible"
but "do you actually do this":

- **ADAS recalibration, in-house, after major repairs.** The page says "we also
  perform ADAS recalibration". `pagemap.md` gates the whole ADAS calibration
  page on the owner confirming calibration happens in-house, so **this page
  already makes the claim the other page is gated on.** If the answer is that
  it is sublet, this sentence changes and the ADAS page is settled at the same
  time.
- **Frame straightening and structural repair.**
- **Computerized color matching** (FAQ 2).
- **Paintless dent repair**, offered for qualifying dents.
- **Vehicles detailed inside and out after every repair.** "Every" is doing
  real work in that sentence.
- **Environmentally friendly repair products** throughout the repair process.
- **State-of-the-art equipment and facilities.**
- **Direct repair relationships with all major insurance companies.** A "direct
  repair relationship" is a specific arrangement, not a synonym for accepting
  insurance. Confirm it is the right phrase.
- **We advocate with the insurer for more extensive repairs** than the adjuster
  approved.
- **Loaner or rental coordination** where the policy provides for it (FAQ 1).

### 4.3 Timelines

- **Minor repairs typically 2 to 5 days.**
- **Major structural work 2 to 4 weeks.**

Both are in FAQ 1 and both are the kind of number a customer will hold the shop
to.

### 4.4 The rating, which is a point-in-time number

The hero badge reads **"Excellent, based on 231 reviews"**, migrated from the
live page's Trustindex widget, which reads Google.

Two decisions:

1. **It is a static number in static HTML.** It was true on 2026-09-05 and it
   is quietly wrong every week after that. Either it stays a live widget, or it
   gets a "as of" date, or it comes off. A number that decays silently is a
   stale-clock claim and the standards name it as a defect.
2. **No rating or review markup is in the schema, deliberately**, and none
   should be added on the strength of a widget. Rating markup needs real,
   owned, publishable data and an owner who has decided to publish it.

### 4.5 Ownership and history

- **Family owned and operated, not a chain or a franchise.**
- **"has served drivers across Bucks County and Montgomery County for years."**
  Migrated exactly. The live schema says the shop has been in Southampton
  **since 1974** and is in its **second generation**, and neither is used on
  this page. Both are much stronger than "for years". **If they are confirmed,
  say them**: "for years" is the weakest true version of a genuinely good fact.

### 4.6 Facts in the live schema, confirmed and available, not yet used

Candidates for the homepage rather than a service page, listed so they are not
lost: founded 1974, second generation, family owned, all major insurance
accepted with direct claim coordination, free in-person estimates and online
photo estimates, foreign and domestic cars, trucks, commercial and fleet
vehicles.

### 4.7 Contact facts carried into the schema

- **Geo coordinates** 40.1660232, -75.0538596. Migrated from the live schema.
  `CLAUDE.md` lists coordinates as unconfirmed, so this is a migrated published
  value, not a confirmed one. Check it drops a pin on the building.
- **Hours**: Monday to Friday 8 a.m. to 6 p.m., Saturday by appointment only.
  Must match the Google Business Profile exactly.
- **hasMap**, the `share.google` link, migrated from the live schema.

### 4.8 The photographs, and this one is a cutover blocker

Three photographs are carried onto this page, all from the live site:
`accent-collision-repair-1.jpg`, `accent-minor-collision-repair.jpg` and
`accent-major-collision-repair.jpg`.

**All three look like stock photography.** None shows the shop's building,
signage, or anyone identifiable as its staff, and the live site's blog images
are named `AdobeStock_*.jpeg`, so the site demonstrably uses stock elsewhere.

The standards are not ambiguous: real photos only, the owner, the shop, the
work, no stock and no AI imagery. A firm that tells clients real beats stock
has to live by it, and a collision shop has the easiest photographs in the
world to take: the bays, the frame rack, the paint booth, a finished car, the
people who did it.

They are carried today because the migration is faithful and because staging is
not public. **Confirm each one is the shop's own work, or replace it before
cutover.** This is the only item on this list that should stop a launch.

---

## 5. What the owner needs to answer first

Ordered by how much else depends on it.

1. **The business name.** What does the Google Business Profile say? Everything
   after this page inherits the answer. See 1.1.
2. **The email.** `contact@` is published; the live footer also shows `info@`.
   Which does the shop read, and does the other forward? See section 2.
3. **The photographs.** Shop's own, or stock? See 4.8.
4. **ADAS recalibration in-house, yes or no.** It settles this page's copy and
   the ADAS page's gate at once. See 4.2.
5. **The warranty**, in the owner's own words: lifetime of what, covering what,
   transferable or not. See 4.1.
6. **The rating**: live widget, dated number, or nothing. See 4.4.
7. **1974 and second generation**: publish them or not. See 4.5.
8. **priceRange**: publish `$$` or not. See section 2.
9. **The verified `sameAs` list.** See 3.5.
