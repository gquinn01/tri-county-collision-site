# Proposed changes, awaiting the owner's fact-check

Every text change made during the migration, as before/after pairs, plus every
claim the migrated pages carry. Nothing in here is settled. The standards make
the **client-owner the fact-checker of record**, and this file is how that role
gets exercised: read it, say yes or no to each line, and anything that gets a
no comes off the page.

**Status: 5 pages migrated.** `/collision-repair/`, built 2026-09-05, `/`,
built 2026-09-10 from `https://tricountycollision.com/` read the same day, and
`/auto-glass-repair-replacement/` (3.47), `/paintless-dent-repair/` (3.48) and
`/commercial-collision-repair/` (3.49), all built 2026-09-24 from their live
pages read the same day.

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

### 1.20 The stat band is reordered: Lifetime, 274, 12

Supersedes the order in 1.16. Same three stats, same words. The review count
in the table below was refreshed on 2026-09-10, separately from the reorder;
see 4.4. **Reordered in the DOM**, so the markup, the screen reader, the
tab order and every viewport agree on the sequence. No `order`, no
`row-reverse`, nothing that would make what a sighted reader sees disagree with
what the document says.

| Stat | Label | Supporting line |
|---|---|---|
| **Lifetime** | Warranty on all repair work | If anything isn't right, we'll make it right. |
| **274** | Google reviews | **4.9 stars on Google, counted on September 10, 2026.** |
| **12** | Vehicle brands, factory-certified | INFINITI, Nissan, Hyundai, Kia, Acura, Honda, GM, Chrysler, Ford, Dodge, Subaru and Jeep. |

On a phone the three stack in source order, so the warranty is the first thing
under the hero. On desktop they are three columns and the warranty is the left
one. The band's `aria-label` names the same sequence.

**Reordered again 2026-09-10**, to Lifetime, 274, 12: the review count moves to
second and the brand count to third. Same three stats, same words, same DOM
rule. The `aria-label` follows to "Warranty, reviews and certifications".

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

### 1.22 The Minor card named one county where the page claims two

| | |
|---|---|
| **Before** | They're a normal part of driving, especially around the busy neighborhoods of Bucks **County**. |
| **After** | They're a normal part of driving, especially around the busy neighborhoods of Bucks **and Montgomery County**. |

**Consistency, not new scope.** The shop sits on the county line, and every
other place the page states its geography already claims both. Checked rather
than assumed, and this was the only sentence naming one alone:

```
meta description        Bucks & Montgomery County
og:description          Bucks & Montgomery County
schema areaServed       Bucks County, Pennsylvania / Montgomery County, Pennsylvania
H2, after a crash       What to Do After a Car Accident in Bucks & Montgomery County
Why Choose list         serving Bucks and Montgomery Counties
H2, serving areas       Collision Repair Serving Bucks County and Montgomery County
serving-areas copy      the greater Bucks County and Montgomery County areas
footer                  Bucks County, Montgomery County and Northeast Philadelphia
Minor card              Bucks County                                  <- the odd one
```

So the change closes a gap rather than opening a claim. The service area
itself is unchanged, and nothing here adds a town, a route or a radius.

**One thing for the owner's pass anyway**, because 4.2 is about scope and this
is a geography sentence: the towns listed in the serving-areas section are the
live site's own list and are still on the claims list. This edit does not touch
them.

**A note on the form.** "Bucks and Montgomery County", singular, matches the
"Bucks & Montgomery County" already in the meta description, the og
description and the crash H2. The page also carries "Bucks and Montgomery
Counties" and "Bucks County and Montgomery County" elsewhere, all from the
live site. **Three forms of the same pair is a tidy-up worth doing in one
pass**, and it is deliberately not done here: it would touch a heading and a
meta description, and headings and descriptions are not something to change
while making a one-sentence consistency fix.

### 1.23 The Major card's ADAS sentences, broadened past structural work

**Flagged for the owner's pass, and this one is a scope change rather than a
placement.** 1.18 and 1.19 moved claims the page already made. This one widens
a claim.

| | |
|---|---|
| **Before** | For major repairs, we also perform ADAS recalibration. This ensures your vehicle's advanced safety systems, like lane departure warnings and automatic braking, function correctly after structural work. |
| **After** | We also perform ADAS recalibration whenever a repair calls for it. Structural work is the obvious case, but a replaced windshield or a repaired bumper can disturb the sensors behind it too. Recalibration ensures your vehicle's advanced safety systems, like lane departure warnings and automatic braking, work the way the manufacturer intended. |

The rest of the block is untouched: the state-of-the-art equipment sentence,
the environmentally friendly products, the lifetime warranty and the closing
line all stand as they were.

#### What is sourced, and what is not

Checked against the live `/auto-glass-repair-replacement/` page on 2026-09-10,
not assumed. `pagemap.md` already names that page's in-house statement as the
source material for the gated ADAS page, so it is the right place to look.

| New element | Basis |
|---|---|
| ~~"in our facility"~~ | **Dropped 2026-09-10, before the owner ever saw it.** It was published (the glass page says "We perform ADAS recalibration at our Southampton facility") but it is no longer in this sentence. See below. |
| "work the way the manufacturer intended" | **Published, verbatim, twice.** Deliberately reused so the two pages say the same thing in the same words. |
| a replaced windshield disturbing sensors | **Published.** "Many newer vehicles mount cameras and sensors behind the windshield to power safety features like lane departure warning and automatic emergency braking." |
| **a repaired bumper disturbing sensors** | **NOT PUBLISHED ANYWHERE.** The glass page is about windshields and says nothing about bumpers. This is the new part. |
| "whenever a repair calls for it" | **Widened.** The old sentence said "for major repairs". |

Radar behind a bumper cover is ordinary in modern vehicles, so the sentence is
plausible. Plausible is not the test. **The claim is not about what cars are
like, it is about what this shop does**, and no published page of the shop's
says it recalibrates after bumper work.

#### The scope question for the owner

**Does the shop recalibrate, or check the need for recalibration, on minor
jobs like bumpers and mirrors, and not only on structural work?**

There are three different honest answers and they need different sentences:

1. **It recalibrates whenever the job calls for it, bumpers included.** The
   copy above is right and ships as written.
2. **It checks whether recalibration is needed and recalibrates when it is.**
   Then "we also perform ADAS recalibration whenever a repair calls for it"
   overstates it slightly and should say the shop checks.
3. **Structural and glass work only.** Then the bumper example comes out and
   the sentence goes back to naming the cases it covers.

#### It also raises the in-house claim's stakes

4.2 already flagged that this page asserts in-house ADAS recalibration, which
is one of the two gates on the ADAS calibration page in `pagemap.md`. The
glass page publishes the same claim, so the collision page is not exceeding
the live site on that point. But **this edit makes the claim broader and more
prominent**, so if the answer is that calibration is sublet, more than one
sentence changes and the ADAS page is settled at the same time.

#### "in our facility" came back out, 2026-09-10

The first sentence carried it for one commit and now reads "We also perform
ADAS recalibration whenever a repair calls for it." Two things follow, and the
second is worth being exact about.

**The repetition is resolved.** The phrase appeared twice in one paragraph
while it was in, once in the new sentence and once in the untouched equipment
sentence. It appears once now.

**The page no longer states in-house recalibration outright.** What is left is
"we also perform ADAS recalibration", which says the shop does it and stops
short of saying where, sitting two sentences above "We use state-of-the-art
equipment in our facility". That equipment sentence is a general claim about
the shop's tooling; it is adjacent to the calibration claim rather than a
statement about it. **A reader will infer in-house. The page no longer asserts
it.**

That is a reduction in exposure while the claim is unconfirmed, and it changes
nothing about the gate: `pagemap.md` rests the ADAS page on the **glass page's**
in-house statement, which is untouched and still explicit. It does mean the
line in 4.2 about this page asserting the claim is now weaker than it was, and
4.2 says so.

### 1.24 The process kicker, and what the kicker register is

**Not a before/after pair, because there is no "before" from the live site.**
Section kickers are builder-authored; the live page has none. This is recorded
as a **voice decision** rather than a text change, because the register is a
mold element and pages 2 through 37 inherit it.

```
was   What happens between the phone call and the keys
now   What we do, in the order we do it
```

**Why it changed.** The old line framed a span, and the H2 above it already
frames the same span: "Our Collision Repair Process: From Accident to
Road-Ready". A kicker that restates its own heading spends a line saying
nothing.

#### The register, which is the part that generalizes

All nine kickers on this page, so the rule is visible rather than asserted:

```
Two kinds of damage, one shop
The moments right after a collision can feel chaotic
We talk to the adjuster so you do not have to
In their words, not ours
Twelve manufacturers, and the procedures that come with them
You are choosing who cares for your vehicle during a stressful time
One phone number, one email address, one shop
The questions drivers actually call and ask
What we do, in the order we do it
```

What holds across them:

- **Short, and no terminal punctuation.** A kicker is a label, not a sentence
  the reader finishes.
- **Usually a contrast or a parallel.** "X, not Y". "One, one, one".
- **Never a command and never marketing-speak.** No "discover", no
  "solutions", no verb-first instruction to the reader.
- **It says something the H2 does not.** That is the whole job. A kicker that
  paraphrases its heading is the failure mode, and it is the one that just got
  fixed.
- **It carries no claim the page does not already carry.** Three of the nine
  are reader-facing ("We talk to the adjuster so you do not have to"), and each
  restates something stated at length below it.

#### What was rejected, and why it is worth writing down

Three other lines were on the table:

| Candidate | Why not |
|---|---|
| Six steps, from the first call to the keys | True, and closest to the old line, but it still overlaps the H2's span, and as a mold every page would have to supply its own step count. |
| The order it actually happens in | Plain and short, and "actually" is already in the register. Implies the page is not an idealized version, which is a quiet claim about candor. |
| You will know which step your car is on | The strongest line of the four and **the only one that is a claim**. It restates FAQ 1's progress-updates promise as a heading, so it would need the owner's pass, and as a mold it would push future kickers toward promises rather than labels. |

**The one that shipped adds no claim at all**, which is why it needs nothing
from the owner and why it fits any service page unchanged.

### 1.25 The homepage, four changes to the live copy

Everything else on `/` is the live homepage's own words, in its own order.

**a. The business name, 2 changes.**

| | |
|---|---|
| **Before** | Tri County Collision Center |
| **After** | Tri-County Collision |

Same open question as 1.1. **Whatever the Google Business Profile says is the
answer**, and it is still the swap of record for every page built so far.

**b. The street, in the "who you are handing the keys to" paragraph.**

| | |
|---|---|
| **Before** | a family-owned shop on Jaymor **Road** in Southampton |
| **After** | a family-owned shop on Jaymor **Rd** in Southampton |

Not a style choice. `scripts/audit.py` fails any page that spells the street a
second way, and "Jaymor Road" is the variant the live site's own schema uses
against its own footer. See 3.1.

**c. The review claim comes out of the paragraph entirely.** See 3.12.

| | |
|---|---|
| **Before** | ...on Jaymor Road in Southampton, **with more than 1,500 five-star reviews from drivers across Bucks and Montgomery County**. |
| **After** | ...on Jaymor Rd in Southampton, **serving drivers across Bucks and Montgomery County**. |

**d. The hero CTA.**

| | |
|---|---|
| **Before** | GET MY FREE ESTIMATE |
| **After** | Call (215) 322-5350 &nbsp;/&nbsp; Email the shop |

The live button posts to a form this site does not have yet. The house
grammar is one filled button meaning act, and act means the phone. The words
"request an estimate online" survive in FAQ 4 carrying a `data-pending-href`
to `/contact-us/`, so the sentence returns to being a link the day that page
ships.

### 1.26 The services grid's one-line promises, composed

The live homepage gives two of its four services a blurb and the other two
nothing but a "Learn More" button. The grid needs one line per card, so two
were composed and two were shortened. **None adds a claim.**

| Service | Line | Where it comes from |
|---|---|---|
| Collision Repair | Minor and major damage, repaired to manufacturer standards. | **Composed.** "Minor and major" is the live site's own split; "to manufacturer standards" is step 04 on /collision-repair/ verbatim. |
| Commercial Collision Repair | Commercial and fleet vehicles. | **Composed, and deliberately empty of promise.** The live page gives this service no words at all. Rather than invent a benefit, this restates the service name. **If the shop wants this card to say something, the owner supplies it.** |
| Paintless Dent Repair | Dents removed without touching your paint. | Shortened from the live blurb, "remove dents without affecting your vehicle's paint job". |
| Auto Glass Repair | Cracked windshields and broken side windows. | Shortened from the live blurb, "cracked windshields, broken side windows, and more". **"And more" was dropped**: it is scope with no edges. |

**No card says "Learn more" any more.** Three of the four have no page to link
to, and a label that looks like a link and is not one is worse than no label.
The linked card is the whole card; the unlinked cards are not clickable and do
not pretend to be, including the lift, which is on the linked card only.


### 1.27 The contact band gives up the ask, two changes

**The client's diagnosis, 2026-09-17, and it is the right one: the act band
and the contact band read as the same band twice, because THE ASK IS
DUPLICATED AND THE INFORMATION IS NOT.** `#start` asks; `#contact` was
asking again in a smaller voice, in front of the same phone number it had
already printed as a fact eight lines above.

**The fix is one job each.** The act band is untouched: the restore line,
"Estimates are free and there is no obligation", both buttons, and it stays
the page's one conversion moment under the act-band rule. The contact band
becomes pure reference.

**a. The heading drops the pitch.**

| | |
|---|---|
| **Before** | Contact Us for Your **Free Estimate** |
| **After** | Contact Us |

The estimate pitch lives one band up, in a band that exists to make it. A
heading whose job is to label a block of facts should label the block of
facts.

**b. The closing line drops everything the band had already said.**

| | |
|---|---|
| **Before** | **Estimates are free.** Call **(215) 322-5350**, email **contact@tricountycollision.com**, or send us your details online. |
| **After** | Prefer to write? Send us your details online. |

Three of that sentence's four clauses were repeats: the estimate claim from
the band above, and the phone and the email from the grid directly above it,
where both are already tappable. **The fourth clause was the only thing in
the band that appears nowhere else on the page**, and it is what is left.

**Nothing was lost and the removal is checkable.** The phone, the email, the
address and the hours are facts in the grid, unchanged. The
`data-pending-href` to `/contact-us/` is intact, so the sentence becomes a
real link the day that page ships, and the pending-link test still sees it.
The audit reads **12** tappable phone and email mentions on the homepage where
it read 14, which is exactly the two duplicate links, and the NAP address
check still reads the canonical spelling.

**The sub line stays**, because it is not a repeat of anything: "One phone
number, one email address, one shop" is the one-email doctrine made visible,
and it is the sentence that tells a reader the `info@` address they may have
seen elsewhere is not a second shop. See section 2.

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
| ~~The link on "paintless dent repair (PDR)"~~ | **Now carried**, as of 2026-09-24. `/paintless-dent-repair/` landed and the pending-link test forced the link back in the same commit. See 3.48. |
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

**Amended 2026-09-17, and the amendment is about which bands the sentence was
ever describing.** It governs ACT bands, the ones that ask for something, and
it still governs them exactly: the CTA band is the only oxblood band on a page
that asks for an action. Oxblood may also be a prose section's ground, which
`#who-we-are` now is. See 3.25 and the `.dark` note in `site.css`.

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

### 3.9 The safety-systems icon was a wifi signal

**Design note. No copy changed**, and the card still reads "Your vehicle's
safety systems work exactly as designed."

The middle card of the payoff trio wore three stacked arcs over a stem. At
44px that is the wifi glyph, and it anchored a card about lane departure
warnings and automatic braking to connectivity. An icon is a handle for
finding a sentence again; a handle that points at the wrong thing is worse
than none, because the reader trusts it.

```
was   <path d="M12 20.4v-7.6"/>
      <path d="M8.6 15.8a4.8 4.8 0 0 1 6.8 0"/>
      <path d="M5.7 12.7a8.9 8.9 0 0 1 12.6 0"/>

now   <path d="M3.2 21.2L9.8 4.2"/>
      <path d="M20.8 21.2L14.2 4.2"/>
      <path d="M12 20v-3.4M12 14.4v-2.6M12 9.4v-2"/>
```

Two road edges converging upward with a dashed centre line: the lane a lane
departure system watches. House style throughout, and none of it is set on
the element, because `.tile svg` in `site.css` already supplies it: 24x24
viewBox, no fill, 2px strokes, round caps and joins. `aria-hidden="true"`
stays, because the sentence beside it is the content and the glyph is
decoration.

**Drawn at three splays and compared at the real 44px tile**, not at 5x where
everything reads. The committed one has the widest base of the three: a
narrower road turns to mush at 24px, and the trapezoid is what makes it a road
rather than three strokes.

#### The set was checked both ways

**Nothing else means "road".** The full set is twelve glyphs: certification
shield, sparkles, document, umbrella, magnifier, wrench, dent, panel grid,
quote mark, tag, phone, and now the lane. **The dent and the panel grid were
both redrawn on 2026-09-10; see 3.11.** The nearest neighbour is the Minor
card's dent, an arch over a horizontal rule, which shares no geometry with two
converging diagonals.

**The arc glyph is now used nowhere.** It had exactly one use on the site, so
retiring it from that card retires it entirely and there is no second meaning
left to keep unique. Swept across `docs/` and `templates/` by its path data
rather than by eye.

### 3.10 The waiting is mechanized: data-pending-href

**Design note. No copy changed and nothing became a link.**

This site never writes a link to a page that has not been built, and that rule
is enforced: a relative `href` with no file behind it fails the build.
Enforcing it leaves a residue, which is every element that *should* be a link
and is not yet. **The residue was the unmechanized part.** Nothing recorded
what each element was waiting for, and nothing would notice the day the wait
ended. The failure mode is a page shipping built and unlinked, with a span
sitting where its link belongs, while the link test reports a clean site the
whole time.

Each waiting element now carries `data-pending-href` with the URL it becomes.
Converting one is renaming the attribute and changing the tag.

#### The inventory, nine elements across four target pages

| Element | Becomes |
|---|---|
| Header logo | `../` |
| Footer logo | `../` |
| Breadcrumb "Home" | `../` |
| "paintless dent repair (PDR)", Minor card | `../paintless-dent-repair/` |
| "request one online", step 01 | `../contact-us/` |
| "request a free estimate online", Minor card | `../contact-us/` |
| "requesting one online", insurance section | `../contact-us/` |
| "request an estimate online", FAQ 4 visible | `../contact-us/` |
| "our blog post on the topic", FAQ 5 visible | `../your-right-to-choose-a-body-shop/` |

**The blog slug was read, not invented.** `pagemap.md` says the 16 posts keep
their existing slugs but does not list them, so the live page was read on
2026-09-10 and it links `/your-right-to-choose-a-body-shop/`. A URL is a fact.

**The two FAQ spans do not break the mirror.** They wrap visible text only; the
schema strings two hundred lines up are untouched, and the audit still reports
all 7 questions and answers byte-identical.

#### The test cuts both ways now

```
direction 1   a real href with no file behind it            FAILS  (as before)
direction 2   a data-pending-href whose target NOW EXISTS   FAILS  (new)
```

Direction 2 is the half that was missing. Both resolve through one shared
function, `audit.resolve_local_link`, so they cannot drift apart by one of them
deciding `../` means something different.

**Live-fired before committing.** `docs/contact-us/index.html` was created on
purpose: the test failed, and the audit note flipped the `../contact-us/` row
to "BUILT, convert these to real links". Then it was deleted and both went
quiet again.

**One bug this turned up immediately**, and it is the reason the fixtures
exist: `href` is a substring of `data-pending-href`, so the dead-link pattern
matched the new attribute and reported all nine pending links as dead links.
The pattern now requires an attribute boundary, and a harness case holds that
exact trap.

#### It shows up in the Monday report

`scripts/audit.py` carries the inventory as a **note**, grouped by target, in
every run. A note rather than a warning, because an unbuilt page is the plan
working rather than a defect. When a target does exist, the note says so in
that row and the test is what fails.

#### One thing the inventory turned up, for the owner

The live site's "request an estimate online" links do **not** go to a
first-party form. They go to `carwise.com`, a third-party photo-estimate tool.
`pagemap.md` retired `/customer-information/` precisely because it "carried a
third-party intake form the shop does not own", and it makes `/contact-us/`
the only intake form on the site. So the pending target above follows the
spec. **But somebody has to decide whether the Carwise photo-estimate flow is
being replaced by our form or kept alongside it**, because four sentences point
at it today and 3.2 already says those sentences come out if no form ships.

### 3.11 The Minor and Major card icons were too abstract to mean anything

**Design note. No copy changed.**

```
Minor   was  an arch over a horizontal rule
        now  two lines dipping together: the panel surface, and the
             character line bending over the dent

Major   was  a rectangle divided into six panes, which read as a window
        now  the tapered unibody outline, overhead, measured corner to
             corner with the diagonal cross-measures
```

**Minor is the thing paintless dent repair exists for.** Two lines dipping
together is what a tech actually sees sighting down a wing: the surface
falls away and the reflection line bends with it. The old arch was a shape,
not a dent.

**Major is the drawing a structural tech works from.** The cross-measures are
the ones that prove a unibody is square, which is what frame straightening
means, and the card claims exactly that.

#### Round one was drawn, rendered and thrown away

The first four candidates were 8 to 12 path segments each and **none of them
survived 24px**: one dip was too shallow to register, one panel-with-rings
read as an eye, and both structural candidates mushed into a dense block.
**At 24px with a 2px stroke the budget is about five to seven strokes.** The
shipped pair is two paths and three paths. Judging at 96px would have passed
all four; judging at the real tile size failed them, which is the only reason
to render at real size.

#### The set was checked both ways

**Neither old glyph survives anywhere.** Each had exactly one use, so
replacing them retires them; swept `docs/` and `templates/` by path data.
The set is still twelve distinct glyphs across twenty uses.

**Nothing else in the set means either thing.** The nearest neighbour to the
new Major is the lane: both are tall and tapered. They stay apart because the
lane is two open diagonals with a dashed centre line and no outline, and the
Major is a closed outline with an X and no dashes.

#### One thing the brief asked for that could not be delivered

The Major icon was asked to echo **the frame-datum band art**, so the card and
the Why Choose band would speak the same structural language. **That band art
was reverted in `5d30750`** and the band carries the gradient now, so there is
nothing left to echo. The icon is right on its own terms, and the shared
language is a separate decision about bringing the drawing back.

### 3.12 The live homepage disagrees with itself about the review count

**This is the finding, and it is why the claim could not be migrated.**

```
live homepage, body copy      "more than 1,500 five-star reviews"
live homepage, its own widget "Based on 231 reviews"      (same page)
the Google Business Profile   274 reviews, 4.9 stars      (read 2026-09-10)
```

The prose and the widget are **on the same page** and differ by a factor of
six. So this was never a question of our number being newer than theirs: the
live page already contradicted itself, and one of its two figures was wrong
before we arrived.

`scripts/audit.py` would have caught it anyway. The site-wide check criticals
on any two review counts that disagree, counting `REVIEW_COUNT` as one of the
instances, so shipping 1,500 would have failed the build. **That is the check
doing the job it was written for on the first page it was pointed at.**

**What shipped instead**: the verified stat band from the mold, 274 and 4.9,
carrying the day it was counted. The homepage paragraph now makes no
quantified review claim at all, because one page should not state a number
its own stat band already states, and because the only honest version of the
sentence is the one the band already says better.

**For the owner:** 1,500 is not a small rounding. If the shop has 1,500
five-star reviews somewhere other than Google, that is a real asset and it
should be named and linked. If it does not, the claim should come off the
live site too, not just out of this migration.

### 3.13 The homepage FAQ, and where each question came from

`pagemap.md`'s Home row asks for "5 to 7 questions from the phone log, owner
supplies". **There is no phone log in this repo and the owner has not supplied
one**, so this is an interim built from Q&As the live site already publishes,
and it should be replaced or confirmed when the real list arrives.

Six questions, all from `/collision-repair/`, carried **byte-identical** to
the way that page carries them, because a house answer renders as one string
on every page that holds it:

| # | Question | Source | Why it made the cut |
|---|---|---|---|
| 1 | Can I choose my own collision repair shop after an accident in Pennsylvania? | /collision-repair/ | Anti-steering. The most valuable thing this shop can tell a driver an insurer will not. |
| 2 | Do you work with my insurance company? | /collision-repair/ | The first question on the phone. |
| 3 | How long does collision repair take? | /collision-repair/ | The second question on the phone. |
| 4 | How much does collision repair cost? | /collision-repair/ | Estimates, and it carries "free" and "no obligation". |
| 5 | Will my car look the same after collision repair? | /collision-repair/ | The lifetime warranty lives in this answer. |
| 6 | What certifications do your technicians have? | /collision-repair/ | ASE and I-CAR, stated at length rather than as a chip. |

**All six already passed the standalone test** when they were fixed on
`/collision-repair/` (see 1.2 to 1.4), so none needed comma-merging here. The
visible text and the FAQPage schema are generated from one set of strings, so
the mirror cannot drift.

**One consequence to weigh:** six answers now appear word for word on two
pages. That is what the house-canonical rule requires, and it is the opposite
of what a duplicate-content instinct would say. If the two pages ever need to
differ, the rule is that a page omits a question rather than writing a variant
of its answer.

### 3.14 Four of the live homepage's eight testimonials were carried

The live homepage publishes eight. Four are carried, byte for byte, typos and
loose punctuation included. The four dropped are the shortest: "My car looks
beautiful. They went above and beyond.", "Very easy to deal with. Justin does
exceptional work.", "Excellent service, repair was perfect.", and the "only
place i will take my car" one, which is strong but overlaps the Joe Chiclets
quote on detailing.

The four carried were chosen for specificity: each names something checkable,
a tow arranged, a deer strike, paint blended between new and original panels,
updates that arrived when promised. **None of them is edited.** See 4.8 for
what still needs confirming about testimonials generally; the same questions
apply to these.

### 3.15 The homepage reuses the pattern page's hero photograph

There are three real photographs in this repo and all three are already on
`/collision-repair/`. The homepage hero is the same image as that page's hero.
**It should have its own**, and that sits with the rest of the photography
question in 4.9, which is already a cutover blocker.

### 3.15b The llms.txt check cannot fail on the root page

Noticed while building `/`. The audit reported the homepage as "listed in
llms.txt" before it was listed: the check looks for the page's URL anywhere in
the file, and the root URL `https://tricountycollision.com/` appears in the
paragraph that tells an agent the live site is the one to read today. **The
root page can never fail that check**, because any mention of the domain
satisfies it.

The homepage is properly listed under Key pages now, so the pass is honest.
**The check's blind spot is not fixed**, and it is recorded here rather than
left to be rediscovered: it wants to read the Key pages list rather than the
whole file, the same way the dead-link scan learned to require an attribute
boundary rather than a substring.

### 3.16 The homepage's WebPage node points at a WebSite node

`/` carries a `WebSite` node and its `WebPage` is `isPartOf` that node.
`/collision-repair/` has no `WebSite` node and its `WebPage` is `isPartOf` the
**business** node, which is how it was built. Both are valid and neither
breaks anything today. **They should agree before the third page ships**, and
the homepage's shape is the correct one.

**No `BreadcrumbList` on the root**, deliberately: a breadcrumb whose only
rung is the page you are standing on is furniture. The visible page has no
breadcrumb either, so the mirror holds.

### 3.17 Four service cards, three photographs

The router grid wants a photograph per card and this repo has three real ones.
**One image is used twice in the grid and one of those is also the hero.**

```
hero                          accent-major-collision-repair.jpg
Collision Repair              accent-minor-collision-repair.jpg
Commercial Collision Repair   accent-major-collision-repair.jpg   <- also the hero
Paintless Dent Repair         accent-collision-repair-1.jpg
Auto Glass Repair             accent-minor-collision-repair.jpg   <- repeat
```

Not a design decision. **Real photos only** is a standing rule, so the
alternative was stock or nothing, and both are worse than a repeat that is
written down. **The grid needs four distinct photographs**, and really wants
one per service showing that service. This joins 4.9, which is already a
cutover blocker.

**3.15 is resolved differently than it said.** It flagged that the homepage
reused the pattern page's hero. The two pages now use different photographs
and different hero architectures, so they no longer read as the same page. The
underlying shortage did not go away; it moved into this note.

**UPDATED 2026-09-17: the first real photographs are in, and they are not
these.** Ten frames of the shop's own customer vehicles landed for the Real
Repairs band, section 3.23. **The hero and all four service cards still carry
the three stock images**, and this note stands unchanged for them: the grid
still needs four distinct photographs, one per service, showing that service.

What the shoot still owes, and none of it is covered by the repair
photographs: **the building, the signage, the bays, the frame rack, the paint
booth, and the people who do the work.** Two of the ten repair frames happen
to include the Tri-County sign in the background, which is evidence the cars
were photographed at this shop, and it is not a photograph OF the shop. 4.9
stays a cutover blocker.

### 3.18 The homepage carries two testimonials, not four

The live homepage publishes eight and the first build of this page carried
four. It carries two now: Theresa Helt and Joe Chiclets, the two that name the
most checkable things, a tow arranged and an insurer dealt with, a deer strike
and a car detailed inside and out.

A front door quotes its best and moves on; the four-up grid belongs on a page
someone is already reading. Both are byte for byte, typos included. **Neither
is owner-approved**: 4.8 is open and applies to these two exactly as it
applies to the rest.

### 3.19 "We Fix It All" is a diagram now, and the drawing was redrawn

The five-line checklist is the estimator's car profile with the checklist's own
words pointing at the panels they name: windshield to the glass, hail to the
roof, dings to the door, deer to the front, collisions to the rear quarter.
**The labels are the checklist's words and nothing was added.**

**The drawing has been redrawn twice, and the second time properly.** The
band-art version was made for 7 percent opacity at the edge of a band; at full
size its outline was open at the front with a stray tail where the bumper
should close, and one leader landed on that tail. Closing it made it usable but
it still read as elementary, which is not good enough for the page's signature
section.

**The current drawing is built from measured ratios rather than eyeballed.**
Overall length 620 units: wheelbase 372, which is **60 percent** of length;
body height 186, **30 percent**; front overhang 110 against a rear overhang of
138, so the front is the shorter one; cabin centred 75 units **rearward** of
the car's midpoint; tyre diameter 13.5 percent of length.

**Three line weights in one ink**, which is how a sheet like this is drawn: the
silhouette at 3.2, panel seams at 2.0, details and dimensions at 1.2. The
hierarchy is weight, not tone.

**The details are the ones an estimator would look for**: A, B and C pillars
with the glass inset inside them, a rear quarter window, a side mirror seated
on the beltline, both door handles, the rocker crease with the door cuts
stopping **on** it, wheel arches concentric with the wheels, hub circles, a
ground line, and a dimension run with arrowheads under the wheelbase. The rear
door cut terminates on the arch curve at its computed intersection rather than
near it.

**Judged at full size every time, never zoomed**, which is the only reason the
faults were caught: the first pass ran door cuts through the wheel arches and
doubled the outline with the sill; the second crossed the rocker instead of
stopping at it and left the mirror reading as a floating flag. None of that is
visible at a thumbnail.

**It is a diagram, so it does not move.** Solid single colour, no fill, no
motion, no arrival effect. The arrival amendment covers a number counting, a
word rolling and a lane drawing, and this is none of those.

**The labels do not survive a phone**, which is a real limit rather than a
detail. At 390 the drawing scales to about a third and a 19px label becomes
6px. Below 900px the callouts are hidden and the same five lines render as an
ordinary list. **The list is in the DOM at every width**, visually hidden above
900, so a screen reader gets the words whatever the viewport is.

### 3.20 The hero is text over photograph, and the scrim is measured

