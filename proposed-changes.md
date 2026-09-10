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

### 1.12 The orphaned connective

| | |
|---|---|
| **Before** | **That's why** our family-owned shop has served drivers across Bucks County and Montgomery County for years, delivering expert collision repair with genuine care. |
| **After** | Our family-owned shop has served drivers across Bucks County and Montgomery County for years, delivering expert collision repair with genuine care. |

Fallout from the 1.5 split. "That's why" pointed back at a sentence that is
now in the hero, so it opened a section by referring to something the reader
had scrolled past. The connective is dropped rather than the antecedent
restored, because the hero sentence still carries the reason and repeating it
would be worse.

### 1.13 The process paragraph becomes six steps

**Before**, one paragraph of about 180 words:

> We've refined our collision repair process over years of experience to make
> sure you get back on the road with confidence. It all starts with a free
> estimate. You can request one online or give us a call at (215) 322-5350.
> Once you're ready to move forward, we take care of the insurance
> coordination so you're not juggling calls with adjusters. Our team performs
> a thorough damage assessment and creates a detailed repair plan that we walk
> you through. Using state-of-the-art equipment and factory-certified
> techniques, our ASE/I-CAR Gold technicians perform precision repairs to
> manufacturer standards. After the structural and cosmetic work is complete,
> we don't just hand you the keys; we run a full quality control inspection to
> ensure everything meets our standards. Then comes the detail: we thoroughly
> clean the interior and exterior, making your vehicle look as good as it
> runs. Finally, we walk through the finished work with you, answer any
> questions, and make sure you're completely satisfied. From start to finish,
> we handle the heavy lifting so you can focus on getting back to your life.

**After**: the first sentence is the lead-in, the last sentence is the closing
line, and the eight sentences between them are six numbered steps, split at
their own sentence boundaries. **Not one word changed, and not one sentence
moved out of order.** Step 6 carries two sentences, the detail and the
walkthrough, because they are one handover.

**Six step titles are new text.** Each is lifted from the words inside its own
step, so none of them is a new claim:

| Step | Title | Lifted from |
|---|---|---|
| 01 | The free estimate | "It all starts with a free estimate" |
| 02 | Insurance coordination | "we take care of the insurance coordination" |
| 03 | Damage assessment and repair plan | "a thorough damage assessment and creates a detailed repair plan" |
| 04 | Precision repairs | "perform precision repairs to manufacturer standards" |
| 05 | Quality control inspection | "we run a full quality control inspection" |
| 06 | Detail and walkthrough | "Then comes the detail" / "we walk through the finished work with you" |

### 1.14 Minor and Major become side-by-side cards, with subheads

The two blocks are now two cards standing next to each other so a reader can
tell at a glance which one is theirs. The text inside each is the live page's,
unchanged and in order, chunked under subheads.

**Seven subheads are new text**, and every one is a label rather than a claim:

- Minor: **What counts as minor** / **How we fix it** / **Why not to wait**
- Major: **What counts as major** / **Who does the work** / **The parts we use** /
  **Safety systems and warranty**

**One new H2 is added**, "Minor and Major Collision Repair", to head the pair.
On the live page the two H3s float under the process heading with no parent of
their own.

### 1.15 The "three critical things" sentence becomes three cards

| | |
|---|---|
| **Before** | Why does this matter to you? Because factory certification ensures three critical things: your vehicle's warranty protection isn't compromised, your vehicle's safety systems work exactly as designed, and your vehicle's resale value is protected. |
| **After** | Why does this matter to you? Because factory certification ensures three critical things: <br>• Your vehicle's warranty protection isn't compromised. <br>• Your vehicle's safety systems work exactly as designed. <br>• Your vehicle's resale value is protected. |

Three clauses become three cards. The only change is a capital letter and a
full stop on each. No words added, none dropped.

### 1.16 The proof band became a stat band

Superseded 2026-09-06, when the photographic direction was picked. The band
under the hero is now **three stats**, not four badges and a chip row.

