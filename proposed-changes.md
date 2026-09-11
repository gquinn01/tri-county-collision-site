# Proposed changes, awaiting the owner's fact-check

Every text change made during the migration, as before/after pairs, plus every
claim the migrated pages carry. Nothing in here is settled. The standards make
the **client-owner the fact-checker of record**, and this file is how that role
gets exercised: read it, say yes or no to each line, and anything that gets a
no comes off the page.

**Status: 2 pages migrated.** `/collision-repair/`, built 2026-09-05, and `/`,
built 2026-09-10 from `https://tricountycollision.com/` read the same day.

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

### 4.1b Claims the homepage adds

- **"We fix it all", and the five damage types under it**: minor and major
  collisions, cracked windshields, door dings and dents, deer strikes, hail
  damage. Rule 2, scope honesty: **does the shop do all five, in house?**
  Hail and deer strikes in particular are the kind of work a shop either
  takes or sublets.
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