Rebuilt 2026-09-10 on the client's ruling: the photo-above-panel arrangement
is out. **Copy unchanged.** This was arrangement and motion.

**The measured worst cases**, sampled out of real renders per the readability
amendment: the page is rendered twice, once normally and once with the copy at
`visibility: hidden` so the ground can be sampled without the glyphs, and each
element's **glyph runs** are measured rather than its block box.

**Re-measured 2026-09-13** at the eyebrow's restored size, and these are the
numbers that stand. The first set was taken on 2026-09-10, and between those
two dates the eyebrow was rendering at the wrong size; see "The eyebrow was
swept and restored" below.

| Element | 1440x900 | 1920x1080 | 390x664 | 360x640 | Needs |
|---|---|---|---|---|---|
| Eyebrow | 13.93 | 13.89 | 13.09 | 9.94 | 7 |
| H1 | 11.86 | 13.19 | 13.23 | 13.23 | 4.5 |
| Lead | 9.47 | 9.47 | 9.72 | 9.72 | 7 |
| Ghost button label | 13.87 | 13.57 | 14.28 | 14.28 | 7 |

**Every element clears the 7:1 target, not just the 4.5 floor.** The eyebrow is
small tracked caps, so 7 is the number it has to clear and not 4.5, and it
clears it at its restored size at every width. **The scrim did not move for
this.** Smaller glyphs sample less photograph, not more, so the restore cost
the composite nothing; the 360x640 worst case is the tightest at 9.94 and has
almost three points of headroom.

**They were not all passes first time, and that is the point of measuring.**
The phone eyebrow measured **2.13** and the 360 H1 **4.25** against a scrim
that had faded to nothing above the copy. The scrim was deepened until they
cleared. The standard was not touched.

**The measurement also found a layout bug the geometry probe missed.** The
ghost button's glyph run measured 1.12 against silver, which is silver on
white, which is the stat card: **the card was sitting on top of the CTA
buttons**. The hero copy's bottom padding is now the card's overlap plus air,
at both breakpoints.

#### Geometry

**Measured 2026-09-13**, staging banner hidden, which is the post-cutover
state. The CTA-to-card column is new and it is now a construction invariant
rather than a measurement: see "The card's overlap is one number now" below.

| Viewport | Hero depth | CTA ends | Fold budget | | CTA to stat card |
|---|---|---|---|---|---|
| 1440 x 900 | 566 | 553 | 900 | clears by 347 | 28 |
| 1920 x 1080 | 566 | 553 | 1080 | clears by 527 | 28 |
| 430 x 745 | 560 | 553 | 685 | clears by 132 | 28 |
| 390 x 664 | 541 | 534 | 604 | **clears by 70** | 28 |
| 360 x 640 | 582 | 575 | 580 | clears by 5 | 28 |

**Both recorded exceptions are retired.** The desktop trade, CTA at ~1037
against a 900px viewport, is gone: 553. The phone exception, CTA at 646
against the 604 budget, is gone: 534.

#### The card's overlap is one number now

Changed 2026-09-13. The card's overlap and the hero copy's bottom padding used
to be two independent clamps tuned to approximately agree, and the air between
the buttons and the card's top edge was the leftover: **12px at 1440, about 8px
near 1300, 6px at 390.** The overlap is now `--statcard-overlap`, the card
takes its negative and the hero copy takes `overlap + 28px`, so **the air is
28px by construction** at every width where the hero is content driven, and
more where min-height governs. Two values that must agree are one value plus a
derivation.

The CTA moved up or held everywhere when this landed: 566 to 553 at desktop,
573 to 553 at 430x745, unchanged at 390 and 360. All of the added padding sits
below the buttons.

#### The eyebrow was swept and restored

**Swept 2026-09-10 in the commit that deleted the old split hero. Restored
2026-09-13, verbatim.** The base `.eyebrow` rule, which is site type and not
hero type, happened to sit beside the `.heroA` block in the stylesheet and went
out with it. For three days both heroes rendered their eyebrow as plain 1rem
sentence case: no `.82rem`, no 800 weight, no `.12em` tracking, no caps. **The
home page read "Family owned and operated" in sentence case** where the
signed-off pages read it small, bold, tracked and upper case.

What it cost, measured: the eyebrow grew from **22px to 28px** tall on a phone,
and everything under it slid 7px. The h1 top went 118 to 125, the lead 336 to
342, and **the 360x640 CTA went from 575 to 582 against a 580 budget**, so the
tightest phone in the record stopped clearing the fold. The restore puts all of
it back: 22px, and 575 again.

**The two contrast tables in 3.20 and 3.21 changed twice for this reason**, once
on 2026-09-10 at the regressed size and once on 2026-09-13 at the restored one.
The numbers that stand are the 2026-09-13 ones.

**The lesson, which is a discipline and not a mechanism: a sweep may delete
only rules scoped to the thing being swept.** Before deleting a rule in a
cleanup, grep its selector across every page. A base-class rule that merely
lives near a section's block belongs to the site, not the section. Nothing
would have caught this but reading the diff or measuring the render, and it was
the render that caught it.

**Two other base rules went out in the same sweep and were restored the same
day**, in the commit after the eyebrow's. `.hero { padding-top }` and
`.lead { font-size / color / max-width }`. **Neither changes either page**, and
that was verified rather than assumed: `.hero`'s padding computes to 0 on both
heroes because `.heroB` zeroes it, both leads take their size, colour and
measure from `.heroB .lead`, and the document heights and hero and CTA boxes
are identical at 1440 and 390 on both pages before and after.

They are restored because a base rule that is invisible today is not a base
rule that is unused: it is the default every future page inherits, and the
sweep took the default away. `templates/service-page-template.html` already
puts a `.lead` outside a hero.

#### What the phone scrim costs, stated rather than hidden

On a phone the copy fills the frame, so **the scrim is strong across almost
all of it**: 0.96 at the bottom easing to 0.92 at 95 percent and clearing only
in the top 5 percent. The clear band is roughly 25 to 30 pixels. **On a phone
the photograph is a texture, not a picture.**

That is not what the brief pictured, and the arithmetic is why: for the
eyebrow to clear 7:1 over the brightest pixel in this photograph the scrim
needs alpha 0.745 under it, and at 360x640 the copy's top sits 26px below the
hero top. Pushing it down far enough for a real clear band costs about 40px,
and 360x640 clears the fold by 5. **The fold and the readability floor were
held; the clear band is what gave.** At 390 and above there is more room, and
if the phone photograph matters more than the phone fold, that is a trade
worth naming rather than one to discover.

#### The entrance

One fade on load, opacity only, photo then copy 200ms behind, 500ms each.
CSS-only so it runs with JavaScript off. Base opacity is 1 and the fade lives
only inside `prefers-reduced-motion: no-preference`, so every no-animation
context rests with everything visible. It amends "nothing animates on load",
and the amendment is dated in `site.css` and `CLAUDE.md`.

### 3.21 /collision-repair/ gets the same hero, grounded in ox

Rebuilt 2026-09-10. **Copy unchanged.** Arrangement and motion only, and the
same `.heroB` machinery the homepage uses with one modifier class for the
scrim colour. The entrance keyframes exist once for both pages.

#### Measured composite, worst case under any glyph run

**Re-measured 2026-09-13** at the eyebrow's restored size, with the whole copy
block sitting 6 or 7px higher for the same reason, so every row was taken
again rather than just the eyebrow's.

| Element | 1440 | 1920 | 430 | 390 | 360 | Needs |
|---|---|---|---|---|---|---|
| Breadcrumb | 9.65 | 9.65 | 9.52 | 9.21 | 9.01 | 7 |
| Eyebrow | 9.65 | 9.52 | 9.59 | 9.39 | 9.21 | 7 |
| H1 | 9.27 | 9.33 | 9.59 | 9.52 | 9.27 | 4.5 |
| Lead | 9.39 | 9.39 | 9.53 | 9.46 | 9.46 | 7 |
| Ghost button label | 9.73 | 9.40 | 9.66 | 10.18 | 10.18 | 7 |
| Chips (desktop) | 9.99 | 9.72 | n/a | n/a | n/a | 7 |

**Everything clears 7:1**, and nothing moved by more than half a point from the
2026-09-10 reading. The ox scrim is near solid where the copy sits, so what the
type is standing on barely changes when the type changes size or shifts a few
pixels. That is the opposite of the home hero, where the scrim fades and the
numbers move with the glyphs. It took four corrections to get there and every one
was found by the probe rather than by looking:

1. **The breadcrumb link was inheriting the page link colour**, which is
   oxblood, on an oxblood scrim. That is 1.42: oxblood on oxblood.
2. **The lead in `--silver-2` measured 6.57.** `--silver-2` on *solid* ox is
   7.34, so against a 7:1 target it has 0.34 of headroom and any photograph
   showing through takes it under. Deepening the scrim to opaque would just
   about reach 7.34 and would put no photograph under the lead at all, which
   is the thing this hero exists to do. **The lead is `--silver` on ox**, which
   reads 10.50 on solid ox, so the scrim can stay short of opaque. The standard
   did not move; the tone with headroom did. The breadcrumb went the same way
   for the same arithmetic. **There is no secondary text tone on an ox ground.**
3. **The chip row reached 76% of a 1440 frame**, inside the scrim's fade, and
   its rightmost glyphs measured 1.06. Capped to 620px it wraps to two rows
   that end at 46%.
4. **Two of the "failures" were the probe, not the page.** It read the
   *container's* colour, but a `<nav>` and a `<ul>` inherit the page colour
   while the `<ol>` and `<li>` inside carry the real one — so silver type was
   being measured against ink. The probe now takes the colour from each text
   node's own parent. **A measurement that reports a false failure is as
   dangerous as one that reports a false pass**, and this one nearly bought a
   scrim deepening that nothing needed.

#### Geometry

**Measured 2026-09-13**, after the eyebrow restore. Nothing on this page was
changed for the stat card's derivation: a service page sits above a stat
*band*, so `.heroB--ox` keeps its own foot at both breakpoints.

| Viewport | Depth | CTA ends | Budget | | CTA to stat band |
|---|---|---|---|---|---|
| 1440 x 900 | 562 | 489 | 900 | clears by 411 | 166 |
| 1920 x 1080 | 562 | 489 | 1080 | clears by 591 | 166 |
| 430 x 745 | 560 | 573 | 685 | clears by 112 | 278 |
| 390 x 664 | 505 | 520 | 604 | clears by 84 | 276 |
| 360 x 640 | 503 | 518 | 580 | clears by 62 | 277 |

**The stat band sits clear of the buttons at every width**, by 166px at
desktop and 276 on a phone. That check exists because of the home lesson: the
stat card sat *on* the CTA buttons there and only the contrast probe saw it.

#### The chips shipped in the hero on desktop, in a strip on phones

**Desktop holds them: depth 575, inside the 600 ceiling, and every chip glyph
run clears 7:1.** Two things bought the room. The chips are capped at 620px so
they wrap to two rows inside the scrim's strong zone rather than running one
row into the fade. And **the ox hero's foot comes in**, because this page sits
above a stat *band* rather than the homepage's floating card, so there is no
overlap to clear.

On phones they move to a strip directly below the hero, on the page ground.
Four rows of chips over a phone photograph costs about 210px and fails both
the fold and the picture.

**There are two chip lists in the markup and exactly one renders at any
width.** A single element cannot occupy two DOM positions, and `display: none`
keeps the hidden one out of the accessibility tree as well as off the screen.
All four chips are verbatim in both. **The strip does not animate**: it is
page, not hero, and the entrance stops at the hero's edge.

#### The photograph

No change was needed. `/` wears `accent-major-collision-repair.jpg` and this
page wears `accent-minor-collision-repair.jpg`; **two front doors were never
going to wear the same picture.** The shortage recorded in 3.17 is unchanged:
four service cards still share three photographs.

### 3.22 We Fix It All: the licensed render and the eight. BUILT, then REVISED 2026-09-17

The drawn intake diagram is gone and the band is a licensed wireframe car
render, full width on the ink ground, with eight damage types in a grid
beneath it. Section head grammar unchanged: centred H2 plus the kicker line
every other section carries.

#### The asset, and the two that were rejected first

**`AdobeStock_1604222224`, provenance verified before a line was built on it.**
Three candidates were offered and the first two were rejected as AI-generated,
which their own metadata declared:

| Candidate | What the file declares | Verdict |
|---|---|---|
| `AdobeStock_1060063701`, top-down | IPTC `DigitalSourceType` = `trainedAlgorithmicMedia`, plus a remote Adobe C2PA manifest | rejected, AI |
| `AdobeStock_746591791`, side profile | `xmp:CreatorTool` = `OkiDokiBot AI Art Generator` | rejected, AI |
| **`AdobeStock_1604222224`, side profile** | **intact Adobe-signed C2PA manifest, 179KB embedded, claim generator `Adobe_Stock adobe_c2pa/0.14.2`, asset id `stock.adobe.com/1604222224`, one action `c2pa.published`, and NO `digitalSourceType` assertion anywhere** | **accepted** |

**What the accepted file's evidence is and is not.** Adobe requires
contributors to declare generative AI and labels the assets it distributes,
the first candidate carried that label plainly, and this one's manifest is
present, signed and silent on the question rather than absent. That is the
strongest evidence available short of the contributor's word. It is not a
positive attestation of human authorship: Adobe Stock's manifest records
**publication**, not creation, so there is no `softwareAgent` in it and no
claim about which tool drew the pixels.

**The shipped files carry none of that metadata**, and that is a side effect
of re-encoding rather than anything done to them on purpose. `sips` drops
metadata, and a C2PA manifest is invalidated by cropping anyway because it
hashes the pixels. The source asset id is recorded here, in the section's own
HTML comment, and in `scripts/prepare-car-render.py`, so the chain is
followable even though the derivative cannot carry it.

#### The client's ruling, 2026-09-17

**The asset qualifies, and the amendment is recorded as the client's.** Greg
chose this file after seeing it rendered. Two constraints it does not meet on
their face were considered and waived by him:

- **It is a side profile, not the top-down view the direction named.** The
  client's pick amends the spec.
- **It is a wireframe, which is line art rather than a photograph.** The
  no-third-drawing ruling covers **drawings made by us**, not a licensed
  engineering render the client selected. The drawn diagram is still dead.

#### The ground bug, and how a passing check missed it

**The first build shipped the 2x file with its entire ground encoded at v=1
instead of 0.** Screen-blended onto ink that put a rectangle one level lighter
than the band across the whole image, which the client saw on a retina
display. The 1x file was clean, so nothing looked wrong at DPR 1.

**The pipeline was not at fault and every stage was clean.** Crop, resize, the
PNG conversion and the black-point correction all end at a ground of exactly
0; each was measured. **It is the JPEG encoder, and it is not monotonic in
quality**: sips quantises an all-black block's DC coefficient, and whether the
dequantised value returns to 0 or lands at 1 depends on the quantisation table
for that particular quality. Measured at 2160px: q55 clean, q50 v=1, q45
clean, q40 v=1, q37 clean, q35 v=1. **There is no threshold to stay above**,
so there was nothing to correct upstream.

**Two things let it through.** The quality search stepped by 5 and took the
first size that fitted, which is how it chose q40. And the only thing it
measured about the ground was the 95th percentile of the ringing around the
lines, which was 1.05:1 and true, **while the modal value of the ground itself
was never read at all**. A uniform offset is invisible to a percentile taken
over the same uniform field.

**The fix, and it is three checks rather than one:**

1. **The search walks every integer quality** and requires both the size
   budget and a surviving ground. It chose **q43, 248KB**.
2. **A post-encode decode assertion.** The emitted file is decoded again and
   its ground's modal value read. The export fails if it is not 0.
3. **A decoder-independent assertion, added because check 2 is not enough.**
   Check 2 asks sips what sips wrote, which is the encoder graded by its own
   vendor's decoder. So the file's own quantisation table is read instead and
   the arithmetic done: a uniform black block has every sample at -128 after
   the level shift, so its DC is exactly -1024 and its AC all zero, and a
   DC-only block's inverse DCT is flat, putting every one of its 64 samples at
   dequantised/8 + 128. That number is fixed by the table in the file, not by
   whose decoder reads it. **Both shipped files read Q00=8 and Q00=1, giving
   exactly +0.000, so the ground clamps to 0 in any conformant decoder.**

**A fourth fix, from a mistake made while diagnosing this.** The export wrote
each candidate quality straight into `docs/assets/img/`, so a failed export
left the last rejected candidate sitting in the repo as the shipped asset. A
mutation test of the new assertion did exactly that, and the q25 file it left
behind was then measured in the browser and misdiagnosed as a decoder
discrepancy. **The export now builds in a temp directory and installs only
after every assertion passes**, and that was verified by running a failing
export and confirming the committed file's hash did not change.

#### The eight items, revised, and where every word comes from

**Deer strikes was removed and minor/major split back into two**, on the
client's ruling, 2026-09-17. Dropping a claim needs no source. Deer work stays
covered under collisions and by the existing post, verified on the live site
as `/blog/deer-season-in-bucks-county-insurance-coverage-next-steps/`.
**Every item now carries a supporting line and the heading-only gap is gone.**

| # | Item | Supporting line | Source |
|---|---|---|---|
| 1 | Minor collisions | Scratches, scuffs, small dents and fender benders. | **trim** of `/collision-repair/`'s "Scratches, scuffs, small dents, bumper damage, and fender benders happen", with "bumper damage" dropped because Bumper damage is its own item two slots away |
| 2 | Major collisions | Frame straightening, structural repair and full panel replacement. | **trim** of `/collision-repair/`'s "When frame straightening, structural repair, and full panel replacement are needed" |
| 3 | Cracked windshields | Small chips and short cracks can often be repaired. | **trim** of the live glass page's "Small chips and short cracks can often be repaired, saving you the cost of a full replacement" |
| 4 | Broken side and rear glass | A shattered door window or rear window can't wait. | **verbatim**, live `/auto-glass-repair-replacement/` |
| 5 | Door dings and dents | No filler, no sanding, no spraying. Your original finish stays untouched. | **verbatim**, live `/paintless-dent-repair/` |
| 6 | Bumper damage | A repaired bumper can disturb the sensors behind it, and we recalibrate. | **composed** from two sentences in one paragraph of `/collision-repair/` |
| 7 | Scratched and chipped paint | Small paint chips can lead to rust over time. | **trim** of `/collision-repair/`'s "Small paint chips can lead to rust over time, dents affect resale value, and unaddressed damage can escalate" |
| 8 | Hail damage | Often lifted out with paintless dent repair, so the finish stays untouched. | **composed** from the live PDR page, which lists hail among what PDR fixes |

**So the count is now four trims, two verbatim and two composed.** The four
trims add no words. Three of them cut only from the end of a published
sentence; the Minor collisions line also drops two words from the middle,
which the client ruled safe on the grounds that dropping words from a trim
cannot add a claim. Items 2 and 7 also drop a serial comma, which is the
typographic normalization already established in 1.11.

**Only two lines are composed now, down from three**, because retiring the
merged collisions line replaced a composed sentence with two trims. **Both
remaining composed lines still need the owner**, as does the question of
whether the shop does all eight in house.

**The glass scope was verified rather than assumed, and it decided an item.**
The instruction made "Broken side and rear glass" conditional on the live
glass page actually going beyond windshields, with "Fender benders" as the
fallback. The live page was read on 2026-09-17 and it does, repeatedly and
unambiguously: "we handle auto glass repair and replacement for windshields,
side windows, and rear windows", a "Side and Rear Windows" heading, and an FAQ
answering "Yes. Our technicians handle all types of auto glass: windshields,
side windows, and rear windows." **So the glass item shipped and the fallback
was not needed.**

#### The measurements

**Contrast on the ink ground**, `--ink` #121B27, computed from the tokens:

```
item headings    --silver   #F0F2F2   15.42:1     floor 4.5, target 7
supporting lines --silver-2 #C9CCD3   10.78:1     floor 4.5, target 7
icon glyphs      --mark     #E92424    3.91:1     floor 3 as a non-text graphic
```

**The icons are logo red and it is one measurement, not eight.** All eight
glyphs are strokes of the single `--mark` token, so the ratio is a property of
the token and the ground, not of the drawing. For the record of what was never
available on ink: `--ox` is 1.47 and `--ox-tx` is 1.94.

**The render, measured as the screen composite it actually is:**

```
car-xray-top@2x.jpg   2160x795   248 KB  q43  median line 8.51:1  Q00=8  DC +0.000
car-xray-top.jpg      1080x397   143 KB  q85  median line 4.01:1  Q00=1  DC +0.000
JPEG ringing around a line                                        1.05:1, below sight
```

**The band verified by pixel sample on the rendered page**, not by reading the
file and not by a canvas re-implementation, at every DPR the srcset can serve:

```
1440 @ DPR1   1x file, 1080x397 device px    ground rgb(18,27,39) == ink   exact
1440 @ DPR2   2x file, 2160x794 device px    ground rgb(18,27,39) == ink   exact
 390 @ DPR2   1x file,  700x258 device px    ground rgb(18,27,39) == ink   exact
 390 @ DPR3   1x file, 1050x387 device px    ground rgb(18,27,39) == ink   exact
```

All four corners of the image area equal the band ink exactly at every one.
**One measurement was thrown away as invalid before these**: a canvas that
filled ink and drew the image in screen mode reported rgb(20,29,41) at DPR 2,
because it drew a 2160px source into a 1080px canvas, a downscale the real
page never performs since at DPR 2 the 2x file renders 1:1 in device pixels.

**No level lift was applied, and that is a measurement rather than an
omission.** The median line already cleared the 3:1 floor at both sizes. An
earlier pass reported the median as 86, which was wrong: it came off a 500px
proxy rather than the export, and downscaling dims line art. The pipeline
still solves a gamma if a future size or ground pushes the median under.

**PNG was tried first and lost.** 479KB for the 2x even with a clean ground,
because a dense wireframe is high-entropy; quantising to 16 grey levels to fit
the budget banded the lines visibly. The objection to JPEG was that ringing
would read as a glow, which is banned, so it was measured instead of argued
and it reads 1.05:1.

#### The icons, and the two that replaced the combined glyph

**Drawn at 30px where the approved chip scale is 17px**, a recorded deviation.
The chips carry three repeated glyphs inline beside their own label, where
position identifies them as much as shape does. These are eight distinct
glyphs standing alone above a heading, and eight damage types have to be told
apart from each other.

**They were drawn at 26px first and rendered, and four of the eight were
unreadable**, which is the same failure already on record in 3.11: the broken
glass glyph read as a cancel symbol, the door read as a picture frame, the
bumper read as a football, and the deer read as an insect. All four were
redrawn and re-rendered.

**The deer glyph died with its item. The combined collisions glyph became
two**, and they have to read apart at 30px:

- **Minor collisions**: two short arrows converging on a small burst. A
  localised knock.
- **Major collisions**: a car in profile with a jagged fracture through the
  body. The whole vehicle, structurally, which is what the line says.

**A starburst was drawn for Major and rejected: it read as a sun** at both 96px
and 30px, which is the same class of error as the wifi-signal icon in 3.9. Two
further candidates, a deeper front crumple and a folded-in front end, both lost
to the fracture because the fracture is the only one still visible at 30px.

The drawing grammar is unchanged from the chips throughout: a 24 viewBox, a 2
stroke, round caps and joins.

#### The band rhythm, and the white band this retires

**Nothing had to move.** Today's order and grounds: hero on ox, stat card on
white, services on silver, **We Fix It All on ink**, who we are on silver,
testimonials on ink, the one act band on ox, contact on ink, FAQ on silver.
`#who-we-are` sits on silver between this band and the ink quote band, so the
adjacency the brief expected does not exist.

**What the change fixes is a palette inconsistency.** The section was
`.band-panel`, which is `--panel`, which is `#FFFFFF`: a second white band on
a page whose palette note allows exactly one, the stat card. Putting this
section on ink retires it.

**`/collision-repair/` still carries two `.band-panel` sections**, so the same
inconsistency is still live on that page. Not touched here, because that page's
copy is approved and this was not the brief. **Noted so it is not lost.**

#### Motion, and what was deliberately not taken

**The rule sweep only.** Each item's `::after` goes from the quiet 28px mark to
full width on hover, on the same 260ms clock and easing as every card on the
site, in silver because oxblood is invisible against this band. **The lift's
3px rise and its ink shadow are absent on purpose**, because the brief bans
the float. Hover-only behind `@media (hover: hover)`, and since only width and
opacity move the state still answers under `prefers-reduced-motion`.

#### The phone, and the one thing to flag

**The section is 1530px tall at 390**, up from 1504 before the revision,
because every item now carries a line. Against the 604px usable height
recorded in `scripts/mobile-check.md`, which is a 390x664 viewport less the
60px fixed call bar, **that is 2.53 screens, so it still eats more than two.**
Flagged as instructed and not changed, because one column at 390 is the
client's sizing.

What it costs and what it does not: the render is cheap there, because a
2.74:1 asset in a 350px column is only 129px tall, so the height cap the brief
asked for turned out to be unnecessary rather than skipped. The rest is the
eight items themselves. **Two columns at 390 would cut it to four rows and
land near 900px**, if the height matters more than the single column does.
Measured at 1440 for comparison: 1053px, four across in two rows, no
horizontal overflow at either width.
### 3.23 Real Repairs: the first real photographs. BUILT 2026-09-17, REVISED 2026-09-17

Five before and after pairs of customer vehicles, directly after We Fix It
All, on silver. **The claim is in the band above and the evidence is in this
one**, which is the only reason for that placement.

**REVISED THE SAME DAY ON THE CLIENT'S RULING, after seeing it live: a pair
shows BOTH frames at once, before beside after, and the tap-to-crossfade is
retired.** The section is now static. What changed is the arrangement, the
interaction and one sentence of the note; **no asset changed**, and the ten
frames, their redactions and the pipeline that made them are untouched. The
revision is recorded in place below, under the mechanism, the layout, the
chips and the note, rather than appended as a second account.

#### Provenance, which is the whole point

**The shop's own photographs of its own customers' vehicles, supplied by Greg
on 2026-09-17.** Not stock, not licensed, not generated. This is the first
real photography on the build and it closes the showstopper 3.17 has been
carrying since 2026-09-05.

The ten frames arrived as platform-hosted files, and their metadata was read
before anything was done to them: **no GPS and no EXIF in any of the ten**,
already stripped by whatever they passed through. That was checked, not
assumed, and it is checked again on the output.

**One thing the owner still has to confirm**, and it is in section 5:
**whether the shop has permission to publish photographs of customers'
vehicles**, and what its practice is. The vehicles are identifiable by make,
model and colour even with plates gone. Nothing here is a person, a name or a
date, but a customer's car outside a body shop is still their car.

#### Redaction: three regions, destroyed rather than softened

**All ten frames were inspected at magnification** before the list was
written. Three carry identifying numbers:

| Frame | What | Result |
|---|---|---|
| `job4-after` Murano | Rear plate at the left edge, characters and registration sticker legible | 52x126px, local detail 13.2 to 1.6, **12% left** |
| `job3-after` BMW | Green Pennsylvania inspection sticker on the windshield, characters legible | 80x36px, detail 6.3 to 0.9, **15% left** |
| `job5-after` Mercedes | Rear plate in shadow, faint, registration sticker still visible | 100x43px, detail 2.4 to 0.3, **14% left** |

**The other seven are clean, and there is a reason rather than luck.**
Pennsylvania issues rear plates only, and five of the remaining frames face
forward. The Jeep's before frame has its entire rear clip removed, plate mount
included. Background vehicles were checked in every frame: a truck flank, a
USPS van, a silver coupe's nose, a distant fence line, none with a readable
plate.

**The method is pixelate then blur, in that order**, and the order is the
argument. Averaging into large blocks throws the information away; the blur
afterwards only stops the blocks reading as a deliberate mosaic. A Gaussian
alone can sometimes be partly undone and a plate is not the thing to be
clever about. `scripts/prepare-repair-photos.py` measures local detail inside
each box before and after and **fails the export** if more than 25% survives.

#### Metadata: stripped structurally, because re-encoding adds it back

**`sips` writes metadata INTO its output.** Re-encoding produced an APP1 Exif
block, an APP1 XMP packet, an APP13 Photoshop block and an APP2 ICC profile,
none of which was in the input. So every APP1 through APP15 segment and every
comment is walked and dropped, leaving APP0 JFIF and the coding markers.
**All ten finished frames carry no metadata segment at all.**

**The first version of that check was wrong in both directions**, and both are
recorded because both are instructive. It counted the string "exif" in the
file, which cannot tell a harmless orientation tag from a GPS record and
false-positived "gps:1" on a frame whose metadata was clean. Rewritten to walk
the marker segments, it then reported APP0 JFIF as a survivor and **failed all
ten frames, which is a check calling its own correct output a defect**. APP0
JFIF is the density header every baseline JPEG carries; it identifies nobody
and it is kept on purpose.

#### Sizing, and what it cost

```
job1 Jeep       960x720    104 + 98 KB    copied and stripped, NEVER re-compressed
job2 Dodge      960x540    119 + 149 KB   before copied, after re-encoded q57
job3 BMW        766x574    149 + 135 KB   width stepped down, see below
job4 Murano    1050x787    140 + 147 KB   q60 both
job5 Mercedes  1050x590    142 + 123 KB   before cropped to 16:9, q60 and q58
                          1312 KB total, ten frames, every one lazy-loaded
```

**Three frames are copied and stripped rather than re-compressed.** A frame
with no crop, no redaction and no resize gets its metadata removed and nothing
else, because re-encoding an already-compressed photograph only compounds the
loss. The first run re-encoded a 98KB source into a **139KB** output at
quality 68, which is worse on both counts, so no output may now exceed its
own source's size.

**job3 is the one pair that paid for the budget in sharpness.** The BMW's
before frame is foliage, gravel and a chain-link fence, which is JPEG's worst
case: 154KB even at quality 40. Rather than ship quality 40 photography, the
script steps the **pair** down in width until the budget holds at quality 52
or better, and job3 landed at 766px for a 526px card, about 1.46x rather than
2x. **Width steps apply to the pair, never to one frame**, or the crossfade
would stop registering.

**job5's before was cropped 4:3 to 16:9 to match its after**, 18.5% off the
top and 6.5% off the bottom. What came off is building and sky above and
gravel below; the crushed bumper, the torn quarter panel and the dislodged
tail light are all still in frame. Verified by eye after the crop. **No crop
on this site hides damage or flatters a repair.**

**Rounding put that pair one row apart**, 591 against 590, so the taller frame
is trimmed a single row. Both frames of every pair now ship at identical pixel
dimensions, which is what keeps a dissolve from drifting.

#### The mechanism: RETIRED 2026-09-17, and both frames now show at once

**The client's ruling, after seeing the section live: show the before and the
after together.** A pair is two photographs side by side on a desktop row,
before left and after right, and stacked before above after on a phone. The
comparison is made by the layout, so a reader makes it without doing
anything, and there is nothing to discover.

**What went, and it went rather than being switched off**: the `[data-ba]`
block in `site.js` whole, the `.is-ready` and `.is-after` stacking rules, the
`role`, `tabindex`, `aria-pressed` and `aria-hidden` machinery a two-state
control needs, the 24px drag threshold and the swallowed click after a drag,
and the `--ar` custom property the stacked layout needed on each figure. A
tombstone at the block's old line in `site.js` says what stood there and why
it does not any more.

**THE SECTION NOW HAS NO MOTION AND NO STATE.** It carried kind-one motion, a
400ms dissolve that fired on a reader's tap and never on its own. Nothing
fires at all now. It has no hover state either, and that is deliberate rather
than left out: these are photographs and not links, and a shape that answers a
pointer is telling a reader it can be clicked.