**The ORDER below is superseded again by 1.20, on 2026-09-10.** The three
stats and their words are unchanged; the warranty now leads.

| Stat | Label | Supporting line |
|---|---|---|
| **12** | Vehicle brands, factory-certified | INFINITI, Nissan, Hyundai, Kia, Acura, Honda, GM, Chrysler, Ford, Dodge, Subaru and Jeep. |
| **274** | Google reviews | **4.9 stars on Google, counted on September 10, 2026.** |
| **Lifetime** | Warranty on all repair work | If anything isn't right, we'll make it right. |

**Three, not four, and the third is a word.** There is no fourth honest number
to put in a four-across row, and inventing one to balance a layout is the exact
failure the prime law exists to stop.

**The review count now carries the date it was true**, which it did not before.
That is a partial answer to 4.4, not the whole one: dating it stops it lying
silently, but somebody still has to decide between a dated number and a live
widget, and re-date it if it stays static.

The four claims themselves did not leave the page. ASE and I-CAR Gold, the
lifetime warranty and free estimates are now three chips in the hero panel, and
each is also stated at length further down: the certifications in FAQ 6 and the
Major card, the warranty in the Major card and the Why Choose list, free
estimates in FAQ 4 and the Why Choose list.

**Two label lines I had written are retired**, and both were my recombinations
rather than the live page's sentences: "Automotive Service Excellence, held by
our technicians" and "Online and by phone. No obligation and no surprises." The
underlying claims are still on the page in the live site's own words.

### 1.17 The four customer quotes are migrated verbatim

The live page's testimonials carousel is now four quote cards on an ink band.
**The quotes are byte-for-byte what the live site publishes**, which includes
one typo ("The were great about sending e-mail updates"), two emoji, and some
loose punctuation. A testimonial is somebody else's words, and tidying one is
not a style fix. See 4.8 for what needs confirming about them.

### 1.18 A fourth hero chip: the insurance paperwork

**Flagged for the owner's pass as a new visible promise**, even though it is
not a new fact.

| | |
|---|---|
| **Before** | ASE and I-CAR Gold certified &nbsp;•&nbsp; Lifetime warranty &nbsp;•&nbsp; Free estimates |
| **After** | ASE and I-CAR Gold certified &nbsp;•&nbsp; Lifetime warranty &nbsp;•&nbsp; Free estimates &nbsp;•&nbsp; **Insurance paperwork handled** |