**IT NEEDS NO JAVASCRIPT-OFF FALLBACK, BECAUSE IT NEVER LEAVES NORMAL FLOW.**
The ten frames are ten images in the flow of the page, each with its own chip
and each still lazy-loaded. The fallback the crossfade needed retired with the
crossfade: there is no enhanced state left for a reader without JavaScript to
miss. Measured after the change, on both pages at both widths, with scripting
**on**: no `[data-ba]`, no `role`, no `.is-ready` and no `.is-after` anywhere,
no script error, and no image in the section at anything but full opacity and
full visibility.

**The retired argument, kept because it is still true of a crossfade.** The
pairs were shot from different angles, distances and seasons, by whoever had a
phone. The Murano's before is a close-up of one door; its after is the whole
car from behind. **A wipe slider would have read as broken halfway through
every drag**, because there is no shared frame to wipe between, which is why
the retired interaction was a dissolve. Showing both frames at once answers
the same problem without asking the reader for a gesture.

#### The chips, measured over the photographs

`Before` and `After` in the established chip grammar, top left, **with one
change: the border is `--ink`, not `--rule`.** The standard chip's `--rule`
hairline measures 1.46 against its own white fill and cannot edge a shape
sitting on an unknown photograph.

**Text is photo-independent by construction.** The fill is opaque, so no
photograph pixel is ever under a glyph: `--ink` on `--panel` is **17.33:1**
against a 4.5 floor and a 7 target, whatever the picture does.

**The chip as a shape was measured on the rendered page, locally.** At each
position along the perimeter the transition a reader sees is photo, then ink
border, then white fill, and the boundary is visible there if **either** tone
clears 3:1 against the photo pixel beside it.

**RE-MEASURED 2026-09-17 ON THE NEW LAYOUT, because the chips moved.** The
positions are a property of the layout, not of the chip: side by side at 532px
a chip sits over different photograph pixels than it did stacked. Both widths,
all ten chips, every position around every perimeter, sampled 2px outside the
outline:

```
1440   1820 positions over ten chips   0 below 3:1   worst 4.16:1
 390   1820 positions over ten chips   0 below 3:1   worst 4.17:1
which tone carries it                  fill on 4 chips, edge on 6, at both widths
internal edge, photo-independent       17.33:1
```

**The measurement is calibrated rather than assumed.** A screenshot clip is
not guaranteed to start on the page pixel it was asked for, and a silent
offset between page coordinates and image coordinates samples the wrong pixels
while looking perfectly healthy. Two magenta marks at known page positions
make the mapping a measurement: both landed where they were put, so page
coordinates and image coordinates are 1:1. The page was served over HTTP for
this, not opened from disk, because `file://` blocks the self-hosted fonts on
CORS and a chip measured in fallback type is a chip of the wrong width.

**The first version of this measurement was wrong and is recorded as such.**
It took the minimum contrast across the whole ring around each chip and
reported all ten as failures. On a photograph spanning luminance 0.004 to
0.998 there is always some pixel matching any given colour, so that test is
unpassable for any chip on any photo. Contrast for a shape is a **local**
question, and the fix was to ask it per position.

#### Layout, with the numbers

**REVISED 2026-09-17: one pair per row, five rows.** Before left, after right,
equal widths, the caption under the row it describes. Two pairs across a
desktop row would put four frames across and halve every photograph, and the
damage is the evidence the section exists to show. The aspect-ratio pairing
the two-up grid needed is gone with it: each row is as tall as its own
photographs.

**Equal heights come free, and that is not luck.** Both frames of every pair
ship at identical pixel dimensions, which
`scripts/prepare-repair-photos.py` enforces and fails on, so equal widths give
equal heights with no aspect-ratio box, no `object-fit` and no crop at render
time.

Rendered and measured over HTTP, so the self-hosted faces are the ones in
play:

```
1440   five rows, frames 532x299, 532x299, 532x399, 532x399, 532x399
       16px between the two frames of a pair, 44px between rows,
       53px caption under each row
       section height 2640px   (it was 1718 crossfaded, 2833 with JS off)
 390   one column, frames 350 wide and 197 to 263 tall, before above after
       12px between the frames of a pair, 36px between rows
       section height 3157px
overflow   document scrollWidth equals the viewport at both widths, on both
           pages: 1440 and 390, nothing scrolls sideways
images     all ten still loading="lazy", all ten still carrying alt text,
           68 to 110 characters
```

**The phone stacks the pair rather than shrinking it.** Two frames side by
side inside a 350px column are about 165px wide each, which buries a crease in
a quarter panel. Below 600px the pair reads top to bottom instead, before
above after, both chips, one caption. The breakpoint is 599px, which is the
one this stylesheet already uses for a phone.

**The Jeep is the fifth card on purpose.** Its before frame is mid repair,
with the rear clip off and the glass out, so it goes last and its caption says
so rather than dressing it as finished damage.

**A featured pair with selectable thumbs was rejected, and the JS-off rule is
why.** Every frame has to be reachable with scripting off, so all ten render
either way; a featured layout would then be one large pair plus nine images a
reader cannot select, which is worse than a grid. Paging fails the same test
and hides evidence behind a control.

#### Captions and alt text

**Model and damage class only.** No accident stories, no customer details, no
dates, nothing about fault or insurance.

```
Dodge Grand Caravan      Front-end collision
Mercedes CLE 300         Rear-end collision
BMW 5 Series             Front-end collision
Nissan Murano            Door dents
Jeep Grand Cherokee L    Rear end, before frame shown mid repair
```

**The damage classes are read off the photographs**, which is a judgement and
is flagged as one: a crushed front bumper is a front-end collision on any
reading, but the class is our description of an image, not something the shop
has published about that job. The Jeep's caption deliberately describes the
frame's state instead of a class, because its damaged parts had already been
removed when the photograph was taken and naming a cause would be inventing
one.

Alt text names the vehicle, its colour and the specific visible damage, and
the after frames say "the same" so the pairing is explicit to a reader who
cannot see them.

#### The heading, the kicker and the note

**H2 "Real Repairs"**, with the working title kept because it is accurate and
plain. **Kicker "Restored to pre-accident condition"**, which is published
copy: `/collision-repair/`'s own FAQ says "restore your vehicle to its
pre-accident condition".

**A short note under the head**, and every clause of it is a fact the site can
stand behind. **Revised 2026-09-17 with the interaction it instructed:**

```
before  Vehicles repaired at our Southampton shop. Tap or click a
        photograph to see it finished. License plates are blurred.
after   Vehicles repaired at our Southampton shop. License plates are
        blurred.
```

The middle sentence was the instruction for the retired crossfade, and an
instruction to tap a photograph that does nothing is worse than no note at
all. What is left is the owner-supplied premise of the section and the
disclosure of what we did to the pictures. **The heading, the kicker and every
caption are unchanged.**

#### The band rhythm, reported, and RESOLVED 2026-09-17

```
hero ox | stat card white | services silver | We Fix It All INK |
Real Repairs SILVER | who we are SILVER | testimonials ink |
act band ox | contact ink | FAQ silver
```

**This puts two silver sections next to each other**, Real Repairs and who we
are, which is new on this page. It breaks no written rule: the rules are that
white is exactly one band and oxblood is two, and silver is not a band at all,
it is the page. Consecutive silver sections read as continuous page rather
than as a contrast switch, and each carries its own centred section head with
`--pad` above and below. **Recorded because it is a change in rhythm, not
because it is a defect.** The alternation that matters, ink against page, is
intact on both sides.

**The client ruled on it on 2026-09-17 and it is no longer the rhythm.**
`#who-we-are` moved to the oxblood ground, so the two adjacent light bands are
one light band and one dark one. The new rhythm, the amendment it needed and
the measured type are in **3.25**.

### 3.24 The oxblood divider under the header. BUILT 2026-09-17

**The client's ruling, from the live staging pages: a red divider between the
nav and the page, matching the brand accent the shop's live site carries.**
Implemented as a `border-bottom: 4px solid var(--ox)` on `.nav`, which
replaces the 1px silver hairline that was there.

**It is the header's own border, so it rides with the header.** The header is
sticky, so the divider is under the nav at every scroll position instead of
being a rule at the top of the document that scrolls away. Site-wide: both
pages and `templates/service-page-template.html` share one `.nav`.

**It is recorded in the palette note as a SANCTIONED CHROME ACCENT.** Oxblood
means act, and this is oxblood doing something that is not an act: it is a
ground element, chrome, like the scrim. It asks for nothing and cannot be
clicked. **It is `--ox` and not `--mark`:** the logo's red stays mark-only,
because #E92424 measures 3.94 on the silver ground and the two reds are two
tokens for exactly this reason.

#### The fold table, re-run, because the divider costs 3px everywhere

The sticky header is in flow, so every pixel the border gains comes off the
fold budget of every page under it. **1px to 4px is +3px, and it lands on all
five viewports.** Measured with the staging banner hidden, which is the
post-cutover state and the state the standing table is in. The budget is the
viewport less the 60px fixed call bar on a phone, and the whole viewport on
desktop where the call bar is not displayed.

```
HOME                       nav   hero depth  CTA ends  budget  clears by
1440 x 900                  96      566        556      900      344
1920 x 1080                 96      566        556     1080      524
 430 x 745                  68      560        556      685      129
 390 x 664                  68      541        537      604       67
 360 x 640                  68      582        578      580        2

/collision-repair/         nav   hero depth  CTA ends  budget  clears by
1440 x 900                  96      562        492      900      408
1920 x 1080                 96      562        492     1080      588
 430 x 745                  68      560        576      685      109
 390 x 664                  68      505        523      604       81
 360 x 640                  68      503        521      580       59
```

**360x640 went from clearing by 5px to clearing by 2px, and 2px is the floor
the ruling set, not below it.** So the divider ships at 4px and nothing was
reclaimed from the hero copy block. **This is the number to watch:** the
tightest phone in the record now has two pixels of headroom, and the next
thing that grows the header or the hero copy by even 3px puts the CTA under
the fold. Thinning the divider to 3px would buy one of those pixels back and
is a one-character change if it is ever wanted.

**The staging state was measured too**, because it is what a reviewer sees
today and it is 57px worse: the banner's sentence wraps to two lines on a
phone. The Call button is the one that has to clear, and it does.

```
WITH the staging banner    banner  Call button ends  budget  clears by
 430 x 745                   57         613          685       72
 390 x 664                   57         520          604       84
 360 x 640                   57         561          580       19
```

#### What the divider reads against, measured

**--ox on --ink is 1.47**, so the divider does not read against the header
above it and is not meant to: what it separates is the header from the PAGE.
So it was measured against the strip directly below it, sampled across the
full width at four scroll positions on both pages.

```
under the divider                     worst   mean    best
the silver page, the white card                       10.50 to 11.80
the hero photograph, 1440 home         1.00   1.61     5.53
the hero photograph,  390 home         2.64   6.24    11.32
an ink band under a sticky header      1.07   1.48     4.53
AN OXBLOOD BAND under a sticky header  1.00   1.43    10.50
```

**IT DISAPPEARS OVER AN OXBLOOD GROUND, AND THAT IS REPORTED RATHER THAN
QUIETLY SHIPPED.** Ox on ox is 1.00, which is the same colour. Two places
this is visible today: the header floating over `#start` or `#who-we-are` as
a reader scrolls, and **the top of `/collision-repair/` at desktop**, where
the ox hero scrim is near-solid under the copy and the divider merges into it
for the left part of the frame. At 390 the same page reads the divider
clearly, because the phone scrim anchors to the bottom and the top of the
frame is clear photograph.

**It is not a regression.** The 1px silver hairline it replaced was 16% silver
over ink, and it vanished over an oxblood band too; the divider is far more
visible everywhere else, 10.50 against the page where the hairline was a
whisper. But the site's own law says never to put a dark shape on a dark
ground without an edge, and this is that shape.

**The one-line answer, if the client wants it**, is a paper hairline under the
divider: `box-shadow: 0 1px 0 rgb(var(--silver-rgb) / .16)` on `.nav`. A
shadow does not participate in layout, so **it costs zero fold budget** and
the 2px at 360x640 stands. It is not applied: the ruling said a 4px ox border
and nothing about a hairline, and a design element nobody asked for is not a
thing to add quietly.

### 3.25 Family Owned moves to the oxblood ground. BUILT 2026-09-17

**The client's ruling, resolving the flag 3.23 raised when Real Repairs
shipped**: Real Repairs and `#who-we-are` were both silver and read as one
long run of page. `#who-we-are` now carries `class="dark field-ox"`, which is
the same 104-degree gradient the act bands wear, not a copy of it.

#### The amendment, which is about what the old rule was ever describing

The rule read: oxblood means act, a `.field-ox` band always carries the CTA
row, there are exactly two on a page and one on the front door. **It was
written about the bands that ASK FOR SOMETHING, and it still governs them
exactly.** `#start` remains the only oxblood band on the homepage that asks
for an action; it carries the only CTA row on an ox ground on this page.

**What is new is oxblood as a prose section's ground.** `#who-we-are` carries
no CTA row, no button and no link. It joins the recorded section-background
gradient exception rather than creating a second one: same class, same stops,
same fallback chain, and the dark-ground act rule still waiting if a button
ever lands in one.

**The test, if a third case ever comes up: does the band ask the reader to do
something?** If it does, it is an act band and the act-band count governs it.
If it only says something, it is a ground. That sentence is now in `site.css`
beside `.dark`, where someone adding a section will meet it.

#### Type on the new ground, measured rather than assumed

Headings and the kicker take `--silver` from `.dark`; the body takes
`--silver-2`, which is the same hierarchy the ink bands already use, through
one new rule: `.dark .prose p`.

**Measured by the readability amendment's method**, on the real render at both
widths: the page rendered, then rendered again with the section's copy at
`visibility: hidden` so the layout holds and the glyphs go, each text node's
**glyph runs** taken via `Range.getClientRects()` rather than its block box,
and every composited pixel under those runs sampled against the element's own
computed colour.

```
element                colour        size      1440     390    floor  target
h2.sec-title           --silver      36.8px   10.50   10.50     4.5      7
p.sec-sub              --silver      13.4px   10.50   10.50     4.5      7
p, body copy           --silver-2    17px      7.34    7.34     4.5      7
worst under any glyph run on this band                 7.34
```

**The worst pixel is the same at both widths and that is arithmetic, not
coincidence.** The gradient's brightest stop is `--ox` exactly, so `--ox` is
the worst ground any glyph can sit on, and the ends only get better: 12.39 on
`--ox-dk` and 13.68 at the deep end. Where the type falls across the band
changes with the width; the worst case cannot.

**There is no act button in this section**, so the dark-ground act rule has
nothing to apply to here. If one ever lands, `.field-ox .btn` already fills it
with ink and gives it the paper hairline, because the rule is keyed to the
ground rather than written per section.

#### The hero's "no secondary tone on ox" rule was SCOPED, not relaxed

`site.css` said, in the hero note: on an ox ground there is no secondary text
tone, because `--silver-2` tops out at 7.34 there. **That is right about the
hero and the reason is a photograph.** 0.34 of headroom over a 7 target is
spent by the first photograph pixel showing through a scrim; it measured 6.57
in the hero, which is why the ox hero's lead and breadcrumb are `--silver`.

**A band has no photograph under it.** 7.34 is the number and nothing takes it
down, which the render above confirms rather than assumes. The sentence now
reads: on ox **over a photograph** there is no secondary tone. Recorded here
because narrowing a written rule is exactly the kind of change that should
never happen quietly.

#### The full band rhythm, top to bottom

```
hero            photograph under an INK scrim
proof           WHITE stat card, overlapping the hero's seam
services        silver
We Fix It All   INK
Real Repairs    silver
who we are      OX  <- moved 2026-09-17, asks for nothing
testimonials    INK
start           OX  <- the act band, the only one that asks
contact         INK
FAQ             silver
```

**No two touching sections share a ground now**, which the old rhythm could
not say. The page alternates page, dark, page, dark from the services grid to
the footer, and the two oxblood grounds are separated by an ink band. **One
act band, two ox grounds, one white band, and silver is the page rather than a
band.**


### 3.26 The brand strip: twelve marks, drifting. BUILT 2026-09-17

The live homepage's manufacturer carousel, migrated on the client's ruling and
placed directly after the testimonials, on silver, between the ink quote band
and the oxblood act band.

#### The finding first, because it decided what shipped

**The live strip shows fourteen marks; the live prose says a dozen.** The extra
two are RAM and Fiat. The full record of the discrepancy, what this build does
about it and what one owner answer would change is in **4.1**, and the question
is **5.6b**. In short: **the strip ships the twelve the site claims in words**,
and a check now makes the marks, the words and the schema agree or fail.

#### The check, which is the review count's argument in a second key

`scripts/audit.py` carries `BRAND_COUNT = 12` and `BRANDS`, reads:

```
marks    the <img> elements in the one .brandtrack that is NOT aria-hidden
text     every count claimed in visible text, comments and scripts stripped
schema   every count claimed inside <script type="application/ld+json">
```

and **fails as a CRITICAL when any two disagree**, with the constant counting
as one of the voices so that a lone page drifting from it still fails.

**It reads "12", "12+", "a dozen" and "Twelve" as the same number**, because
they are the same claim. Whether the site should say "12" or "12+" at all is a
different question and it stays in 4.1 where the owner can answer it.

**The duplicate tracks do not count.** The marquee ships the marks three times
so the drift has no seam; two of those tracks are `aria-hidden`. Counting them
would report thirty-six brands, which is why the count comes from the one track
a screen reader is offered.

**Twenty assertions in `scripts/test-audit-checks.py` hold it**, including the
live site's own state as a fixture: fourteen marks over a sentence saying a
dozen is a critical. The real page is checked too, because a fixture that
passes while the page fails is a fixture that lies. Proved end to end as well:
a thirteenth mark added to the shipping page made `--strict` exit 1 and the
report named the strip.

#### The assets

**The client's own published files**, read off `https://tricountycollision.com/`
on 2026-09-17, one per brand, all under `/wp-content/uploads/`.

**Provenance read before anything was done to them**, through the same reader
the audit uses, and `scripts/prepare-brand-logos.py` refuses to process a file
that carries an AI tell: nine name Adobe Photoshop CC 2018 in the tool field,
three carry no tool at all, **none carries a DigitalSourceType and none names a
generator**. Clean, and the outputs carry no metadata at all because the writer
emits IHDR, IDAT and IEND and nothing else.

**One treatment, and it is an alpha mask rather than a picture.** Luminance
becomes opacity: the white ground goes transparent, the darkest ink goes
opaque, and everything between lands between, so a logo's internal tones
survive. The Ford script stays legible inside its oval because the white script
is transparent rather than white.

**The pixels are black and the stylesheet owns the tone.** `--brand-ink` is one
number in `site.css`, not twelve baked greys in twelve files, and the marks
carry no ground, so a future change to `--silver` cannot leave twelve
rectangles behind. The palette note records that this exact mistake has been
made on this site once already, with ten rgba() washes.

**Measured on the render:** at `.72` the darkest composited pixel in the strip
is rgb(67,68,68), **8.70:1 against `--silver`**, well past the 3:1 a graphic
needs.

```
brand      source     trimmed    shipped     bytes   note
Subaru     164x158    164x82     120x60       4576
Nissan     164x158    156x132     71x60       3835
Kia        199x158    184x96     115x60       5126
Jeep       199x158    194x85     137x60       3168
INFINITI   199x158    199x96     124x60       2981
GM         153x158     94x92      61x60       2629   badge cropped to its mark
Hyundai    208x158    189x114     99x60       4545
Ford       214x158    204x77     159x60       7878
Dodge      138x160    137x155     53x60       2153
Chrysler   161x161    161x56     161x56       5762   shorter than target, NOT upscaled
Acura      199x158    175x99     106x60       3029
Honda      199x158    184x121     91x60       3758
TOTAL                                        49440   budget 153600
```

**One source is a badge rather than a mark, and it was cropped to its mark.**
The GM file is the "GM CERTIFIED Collision Repair Center" badge: the GM box,
ten empty rows, then two lines of fine print. At 30px that print is three
pixels tall and reads as a grey smudge, which is worse for GM than for any
other brand in the row. **It removes no claim**: "factory-certified for 12
vehicle brands", GM among them, is published in words on `/collision-repair/`
and is in the claims list. A claim belongs in text a person and a crawler can
both read, not in three pixels.

**Chrysler ships 4px shorter than the others at 2x** and the script says so
rather than upscaling it. The stylesheet sets the height, so it renders at the
same 30px as everything else; what it gives up is 7% of its own resolution.

#### The marquee, and the motion law it amended

**This is the motion law's fourth kind and the largest amendment the law
carries**, because "nothing loops" was written twice in `site.css`. It is dated
in the stylesheet header and in `CLAUDE.md`. **One strip, never a second one**,
and anything else that wants to loop needs its own dated amendment.

**Why this one earns it.** Twelve marks cannot be shown legibly across a phone.
The alternatives are worse than motion: shrink them until nobody recognises
them, or hide some behind a control, which is the failure the Real Repairs
pairs were rebuilt to avoid. The drift shows every mark at full size at every
width.

```
one strip     #brands only
~40s          a cycle: a drift, not a carousel
transform     the only property that animates
pauses        under a pointer, and on focus-within
stops         entirely under prefers-reduced-motion
no JS         none at all, so scripting off renders the same page
```

**The resting state is the base and the motion is the addition**, the same
construction the hero entrance uses. The rules outside the media query lay the
twelve marks out as a wrapped, centred, static row with the duplicate tracks
`display: none`. Reduced motion, an old browser, a half-loaded stylesheet or a
browser that never heard of `@keyframes` all rest with all twelve visible.
**Nothing here is ever hidden waiting for an animation.**

**The geometry is arithmetic rather than taste.** Three identical tracks,
translated by exactly one third of the marquee's width, which is one track plus
one gap, so the second track lands precisely where the first began and the loop
has no seam. The gap is the track's own `padding-right` rather than a flex gap
between tracks, because one third has to be one whole unit and a gap between
units is not inside one.

**Three tracks and not two, and this is the number that decides it.** What is
on screen at the end of a cycle is the total width less one unit, so two tracks
cover a viewport only while one unit is wider than it. A unit is 654px of marks
plus twelve gaps: **1866px at 1440 and 2094px at 1920**, which covers those and
not a 2560 monitor. Three tracks cover two units, 4188px, which covers any
screen this site will meet. The third costs twelve `<img>` elements the browser
has already downloaded.

#### Measured on the page

```
1440   section 127px tall, strip 30px, three tracks of 1864px, gap 101px
        marks 27 to 86px wide, all exactly 30px tall
 390   section  83px tall, strip 30px, three tracks of 1134px, gap 40px
reduced motion, 1440   section 179px: two centred rows, all twelve visible
reduced motion,  390   section 187px: three centred rows, all twelve visible
pointer on the strip   paused        pointer off again   running
a focusable element inside            paused
overflow    document scrollWidth equals the viewport at both widths
images      all 36 lazy, alt text is the brand name and nothing else
```

**The pause was verified on the rendered page and the first two runs were
wrong.** `scrollIntoView()` parks the strip directly under the sticky header,
so the synthetic pointer was landing on the nav and the strip never saw it.
Scrolling the strip to the middle of the viewport first, the pointer pauses it
and moving away resumes it.

#### The copy, the heading it does not have, and the rhythm

**No heading, like the live site.** The stat band already carries the
twelve-brands claim in text and `/collision-repair/` names every brand in
prose. **The strip is recognition, not a second claim**, so it gets no H2 and a
plain `aria-label="Manufacturer logos"` that describes what it is without
making a claim of its own. **Alt text is the brand name and nothing more.**

**The band rhythm as it landed**, top to bottom:

```
hero            photograph under an INK scrim
proof           WHITE stat card, overlapping the hero's seam
services        silver
We Fix It All   INK
Real Repairs    silver
who we are      OX   (2026-09-17, asks for nothing)
testimonials    INK
brands          silver  <- new, and the only silver band between two dark ones
start           OX   (the act band, the only one that asks)
contact         INK
FAQ             silver
```

**No two touching sections share a ground.** The strip is a thin silver breath
between the ink quotes and the oxblood ask, which is what a recognition band
should be: it separates the two dark bands that would otherwise touch.


### 3.27 One job each: the act band asks, the contact band informs. 2026-09-17

The copy pairs are in **1.27**. This is what the change means for the page's
structure and what it does not touch.

#### The diagnosis was precise, and it is worth keeping

Two bands in a row read as redundant. The instinct in that situation is to
merge them or to delete one, and both would have been wrong: **the ask was
duplicated, the information was not.** The contact band carries the address,
the phone, the email and the hours, and none of that appears anywhere else on
the page as a block a reader can scan. What it also carried was a second ask,
in a quieter voice, immediately after the band whose whole job is to ask.

So nothing merged and nothing was deleted. **Each band got one job.**

```
#start    asks        the restore line, "Estimates are free and there is
                      no obligation", Call and Email. UNCHANGED, and still
                      the page's one conversion moment under the act-band
                      rule: one oxblood act band on the front door.
#contact  informs     address, phone and email, hours, and one line for
                      the reader who would rather write than call.
```

#### What was checked rather than assumed

**The NAP is the thing a change like this can quietly break**, because the
phone and the email were deleted from a sentence. They were deleted from a
*sentence*; they live in the *grid*, tappable, spelled the canonical way, and
the grid was not touched.

```
NAP address on /                canonical: 995 Jaymor Rd, Southampton, PA 18966
tappable phone/email mentions   14 -> 12, which is exactly the two removed
                                duplicate links and nothing else
data-pending-href to /contact-us/   still present, still pending, still seen
                                by the link test's second direction
audit, both pages               95/100, sameAs the only warning, 0 critical
```

#### The same shape exists on /collision-repair/ and in the template, and it
#### was NOT changed

`/collision-repair/` carries the same heading, "Contact Us for Your Free
Estimate", and the same closing line in a shorter form, and
`templates/service-page-template.html` carries a closing line of its own.
**The ruling named the homepage's two bands, so the homepage is what changed.**

It is also not obviously the same problem there. The service page has **two**
act bands rather than one, a different rhythm, and a reader arrives at its
contact band having scrolled through a much longer page. Whether the same
diagnosis applies is a judgement about that page, and it is the client's to
make rather than a consistency edit to make on his behalf.

### 3.28 The eight damage marks become a licensed set. BUILT 2026-09-22

The eight hand-drawn glyphs in We Fix It All are retired and replaced with
marks from a licensed icon set, plus three matched redraws for the concepts
the set does not contain. Greg licensed the set and ruled the approach;
every number below was measured here.

#### The icon saga, in order

**The services set was evaluated and archived.** `AdobeStock_57374576`, "Big
set car repair icons", 137 marks, provenance clean: Illustrator CS6, 2013, no
AI markers, intact metadata. **Evaluated in the strategy chat on 2026-09-18
and rejected there**, on two grounds: concept coverage, because six of our
eight damage types have no mark in it, and at-size legibility, because its
wide two-car compositions are unreadable at 30px. That evaluation is Greg's
and it is recorded here as history. **It was not re-run**, and nothing in this
build depends on it.

**The damage set was licensed and adopted.** `AdobeStock_1964340052`, "Car
Accident", 36 editable line icons, licensed 2026-09-22.

#### The provenance, and the limit under it

Read before a line was built on it, through `scripts/audit.py`'s own reader,
which is the standing step rather than a favour to a file somebody already
trusts:

```
AdobeStock_1964340052.ai   2,030,991 bytes
  IPTC DigitalSourceType   (none declared)
  XMP CreatorTool          Adobe Illustrator CC 2015 (Windows)
  C2PA manifest            none, referenced or embedded
  generator string         none anywhere in 2MB
  VERDICT                  clean, no AI tell
```

That confirms the strategy chat's pre-check against the same reader the build
uses. **The .ai is not in this repo** and never was: it stays outside like
every licensed source, and `scripts/prepare-damage-icons.py` takes its path as
an argument.

**The limit is real and this is where it is written down.** The eight ship as
**inline SVG**, which carries no metadata, so there is no derived file for the
audit's provenance reader to scan and **a clean audit says nothing about
them**. The reading above is the floor under them. This is the same
arrangement the car render has in 3.22, and it is stated for the same reason:
a gate that cannot fire should not look like one that passed.

#### What the file actually turned out to be, and what it cost

**The marks are filled outlines, not strokes.** The content stream carries
**253 fill operators and zero stroke operators**, and no line-width setting
anywhere. Dropped into the old rule, which was
`fill: none; stroke: var(--mark); stroke-width: 2`, every one of them would
have rendered as **nothing at all**. The brief described the set as "stroke
style matching the section's existing grammar"; it does not, and the grammar
had to move rather than the artwork.

**The set carries ONE stroke weight**, recovered by measuring dark-run widths
in a large render and dividing by each mark's own normalising scale:

```
icon 19   10.08 set units        icon 07   9.61        icon 25   9.61
```

taken as **9.8 set units**.

#### The size, which is a derivation and not a preference

The first pass normalised each mark to its own bounding box, which destroyed
that single weight: the two-car marks came out at 0.40 units and the
single-subject ones at 0.75. **That was an error in the pipeline, not a
property of the set**, and it is recorded because the first round of
judgements was made on it.

At the recorded 30px the set's own stroke is **0.82 device px**. Against the
site's other icons:

```
chips        17px at stroke-width 2.1 on a 24 viewBox   1.4875 device px
this band    30px at stroke-width 2   on a 24 viewBox   2.5000 device px
set at 30px                                             0.8167 device px
```

So 30px was never available: the marks would have shipped as hairlines, 45%
lighter than the chips and 67% lighter than the glyphs they replace.

**The set's own stroke equals the chip stroke at 54.64px per 360 set units.**
The band ships **56 per 360**, which is 0.155556 px per set unit and puts
every mark at **1.5244 device px, 2.5% off the chips**. Greg ruled on this
with the arithmetic in front of him.

**What that buys is not bigger icons, it is consistency.** The band's old
2.5px glyphs were the heaviest icons on the site and a recorded deviation from
the 17px chip scale. The band now joins the chip grammar instead of being the
exception to it.

#### Natural proportions, and the square box that was rejected

A square box forces the wide two-car compositions to shrink to fit, and the
shrink lands on their stroke:

```
icon 07   528 units wide   fit 0.681   stroke 0.68 of everyone else's
icon 08   618 units wide   fit 0.582   stroke 0.58 of everyone else's
icon 09   502 units wide   fit 0.717   stroke 0.70 of everyone else's
```

A 42% difference standing side by side in one row is visible, and no amount of
size fixes it, because the crowding is in set units and therefore
scale-invariant. **Every mark keeps its natural proportions at one scale
instead**, so the two-car marks are simply wider than tall and all eight carry
an identical 1.524px line. Greg ruled this too.

#### The mapping

| Item | Ships | Source | Alternative shown |
|---|---|---|---|
| Minor collisions | icon 08 | set | icon 07 |
| Major collisions | icon 06 | set | icon 21 |
| Cracked windshields | icon 01 | set | none |
| Broken side and rear glass | redraw | **matched redraw** | none in the set |
| Door dings and dents | **icon 20** | set | icon 25 |
| Bumper damage | **icon 26** | set | icon 04 |
| Scratched and chipped paint | redraw | **matched redraw** | none in the set |
| Hail damage | redraw | **matched redraw** | none in the set |

**Five from the set, three redrawn.** The four alternatives validated at size
and were not shipped; they are printed on every run of the pipeline so the
choice stays visible rather than becoming a fact nobody remembers deciding.

**Two were re-picked by the client on 2026-09-22**, off the numbered contact
sheet, after the first eight shipped: Door dings and dents moved from icon 25
to **icon 20**, and Bumper damage from icon 04 to **icon 26**. Both were
re-validated at the derived scale before they went in; the marks they replace
are now the alternatives above.

- **Minor collisions, 08 over 07.** Both are two cars nose to nose. 07 carries
  a burst between them and 08 carries light impact ticks. 08 ships because it
  is the lighter drawing, which is what "minor" means, and because it leaves
  the burst to Major, which sits directly beside it. **Both are nose to nose
  rather than rear-end**, which is what the brief called them; 09 is the actual
  rear-end mark and it is busier than either.
- **Major collisions, 06 over 21.** 21 is cleaner at every size and 06 is the
  densest mark shipping. 06 ships because it shows actual structural crush,
  which is what "frame straightening, structural repair and full panel
  replacement" claims. 21 is the one to take if the density ever reads as
  noise.
- **Door dings and dents, 20 over 25.** 25 is the car seen from above with a
  burst on the near side. 20 is a three-quarter car with the impact on its
  rear quarter and shake lines beside it, which localises the damage to a
  panel rather than to a whole flank. **The client's pick.**
- **Bumper damage, 26 over 04.** 04 is a front view with the burst below the
  front bumper. 26 is the close-up of two front ends meeting, cropped so the
  bumper line is the subject. **The client's pick.** Icon 31, the side view
  with the burst under the body, reads as undercarriage and was never in
  front.

**One thing the re-pick costs, flagged and not fixed.** Three of the eight are
now two-vehicle frontal impacts: **08** for Minor, two cars nose to nose with
light ticks; **06** for Major, two crushed fronts with a burst; and **26** for
Bumper, two front ends meeting with a burst. 06 and 26 carry the same burst
vocabulary and differ mainly in density. At the ruled scale they are
distinguishable, and the headings do the naming, but a reader scanning the
marks alone gets the same idea three times in a row of eight. Recorded rather
than changed, because the pick is the client's and it was made off the
numbered sheet with all 36 in view.

**Hail was a gate and the gate closed.** The brief made it conditional on an
impact-from-above mark reading honestly as falling objects at size. **There is
no such mark in the 36.** The nearest, icon 24, is a hazard triangle with
engine smoke. So hail went to a redraw rather than to a mark that would have
had to be argued into meaning.

#### The three matched redraws

Drawn in the set's own hand: the same 9.8-unit stroke, the same round caps and
joins, the same corner radii. **Two of the three are built on the set's OWN
car**, lifted whole from icon 29, so one hand appears across all eight by
construction rather than because somebody matched them up by eye.

- **Scratched and chipped paint.** The donor car untouched, plus one scratch
  and two filled flakes. **The scratch is a zigzag rather than a straight
  line**, because at a single stroke weight a straight line reads as a body
  crease, which the set's own cars already carry. The flakes are **filled**
  because a 10-unit dash is 1.6px at the ruled size and simply disappears.
- **Hail damage.** The same car dropped 78 units down the box, with six filled
  stones and six **slanted** travel lines above them. Stones are filled
  because an 18-unit ring at 9.8 of stroke has no hole left in it. The first
  pass put vertical lines directly above each stone and the pair read as a pin;
  the slant reads as travel.
- **Broken side and rear glass.** **A door, not the donor car, and that is a
  measurement rather than a preference.** The donor's rear side window is 65 x
  32 set units, which is **10.1 x 5.0 device px** at the ruled scale, and no
  crack survives that. It also has to read apart from icon 01, which is a
  cracked windshield sitting in the same row of eight. The wing mirror is what
  makes a door unmistakably a car door. **It is a different zoom level from the
  other seven, and that is the cost of the measurement.**

**Every placement on the donor was measured, not eyeballed.** The car's panel
between the wheels was probed row by row: solid beltline at y 69..75, free
from y 78..132 apart from the door-gap line, solid sill at y 135..141.
Everything added sits inside y 78..132. The first pass put the scratch at y 123..136 and it collided
with the sill.

#### What it costs, measured through the iframe method

`scripts/mobile-check.md` exists because headless Chrome will not lay a page
out below about 500px, and **this session walked straight into that trap**: a
`--window-size=390` render laid out at 500 and cropped to 390, text appeared
clipped mid-word, and it looked exactly like a horizontal overflow bug. It is
not one. Measured properly, in an iframe of the width being tested:

```
                       before      after     delta
1440   #what-we-fix      1053       1085       +32     4 across, 2 rows
 390   #what-we-fix      1530       1658      +128     1 column, 8 rows
```

The before figures match what 3.22 recorded to the pixel, which is the check
that the method is measuring the same thing.

**At 390 that is 2.74 screens against the 604px usable height, up from 2.53.**
The band already ate more than two and it now eats a little more. Flagged
rather than fixed, for the same reason 3.22 flagged it: one column at 390 is
the client's sizing. Two columns would still cut it to four rows.

**Neither width overflows.** `scrollWidth` equals the viewport at both, and
every item sits at L20/R370 at 390, symmetric insets, which is what
`mobile-check.md` calls a correct render.

#### The pipeline, and the guard it now carries

`scripts/prepare-damage-icons.py`. It reads the provenance first and refuses
to process a flagged file, parses the .ai as PDF through the standard
library's zlib alone, walks the content stream tracking the CTM, splits the
page on its own occupancy gaps into the cover illustration plus a 6 x 6 grid,
emits the chosen marks at one scale, builds the three redraws, patches
`docs/index.html`, and prints every number it used.

**It failed destructively once and now cannot.** The first patcher matched
from `<li class="fix">` to a named `<h3>` with a non-greedy `.*?`, which spans
every item in between, because `.*?` stops at the first match of what follows
it and not at an item boundary. It **ate seven of the eight items** and left
the page with one. The page was restored from git. The patcher now cuts the
page into items first and patches each inside its own bounds, and before a
byte is written it proves that the item count is unchanged and that all eight
headings still appear exactly once. **A rule worth keeping became a check**,
which is rule 8, and it is a check inside the one script that can do the
damage.

**Headings and copy are untouched**, which the diff shows: exactly eight lines
changed, all of them `<svg>` elements. The patch is keyed on each item's own
`<h3>`.

### 3.29 The footer is the contact section. BUILT 2026-09-22

The home page's Contact Us band is deleted, the hours are promoted out of the
small print into a headed footer column site-wide, and the one line the band
carried that the footer did not becomes a Get Started item. Client rulings,
2026-09-22.

#### Why the band could go, verified before anything was deleted

The home page ran `#start`, the oxblood act band, directly into `#contact`,
which informs. 3.27 had already taken the duplicated ASK out of the contact
band and left it carrying the facts. This finishes that: **the footer already
carried every fact the band carried.**

```
band carried            footer carried before this change
  address                 yes, .foot-nap and .foot-bottom
  phone                   yes, both
  email                   yes, both
  hours                   yes, but in .foot-bottom small print
  "prefer to write"       NO  <- the one thing that had to move
```

**Nothing linked to it.** `grep '#contact'` across `docs/` and `templates/`
returns no hits at all, so deleting the anchor broke no link on any page.

**The structured data was never in the band.** The `AutoBodyShop` node carries
`address` and `openingHoursSpecification` independently, and the JSON-LD is
**byte-identical before and after** in all three files, proved by hashing every
`ld+json` block: `682748c497ae928b`, `8d243f16f2a6bf72`, `5552adf7fbf1d637`
before and after.

**The visible NAP remains**, in `.foot-nap` and again in `.foot-bottom`.

#### What came out, and what did not

The section and **its own comment block** went together. The comment described
that band and nothing else; leaving it would have been a comment describing
markup that no longer exists, which is the rotting-comment failure CLAUDE.md
already has a rule about. 2,148 bytes, 41 lines, one `<section>`.

**`/collision-repair/` keeps its `#contact` section**, untouched, with its Free
Estimate heading. That page has no act band, so the section is not redundant
there. Its `id="contact"` and the template's are now the only two left.

**No CSS was deleted, and that was checked rather than assumed.** The sweep
rule from 2026-09-13 says grep a selector across every page before deleting
its rule. All four are still live:

```
.contact          collision page, template
.contact-grid     collision page
.contact-alt      collision page, template
.contact-grid h3  collision page
```

#### Hours promoted, not copied

A new `Hours` column with its own `.foot-head`, placed directly after the
identity column, so the grid reads **identity, Hours, Services, Get Started**:
facts first, asks last. The `Hours: ...` line was then **deleted** from
`.foot-bottom`. Each footer now states the hours exactly once.

```
                                       footer   body
docs/index.html                          1        0
docs/collision-repair/index.html         1        1   <- its own #contact, kept
templates/service-page-template.html     1        0
```

**The collision page carries the hours twice at file scope**, and that is the
brief working rather than failing: its `#contact` section stays by instruction,
and that section has always carried hours. The claim that matters, one per
footer, holds in all three.

#### Two columns at 760, four at 900, and the phone number is the reason

`.foot-grid` had to grow a track. Four across from 760 was tried first and
**measured**, not judged:

```
760   identity 226  |  three link columns at 131px each
      "Call (215) 322-5350" breaks between the exchange and the line number
900   identity 241  |  three link columns at 172px each
      the number sits on one line
```

A phone number split across two lines is not a cramped layout, it is an
unreadable fact, and it is the one fact the whole page is for. So the
intermediate breakpoint the brief allowed **shipped**: two columns from 760 at
343px each, four from 900. Rendered and checked at 760, 900, 1440 and 390: no
overflow at any width, no column collision, and no orphan gap where the
`.foot-bottom` hours line came out.

**The identity column resolves wider than its 1.4fr share** because the logo is
200px and min-content wins: 226px at 760 against the 197px the ratio alone
would give. That is why nothing overflows at the narrow end.

#### The one unique line, and where the template diverges

"Prefer to write? Send us your details online." became a third Get Started
item, `data-pending-href` matching each file's own depth convention:
`contact-us/` on home, `../contact-us/` on the collision page,
`{{ROOT}}contact-us/` in the template. The home FAQ answer keeps its own.

**The template has four Get Started items, not three**, because it already
carried a parameterised `{{CTA_LABEL}}` item that the two built pages do not.
The brief's proof expected three everywhere; three is right for the two built
pages and four is right for the template. Recorded rather than forced.

**The template never carried the hours at all**, so there was nothing to
promote there: the column was added so a page built from the template does not
ship a footer poorer than the two that exist. That is the divergence the brief
was guarding against, taken in the only direction that closes it.

#### Band rhythm and the fold

`#start` (ox) then `#faq` (light) then the footer (ink), confirmed by eye at
1440 and 390. The footer moved up **423px** at 1440, which is the removed
band's own height, and three ink bands remain where there were four.

**The fold did not move, and HEAD was measured alongside to prove it.**

```
                    usable   .cta-row bottom   verdict        HEAD
390x664 staging      604          613          misses by  9   identical
390x664 cutover      604          556          clears by 48   identical
360x640 staging      580          654          misses by 74   identical
360x640 cutover      580          597          misses by 17   identical
```

The staging banner costs 57px, matching `scripts/mobile-check.md` exactly.

**One number to flag, and it is not this change's doing.** CLAUDE.md records
that 360x640 "now clears by 2px"; measured with the probe of the day it
appeared to **miss by 17** in the cutover state, on HEAD too.

**CORRECTED 2026-09-23, see 3.36: this flag was wrong.** The miss was an artefact of the measuring probe, whose tall iframe made `vh` resolve against itself. Measured with the iframe set to the real viewport, 360x640 clears by 2 in the cutover state, exactly as CLAUDE.md records. CLAUDE.md never drifted. Not touched here, because the page only got shorter and the cause is
somewhere in the hero's own sizing. It wants its own look.

### 3.30 The ask joins the capability moment and the proof moment. BUILT 2026-09-22

The hero's CTA pair is added at the bottom of `#what-we-fix` and
`#real-repairs`. Client ruling 2026-09-22, with the rationale on the record:
on desktop there was no ask between the hero and `#start`, and these two
section bottoms are where a reader has just finished learning what the shop
can fix and just finished seeing that it did.

**No new wording, no new claims, no new buttons.** The markup is the hero's
own `.cta-row`, copied verbatim, twice. Proved rather than asserted: all four
rows on the page are byte-identical once indentation is normalised, and the
hero's children sit two spaces deeper only because it lives inside
`.heroB-copy > .wrap` rather than `.wrap`.

```
row 0  hero           child indent 12
row 1  what-we-fix    child indent 10
row 2  real-repairs   child indent 10
row 3  start          child indent 10
every one:  tel:+12153225350  +  mailto:contact@tricountycollision.com
            class="btn"       +  class="btn btn-ghost"
```

`/collision-repair/` is untouched. Its only changed line is the cache stamp.

#### The alignment mechanism, and why it is scoped

**`#what-we-fix` got its centring free and has nothing written for it.** It is
a `.dark` band, so the existing `.dark .cta-row` rule centres it and sets its
44px top margin, exactly as it does for `#start`. That is the mould working.

**`#real-repairs` needed a rule, and three existing mechanisms were checked
first:**

```
.dark .cta-row      centres, but only on a dark ground. Not this section.
.prose + .cta-row   centres, but only as the ADJACENT SIBLING of a .prose.
                    This row follows .repairs-grid, so it cannot fire.
.sec-head           centres the heading, not the row.
```

None reaches a light-ground row at the foot of a section, so the rule shipped
is `#real-repairs .cta-row { justify-content: center; }`.

**It is scoped on purpose rather than as a shortcut.** The base `.cta-row` is
left-aligned and has to stay that way: the hero's copy is anchored left inside
the scrim and the whole flush-left hero reads off that edge, so centring the
base rule would move the one thing the design turns on. The narrowest change
that centres this row is a rule for the one section that needs it. **If a
second light section ever wants the same thing, that is the moment to
generalise**, and the comment in `site.css` says so.

**One difference between the two new rows, recorded rather than smoothed
over.** `#what-we-fix` sits 44px below the grid because `.dark .cta-row` says
so; `#real-repairs` sits 26px below the pairs because that is the base
`.cta-row` margin. Both read correctly at both widths. Matching them would
have meant putting a margin into the scoped rule, which is more restyling than
the ruling asked for, so it was left alone and flagged here.

#### The contrast proof, for the pair that had not shipped anywhere

`#real-repairs` is a plain section, so its ground is `--silver`, the page. The
ghost button on that ground is new to this build.

```
                                             measured   floor
ghost label    --ox #691C17 on --silver       10.50:1     4.5
ghost border   --ox on --silver               10.50:1     3    (non-text graphic)
.btn fill      --ox on --silver               10.50:1     3    (shape)
.btn label     --silver on --ox               10.50:1     4.5
```

The label floor is **4.5 and not 3:1**, because `.btn` is 17px at weight 700
and WCAG's large-text cut is 18.66px bold. It clears by more than double
either way, and the figure matches the 10.50 already in the palette table, so
nothing had to be invented and no new button style exists.

#### What it costs

```
                     1440                      390
                before  after  delta     before  after  delta
#what-we-fix      1085   1191   +106       1658   1840   +182
#real-repairs     2640   2728    +88       3157   3321   +164
#start             439    439      0        444    444      0
```

**At 390, against the 604px usable height:** `#what-we-fix` goes 2.74 to
**3.05 screens**, `#real-repairs` 5.23 to **5.50**. The page is 346px longer
at 390 and 194px longer at 1440.

#### The phone behaviour, and one thing the brief expected that does not exist

The brief expected the pair "stacked full-width on the phone". **The site has
never done that and there is no rule for it anywhere**: `.cta-row` is
`flex-wrap: wrap`, so buttons keep their natural width and wrap onto their own
lines. Measured at 390, all four rows are identical:

```
row 0 hero          wrapped  btnW [199, 167]
row 1 what-we-fix   wrapped  btnW [199, 167]
row 2 real-repairs  wrapped  btnW [199, 167]
row 3 start         wrapped  btnW [199, 167]
```

So the new rows **do** match the hero's behaviour, which is what the ruling
actually required; "full-width" described something the hero does not do.
Inventing a full-width rule would have restyled the hero too, or needed a
second scoped rule for a look nobody has approved. Reported instead.

#### The fold, unchanged

Both additions sit far below the fold, and both viewports measure exactly what
they measured before this commit:

```
                    usable   .cta-row bottom   verdict
390x664 staging      604          613          misses by  9
390x664 cutover      604          556          clears by 48
360x640 staging      580          654          misses by 74
360x640 cutover      580          597          misses by 17
```

The 17px figure at 360x640 came from a probe whose tall iframe broke the
hero's `vh` clamp. **CORRECTED 2026-09-23, see 3.36: this flag was wrong.** The miss was an artefact of the measuring probe, whose tall iframe made `vh` resolve against itself. Measured with the iframe set to the real viewport, 360x640 clears by 2 in the cutover state, exactly as CLAUDE.md records.  **Not touched here**, per the ruling: it wants its
own sitting, and the hero was not to be moved for it.

**No CSS was deleted.** The `site.css` diff is 24 added lines and zero
removed.

### 3.31 The card gets its air from a token. BUILT 2026-09-22

The gap between the home hero's CTA row and the stat card's top edge doubles
on desktop, from 28px to 56px. Client ruling 2026-09-22, picked from a
rendered three-way comparison. **This is the number 3.32 noted as reserved;
the gap is now closed.**

#### One token, three places, and that is the whole point

```
:root   --statcard-air: clamp(28px, 3.9vw, 56px);
.heroB-copy   padding-bottom: calc(var(--statcard-overlap) + var(--statcard-air))
```

The literal `+ 28px` appeared **three times** in `site.css`: the base
`.heroB-copy` rule, its `max-width: 599px` variant and its `min-width: 600px`
variant. All three now take the token. **That is why the air became a token
rather than an edited literal**: three copies of one number are three chances
to change two of them, which is the same lesson `--statcard-overlap` already
carries in its own note.

**The overlap is untouched.** The card rides over the hero's seam by exactly
what it did before, measured below.

#### The clamp, and why the floor is the old value

```
 360px viewport   3.9vw = 14.04   ->  air 28.0   floor
 390px viewport   3.9vw = 15.21   ->  air 28.0   floor
 718px viewport   3.9vw = 28.00   ->  air 28.0   the floor stops binding here
1200px viewport   3.9vw = 46.80   ->  air 46.8
1436px viewport   3.9vw = 56.00   ->  air 56.0   ceiling
1440px viewport   3.9vw = 56.16   ->  air 56.0   ceiling
```

The ceiling arrives at 1436, four pixels before 1440, so the ruled 56px is
what a 1440 desktop actually gets. **The floor is the value that shipped
before it**, so a phone's hero is the height it always was: the 390 hero
already runs about two and a half screens and does not pay for a rhythm that
only reads on a desktop.

#### Interior spacing was considered and declined, on arithmetic

The client also looked at spacing out the hero's interior, the copy cluster
and the buttons, and ruled with the strategy chat to leave it alone. The copy
and the buttons are one unit, and **air inside the hero pushes the CTA row
down** — and the CTA row's bottom is the element `scripts/mobile-check.md`
measures the fold against. Bottom padding moves the card away from the buttons
**without moving the buttons**, so the fold arithmetic is untouched by
construction rather than by re-measurement.

#### Measured, against HEAD, on both pages

```
                        HEAD      NOW     delta
1440  padding-bottom    106px    134px     +28
1440  cta-row bottom     592      592        0   <- the point of the design
1440  gap to card         28       56      +28   <- the ruling
1440  overlap             78       78        0   <- untouched
1440  page end          8661     8689      +28

 390  padding-bottom     72px     72px       0
 390  cta-row bottom     613      613        0
 390  gap to card         28       28        0
 390  overlap             44       44        0
 390  page end         12244    12244        0   <- phones pay nothing
```

**The fold, both viewports, both banner states, identical to the pixel:**

```
390x664 staging   613  misses by  9      360x640 staging   654  misses by 74
390x664 cutover   556  clears by 48      360x640 cutover   597  misses by 17
```

The 17px figure at 360x640 came from a faulty probe, not from the page.
**CORRECTED 2026-09-23, see 3.36: this flag was wrong.** The miss was an artefact of the measuring probe, whose tall iframe made `vh` resolve against itself. Measured with the iframe set to the real viewport, 360x640 clears by 2 in the cutover state, exactly as CLAUDE.md records. 

**`/collision-repair/` does not move at either width**, and it is immune by
construction rather than by luck: its hero is `.heroB--ox`, and
`.heroB--ox .heroB-copy` sets `padding-bottom` outright in both media queries,
so it never consumed the overlap-plus-air sum at all.

```
                      HEAD     NOW
1440  padding-bottom   48px    48px      hero h562, page end 10748, both
 390  padding-bottom   58px    58px      hero h560, page end 17483, both
```

#### The comment

`.heroB-copy`'s note used to say "THE AIR IS 28px, and that is the only number
typed here." That stopped being true, so it was rewritten rather than left to
rot. **It names the token and does not repeat the clamp's figures**, which is
the convention `ICO_BOX` set in 3.28: the token is the one home for the
numbers, and a comment quoting them is a copy that nothing updates.

---

### 3.32 A real wreck replaces the stock hero. BUILT 2026-09-22

The home page's hero photograph becomes a real customer vehicle, supplied by
the client on 2026-09-22: a red sedan with its front end crushed, inside the
shop, before repair. **This retires the most prominent stock image on the
site.**

*(3.31 was reserved and empty when this was written. It has since landed: the
hero-to-card air. Nothing is missing.)*

#### Provenance, and where the file lives

Read before anything was built on it, through `scripts/audit.py`'s own reader:

```
474875707_9154568911256256_2223418552262379327_n.jpg   187,107 bytes
  IPTC DigitalSourceType   (none declared)
  XMP CreatorTool          (none declared)
  C2PA manifest            none
  VERDICT                  clean, no AI tell
segment walk               APP0 JFIF, APP13 8BIM "Photoshop" (132 bytes)
                           no APP1, so Exif was already stripped upstream
SOF2 progressive           1440x1078
```

That confirms the strategy chat's pre-scan against the reader the build uses.
**The supplied file never entered a commit**: it was copied to a scratch
directory outside the repo, and `git log --all` confirms no file of that name
has ever been added. `scripts/prepare-hero-photo.py` takes its path as an
argument.

**Permission rides the same practice as the Real Repairs photographs**, and
the same owner-sheet question covers it. **The original full-resolution file
is still to come from the client**; what ships here is the web-resolution copy
supplied, at the hero's existing contract.

#### The contract, which is why the layout cannot move

The hero ships 1200x800 and the `<img>` carries `width="1200" height="800"`.
Those attributes are untouched, so the page's layout is unchanged **by
construction** rather than by inspection. `fetchpriority="high"` and
`decoding="async"` are unchanged too. Only `src` and `alt` changed.

```
alt, before  A technician grinding a damaged front end in the shop while sparks fall.
alt, after   A red sedan with its front end crushed and the bumper torn loose,
             in the shop before repair.
```

The old alt described a technician who is not in this photograph.

#### The crop is measured, and one measurement was wrong first

The vehicle was located by scanning for **saturated** red: red-dominant AND
not a bright warm neutral. The first scan used red-dominance alone and
reported the car running to the bottom edge of the frame. It was the concrete:
warm floor samples at (199,167,110) and (221,189,130) are red-dominant by 30
to 50 and are not a car. With the saturation condition added:

```
whole vehicle        y  86 .. 811
crushed front end    y 236 .. 811   the right of the frame
intact body, left    y  85 .. 632
```

1440x1078 to 1440x960 discards 118 rows. 960 rows must contain 86..811, so the
top edge can sit anywhere in 0..86. **It ships at 0**: that keeps the whole
roofline and the entire crushed front end, and spends all 118 discarded rows
on empty foreground concrete, the only part of the frame carrying nothing.

Then one uniform downscale, 1440 to 1200 by box average, factor 1.2 on both
axes. **No upscaling anywhere**, and the script refuses to run on a source
smaller than the crop.

#### The plate check fired, and the fix was to make it stricter

The check runs although no plate is visible, and on the first run it **flagged
five boxes and stopped the build**. Inspected at magnification, they were the
**rear alloy wheel** (spokes against a dark tyre) and the **torn-open engine
bay**. No plate, no characters, nothing readable.

**The threshold was not lowered.** Detail alone does not identify a plate; a
plate is a bright, neutral rectangle carrying dark glyphs. The check became a
conjunction of three conditions:

```
region                    luma    sat   detail
rear alloy wheel          70.8   60.5   16.65   dark, saturated
alloy wheel edge         124.9   39.2   18.73   saturated
torn engine bay          117.7  117.6   17.71   very saturated
bright garage wall       207.7   13.9    9.76   bright, neutral, no glyphs
a plate                   >150    <35     >14   all three at once
```

660 plate-sized boxes scanned, **none meets all three**, which is the expected
result: the front of this car is torn open and its plate area is gone. The
check is now stricter about what counts as a plate and still catches one.

#### The encode, and the numbers

```
quality search   q92 down to q58, stopping at the first file <= the source
shipped          1200x800 at q58, 183,127 bytes
source           187,107 bytes, so the output is 3,980 bytes smaller (97.9%)
metadata after   APP0 JFIF only, by structural marker walk
decode assertion sips 1200x800, round-trip decode 1200x800 3ch, provenance clean
```

**Why q58 and not higher:** the house rule is that no output may be larger
than its source, and the source is a 0.96 bpp progressive JPEG of a frame that
is half empty floor. The crop throws the floor away and the downscale
concentrates what is left, so the same picture costs more per pixel. Inspected
at 1:1 in both the scrim zone and on the wreck: no blocking, no banding. It is
23KB heavier than the stock image it replaces and 1200x800 like it.

#### The scrim was re-measured and did not move

Per the readability amendment: page rendered, rendered again with
`.heroB-copy` at `visibility: hidden` so the layout holds and the glyphs go,
glyph runs taken with `Range.getClientRects()` rather than block boxes, every
composited pixel under those runs sampled against the element's own computed
colour.

```
                            HEAD (stock)   NEW (wreck)   floor   target
1440  eyebrow  --silver        13.93         14.13        4.5      7
1440  h1       --silver        11.86         13.38        4.5      7
1440  lead     --silver-2       9.47          9.81        4.5      7
 390  eyebrow  --silver        13.09         13.09        4.5      7
 390  h1       --silver        13.38         13.38        4.5      7
 390  lead     --silver-2       9.72          9.72        4.5      7
      WORST GLYPH-BOX PIXEL    9.47          9.72 / 9.81
```

**The scrim values are unchanged and did not need to deepen.** The brief
expected a deepening because the text zone sits over a bright garage wall. It
did not happen, and the reason is arithmetic: the scrim runs at .95 to .97
alpha across the text zone, so the photograph contributes three to five per
cent of the composite and a brighter picture cannot move the number far. The
new photograph measures **better** at 1440 and **identical** at 390.

#### The phone, and the honest answer about framing

**`object-position` ships unchanged at `50% 42%`.**

The brief asked what the 390 crop shows and required the crushed front end to
stay in frame on phones. Rendered and looked at: **on a phone the hero
photograph is almost entirely invisible**, and no framing choice changes that.
The phone scrim is a vertical gradient at .97/.96/.94 that only falls to zero
in the top five per cent of the hero, so what a phone reader sees is a sliver
of picture above the type. That was equally true of the stock photograph.

Changing `object-position` would trade the desktop framing, where the
photograph genuinely shows, for a few pixels of phone sliver. At 1440 the
wreck fills the right of the frame exactly where the scrim fades out, which is
the composition this hero is built for. **So it was left alone, and the reason
is recorded rather than the value quietly kept.**

#### The stock asset stays, and why

`grep accent-major-collision-repair` across every page and template first, per
the brief. The swap does **not** leave it unreferenced:

```
docs/index.html:402                 the Commercial Collision Repair service card
docs/collision-repair/index.html    the .svc photo on that page
```

**So it does not leave the repo**, per the brief's own condition. One side
effect worth recording: 3.17 noted that the hero doubled as the Commercial
Collision Repair card's photograph. **That duplication is now resolved** — the
hero has its own picture. The grid's internal repeat, Auto Glass reusing the
minor-collision photograph, is unchanged.

#### The fold did not move, proved against HEAD

```
                    usable   .cta-row bottom   verdict         HEAD
390x664 staging      604          613          misses by  9   identical
390x664 cutover      604          556          clears by 48   identical
360x640 staging      580          654          misses by 74   identical
360x640 cutover      580          597          misses by 17   identical
```

The 17px figure at 360x640 came from a faulty probe, not from the page.
**CORRECTED 2026-09-23, see 3.36: this flag was wrong.** The miss was an artefact of the measuring probe, whose tall iframe made `vh` resolve against itself. Measured with the iframe set to the real viewport, 360x640 clears by 2 in the cutover state, exactly as CLAUDE.md records. 

**The audit's permanent asset-provenance check now reads 29 of 29 images with
no AI-generation marker**, up from 28, the new one included.

### 3.33 The repairs become prints, and the outcome wears the brand. BUILT 2026-09-23

Two changes to Real Repairs, both on the client's ruling of 2026-09-23, picked
from rendered comparisons: the ten photographs get a resting ink shadow so the
pairs read as physical prints, and the AFTER chip fills in oxblood.

**Variant D was picked from A through F.** Two are worth recording because of
what they would have done:

- **E, both chips red-outlined.** Rejected: it brands the wreck as loudly as
  the repair, which is the opposite of the argument.
- **F, a red base rule under every frame.** Rejected on the same ground and
  harder: a rule under every photograph **red-underlines the wrecks**, so the
  most emphatic mark on the page would have been sitting under the damage.

#### The shadow, and why it rests here

```
box-shadow: 0 12px 28px rgb(var(--ink-rgb) / .16),
            0 3px 8px  rgb(var(--ink-rgb) / .10);
```

**Nothing was tokenized to derive from.** The lift's shadow is a literal
`rgba(18, 27, 39, .34)` on `.card::before` and there is no shadow token in
`:root`, so the strategy chat's measured values ship — but **written against
`--ink-rgb`'s channels rather than retyped as literals**, so the shadow is the
site's own darkest value by construction and not a grey that happens to match.

**Why a shadow rests here when everywhere else it answers a pointer.** The
lift exists to tell a hand that a card is under it. These frames are not
cards: nothing here is hoverable, nothing is a target, there is no gesture to
answer. What they are is the evidence the page argues from, and the ruling is
that evidence should read as a print lying on the page rather than a picture
pasted into it. So the same ink the cards cast under a pointer is cast here at
rest, softer and at lower alpha, describing weight instead of reacting to one.

**No new number entered the stylesheet.** The mock used a 6px radius; the
frames keep `var(--radius)`.

#### The chips, and the asymmetry

```
BEFORE   white fill, ink edge, ink text        byte-identical to HEAD
AFTER    ox fill, silver hairline, silver text new, 2026-09-23
```

The `.ba-chip` base rule is **unchanged to the byte**; the AFTER chip is a new
`.ba-frame--after .ba-chip` rule that sets fill, border colour and text colour
and nothing else. Geometry, type, letter-spacing and position stay the BEFORE
chip's, so the two read as one family with one of them coloured.

**The edge follows the act button's symmetric rule, not the BEFORE chip's.**
The ground under a chip is a photograph nobody controls, so the chip needs a
light tone and a dark tone and lets whichever suits the picture carry it. On
the BEFORE chip that is white fill plus ink edge. On the AFTER chip an ox fill
stands off a bright photograph and a silver hairline stands off a dark one, so
it wears **both** — the same construction as the act button on a dark ground,
built for the same reason.

**The asymmetry is the ruling, not an oversight**: the outcome is the branded
moment and the wreck is not.

#### The measurements, 3.23's machinery re-run

Per-frame perimeter sampling, every position around every AFTER chip, sampled
2px outside the outline, at both widths. **Calibrated first**, as 3.23
requires: two magenta marks at known page coordinates were found exactly where
they were put, so page and image coordinates are 1:1, and the page was served
over HTTP so the self-hosted fonts load and the chips are their real width.