The claim is already on the page three times, in the live site's own words:
the Why Choose list ("Works with all major insurance companies. We handle the
paperwork and communication so you don't have to."), step 02 of the process
("we take care of the insurance coordination so you're not juggling calls with
adjusters"), and the insurance FAQ ("We handle all the paperwork, coordinate
authorizations, and keep your insurer updated on repair progress."). So this
is a placement, not an invention, and the migration rule holds: the page still
claims nothing the live page does not.

**Why it is flagged anyway.** A hero chip is the loudest, shortest, most
quotable form a claim takes on this page, and it is what an assistant lifts
first. "Insurance paperwork handled" reads as an unconditional promise in a way
that the three sentences it compresses do not, and rule 2 says the site may
only sell what the shop actually does. **The question for the owner is scope,
not truth: is the paperwork handled for every insurer and every claim, or are
there carriers or claim types where the customer still files themselves?** If
there are exceptions, the chip comes off and the longer sentences stay, because
they carry their own context and the chip cannot.

Related, and already open in 4.2: whether "direct repair relationship" is the
right phrase for what the shop actually has with those insurers.

The chip's icon is the umbrella step 02 already uses for insurance
coordination. No new icon was drawn.

### 1.19 The warranty chip becomes a detailing chip, and the warranty leads the stat band

**Flagged for the owner's pass as a new visible promise**, like 1.18, and it
carries a second scope question that 1.18 does not.

| | |
|---|---|
| **Before** | ASE and I-CAR Gold certified &nbsp;•&nbsp; **Lifetime warranty** &nbsp;•&nbsp; Free estimates &nbsp;•&nbsp; Insurance paperwork handled |
| **After** | ASE and I-CAR Gold certified &nbsp;•&nbsp; **Detailed after every repair** &nbsp;•&nbsp; Free estimates &nbsp;•&nbsp; Insurance paperwork handled |

The detailing claim is already on the page twice in the live site's own words:
step 06 of the process ("Then comes the detail: we thoroughly clean the
interior and exterior") and the Why Choose list ("Vehicles detailed inside and
out after every repair"). The chip's wording is the Why Choose line compressed,
so "every repair" is the live site's own word and not an escalation of it. The
icon is the sparkles step 06 already uses. No new icon was drawn.

**THE SCOPE QUESTION, and it is the sharp one: every repair, including minor
work and glass-only jobs?** 4.2 already flags that "every" is doing real work
in the Why Choose sentence. Putting it in a hero chip strips away the sentence
around it, so the chip promises a full interior and exterior clean on a bumper
scuff and on a windshield swap as loudly as it does on a rebuild. If the honest
answer is "on any job where the car has been in the shop long enough", the chip
needs different words or it comes off, and the Why Choose sentence needs a look
at the same time.

**The lifetime warranty did not leave the page.** It now LEADS the stat band
directly below the hero, and it is still in the Major Collision Repair card,
the Why Choose list and FAQ 2. 4.1 calls it the single most load-bearing claim
on the page, and it is still the only one of the three stats that is a word
rather than a number.

**What that cost it, measured at 390 after cutover, and it is not what the
reorder was aiming at:**

| Where "Lifetime" first appears on the page | y |
|---|---|
| Before, as the second hero chip | **681** |
| After, as the stat band's leading numeral | **902** |

The stat band reorder moved its own "Lifetime" up 310px, from 1212 to 902. But
the hero chip was earlier than either of those, so dropping it cost 531px and
the word ends up **221px LOWER than it started**. It is still on screen two on
a phone, which is what the reorder was for, but it is mid screen two rather
than at the top of it. **If the warranty leading on mobile is the goal, this
change moved it the wrong way**, and the two halves want deciding separately:
the stat band reorder gains ground on its own, the chip swap gives more back.

53px of that 221 is the chip row itself, see below.

### 1.20 The stat band is reordered: Lifetime, 12, 274

Supersedes the order in 1.16. Same three stats, same words. The review count
in the table below was refreshed on 2026-09-10, separately from the reorder;
see 4.4. **Reordered in the DOM**, so the markup, the screen reader, the
tab order and every viewport agree on the sequence. No `order`, no
`row-reverse`, nothing that would make what a sighted reader sees disagree with
what the document says.

| Stat | Label | Supporting line |
|---|---|---|
| **Lifetime** | Warranty on all repair work | If anything isn't right, we'll make it right. |
| **12** | Vehicle brands, factory-certified | INFINITI, Nissan, Hyundai, Kia, Acura, Honda, GM, Chrysler, Ford, Dodge, Subaru and Jeep. |
| **274** | Google reviews | **4.9 stars on Google, counted on September 10, 2026.** |

On a phone the three stack in source order, so the warranty is the first thing
under the hero. On desktop they are three columns and the warranty is the left
one. The band's `aria-label` was updated to match: "Warranty, certifications
and reviews".

**One is a word rather than a number, and now it is the first one.** That does
not change the rule in 1.16: three, never four, and no number gets invented to
balance the row.

### 1.21 The chip row is four stacked pills on a phone now, not three rows

Not a wording change, a consequence of one, recorded because it is visible.

"Detailed after every repair" renders 232px wide where "Lifetime warranty" was
178px. At 390 the content column is 350px, so the old row two paired the
warranty chip with "Free estimates" at 342px. The new chip cannot pair with
anything:

```
    ASE and I-CAR Gold certified   244
    Detailed after every repair    232
    Free estimates                 154
    Insurance paperwork handled    257
```

Every pair of those exceeds 350 once the 10px gap is added, so **no reordering
of the four gets back to three rows**. The chip row goes from 3 rows to 4 at
390 and 430, and stays at 4 at 360. It is 53px taller, which is what pushes the
stat band from y=799 to y=852 and is 53 of the 221px in 1.19.

Nothing overflows: the widest chip ends at x=277 against a 370px content edge,
and the document scroll width is exactly the viewport at all three widths.

**The CTA pair is untouched by all of this.** The chips render after it, so the
fold numbers from 3.8 are identical before and after, at 360, 390 and 430, in
both the staging and the post-cutover state.

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
| ~~The testimonials carousel~~ | **Now carried**, as of 2026-09-06. The four quotes are migrated verbatim as quote cards on an ink band, moved up the page to sit after the insurance section. The carousel itself is not: they are four cards, all visible, no rotation. See 1.17 and 4.8. |
| The Trustindex review widget | A third-party script, and **it was wrong**: it showed 231 reviews on 2026-09-05 where the shop's own Google Business Profile showed 274 on 2026-09-10. The count is carried as one line of dated visible text instead, read from the profile. See 4.4. |
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

### 3.4 Section order, and what moved

The page keeps the live page's order for everything it carries: intro, process,
minor and major, what to do after a crash, insurance claims, factory
certification, why choose us, service area.

**Three things moved, on 2026-09-06.** A proof band was inserted after the
intro, so the certifications, the warranty, the free estimates and the twelve
brands sit high on the page where a stressed reader meets them first. The
testimonials moved up from the bottom of the live page to between insurance and
factory certification, where they answer the question the insurance section
raises. And the FAQ is the last thing before the footer, with the contact band
above it, which is the house structure every page on this site uses.

No words changed and no section was dropped in any of it. On the live page the
FAQ is followed by the blog feed, the testimonials and then the contact block;
the blog feed is the only one of those not carried, and it belongs on `/blog/`.

### 3.5 The band rhythm, and what oxblood means

Backgrounds now run: paper, ink, paper, white panel, **oxblood**, paper, ink,
paper, **oxblood**, white panel, ink, paper, ink. No two touching sections share
a ground.

**Oxblood means act and nothing else.** There are exactly two oxblood bands on
the page and each one carries the CTA row. The ink bands are structural: they
break the paper run under the proof band and the quotes, where there is nothing
to click. `docs/assets/site.css` splits this into `.dark` for the behavior and
`.field-ox` / `.field-ink` for the ground, so the two can never be confused by
someone adding a section later.

### 3.6 The hero and Minor photographs swapped places

Done 2026-09-06, with the photographic direction. The hero is now a full-bleed
photograph, and a full-bleed band needs a landscape source: the portrait
`accent-collision-repair-1.jpg` is 600px wide and was being stretched across a
1440px band.

So the two traded slots, and **their alt text travelled with them**:

| Slot | Before | After |
|---|---|---|
| Hero | accent-collision-repair-1.jpg (600x900) | accent-minor-collision-repair.jpg (1200x800) |
| Minor card | accent-minor-collision-repair.jpg | accent-collision-repair-1.jpg |

Both photographs are still on the page, once each, with the same alt text they
have always had. The Major card is untouched. `og:image` is unchanged, because
it already pointed at the image that is now the hero.

**1200px is still not enough for a full-bleed hero** on a 1440 or 1920 screen.
Whatever the answer to 4.9 turns out to be, this slot wants a file at 2000px or
better, and a body shop can shoot one in an afternoon.

### 3.7 sameAs is deliberately absent, pending the verified list

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

### 3.8 The phone hero was tightened so the CTA pair clears the fold

**No words changed.** Spacing, the photograph's band height on phones, and
the buttons' own padding. Recorded here because it is a visible change to
what a customer sees first, and because the numbers should not have to be
rediscovered.

At 390x664, which is an iPhone 12, 13 or 14 in Safari, the hero's CTA pair
ran 613 to 751 on the real page. Neither button was on screen. The fixed
call bar owns the bottom 60px of that viewport, so the usable height is 604,
not 664, and the pair was 147px past it.

After the change the pair ends at 596. Both buttons clear, at 360, 390 and
430. During staging the banner adds 57px and pushes the second button under
the call bar; the Call button still clears with 19px to spare, and the banner
comes off at cutover.

What it cost: the photograph's band on phones goes from 52vw to 36vw, 203px
to 140px at 390. It is still full-bleed and still the first thing on the
page. Above 599px nothing changed at all. The arithmetic is in the header of
`docs/assets/site.css`, and `scripts/mobile-check.md` now carries the 604px
budget and how to measure it.

**The reader could always call**, throughout. The call bar is fixed to the
bottom of every phone viewport and that is exactly what it is for. What was
wrong is that the hero asked for an action and then hid its own button.

---

## 4. The claims list

Every claim the migrated page carries. All of them come from the live site, so
none is new. That is not the same as being verified, and the prime law says an
unverified claim does not ship. **Confirm each one.**

### 4.1 Certification and warranty

- **ASE and I-CAR Gold Class certified technicians.** Stated four times on the
  page and in the hero badge strip. Certifications lapse. Confirm current.
- **Lifetime warranty on all repair work.** Leads the stat band as of
  2026-09-10, and is in the Major Collision Repair copy, the Why Choose list
  and FAQ 2. It is no longer a hero chip; see 1.19 for what that cost its
  position on a phone. **Lifetime of what, covering what, transferable to a new
  owner or not?** This is the single most load-bearing claim on the page.
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
  real work in that sentence, and **now also a hero chip**, "Detailed after
  every repair", which is the strongest form the claim takes anywhere on the
  page. **Does it include minor work and glass-only jobs?** See 1.19.
- **Environmentally friendly repair products** throughout the repair process.
- **State-of-the-art equipment and facilities.**
- **Direct repair relationships with all major insurance companies.** A "direct
  repair relationship" is a specific arrangement, not a synonym for accepting
  insurance. Confirm it is the right phrase.
- **The shop handles the insurance paperwork.** In the Why Choose list, step 02
  and the insurance FAQ, and **now also a hero chip**, which is the strongest
  form the claim takes anywhere on the page. Every insurer and every claim, or
  are there exceptions? See 1.18.
- **We advocate with the insurer for more extensive repairs** than the adjuster
  approved.
- **Loaner or rental coordination** where the policy provides for it (FAQ 1).

### 4.3 Timelines

- **Minor repairs typically 2 to 5 days.**
- **Major structural work 2 to 4 weeks.**

Both are in FAQ 1 and both are the kind of number a customer will hold the shop
to.

### 4.4 The rating and the review count, refreshed 2026-09-10

**Current, and on the page now:**

| | |
|---|---|
| **Before** | **231** Google reviews — "Rated Excellent, as of September 2026." |
| **After** | **274** Google reviews — "4.9 stars on Google, counted on September 10, 2026." |

Read off the shop's **own Google Business Profile on 2026-09-10** by Greg Quinn
of Corcoran Communications, **the vendor**. The standards make the client-owner
the fact-checker of record, so this is the same deliberate vendor-confirmation
exception the NAP carries, and it is recorded as one here and in
`scripts/audit.py`. **Owner sign-off is still outstanding.**

**"Rated Excellent" is retired.** It was the Trustindex widget's adjective. 4.9
is the profile's own number, it is first-party, and it says more in less space.
An adjective a third-party script chose is the weakest form of a rating claim
available.

#### The widget and the profile disagreed by 43 reviews in the same week

This is the finding, and it is the argument for the decision below.

```
2026-09-05   Trustindex widget on the live site      231 reviews
2026-09-10   the shop's Google Business Profile      274 reviews
```

Five days apart. A shop of this size does not take 43 Google reviews in five
days, so **the widget was not merely behind, it was wrong**, and it was wrong
in the direction that undersells the shop by 16%. Nobody would have caught that
by eye, because a widget that renders a number looks authoritative in exactly
the way a number typed into HTML does not.

**So the widget does not come through cutover.** A third-party script that is
wrong about the shop's own numbers is worse than a dated line of text that is
right: it costs a request, it hands a vendor control of a claim the shop is
accountable for, and it fails silently. See section 2, where the widget is
already listed as not carried.

#### What is now mechanism rather than memory

`scripts/audit.py` holds `REVIEW_COUNT`, `REVIEW_RATING` and
`REVIEW_COUNTED_ON`, and a site-wide check that:

- reads **every visible review-count mention under `docs/`**, across `.html`
  and `.txt`, with comments and scripts stripped so a comment recording the old
  number is history rather than a contradiction;
- **fails as a critical if any two disagree**, counting the recorded
  `REVIEW_COUNT` as one of the instances, so a single page that drifts is
  caught even when nothing else on the site contradicts it;
- **warns once the count is more than 35 days old**, because past that the
  number is not known to be wrong, it is only no longer known to be right.

`--strict` now exits 1 on a site-wide critical too. It only read per-page
scores before, because there had never been a site-wide critical to raise, so
one would have printed a red heading and exited 0. `scripts/test-audit-checks.py`
section 13 holds the cases, including the two-spans markup shape, the comment
that must not count, the 35 and 36 day boundary, and a date in the future.

#### Still open, and still the owner's

1. **Refresh or go live.** A dated number goes stale honestly rather than
   silently, but it still goes stale. The 35-day warning sets the pace; the
   decision between re-reading the profile on that clock and putting something
   live on the page is the owner's.
2. **No rating or review markup is in the schema, deliberately**, and none gets
   added on the strength of this. Google's own guidelines rule out self-serving
   review markup on a business's own site, and the standards allow none unless
   the data is real and the owner has decided to publish it. Both halves are
   checked: the count for agreement, the schema for absence.

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

### 4.8 The four customer quotes

Carried verbatim from the live page. They are already published there, which is
not the same as being cleared to republish. Four things to confirm:

1. **Permission.** Reviews are the ranking engine and these are real, but a
   quote attributed to a named person is that person's words. Confirm the shop
   has permission to republish each one.
2. **Three staff members are named**: Kevin Bliss, Barry and Victor. A
   testimonial praising someone who has left is a small trap, and a customer
   who asks for them by name and finds them gone is a worse one. Confirm all
   three still work here. The live page's review widget also names Armando and
   Justin, neither of whom is in these four quotes.
3. **An insurer is named** (Nationwide) and **a customer's business is named**
   (Apex Heating). Both are third parties on somebody else's website.
4. **They ship exactly as written**, typo and emoji included. If the owner
   would rather not publish the loosest of the four, the answer is to drop it
   whole, never to tidy it.

**No `Review` or `AggregateRating` markup is in the schema** and none should be
added on the strength of these. Rating markup needs real, owned, publishable
data and an owner who has decided to publish it.

### 4.9 The photographs, and this one is a cutover blocker

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

Since 2026-09-06 the hero is a full-bleed photograph, which raises the stakes
on the answer: a stock photo at the top of the page at 1440px wide is a much
louder mistake than a stock photo in a card. That slot also needs a file at
2000px or better regardless of the answer. See 3.6.

---

## 5. What the owner needs to answer first

Ordered by how much else depends on it.

1. **The business name.** What does the Google Business Profile say? Everything
   after this page inherits the answer. See 1.1.
2. **The email.** `contact@` is published; the live footer also shows `info@`.
   Which does the shop read, and does the other forward? See section 2.
3. **The photographs.** Shop's own, or stock? See 4.9.
4. **ADAS recalibration in-house, yes or no.** It settles this page's copy and
   the ADAS page's gate at once. See 4.2.
5. **The warranty**, in the owner's own words: lifetime of what, covering what,
   transferable or not. See 4.1.
6. **The rating**: live widget, dated number, or nothing. See 4.4.
7. **1974 and second generation**: publish them or not. See 4.5.
8. **priceRange**: publish `$$` or not. See section 2.
9. **The four customer quotes**: permission to republish, and whether the
   staff they name still work here. See 4.8.
10. **The verified `sameAs` list.** See 3.7.