```
1440                                        390
chip  rect y      samples  <3:1  worst      samples  <3:1  worst   carried by
 1    3078          212      0   3.27         212      0   3.26    fill
 2    3489          210      0   3.25         210      0   3.27    fill
 3    3899          210      0   3.25         210      0   3.26    fill
 4    4408          212      0   3.25         212      0   3.26    edge
 5    4918          212      0   3.25         212      0   3.28    edge
      worst across all five      3.25                     3.26     floor 3.0
```

**Zero samples below 3:1 at either width.** Photo-independent, and therefore
true everywhere:

```
label, --silver on --ox      10.50:1   floor 4.5
internal edge, silver on ox  10.50:1   floor 3
```

**One number is worth stating plainly: 3.25 is tighter than the 4.16 the
white/ink chips measured in 3.23.** Oxblood and silver are a narrower pair
against a mid-tone photograph than white and ink are. It clears the floor at
every one of the 1,056 positions sampled, and it clears it with less room than
the BEFORE chip does. If a future photograph ever lands in the band, this is
the measurement to re-run before assuming it still holds.

#### What did not move

Shadows paint outside the box and the chips did not resize, so nothing
reflowed. Measured against HEAD rather than asserted:

```
                      HEAD     NOW
1440  #real-repairs    2728    2728     page end  8689 -> 8689
 390  #real-repairs    3321    3321     page end 12244 -> 12244
 360  #real-repairs    3118    3118     page end 12218 -> 12218
```

**The fold is identical**, which it had to be since the section sits far below
it:

```
390x664  613 / 556      360x640  654 / 597      both, HEAD and now
```

`/collision-repair/` changed by its cache stamp alone. **No CSS was deleted:**
294 selectors against HEAD's 293, the one addition being the AFTER chip rule,
and the ten removed lines are the `.ba-chip` comment that was rewritten.

#### The palette law's third extension

Oxblood means act, and the client has now extended it three times: the
header's 4px divider (2026-09-17), `#who-we-are`'s prose ground (2026-09-17),
and this label. **Recorded where the other two live**, in the palette note in
`docs/assets/site.css` and in CLAUDE.md's palette paragraph, dated and
attributed.

**The test for a fourth case: does the element ask the reader to do
something?** A band that asks is an act band and the act-band count governs
it. **A chip does not ask** — it cannot be clicked, it is not a target, it
names which photograph you are looking at. Nothing else was extended in this
commit.

### 3.34 The collision page takes the proof, the brands, and a wreck of its own. BUILT 2026-09-23

Three client rulings of 2026-09-23, from the template conversation. Real
Repairs and the brand strip graduate from home-page sections into components a
service page may carry; `/collision-repair/` takes both; and its stock hero is
replaced with a real photograph.

#### Real Repairs, and the gate that makes the reuse honest

The home section's markup, adapted **for path depth only**: same five pairs,
same alt text (checked string for string against the home page), same heading,
sub and intro copy, same id. No new claim and no new word.

**A SERVICE PAGE'S PAIRS SHOW THAT SERVICE'S JOBS.** That is the gate, and it
is written on the section in `docs/collision-repair/index.html` and again on
the optional block in `templates/service-page-template.html`, because the
template is where somebody will copy it from. All five pairs are collision
jobs, so on this page they are its own evidence. **A page whose service has no
photographs yet ships WITHOUT the section** — never with stock, never with
another service's work. A glass page showing collision pairs is a claim the
shop did not make.

**Placed directly after `#process`**, so the page reads "here is how we work,
here is what it produces."

**NO CTA ROW at its foot**, and that is the one structural difference from the
home copy. The home section carries the pair because the front door had no ask
between its hero and `#start` (3.30). This page already carries two act bands,
and a third ask inside a proof section is the duplication 3.27 removed.

**The `.ba` grammar arrived free**, as predicted: print shadows and the
branded AFTER chip are shared CSS, and no rule was added for this page.
`#real-repairs .cta-row { justify-content: center }` is home-scoped and stays
home-scoped — it has nothing to centre here.

#### The chips, re-measured on this page

3.23's perimeter machinery, calibrated first: both magenta marks at known page
coordinates were found where they were put, so page and image coordinates are
1:1, and the page was served over HTTP so the chips are their real width.

```
1440                                  390
chip  rect y   samples <3:1  worst    rect y   samples <3:1  worst
 1     2391      210     0   3.46      3980      210     0   3.26
 2     2801      212     0   3.24      4488      212     0   3.28
 3     3211      212     0   3.28      5062      212     0   3.25
 4     3721      210     0   3.25      5702      210     0   3.28
 5     4231      210     0   3.25      6342      210     0   3.28
       worst           3.24                    worst          3.25   floor 3.0
```

**Zero samples below 3:1 at either width**, 2,108 positions in total. Label and
internal edge are 10.50 and photo-independent. The numbers sit where 3.33's
did, a little over three, for the reason recorded there.

**One measurement bug caught and fixed**: the probe's own report panel is
`#0f0`, which is the second chip's mask colour, so the first run merged chip 2
with the panel and reported a rect 719px wide. The search is now bounded to
the page width. Nothing shipped on the bad reading.

#### The brand strip, and the motion law's extension

Placed **under `#factory-certified`'s head**, because that sub counts the
twelve in words and the strip shows which twelve. The section does not name
them in text, so nothing is repeated. **The stat band higher up the page does
name them, and those words stay**: `scripts/audit.py`'s brand check wants every
count on the page agreeing, not merged. It reports **2 strips of marks, 8
mentions in visible text and 1 in JSON-LD, all saying 12**.

**THE CONTINUOUS-MOTION AMENDMENT IS EXTENDED.** It read "`#brands` only ... on
this page or any other", which made the strip a property of the home page. On
the client's ruling it is a **component**, the one thing on this site that may
loop, and **a page carries at most one**. Recorded in CLAUDE.md's
continuous-motion amendment and in the motion note in `site.css`, dated and
attributed.

**Every limit travels verbatim, and by construction rather than by copying
care**: the markup is the same and so is the CSS. The animation exists only
inside `@media (prefers-reduced-motion: no-preference)`, so the static wrapped
row is the base in the cascade; `.brandstrip:hover` and `.brandstrip:focus-within`
pause it; there is no JavaScript. **Rendered in the reduced-motion state**: the
strip rests as a wrapped static row with all twelve marks visible, seven on
one line and five on the next.

**The test for anything else that wants to loop is unchanged, and the answer is
still expected to be no.**

#### The hero, and a second real photograph

`accent-minor-collision-repair.jpg` is replaced by a white GMC SUV with its
front end crushed, shot outside the shop and supplied by the client.

```
source   490357663_1519359622667520_8523311604682603809_n.jpg   273,173 bytes
         1440x1080, APP2 ICC + APP13 8BIM, no APP1 so Exif was stripped upstream
         DigitalSourceType, CreatorTool, C2PA: none. Clean.
shipped  hero-wrecked-gmc-outside-shop.jpg   1200x800 at q62, 270,216 bytes
         98.9% of the source, APP0 JFIF only, decodes to contract both ways
```

The supplied original never entered a commit; `git log --all` confirms no file
of that name was ever added.

**The pipeline was extended, not forked.** `scripts/prepare-hero-photo.py` now
carries a `FRAMES` table, one entry per photograph, because a hero crop has to
keep a particular vehicle in a particular frame and that is a fact about the
photograph. **The home hero rebuilds byte-identically through the
parameterised script**, which is how the refactor was checked.

**How the two crops were obtained is not the same, and that is recorded rather
than smoothed over.** The home frame's car was found by a saturated-red scan.
**No colour test separates this frame**: the vehicle is white on grey asphalt
under a low sun, and a luma-plus-saturation scan scores the sunlit asphalt and
the sky as bodywork just as strongly. The extents — vehicle rows 66..810 —
were **read off the decoded frame under a 120px coordinate grid**. That is an
inspection, not a scan, and the script says so.

#### The plate check fired again, and it exposed a gap in its own design

19 boxes met all three conditions. Inspected at magnification: **backlit sky
through bare trees** (15), the **corrugated building and chain-link fence**
(3), and **the subject's own front alloy wheel on sunlit gravel** (1). The
background parked cars were looked at too, although they did not flag: they
are front-facing and Pennsylvania issues rear plates only. No plate anywhere.

**The thresholds were not touched.** What the check lacked was a path for the
usual answer. Its failure text offered only "redact it if it is a plate" and
had nothing to say for "looked at it, it is not one". So a frame may now carry
**inspected-and-cleared regions**, each with a sentence naming what the thing
actually is. This is deliberately not a threshold: the numbers do not move,
**every suspect outside a cleared region still fails the build**, and clearing
one is an edit to the script that names the region and the reason, which
somebody reviews. A per-frame exception that has to be written down is a
different thing from a global limit that has been loosened.

#### The scrim, re-run with the ox rules

Per the readability amendment, on the ox hero, where **there is no secondary
text tone** — `.heroB--ox .lead` is `--silver`, not `--silver-2` — so all
three runs are measured against `--silver`.

```
                     HEAD (stock)   NOW (GMC)   floor   target
1440  worst glyph        9.27          9.52      4.5       7
 390  worst glyph        9.46          9.52      4.5       7
```

**The scrim did not need to deepen** and its values are unchanged. The new
photograph measures slightly better at both widths.

**`object-position` ships unchanged at `50% 42%`, and the reason is that it is
SHARED.** `.heroB-photo` sets it once for both heroes; there is no `--ox`
override. Changing it for this page would move the home hero too and would
need both re-measured. At 1440 the damaged front fills the right of the frame
where the scrim fades, which is the composition the hero is built for. **At 390
the photograph is almost entirely behind the scrim**, as it is on the home
page, and the sliver above the breadcrumb shows the treeline and the SUV's
roof rather than the crushed front. No framing choice changes that; the phone
scrim is the reason.

#### The old asset, and two references outside this brief

`grep accent-minor-collision-repair` before touching anything returned **seven**
references, not the one the swap assumed:

```
docs/collision-repair/index.html   og:image (47), JSON-LD url (236), hero (399)
docs/index.html                    og:image (47), JSON-LD url (243),
                                   services grid (395, 416)
```

The assumption that the home services grid still uses it **holds**, so the
asset stays and nothing was deleted. **But the collision page's own og:image
and JSON-LD image still point at the stock hero**, which this brief did not
cover. They are untouched and flagged here: the page's social preview and its
schema image now show a photograph its hero no longer uses. That is a decision
for the client, not a silent edit to structured data.

#### What it costs

```
                HEAD      NOW     delta
1440 page      10748    13514    +2766
 390 page      17483    20722    +3239
 360 page      18638    21675    +3037
```

**At 390 that is 28.95 to 34.31 screens** against the 604px usable height. The
page was already long; it is now much longer, and the two components are the
whole of it.

**The hero is unchanged in height at every width** (562 at 1440, 560 at 390 and
360), because the `<img>` keeps `width="1200" height="800"`, `fetchpriority`
and `decoding`. **The fold is identical to HEAD**, both viewports, both banner
states:

```
390x664  629 / 572      360x640  629 / 572
```

The collision page clears 360x640 by 8 in the cutover state, unlike the home
page. **CORRECTED 2026-09-23, see 3.36: this flag was wrong.** The miss was an artefact of the measuring probe, whose tall iframe made `vh` resolve against itself. Measured with the iframe set to the real viewport, 360x640 clears by 2 in the cutover state, exactly as CLAUDE.md records. Both pages clear it.

**The home page is byte-identical except its cache stamp**, and the
site-wide asset provenance check now reads **30 of 30 images with no
AI-generation marker**.

#### The Altima, considered and set aside

A second photograph was offered for the hero. It was set aside on composition,
and because **it carries a customer's name on the glass**. It remains a
candidate for a future before/after pair if its after-photo mate exists.

### 3.35 The share card shows the page it shares. BUILT 2026-09-23

`og:image`, `og:image:alt` and the JSON-LD image on both pages pointed at
`accent-minor-collision-repair.jpg`, the stock photograph **no hero uses any
more**. This was the builder's own flag at the end of 3.34, approved by the
client. Each page's share card and schema image now show that page's own real
hero.

```
                      og:image / primaryImageOfPage
/                     hero-wrecked-sedan-in-shop.jpg    (3.32)
/collision-repair/    hero-wrecked-gmc-outside-shop.jpg (3.34)
```

#### Driven from each page's own hero, not retyped

The edit reads the `<img class="heroB-photo">` element on each page and takes
both the filename and the alt from it, then asserts the filename is the one
expected. **So "og:image:alt matches the hero alt verbatim" is true by
construction rather than by somebody copying carefully**, and the check after
the fact confirms it:

```
                      og:image:alt == hero alt    url == hero src
/                             True                     True
/collision-repair/            True                     True
```

#### The collision page's schema caption had to move too

Its `primaryImageOfPage` carries a `caption` as well as a `url`, and that
caption read "Final collision repair touch-ups being completed on a black
automobile." **Changing only the url would have left a caption describing a
different photograph** — not a stale line but a false one, a sentence claiming
the picture shows something it does not. The caption now follows the alt.

The home page's node carries a `url` and no caption, and it was left that
shape. That asymmetry predates this change and nothing here needed it
resolved.

#### The meta that did not move, and why

`og:image:width` and `og:image:height` stay at 1200 and 800 because **both new
assets really are 1200x800**, confirmed by reading them rather than assumed
from the contract:

```
hero-wrecked-sedan-in-shop.jpg     1200x800
hero-wrecked-gmc-outside-shop.jpg  1200x800
```

**The stock asset itself stays.** It is still referenced twice, by the home
services grid's Collision Repair and Auto Glass cards, exactly as 3.32 and
3.34 recorded. Nothing was deleted.

#### The interim state, on the record

**This is not the final arrangement and it is written down as interim.** When
the photo shoot delivers a building shot, the client's instruction is that the
**schema image becomes the shop itself** while the **og:image stays the page's
hero**.

**One note for whoever does that.** The only image in either page's schema is
`primaryImageOfPage` on the `WebPage` node, and that property means precisely
what it says: the primary image *of the page*. A photograph of the building is
not that; it is a picture of the business. **The `AutoBodyShop` node carries no
`image` at all today**, and that is the property a building shot belongs on.
Putting the shop on `primaryImageOfPage` would make the page claim a hero it
does not have. Recorded now, while the reasoning is in front of us, rather
than discovered on the day.

### 3.36 The chips read in the order the repair happens. BUILT 2026-09-23

Two client rulings of 2026-09-23 on `/collision-repair/`'s hero chips.

#### The order of operations

```
1. Free estimates                        you call; it costs nothing
2. Insurance paperwork handled           the claim is dealt with
3. ASE and I-CAR Gold Class certified    credentialed people do the work
4. Detailed after every repair           the handback
```

**There are TWO chip lists on this page, not one**, and both were reordered
identically. `.heroB .badges` is the desktop arrangement and
`.proofstrip .badges` is the phone band; they are the same four claims in two
DOM positions, exactly one rendered at a time. Reordering one would have made
a phone and a desktop disagree about the order of the repair.

**Each whole `<li>` moved, icon and label together.** Proved by hashing each
chip's SVG path data and printing it beside its label: the four hashes are the
same in both lists and each still sits with the label it belongs to.

#### The credential's full name

The chip read "ASE and I-CAR Gold certified". The credential is **I-CAR Gold
Class**, and **this page's own FAQ answer already says it correctly**. This is
an alignment to the page's own wording, not a new claim.

```
before   ASE and I-CAR Gold certified
after    ASE and I-CAR Gold Class certified          x2, both chip lists
```

**The only text delta on the page is the word "Class", twice.** Proved by
extracting every visible word from HEAD and from the working tree and
comparing the multisets: `added {'Class': 2}`, `removed {}`. The reorder moves
words; it does not change them.

#### The length gate tripped, so three instances were NOT touched

The compressed form appeared in five places, not two. The other three are
**one sentence in three places** — they are byte-identical mirrors of each
other:

```
meta description                158 chars   ->  164 with "Class"
og:description                  158 chars   ->  164 with "Class"
JSON-LD WebPage description     158 chars   ->  164 with "Class"   mirrors the meta exactly
```

The audit's limit is 160. **Adding "Class" pushes all three past it**, and the
instruction was to stop and report rather than trim other words to make room.
So they are unchanged and shipped at 158.

**They have to move together or not at all.** The WebPage schema description
is the same sentence as the meta description, character for character;
aligning one and leaving the others would put three copies of one sentence out
of step, which is the defect class the NAP rule and the byte-identical FAQ
rule both exist to prevent. **Rewording a 158-character meta description to
find six characters is an editorial decision about which promise gives way,
and it is the client's, not a side effect of a chip label.**

The JSON-LD **Service** description already said "Gold Class" and came back
untouched, as expected. `docs/llms.txt` and the home page's prose already say
it correctly too. **The home page carries no chips at all** and no compressed
form, so it is untouched entirely — not even a stamp, because no CSS moved.

#### Nothing moved, measured

```
                 HEAD    NOW        HEAD    NOW        HEAD    NOW
width            1440               800                390
hero h            562    562         522    522         560    560
badges h           96     96          96     96         n/a (display:none)
proofstrip h      n/a                n/a                202    202
page end        13514  13514       14449  14449       20722  20722
```

**Not a pixel, at any of the three widths.** The longer third label does not
orphan a word: at 1440 and 800 the row pairs two-by-two with the
money-and-logistics chips on the first row and the quality chips on the
second, exactly as the ruling intended, and at 390 each chip takes its own row
on one line.

#### And the fold measurement was wrong, in my own favour of caution

Re-measuring the fold as instructed turned up a fault in the **probe**, not
the page.

**`vh` resolves against the iframe's own height.** The hero's size is a `vh`
clamp — `min-height: clamp(380px, 76vh, 560px)` below 600px, plus three more
— and every fold probe in this repo has used a 16000px-tall iframe. `76vh` of
16000 is 12160, so every clamp pinned to its maximum and the hero rendered at
its tallest possible size. The CTA row then sat lower than it ever would on a
phone.

Measured with the iframe set to the actual viewport:

```
                          tall iframe (wrong)     iframe = viewport (right)
home  390x664 banner      613  misses by  9       594  clears by 10
home  390x664 cutover     556  clears by 48       537  clears by 67
home  360x640 banner      654  misses by 74       635  misses by 55
home  360x640 cutover     597  misses by 17       578  CLEARS BY 2
coll  390x664 banner      629  misses by 23       580  clears by 24
coll  390x664 cutover     572  clears by 32       523  clears by 81
coll  360x640 banner      635  misses by 55       579  clears by  1
coll  360x640 cutover     578  clears by  8       521  clears by 59
```

**CLAUDE.md's "360x640 now clears by 2px" is exactly right.** I flagged it as
a false record in 3.29, and repeated the flag in 3.30, 3.32 and 3.34. **The
flag was wrong and all four are corrected**, each pointing here. CLAUDE.md
never drifted; the probe did.

**The trap is now written down** in `scripts/mobile-check.md`, beside the
500px width clamp it is a sibling of, with the rule that a fold probe's iframe
must be the viewport height and must report `innerHeight` and the computed
`min-height` beside its answer so a wrong basis shows in the output instead of
hiding in it. Page height and fold are two different questions and one frame
cannot answer both.

**This change did not move the fold**, on the corrected basis or the old one:
HEAD and the working tree measure identically at both viewports and both
banner states.

### 3.37 The description names the credential in full. BUILT 2026-09-23

The sentence 3.36 stopped on. Client-approved wording, 2026-09-23, closing
that gate.

#### The pair

```
before  Trusted collision repair in Southampton, PA. ASE & I-CAR Gold
        certified, lifetime warranty, free estimates. Serving Bucks &
        Montgomery County. (215) 322-5350.                      158 chars

after   Collision repair in Southampton, PA. ASE & I-CAR Gold Class
        certified, lifetime warranty, free estimates. Serving Bucks &
        Montgomery County. (215) 322-5350.                      156 chars
```

**"Trusted " leaves the front and " Class" joins the credential.** The word
that went was puffery, and its going lets the keyword lead. The word that
arrived is the credential's actual name, which this page's chips (3.36) and
its own FAQ answer already use.

**156 characters, machine-counted**, by the same check that reports it in the
audit: "Meta description present and a good length (156 chars)." The limit is
160, so it clears by four where the compressed form would have exceeded it by
four.

#### All three mirrors, proved identical

The sentence lives in three places and they are byte-identical after the edit,
by SHA-256 of the decoded string:

```
meta description    156 chars   sha256 041c2c44137437e3
og:description      156 chars   sha256 041c2c44137437e3
JSON-LD WebPage     156 chars   sha256 041c2c44137437e3
```

**The stored bytes differ by context and that is correct**, not a discrepancy:
the two `<meta>` attributes hold `&amp;` because an HTML attribute must, and
the JSON-LD holds a raw `&` because JSON must not. The edit rewrote each in
its own encoding. **Byte-identical is a property of the sentence, not of the
file.**

#### Nothing else moved

Three lines changed, and the whole-file word delta accounts for exactly them:

```
added     content="Collision x2, "Collision x1, Class x3
removed   content="Trusted   x2, "Trusted   x1, collision x3
```

The three `collision` removals are the lowercase word being absorbed into the
new capitalised leading `Collision`. Nothing else in the file moved.

**The JSON-LD Service description is untouched** and still names Gold Class,
as it already did. **No compressed form of the credential remains anywhere**
in `docs/` or `templates/`. **"Trusted" now appears zero times on either
page**; that sentence was its only home. No CSS, so no restamp.

### 3.38 The evidence goes on the dark ground, on the collision page too. BUILT 2026-09-23

`/collision-repair/`'s `#real-repairs` takes `class="dark field-ink"`. Client
ruling 2026-09-23, picked from rendered comparisons.

#### The reasoning, and what was rejected

It **ends the two-silver run after `#process`**, which is the adjacency the
client's eye caught. Beyond that: the dark band is where evidence lives on
this site, which the home page's damage list established; the photographs and
the branded AFTER chips read stronger on ink; and red stays reserved for the
ask on a page that already opens red.

**The red option was rendered and rejected**, on the record: it fights the red
chips and the red cars, and this page carries enough ox already.

```
before   #process (silver) -> #real-repairs (silver) -> #services (white)
after    #process (silver) -> #real-repairs (INK)    -> #services (white)
```

#### The .ba grammar gains its dark mode

```
.dark .ba figcaption            --silver-2    10.78:1 on ink
.dark .ba figcaption strong     --silver      15.42:1 on ink
#real-repairs.dark .repairs-note --silver-2   10.78:1 on ink
```

Floor 4.5, target 7; all three clear both. **The tones they replace are why
the rule had to exist at all**: `--ink-2` on ink measures **1.77** and `--ink`
on ink measures **1.00**. Without it the captions would have been invisible on
their own ground.

**Scoped through `.dark`, so it is the component's rule and not a page
one-off.** Any page that darkens this section gets readable captions with
nothing written for it, which is what made it a component in 3.34.

**The heading and kicker needed nothing.** `.dark` gives the sec-title
`--silver` and `.dark .sec-sub` gives the kicker the same, exactly as
`#what-we-fix` gets them on the home page. Confirmed by computed style: both
report `rgb(240, 242, 242)`, where HEAD had ink and `--ox-tx`.

#### One selector was wrong, and the measurement caught it

The intro line's rule first shipped as `.dark #real-repairs .repairs-note`
and **matched nothing**. `.dark` sits ON the section, not around it, so there
is no ancestor for a descendant selector to describe. The probe showed
`figcaption` and `strong` already turned while `repairs-note` still reported
`rgb(60, 68, 83)`, which is `--ink-2` on ink at 1.77:1.

Corrected to `#real-repairs.dark .repairs-note`, both on the same element.
**It names the ID only because the rule it must beat does**: the existing
`#real-repairs .repairs-note` carries an explicit `--ink-2` at specificity
110, so a plain `.dark .repairs-note` at 20 would lose. Rewriting that
selector would have been tidier and a wider change than this needed.

#### The shadow is left invisible on purpose

The `.ba` print shadow is ink on ink inside this section and effectively
invisible. **The shared rule is untouched**, and the shadow comment in
`site.css` now says so in as many words, ending "if you came here to fix the
invisible shadow: it is not broken." A shadow that vanishes costs nothing;
scoping it off would fork a shared component into two implementations to save
nothing.

#### The chips are untouched by construction

Both chips sit **on the photographs**, so the pixels their perimeters were
measured against are photo pixels that did not change. **3.23's and 3.34's
numbers stand** and nothing was re-measured. The ground moved around the
frames, not under the chips.

#### Home stays light, deliberately

`docs/index.html`'s `#real-repairs` is unchanged and the home page differs
from HEAD **only by its cache stamp**. The component wears each page's rhythm:
a page copying it picks its ground by its own adjacency, and the dark text
grammar comes with it either way. That is written on the collision section's
comment and on the template's optional block, so the next page to take it has
the choice in front of it.

#### A ground is a colour, not a size

```
                    HEAD          NOW
1440  #real-repairs h=2640        h=2640      page end 13514 -> 13514
 390  #real-repairs h=3157        h=3157      page end 20722 -> 20722
```

**The fold is identical**, measured with the corrected probe from
`mobile-check.md`'s second trap — the iframe IS the viewport, and it prints
`innerHeight` and the computed `min-height` beside the answer so a wrong basis
would show:

```
390x664   innerHeight=664  min-height=504.64px   580 / 523   clears by 24 / 81
360x640   innerHeight=640  min-height=486.4px    579 / 521   clears by  1 / 59
```

Both identical to HEAD. **No CSS was deleted**: 37 lines added, one removed,
and that one is the comment terminator the shadow note was extended through.

### 3.39 The pairs join the lift, and the sweep stays red in the dark. BUILT 2026-09-23

`figure.ba` becomes a member of the lift, site-wide, on both pages. Client
ruling 2026-09-23. **This is the mold growing a member, not a new effect.**

*(WITHDRAWN 2026-09-23 by 3.41, on the client's ruling after live use. Every
line below was built and proved as written; the client's eye then decided the
pairs read better without it, and the membership was reverted in full. This
record stays because what was done and why is worth keeping. See 3.41.)*

#### Membership, proved as membership

`.ba` was added to **eleven selector lists** and nothing else: the
`position: relative` base, the `::before` shadow, the `::after` rule, the six
rules inside `@media (hover: hover)`, and both lists in the
`prefers-reduced-motion` block. **No bespoke value, no copied block.**

The proof that it is membership rather than authorship is the selector count:

```
selectors in site.css    HEAD 297    now 297
```

**Not one rule was added or removed.** The sixteen removed lines are the
fourteen selector lists that were rewritten to include `.ba` plus two comment
lines that were extended.

**The lift's own requirement was checked before any of it.** A member needs
both pseudo-elements free; `grep` found no `.ba::before` or `.ba::after`
anywhere, and `.ba` itself carried only `margin: 0`.

Confirmed by computed style on both pages, at both widths:

```
figure.ba   position: relative
  ::before  content ""   shadow rgba(18, 27, 39, .34) 0 12px 26   opacity 0
  ::after   content ""   background rgb(105, 28, 23)   width 28px  opacity .4
```

Those are the mold's own numbers, not new ones.

#### The dark-ground exception, and why it is an absence

The lift's rule answers in silver on dark grounds, because `--ox` on `--ink`
measures 1.47. **The pairs' rule stays oxblood on every ground.** Client
ruling, on the header divider's precedent: **ox against ink reads by hue
rather than by luminance**, which is why that divider works at the same 1.47.
The branded sweep is the point of the ask, and a silver sweep would answer a
question nobody asked.

**The implementation is that `.ba` is left OUT of `.dark .card::after`**,
which already named `.card` and only `.card`. So the exception costs no
override and no scoped rule: it is an absence. Recorded in the lift comment,
in CLAUDE.md's lift paragraph, and here, with the note that **adding `.ba` to
that rule later would undo the ruling**.

Measured on the ink section: `::after` background reports `rgb(105, 28, 23)`,
which is `--ox`, not `--silver`.

#### Rendered, with the hover state forced

The first attempt injected the forced class from JavaScript after a timeout
and **silently did nothing** — the scan found 28px resting ticks and no swept
rule anywhere, so nothing was concluded from it. Replaced with a
deterministic method: a temporary copy of each page carrying the mold's own
hover declarations in a `<style>` and the class already on the second pair, so
there is no timing to get wrong. Both copies were deleted afterwards; a stray
page in `docs/` is a page the audit scores and a crawler can find.

Measured off those renders, by scanning for 2px horizontal red runs:

```
                    forced pair          every other pair
home  (silver)      1080px swept rule    28px resting tick
collision (ink)     1080px swept rule    28px resting tick
```

**The resting tick is present and visible on both grounds**, so the question
the brief raised about invisibility on ink did not arise. On ink the full
sweep reads clearly as a dark red line, which is the hue argument holding.

#### The shadow, invisible on one ground on purpose

The lift's `::before` is the same ink as the print shadow 3.33 added, so it
shows on the home page's light ground and does not on the ink section. **The
existing not-broken note in `site.css` now covers the hover shadow too**, in
one sentence, so nobody forks a shared component to fix something that costs
nothing.

#### Reduced motion, inherited rather than rewritten

Read, not reimplemented: `.ba`, `.ba::before`, `.ba::after` and `.ba:hover`
sit in the existing `prefers-reduced-motion: reduce` block alongside every
other member, so the hover **state** still changes and the movement goes.
Nothing was written for it beyond the membership.

#### Layout untouched

The pseudo-elements are absolute and the transform is hover-only, so nothing
reflows:

```
                          HEAD     NOW
home       1440  #real-repairs h=2728  2728   page end  8689 ->  8689
home        390  #real-repairs h=3321  3321   page end 12244 -> 12244
collision  1440  #real-repairs h=2640  2640   page end 13514 -> 13514
collision   390  #real-repairs h=3157  3157   page end 20722 -> 20722
```

**The fold is identical on both pages**, measured with the corrected probe
from `mobile-check.md`'s second trap, and the four reports hash byte-identical
between HEAD and the working tree:

```
home 390x664  7d5fd337    home 360x640  8b8b68f3
coll 390x664  bb9257cb    coll 360x640  911a69f6
```

### 3.40 The marks lead, and the heading captions them. BUILT 2026-09-23

On `/collision-repair/`, `<section id="brands">` moves from **under**
`#factory-certified`'s head to **above** it, becoming the first child of that
section's `.wrap`. Client ruling 2026-09-23.

*(SUPERSEDED 2026-09-24 by 3.43, which moves the strip a third time, to sit
BETWEEN the head and the prose. The arrangement below was built and proved as
written; what unseated it was the client's spacing requirement, not the
composition. See 3.43.)*

**The relationship inverts and nothing else does.** Before, the sub announced
the strip: you read "Twelve manufacturers, and the procedures that come with
them" and then saw twelve marks. Now you watch the marks go by and the
heading tells you what you just watched. The words did not move, the strip's
own markup did not move, and no rule was written for either arrangement.

#### What actually changed, proved rather than asserted

The diff is one block relocated and one comment rewritten. Everything the
block contains is byte-identical:

```
<section id="brands">…</section>   sha256  HEAD ef0636a7d0a6   NOW ef0636a7d0a6   identical
<div class="sec-head">…</div>              identical
visible word multiset, whole page          identical  (2933 tokens)
```

**The strip is still the page's only one**, and the brand check agrees:
`scripts/audit.py` reports 2 strips of marks site-wide, 8 mentions in visible
text and 1 in JSON-LD, all saying 12.

The comment was rewritten because it argued for the old order in its own
words. It now records the ruling, and it keeps the half that is **enforced
rather than argued**: the section names no manufacturer in text, the stat band
higher up the page names all twelve, and the brand check wants every count on
the page agreeing rather than merged.

#### A pure reorder, measured

Nothing reflowed. Both widths, HEAD against the working tree:

```
                 #factory-certified h      PAGE END
1440   HEAD              1065               13514
1440   NOW               1065               13514
 390   HEAD              1521               20722
 390   NOW               1521               20722
```

**Section height delta 0 at both widths**, which is what a reorder inside one
`.wrap` should cost and is the reason no spacing was tuned.

The gaps, for the record:

```
                       section-top -> strip    strip -> sec-head   sec-head -> prose
1440   HEAD                  204                    -242                 166
1440   NOW                    88                       0                  40
 390   HEAD                  197                    -232                 123
 390   NOW                    48                       0                  40
```

**The negative numbers in the HEAD rows are not a defect, they are the probe
reading backwards**: it measures `sec-head.top - brands.bottom`, and in the old
order the head sat above the strip. They are printed rather than hidden so the
two columns are the same measurement.

#### The spacing was left alone, on purpose

The brief allowed a margin if the arrangement needed one. It did not.
`#brands` carries `margin: 0 / 0` and its own `padding: calc(var(--pad) * .55)`
— **48.4px at 1440, 26.4px at 390** — so the air above it is the section's top
padding plus the strip's, and the air below is the strip's padding meeting the
head. That is why the raw `strip -> sec-head` gap reads 0 while the rendered
air is the strip's own 48.4px. Rendered and judged at both widths before
deciding: ink testimonials, then ground, then air, then the marks, then the
heading. **No stylesheet was touched, so there is nothing to restamp.**

#### Reduced motion, rendered in its resting state

Forced with `--force-prefers-reduced-motion` at both widths. The strip rests as
the static wrapped centred row the cascade gives it, **all twelve marks
visible**, now leading the section:

```
1440   two rows, 7 + 5
 390   three rows, 4 + 4 + 4
```

Nothing in the continuous-motion amendment moved. The resting state is still
the base in the cascade rather than something a media query restores, and the
move is markup order, which the animation never read.

#### The fold, unchanged

Measured with the viewport-sized probe from `mobile-check.md`'s second trap,
`innerHeight` printed beside the answer in every run so a wrong basis would be
visible:

```
390x664  usable 604   with banner 580  CLEARS by 24    without 523  CLEARS by 81
360x640  usable 580   with banner 579  CLEARS by  1    without 521  CLEARS by 59
```

Identical HEAD and now; the four reports hash byte-identical:

```
390x664  a85b1f87        360x640  92d39f42
```

Expected, since `#factory-certified` sits 9,098px down the page at 1440, but
measured rather than assumed.

#### Home untouched

`git status` carries one tracked change, `docs/collision-repair/index.html`.
`docs/index.html` and `docs/assets/site.css` are unmodified. The homepage's own
strip keeps its position under its head; this ruling was made about this
section and is recorded in this section's comment, not in the mold.

### 3.41 The pairs leave the lift, on the client's eye. BUILT 2026-09-23

**3.39 is withdrawn.** `figure.ba` leaves the lift on every page. Client
ruling 2026-09-23, after using it on the live staging build.

**This is a withdrawal, not a correction.** 3.39 was built exactly as
specified and worked exactly as proved: the membership was real membership,
the selector count did not move, the exception was an absence rather than an
override, and the swept rule rendered on both grounds. Nothing about it was
wrong. The client looked at it in use and decided the pairs read better still,
which is a judgement the record cannot make and the only person who can make
it made it. **It is recorded forward, in a new commit with its own number.
3.39 stays where it is and gains one line pointing here.** History is not
rewritten to make a decision look like it was never taken.

#### The restoration is exact, not approximate

`docs/assets/site.css` was returned to its state at **662b89a**, the commit
before 3.39, and the proof is that it diffs empty against it:

```
git diff 662b89a -- docs/assets/site.css     (no output)
```

That covers the whole file, not only the lift block, so there is no room for
a line that came back slightly different. `grep` finds **zero** occurrences of
`.ba` inside the lift block, lines 764 to 854. The eleven selector lists read
`.card, .step, .svc, a.svc-card` again, and the banner comment's member list
is `.card, .step and .svc`.

#### The prose came out with the behaviour

Law text describing behaviour that no longer exists is the kind of record that
rots, so every sentence 3.39 wrote was removed with it:

- the ox-on-dark exception paragraph in the lift block's `.dark .card::after`
  comment, including the line saying that adding `.ba` there later would undo
  the ruling;
- the matching paragraph in `CLAUDE.md`, and `.ba` out of the lift's member
  sentence in rule 7;
- the hover-shadow sentence added to the `.ba img` not-broken note, which now
  ends at "it is not broken." again and covers only the resting print shadow;
- the lift paragraph in `templates/service-page-template.html`'s Real Repairs
  block.

`CLAUDE.md` and the template were restored from 662b89a the same way and diff
empty against it too.

#### What stays, and was checked rather than assumed

Nothing from any other record moved. The ink ground on `/collision-repair/`'s
Real Repairs (3.38), the `.dark .ba` caption grammar, the resting print
shadows and their not-broken note (3.33), the AFTER chip's oxblood fill
(3.33), and the brand strip's new position at the head of `#factory-certified`
(3.40) are all untouched. Measured on the rendered page rather than read off
the diff:

```
.ba img box-shadow   rgba(18, 27, 39, .16) 0 12px 28px, rgba(18, 27, 39, .10) 0 3px 8px
```

That is the print shadow, present on both pages at both widths after the
withdrawal.

#### Computed style: the membership is gone at the element

`figure.ba` on both pages, at 1440 and at 390:

```
                 20f87a3 (3.39)                     now
position         relative                           static
transition       transform                          all  (the default)
::before         content ""  shadow rgba(18,27,39,.34)   content none
::after          content ""  width 28px  bg rgb(105,28,23)   content none
```

Both pseudo-elements are free again, which is the lift's own requirement for
whatever might want them next.

#### Nothing moved, and one thing stopped being painted

**Layout is identical everywhere**, which the brief expected because the lift
was hover-only:

```
                          20f87a3     NOW
home       1440  #real-repairs h=2728  2728   page end  8689 ->  8689
home        390  #real-repairs h=3321  3321   page end 12244 -> 12244
collision  1440  #real-repairs h=2640  2640   page end 13514 -> 13514
collision   390  #real-repairs h=3157  3157   page end 20722 -> 20722
```

**But "minus the hover behaviour" is not the whole of it, and that is worth
saying plainly.** The lift's `::after` painted **at rest** as well: a 28px by
2px oxblood tick at the base of every member, at opacity .4. Joining the mold
gave the pairs that tick; leaving it takes the tick away. So five marks per
page stop being drawn, and a full-page pixel diff at 1440 finds exactly them:

```
home       5 clusters  x180..207  2px tall   (186,156,154) -> (240,242,242)
collision  5 clusters  x180..207  2px tall   ( 52, 27, 32) -> ( 18, 27, 39)
```

Both reduce to the mold's own arithmetic. Ox is rgb(105,28,23); at alpha .4
over `--silver` rgb(240,242,242) that composites to **(186,156,154)** and over
`--ink` rgb(18,27,39) to **(53,27,33)**, against a measured (52,27,32), one
level per channel of the browser's own rounding. **The ink row is the 3.39
exception disappearing**: that tick stayed oxblood on the dark ground rather
than turning silver, and it is what the ruling was about.

Five per page is one per `figure.ba`, and both pages carry five.

#### The rest of the diff is the strip's animation phase

The pixel diff also flags a band across `#brands` on each page, at y6817..6846
on home and y9235..9264 on the collision page. **Those are the drifting
manufacturer marks caught at a different point in their 40-second cycle, not a
change.** Proved rather than argued: the home page was rendered **twice from
the same server, same commit, same URL**, and the two renders of the identical
page differ like this:

```
#brands band        rows 6768..6896    16088 differing pixels
tick row 1          rows 3420..3445        0   identical
tick row 5          rows 5360..5385        0   identical
above the pairs     rows 2500..3400        0   identical
below the strip     rows 7000..8000        0   identical
```

The strip is `animation: brand-drift 40s linear infinite`, a pure transform, so
two headless renders sample it at different phases and nothing else moves. **The
five ticks per page are the only real change in the whole diff.**

#### The fold, unchanged on both pages

Viewport-sized probe, `innerHeight` printed beside every answer. Eight runs,
two pages by two viewports by before and after, and the four report pairs hash
byte-identical:

```
home       390x664   with banner 594  CLEARS by 10    without 537  CLEARS by 67   f12d0a1f
home       360x640   with banner 635  MISSES by 55    without 578  CLEARS by  2   e889cfec
collision  390x664   with banner 580  CLEARS by 24    without 523  CLEARS by 81   a85b1f87
collision  360x640   with banner 579  CLEARS by  1    without 521  CLEARS by 59   92d39f42
```

The home page's 360x640 miss with the banner showing is the standing state and
not something this change caused: the banner comes off at cutover, and the
without-banner row is the one that describes a customer. It is identical
before and after, as are the other seven.

#### The stamp went backwards, which is correct

`site.css` is byte-identical to 662b89a, so its content hash is too, and
`scripts/stamp-assets.py` put `?v=e9d90441` back on all three files. **A
returning stamp is still a changing stamp**: any browser holding the 3.39
stylesheet at `?v=35795e3f` is asked for a different URL and gets the
reverted file.

#### The mold is back to three members

`.card`, `.step` and `.svc`, plus `a.svc-card`. **A future component still
needs both of its own pseudo-elements free to join**, and `figure.ba` has both
free again, so this is a withdrawal rather than a door closing.

### 3.42 The print shadow learns to speak dark-ground. BUILT 2026-09-23

On a dark ground the Real Repairs photographs get their lifted look back.
Client ruling 2026-09-23. One scoped rule, in the `.ba` component's dark mode,
beside the caption grammar that already lives there:

```css
.dark .ba img {
  box-shadow: 0 14px 32px rgb(0 0 0 / .62),
              0 4px 10px rgb(0 0 0 / .50);
}
```

**It is the dark-ground expression of an idea the site already has, not a new
one.** The print shadow 3.33 added is `--ink` by its channels, so on the ink
section it is ink on ink and describes nothing. The answer is the same
argument in the ground's own language: a **true black** shadow, which reads
because black is darker than ink. **Black is the floor** — a shadow has to be
darker than whatever it lies on, and ink is the darkest ground this section can
sit on.

**The geometry runs larger and the alpha deeper than the light-ground shadow,
deliberately.** Dark grounds eat shadow contrast, so the numbers that describe
weight on silver describe nothing on ink. **The client picked the assertive
strength from rendered comparisons**, and it is his pick rather than a
derivation from anything in this file.

#### It paints over the base rule; nothing forks

`.ba img` keeps its `--ink` shadow untouched. This rule simply wins the cascade
on a dark ground, at `(0,2,1)` against `(0,1,1)`. **The not-broken note is
updated rather than deleted**: it still says the base rule is deliberately left
alone and still tells anyone who came to "fix" the invisible shadow that it is
not broken, and it now ends by naming `.dark .ba img` as the sanctioned answer.
The old note's sentence "a shadow that vanishes costs nothing" is gone, because
the client has now decided it costs something.

#### Scoped through `.dark`, so it is the component's rule

Any page that darkens this section gets lifted prints with nothing written per
page, exactly as the captions have worked since 3.38. **Its reach was measured
structurally rather than assumed** — every `<section>` carrying `dark` on both
pages, counting `figure.ba` inside:

```
docs/index.html              #what-we-fix 0   #who-we-are 0   #testimonials 0   #start 0
docs/collision-repair/...    #real-repairs 5  #after-a-crash 0  #testimonials 0
                             #why 0   #contact 0
```

**So the rule can fire in exactly one place on the whole site**, and the ten
photographs inside it. The home page's Real Repairs carries no class at all, so
it is not a near miss; there is no dark `.ba` on that page to reach.

#### Computed style, read off the rendered pages

Both pages, at 1440 and at 390:

```
                      HEAD                                    NOW
home       rgba(18,27,39,.16) 0 12px 28px            unchanged
           rgba(18,27,39,.10) 0 3px 8px
collision  rgba(18,27,39,.16) 0 12px 28px            rgba(0,0,0,.62) 0 14px 32px
           rgba(18,27,39,.10) 0 3px 8px              rgba(0,0,0,.50) 0 4px 10px
```

`.ba img count=10` on both pages, so the rule reaches every photograph in the
section and nothing else.

#### The chips are untouched, by construction

The rule names `img`. The chips are spans lying on top of the photographs, and
they report identically before and after, at both widths:

```
AFTER chip   background rgb(105, 28, 23)   border rgb(240, 242, 242)   box-shadow none
```

#### Nothing moved

Shadows paint outside the box, so no section grows:

```
                    HEAD                           NOW
collision 1440  #real-repairs t2133 h=2640     identical
                #factory-certified t9098 h=1065  #brands t9186 h=127
                PAGE END 13514   doc 13514
collision  390  #real-repairs t3551 h=3157     identical
                #factory-certified t14403 h=1521
home      1440  #real-repairs t2820 h=2728     identical
                #what-we-fix t1630 h=1191   PAGE END 8689
home       390  #real-repairs t4894 h=3321     identical
                #what-we-fix t3054 h=1840
```

**The fold is identical on both pages**, measured with the viewport-sized probe
from `mobile-check.md`'s second trap, `innerHeight` printed beside every
answer. Eight runs, and the four report pairs hash byte-identical:

```
home 390x664  f12d0a1f    home 360x640  e889cfec
coll 390x664  a85b1f87    coll 360x640  92d39f42
```

Those are the same four hashes 3.40 and 3.41 recorded, so the fold has not
moved across three commits.

#### The pixel diff, and what it found

Full-page renders at 1440, working tree against HEAD, compared row by row. The
`#brands` marquee band is excluded from both counts: **3.41 proved it is
animation phase** by rendering one page twice and finding it the only thing
that differs.

**Collision: 2,215 differing rows, 30 of them the marquee, and the other 2,185
fall in exactly five bands.**

```
y2354..2730   x141..1298   120498 px
y2764..3140   x141..1298   120510 px
y3174..3650   x141..1298   132215 px
y3684..4160   x141..1298   131877 px
y4194..4670   x141..1298   132090 px
sample A=(18, 27, 39)  ->  B=(17, 26, 38)
```

**Five bands, one per `figure.ba`**, each spanning both photographs in its row,
and every one of them inside `#real-repairs`, which runs 2133 to 4773. Nothing
outside that section changed. The sampled pixel is the ink ground one level
darker, which is the black shadow's outermost falloff.

**Home: 31 differing rows, 30 of them the marquee, and one row left over.**

```
y1143   x429..1010   12 px   A=(223, 223, 223) -> B=(222, 223, 223)
```

Twelve pixels, one level of red, on the antialiased top edges of the services
router photographs — nowhere near a `.ba`, and unreachable by a `.dark`-scoped
rule. **It was chased rather than waved away, and it is rasterization noise.**
HEAD was rendered a second time and diffed against its own first render:

```
HEAD vs HEAD, second render     row 1142  0 px  identical
                                row 1143  12 px  first x429  A=(223,223,223) B=(222,223,223)
                                row 1144  0 px  identical
```

**The identical twelve pixels, at the identical x, with the identical colours,
between two renders of the same build.** A difference that reproduces with the
stylesheet held constant is not caused by the stylesheet. For completeness the
working tree was also rendered twice against itself and differed by **zero**
rows outside the marquee.

**And the assets are not the explanation either**: `diff -r` between the two
served trees reports `site.css` and nothing else, so every image is
byte-identical.

#### Rendered, and it reads

The section was rendered at 1440 and at 390. Each photograph now sits on a
visible dark halo and reads as a print lying on the ink rather than a picture
pasted into it; at HEAD the same frames are flat against the ground with no
separation at all.

#### The run was interrupted, and the proofs were finished across sessions

The machine slept repeatedly during this work. The edit sat proven but
uncommitted in the working tree, and several long pixel diffs were killed by
the sleeps and re-run. **Every number above is a real measurement that was read
back**, and the gates were re-run fresh after the interruptions rather than
trusted from before them: both test scripts exit 0, stamps and sitemap current,
audit 0 critical with both pages at 95/100 and `sameAs` the only warning.

`site.css` changed, so all three stamped files carry `?v=f26d599d`.

### 3.43 The marks take their place in the section's flow. BUILT 2026-09-24

On `/collision-repair/`, `<section id="brands">` moves a third time: it now
sits **between** `#factory-certified`'s head and its first paragraph. Client
ruling 2026-09-24, revising 3.40.

**The head introduces, the marks illustrate, the prose explains.** You read
"Factory-Certified Collision Center" and "Twelve manufacturers, and the
procedures that come with them", you see which twelve, then you read what the
certification means.

#### The third arrangement, and what actually settled it

```
3.34   under the head          the sub announced the strip
3.40   above the head          the head captioned the strip
3.43   between head and prose  the head introduces, the marks illustrate
```

**The client's second requirement is what chose the position, and it was not a
composition argument: no huge spaces around the strip.** That requirement and
the position are the same decision. A **leading** strip needs band-air above it
or it collides with the section's top edge. An **inline** strip must not have
that air, or it reads as a stripe with moats instead of a step in the flow. One
position can be quiet; the other cannot. The strip's markup did not change and
neither did a word of copy.

#### The air, and why the strip had too much of it

`#brands` carries `padding: calc(var(--pad) * .55) 0`. That is **band** padding
and it is correct where the strip is a band: on the home page `#brands` is a
standalone section between two others. Inside `#factory-certified` the same
padding sits on top of the section's own gaps and doubles them.

**The reference is not a matter of taste and it was not eyeballed.** The
section's head-to-body grammar is the margin `.sec-head` already leaves under
the sub before body text:

```
.sec-head { margin: 0 auto 40px }      ->   the grammar is 40px, flat at every width
```

Measured on the page after the move and before the fix, against that reference:

```
                              1440          390        target
sec-head box -> #brands        40            40          (the grammar itself)
sub text -> first mark         88            67           40
last mark -> first paragraph   48            26           40
#brands padding             48.4/48.4    26.4/26.4
first p margin-top              0             0
```

**The two sides do not start from the same place**, which is why the answer is
not one symmetric number. Above the strip, `.sec-head`'s own margin already
supplies the whole 40, so the strip must add **nothing**. Below it nothing else
contributes at all, because `p` has `margin-top: 0`, so the strip must supply
**all** of it. Hence:

```css
#factory-certified #brands { padding-top: 0; padding-bottom: var(--sec-gap); }
```

Measured again after:

```
                              1440          390        target
sub text -> first mark         40            40          40
last mark -> first paragraph   40            40          40
#brands padding              0/40px        0/40px
```

**Both gaps land on the grammar exactly, at both widths.** A consequence worth
noting: inline, `#brands` is now **70px tall at every width** where it was 127
at 1440 and 83 at 390. A band scales with `--pad`; an element matching a flat
grammar is flat.

#### One value plus a derivation

Two places now have to agree on 40px, so it became a token rather than a number
typed twice:

```css
--sec-gap: 40px;                                    /* new, beside --statcard-air */
.sec-head { margin: 0 auto var(--sec-gap); }        /* was the literal 40px */
```

`.sec-head`'s computed value is unchanged, so nothing renders differently for
it. This is the same move `--statcard-air` made in 3.31 and the reason is
CLAUDE.md's own line: two values that must agree are one value plus a
derivation. **The other `40px` values in the stylesheet were deliberately left
alone** — the footer's `margin-top` and the badge list's margin are not this
grammar and tokenising them would be a claim that they are.

#### Scoped to the nested context, on purpose

`#factory-certified #brands` describes **where** the element is, not what it
is, which is the same genre as the compound-selector lesson. The home page's
standalone band keeps its band padding untouched, and this was checked rather
than assumed: `docs/index.html` contains no `#factory-certified` element at all
— the only occurrence of that string is a stat label, `"Vehicle brands,
factory-certified"` — so the rule cannot reach it. Confirmed on the rendered
pages:

```
collision  #brands padding  0px / 40px
home       #brands padding  48.4px / 48.4px
```

#### The marquee limits are untouched

Nothing in the animation block was edited, and the diff proves it: no line
containing `animation`, `hover`, `focus-within`, `keyframes`, `brandtrack`,
`brandmarquee` or `prefers-reduced` appears in the stylesheet diff at all. Read
back off both pages:

```
.brandmarquee  animation-name brand-drift   duration 40s   linear   infinite
               play-state running           transform only
tracks 3   marks in the real track 12   visible 12   flex-wrap nowrap
.brandstrip    overflow hidden
```

**Rendered under `--force-prefers-reduced-motion`** at both widths: the static
wrapped centred row, **all twelve marks visible**, now sitting in the section's
flow — two rows of 7 + 5 at 1440, three of 4 + 4 + 4 at 390. The resting state
is still the base in the cascade, and the move is markup order, which the
animation never read.

#### The section shrinks, which is the point

```
                          3.42        NOW      delta
1440  #factory-certified  1065        1009      -56
      PAGE END           13514       13457      -57
 390  #factory-certified  1521        1508      -13
      PAGE END           20722       20710      -12
```

**This is the padding coming out, not a regression.** At 1440 the strip loses
48.4 above and 8.4 below; at 390 it loses 26.4 above and *gains* 13.6 below,
because a flat 40 is more than a phone's band padding was. The grammar is flat,
so matching it costs a little height on a phone and saves a lot on a desktop.

#### Order, count and the fold

```
order inside #factory-certified   .sec-head, #brands, .prose, .payoff, .prose
strips on the page                1
brand check                       2 strips of marks, 8 mentions in visible text,
                                  1 in JSON-LD, all saying 12
```

**The fold is identical on both pages**, viewport-sized probe, `innerHeight`
printed beside every answer, eight runs, four report pairs hashing
byte-identical:

```
home 390x664  f12d0a1f    home 360x640  e889cfec
coll 390x664  a85b1f87    coll 360x640  92d39f42
```

Those are the same four hashes 3.40, 3.41 and 3.42 recorded. **Four commits and
the fold has not moved.**

**Home is byte-identical except its stamp** — one line changed, the
`?v=bdb05a6c` on the stylesheet link.

#### Judged by eye, at both widths

Rendered and read: ink band, ground, heading, sub, marks, prose. The marks read
as a step in the section rather than a stripe with moats, at 1440 and at 390.
That was the client's requirement and it is the thing the numbers above were
chosen to produce.

`site.css` changed, so all three stamped files carry `?v=bdb05a6c`.

### 3.44 The ask joins the collision page's section bottoms. BUILT 2026-09-24

The hero's CTA pair is added at the foot of `#process`, `#real-repairs` and
`#factory-certified` on `/collision-repair/`. Client ruling 2026-09-24. **This
extends to this page the rhythm the client approved on the home page in 3.30:
the ask at the moment a section finishes its argument.**

#### It supersedes 3.34's no-CTA reasoning, which is kept rather than deleted

3.34 gave `#real-repairs` no CTA row on this page and said why: the home
section carries the pair only because the front door had no ask between its
hero and `#start`; this page already carries two act bands; a third ask inside
a proof section would be the duplication 3.27 took out.

**That was a real argument and it lost to use.** The home page's
section-bottom asks proved themselves in practice, and the client extended the
pattern. The note in the page's own markup now records the reversal in place,
with the old reasoning quoted inside it, because a comment that simply
disappears takes the argument with it.

#### The markup: nothing new was written

The hero's own `.cta-row`, copied verbatim, three times, as the last element
inside each section's `.wrap`. **No new wording, no new claim, no new button.**
Proven as in 3.30, by normalising indentation and hashing:

```
                       rows   distinct shapes   sha256
/collision-repair/      6            1          6a965cc84ded
/                       4            1          6a965cc84ded
```

**All ten rows on the site are the same four lines**, and every one carries the
same two hrefs, `tel:+12153225350` and `mailto:contact@tricountycollision.com`.
The count on this page goes **3 to 6**: the hero plus the two act bands, plus
the three new.

#### The generalisation 3.30 asked for

3.30 centred one light section with `#real-repairs .cta-row` and said in as
many words that a **second** light section wanting the same thing would be the
moment to generalise. `#process` and `#factory-certified` are the second and
third, so the trigger has fired. The id-scoped rule is gone and one mold
replaced it:

```css
section > .wrap > .cta-row:last-child { justify-content: center; }
```

**It is position, not identity.** A `.cta-row` that closes a section's `.wrap`
is a section-bottom ask, and section-bottom asks centre. No page and no section
is named, and a fourth one needs nothing written for it. The old comment's
trigger sentence is resolved in place rather than deleted: the new comment
quotes what 3.30 predicted and says that it happened.

**The hero is excluded by structure, not by an exemption**, which is why there
is no `:not()` to keep in sync. Both heroes nest their copy as
`.heroB > .heroB-copy > .wrap`, so the hero's row is not the child of a wrap
that a **section** owns and the child combinator cannot reach it.

**That was measured before the rule was written, and it is the reason the rule
has the `section >` step at all.** The obvious selector,
`.wrap > .cta-row:last-child`, would have been wrong:

```
home hero row    parent = .wrap    lastChild = TRUE    justify = normal
```

The home hero's row **is** the last child of its wrap. A positional selector
without the `section >` step would have centred it and moved the one thing the
flush-left hero turns on. **The base `.cta-row` stays left-aligned**, as 3.30
recorded.

#### Every row, measured after

```
/collision-repair/  1440
  [0] HERO                light  last=false  mold=false   justify=normal  mt=24px
  [1] #process            light  last=true   mold=true    justify=center  mt=26px
  [2] #real-repairs       DARK   last=true   mold=true    justify=center  mt=44px
  [3] #after-a-crash      DARK   last=true   mold=true    justify=center  mt=44px
  [4] #factory-certified  light  last=true   mold=true    justify=center  mt=26px
  [5] #why                DARK   last=true   mold=true    justify=center  mt=44px

/  1440
  [0] HERO                light  last=TRUE   mold=false   justify=normal  mt=24px
  [1] #what-we-fix        DARK   last=true   mold=true    justify=center  mt=44px
  [2] #real-repairs       light  last=true   mold=true    justify=center  mt=26px
  [3] #start              DARK   last=true   mold=true    justify=center  mt=44px
```

**Home's values are identical to HEAD's**, row for row, including
`#real-repairs` at `center` / 26px — which used to come from the id-scoped rule
and now comes from the mold. That is the home page proved unchanged by computed
style rather than by assumption.

**The grounds arrive free.** `#process` and `#factory-certified` are light, so
the base button grammar applies, the ox fill at the 10.50 recorded in 3.30.
`#real-repairs` is dark, so `.dark .cta-row` gives it centring **and** the
deeper 44px margin, and the dark button grammar gives the ink fill with silver
text, exactly as on the home page's ink band. Nothing was written per section.

**`.dark .cta-row` and the mold do not collide**: the first sets
`justify-content` and `margin-top`, the second sets only `justify-content`, so a
dark row keeps its deeper air and a light one keeps the base 26px.

#### At 390 the rows stack, as the hero does

```
          row height   x span
new rows     138       20..370
hero row     136       20..370
```

138 is 62 + 14 + 62, two buttons at natural width with the base gap. The hero
is 136 because it carries its own `gap: 12px` below 600px. **Same wrap
behaviour, one pixel pair of difference, and that difference is the hero's own
rule.**

#### Heights, and what they cost

```
                      HEAD     NOW    delta
1440  #process        1079    1167     +88
      #real-repairs   2640    2746    +106
      #factory-cert   1009    1097     +88
      PAGE END       13457   13739    +282
      screens @604   22.28   22.75   +0.47

 390  #process        2045    2209    +164
      #real-repairs   3157    3339    +182
      #factory-cert   1508    1672    +164
      PAGE END       20710   21220    +510
      screens @604   34.40   35.25   +0.85
```

**Every delta is exact arithmetic**, margin plus row height: at 1440, 26 + 62 =
88 on the light sections and 44 + 62 = 106 on the dark one, and 88 + 106 + 88 =
282. At 390 the row stacks, so 26 + 138 = 164 and 44 + 138 = 182, and
164 + 182 + 164 = 510. `#services`, `#after-a-crash` and `#why` are unchanged.

**The page costs a phone reader about nine tenths of one screen** for three
more chances to call.

#### The ask rhythm, which is the point of the ruling

Measured at 1440, every ask on the page including the contact block:

```
                        HEAD                          NOW
1  HERO                 466                           466
2  #process             --                           2071   gap 1543
3  #real-repairs        --                           4817   gap 2684
4  #after-a-crash      7229   gap 6701               7423   gap 2544
5  #factory-certified   --                          10239   gap 2753
6  #why               10831   gap 3540              11113   gap  812
7  #contact           11561   gap  668              11843   gap  668
```

**The finding is the 6,701px hole.** A reader who did not act in the hero had
to scroll nearly seven thousand pixels before the page asked again. It is now
1543, then a steady 2544 to 2753 through the body, and the tail is unchanged:
the act band, the area block and the contact block still cluster at 812 and
668, because they always did.

An annotated full-page render at 1440, with every ask marked and every gap
labelled, was produced for the client's eye and is in the session scratchpad as
`askrhythm.png` (1450 x 14200). It is not committed: a staging render is not a
repo asset.

#### The fold, and the rule that was not swept

**The fold is identical on both pages**, viewport-sized probe, eight runs, four
report pairs hashing byte-identical:

```
home 390x664  f12d0a1f    home 360x640  e889cfec
coll 390x664  a85b1f87    coll 360x640  92d39f42
```

The same four hashes 3.40, 3.41, 3.42 and 3.43 recorded. **Five commits and the
fold has not moved.**

**`.prose + .cta-row` is now redundant and was deliberately left standing.**
Measured by DOM matching: it matches 2 rows on this page and 0 on the home
page, and the count it matches that the mold does **not** is **zero**. So it
changes nothing today. It was not swept because it is not this rule's to sweep:
it centres a row following a `.prose` anywhere, including mid-section, and the
service-page template can still produce that shape. A sweep deletes only what
it owns. The finding is recorded in the stylesheet beside the mold so the next
person has the number.

`site.css` changed, so all three stamped files carry `?v=ce5093ed`.

### 3.45 The closing promise reaches the collision page, wearing ink. BUILT 2026-09-24

`/collision-repair/`'s "Contact Us for Your Free Estimate" facts block retires,
and the home page's closing act band takes its place. Client ruling 2026-09-24.
**The block informed; this one asks.**

#### The before and after

**The heading pair:**

| | |
|---|---|
| **Before** | **Contact Us for Your Free Estimate** — "One phone number, one email address, one shop" |
| **After** | **We will get you back on the road with your vehicle restored to its pre-accident condition.** — "Estimates are free and there is no obligation" |

**The facts block, removed whole.** Its entire visible text was:

```
Contact Us for Your Free Estimate
One phone number, one email address, one shop
Address    995 Jaymor Rd, Southampton, PA 18966
Phone and email    (215) 322-5350    contact@tricountycollision.com
Hours    Monday to Friday, 8 a.m. to 6 p.m.    Saturday by appointment only
Estimates are free. Call (215) 322-5350 or email contact@tricountycollision.com.
```

**No word of it was rewritten; it was deleted, and nothing it said was lost.**

#### Every fact it carried is already in this page's footer

3.29 made the footer the contact section on the home page on 2026-09-22. **This
completes the same move on the second page**, and the condition was checked by
grep before the block was deleted rather than remembered:

```
address + ZIP   docs/collision-repair/index.html:1147-1148   (again at :1179)
phone           :1149                                        (again at :1169, :1179)
email           :1150                                        (again at :1170, :1179)
hours           :1155-1156
```

`#area` also names the street in prose. **Nothing the block published stopped
being published.**

#### Verbatim from home's `#start`, with one difference

The block was copied from `docs/index.html`'s `#start`. The proof is a hash:
normalising **only** the ground class turns one into the other exactly.

```
collision block as shipped                    sha256 3c7aa385e03f
home #start                                   sha256 35bcfe67f30a
collision with field-ink -> field-ox           sha256 35bcfe67f30a   IDENTICAL
```

Headline and eyebrow are byte-identical strings, checked separately:

```
h2       "We will get you back on the road with your vehicle restored to its pre-accident condition."
sec-sub  "Estimates are free and there is no obligation"
```

#### The ground is the one difference, and it is not an exception

Home's closing band is `field-ox`; this one is `field-ink`. **The palette law
and the ruling agree by construction, because ox maps to act, not act to ox.**
The act-band rule caps a page at its two oxblood bands and this page already
spends both, on `#after-a-crash` and `#why`. An ink band may still ask, exactly
as the ink hero on the home page asks. No amendment is needed and none was
written.

#### The button grammar arrived free, and was verified rather than assumed

Nothing was written for the buttons. `.dark` supplies the treatment and
`.dark .cta-row` centres the row, the same rules home's band rides. Computed
style on the rendered page, at 1440 and at 390:

```
row      justify-content: center     margin-top: 44px
FILL     background rgb(105, 28, 23)   colour rgb(240, 242, 242)   border 2px rgb(240, 242, 242)
GHOST    background rgba(0, 0, 0, 0)   colour rgb(240, 242, 242)   border 2px rgb(240, 242, 242)
```

That is `--ox` filled with `--silver` text and the silver hairline for Call, and
a silver outline for Email: **the hero's own ink treatment**, which is the
symmetric act-button rule of 2026-09-10 doing its job on a third ground without
being told.

#### The id changed and nothing linked to it

`grep` found **no `href="#contact"` anywhere under `docs/` or `templates/`**,
and this page carries no in-page anchors at all. So the id is now `start`,
matching its new job and the home page's grammar for the same component.

#### `.contact` came off the section; its rules stay

The brief's sweep condition was tested and **it fails**, so nothing was deleted:

```
templates/service-page-template.html:612   <section class="dark contact field-both" id="contact">
templates/service-page-template.html:670   <p class="contact-alt">...
```

The template still carries `.contact` and `.contact-alt`, and the
`.contact-grid` rules with them. **This page was not their last user.** A sweep
deletes only what it owns, so the class came off this one section and
`site.css` was not touched at all.

#### The band rhythm did not move, because the old block was already ink

This is the cleanest answer to the seam question: the retired block was
`dark field-ink` too, so **the ground sequence at the page tail is identical
before and after.** Only the content inside the slot changed.

```
                 HEAD                          NOW
#why             OX     t10389 h=874          OX     t10389 h=874
#area            panel  t11263 h=579          panel  t11263 h=579
the band         INK    t11843 h=423   ->     INK    t11843 h=439
#faq             silver t12265 h=883          silver t12281 h=883
footer.site      INK    t13148 h=591          INK    t13164 h=591
```

**Same slot, same ground, same neighbours.** No two same-ground bands abut: the
FAQ puts 883px of silver between the closing ink band and the ink footer, as it
always did. Rendered and read at 1440 and at 390 to confirm by eye as well as by
number.

#### Heights, and a page that gets shorter on a phone

```
              HEAD      NOW     delta
1440  band     423      439      +16
      page   13739    13755      +16
 390  band     614      444     -170
      page   21220    21049     -171
```

**At 390 the page gets shorter by 171px.** The facts block stacked three
columns on a phone; the promise band is a headline, a line and two buttons.
At 1440 it costs 16px.

#### Untouched

- **JSON-LD is byte-identical**, one block before and after, sha256
  `3dc46f8a5b18`. The retired block carried no schema of its own, verified the
  same way 3.29 verified it.
- **`site.css` was not touched**, so there is no restamp and **the home page is
  byte-identical — not even a stamp line changed.** One file is modified in this
  commit.
- **The fold is identical on both pages**, viewport-sized probe, eight runs,
  four report pairs hashing byte-identical:

```
home 390x664  f12d0a1f    home 360x640  e889cfec
coll 390x664  a85b1f87    coll 360x640  92d39f42
```

The same four hashes 3.40, 3.41, 3.42, 3.43 and 3.44 recorded. **Six commits and
the fold has not moved.**

#### What this leaves open

The contact block was the page's only home for the hours, and the hours now
appear on this page **only** in the footer and the schema. That is the same
arrangement the home page has carried since 3.29 and it is deliberate, but it is
worth the owner knowing that a reader looking for opening times on a service
page now finds them at the bottom rather than in a band of their own. The form
question is unchanged: it lands on `/contact-us/` per `pagemap.md`, and the
retired block's note about it went with the block.

### 3.46 The spacing audit finds nothing, and two wrap orphans get bound. BUILT 2026-09-24

A full spacing audit of both pages at 1440 and 390 — a pixel whitespace scan
plus section-box probes, run against `origin/main` at `b39866e` — **found no
spacing defects.** What it did surface was two typographic wrap orphans and one
measurement trap.

#### What the audit found, which is nothing

Recorded because a clean result is worth keeping: it is the baseline the next
change is measured against, and it is the answer to "should we tune the
spacing" for as long as the numbers hold.

```
section seams        two pads, 88-93px at 1440, 48-54px at 390
head-to-body gaps    40-54px
brand strip inline   40 / 40, as 3.43 set it
stat bands           even
ox act bands         proportionate
```

**No spacing was changed by this commit.** `site.css` was not touched at all.

#### Two orphans, and only the break points moved

**The footer hours.** At four-column footer widths the line broke as
`Monday to Friday, 8 a.m. to 6` / `p.m.`, leaving the meridiem alone on a line
of its own. Bound in all three footer copies:

```
BEFORE  <p>Monday to Friday, 8 a.m. to 6 p.m.<br>
AFTER   <p>Monday to Friday, 8&nbsp;a.m. to 6&nbsp;p.m.<br>
```

`docs/index.html:924`, `docs/collision-repair/index.html:1173`,
`templates/service-page-template.html:717`. **The Saturday line is untouched**
in all three.

**The home page's who-we-are heading.** At 1440 it broke as
`Family Owned and Operated, on Jaymor` / `Rd`.

```
BEFORE  <h2 class="sec-title">Family Owned and Operated, on Jaymor Rd</h2>
AFTER   <h2 class="sec-title">Family Owned and Operated, on Jaymor&nbsp;Rd</h2>
```

`docs/index.html:727`, **the heading only.** The body prose "on Jaymor Rd in
Southampton", the footer address block and the legal row all keep ordinary
spaces, deliberately: an address in a narrow column needs its break points, and
none of them orphans today.

**No word changed, only where a line may break.** Proved by decoding `&nbsp;`
back to a space and comparing word multisets against HEAD:

```
docs/index.html                        identical   1261 tokens
docs/collision-repair/index.html       identical   2893 tokens
templates/service-page-template.html   identical    148 tokens
```

Four lines changed across three files.

#### Verified on the lines the browser actually drew

Not by eye and not by arithmetic: each text node was walked a character at a
time, each character's client rect taken, and the characters grouped by the top
of their rect, which reconstructs the lines as rendered.

```
FOOTER HOURS                 BEFORE                          AFTER
home  1440   [1] "Monday to Friday, 8 a.m. to 6 "   "Monday to Friday, 8 a.m. to "
             [2] "p.m."                             "6 p.m."
coll  1440   [1] "Monday to Friday, 8 a.m. to 6 "   "Monday to Friday, 8 a.m. to "
             [2] "p.m."                             "6 p.m."
home   900   [1] "Monday to Friday, 8 "             "Monday to Friday, "
             [2] "a.m. to 6 p.m."                   "8 a.m. to 6 p.m."
coll   900   [1] "Monday to Friday, 8 "             "Monday to Friday, "
             [2] "a.m. to 6 p.m."                   "8 a.m. to 6 p.m."

HOME H2
      1440   [1] "Family Owned and Operated, on Jaymor "   "Family Owned and Operated, on "
             [2] "Rd"                                      "Jaymor Rd"
       900   [1] one line, no wrap                         one line, no wrap
```

**`p.m.` is never alone and no line ever ends with `Jaymor`.** Worth noting
precisely: at 1440 the break now lands before the **6**, at 900 before the
**8**. Both are correct — the binding makes `8 a.m.` and `6 p.m.` single units,
so the line breaks at whichever unit boundary fits, and the orphan cannot recur
at any width.

#### No CSS, so no stamp

`site.css` was not touched, `stamp-assets.py --check` exits 0 with all stamps
current, and no `?v=` moved. This is the first change in a while that alters
both pages and the template without a restamp.

#### The third probe trap, now recorded

`scripts/mobile-check.md` gains an entry beside the `vh` trap, because the
audit's own section probe produced a map about **400px wrong in the lower half
of a page** and the cause is worth never rediscovering.

**A probe iframe SHORTER than the page scrolls, and its scrollbar steals about
15px of layout width.** A frame asked for at 390 then lays the page out at
about 375. Nothing announces it. What makes it nastier than a flat offset:
every box is right until the first element whose text re-wraps at the narrower
width, and from there the error **grows** as more paragraphs re-wrap beneath
it. The top of the report agrees with the rendered page and the bottom does
not, which is the shape most likely to be believed.

```
                     iframe 20000 (short)   iframe 21700 (tall enough)
page width laid out  ~375                   390
lower-page boxes     ~400px off             to the pixel
```

**It is the exact complement of the `vh` trap**, and the two rules pull in
opposite directions, which is why both are easy to walk into:

```
a FOLD probe's iframe must EQUAL the real viewport
a SECTION probe's iframe must be AT LEAST as tall as the page
```

That is not a contradiction: a fold probe asks what fits on one screen, so its
frame is one screen; a section probe asks where things sit in the whole
document, so its frame must contain the document. **Two cheap ways to make the
mistake visible**: probe twice at two different tall heights and require the
maps to agree, or check one landmark such as the footer's top edge against
rendered pixels. Either would have caught it in one run.

The probe used for this record's own measurements reports its laid-out width
beside every answer for exactly that reason, and read **1440 OK** and **900 OK**
on all eight runs.

### 3.47 Auto glass joins the site, migrated from the live page. BUILT 2026-09-24

`/auto-glass-repair-replacement/`, built to the mold of `/collision-repair/`
from the shop's live page at
`https://tricountycollision.com/auto-glass-repair-replacement/`, **read on
2026-09-24.** The slug is kept, because the page keeps its purpose and every
unnecessary redirect spends a little of the rankings the migration promises to
keep. Nothing on the page was written for the shop; every wording change is
below, and every claim is on the claims list.

#### The before and after

| # | Where | Before (live) | After (this build) |
|---|---|---|---|
| 1 | `<title>` | Auto Glass Repair & Replacement, Southampton PA \| Tri County | Auto Glass Repair in Southampton, PA \| Tri-County Collision |
| 2 | meta, og and JSON-LD description | Windshield repair, replacement, and side and rear window service in Southampton, PA. Quality materials, insurance help, free estimates. Call (215) 322-5350. | Auto glass repair in Southampton, PA. Windshields, side and rear windows, insurance help, free estimates. Serving Bucks & Montgomery County. (215) 322-5350. |
| 3 | intro, paragraph 2 | At Tri County Collision Center, we handle auto glass repair... | At Tri-County Collision, we handle auto glass repair... |
| 4 | the Why list's heading | Why Choose Tri County Collision Center for Auto Glass | Why Choose Tri-County Collision for Auto Glass |
| 5 | FAQ 1 opener | It depends on the size, depth, and location of the damage. | Whether a chipped windshield can be repaired or needs replacement depends on the size, depth, and location of the damage. |
| 6 | FAQ 2 opener | It's a risk that grows with time. | Driving with a cracked windshield is a risk that grows with time. |
| 7 | FAQ 3 opener | Yes. Our technicians handle all types of auto glass: ... | Yes, our technicians handle all types of auto glass: ... |
| 8 | FAQ 4 opener | That depends on your coverage. | Whether insurance covers your auto glass repair or replacement depends on your coverage. |
| 9 | FAQ 5 opener | If your vehicle has camera-based safety features like lane departure warning, automatic emergency braking, or adaptive cruise control, then very likely yes. | Your windshield very likely needs recalibration after it's replaced if your vehicle has camera-based safety features like lane departure warning, automatic emergency braking, or adaptive cruise control. |
| 10 | FAQ 6 opener | Call us at (215) 322-5350 or request an estimate online. | To get an estimate for auto glass work, call us at (215) 322-5350 or request an estimate online. |
| 11 | CTA buttons | Call Now for a Free Quote / Get an Estimate Online | Call (215) 322-5350 / Email the shop |

**1.** The collision grammar, and 59 characters counted by machine. "&
Replacement" leaves the title and nothing else: it is still the H1, the
breadcrumb, the intro H2 and the FAQ heading. The name follows 1.1.

**2.** Adapted from the collision description's grammar, and it claims nothing
the live page does not: windshields, side and rear windows, "insurance help"
(the live meta's own words) and free estimates. **ADAS is deliberately not in
it**: the in-house recalibration claim is the one flagged sentence on this
page, and a meta description is not where it gets promoted. 156 characters,
counted by machine. **The three mirrors are byte-identical once decoded,
proved by hash:**

```
meta        156  f1447fa5a7a5c886
og          156  f1447fa5a7a5c886
JSON-LD     156  f1447fa5a7a5c886
```

**3 and 4.** The business name, per 1.1. Two places on this page.

**5 to 10, the standalone test.** Every one of the live page's six openers
failed it: four lean on the question for their subject ("It depends", "It's a
risk", "That depends", "then very likely yes"), one is a bare "Yes." and one is
an imperative with no subject matter. Each fix echoes the question's own words
and **nothing after the opening sentence changed**. FAQ 5 is a reorder, not a
rewrite: the same clauses, with the answer first. FAQ 6 also gains the
collision FAQ's link grammar: the number is a `tel:` link and "request an
estimate online" is a pending link to `/contact-us/`, which the live page left
as plain text.

**11.** Per 1.9: the number on the button, and the online estimate, which
pointed at a third-party CarWise form, replaced by the shop's one mailbox until
`/contact-us/` ships.

**Split and relevelled, no words changed.** The live page's first paragraph's
first two sentences are the hero lead and every sentence after them opens the
intro section, exactly as 1.5 did for the collision page. The live H3s become
section H2s and the three H4s under "Repair or Replace?" become card H3s.
Heading levels only. Curly quotes are straight, per 1.11, which the new FAQ
mirror needs anyway.

#### The FAQPage schema is new

**The live page shows six questions and carries no FAQPage node.** This build
adds it, generated from the same strings as the visible answers, so the mirror
holds by construction and the audit confirms it: **all 6 questions and answers
byte-identical, both directions.**

#### The in-house ADAS statement, migrated as written

"We perform ADAS recalibration at our Southampton facility, so your vehicle's
safety features work the way the manufacturer intended after the new glass goes
in." **Word for word, in its own section, neither strengthened nor softened
nor dropped.** It is the explicit claim `pagemap.md`'s ADAS gate rests on, and
until now it lived only on the live site (4.1b). It now ships on this staging
page, which makes the owner's answer to 4.2 more urgent rather than less.
FAQ 5 and the Why list also carry "We perform ADAS recalibration" without the
location, as the live page does.

#### The closing promise is held, and a page-true sentence is proposed

Tested against this page's own work, home's sentence reads wrong here:

| | |
|---|---|
| **Home and /collision-repair/** | We will get you back on the road with your vehicle restored to its pre-accident condition. |
| **Proposed for this page** | We will get you back on the road with quality glass, installed with the same care we bring to every repair. |

This page opens on a stone chip off Street Road, and **a chip is not an
accident in a customer's mouth**; the live glass page never uses the word. The
proposal keeps the shared frame, "We will get you back on the road with", and
completes it with the live page's own words from the Windshield Replacement
paragraph: "we install quality glass with the same care we bring to every
repair." **Nothing ships until Greg rules.** The band's slot carries a comment
naming the markup it takes, `class="dark field-ox" id="start"`, and it is the
last thing on this page waiting on an answer.

#### The hero is interim stock, and a cutover blocker

`hero-windshield-replacement-in-shop.jpg`, built by
`scripts/prepare-hero-photo.py --frame glass` from **AdobeStock_64691325**,
licensed by Greg with the generative-AI filter excluded. It is not this shop's
bay. **It joins the three stock accents in 4.9 as a cutover blocker**, and a
real Tri-County glass job joins the shoot list.

```
PROVENANCE, read before anything was built on it
  DigitalSourceType  (none declared)
  CreatorTool        Capture One 7 Windows       a raw converter
  C2PA               embedded manifest
  VERDICT            clean, no AI tell
SOURCE   4255x2832
CROP     columns 4..4251, all rows  ->  4248x2832, exact 3:2
SUBJECT  suction-cup lifters x 962..3544, y 877..2310  (saturated-red scan)
         INSIDE
RESAMPLE one box downscale, factor 3.54  ->  1200x800
PLATES   660 boxes of 100x50 on the output, 0 meet all three conditions
ENCODE   q92, 260,714 bytes; only APP0 JFIF survives the strip
```

**The script had to learn a wider source.** Both earlier heroes were 1440 wide;
these are four to eight thousand. Each new frame carries an explicit crop box,
the script refuses a box that is not exactly 3:2, and a crop wider than 1440 is
plate-scanned after the downscale with the box scaled by 1200/1440, so a plate
is the same fraction of the box in every frame. **The two existing frames take
exactly the path they always did**: the collision frame was re-run to a temp
directory and is **byte-identical** to the shipped asset. The home frame's
original is not on this machine and could not be re-run; it takes the same
default-box path the collision frame just proved. A new `--out-dir` flag makes
that proof possible without touching `docs/`.

**The windshield sticker was inspected at full resolution** and is out of
focus with no legible text. **The alt describes what the photograph shows**:
"Red suction-cup lifters set on a car's windshield in a repair bay, with a
second car behind it, hood up, carrying more lifters." og:image,
og:image:alt and `primaryImageOfPage` are driven from the hero element, per
3.35, and all three move again when a real photograph lands.

#### Chips, stat band, and what is withheld

**The chips are the collision four, in the same journey order**, byte-identical
in both chip lists. The live glass page argues no service-specific swap: it
makes no mobile-service or same-day claim, so there is nothing to propose.
**"Detailed after every repair" on a glass-only job is the open question 4.2
already asks**, and it now applies to this page too.

**The stat band travels byte-identical.** It is shop-wide, the same three proof
figures home's stat card carries. One question comes with it: **the live glass
page never mentions the lifetime warranty**, and the band says "Warranty on all
repair work". "All" includes glass work if it is true; see section 5.

**Real Repairs is withheld** under its own gate, since the shop has supplied no
glass-job photographs, and **the brand strip is withheld** because
certification is the collision page's subject. Both are recorded in a comment
where the section would sit.

#### Measured

**Fold**, viewport-sized iframe, `innerHeight` and computed `min-height`
printed beside every answer. Budget is `innerHeight` less the 60px call bar
below 900.

```
                  innerHeight  min-height  CTA ends  budget
390x664  banner       664      504.64px      599      604   clears by  5
390x664  cutover      664      504.64px      542      604   clears by 62
360x640  banner       640      486.4px       598      580   MISSES by 18
360x640  cutover      640      486.4px       541      580   clears by 39
430x745  cutover      745      560px         576      685   clears by 109
1440x900 cutover      900      522px         533      900   clears by 367
```

**The 360x640 banner-state miss is the H1, and it is recorded rather than
fixed.** "Auto Glass Repair & Replacement" runs three lines at 360 (127px)
where "Collision Repair" runs two, while this page's lead is a line shorter
than collision's. The H1 is the live page's own and it stays. The banner comes
off at cutover and **the without-banner row is the one that describes a
customer**, which is the standard 3.41 applied to home's standing 360x640
miss of 55. At 1440 the same two-line H1 makes the hero **603px deep, 3 past
the 600 3.21 held**.

**Scrim**, per the readability amendment: copy rendered, then rendered again
with every glyph transparent so the layout holds and the ground shows, and
every pixel under every glyph run sampled against its own text node's colour.

| Element | 1440 | 1920 | 430 | 390 | 360 | Needs |
|---|---|---|---|---|---|---|
| Breadcrumb | 9.40 | 9.40 | 9.52 | 9.01 | 9.60 | 7 |
| Eyebrow | 9.79 | 9.72 | 9.66 | 9.72 | 9.72 | 7 |
| H1 | **6.47** | 7.39 | 9.53 | 9.27 | 9.27 | 4.5 |
| Lead | 9.53 | 9.33 | 9.66 | 9.53 | 9.53 | 7 |
| Ghost button label | 9.98 | 10.25 | 9.72 | 9.66 | 9.66 | 7 |
| Chips (desktop) | 9.46 | 9.40 | n/a | n/a | n/a | 7 |

**Everything clears its standard; the scrim did not deepen.** The H1's 6.47 at
1440 is display type against a 4.5 floor. It dips because the two-line H1's
first line, "Auto Glass Repair &", reaches further into the fade than
collision's one line does. **The probe was calibrated first**, on
`/collision-repair/`, and landed within 0.3 of every figure in 3.21.

**Seams and heads**, section probe with the iframe taller than the page,
laid-out width printed, and the map taken at two iframe heights and required
to agree (**it did, at both widths**):

```
            seams            head-to-body
1440        176-178 (88+88)  40 on every section
390          96-98  (48+48)  40 on every section
```

Identical to `/collision-repair/`'s own seams on the same probe, 176-177 and
96-97.

**The ask rhythm.** Four asks: the hero, and the section bottoms of `#intro`,
`#repair-or-replace` and `#why`, the last being the oxblood act band.

```
                     1440            390
hero                  471             434
#intro               1509  gap  976  1975  gap 1405
#repair-or-replace   2300  gap  729  3362  gap 1249
#why                 3705  gap 1343  5158  gap 1658
tail to the footer         1228            1309
```

**The `#repair-or-replace` ask is the rhythm's answer, and it is also the live
page's.** Without it the phone ran 2,881px from `#intro` to `#why`, under the
3,000 bound but close to five phone screens. The live page puts its second
call button in the same place. With it, every phone gap is 1,249 to 1,658,
about two and a half screens.

#### What landing this page moved elsewhere, by mechanism

- **Home's Auto Glass router card became a link.** It was a `div` carrying
  `data-pending-href`, and the pending-link test fails from the day its target
  exists. It is now an `<a class="svc-card">`, words, image and alt untouched,
  so it gains the lift and the oxblood heading the linked cards wear.
- **The footer's two unbuilt services are pending spans.** This page is born
  with the four-service footer; Paintless Dent Repair and Commercial Collision
  Repair are `data-pending-href` until their pages land, and the same test will
  force each one into a link on its page's commit.
- **`docs/llms.txt`** lists the page and **`docs/sitemap.xml`** was regenerated
  with it, `lastmod` 2026-09-24 from the page's own `dateModified`.
- **No CSS.** Every component on the page already existed; `stamp-assets.py
  --check` exits 0.

#### Not carried from the live page

The Trustindex review widget and its eight reviews (4.4); the CarWise "Get an
Estimate Online" and "Book an Appointment" links; the live page's image
`accent-glass-repair-replacement.jpg`, **because old-site imagery is banned
from this repo** whatever it looks like, since the old vendor's licences cannot
be verified; the DocuSign "Authorization Forms" nav link; the duplicate
navigation; the CallRail number in the header; `info@` in the footer; and the
live schema's `priceRange`, offer catalogue and credential nodes. **The contact
block retired into the footer**, per 3.45: address, phone, email and the bound
hours line are all there.

#### Found while building, not changed

- **3.16 is now overdue.** It asked that the collision page's graph shape and
  home's agree "before the third page ships", with home's WebSite node the
  correct one. This page follows the collision page's shape, because the mold
  rule says the collision page wins and changing it is outside this run.
- **The collision page's intro paragraph is missing.** 1.12 records "Our
  family-owned shop has served drivers across Bucks County and Montgomery
  County for years, delivering expert collision repair with genuine care" as
  migrated. It was dropped in b7baa89's design fold on 2026-09-06 with no pair,
  and **"for years" is a live claim that silently disappeared.**
- **The collision page breaks the 3,000px ask bound at 390.** On the same probe
  its phone gaps run 4,650 and 4,546, `#services` to `#after-a-crash` and on to
  `#factory-certified`.
- **A fourth probe trap.** A screenshot taken with the window TALLER than the
  iframe froze the page mid-entrance, before the probe's CSS injection ran:
  veil translucent, copy at opacity 0. The scrim measurements here all used a
  window equal to the iframe, and were checked by eye to be settled.

### 3.48 Paintless dent repair joins the site, FAQ and all. BUILT 2026-09-24

`/paintless-dent-repair/`, built to the mold of `/collision-repair/` from the
shop's live page at `https://tricountycollision.com/paintless-dent-repair/`,
**read on 2026-09-24.** Slug kept. `pagemap.md` said to check the live page for
a visible FAQ: **it has one, six questions, and no FAQPage schema.** Both are
migrated. Absence would have beaten invention; there was nothing to invent.

#### The before and after

| # | Where | Before (live) | After (this build) |
|---|---|---|---|
| 1 | `<title>` | Paintless Dent Repair in Southampton, PA \| Tri County | Paintless Dent Repair in Southampton \| Tri-County Collision |
| 2 | meta, og and JSON-LD description | Paintless dent repair (PDR) in Southampton, PA removes door dings, hail dents, and minor damage without repainting. Free estimates. Call (215) 322-5350. | Paintless dent repair in Southampton, PA. Door dings and hail dents, no repainting, free estimates. Serving Bucks & Montgomery County. (215) 322-5350. |
| 3 | intro, paragraph 2 | At Tri County Collision Center, our skilled technicians use... | At Tri-County Collision, our skilled technicians use... |
| 4 | the Why list's heading | Why Choose Tri County Collision Center | Why Choose Tri-County Collision |
| 5 | FAQ 1 opener | PDR is a repair technique that removes minor dents without any repainting. | Paintless dent repair (PDR) is a repair technique that removes minor dents without any repainting. |
| 6 | FAQ 2 opener | No. Protecting your paint is the entire reason PDR exists. | No, PDR will not damage your paint. Protecting your paint is the entire reason PDR exists. |
| 7 | FAQ 3 opener | Yes. Hail damage is one of the things PDR handles best. | Yes, hail damage is one of the things PDR handles best. |
| 8 | FAQ 4 opener | ...usually need conventional bodywork instead. | ...usually need conventional bodywork instead of PDR. |
| 9 | FAQ 5 opener | That varies with the dent itself: ... | The cost of paintless dent repair varies with the dent itself: ... |
| 10 | FAQ 6 opener | Yes. Paintless dent repair works on most vehicles, ... | Yes, paintless dent repair works on most vehicles, ... |
| 11 | CTA buttons | Call Now for a Free Quote / Get an Estimate Online | Call (215) 322-5350 / Email the shop |

**1. The title gives up ", PA" to keep the whole name.** The collision grammar,
"Paintless Dent Repair in Southampton, PA | Tri-County Collision", is **63
characters**, three over the limit. The live title fitted by cutting the name
to "Tri County", which rule 6 does not allow. So the state goes, not the name:
59 characters, counted by machine. "PA" is still in the description, the
eyebrow, the intro H2 and the schema. **If Greg would rather keep the state,
the other 60-character option is "Paintless Dent Repair Southampton, PA |
Tri-County Collision"**, which reads as a keyword string rather than a
sentence.

**2.** The collision grammar again, claiming only what the live page claims:
door dings, hail dents, no repainting, free estimates. 150 characters. **The
three mirrors are byte-identical once decoded, proved by hash:**

```
meta        150  851e75c8d3a7ea6d
og          150  851e75c8d3a7ea6d
JSON-LD     150  851e75c8d3a7ea6d
```

**3 and 4.** The business name, per 1.1.

**5 to 10, the standalone test.** FAQ 1 opened on an acronym that means
nothing once lifted, and now defines it. FAQ 2, 3 and 6 opened on a bare "No."
or "Yes.": 3 and 6 are comma-merged into the sentence that follows, the
smallest fix, and FAQ 2 gains a sentence that says in words what "No." said,
because "No, protecting your paint is the entire reason PDR exists" still does
not say what is being denied. FAQ 4's "instead" had no antecedent once lifted.
FAQ 5's "That" was the question. **Nothing after the opening sentence changed**,
except that FAQ 5's phone number is now a `tel:` link, which it was not on the
live page.

**11.** Per 1.9.

**Split and relevelled, no words changed.** The live page's first two sentences
are the hero lead and the rest of its opening follows under the intro H2, per
1.5. The live H3s become section H2s. **The "What PDR Can Fix" list became
three cards**, the same shape `/collision-repair/` gives its three-item list
in `#factory-certified`, down to the closing paragraph's `margin-top:34px`: a
list inside the prose column rendered its closing sentence flush against the
last item, and the collision page had already solved that shape. Items
unchanged, no periods added. **The four "Why Drivers Choose PDR" reasons now
lead in bold** with their own first sentence, the grammar the collision page's
`#why` list uses. Plain on the live page; emphasis added, no word changed.

#### The closing promise is held, and a page-true sentence is proposed

| | |
|---|---|
| **Home and /collision-repair/** | We will get you back on the road with your vehicle restored to its pre-accident condition. |
| **Proposed for this page** | We will get you back on the road with the panel looking like nothing ever happened. |

This page opens on a door ding in a grocery store car park and names hail as
what PDR does best. **Neither is an accident in a customer's mouth**, which is
exactly the case the ruling anticipated. The proposal keeps the shared frame
and completes it with the live page's own words: "a dent isn't gone until the
panel looks like nothing ever happened." **It was chosen over "your factory
paint exactly as it is" on purpose.** That phrase is true of PDR, but this page
also promises conventional repair for dents that do not qualify, and
conventional repair repaints. The panel sentence is true of both routes. **Nothing
ships until Greg rules**, and the band's slot carries a comment naming its markup.

#### The hero is interim stock, and a cutover blocker

`hero-dent-lifter-on-red-door.jpg`, built by
`scripts/prepare-hero-photo.py --frame dent` from **AdobeStock_1571353580**.

```
PROVENANCE, read before anything was built on it
  DigitalSourceType  (none declared)
  CreatorTool        Adobe Photoshop 26.8 (Windows)
  C2PA               embedded manifest, no digitalSourceType asserted
  VERDICT            clean, no AI tell
SOURCE   8192x5464
CROP     columns 1..8190, rows 2..5461  ->  8190x5460, exact 3:2
SUBJECT  lifter x 4620..7463, y 975..2785, INSIDE
         (gold scan for the lifter, blue scan for the glue tab: a red car
          defeats a red scan)
RESAMPLE one box downscale, factor 6.825  ->  1200x800
PLATES   660 boxes of 100x50 on the output, 0 meet all three conditions
ENCODE   q92, 171,011 bytes; only APP0 JFIF survives the strip
```

**Photoshop is the one creator tool of the three that could have done
generative work**, so it was checked beyond the audit's reader: the embedded
manifest was searched for `trainedAlgorithmicMedia` and
`compositeWithTrainedAlgorithmicMedia` and carries neither. **What the frame
shows is a glue-pull lifter**, a paintless dent repair method, so the
photograph honestly shows this service even though it is not this shop. Alt:
"A gloved hand working a glue-tab dent lifter on a red car door, beside the
door handle."

#### Chips, stat band, and what is withheld

**The collision four, same order, byte-identical in both chip lists.** The live
page argues no swap: it says qualifying dents "can often be handled quickly"
but never "same day", so there is no service-specific chip to propose. **The
stat band travels byte-identical**, with the same question glass raised: the
live dent page never mentions the lifetime warranty.

**Real Repairs is withheld, and one pair nearly qualified.** The collision
page's Nissan Murano pair is captioned "Door dents", and it is still not this
page's evidence: **nothing records that it was repaired paintlessly**, and a
pair on the PDR page would claim it was. Recorded in the comment where the
section would sit. **The brand strip is withheld** as on glass.

#### Measured

**Fold**, viewport-sized iframe:

```
                  innerHeight  min-height  CTA ends  budget
390x664  banner       664      504.64px      580      604   clears by 24
390x664  cutover      664      504.64px      523      604   clears by 81
360x640  banner       640      486.4px       562      580   clears by 18
360x640  cutover      640      486.4px       504      580   clears by 76
430x745  cutover      745      560px         576      685   clears by 109
1440x900 cutover      900      522px         533      900   clears by 367
```

**Every row clears, banner state included.** The shorter lead buys back what
the two-line H1 costs. At 1440 the hero is 603 deep, as on glass, because
"Paintless Dent Repair" also runs two lines at `max-width: 17ch`.

**Scrim:**

| Element | 1440 | 1920 | 430 | 390 | 360 | Needs |
|---|---|---|---|---|---|---|
| Breadcrumb | 10.49 | 10.34 | 9.59 | 10.10 | 10.15 | 7 |
| Eyebrow | 10.43 | 10.10 | 9.97 | 10.27 | 10.10 | 7 |
| H1 | 9.59 | 9.46 | 9.65 | 9.53 | 9.39 | 4.5 |
| Lead | 9.78 | 9.72 | 9.85 | 9.53 | 9.53 | 7 |
| Ghost button label | 10.43 | 10.10 | 10.11 | 10.24 | 10.18 | 7 |
| Chips (desktop) | 9.84 | 10.17 | n/a | n/a | n/a | 7 |

**Every element clears 7:1 at every width; the scrim did not deepen.**

**Seams and heads**, iframe taller than the page, maps agreeing at two heights:
seams 176-178 at 1440 and 96-98 at 390, head-to-body 40 on every section.

**The ask rhythm:**

```
                     1440            390
hero                  471             434
#intro               1509  gap  976  1947  gap 1377
#when-not            2853  gap 1282  3600  gap 1515
#why                 4249  gap 1334  5372  gap 1634
tail to the footer         1228            1190
```

**`#when-not` carries the second ask because that is where the live page puts
its second button**: after the page has told you when PDR is the wrong fix, and
that the shop does the right one too.

**The grounds alternate**: white stat band, panel, ink, silver, panel, silver,
panel, oxblood, panel, silver. `#how-it-works` took the ink so the list could
sit on silver. `.payoff .card p` sets `--ink-2` after `.dark .card p` in the
cascade, so payoff cards on ink would be dark text on a dark card. **That is a
latent trap in the stylesheet, recorded here and not fixed**, because no page
puts payoff cards on ink and a rule nobody needs is not this run's to write.

#### What landing this page moved elsewhere, by mechanism

- **`/collision-repair/`'s "paintless dent repair (PDR)" is a link again**, as
  the live page has it. It waited as a pending span, section 2 promised it
  back, and the pending-link test forced it the moment the page existed. The
  comment above it is updated to say so, and section 2's row is struck.
- **Home's Paintless Dent Repair router card became a link**, as glass's did.
- **The glass page's footer span became a link**; the generator reads which
  pages exist, so the one line that changed there is exactly that.
- **`docs/llms.txt`** and **`docs/sitemap.xml`** carry the page. **No CSS.**

#### Not carried from the live page

The Trustindex widget; the CarWise links; the live image `Paintless-Dent-Repair.jpg`,
"Dent being buffed out of a car.", **because old-site imagery is banned from
this repo**; the DocuSign nav link; the CallRail number; `info@`; the live
schema's price and offer nodes. The contact block retired into the footer, per
3.45.

### 3.49 Commercial collision repair joins the site, and the promise ships. BUILT 2026-09-24

`/commercial-collision-repair/`, built to the mold of `/collision-repair/`
from the shop's live page at
`https://tricountycollision.com/commercial-collision-repair/`, **read on
2026-09-24.** Slug kept. The live page already carries FAQPage schema; it is
regenerated here from the same strings as the visible answers. **This page
carries the heaviest scope claims on the site**, and every one of them is
migrated as the live page makes it and listed in 4.10.

#### The before and after

| # | Where | Before (live) | After (this build) |
|---|---|---|---|
| 1 | `<title>` | Commercial Collision Repair in Southampton, PA \| Tri County | Commercial Collision Repair \| Tri-County Collision |
| 2 | meta, og and JSON-LD description | Commercial collision repair in Southampton, PA for work vehicles and fleets of all sizes. Certified technicians, free estimates, help with insurance claims. Call (215) 322-5350. (177) | Commercial collision repair in Southampton, PA for work vehicles and fleets. Free estimates, insurance help. Serving Bucks & Montgomery County. (215) 322-5350. (159) |
| 3 | intro, paragraph 2 | At Tri County Collision Center, we've built... | At Tri-County Collision, we've built... |
| 4 | the process lead-in | Here's how a commercial repair works at Tri County Collision Center: | Here's how a commercial repair works at Tri-County Collision: |
| 5 | the Why list's heading | Why Businesses Choose Tri County Collision Center | Why Businesses Choose Tri-County Collision |
| 6 | the area paragraph | ...businesses throughout the region rely on Tri County Collision Center for... | ...businesses throughout the region rely on Tri-County Collision for... |
| 7 | the Why list, item 1 | Family owned and operated [em dash] you'll deal with people, not a call center | Family owned and operated: you'll deal with people, not a call center |
| 8 | FAQ 1 opener | Just about all of them. | We repair just about all types of commercial vehicles. |
| 9 | FAQ 2 opener | That depends on the damage, and we won't pretend otherwise. | How long your work vehicle will be in the shop depends on the damage, and we won't pretend otherwise. |
| 10 | FAQ 3 opener | Yes. We work with all major insurance companies... | Yes, we work with commercial insurance policies. We work with all major insurance companies... |
| 11 | FAQ 4 opener | Yes. We work with businesses of every size. | Yes, we can repair multiple vehicles from the same fleet. We work with businesses of every size. |
| 12 | FAQ 5 opener | That's the standard. | Pre-accident condition is the standard. |
| 13 | FAQ 6 opener | Call (215) 322-5350 or request an estimate online. | To get a commercial repair estimate, call (215) 322-5350 or request an estimate online. |
| 14 | CTA buttons | Call Now for a Free Quote / Get an Estimate Online | Call (215) 322-5350 / Email the shop |

**1. No form of the collision grammar fits this service's name.** "Commercial
Collision Repair in Southampton, PA | Tri-County Collision" is 69 characters,
and even "Commercial Collision Repair, Southampton | Tri-County Collision" is 63.
The live title fitted by cutting the name to "Tri County", which rule 6 does
not allow. **So the location goes and the name stays**: 50 characters, counted
by machine. Southampton, PA is in the description, the eyebrow, the intro H2
and the schema. **Greg's alternative, if he will take a shortened name in
titles only**: the live pattern, "Commercial Collision Repair in Southampton,
PA | Tri-County" at 59.

**2. `pagemap.md` asked for "meta to 160", and it was 177.** It now claims
work vehicles and fleets, free estimates and insurance help (a trim of the live
"help with insurance claims"). "Certified technicians" and "of all sizes" came
out for length; both are still on the page. **The three mirrors are
byte-identical once decoded, proved by hash:**

```
meta        159  9ee41cbcb7b93a6b
og          159  9ee41cbcb7b93a6b
JSON-LD     159  9ee41cbcb7b93a6b
```

**3 to 6.** The business name, per 1.1. Four places on this page.

**7. The live list carried an em dash**, which the standards ban anywhere. A
colon does the same job and adds no word.

**8 to 13, the standalone test.** FAQ 1 and 2 opened on a pronoun that was the
question; FAQ 3, 4 and 6 on a bare "Yes." or an imperative. FAQ 3 and 4 gain
the question's own words rather than a bare comma-merge, because "Yes, we work
with all major insurance companies" lifted alone never says "commercial".
**FAQ 5 deliberately does not say "Yes."** The live answer is "That's the
standard," and "Pre-accident condition is the standard" is the same claim at
the same strength. The collision page's FAQ 2 did add a "Yes" (1.3); this one
did not need to. Nothing after any opening sentence changed, except that the
phone numbers in FAQ 1 and 6 are `tel:` links and "request an estimate online"
is a pending link to `/contact-us/`, as on the collision FAQ.

**14.** Per 1.9.

**Split and relevelled, no words changed.** The first two sentences of the live
opening are the hero lead; the rest, including the closing fragment "Whether
that's one delivery van or a lineup of tractor-trailers.", follows under the
intro H2, per 1.5. **The fragment is kept as it is**: it is the live page's
voice, and the standards protect voice. The live H2s stay H2s. **The six-item
process list became six `.step` cards**, each titled with its item's own lead
words and carrying the rest of the item, the treatment 1.13 gave the collision
process. The tiles are the collision page's own icons, reused, with the lane
icon from its safety card on step 06, "Back to work". Nothing was drawn.

#### The closing promise ships, byte-identical, on ox

| | |
|---|---|
| **The test** | Is "We will get you back on the road with your vehicle restored to its pre-accident condition." honestly true of this page's work? |
| **The answer** | Yes, in this page's own words: "Every vehicle leaves our shop in pre-accident condition", and its FAQ asks whether a work vehicle will "really be back to pre-accident condition". |

**The band is byte-identical to home's `#start` and the collision page's**,
proved by comparing the section's inner markup: **True** against both. **The
ground is ox**, the service-page default. The collision page's ink was that
page's own ruling, because its two oxblood bands were already spent. This
page's two are `#why` and this one, with `#area` between them, which is the
collision page's own tail shape.

**Glass and dent now each hold a proposed variant** (3.47, 3.48). If Greg
approves them as written, the three service pages share one frame, "We will
get you back on the road with", and each variant ships byte-identical
everywhere it appears.

#### A chip swap is proposed, and the default stays

**The live page argues downtime harder than anything else**: an H2 "Built to
Limit Downtime", a section "Downtime Is the Real Cost of an Accident", and a
Why item "Fast, efficient turnaround to limit downtime". So, per the ruling, a
pair is proposed and **the collision four ship unchanged**:

| | |
|---|---|
| **Default, shipped** | Free estimates · Insurance paperwork handled · ASE and I-CAR Gold Class certified · Detailed after every repair |
| **Proposed** | Free estimates · Insurance paperwork handled · ASE and I-CAR Gold Class certified · Built to limit downtime |

"Built to limit downtime" is the live H2's own words. It would replace the
detailing chip, which is the one of the four a fleet manager weighs least and
the one 4.2 already questions. **It is a claim about process, not a turnaround
promise**, and the page makes no numbered turnaround promise anywhere. If
approved, both chip lists change together, as 3.36 requires.

#### The brand strip is flagged, not added

**This page makes a manufacturer argument**, in `#fleet`: factory
certification for 12 brands, naming Ford, GM, Dodge and Chrysler, is why a
fleet's cars, vans and pickups can be repaired to manufacturer standards
without leaving Southampton. **That may earn the strip here.** One per page is
a ceiling, not a quota, and certification is the collision page's subject, so
it is not added. **Greg's call.** If it goes in, it goes in `#fleet` under the
paragraph that makes the argument, and the brand check will want the count
agreeing, which it already does.

#### The hero is interim stock, and a cutover blocker

`hero-wrecked-work-van.jpg`, built by
`scripts/prepare-hero-photo.py --frame commercial` from **AdobeStock_430555209**.

```
PROVENANCE, read before anything was built on it
  DigitalSourceType  (none declared)
  CreatorTool        Capture One 21 Macintosh    a raw converter
  C2PA               embedded manifest, c2pa.published only
  VERDICT            clean, no AI tell
SOURCE   5916x3944, already exact 3:2, so no pixel discarded
SUBJECT  the van x 1124..5679, y 402..3638, INSIDE
         (silver on grey under overcast: read off a 592px grid, an
          inspection and not a scan, exactly as the GMC was)
RESAMPLE one box downscale, factor 4.93  ->  1200x800
PLATES   660 boxes of 100x50 on the output, 0 meet all three conditions
ENCODE   q92, 271,550 bytes; only APP0 JFIF survives the strip
```

**Three things in the frame were inspected at full resolution before the
check ran**: the van's own plate mount is **empty**, bare bolts and rust; the
black car at the right edge shows a **blank** plate strip; and a "2" on the
van's door is **a reflection of a bay number**, not identifying. The densest
box the scan found, detail 13.01 at the van's hood, fails on detail alone.
Alt: "A silver work van with its hood crumpled and its front end torn open,
parked in a lot beside another car."

#### Real Repairs is withheld

The collision page's Dodge Grand Caravan is a minivan, and nothing this repo
holds makes it a work vehicle. **No commercial job has been photographed.**
Recorded where the section would sit.

#### Measured

**Fold**, viewport-sized iframe:

```
                  innerHeight  min-height  CTA ends  budget
390x664  banner       664      504.64px      580      604   clears by 24
390x664  cutover      664      504.64px      523      604   clears by 81
360x640  banner       640      486.4px       598      580   MISSES by 18
360x640  cutover      640      486.4px       541      580   clears by 39
430x745  cutover      745      560px         576      685   clears by 109
1440x900 cutover      900      522px         533      900   clears by 367
```

The same shape as glass, for the same reason: "Commercial Collision Repair"
runs three lines at 360. **The customer row clears by 39**; the banner row is
recorded, per 3.41. Hero depth at 1440 is 603, as on the other two.

**Scrim:**

| Element | 1440 | 1920 | 430 | 390 | 360 | Needs |
|---|---|---|---|---|---|---|
| Breadcrumb | 9.53 | 9.46 | 9.53 | 9.20 | 9.14 | 7 |
| Eyebrow | 9.53 | 9.65 | 9.66 | 9.39 | 9.39 | 7 |
| H1 | **5.11** | **6.03** | 9.59 | 9.46 | 9.46 | 4.5 |
| Lead | 9.39 | 9.33 | 10.05 | 9.53 | 9.53 | 7 |
| Ghost button label | 9.91 | 9.98 | 10.24 | 10.11 | 10.11 | 7 |
| Chips (desktop) | 9.98 | 9.91 | n/a | n/a | n/a | 7 |

**Everything clears its standard, and the H1 at 1440 is the thinnest margin
this run measured.** Its first line, "Commercial Collision", runs to **62.8% of
the frame**, into the scrim's fade and over the van's pale hood. The collision
page's H1 stops at 49.6%. At 5.11 against a 4.5 floor for display type, the
amendment says the scrim does not deepen, and it did not. **The obvious markup
fix is ruled out**: binding "Collision&nbsp;Repair" would keep the first line
short, but at 360 those two words need two lines and a bound pair would
overflow. **If Greg wants more headroom, the lever is the scrim's 68% stop in
`site.css`**, which is a CSS change and a decision for every hero, not this
page's to make.

**Seams and heads**, iframe taller than the page, maps agreeing at two heights:
seams 176-178 at 1440 and 96-98 at 390, head-to-body 40, and 44 on `#start`,
exactly as the collision page's `#start` measures.

**The ask rhythm:**

```
                     1440            390
hero                  471             434
#intro               1481  gap  948  1947  gap 1377
#process             3085  gap 1542  4594  gap 2509
#why                 4686  gap 1539  6668  gap 1936
#start               5591  gap  843  7587  gap  781
tail to the footer          817             890
```

**The longest phone run is 2,509**, from the intro to the foot of the process,
because six step cards stack to 1,924px on a phone. That is under the 3,000
bound. **Every ask sits where the live page puts one**, except the live page's
ask after the insurance section, which would sit one section before `#why`'s.

**The lane draws here.** `site.js` builds it on the first `.steps` of any page,
below 720px only, and this process runs from the first call to the vehicle back
in service. That is a road, which is the argument the lane was admitted on.
Checked at 390: the dashes sit between the six cards.

#### What landing this page moved elsewhere, by mechanism

- **Home's Commercial Collision Repair router card became a link**, the last of
  the three. **The router grid now links all four services.**
- **The glass and dent footers' commercial spans became links**, one line each.
  **The three new footers hash identical** once each page's `./` self-link is
  expanded to its slug: `70e68e99e9ff3d74`.
- **No `data-pending-href` points at any of the three service slugs anywhere
  under `docs/`.**
- **`docs/llms.txt`** and **`docs/sitemap.xml`** carry the page. **No CSS.**

#### Not carried from the live page

The Trustindex widget; the CarWise links; the live image `accent-welding.jpg`,
**because old-site imagery is banned from this repo**; the DocuSign nav link;
the CallRail number; `info@`; the live schema's price and offer nodes. The
contact block retired into the footer, per 3.45.

### 3.50 Every footer lists all four services. BUILT 2026-09-24

The three service pages of 3.47 to 3.49 were born with the four-service footer.
**Home, the collision page and the template now carry the same column**, in the
same order and the same words, each at its own depth.

#### The page list, grepped before applying

```
docs/index.html                                   swept
docs/collision-repair/index.html                  swept
docs/auto-glass-repair-replacement/index.html     already four, one label bound
docs/paintless-dent-repair/index.html             already four, one label bound
docs/commercial-collision-repair/index.html       already four, one label bound
templates/service-page-template.html              swept, token retired
```

#### The before and after

```
BEFORE  <li><a href="collision-repair/">Collision Repair</a></li>              (home)
AFTER   <li><a href="collision-repair/">Collision Repair</a></li>
        <li><a href="auto-glass-repair-replacement/">Auto Glass Repair</a></li>
        <li><a href="paintless-dent-repair/">Paintless Dent Repair</a></li>
        <li><a href="commercial-collision-repair/">Commercial Collision&nbsp;Repair</a></li>
```

The collision page's own item keeps its `./`, and the three new pages carry
`./` for themselves the same way. The template's `{{FOOTER_SERVICES}}` token
becomes the four items through `{{SERVICES_PATH}}`, which is the template's
existing token for cross-links to service pages, so a town page three levels
down gets the right depth for free. **The token's line in the template's token
list was rewritten to say so**; that line is the only change outside a footer
in this commit, and it is the documentation of the footer.

**The column is identical everywhere once depth is normalised**, proved by
parsing it out of all six files, stripping the relative prefix and expanding
each `./` to its page's slug: **all six equal.**

#### One label is bound, and it is the 3.46 orphan again

At 900 the new column broke "Commercial Collision Repair" as `Commercial
Collision` / `Repair`, a single word alone on the last line, the shape 3.46
bound out of the hours line. **"Collision&nbsp;Repair" is now one unit**, so
the break lands after "Commercial", and a page's words are unchanged. Because
the label is pattern text, **it is bound on all six files at once**, and the
three generated pages were regenerated to prove the build reproduces the swept
files byte for byte. It did. Rendered at 1440 the item sits on one line, and
at 900 it reads `Commercial` / `Collision Repair`.

#### Footers only, proved

Every changed line in `docs/` sits below its page's `<footer class="site">`.
Checked by hunk position, not by eye:

```
docs/index.html                                 footer at  908, hunk at  933
docs/collision-repair/index.html                footer at 1159, hunk at 1184
docs/auto-glass-repair-replacement/index.html   footer at  674, hunk at  701
docs/paintless-dent-repair/index.html           footer at  698, hunk at  725
docs/commercial-collision-repair/index.html     footer at  742, hunk at  769
templates/service-page-template.html            footer at  704, hunks at 111 (token list), 732
```

**The home router grid was not edited here.** It was converted card by card as
each page landed (3.47 to 3.49), because the pending-link test forced each one,
and it now links all four services. **No CSS, no stamp, no sitemap change**:
no page's `dateModified` moved, following 3.46, which bound a footer line on
both pages without moving either.

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

  **NEW FINDING, 2026-09-17, from the live site itself: the live homepage's
  logo strip shows FOURTEEN marks, not twelve.** The twelve above plus **RAM**
  and **Fiat**. The same live page's prose says "a dozen vehicle brands", so
  **the live site contradicts itself**: a reader who counts the pictures and a
  reader who reads the sentence get different answers, and an assistant reading
  the page gets the sentence.

  Nobody typed that on purpose. A logo carousel is built once in a page builder
  and the prose is written somewhere else, and after that neither knows about
  the other.

  **What this build does about it, and it is deliberately the conservative
  choice: the strip ships the TWELVE the site claims in words.** Adding RAM and
  Fiat because they appear in a carousel would be publishing a certification
  claim on the strength of a picture, and rule 1 says a fact is confirmed or it
  does not ship. Dropping the strip would lose the client's own recognition
  asset over a question that has an answer.

  **If the owner confirms RAM and Fiat, the count moves to fourteen
  EVERYWHERE in one commit**: `BRAND_COUNT` in `scripts/audit.py`, the two stat
  bands, the two prose lists on `/collision-repair/`, the FAQ answer, the FAQ
  schema, and two more marks in the strip. That is now enforced rather than
  remembered: the brand-count check fails the build if the marks, the visible
  text and the schema do not all say the same number, so a half-done update
  cannot ship. See 3.26.

### 4.1b Claims the homepage adds

- **"We fix it all", and the EIGHT damage types under it.** Rule 2, scope
  honesty: **does the shop do all eight, in house?** Hail in particular is the
  kind of work a shop either takes or sublets, and the glass items are the
  kind a shop often sublets whole.

  **THE ITEM COUNT HAS NOW MOVED THREE TIMES. Plainly, in order:**

  | When | Count | What |
  |---|---|---|
  | the live site | **five** | minor and major collisions as one item, cracked windshields, door dings and dents, deer strikes, hail damage |
  | 2026-09-13, planned | **six** | split minor from major. **Never reached a page.** |
  | 2026-09-17, shipped | **eight** | minor/major merged back to one, and three added: bumper damage, scratched and chipped paint, broken side and rear glass. Deer strikes kept, as a heading with no line. |
  | 2026-09-17, revised | **eight** | **deer strikes REMOVED** on the client's ruling, and minor/major **split back into two**. Every item now carries a line. |

  **Deer strikes was removed, not softened.** Dropping a claim needs no source.
  Deer work stays covered under collisions and by the existing post, verified
  on the live site as
  `/blog/deer-season-in-bucks-county-insurance-coverage-next-steps/`. **So the
  owner question about a deer line is closed**, and it was closed by deleting
  the claim rather than by answering it.

  **The three additions are ours, not the live site's**, and all three are
  sourced from published copy: bumper damage and scratched and chipped paint
  both come out of `/collision-repair/`'s own minor-damage paragraphs, and
  broken side and rear glass comes out of the live glass page, whose scope was
  **verified on 2026-09-17** as covering side and rear windows and not only
  windshields. Full sourcing table in 3.22.

  **Two of the eight lines are composed rather than migrated** and both need
  the owner: the bumper line and the hail line. The other six are four trims
  and two verbatim, and none of them adds a word.
- **"We perform ADAS recalibration at our Southampton facility."** Read off
  the live auto glass page on 2026-09-13. It is not carried on any page here
  yet, and it matters beyond its own sentence: `pagemap.md` gates the ADAS
  calibration page on the owner confirming calibration happens in house, and
  **the shop's own live site already says it does.** That is evidence for the
  gate, not the owner's confirmation of it. Ask the question anyway.
- **"Your insurance claim handled for you."** The hero says it as a flat
  promise. Same scope question as 1.18 and 4.2.
- **"Your repair done right the first time and guaranteed for life."**
  The warranty again, in its strongest wording anywhere on the site.
- **"Family owned and operated."** Also in the Why Choose list on
  /collision-repair/.
- **"Factory training for a dozen vehicle brands."** The 12 again; see 4.1.
- **"Today's cars hide cameras and sensors in the bumpers, the mirrors, even
  the windshield glass."** A statement about cars rather than about the shop,
  but it sits next to the claim that this shop puts them back right.
- **"Collision work is most of what we do, but we also handle auto glass,
  paintless dent repair, and commercial fleets."** Four services, and the
  services grid names the same four. Confirm all four are in house.
- **Hours: Monday to Friday, 8 a.m. to 6 p.m., Saturday by appointment
  only.** In the contact block and in the schema's
  `openingHoursSpecification`. Confirm they are current.

### 4.2 Scope of work

Rule 2, scope honesty. For each of these the question is not "is it plausible"
but "do you actually do this":

- **ADAS recalibration on any repair that calls for it.** Broadened 2026-09-10
  from "after major repairs"; see 1.23. **This page no longer says "in our
  facility"** in that sentence, so it implies in-house rather than asserting
  it. `pagemap.md` gates the whole ADAS calibration page on the owner
  confirming calibration happens in-house, and the explicit claim the gate
  rests on is the **live glass page's**, which is unchanged. **Does the shop recalibrate, or check the need,
  on bumpers and mirrors as well as structural work?** If the answer is that it
  is sublet, or that minor jobs are checked rather than recalibrated, more than
  one sentence changes and the ADAS page is settled at the same time.
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

#### The service-page heroes are interim stock too, and each is a blocker

**Greg's ruling, 2026-09-24: the heroes of the three remaining service pages
are licensed stock, and each is a cutover blocker beside the three accents
above.** Licensed from Adobe Stock with the generative-AI filter excluded,
provenance read clean before anything was built on them, and **none of them is
this shop.**

| Page | Hero | Asset | Record |
|---|---|---|---|
| `/auto-glass-repair-replacement/` | `hero-windshield-replacement-in-shop.jpg` | AdobeStock_64691325 | 3.47 |
| `/paintless-dent-repair/` | `hero-dent-lifter-on-red-door.jpg` | AdobeStock_1571353580 | 3.48 |
| `/commercial-collision-repair/` | `hero-wrecked-work-van.jpg` | AdobeStock_430555209 | 3.49 |

**The shoot list gains one photograph per page**, each showing that service's
own work at this shop:

- **a real Tri-County glass job**, a windshield going in or a chip being
  repaired, in one of the bays (for 3.47);
- **a real Tri-County dent job**, a technician working a panel paintlessly,
  ideally with the before and after frames Real Repairs would need (for 3.48);
- **a fleet vehicle at the shop**, a work van or box truck in or outside a bay,
  ideally one of the shop's own commercial customers with their permission
  (for 3.49).

---

### 4.10 Claims the service pages add

Every claim below is migrated from the live page named, word for word, so none
is new. The question for each is the scope question, **"do you actually do
this?"**, not "is it plausible".

**`/auto-glass-repair-replacement/`** (3.47)

- **"We perform ADAS recalibration at our Southampton facility."** Now on a
  page in this build, not only on the live site. The same question as 4.2 and
  section 5 item 4, and the answer settles the ADAS page's gate.
- **"Skilled technicians experienced with all types of auto glass."** Is glass
  work done in house, or sublet? 4.1b asks it for the homepage's glass items;
  this page is where the answer matters most.
- **Windshield chip and crack repair, windshield replacement, and side and rear
  window replacement.** All three in house?
- **"We work directly with your insurance company"** on glass claims. Direct
  billing to the insurer, or help with the claim?
- **"Fast, efficient service without cutting corners."** A timeline claim with
  no number in it; the owner should be comfortable being held to it.
- **"Free estimates and free consultations."** Also in FAQ 6. The same
  question as 1.7: is a consultation something distinct from an estimate?
- **"Quality glass, materials, and tools on every vehicle."** OEM glass,
  aftermarket, or either? The page does not say, and a customer may ask.
- **The stat band's "Warranty on all repair work."** The live glass page never
  mentions the lifetime warranty. Does it cover glass work?
- **The hero chip "Detailed after every repair."** On a glass-only job too? 4.2
  asks it; it now applies here.

**`/paintless-dent-repair/`** (3.48)

- **"Skilled technicians experienced in paintless dent repair."** Is PDR done
  by the shop's own technicians, or by a PDR specialist who comes in? Many
  shops sublet it, and the page says "our technicians" throughout.
- **Hail damage**, which the page names as what PDR handles best. 4.1b asks
  whether hail is taken or sublet; this page is the one that sells it.
- **"PDR for cars, trucks, and SUVs"** and "works on most vehicles".
- **"PDR typically costs less than conventional dent repair"** and "one of
  the most cost-effective repairs you can get." Comparative cost claims.
- **"Qualifying dents can often be handled quickly."** A timeline claim with no
  number in it.
- **"Call (215) 322-5350 or stop by."** Does the shop take walk-ins for a dent
  look, given Saturday is by appointment only?
- **"Free estimates and free consultations"**, as on glass.
- **The stat band's lifetime warranty**, as on glass: never mentioned on the
  live dent page. Does it cover PDR?
- **"Detailed after every repair"** on a PDR-only job.

**`/commercial-collision-repair/`** (3.49). **The heaviest scope claims on the
site.**

- **Tractor-trailers and buses.** Named in the vehicle list, FAQ 1 and FAQ 4
  ("a company running dozens of tractor-trailers"), and in the intro ("a
  lineup of tractor-trailers"). **Can 995 Jaymor Rd physically take a
  tractor-trailer or a bus, and does the shop repair them itself?** If not,
  five sentences change. The Service schema already leaves both out until this
  is answered.
- **"No business is too small for us, and no fleet is too large."**
- **"Our certified technicians bring years of experience across the full range
  of working vehicles"** and "Certified technicians with years of commercial
  vehicle experience." Certified in what, for commercial work?
- **"We'll arrange to assess the damage."** Does the shop go to the vehicle, or
  does the vehicle come in?
- **"We deal with all the major insurance carriers and manage the claims
  process directly."** Commercial policies included? Direct billing?
- **Fleet accounts, billing terms and turnaround promises**: the live page
  makes **none**, and so this page makes none. Worth saying so to the owner,
  because a fleet manager will ask.
- **"Fast, efficient turnaround to limit downtime"**, "we work quickly to
  assess your vehicle and start repairs without unnecessary delays", and "Our
  team is available to answer questions and give you status updates."
- **"Top-quality parts and equipment on every job."** OEM, or not always?
- **"From contractors in Warminster to delivery services in Bensalem."** This
  reads as real customers. Are there?
- **"Lifetime warranty on repair work"** on commercial vehicles. The live page
  says it twice, so the stat band is supported here; the question is whether it
  holds for a vehicle that does commercial mileage.
- **"Free estimates in person or online."** The online half waits on
  `/contact-us/`.

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
6b. **RAM and Fiat: certified or not?** The live logo strip shows fourteen
   marks and the live prose says a dozen. This build ships the twelve the
   words claim. One answer moves the count everywhere, in one commit, and
   the build now fails if it moves in only some places. See 4.1 and 3.26.
7. **1974 and second generation**: publish them or not. See 4.5.
8. **priceRange**: publish `$$` or not. See section 2.
9. **The four customer quotes**: permission to republish, and whether the
   staff they name still work here. See 4.8.
10. **The verified `sameAs` list.** See 3.7.
11. **The eight damage types on the homepage, all in house?** And the two
    composed lines, the bumper one and the hail one. The deer strikes question
    is closed: the item was removed on 2026-09-17 rather than answered. See
    4.1b and 3.22.
12. **The customer-vehicle photograph practice.** Does the shop have
    permission to publish photographs of customers' vehicles, and what is its
    practice for asking? The Real Repairs band publishes ten frames of five
    identifiable vehicles. Plates and stickers are destroyed and no person,
    name or date appears, but a customer's car outside a body shop is still
    their car. See 3.23.
13. **The glass page's scope** (4.10): glass in house or sublet, direct
    insurance billing on glass claims, OEM or aftermarket glass, and whether
    the lifetime warranty and the detailing promise reach glass-only jobs.
14. **The glass page's closing promise**, Greg's to rule on before the owner
    sees it: "We will get you back on the road with quality glass, installed
    with the same care we bring to every repair." See 3.47.
15. **The dent page's scope** (4.10): PDR in house or sublet, hail taken or
    sublet, walk-ins, and whether the warranty and the detailing promise
    reach PDR-only jobs.
16. **The dent page's closing promise**, Greg's first: "We will get you back on
    the road with the panel looking like nothing ever happened." See 3.48.
17. **The commercial page's scope** (4.10): tractor-trailers and buses above
    all, then on-site assessment, commercial insurance handling, the
    turnaround language, and whether the named customer types are real.
