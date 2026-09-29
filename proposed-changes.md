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

**Scope clarified by Greg, 2026-09-24 (3.54): the no-third-drawing ruling does
not reach cartography.** Its subject was illustrative artwork, a decorative
drawing for this band after two AI assets were rejected, and it ended when the
client picked a licensed render over a third attempt at art. A map is not
that. It is a diagram of verifiable fact, rendered from licensed survey data,
and every line in it can be checked against the world. The same reasoning
lets this repo draw its own coordinate grids and probe overlays. So
`/contact-us/`'s road map, drawn by `scripts/prepare-map-image.py` from
OpenStreetMap data, is outside this ruling. **The drawn intake diagram is
still dead, and so is any illustration made by us.**

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

### 3.51 Greg rules on four open items: two promises, a chip, a strip. BUILT 2026-09-24

Greg ruled on the four open items from 3.47 to 3.49. **All four are applied in
one commit.** The two promise sentences and the chip label are **Greg-approved
wording, not migrations**, and are recorded as approved pairs.

#### 1 and 2. The glass and dent closing bands ship

| Page | Before | After, approved |
|---|---|---|
| `/auto-glass-repair-replacement/` | (band held, pending) | We will get you back on the road with quality glass, installed with the same care we bring to every repair. |
| `/paintless-dent-repair/` | (band held, pending) | We will get you back on the road with the panel looking like nothing ever happened. |

**The grammar is home's `#start` exactly**: the promise as the headline, the sub
line "Estimates are free and there is no obligation" byte for byte, and the same
CTA pair. The NOT-SHIPPED comments came out; the reasoning is in 3.47 and 3.48
and the approval is here. **Each sentence ships byte-identical everywhere it
appears, which today is one page each.**

**The ground is ox on both, the recorded service-page default, and each page's
own sequence agrees rather than argues ink.** On both pages `#why` was the only
oxblood band, `#area` sits between it and the new band on panel, and FAQ follows
on silver. That is exactly the tail `/collision-repair/` and
`/commercial-collision-repair/` carry. Ink would have been the answer only if
the page's two oxblood bands were already spent, which is why the collision
page's band is ink, and neither page's were.

#### 3. The commercial chip swap, both lists, this page only

| | |
|---|---|
| **Before** | Detailed after every repair |
| **After, approved** | Built to limit downtime |

**The mark is the road glyph the site already owns**: the lane from
`/collision-repair/`'s safety card, already on this page as step 06, "Back to
work". A vehicle back on the road is what limited downtime means, and no other
glyph the site owns says it. Nothing was drawn. **Both chip lists changed
together**, as 3.36 requires, the whole `<li>` swapped, mark and label. **The
other four pages are untouched**: glass, dent and collision still carry
"Detailed after every repair" in both lists, and home carries no chips.

#### 4. The brand strip joins commercial

**The seat is `#fleet`, between its sec-head and its prose**, the section where
the page makes its 12-brand argument. That is the same seat the strip holds on
the collision page, and **the seat was chosen so that collision's padding
derivation holds unchanged**: the head supplies `--sec-gap` above, the strip
supplies `--sec-gap` below, and the paragraph after it has no top margin. So
the selector was extended, not written:

```
BEFORE  #factory-certified #brands { padding-top: 0; padding-bottom: var(--sec-gap); }
AFTER   #factory-certified #brands, #fleet #brands { padding-top: 0; padding-bottom: var(--sec-gap); }
```

**That line is the whole `site.css` diff.** `stamp-assets.py` restamped every
page and the template from `?v=2983cc72` to `?v=95d0714b`, and on home, the
collision page and the template the stamp is the only line that moved.

**The seat under the argument paragraph was considered and rejected**, because
its neighbours differ. Above it sits a paragraph's 1.1em bottom margin, and
below it the section's own padding, so it would need its own rule. This commit
permitted one selector-list change and no new rule.

**The strip needed a light ground.** The marks are black alpha masks at
`--brand-ink`, and `#fleet` was ink, where they would be black on near-black.
Three ground classes moved, on this page only, so the page still alternates:

```
            BEFORE   AFTER
#intro      panel    silver
#fleet      ink      panel      the strip's section
#downtime   panel    ink        prose on ink, which is what ink carries
```

**The markup is collision's, lifted rather than retyped**, and compares
byte-identical to it, so every limit travels verbatim. **The brand check is
green: three strips site-wide**, home's standalone band, collision's and this
one, with **12 mentions in visible text and 1 in JSON-LD, all saying 12.** (The
ruling said two strips; home carries the third, and always has.) The Real
Repairs withheld note on this page was corrected to say the strip is no longer
withheld.

#### Measured

**The fold is identical to HEAD, proved by hash**, twelve runs, viewport-sized
iframe. Each hash covers `innerHeight`, laid-out width, computed `min-height`,
and the hero, CTA and stat-band boxes. HEAD was probed with this commit's
changes stashed:

```
glass       390x664 banner 80d7a4b1  cutover 4efed6c7   360x640 banner 4ef0b61d  cutover 68ca333d
dent        390x664 banner 5d6e5c37  cutover ec543417   360x640 banner a1f4ee8d  cutover af47ec0b
commercial  390x664 banner 5d6e5c37  cutover ec543417   360x640 banner 4ef0b61d  cutover 68ca333d
```

Expected, since a closing band and a strip change page length rather than the
hero, and the chip swap is a same-width label inside the same two-row cap.

**The strip's seat matches collision's to the pixel:**

```
                    head -> marks   marks -> prose   brand padding
collision  1440          40               40             0 / 40
collision   390          40               40             0 / 40
commercial 1440          40               40             0 / 40
commercial  390          40               40             0 / 40
```

**The marks read at 9.44:1 on the panel**: the darkest composited pixel is
rgb(70,70,70) against white, which beats the 8.70 recorded over silver in the
strip's own note.

**Seams and heads**, iframe taller than the page, maps agreeing at two heights,
laid-out width true: seams 176-178 at 1440 and 96-98 at 390 on all three pages.
Head-to-body is 40, and 44 on each new `#start`, exactly as the collision and
commercial pages' `#start` measure. **The 3.46 baseline holds.**

**The ask rhythm gains a fifth ask on glass and dent**, the band, and the tail to
the footer shortens:

```
                     longest run at 390    tail at 390
glass                      1658              890   (was 1309)
dent                       1634              772   (was 1190)
commercial                 2684              890   (was 2509: the strip adds 172)
```

**Rendered and checked by eye at 1440 and 390**: both bands and the strip's
seat, and the swapped chip at 1440. The strip was rendered at rest, the probe
forcing reduced motion, which is its base state: two rows at 1440 and three at
390, all twelve visible.

#### Found, not fixed

**The comment above the extended selector in `site.css` still says only a
`#brands` inside `#factory-certified` is trimmed.** It is now one context of
two. It was left alone because this commit's CSS change had to be the selector
list and nothing else; it wants one sentence in the next CSS commit.

### 3.52 One white band under the hero, and the intros centre. BUILT 2026-09-24

Greg reviewed the three new pages. **Commercial reads right; glass and dent did
not, for two named reasons**, and both are fixed here, on those two pages only.

#### 1. The stat band is the one white band under the hero

**The fault, measured rather than described.** On both pages `#intro` sat on
`band-panel`, and `--panel` is `#FFFFFF`, so the white stat band landed on a
white section: two white grounds back to back. Commercial's 3.51 shape is the
reference, with `#intro` on silver and the page alternating from there.

**The rules:** no two adjacent sections share a ground; every card sits on a
ground its edges read on; the oxblood act bands do not move.

**Ground sequences, read off the rendered pages** as each section's computed
background (silver where a section has none and shows the body):

```
GLASS  BEFORE  stat(white) > intro(WHITE) > repair-or-replace(silver) > adas(ink)
               > insurance(silver) > why(ox) > area(white) > start(ox) > faq(silver)
               adjacent same-ground pairs: stat + intro
GLASS  AFTER   stat(white) > intro(silver) > repair-or-replace(INK) > adas(WHITE)
               > insurance(silver) > why(ox) > area(white) > start(ox) > faq(silver)
               adjacent same-ground pairs: none

DENT   BEFORE  stat(white) > intro(WHITE) > how-it-works(ink) > what-pdr-can-fix(silver)
               > when-not(white) > why-pdr(silver) > assessment(white) > why(ox)
               > area(white) > start(ox) > faq(silver)
               adjacent same-ground pairs: stat + intro
DENT   AFTER   stat(white) > intro(silver) > how-it-works(ink) > ... unchanged
               adjacent same-ground pairs: none
```

**Dent is one class change.** `#intro` leaves `band-panel` and shows the silver
body, and `#how-it-works` below it is already ink.

**Glass is the page with the decision in it.** `#intro` on silver would sit
beside `#repair-or-replace`, which is also silver and carries the three white
cards. Moving the cards to panel would lose them (a white card on a white
ground), and leaving them on silver would break the adjacency rule. **So the
cards go to ink**, and that is safe by cascade rather than by hope:

- `.dark .card` gives a card a translucent silver fill and a silver hairline,
  and `.dark .card p` sets its text in `--silver`.
- `.card h3` carries no colour of its own, so the heading inherits `--silver`
  from `.dark`. Checked by grep that no rule pins an `h3` colour on this path,
  then read off the render: **h3 and p both compute to rgb(240,242,242).**
- These are `.grid3` cards, not `.payoff`, so the trap recorded in 3.48, where
  `.payoff .card p` sets `--ink-2` after `.dark .card p`, does not apply.
- `.dark .card::after` already gives the lift's sweep its silver.

**`#adas` gives its ink to the cards and takes the panel**, so ink does not sit
beside ink. It is prose, and prose reads on any ground.

**The card edges read better than before, measured on rendered pixels** at the
first card's left edge:

```
                     edge vs ground   edge vs fill   fill vs ground
BEFORE, on silver         1.46            1.64            1.12
AFTER, on ink             2.81            2.32            1.21
```

The ox bands are exactly where they were on both pages: `#why` and `#start`.

#### 2. The intro text centres

**Mechanism: home's own inline pattern**, `text-align:center` on the intro's
`.prose` block. Home carries it as `style="margin-top:34px;text-align:center"`;
these intros take the centring half, since they need no extra margin. The same
inline centring already sits on the collision page's `#process` lead and on
glass's and commercial's section leads.

**A shared rule was considered and not chosen.** The pattern now repeats, but
every instance is one attribute on one element, and a shared rule would be the
first CSS in a commit that can otherwise stay CSS-free. That is a reasonable
next step, not a necessary one. **So this commit is CSS-free, and the pending
sentence for the comment above `#factory-certified #brands, #fleet #brands`
(3.51) stays pending for the next CSS commit.**

**Commercial's intro is untouched**, by the ruling's scope. Matching it is one
attribute if Greg extends the ruling.

#### Measured

**The fold is identical to HEAD, proved by hash**, eight runs, viewport-sized
iframe, HEAD probed with this commit stashed. The hashes are the same ones 3.51
recorded, because nothing above the stat band moved:

```
glass  390x664 banner 80d7a4b1  cutover 4efed6c7   360x640 banner 4ef0b61d  cutover 68ca333d
dent   390x664 banner 5d6e5c37  cutover ec543417   360x640 banner a1f4ee8d  cutover af47ec0b
```

**Seams hold the 3.46 baseline**: iframe taller than the page, maps agreeing at
two heights, laid-out width true. Seams are 176-177 at 1440 and 96-97 at 390,
head-to-body 40, and 44 on `#start`. **Rendered and checked by eye** from the
hero through the first two sections at 1440 and 390 on both pages.

**The diff is class and style attributes plus comments**: four attribute changes
on glass (`#intro`, the intro prose, `#repair-or-replace`, `#adas`) and two on
dent (`#intro`, the intro prose). Every other page regenerates byte-identical.


### 3.53 Contact joins the site, with no form on it. BUILT 2026-09-24

`/contact-us/`, built from the shop's live page at
`https://tricountycollision.com/contact-us/`, **read on 2026-09-24.** Slug kept.
Greg's rulings of 2026-09-24 govern it, and each one is here in his words or in
what it decided:

- **No form on this site.** The recorded form-endpoint question is answered:
  there is no endpoint, because there is no form.
- **The CarWise estimate and appointment links stay**, pending the owner's
  confirmation that CarWise is still in use.
- **The page top is a compact header with the actions first**, not a photo
  hero. The page's whole job, in Greg's words: "the options the live page
  provides, very easy to find and very easy to execute."

#### 1. The map changed first

`pagemap.md` was amended before any page was written, struck rather than
deleted where it had said something else:

- **Contact row.** "Form on an endpoint the client owns. This page is now the
  only intake form on the site" is struck. It now records the ruling: no form;
  call, email, the shop's CarWise estimate and appointment links (owner to
  confirm), and directions. It is still the destination of the
  `/customer-information/` 301, which stays genuinely equivalent, because it
  is where a customer reaches the shop.
- **Thank-you row: out of the map**, struck with the reason. It existed as the
  form's success target and there is no form.
- **Customer-information row.** "We build our own form, on an endpoint the
  client owns" was a stale instruction and is struck hardest, per the
  correction rule.
- **Privacy row.** Its reason, "the forms need it", is struck and replaced
  with the reason that still holds: GA4 and the CallRail snippet need it. The
  page itself is not in question.
- **Counts, the third time these numbers have moved**, with the arithmetic
  spelled out: utility pages 1 - 1 = 0; indexable pages unchanged at 37 (38
  with ADAS); redirects unchanged at 11.

**One fact the brief did not have: `/thanks/` is live, and it is in the live
sitemap.** So taking its row out also decides what its URL does. The old
sitemap was counted off the live index on 2026-09-24 and it is 48 entries.
They reconcile as 36 migrated + 11 redirected + `/thanks/` = 48. **`/thanks/`
gets an honest 404 at cutover**: it is plumbing, and a thank-you page has no
genuinely equivalent destination, so a 301 to Contact would be a forced
mapping. That is inside the ruling (redirects unchanged at eleven), but it is
recorded here so nobody is surprised by it at cutover.

#### 2. What migrated, as pairs

Everything on the page is the live page's words except the card labels, which
are this site's existing labels ("Email the shop" is the label every CTA row
carries).

**Head**

- Title. BEFORE: `Contact Us | Tri County Collision – Southampton, PA`.
  AFTER: `Contact Us | Tri-County Collision, Southampton, PA`. Why: the
  business name is the NAP's, with the hyphen, and the en dash becomes a
  comma. 50 characters, machine-counted.
- Meta description. BEFORE: none; the live page has none, which is what the
  map said to fix. AFTER: `Call Tri-County Collision in Southampton, PA at
  (215) 322-5350, email the shop, get a free online estimate, book an
  appointment or get directions.` 146 characters, machine-counted. It carries
  no street address, because the address check wants the full line wherever
  the street appears and a description is not the place for it.
- **The title, the description and the page node mirror each other byte for
  byte, decoded, and hashing proves it.** Title `a6882bc045ca`, three times;
  description `08fc7b436479`, three times.

**The header**

- H1 `Contact Us`, unchanged.
- Eyebrow `Southampton, PA`: added. It is the site's own eyebrow, the one
  every service hero carries, not new wording.
- Lead. `If you're standing next to a damaged car right now, just call. That's
  the fastest way to get help.` **Unchanged, and it leads the page**, as Greg
  directed: protected voice.
- Hours. BEFORE, under the live "Address & Hours" heading: `Hours: Monday -
  Friday 8 AM - 6 PM` / `Saturday By Appointment Only`. AFTER, beside the call
  button: `Monday to Friday, 8 a.m. to 6 p.m.` / `Saturday by appointment
  only`, **the footer's two lines, byte for byte.** More below on why they carry
  no label.

**The options**

- H2 `Let's Get You Back on the Road Safely`, unchanged. It moves from above
  the live intro to above the cards.
- BEFORE: `Otherwise, pick whichever option below fits your situation.` AFTER:
  `If you're not calling, pick whichever option below fits your situation.`
  Why: T5. The sentence now sits under its own heading, a section below the
  "just call" it answered, so "Otherwise" had lost what it referred to. The
  next sentence, `Either way, you'll get a straight answer and know exactly
  what happens next.`, is unchanged.
- Call. BEFORE: heading `Need to Talk Now?`, then `For immediate answers or to
  discuss your repair directly with our local team: Call Us: (215) 515-4662
  (Lines open Mon-Fri, 8 a.m. - 6 p.m.) - A real person answers, no phone
  tree.` AFTER: heading `Call (215) 322-5350`, then `For immediate answers or to
  discuss your repair directly with our local team.` Why: the number is the
  NAP's, and the 515 number does not ship (section 3). The hours moved up
  beside the header's button. **"A real person answers, no phone tree" is
  HELD**, because it was written about the 515 line. Attaching it to 322-5350
  would be fabrication by fusion: a true sentence about one line, made into a
  claim about another. It goes to the owner.
- Email. BEFORE: heading `Prefer to Email Us?`, then `For non-urgent questions
  or to send photos of damage: Email Our Team: contact@tricountycollision.com
  - We reply the same business day.` AFTER: heading `Email the shop`, then `For
  non-urgent questions or to send photos of damage.` with the address on its
  own line. **"We reply the same business day" is HELD** for the owner. It is
  a service-level promise, and a customer will hold the shop to it.
- Estimate. BEFORE: heading `Start with a Free Online Estimate`, then `Get a
  quick, no-obligation idea of repair costs by submitting your vehicle's
  details online. Get Your Free Online Estimate Here - Takes about five minutes
  with photos of the damage.` AFTER: heading `Free online estimate`, then the
  first sentence alone. Why: Greg asked for one line per CarWise card, so a
  reader can tell the two apart before tapping. The link text is gone because
  the whole card is the link. **"Takes about five minutes" is HELD**: it is a
  timing claim about a third party's tool.
- Appointment. BEFORE: heading `Book Your In-Shop Appointment Online`, then
  `Schedule a convenient time for a thorough, in-person assessment at our
  Southampton facility. Book Your Appointment Now - Pick your time online, and
  you're booked, with a confirmation to your inbox.` AFTER: heading `Book an
  appointment`, then the first sentence alone. Same reason. **The
  confirmation-email line is HELD**, since it describes CarWise's behaviour.
- Directions. BEFORE: `Address: 995 Jaymor Rd Southampton, PA 18966`, with
  **the comma missing**. That is a NAP variant, and the audit would fail it.
  AFTER: a `Get directions` card carrying `995 Jaymor Rd` / `Southampton, PA
  18966`. It links to the maps URL the footers already use.

**The CarWise hrefs are the live page's own, verbatim.** The live page carries
each link in three shapes. The body-copy links, which are the ones that
shipped, are parameter-free:

```
https://www.carwise.com/online-photo-estimate/tri-county-collision-center-southampton-pa-18966/481195
https://www.carwise.com/auto-body-shops/book-appointment/tri-county-collision-center-southampton-pa-18966/481195
```

The header and footer buttons append plugin parameters to the same paths. One
of the appointment links carries `clientId=1924865829.1668790684`, which is **a
single visitor's Google Analytics client id**, frozen into the markup. That is
session-specific, and none of those shapes were carried. Both links open in a
new tab with `rel="noopener"`, the site's convention for the maps link. **They
could not be proven live from a terminal.** CarWise answers every automated
fetch, its own homepage included, with a Cloudflare challenge
(`cf-mitigated: challenge`, HTTP 403). That is bot protection, not a dead
link, and it is why the owner's confirmation matters.

#### 3. What did not migrate, and why

Each of these was already ruled:

- **(215) 709-9665**, the CallRail tracking number, printed on the live page as
  a heading. The audit would score it as a critical.
- **(215) 515-4662**, **a third number, new to the record**, printed as the
  live page's "Call Us" line. It is unconfirmed, it ships nowhere, and it
  joins the owner questions.
- **`info@tricountycollision.com`**, the banned second address, three times in
  the live page's closing contact block.
- **"1,500+ five-star reviews"** and the Trustindex widget's **"Based on 231
  reviews"**, together with its eight reviews. Both contradict the counted
  figure in `REVIEW_COUNT`, and they disagree with each other as well. The
  lifetime-warranty half of the same line is not contradicted. It stays off
  because this page executes rather than persuades, and every page in front of
  it carries the warranty in its stat band.
- **The Google Maps embed** becomes a Get Directions link. Nothing on this site
  makes a third-party request at runtime, and a link that opens the reader's
  own navigation app is easier to use anyway.
- **The form**: first, last, email, phone, a service select and a message. Not
  migrated, because there is no form. It went with its "Contact Us for Your
  Free Consultation" block and that block's duplicate address and hours.
- The CarWise header and footer plugin buttons and the live page's "Call to
  Speak with an Expert" button, for the reasons above.

#### 4. The page

**No new CSS.** Every piece already existed:

- `.hero` and `.lead` outside a hero: the two base rules restored on
  2026-09-13 for exactly this.
- `.band-panel` as the header's ground.
- `a.svc-card`, the home router's whole-card link, so the lift comes with it.
- `.grid2` for the five cards.

`stamp-assets.py --check` exits 0.

**The ground is white, not oxblood, argued:**

- **Oxblood means act, and here it goes on the act itself.** On a light
  ground the call button is filled oxblood, the strongest act signal the site
  has. On an ox band it turns ink, by the act-button rule, so the colour would
  sit behind the act instead of on it.
- **The system lacks the rules an ox header would need.** `.crumb ol` is
  `--ink-2`, and the only dark-ground breadcrumb rules are scoped to `.heroB`.
  `.lead` is `--ink-2` with no `.dark` variant. On ox, both print dark on dark.
  So ox needs two new rules, and Greg's instruction was to stop and say so
  rather than write them. **If Greg wants ox, those two rules are the whole
  cost**, and the palette law permits it, because this band asks.
- Silver was ruled out as well. The cards sit on silver below the header, and
  3.52's rule is that no two adjacent sections share a ground.

**Two structural choices, both commented in the page:**

- **The header's content sits in a plain `<div>`.** A `.cta-row` that closes a
  section's `.wrap` is a section-bottom ask, and those centre. This one belongs
  to the left-aligned copy above it. It is excluded by structure, the way the
  hero is.
- ~~**The hours sit inside the call row with no "Hours" label.** They sit beside
  the button where there is room and under it where there is not. With the
  label, the block was three lines. At 1440 the flex row stretched the button
  to 84px to match it, and at 360x640 the hours cleared the fixed call bar by
  **1px**. Without the label, the button is its own 62px, and the fold numbers
  are below.~~ **SUPERSEDED 2026-09-24 by Greg's ruling, 3.55: the hours left
  the header. Do not restore them there, or the requirement below, from this
  paragraph.**

**The page node is a `ContactPage`**, which is what the page is. The builder
matched `WebPage` by exact type and would have left this page without a
`lastmod`, so `scripts/build-sitemap.py` now reads a `PAGE_NODE_TYPES` tuple
instead. The graph is the full `AutoBodyShop` node, copied byte for byte from
`/paintless-dent-repair/` under the shared `@id`, then `ContactPage`, then
`BreadcrumbList`. **There is no `primaryImageOfPage`**, because no image is on
the page. **og:image follows home's**, four lines byte for byte, with a comment
saying so. It moves to a real shop photograph after the shoot. The CarWise
links are not in the schema, because they are a third party's pages.

**Hours, from where they actually live.** The brief said to take hours from
`audit.py`'s constants. **`audit.py` has no hours constant.** The hours live in
each page's `openingHoursSpecification` and in the footer, as two lines of text
that are byte-identical on all six pages. This page takes the footer's lines.
They could drift one day, and a check that holds them together would be
mechanism over memory. Not written here; it is proposed below.

#### 5. The execution-page ruling, and the rubric

**Greg's ruling, 2026-09-24, option 1, in his reasoning:** the thin-content
check and the FAQPage check "measure a page whose job is persuading and
answering, by word count and by FAQ presence. This page's job is executing,
and its success measure is different: every option within reach, the call
inside the first screen, which the fold probe already proves. A check that
forces 300 words of filler or an invented FAQ onto an execution page would be
the check designing the page, and the check serves the page, never the
reverse."

Option 2, shipping below the bar with a note, was rejected: "a permanent
sub-bar score turns the Monday report into something the reader learns to skim
past, and the monitoring product's value is that its warnings mean something."

**Built to his four conditions:**

1. **Exactly two checks, for exactly the declared kind.** The page declares
   `<meta name="tri-county-page" content="contact">` in its own head, with a
   comment. `RUBRIC_EXEMPTIONS = {"contact": ("faq-schema",
   "thin-content")}` in `audit.py`. Every other check runs, and the page still
   counts as a page in the report's headline. An exempt check reports as a
   **note** naming the ruling, so the report says what it did not measure.
2. **Both directions tested**, `test-audit-checks.py` section 19, 16 checks.
   A contact page still fails the CallRail number, the second email, a wrong
   street spelling and a missing H1, and still warns on a bare contact. An
   undeclared page, a misspelled kind (`contct`) and `utility` get no
   exemption. The shipped page has no critical and sameAs as its only
   warning. **The test was itself tested by mutation.** Adding a blanket
   `utility` kind turns 2 checks red. Emptying the contact kind turns 5 red.
   Adding a third exemption turns 1 red.
3. **Recorded with the principle**: here, and in CLAUDE.md under "Execution
   pages measure differently".
4. **Per kind, explicit, forever.** The privacy page declares its own kind
   with its own recorded scope when it lands. The test fails if any kind but
   `contact` exists today.

**The page scores 94, not 95, and it is exactly as clean.** The score is the
share of checks passed, and that formula is unchanged on purpose. A service
page runs 19 checks and passes 18, which is 94.7 and rounds to 95. This page
runs 16, because the two exempt checks are notes and there is no FAQ to
mirror. It passes 15: 93.75, which rounds to 94. **Its only warning is sameAs,
the same one every page carries, and it reaches 100 on the same day they do.**
Rounding it up by counting an exempt check as a pass would report a check as
passing that never ran, so that was not done. If Greg wants the table to read
95 for this page, that is a change to the formula, and it is his to rule on.

#### 6. The landing forces

**13 elements became links, on five pages.** The brief's "15 spans" was the
whole pending inventory. 13 of them pointed at `contact-us/` and the other 2
wait on unbuilt pages (`areas-served/` from home,
`your-right-to-choose-a-body-shop/` from collision), and those 2 are untouched.

```
docs/index.html                                2   FAQ, footer
docs/collision-repair/index.html               5   process card, minor repair, insurance, FAQ, footer
docs/auto-glass-repair-replacement/index.html  2   FAQ, footer
docs/paintless-dent-repair/index.html          1   footer
docs/commercial-collision-repair/index.html    3   process card, FAQ, footer
templates/service-page-template.html           1   footer, so a page built from it is born linked
```

**The footer's "Send us your details online" keeps its label**, as ruled:
with CarWise kept, sending your details online is exactly what the page
offers. On this page it links to `./`, the way every page's footer links to
itself. The footer item's odd 22-space indentation, left over from the span
era, was restored to the list's own on the same line.

**3.2 and 3.10 are resolved** by this landing, not by rewriting. The "request
an estimate online" sentences they worried about now link to a page that
offers exactly that, through the shop's own CarWise estimate. They are true
for as long as CarWise is in use, which is the owner question.

**Following 3.47 to 3.50, no page's `dateModified` moved.** Link conversions and
footer edits have not moved it before. `docs/llms.txt` gains the page, naming
CarWise as a third-party service. `docs/sitemap.xml` was regenerated and now
has 6 URLs, with `lastmod` 2026-09-24 from the page's own `dateModified`.

#### Measured

**The fold, with an iframe the size of the viewport**, positions in CSS px from
the top of the first screen:

```
             innerHeight  call button  hours      call bar top  clears it by
390x664          664       419-481     495-551        604            53
360x640          640       419-481     495-551        580            29
1440x900         900       463-525     463-525        none          375
```

The call button and ~~both hours lines are~~ is inside the first screen at both
phone sizes and above the fixed call bar. **The hours-in-the-first-screen
requirement is SUPERSEDED, 3.55: the hours left the header by Greg's ruling.** Before the label came off, the 360x640
margin was 1px. Laid-out width is true at every size (`scrollWidth` equals
the viewport).

**Seams hold the 3.46 baseline**, with the iframe taller than the page: 177 at
1440 and 97 at 390 from the header's last line to the options heading, and
head-to-body 40 at both. **Rendered and checked by eye** at 1440 full page, at
390 full page, and at 360x640 as the first screen.

**A probe trap, recorded because it will recur.** Headless Chrome will not
make a window narrower than about 500px, so a direct screenshot at 360 lays
the page out wider and crops it, which looks like overflow. It is not.
Phone renders go through the viewport-sized iframe, which is why the method
exists.

**The suite.** Both test scripts pass. `stamp-assets.py --check` and
`build-sitemap.py --check` exit 0. `STAGING=1 audit.py --strict` finds **zero
criticals and six warnings, one per page, all sameAs**, and exits 1 on the
sameAs bar as every run has. `/contact-us/` carries none of 709-9665,
515-4662, `info@`, "1,500" or "231", checked by grep as well as by the audit.

#### Found while building, not changed

- **The form machinery outlives the form.** `templates/service-page-template.html`
  still carries a `<form>` with `{{FORM_ENDPOINT}}` and `{{FORM_SUBMIT_LABEL}}`,
  and `docs/assets/site.js` still has its `form_submit` event code. Neither is
  reached by any page. Removing them is a sweep of its own, and it touches
  `site.js` and its stamp. `build-sitemap.py`'s docstring was corrected here,
  because it named the thank-you page as the utility page this repo expects.
- **CarWise lists the shop as "Tri-County Collision Center"**, going by its
  own URL slug. That is a business-name variant on a directory this site now
  links to, and it joins 1.1's name question.
- **The header's call button and the first card are both a call**, one above
  the other on a phone, which is the arrangement the brief asked for. Worth
  Greg's eye on the render. If one of the two goes, the card is the one that
  should, because the button is what the fold probe proves.
- **An hours check.** The hours text appears in six footers and now in this
  header, with nothing holding them together. The shape would be the
  review-count check's: one constant, every mention compared.


### 3.54 The contact header goes ox, and the page learns where the shop is. BUILT 2026-09-24

**Record number: 3.54.** The blog run has not landed, so this is the next
number after 3.53.

Greg's rulings of 2026-09-24:

- **The compact header goes ox.**
- **The page gains a details-and-directions section**, after a reference
  layout he supplied: the details and hours on the left, a map on the right.
- **The CSS commit pays its debts**: the 3.51 comment sentence, and the hours
  constant 3.53 proposed.
- **After this sitting stopped on it: the map is drawn from OpenStreetMap
  data, not stitched from tiles.** The no-third-drawing ruling does not reach
  cartography.

#### 1. The header goes ox

`#contact` changes from `band-panel` to `dark field-ox`, reversing 3.53's
white. Some of it came free. The act button turns ink with the silver
hairline, by the symmetric rule. The crumb's link is silver through `.dark a`.
The eyebrow is silver through `.dark .eyebrow`. The H1 and the hours inherit
silver from `.dark`. **Three rules were written, and each one is commented
with what it serves:**

- **`.heroB--ox .lead, .field-ox .lead { color: var(--silver); }`**, and
- **`.heroB--ox .crumb ol, .field-ox .crumb ol { color: var(--silver); }`**.
  These are the two 3.53 scoped. They are derived, not retyped: the ox hero's
  own declarations, with `.field-ox` added to the selector list, so there is
  one line and one value, not a second copy of it.
- **`.hero.dark .cta-row { justify-content: flex-start; margin-top: 26px; }`**,
  which 3.53 did not foresee. `.dark .cta-row` centres every button row on a
  dark ground and gives it a 44px top margin. That is right for an act band,
  and wrong for a header whose call row belongs to the left-aligned copy above
  it. It would also have spent 18px of a phone's fold. It restores the base
  row. **Its reach was checked by grep**: `.hero.dark` exists on exactly one
  element, this header, because `.hero` is otherwise worn only by `.heroB`, and
  `.heroB` is never `.dark`.

**Every text tone on the band, measured scrim-style.** The method: render;
render again with the header's copy set transparent; take each element's
glyph runs by `Range.getClientRects()`; sample every pixel under them against
the element's computed colour. Worst case under any glyph:

```
                  1440    390    360   needs
crumb link       12.52  12.59  12.52     7
crumb current    12.16  11.43  11.22     7
eyebrow          12.08  11.15  11.01     7
H1               10.93  10.50  10.50   4.5
lead             10.50  10.50  10.50     7
hours            10.50  10.50  10.50     7
button label     15.42  15.42  15.42     7   (silver on the ink fill)
crumb separator   8.34   7.84   7.69     3   (--rule, a graphic)
```

**The probe calibrates itself.** Its floor, 10.50, is exactly the stylesheet's
recorded `--silver` on `--ox`, the gradient's brightest stop. The button
label's 15.42 is the recorded silver on ink. **The hours take `--silver`**,
the measured light tone, at 10.50 against a 7 target. The separator stays on
the base `--rule`, which clears the 3:1 graphic floor by more than double, so
it needed no rule.

**The fold did not move**, probed with an iframe the size of the viewport:

```
             innerHeight  call button  hours      call bar top  clears it by
390x664          664       418-480     494-550        604        54 (53 in 3.53)
360x640          640       418-480     494-550        580        30 (29 in 3.53)
```

The one pixel gained is the white band's top hairline, which went with the
white.

#### 2. Details and directions, `#find-us`

On white (`band-panel`), because the cards above sit on silver and the footer
below is ink. Two columns in the existing `.split`: one column on a phone,
two equal columns from 900px.

**The left column.** Eyebrow `Details and directions`, H2 `Find the Shop`.
BEFORE: none; both are new wording, Greg's name for the section and a plain
heading. Then three tappable lines: the address (to the directions URL), the
phone and the email, all the NAP block's values and all checked by the audit.
Then the **hours box**: `Monday to Friday, 8 a.m. to 6 p.m.` / `Saturday by
appointment only`, under an h3 `Hours`.

**Only what the record knows.**

- **Sunday is not written.** The gate was the live site's own schema, and it
  lists Monday to Friday plus "Saturday Hours: By appointment only" and never
  mentions Sunday. **But the Google Business Profile does**, and it
  disagrees with more than Sunday. See section 5.
- The reference's cancellation-fee and no-children lines were that business's,
  and nothing like them ships.
- There is no parking or arrival note, because nothing true is known to say.
  It is offered to the owner.

**New CSS, the minimum**, each rule commented with what it serves:
`.contact-lines`, `.hours-box` (plus a margin for its label, which is
`.sec-sub` on an h3 and so needed no type rule), `.map-box`, `.map-credit`,
and the map's own drawing classes. **The drawing classes are why the map is
inline**: each mark is a class that `site.css` paints from the palette
tokens, so no colour is typed outside the one file that defines the palette.
The only oxblood on the map is the pin.

#### 3. The map

**The brief said to stitch tiles from tile.openstreetmap.org. That was stopped
before a single tile was fetched**, and Greg agreed: "the tile policy's own
text prohibits it, and stopping was correct." Two policies were read on
2026-09-24:

- **The OSMF Tile Usage Policy, section 4**, prohibits "any pre-emptive
  fetching of tiles other than those a user is actively viewing" and "offline
  use". A static image built from tiles at build time is both.
- **The OSMF API Usage Policy** rules out the editing API the same way: "The
  editing API is provided in order to edit the map data, not for read-only
  purposes or projects."

**So the map is drawn, from data**, by the new `scripts/prepare-map-image.py`:

- **ONE Overpass API query**, within that service's fair use: the roads in a
  bbox around the shop, plus the building footprints within 120m. The
  footprints are used only to verify the pin and are never drawn.
- **Nominatim was queried once**, within its one-request-per-second rule.
- Overpass answered 504 for several minutes (load shedding across its
  servers). The retry was spaced 75 seconds apart and rotated across the
  main server's backends. It answered on the third attempt.

**The licence basis**, recorded in the script's header:

- OSM data is ODbL 1.0.
- A map drawn from it is a Produced Work under ODbL 4.3, and it must carry
  a notice crediting the contributors and saying the data is ODbL.
- The figcaption carries exactly that, visibly: *Map data (c) OpenStreetMap
  contributors, available under the Open Database License*, linked to
  openstreetmap.org/copyright and to the licence text.
- Share-alike attaches to derivative databases, and none leaves the script:
  the Overpass response is cached outside the repo, and the script refuses a
  cache path inside it.

**Greg's scope ruling is recorded where the original ruling lives**, 3.22,
and beside it in CLAUDE.md: the no-third-drawing ruling does not reach
cartography.

**Accuracy, which is the whole point.** Three candidate positions for the
shop, measured against each other:

```
Google's place pin, "Tri-County Collision" (the footer's search URL)   40.1660232, -75.0512847
the schema's geo, on every page, migrated from the live site           40.1660232, -75.0538596   ~220m west
Nominatim, "995 Jaymor Rd"                                            40.1650509, -75.0494633   ~190m southeast
```

- **The schema's latitude matches Google's to the digit, and its longitude is
  about 220m off.** That is the signature of a Google Maps URL's
  `@lat,lon` copied as the pin: that value is the viewport centre, which
  Google shifts sideways for its side panel. See 4.7, and section 5 item 26.
- **Nominatim's point is an interpolated house number** on the Jaymor Road
  way. It is not a building.

**The pin is Google's place point, and the script refuses to draw unless it
falls inside an OSM building footprint.** It does: building way 902318081,
unnamed, about 3,600 m². **Checked by eye against Google twice**: the footer's
own Google Maps link rendered, and the satellite view at the pin. Both show
"Tri County Collision Center" in the south end of the multi-tenant building on
the northeast side of Jaymor Rd, at its junction with James Way and Knowles
Ave. That is this footprint. **The road geometry was checked the same way**:

- Jaymor Road leaves that junction to the southeast and meets Second Street
  Pike (PA 232).
- Knowles Avenue runs northeast from the junction, and James Way southwest.
- The Turnpike (I-276) runs along the south, with County Line Road on the
  southwest diagonal.

The drawing agrees with Google on every one.

**What the map renders**, and nothing else:

- Roads of the drivable classes, not service drives.
- The names of the pin's street, the through roads, and the streets within
  160m of the pin.
- OSM's route numbers.
- The pin and the shop's NAP name.

**No business, landmark or POI in the data ships**, by the condition.

**The numbers the script printed:**

```
data     OSM base timestamp 2026-09-24T20:08:04Z, 707 elements
pin      40.1660232, -75.0512847 inside building way 902318081
roads    92 runs in frame: motorway 6, primary 38, residential 48
frame    480x360 units at 3.4 m/unit = 1632m x 1224m, pin at the centre
label    Jaymor Road            written "Jaymor Rd"
label    Pennsylvania Turnpike  written "Pennsylvania Tpke"
label    2nd Street Pike        written "2nd Street Pike"
label    East County Line Road  written "E County Line Rd"
label    Knowles Avenue         written "Knowles Ave"
shield   I-276   (OSM ref "I 276;PATP")
shield   PA 232  (OSM ref "PA 232")
skip     James Way: no stretch long and straight enough to carry its name
size     22,210 bytes of inline SVG
```

**The frame leaves Street Road (PA 132) out.** It is over 1km north. Reaching
it would shrink every label below legibility on a phone, and Google's own view
at this scale does not show it either.

**The alt text is computed from what was drawn**, so it cannot claim a road
the map does not show: *"Map of the roads around Tri-County Collision, marked
on Jaymor Rd in Southampton, near Pennsylvania Tpke, 2nd Street Pike, E County
Line Rd and Knowles Ave. Opens directions in Google Maps."* It is the SVG's
`aria-label`, and the SVG has `role="img"`. **The whole map is one link** to
the directions URL the card and the footers use, and so is the address line
beside it, so the action exists in text as well. The Get Directions card
stays: the map is a picture of the answer, and the card is the button for it.

**What the first draws got wrong, and the rule each one became**, every one
now written into the script:

1. **A name on a hairpin folds over itself.** "James Way" was unreadable at
   its junction. A name may only sit where the road turns less than 25° under
   its letters.
2. **Dual carriageways chained into a U.** PA 232 and County Line Road are two
   OSM ways each, meeting end to end, and the joiner made each road a U-turn.
   Runs now join only where they continue within 60°.
3. **Greedy placement starved later names.** The first name placed took the
   best spot and blocked more useful ones, and the pin's own label sat right
   across PA 232. **Placement is now an exhaustive search** over about ten
   items with up to nine places each. It writes the most items in priority
   order: the pin's street, the through roads, the route numbers, the corner
   streets. The pin's name goes left or right, whichever lets more be written.
   Label footprints are chains of small boxes that follow the letters, not
   one rectangle around a diagonal.
4. **A route number on a crossing reads as the other road's.** "PA 232" landed
   on the Turnpike crossing. A route box is now refused anywhere a major road
   carrying a different number passes under it.
5. **"Jaymor Road" on the page failed the NAP check**, and the check was
   right. OSM spells suffixes out, and the NAP is `995 Jaymor Rd`. Every label
   now takes the USPS Publication 28 abbreviation for a trailing suffix and a
   leading direction: the convention Google's own map uses on the link this
   map opens. It abbreviates what the data says, and it makes the pin's
   street match the NAP character for character. The check was not weakened.

**Idempotent, proved**: patching twice leaves exactly one map, and the
patcher refuses a page without exactly one marker pair.

**The audit's parser learned something.** An inline SVG's `<title>` would have
been read as part of the page's `<title>`, silently lengthening the measured
title. `PageParser` now ignores a `<title>` inside `<svg>`, and
`test-audit-checks.py` section 21 holds it. The map carries its alt text as
`aria-label` in any case.

#### 4. The debts

- **The 3.51 comment sentence.** The comment above `#factory-certified
  #brands, #fleet #brands` now says the trim applies to a strip nested inside
  a section, in two contexts, and names both.
- **The hours constant.** `HOURS_WEEKDAYS`, `HOURS_SATURDAY` and the schema's
  days, opens and closes now sit in `audit.py` beside the NAP. Every page's
  visible text and `llms.txt` must write any day name, `Mon-Fri`-style range
  or clock time only inside those two strings. Anything else is a critical.
  **Any Sunday is a critical**, because the record has no Sunday. The
  schema's `openingHoursSpecification` must match too. The copies are eight
  (six footers, the contact header and the new hours box) and all eight pass,
  plus `llms.txt`. **`test-audit-checks.py` section 20** holds both
  directions: the canonical pair passes, `&nbsp;` and all; and each of these
  fails:
  - the live contact page's own `Monday - Friday 8 AM - 6 PM`
  - `Mon-Fri`
  - the right days at the wrong time
  - `Saturday By Appointment Only`
  - a stray clock time
  - a stray day
  - Sunday, twice
  - a schema that closes at 17:00

  Words that only look like hours ("hours of training", "sun damage", "open")
  are left alone. **Mutation-tested**: a wrong weekday constant turns 5
  checks red, a wrong closing time 3, a neutered check 11. Disabling the SVG
  title fix turns section 21 red.

**Scores after the new per-page check.** It is one more pass on every page
that carries hours, so a service page is 19 of 20 (95) and `/contact-us/` is
17 of 18 (94). **Each page holds its recorded bar**, and sameAs is still every
page's only warning.

#### Measured

- **Seams hold the 3.46 baseline.** Header to options heading is 176 at 1440
  and 96 at 390; head-to-body is 40 at both. Each is one pixel under 3.53, and
  that pixel is the white band's hairline.
- **A 30px discrepancy was investigated rather than assumed.** 3.53's first
  probe ran while the hours still carried their "Hours" label. The label's
  removal took 28px out of the header, and the two hairlines account for the
  other 2.
- **Rendered and inspected** at 1440 full page and at 390 full page through
  the iframe. The map was inspected in the render, with the pin's position
  confirmed against the Google link by eye, as section 3 records.
- **The suite:**
  - both test scripts pass, sections 19 to 21 included;
  - `stamp-assets.py --check` and `build-sitemap.py --check` exit 0, after the
    restamp this CSS commit required on every page and the template;
  - `STAGING=1 audit.py --strict` finds **zero criticals and six warnings, all
    sameAs**.

#### Found while building, not changed. Every one goes to the owner.

- **The Google Business Profile disagrees with this site's NAP and hours**,
  read 2026-09-24 off Google's own data for the footer's search:

  ```
                     this site / live schema             Google Business Profile
  name               Tri-County Collision                Tri County Collision Center
  phone              (215) 322-5350                      (215) 999-3497
  Mon-Fri            8 a.m. to 6 p.m.                    8 AM-6 PM
  Saturday           by appointment only                 Closed
  Sunday             (not stated)                        Closed
  ```

  **(215) 999-3497 is a fourth number**, after 322-5350, the CallRail
  709-9665 and the live contact page's 515-4662. It may be a tracking number
  on the profile; nobody here knows, and CLAUDE.md says the NAP is checked
  against the profile character for character. **Nothing on this site changed over it.**
  The owner decides which is true and which side moves. Section 5, items 21
  to 24.
- **The schema's geo is about 220m west of the shop**, on all six pages (4.7).
  The brief's premise that geo is an unfilled token holds only for the
  template. ~~The coordinates found here did not enter the schema, as ruled.
  Correcting geo to the verified pin is a one-value change for Greg to rule
  on.~~ **RULED 2026-09-25, 3.56: the schema's geo is now the verified pin,
  held by `GEO_LAT` and `GEO_LON` in `scripts/audit.py`.** Section 5, item 26.
- **The focus ring on ox.** `a:focus-visible` draws a 3px `--ox` outline,
  which on an ox band is oxblood on oxblood. It is site-wide on every `.field-ox`
  band that carries a link or button, and not new here; the breadcrumb's Home
  link is simply the first link in an ox band near the top of a page. It wants
  a `.dark` focus colour in the next CSS commit. **BUILT 2026-09-28, 3.59.**


### 3.55 The header is the call alone, and the lone card centres. BUILT 2026-09-24

**Record number: 3.55**, the next after 3.54. Two rulings from Greg on
`/contact-us/`, 2026-09-24, in one commit.

#### 1. The hours come out of the ox header

The header keeps the breadcrumb, the kicker, the H1, the just-call lead and
the call button. **The hours line beside the button is gone.** The hours still
live on the page in `#find-us`'s hours box, and in the footer and the schema.

**THE 3.53 REQUIREMENT IS SUPERSEDED, NOT FORGOTTEN.** 3.53 required the hours
inside the first screen on a phone, next to the call. **Greg's ruling
withdraws it: do not restore it from reading 3.53 or 3.54.** 3.53's own
paragraphs are struck where they state it, with a pointer here. The page's
header comment says the same thing where the next editor will look.

**The fold, probed with an iframe the size of the viewport:**

```
             innerHeight  call button  call bar top  clears it by
390x664          664       418-480        604        124 (54 in 3.54)
360x640          640       418-480        580        100 (30 in 3.54)
```

The button did not move. On a phone the hours wrapped under it, so what came
back is the room they took: **the header is 70px shorter on a phone** (473 to
403), and everything below it rises by the same. At 1440 the hours sat beside
the button, so the header's height there is unchanged at 480.

**The hours constants check counts one fewer copy.** The copies site-wide are
seven, not the eight 3.54 counted: six footers and the hours box.
`/contact-us/` now reports four visible mentions (two copies, two strings
each), and every page still passes.

The `.hero.dark .cta-row` rule stays. It keeps the row left at the base
margin, which the fold still benefits from. Its comment already argues from
the fold rather than from the hours.

#### 2. The Get Directions card centres in its row

**Written as a general rule on `.grid2`**, the site's two-column card grid:
a lone last card keeps its siblings' width and centres. **What it reaches
today, grepped across every page** (comments and SVG stripped, direct
children counted):

```
docs/contact-us/                  .grid2 x5   <- the one grid it reaches
templates/service-page-template   .grid2 (template shell, cards from a token)
every other page                  no .grid2
```

**What it does not reach, on purpose**, named in the comment:

- **Glass's three `.grid3` cards** are two across from 700 to 999px, with the
  third alone. `.grid3` is designed as three across, and that width is its
  transition, so it is a separate decision.
- **`.payoff`** (3 on collision, 3 on dent) goes from one column straight to
  three.
- **`.repairs-grid`** (5 on home and collision) is always one column.

So neither of those ever has a lone card in two columns.

**The mechanism avoids a second copy of the gap.** `.grid2` becomes four
tracks with every card spanning two, which is exactly the old two columns: a
card is two tracks plus one gap, which is (width - gap) / 2. A lone last card
(`:last-child:nth-child(odd)`) starts at track 2 and lands centred. The
alternative, a `calc()` width with the 22px gap typed in again, would be two
values that must agree kept as two values. `.grid2` leaves the shared
`.grid2, .grid3, .grid4` media line, because its column definition is now its
own.

**Measured, the card widths are unchanged to the pixel**, before against
after:

```
width   cards before          cards after             lone card centre  column centre
1440    529 x5, 5th at 180    529 x5, 5th at 456          720.5            720
1000    -                     469 x5                      500.5            500
760     -                     349 x5                      380.5            380
700     -                     319 x5                      350.5            350
699     one column            one column, 659             349.5            349.5
390     one column, 350       one column, 350               -                -
```

The half pixel is subpixel rounding in the track split.

#### Measured

- **Seams hold the 3.46 baseline**, the same as 3.54: header to options
  heading is 176 at 1440 and 96 at 390; head-to-body is 40 at both.
- **Rendered and inspected** at 1440 and 390, the header and the cards: the
  header is the call alone, the fifth card sits centred under the four at
  1440, and phones are unchanged.
- **The suite:**
  - both test scripts pass;
  - `stamp-assets.py` restamped every page and the template, and `--check`
    exits 0, as does `build-sitemap.py --check`;
  - `STAGING=1 audit.py --strict` finds **zero criticals and six warnings,
    all sameAs**, with every page at its bar (95, and contact at 94).


### 3.56 The schema's geo takes the verified pin. BUILT 2026-09-25

**Record number: 3.56**, the next after 3.55. Greg's ruling, 2026-09-25: the
schema's geo **adopts the verified pin**, the point 3.54 proved three ways:

- it is Google's own place point for the shop;
- it falls inside the OpenStreetMap footprint of the building (way
  902318081);
- the satellite view shows the shop in that building, on the northeast side
  of Jaymor Rd at James Way and Knowles Ave.

#### The pair

On all six pages' `AutoBodyShop` node, and in the template:

```
BEFORE  "latitude": 40.1660232,  "longitude": -75.0538596
AFTER   "latitude": 40.1660232,  "longitude": -75.0512847
```

**Why the old one was wrong, in one line, so nobody pastes that class of
coordinate again:** it was a Google Maps URL's `@lat,lon`, which is the
viewport centre that Google shifts sideways for its side panel, not the pin.
The shift is about 220m west. **The latitude was already right**, which is why
only the longitude moves. **Take coordinates from the place's own data, never
from a map URL.**

#### The constants, and the check

- **`GEO_LAT` and `GEO_LON` in `scripts/audit.py`**, beside the NAP and the
  hours. The comment carries the provenance: Google's pin, verified
  2026-09-24 against the OSM footprint and the satellite view, and adopted by
  Greg's ruling of 2026-09-25. **Owner sign-off is outstanding**, a recorded
  vendor-verified exception like the NAP's, **and it folds into his NAP
  sign-off rather than being a new ask.** The comment also records the old
  value and the diagnosis.
- **The check:** every business node's `geo`, on every page, must equal the
  constants exactly. A business node with no `geo` fails too, because the
  node repeats in full on every page, so a missing value is drift. It is one
  pass line per page.
- **`scripts/prepare-map-image.py` now reads the same two values** instead of
  keeping its own `PIN_LAT, PIN_LON`. The map's pin and the schema's geo are
  one pair of values, so they cannot disagree. **Redrawn from the cached data,
  the page came out byte-identical** (`d091eeba5157` before and after), which
  proves the pin did not move.
- **Each page's schema comment gains the same three lines**, naming where geo
  comes from and why a map URL is never the source. The **template's
  `{{GEO_LAT}}`/`{{GEO_LON}}` tokens become the values**. Their entries leave
  the token list, and a comment above the schema says geo is no longer a
  token.

#### Proved, both directions

**`test-audit-checks.py` section 22**, 9 checks:

- **Passes:** the verified pin.
- **Fails:**
  - the old live-site value;
  - latitude and longitude swapped;
  - one digit off in the seventh decimal place;
  - Nominatim's interpolated point;
  - coordinates that are not numbers;
  - a business node with no `geo`.
- **Left alone:** a `geo` on a node that is not the business.
- **All six shipped pages** carry the pin.

**Red under a mutated value, proved and restored:**

1. **Before the pages changed**, the new check failed the old value on all
   six pages: one critical each, 6 in all. That is the check catching the
   exact error it was written for.
2. **In memory**, moving `GEO_LON` one digit turns section 22's
   seventh-place case and the shipped-pages check red.
3. **On disk**, setting `GEO_LON` back to the old value makes the full audit
   report **6 criticals**. Restored from a copy, the audit reports **0**, and
   `grep` confirms the constant reads `-75.0512847`.

#### The corrections forward

- **`prepare-map-image.py`'s header** said "THE COORDINATES DO NOT ENTER THE
  SCHEMA". It now says the schema carries this pin by this record, and that
  the map reads it from the constants.
- **3.54's paragraph** saying the coordinates stayed out of the schema is
  struck with a pointer here.
- **4.7's geo line** is marked RULED.
- **Section 5 item 26 closes as RULED**, with the note that the owner's
  confirmation folds into his NAP sign-off.
- **CLAUDE.md**: geo leaves the template's still-tokenized list and joins the
  constants beside the NAP and the hours.

#### The score table moved, and nothing got cleaner

**`/contact-us/` now reads 95, not 94.** The new check is one more pass on
every page: a service page is 20 of 21 (95.2), and contact is 18 of 19
(94.7), which rounds to 95. That is arithmetic, not improvement: contact
still runs two fewer checks by the execution-page ruling, and sameAs is still
its only warning. CLAUDE.md's paragraph on why contact read 94 now carries the
same note, so the next reader is not puzzled either way.

**No `dateModified` moved**, following 3.47 to 3.50. **No CSS, and no
restamp.** `stamp-assets.py --check` exits 0 unchanged.

#### Measured

The suite:

- both test scripts pass, section 22 included;
- `stamp-assets.py --check` and `build-sitemap.py --check` exit 0;
- `STAGING=1 audit.py --strict` finds **zero criticals and six warnings, all
  sameAs**, with **every page at 95**;
- the geo check is green on all six.


### 3.57 The blog tier: the index, the post shape, and the first post. BUILT 2026-09-25

**Record numbers: 3.57 and 3.58.** This record covers `/blog/`, the post shape
and the one post that proves it. **3.58** covers the other fifteen posts,
landed in batches of five with a commit per batch. The two category-archive
301s are cutover redirect-map material, not this run's.

#### The inventory, before anything was built

The live `/blog/` is paginated: 9 posts on page one and 7 on page two, and
pages three and four are empty. **16 distinct posts, the same 16 as the live
`post-sitemap.xml`**, which is `pagemap.md`'s count, so the map stands.
Dates are the live posts' own `article:published_time` and
`article:modified_time`, in Eastern time. **Every visible date on the live
index matches its post's Eastern publish date.** Word counts are the article
body, measured on the live page.

```
 #  published   modified    words  slug
 1  2023-03-29  2023-03-29    875  what-do-all-those-lights-mean-in-my-car-understanding-your-vehicles-language
 2  2023-05-02  2023-05-02    477  the-ultimate-guide-to-collision-repair-services-what-to-expect-and-how-to-choose-the-best-provider
 3  2023-05-02  2023-05-02    448  the-importance-of-oem-parts-in-collision-repair-ensuring-quality-and-safety-for-your-vehicle
 4  2023-05-23  2023-05-23    591  the-art-of-paintless-dent-repair
 5  2023-05-23  2023-05-23    491  assessing-collision-damage
 6  2023-07-10  2025-06-06    590  preserving-value-how-tri-county-collision-center-impacts-the-resale-value-of-your-car-through-collision-repair
 7  2023-07-11  2023-07-11    570  unveiling-the-hidden-benefits-of-paintless-dent-repair-in-collision-restoration
 8  2025-05-22  2025-06-06    758  collision-repair-near-me-in-southampton-how-to-choose-the-right-auto-body-shop
 9  2025-06-06  2025-06-06   2447  critical-questions-to-ask-any-collision-center-in-bucks-county-before-handing-over-your-keys
10  2025-07-31  2025-07-31    502  is-my-car-totaled-expert-insights-from-your-southampton-collision-repair-specialists
11  2025-07-31  2025-07-31    488  after-the-unthinkable-your-first-steps-following-a-car-accident-in-bucks-county-before-calling-a-collision-shop
12  2025-08-12  2025-08-12    734  misconceptions-about-collision-repair
13  2025-08-12  2025-08-12    612  the-risks-of-driving-a-damaged-vehicle-in-the-southampton-area
14  2025-09-16  2025-10-02    739  deer-season-in-bucks-county-insurance-coverage-next-steps
15  2025-09-16  2025-09-16    829  your-right-to-choose-a-body-shop
16  2025-09-24  2025-09-24    781  adas-calibrations-after-a-crash
```

**What the survey found across all sixteen**, before a line was written:

- **Only post 1 uses images**: 21 warning-light screenshots. It is flagged
  in 3.58.
- **Only post 1 trips the hours check**, and its trips are genuine HOURS
  mentions ("shop hours are Monday-Friday 8am-6pm, and Saturday by
  appointment"). That is the check doing its job, the hours written a
  second way, so it is a pair in 3.58 and not the question the brief feared.
- **No post mentions a day or a time outside the hours.** The brief's
  non-hours question, "rear-ended on a Saturday", does not arise in this
  blog.
- **Post 1 prints "995 Jaymor Road"**, the one address variant.
- **Two posts carry em dashes, and two carry spaced en dashes used as em
  dashes.** Numeric ranges ("1–3 business days") are correct en-dash use
  and stay.
- **"Tri County Collision Center" and its variants appear 77 times** across
  all sixteen posts, counted by the script.
- **Two posts carry real FAQ sections**: deer season, 4 questions, and this
  record's post, 4 questions.
- **The live posts carry a "Greg Quinn" byline and author box.** Per the
  brief, authorship is the shop's, and no personal byline migrates.

#### Greg's ruling: two new declared kinds

Asked before anything was built, because the FAQPage warning would have held
all seventeen pages under the gate. **Ruling, 2026-09-25: two kinds, `post`
and `blog-index`, each exempt from `faq-schema` and nothing else.**

In his words: "a post is a read and an index routes; neither page type
answers questions, so neither is measured for an answer block." **Thin
content stays live on both, deliberately**: "a post below 300 words SHOULD
warn, because a thin post is a real editorial problem in a way a missing FAQ
is not."

**His condition, beyond the proposal**: the exemption means a post is not
REQUIRED to carry FAQPage, **never that FAQs on a post go unmeasured**.

**Building to it found a real gap.** On an ordinary page, a visible FAQ with
NO schema is caught only by the general FAQPage warning; the mirror branch
deliberately stays quiet there. With `faq-schema` exempted, such a page would
have gone entirely unmeasured. **So the exemption applies only to a page that
shows no visible FAQ.** A post-kind page with one is measured like any page:

- no schema warns;
- a mismatched schema fails the mirror;
- a matching schema passes.

This holds for contact too.

**`test-audit-checks.py` section 23**, 14 checks, covers both kinds and both
directions:

- **Exempt:** a post or index with no FAQ gets no warning, and a note says
  so.
- **Still measured:**
  - a thin one still warns;
  - one with a visible FAQ and a mismatched schema fails;
  - one with a visible FAQ and no schema is warned, not excused;
  - one with a matching FAQ passes.
- **No exemption:** a misspelled kind, and contact showing an FAQ.

Section 19's "no blanket kind" test now pins exactly three kinds with their
exact scopes. **Mutation-tested**: dropping the visible-FAQ guard turns both
"warned, not excused" checks red. Restored.

#### The post shape, built once for sixteen

Built by the new **`scripts/migrate-blog.py`**:

- It reads the live posts from a cache outside the repo.
- It takes the site's current shell from `/contact-us/`: the head assets,
  the nav, the four-service footer and the call bar.
- It applies every rule mechanically, and prints every change as a pair.
- **It refuses to write** if a title or meta is over its limit, or if an
  edit does not match exactly once.

**The shape:**

- **Header**, white (`hero band-panel`): breadcrumb Home / Blog / the post,
  the H1, and a quiet date line, "Published ..." with "Updated ..." added
  when the live post was modified on a later day.
- **Body** on silver: the prose in `.prose`, the site's existing reading
  width, **no new CSS**.
- **A visible FAQ, if the live post has one**, on white, in the site's FAQ
  grammar with a byte-identical FAQPage node.
- **ONE ask at the foot**: the Call and Email CTA row in the mold, centred as
  a section-bottom ask. Not the promise band: a post is a read, not a service
  argument.
- **The four-service footer**, with Send us your details linking to
  `/contact-us/`.

**Schema, one `@graph` per post:**

- **The full `AutoBodyShop` node** under the shared `@id`, carrying the NAP,
  the hours and the verified geo, all green on the audit's checks.
- **A `WebPage`**, whose `dateModified` is the sitemap's `lastmod`.
- **A `BlogPosting`**, with headline = the H1, datePublished and
  dateModified = the live post's own, **author and publisher = the business
  node**, and no image.
- **A `BreadcrumbList`.**
- **An `FAQPage`**, only where the post shows one.

**Staging noindex on every page, with the canonical absolute per slug.**
og:image follows home's, commented, as `/contact-us/`'s does.

**Titles drop the `| Tri-County Collision` suffix**, and this is argued
rather than defaulted. At 60 characters, a 22-character brand name leaves 38
for the promise, which would cut the words the post exists for. **Every
title is the live H1's own words, trimmed.** Google shows the site name in
results separately. The service pages keep their suffix; a post's title is
the headline's promise.

**Mechanical rules, applied to every post:**

- the business name as the NAP writes it;
- own-site links made relative, or made pending spans until their target
  lands;
- Google Maps and search links become the footers' one directions URL;
- a malformed href repaired to what its anchor says;
- no image;
- markup reduced to the prose the site styles (`p`, `h2` to `h4`, lists,
  `strong`, `em`, `a`);
- no-break spaces and empty paragraphs removed.

**Dates are facts**: nothing is freshened.

**The AI-disclosure rule does not bite here**, because these posts are
migrated, not drafted. It applies the day a new post is drafted in this
repo.

#### The index, `/blog/`

**Its `pagemap.md` row: add the H1 and the meta the live index lacks.**

- **H1: "Collision Repair Tips & Advice"**, which is the live index's own
  `<title>`.
- **Title: "Collision Repair Tips & Advice | Tri-County Collision"** (53).
  BEFORE: "Collision Repair Tips &amp; Advice | Tri County Collision".
- **Meta** (153, new; BEFORE: none): "Collision repair tips and advice from
  Tri-County Collision in Southampton, PA: insurance claims, your right to
  choose a shop, dent repair, ADAS and more."
- **The same sentence is the header's lead, word for word**, so the index
  adds no copy beyond that one pair.

**The 16 posts are cards** in the home router's whole-card grammar
(`a.svc-card` in `.grid2`, which is even, so no lone card), newest first.
Each card carries the post's H1, its date line and **the first sentence of
its own opening**. **A card whose post has not landed is a
`div.svc-card data-pending-href`** with no lift and an ink heading, which is
the home router's precedent. The pending-link test turns each into a link the
day its post exists. Today that is 1 linked and 15 pending.

**Schema:** `CollectionPage` (added to `build-sitemap.py`'s
`PAGE_NODE_TYPES`, as that constant's comment anticipated), plus a `Blog`
node whose `blogPost` lists only the posts that exist, each as a bare `@id`.
Its `dateModified` is 2026-09-25, the day it was built, because the index is
new.

**The ground is white, not ox, argued:**

- The band routes rather than asks, and the palette law keeps oxblood for
  asking.
- Ink would need a breadcrumb and a lead rule the system lacks. That is the
  gap 3.53 found for ox, and 3.54 closed it for ox only.
- White is fully supported: the crumb at `--ink-2` reads 9.80 there, and the
  cards below sit on silver, per 3.52's adjacency rule.

**Reachability is deliberately deferred.** Nothing in the nav or the footers
links `/blog/` yet: the header-nav sweep is its own queued sitting, and the
footer's columns have no honest seat for it. The index is in the sitemap and
`llms.txt` today, and the nav sweep gives it its visible door.

**`llms.txt`** gains `/blog/` under Key pages and a "Blog posts" section, one
line per post (title and date), generated from the built pages so it cannot
drift from them.

#### The first post: `/your-right-to-choose-a-body-shop/`

**Chosen because it proves the most at once:**

- a visible FAQ;
- a held certification claim;
- standalone-test openers;
- and it is the target of `/collision-repair/`'s long-pending link.

**That link landed**: the collision page's "our blog post on the topic" in
its right-to-choose FAQ was a pending span, the test failed the day this post
existed, and it is now a link.

**The pairs, as the script printed them:**

| Where | Before | After | Why |
|---|---|---|---|
| title | PA Law: Your Right to Choose a Body Shop (Anti-Steering Explained) \| Tri County Collision | PA Law: Your Right to Choose a Body Shop (Anti-Steering) | 56 characters, machine-counted |
| meta | In Pennsylvania, the repair shop is your choice, not the insurer's. Learn how anti-steering rules work, how to document your choice with Tri County Collision in Southampton, and more. | In Pennsylvania, the repair shop is your choice, not the insurer's. How anti-steering rules work and how to document your choice with Tri-County Collision. | 155 characters, machine-counted |
| name, 5 places | Tri County Collision Center (and variants) | Tri-County Collision | the NAP's name; the service pages' precedent |
| body | (Honda, Toyota, Subaru, Ford, GM, and more) | (Honda, Subaru, Ford, GM, and more) | **HELD**: Toyota is not among the twelve factory certifications the site checks and publishes. An unconfirmed certification does not ship. Owner question 27 |
| FAQ 1 opener | No. In Pennsylvania, you choose where to repair your vehicle. | No, in Pennsylvania you choose where to repair your vehicle. | standalone test: a bare "No." comma-merges |
| FAQ 2 opener | It shouldn't be. | No, your claim shouldn't be delayed if you use a different shop. | standalone test: says nothing when lifted |
| FAQ 4 opener | It's not required by the PA Insurance Department's guidance; | Multiple estimates are not required by the PA Insurance Department's guidance; | standalone test: "It's" has no antecedent |

The H1 is the live one, unchanged.

**FAQ 3's opener stands alone and is untouched:** "The repair warranty comes
from the shop that performs the work."

**The four FAQs mirror byte-identically**, and the audit passes the mirror.

#### Measured

- **The mirrors, by hash.** Title, og:title and the page node's name, and
  meta, og:description and the node's description, are each byte-identical,
  decoded:

  ```
  /blog/                    title 53  af721126cbaf x3   description 153  bde39160cb85 x3
  /your-right-to-choose-.../ title 56  ef384218edbc x3   description 155  ab5298390ade x3
  ```

- **The banned strings, grepped before the audit ran.** Neither page carries
  709-9665, 515-4662, 999-3497, `info@`, "Jaymor Road", "Jaymor Rd.", "Tri
  County" or an em dash. The one grep hit, "Any Collision Center" in a post
  title on the index, is a generic phrase, not the shop's name.
- **The fold at 390x664**, with an iframe the size of the viewport:
  - **Index:** the H1 is at 239 to 320 and the lead ends at 465. **The first
    card starts at 562, inside the first screen**, above the call bar at
    604.
  - **The post:** the H1 is at 263 to 466 (five lines), the date line at 484
    to 512, and **the first paragraph starts at 609**, just under the call
    bar at 604. See the first open question below.
- **Seams hold the 3.46 baseline:**
  - **The post:** header to body 177 at 1440 and 97 at 390; body to FAQ the
    same; head-to-body 40.
  - **The index:** 177 and 97, **after a fix**. Its header first ended on
    the H1, whose .5em bottom margin put the seam at 208 and 115. Closing it
    on the lead paragraph, whose last-child margin is 0, fixed that.
- **Rendered and inspected** at 1440 and 390, the index and the post.
- **The suite:**
  - both test scripts pass, sections 19 to 23;
  - `stamp-assets.py --check` and `build-sitemap.py --check` exit 0, and the
    sitemap now has 8 URLs, the post's `lastmod` 2025-09-16;
  - `STAGING=1 audit.py --strict`: **eight pages, every one at 95, zero
    criticals, sameAs the only warning.**

#### Open, for Greg

1. **A post-scale H1.** The site's H1 is sized for short service titles:
   `clamp(2.3rem, 6.2vw, 3.9rem)`. Post headlines run 60 to 114 characters.
   On a phone, this post's 66-character H1 takes five lines, and its first
   paragraph lands under the call bar. The longest, post 11 at 114
   characters, will take about nine lines. **Not written, per Part C.**
   Proposed: one rule scoped to the post header, e.g. `#post-head h1 {
   font-size: clamp(1.9rem, 4.6vw, 2.9rem); }`, measured on the render
   before it lands. **BUILT 2026-09-28, 3.59.**
2. **The breadcrumb's third item wraps onto its own line on a phone**, with
   its separator leading. It reads, but a post title in a crumb is long by
   nature. Truncating it would need CSS too; noted, not proposed.


### 3.58 The other fifteen posts, in batches of five. BUILT 2026-09-25

The post shape and every rule are 3.57's. `scripts/migrate-blog.py` built each
batch and printed its pairs, and **every batch passed the gates before its
commit**:

- the banned-string grep, before the audit;
- both test scripts;
- `STAGING=1 audit.py --strict`: every page at 95, sameAs the only warning,
  zero criticals.

Each landing turns the index's pending cards into links. `llms.txt` and the
sitemap regenerate with each batch.

**Every post in this record carries its own publish date as `lastmod`**, so
the sitemap now says truthfully that most of the blog is old. The three
posts the live site modified later carry that later date and an "Updated"
line.

#### Batch 1, posts 1 to 5 (2023-03-29 to 2023-05-23)

**FLAGGED, post 1, `/what-do-all-those-lights-mean-in-my-car-.../`: NO
IMAGE.** The live post pairs each of its 21 warning lights with a screenshot
of the symbol, and a reader matches a light by its symbol. **The text names
and explains every light and stands on its own, but the post is weaker
without them.** The screenshots are old-site imagery, and so banned. Shipped
text-first. A licensed or owner-supplied symbol set would restore it.

| Post | Where | Before | After | Why |
|---|---|---|---|---|
| 1 lights | title | What do all those lights mean in my car? Understanding your vehicle's language! \| Tri County Collision | What do all those lights mean in my car? | 40, the H1's own question |
| 1 | meta | In this blog post, Tri County Collision helps drivers understand their vehicle's warning lights and indicators. From the check engine light to the oil pressure warning, our experts explain what each light means and what to do if it comes on. | What your car's warning lights mean, from engine temperature and oil pressure to tire pressure and traction control, and what to check when one comes on. | 153. **The live meta promised "the check engine light", which the post never covers**; the new one names only lights it explains |
| 1 | name, 5 places | Tri-County Collision Center | Tri-County Collision | the NAP's name |
| 1 | body | such as[em dash]the anti-lock | such as the anti-lock | no em dashes; the glyph is named here, not printed |
| 1 | body | 995 Jaymor Road, Southampton, PA  18966 | 995 Jaymor Rd, Southampton, PA 18966 | the NAP's street, and one space before the ZIP |
| 1 | body, and the link | 215.322.5350, `tel:12153225350` | (215) 322-5350, `tel:+12153225350` | the NAP's phone and tel: form |
| 1 | body | shop hours are Monday-Friday 8am-6pm, and Saturday by appointment. | shop hours are Monday to Friday, 8 a.m. to 6 p.m., and Saturday by appointment only. | the hours as `HOURS_*` write them; the audit fails any other spelling |
| 2 guide | title | The Ultimate Guide to Collision Repair Services: What to Expect and How to Choose the Best Provider \| Tri County Collision | The Ultimate Guide to Collision Repair Services | 47, the H1 to its colon |
| 2 | meta | Discover the ultimate guide to collision repair services, including what to expect during the process and expert tips on selecting the best provider for your vehicle's needs. | The ultimate guide to collision repair services: what to expect during the process and expert tips on choosing the best provider for your vehicle. | 146 |
| 2 | name, 9 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 2 | link | google.com/search?q=tri+county+collision+center&... | the footers' directions URL | "Research online reviews and testimonials": one Google destination, no tracking parameters |
| 3 OEM | title | The Importance of OEM Parts in Collision Repair: Ensuring Quality and Safety for Your Vehicle \| Tri County Collision | The Importance of OEM Parts in Collision Repair | 47, the H1 to its colon |
| 3 | meta | Learn why Tri County Collision Center prioritizes OEM parts in collision repair, and discover how they ensure the highest quality, safety, and value for your vehicle during the repair process. | Learn why Tri-County Collision prioritizes OEM parts in collision repair and how they ensure quality, safety, and value for your vehicle. | 137 |
| 3 | name, 6 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 4 PDR | title | The Art of Paintless Dent Repair: A Cost-Effective Solution for Minor Collisions \| Tri County Collision | The Art of Paintless Dent Repair: A Cost-Effective Solution | 59 |
| 4 | meta | Discover the art of paintless dent repair at Tri County Collision Center. Explore the cost-effective and efficient solution for minor collisions, preserving your vehicle's original finish. | The art of paintless dent repair at Tri-County Collision: a cost-effective, efficient fix for minor collisions that preserves your vehicle's original finish. | 157 |
| 4 | name, 7 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 5 damage | H1 | ... Assessing Collision Damage Severity at Tri County Collision Center | ... Assessing Collision Damage Severity at Tri-County Collision | the NAP's name |
| 5 | title | From Fender Benders to Major Crashes: Assessing Collision Damage Severity at Tri County Collision Center \| Tri County Collision | Assessing Collision Damage: Fender Benders to Major Crashes | 59; the promise words kept, reordered |
| 5 | meta | Discover how Tri County Collision Center accurately assesses collision damage severity, from minor fender benders to major crashes | Discover how Tri-County Collision accurately assesses collision damage severity, from minor fender benders to major crashes | 123; the name only |
| 5 | name, 7 places | Tri County Collision Center | Tri-County Collision | the NAP's name |

**Gates:**

- the grep is clean on all five;
- both test scripts pass;
- **thirteen pages, every one at 95, zero criticals, thirteen sameAs
  warnings and nothing else**;
- post 1's rewritten hours line passes the hours check;
- the index now has 6 linked cards and 10 pending;
- the sitemap has 13 URLs.

#### Batch 2, posts 6 to 10 (2023-07-10 to 2025-07-31)

**Post 6 links to post 3**, the blog's one post-to-post link. Post 3 landed
in batch 1, so it is a real link from the start.

**Two posts keep their live metas verbatim**, because they already fit: post
8 (147) and post 9 (153).

| Post | Where | Before | After | Why |
|---|---|---|---|---|
| 6 value | H1 | Preserving Value: How Tri County Collision Center Impacts ... | Preserving Value: How Tri-County Collision Impacts ... | the NAP's name |
| 6 | title | Preserving Value: How Tri County Collision Center Impacts the Resale Value of Your Car through Collision Repair \| Tri County Collision | Preserving Value: How Collision Repair Impacts Resale Value | 59; the brand leaves the title, where it is not the promise |
| 6 | meta | Protect your car's resale value with Tri County Collision Center's expert collision repair services. Trust us to restore your vehicle to its pre-collision condition and enhance its appeal. | Protect your car's resale value with Tri-County Collision's expert collision repair, restoring your vehicle to its pre-collision condition and appeal. | 150 |
| 6 | name, 7 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 7 PDR benefits | title | Unveiling the Hidden Benefits of Paintless Dent Repair in Collision Restoration \| Tri County Collision | Unveiling the Hidden Benefits of Paintless Dent Repair | 54 |
| 7 | meta | Discover the hidden benefits of paintless dent repair at Tri County Collision Center. Preserve your vehicle's original factory finish, save money, and get back on the road faster with this cost-effective and environmentally friendly collision restoration technique. | The hidden benefits of paintless dent repair at Tri-County Collision: your original factory finish preserved, money saved, and back on the road faster. | 151; "environmentally friendly" leaves the meta only |
| 7 | name, 6 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 8 near me | title | "Collision Repair Near Me" in Southampton? How to Choose the Right Auto Body Shop \| Tri County Collision | "Collision Repair Near Me"? Choosing a Southampton Body Shop | 60; the searched phrase kept, which is the post's promise |
| 8 | name, 4 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 8 | body | the Tri County Difference | the Tri-County Difference | the name as the NAP writes it; caught by the grep, not by the mechanical rule, which needs the full name |
| 8 | link | google.com/maps/place/Tri+County+Collision+Center/@40.1660232,-75.0512847,... | the footers' directions URL | "Online reviews": one Google destination |
| 9 questions | title | Critical Questions to Ask Any Collision Center in Bucks County Before Handing Over Your Keys \| Tri County Collision | Critical Questions to Ask a Bucks County Collision Center | 57 |
| 9 | name, 9 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 9 | body, 3 places | (like ADAS [spaced dash] Advanced ...), (Original Equipment Manufacturer [spaced dash] parts made by ...), updates [spaced dash] a simple | (like ADAS, Advanced ...), (Original Equipment Manufacturer: parts made by ...), updates: a simple | a spaced dash is an em dash by another glyph |
| 9 | link, 2 places | google.com/maps/place/... | the footers' directions URL | review links: one Google destination |
| 10 totaled | title | Is My Car Totaled? Expert Insights from Your Southampton Collision Repair Specialists \| Tri County Collision | Is My Car Totaled? Expert Insights from Southampton | 51 |
| 10 | meta | Wondering if your car is totaled? Get expert insights from Southampton's trusted collision repair specialists. Learn what 'totaled' really means and get a free professional assessment today. | Wondering if your car is totaled? Southampton's collision repair specialists explain what 'totaled' really means and offer a free professional assessment. | 154 |
| 10 | name, 3 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 10 | body | close to[em dash]or exceeds[em dash]its market value | close to, or exceeds, its market value | no em dashes; commas carry the aside |

**The review links carry the verified pin.** The live posts' three Google
Maps links carry `@40.1660232,-75.0512847`, which is 3.56's value exactly:
independent confirmation that the place point adopted is the one the shop
itself linked to.

**Post 9's Toyota mentions are illustrations, not claims**: "a Toyota
collision center", "a new Toyota", and what a good shop "might say". They
stay.

**Gates:**

- the grep is clean;
- both test scripts pass;
- **eighteen pages, every one at 95, zero criticals, eighteen sameAs
  warnings and nothing else**;
- the index now has 11 linked cards and 5 pending;
- the sitemap has 18 URLs.

#### Batch 3, posts 11 to 14 and 16 (2025-07-31 to 2025-09-24)

**The ADAS post stays a post**, as `pagemap.md`'s ADAS gate names it as
source material. Its live link to the glass page ("Book Auto Glass Repair &
Replacement and we'll coordinate the calibration step") now lands on the
glass page's `#adas` section. It gains a link to an ADAS page only if that
page ever clears its gate.

| Post | Where | Before | After | Why |
|---|---|---|---|---|
| 11 first steps | title | After the Unthinkable: Your First Steps Following a Car Accident in Bucks County (Before Calling a Collision Shop) \| Tri County Collision | Your First Steps Following a Car Accident in Bucks County | 57; the promise kept, the flourish dropped. The H1 is unchanged |
| 11 | meta | Just had a car accident in Bucks County? Stay calm with our step-by-step guide on what to do before choosing a collision shop. Local tips from Southampton's trusted repair experts. | Just had a car accident in Bucks County? A step-by-step guide to what to do before choosing a collision shop, from Southampton's trusted repair experts. | 152; the live non-breaking hyphens become plain ones |
| 11 | name, 2 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 12 myths | title | Top 5 Misconceptions About Collision Repair (And the Truth from Your Southampton Experts) \| Tri County Collision | Top 5 Misconceptions About Collision Repair | 43 |
| 12 | meta | ... Get the expert facts from Tri County Collision. | ... Get the expert facts from Tri-County Collision. | 155; the name only |
| 12 | name, 2 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 12 | link | `http://ASE/ I-CAR® Gold technicians` | `../contact-us/` | "Contact Us today": a malformed href; the anchor says Contact Us |
| 13 risks | title | Don't Delay Repairs! The Risks of Driving a Damaged Vehicle in the Southampton Area \| Tri County Collision | Don't Delay Repairs! The Risks of Driving a Damaged Vehicle | 59 |
| 13 | meta | ... dangers of delaying your collision repair. Protect yourself and your vehicle. | ... dangers of delaying your collision repair. | 133 |
| 13 | name, 2 places | Tri County Collision Center | Tri-County Collision | the NAP's name |
| 14 deer | title | Deer Season in Bucks County: Insurance Coverage & Next Steps \| Tri County Collision | Deer Season in Bucks County: Insurance Coverage & Next Steps | 60, the H1 exactly |
| 14 | meta | Navigate deer season smart: Safety and documentation tips, how claims work, and expert repairs from Tri County Collision to restore your vehicle to pre-accident condition. | Navigate deer season smart: safety and documentation tips, how claims work, and expert repairs from Tri-County Collision to restore your vehicle. | 145 |
| 14 | name, 2 places, and a heading | Tri County Collision Center; How Tri County handles | Tri-County Collision; How Tri-County handles | the NAP's name; the heading caught by the grep |
| 14 | FAQ 1 opener | Yes, if you carry comprehensive coverage. | Hitting a deer is covered by your insurance if you carry comprehensive coverage. | standalone test: "Yes, if" carries no subject |
| 14 | FAQ 4 opener | Only if it's truly safe: | You can drive home after hitting a deer only if it's truly safe: | standalone test: "Only if" carries no subject |
| 16 ADAS | title | ADAS Calibrations After a Crash: The Hidden Step That Protects Your Family \| Tri County Collision | ADAS Calibrations After a Crash: The Hidden Step | 48 |
| 16 | meta | Not just body work: ADAS calibrations after a crash restores lane, brake, and blind-spot tech ... | ADAS calibrations after a crash restore lane, brake, and blind-spot tech ... | 160; the verb agrees with its subject |
| 16 | name, and a heading | Tri County Collision Center; How Tri County coordinates | Tri-County Collision; How Tri-County coordinates | the NAP's name |
| 16 | body, 6 places | Label [spaced dash] Text, in the six-step list | Label: Text | a spaced dash is an em dash by another glyph; "1–3 business days", a range, stays |
| 16 | link | ../auto-glass-repair-replacement/ | ../auto-glass-repair-replacement/#adas | the brief's ruling on the ADAS post |

**The deer post's four FAQs and the right-to-choose post's four mirror
byte-identically.** FAQs 2 and 3 of the deer post already stood alone:
"Pennsylvania law says insurers may not increase your premium..." and "Call
police if anyone is hurt or the vehicle needs a tow...".

**Gates:**

- the grep is clean, and **"Tri County" appears nowhere on the site**;
- both test scripts pass;
- **twenty-three pages, every one at 95, zero criticals, twenty-three sameAs
  warnings and nothing else**;
- seven FAQ mirrors pass site-wide;
- **the index links all 16**, none pending;
- the sitemap has 23 URLs.

#### Measured, and one proof owed

**Part D asked for the fold probe, renders and seams on EVERY commit. They
ran for 3.57's commit and for this last one, NOT for batches 1 and 2**,
whose commits were gated on the suite alone. That is recorded rather than
smoothed over. **To cover it, the seams were measured on all sixteen posts
and the index at this commit**, which includes every page those two batches
landed:

- **The index and 15 of 16 posts hold the 3.46 baseline**: 177 at 1440 and
  97 at 390, and every page's laid-out width is true.
- **The deer post's body-to-FAQ seam is 194 and 114, 17px over.** Its prose
  ends on a list, and `ul` keeps its bottom margin where a last paragraph's
  is zeroed. Right-to-choose ends on a paragraph, which is why it measured
  clean. **One CSS rule fixes it, and per Part C it is not written.** Open
  item 2.

**The fold at 390x664:**

- **Index:** the first card at 562, inside the first screen.
- **The worst-case post**, 11, with its 114-character headline: the H1 runs
  eight lines (263 to 587), and **the first paragraph starts at 731, below
  the call bar at 604.**

**Headline heights on a phone** run 202 to 324px: 5 to 8 lines at the
site's H1 scale.

**Rendered and inspected at this commit:**

- the index at 1440 and 390;
- post 11 at 1440 and 390;
- the deer post at 1440, with its FAQ on white and the one ask at its foot.

#### Open, for Greg, ranked

1. **A post-scale H1.** Measured across all sixteen: 5 to 8 lines on a
   phone. On the worst case the first line of reading starts below the fold.
   Proposed: `#post-head h1 { font-size: clamp(1.9rem, 4.6vw, 2.9rem); }`,
   measured before it lands. **BUILT 2026-09-28, 3.59.**
2. **A list that ends the prose keeps its margin**, putting the deer post's
   seam 17px over baseline. Proposed: `.prose > :last-child {
   margin-bottom: 0; }`. It reaches every `.prose` block, so the grep and a
   re-measure come first. **BUILT 2026-09-28, 3.59.**
3. **The post breadcrumb's long third item wraps on a phone.** It reads;
   noted, not proposed.
4. **Owner questions 27 and 28**, and the claims in 4.11. The heaviest are
   the posts' **legal statements** and post 9's **specific warranty terms**.

### 3.59 Three CSS rules: post headlines, the prose seam, the focus ring on dark. BUILT 2026-09-28

One housekeeping commit carrying three rules that were already proposed and
measured, or queued, in earlier records: 3.57 and 3.58 open item 1, 3.58 open
item 2, and the focus-ring note in 3.54. **The number is 3.59, taken in
sequence**: nothing has landed since 3.58. One restamp covers all three
(`?v=078d4f49`), and the diff is `site.css` plus the 24 stamp lines and
nothing else. **No copy, markup or schema changed.**

**How it was measured.** Headless Chrome with reduced motion forced, and every
page in an iframe inside a wider window, per `scripts/mobile-check.md`:

- **Fold probes** use an iframe exactly the viewport's size, with
  `innerHeight` printed beside every answer.
- **Section maps** use an iframe taller than the page, taken twice at two
  heights. The two maps agree on all 23 pages at 1440 and 390, and every
  page lays out at its true width.
- **The layout hash** fingerprints every element box on the page, at
  quarter-pixel resolution, at 1440x900, 390x664 and 360x640. It was taken on
  all 23 pages before the change and again after it.

#### 1. Post headlines scale down

```css
#post-head h1 { font-size: clamp(1.9rem, 4.6vw, 2.9rem); }
```

**It is the proposed value, unchanged**, and the reason it was not tuned is
below. On a phone the floor governs, so the size is 30.4px where it was
36.8px. At 1440 the cap governs, so it is 46.4px where it was 62.4px.

**Across all sixteen posts:**

```
            lines before   lines after   H1 height before   after
1440           3 to 4         2 to 3         206 to 275     102 to 153
 390           5 to 8         4 to 7         202 to 324     134 to 234
 360           5 to 9         4 to 8         202 to 364     134 to 268
```

**The worst three titles, by length**, measured before and after with the
iframe equal to the viewport. `innerHeight` was 664 and 640 on every row, and
the page laid out at 390 and 360. "Line 1 ends" is the bottom of the first
paragraph's first line box. The call bar starts at 604 on a 390x664 viewport
and at 580 on 360x640.

```
                                        H1 lines   para top   line 1 ends   against the bar
post 11, 114 chars   390 cutover  before    8         673         699        below by 69
                                  after     7         581         607        top on screen, line 1 cut by 3
                     390 banner   before    8         731         757        below by 127
                                  after     7         638         664        below by 34
                     360 cutover  before    9         714         740        below by 134
                                  after     8         614         640        below by 34
                     360 banner   before    9         771         797        below by 191
                                  after     8         671         697        below by 91
post 6, 104 chars    390 cutover  before    7         633         659        below by 29
                                  after     6         547         573        ON SCREEN, 31 to spare
                     390 banner   before    7         690         716        below by 86
                                  after     6         604         630        below by 0
                     360 cutover  before    8         701         727        below by 121
                                  after     6         575         601        top on screen, line 1 cut by 21
                     360 banner   before    8         759         785        below by 179
                                  after     6         632         658        below by 52
post 7, 99 chars     390 cutover  before    7         608         635        below by 4
                                  after     6         522         549        ON SCREEN, 55 to spare
                     390 banner   before    7         665         692        below by 61
                                  after     6         579         606        top on screen, line 1 cut by 2
                     360 cutover  before    8         648         675        below by 68
                                  after     6         522         549        ON SCREEN, 31 to spare
                     360 banner   before    8         706         733        below by 126
                                  after     6         579         606        top on screen, line 1 cut by 26
```

**The worst case does not quite make it, and here is how close.** On post 11
at 390x664, in the state a customer will see after cutover, the first
paragraph now starts on screen at 581, and its first line ends at 607, **3px
under the call bar**. A render with a 2px line drawn at 604 agrees: the line
sits across the descenders of "One second you're driving along Route 132 or".
At 360 the same post misses by 34. The first paragraph rose 86 to 127px on
every row, and posts 6 and 7 clear at 390 in the cutover state.

**Why the value was not tuned to close the 3px.** A size that clears it was
measured:

```
clamp(1.8rem, 4.6vw, 2.9rem)   28.8px on a phone, 1440 unchanged
  post 11   390 cutover  line 1 ends 562   ON SCREEN, 42 to spare
            360 cutover  para top 599      below by 19
  post 6    360 cutover  line 1 ends 590   cut by 10
```

**It clears the worst case at 390 and still misses at 360.** It also brings the
post H1 to 28.8px against a post H2 of 25.6px, a ratio of 1.125 where 1.9rem
holds 1.19. That spends the headline hierarchy for a result that stays short
at 360, which is a design call and not a housekeeping one. It is Greg's, and
it is open item 2 below.

**The larger lever is above the H1.** Post 11's breadcrumb is 83px tall at 390
(158 to 241), three lines, because its third item wraps onto two of its
own. That is the 3.57 open item on the breadcrumb, still not
proposed here, but it is now the biggest remaining cost in the first screen.

**No other page's H1 moved, by computed style and by layout hash.** On
the seven pages that are not posts, the H1's computed `font-size` and box are
identical before and after at all three widths:

```
/ and the four service pages   64px at 1440, 38.4px at 390 and 360
/blog/ and /contact-us/        62.4px at 1440, 36.8px at 390 and 360
```

The layout hash of **every element on those seven pages is identical before
and after at all three widths**, with one qualification recorded below the
seam table. On the sixteen posts, the only boxes that changed SIZE are
`MAIN`, the post-head `SECTION` and `DIV`, and the `H1` itself. Every other
change is a vertical shift below the H1.

#### 2. The last child of a prose block carries no margin

```css
.prose > :last-child { margin-bottom: 0; }
```

**Every `.prose` on the site was listed first**: 43 blocks on 21 pages. The
contact page and the blog index carry none. **Three end on a child with a
margin**:

```
page                          block    last child   margin   followed by   seam effect
deer-season post              #post    ul           17px     nothing       +17, the defect
adas-calibrations post        #post    ul           17px     .cta-row      none: the row's 26px wins the collapse
collision-repair-near-me post #post    h2 (EMPTY)   18.4px   .cta-row      none: the row's 26px wins the collapse
```

Of the other 40, 39 end on a paragraph, which `p:last-child` already
zeroes, and one, commercial's `#fleet`, ends on a `ul.ticks` whose margin is
already 0.

**Every seam on every page was re-measured against the 3.46 baseline.** The
maps were taken twice at two tall heights, agreed, and were diffed before
against after on all 23 pages at 1440 and 390:

```
deer post, body to FAQ    1440   194 -> 177     390   114 -> 97     the 17px correction, exactly
every other section seam  unchanged, 176-177 at 1440 and 96-97 at 390
```

**Nothing moved by more than the deer post's 17px, and nothing unexpected
moved at all.** Two readings changed by 1px: the FAQ-to-footer figure on the
deer post (132 to 131, 16 to 15) and on right-to-choose at 390 (71 to 72).
Both are on posts whose H1 changed height, and that measurement runs to the
footer's contents, so these are sub-pixel roundings of a shifted page and not
seam changes. Every other seam on those two pages is unchanged.

**The layout hash's one qualification.** On `/collision-repair/` at 390 and
360 and `/commercial-collision-repair/` at 390, a handful of 3px-wide spans
moved: the lane's dashes. **They vary between Chrome launches with the CSS
held fixed.** Three probes of the new CSS reproduced the old hash exactly on
`/collision-repair/`. With those spans left out, both pages hash identical
before and after at all three widths. The cause is recorded as a finding
below.

#### 3. The focus ring on a dark ground

```css
.dark a:focus-visible, .dark button:focus-visible, .dark summary:focus-visible { outline-color: var(--silver); }
```

**Only the colour changes.** The width, style and 2px offset stay the base
rule's. It is scoped to `.dark`, like `.dark a`, `.dark .btn` and every other
dark-ground answer, so it reaches the ox and ink bands and nothing on silver
or white, where `--ox` already measures 10.50 and 11.80.

**Silver, measured on both dark grounds:** 10.50 on `--ox` (the gradient's
brightest stop, and therefore the worst case), 12.39 on `--ox-dk` and 15.42 on
`--ink`. The floor for a focus indicator is 3:1.

**Tabbed through in the render.** Focus was moved through each scope's
focusables in document order, which is the tab order because nothing on
these pages sets a `tabindex`. Each stop was confirmed to match
`:focus-visible`, then shot, and the rendered ring's pixels were sampled
against the ground 5px outside them:

```
                                   stop                  before   after
/contact-us/ header   390          Home (crumb)           1.23    12.96
                                   Call (215) 322-5350    1.06    11.14
/contact-us/ header   1440         Home (crumb)           1.21    12.67
                                   Call (215) 322-5350    1.14    12.01
/ #start, ox promise  1440         Call (215) 322-5350    1.01    10.65
                                   Email the shop         1.07    11.21
/collision-repair/ #start, ink     Call (215) 322-5350    1.47    15.42
                      1440         Email the shop         1.47    15.42
```

**Rendered ring before:** rgb(105, 28, 23), which is `--ox` on `--ox`.
**After:** rgb(240, 242, 242), which is `--silver`, on every stop. Inspected by
eye as well: on home's promise band, "Email the shop" with focus showed no
ring at all before, and shows a clear silver ring after.

**Site-wide, the `.dark` bands this reaches:** every focusable in `#start`,
`#why`, `#after-a-crash`, `#contact`, `#what-we-fix`, `#repair-or-replace`,
`#real-repairs` and the ink `#start`: fourteen bands on six pages. Every stop
in them measured 1.00 on ox or 1.47 on ink before.

#### Found while building, not changed

1. **The same invisible ring is on every page's header and footer, and on the
   photo heroes.** None of them is `.dark`, so the brief's scope does not
   reach them. Measured site-wide at 1440, before and after, with nothing
   changed:

   ```
   header (.nav), ink            69 stops on 23 pages   1.47
   footer (footer.site), ink    322 stops on 23 pages   1.47
   .heroB--ox, service heroes    12 stops on 4 pages    1.00
   .heroB, home hero              2 stops               1.47
   .callbar, ox                  phones only            ox on ox
   ```

   **The header is every page's first tab stop**, so a keyboard reader still
   starts every page unable to see where they are. The same one-colour answer
   fits all of them: silver reads 15.42 on ink and 10.50 on ox. The hero
   rings sit over the scrim and need the scrim measurement before they land.
   Open item 1.

2. **An empty `<h2></h2>` closes the collision-repair-near-me post's prose.**
   It was carried over from WordPress. A screen reader announces it as a
   heading with no name. `migrate-blog.py` drops empty paragraphs and not
   empty headings, which is how it got through. It is the only empty heading
   or empty paragraph on the site, by grep. Removing it is a markup change
   outside a CSS commit, and rule 2 does not move it. Open item 3.

3. **The lane's dashes are measured before the webfonts may have loaded.**
   `buildLane()` in `site.js` runs once at script time and again on resize,
   never after `document.fonts.ready`. If Source Sans 3 swaps in after the
   lane is built and the step text rewraps, the dashes sit off their gaps.
   That is what made them vary between probe runs. It would do the same on a
   phone with a slow font. Open item 4.

4. **Post 6's date line wraps to two lines at 360** (56px, not 28), which is
   part of why it misses there.

#### The suite

- Both test scripts pass.
- `stamp-assets.py --check` and `build-sitemap.py --check` exit 0, and the
  sitemap is 23 pages.
- `STAGING=1 audit.py --strict`: **23 pages, every one at 95, zero
  criticals, 431 passing, and 23 warnings, every one of them sameAs.** It
  exits 1 on the sameAs bar, as every run has.
- The grep is clean: no em dash in `site.css`.

#### Open, for Greg, ranked

1. **Carry the silver ring to the header, the footer, the call bar and the
   heroes.** Same defect, same colour, and it reaches every page. The header
   and footer are ink with no photograph, so they are one selector each. The
   heroes need the scrim measured under the ring first. **BUILT 2026-09-28,
   3.60**, the call bar with its ring inset, on Greg's ruling.
2. **The post H1 at 1.8rem**, if 3px at 390 is worth the H1-to-H2 ratio
   dropping from 1.19 to 1.125. Measured above. It still misses at 360.
   **RULED 2026-09-28, 3.60: the 1.9rem clamp stands; the crumb is fixed
   instead.**
3. **Delete the empty `<h2>`**, and teach `migrate-blog.py` to drop empty
   headings the way it drops empty paragraphs. **BUILT 2026-09-28, 3.60**,
   with an audit check.
4. **Rebuild the lane after `document.fonts.ready`**: one line in `site.js`.
   **BUILT 2026-09-28, 3.60.**
5. **The post breadcrumb's long third item**, now measured at 83px on post 11
   at 390, and the largest remaining cost above the H1. **BUILT 2026-09-28, 3.60.**

### 3.60 The crumb, the rest of the ring, one empty heading, one font race. BUILT 2026-09-28

A housekeeping bundle closing 3.59's open items 1, 3, 4 and 5, in one commit
with one restamp (`site.css ?v=64bea0dd`, `site.js ?v=e67e271c`). **No copy
changed.** One element left the markup: an empty heading with no words in it.

#### Greg's rulings, 2026-09-28

1. **The post H1 clamp from 3.59 STANDS**, and is not dropped to 1.8rem. The
   first-screen cost on a post is the breadcrumb, whose last item repeats the
   H1. We fix the crumb, not the headline.
2. **The call bar's ring sits inside the bar**, with a negative offset (item 2
   below).
3. **The breadcrumb mirror check is recorded, not added.** The brief assumed
   a visible-crumb / BreadcrumbList mirror check in `audit.py`. **There is
   none**: the only mirror law in the audit is the FAQ's, and the crumb
   markup carries only a comment saying it mirrors the schema. The mirror was
   therefore proved by probe instead (item 1). A real check is open item 1.
4. **The empty-heading check is a critical.**
5. **The footer logo gets a box of its own**, with the mechanism named in the
   comment and the header logo checked for the same defect (item 2).

**How it was measured:** the 3.59 harness, unchanged. It uses headless Chrome
with reduced motion forced, iframes sized per `scripts/mobile-check.md`, and a
layout hash of every element box on all 23 pages at 1440x900, 390x664 and
360x640. The hash was taken at HEAD (`053d7bf`) and again with the finished
tree.

#### 1. The last crumb is one line

```css
.crumb li:last-child { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
```

**Adapted to what the crumb CSS actually is.** `.crumb ol` is a wrapping flex
row. The last item keeps `display: list-item` and the wrap is untouched;
**`min-width: 0` is the one adjustment**, because a flex item's automatic
minimum is its content, and without it the item cannot shrink below its text
and the ellipsis never fires. The item still drops to its own row under
"Home / Blog", as it did before. What changes is that it takes one line on
that row instead of two.

**The worst title's crumb, computed, before and after**
(`after-the-unthinkable...`):

```
                         BEFORE, 390        AFTER, 390          AFTER, 360
crumb height             83                 58                  58  (83 before)
last li display          list-item          list-item           list-item
white-space              normal             nowrap              nowrap
overflow                 visible            hidden              hidden
text-overflow            clip               ellipsis            ellipsis
min-width                auto               0px                 0px
lines                    2                  1                   1
clientWidth/scrollWidth  350/350            350/374, clipped    320/374, clipped
visibility, aria-hidden  visible, none      visible, none       visible, none
textContent              "Your First Steps Following a Car Accident in Bucks County", all three
BreadcrumbList name      the same string; the mirror holds
```

**Clipped, never hidden.** No `display: none`, no `visibility: hidden`, no
`aria-hidden`. The full title stays in the DOM and in the accessibility tree.
Only the painted line ends in an ellipsis.

**Across the site**, on 69 probes (23 pages at three widths):

- **Every visible crumb equals its BreadcrumbList, before and after.**
- **The crumb moves only where the title wrapped.** Ten posts at 390 and
  twelve at 360 go from 83 to 58. The other posts already fit on one line of
  their own and do not move, and neither does any service page, the index,
  contact, or home, which has no crumb.
- **At 1440 nothing triggers it.** The widest last item there is 423px, in a
  1080px crumb, and every 1440 hash is identical before and after.

**It reclaims 25px, not the roughly 29 the brief estimated.** A crumb line box
is 25px, measured.

**The fold, `after-the-unthinkable...` at 390x664**, with the iframe equal to
the viewport and `innerHeight` 664 on every row. The call bar starts at 604:

```
                       crumb   H1           first paragraph   line 1 ends   against the bar
cutover   before (3.59)  83    206 to 440   581               607           cut by 3
          after          58    181 to 415   555               581           ON SCREEN, 23 to spare
banner    before         83    263 to 498   638               664           below by 34
          after          58    238 to 472   613               639           below by 9
```

**The worst title now clears the first screen in the state a customer will
see.** It has 23px to spare, where 3.59 left it 3px short. The line moved 26px
where the crumb gave back 25; the extra pixel is sub-pixel rounding of a
shifted page. With the staging banner showing, it is 9px short, and the banner
comes off at cutover. At 360 in the cutover state, the first paragraph starts
at 589 against a bar at 580: 9px short, where it was 34.

#### 2. The ring on the dark surfaces `.dark` missed

```css
.nav a:focus-visible, .nav button:focus-visible,
footer.site a:focus-visible,
.heroB a:focus-visible { outline-color: var(--silver); }
.callbar:focus-visible { outline-color: var(--silver); outline-offset: -6px; }
.foot-home { display: block; width: fit-content; }
```

**Measured before anything was added to a selector.** Each stop was focused
in document order, which is the tab order here, and each matched
`:focus-visible`. Two renders were taken of every stop: one with the ring, and
one with the ring made transparent. The second gives the ground under the
ring's exact footprint, 2 to 5px outside the element. Silver was then measured
against every pixel of that ground, and the worst pixel is the figure.

```
surface                      stops   before (--ox)   silver, worst pixel   silver, median
header, ink                    10      1.47            15.42                 15.42
footer, ink                    28      1.47            15.42 on the ground   15.42
heroes, photo under scrim      42      1.00 to 1.36    6.65                  9.39 lowest
call bar, ring outside         40      1.00            1.00                  1.00 lowest   HELD, see below
call bar, ring inset 6px       40      -               10.50                 10.50         SHIPPED
```

**The heroes, every stop at every width.** Worst pixel over median, for the
crumb's Home link (on the four service pages), the call button and the email
button:

```
                              1440                 390                  360
/ (ink scrim, no crumb)       13.95 13.73          14.07 14.13          14.10 14.30
/collision-repair/            9.78  9.66  9.72     9.64  9.91  9.78     8.24  9.78  9.85
/commercial-collision-repair/ 9.66  9.79  9.98     9.33  10.05 10.11    6.65  10.05 10.11
/paintless-dent-repair/       10.50 10.50 10.10    10.42 9.85  10.11    10.16 9.85  10.04
/auto-glass-repair-replacement/ 9.85 9.78 10.05    9.01  9.66  9.79     9.07  9.66  9.79
```

**Every stop clears the 3:1 floor, so the heroes shipped**, per the brief's
rule that they ship whole or not at all. The one reading under 8.24 is
commercial's Home at 360, at 6.65.

**The footer's three low worst-pixels are not the ground.** The stops are the
inline address, phone and email in the bottom line, which read 1.43 to 1.77.
Under 3:1 there are **2 to 4 pixels out of 600 to 1,600**. They are the
anti-aliased edges of the neighbouring `--silver-2` words (201, 204, 211),
which the ring's footprint crosses. The ground under every footer ring is ink,
15.42.

**The call bar could not take the pattern.** The bar is fixed to the foot of
the viewport, so a ring drawn outside it lands on whatever has scrolled up
behind it. Measured at five scroll positions on four pages, silver outside the
bar reads 1.00 on the silver page, and the old `--ox` reads 1.00 on an ox band.
**No colour survives every ground.** Greg's ruling: the ring moves inside, onto
the bar's own `--ox`. With a `-6px` offset it sits 3 to 6px in from the edge,
clear of the 2px top border. Measured shipped, at 390 and 360, at scroll 0,
.25, .5, .75 and 1, on home, a post, `/collision-repair/` and `/contact-us/`:
**10.50 at all 40 positions, and 100% of the ring's pixels are exactly
`--silver`.**

**The footer logo drew no ring at all, and it never had.** `.foot-home` was
an inline `<a>` around a `display: block` image. An inline box around a block
child is empty: the image sits outside it, so the outline had nothing to be
drawn around. The link matched `:focus-visible` and computed a 3px outline,
and **nothing painted, in silver or in `--ox`**. A render at HEAD showed the
same. `display: block` gives the link a box. `width: fit-content` keeps that
box, which is also the focus target, the logo's 200x80 rather than the
column's 311px (350 at 390, 320 at 360).

**Measured before it landed:** the link's own box is the only box that
changes, on all 23 pages at all three widths. After it landed, its ring
renders 100% silver.

**The header logo does not share the defect**, checked because it is the
same shape:

```
            display   parent   boxes   <a> box            <img> box          ring pixels exactly silver
.nav-home   block     flex     1       168x67 at 1440     168x67 at 1440     100%, 1440 and 390
.foot-home  inline    block    3       311x80 at 1440     200x80 at 1440     none, before the fix
```

`.nav-home` is `display: block` by its own rule, and a flex item besides, so
it is one box exactly the logo's size. **The site's first tab stop draws its
ring**, and a render shows it plainly.

**Two partial readings are geometry, not a missing ring.** The two-line NAP
address, and at 390 the bottom line's address, read 81% and 48% silver under
a single-rectangle footprint. The outline follows each line fragment of a
wrapped link separately, and a render shows the ring whole around both lines.

#### 3. The empty heading, and the mechanism behind it

**The instance.** The collision-repair-near-me post lost its closing
`<h2></h2>`:

```
BEFORE  ...<a href="../contact-us/">We’re here when you need us.</a></p><h2></h2>
AFTER   ...<a href="../contact-us/">We’re here when you need us.</a></p>
```

It had a height of 0, so removing it moves nothing. At 1440 every other
element box on the page is identical before and after.

**`migrate-blog.py`** now drops any h1 to h6 whose text is empty, after the
empty strong and em go, so `<h2><strong> </strong></h2>` is caught as well.
Proved on the cached live posts in two throwaway copies of the repo:

- With the unmodified script, the post regenerates **byte-identical to the
  shipped file**, so the round trip is a fair test.
- Regenerating **all sixteen posts and the index**, old script against new,
  the output differs in **exactly one place**, the trailing `<h2></h2>`. All
  73 printed pairs are identical.
- **The new script's output equals the hand-edited post byte for byte.**

**`audit.py`** gains a check: any h1 to h6 whose text content is empty, or
only whitespace (no-break spaces included), is a **critical**. It names each
tag and line. The parser collects headings on a stack, and a heading's text
counts through any nested markup. Against the shipped HEAD version of the
post, the check fails it at `<h2> on line 322`; against the fixed page, it
passes.

**Every page gains one pass.** Posts go from 18 of 19 to 19 of 20, and the
others from 20 of 21 to 21 of 22. Both still round to 95.

**`test-audit-checks.py` section 24**, both directions:

- **Passes:** a page whose headings all carry words.
- **Caught:**
  - the shipped case;
  - spaces and a line break;
  - `&nbsp;`;
  - an empty strong;
  - a comment alone;
  - an empty link;
  - an empty `h6`;
  - an empty second `h1`;
  - two empty headings, both named.
- **Left alone:**
  - words inside a link;
  - words beside an empty icon span;
  - a heading that is only "01";
  - `<h2></h2>` inside a script string, which is not markup.
- **Every shipped page (23) has no empty heading.**

**Mutation-tested, in place, restored from a copy with the checksum
confirmed** (`b3a4d2d2be57` before and after):

```
mutant                                   red, beyond the pending restamp
the check switched off                   9: every "caught" case, and the two-named case
no-break spaces counted as words         1: the &nbsp; case
h4 to h6 dropped from the tags           2: the comment-only h4 and the empty h6
text in nested markup not counted        3: both "left alone" nesting cases, and the shipped-pages sweep
```

#### 4. The lane waits for the fonts

```js
if (document.fonts && document.fonts.ready) { document.fonts.ready.then(function () { buildLane(steps); }); }
```

One promise, settled once, after the first build. There is no listener and no
polling. The resize handler is untouched.

**Proved on the race itself.** For every dash, the check was whether its
position equals the gap `buildLane` would compute from the final layout. It
ran 24 separate Chrome launches per state: `/collision-repair/` and
`/commercial-collision-repair/`, at 390 and 360, six launches each.

```
HEAD      3 of 24 aligned in one run, 4 of 24 in a second; worst dash 80px off its gap
after     24 of 24 aligned
```

That is the variance 3.59 saw in its layout hashes, and it is what a phone on
a slow font would show: dashes on the step cards instead of between them.

#### What else moved, and nothing else did

Layout hash, HEAD against the finished tree, all 23 pages at three widths.
The lane dashes are left out, since item 4 moved them on purpose:

- **47 of 69 page-widths:** the only change is the footer logo link's width.
- **22 of 69:** that, plus the crumb's 25px and the vertical shift of
  everything beneath it. These are the post-widths where a title wrapped.
- **Nothing else, on any page, at any width.**
- **Section seams unchanged on all 23 pages.** The two FAQ-to-footer readings
  flipped by 1px, the sub-pixel rounding recorded in 3.59.

#### Found, not changed

- **An 8px strip of silver between the footer and the call bar** at the very
  end of every page on a phone. `body` reserves 68px of bottom padding for a
  60px bar. It is pre-existing, and it was seen in the footer ring renders.

#### The suite

- Both test scripts pass: 164 checks, including section 24.
- `stamp-assets.py --check` and `build-sitemap.py --check` exit 0, and the
  sitemap is 23 pages.
- `STAGING=1 audit.py --strict`: **23 pages, every one at 95, zero
  criticals, 454 passing, and 23 warnings, every one sameAs.** It exits 1 on
  the sameAs bar, as every run has.
- No em dash was added to any file this commit touches.

#### Open, for Greg

1. **A breadcrumb mirror check**, since the audit has none (ruling 3). The
   visible crumb against the BreadcrumbList, both directions, in the FAQ
   mirror's shape.
2. **The 360 fold on the worst post**, still 9px short in the cutover state.
3. **The 8px strip above the call bar**, found above.

### 3.61 The ox header comes to the blog. BUILT 2026-09-28

`/blog/` and all sixteen posts take the compact ox header `/contact-us/` has
worn since 3.54. One commit, one restamp (`site.css ?v=8cba00cb`). **No copy
changed**, and no header's contents changed.

#### Greg's ruling, recorded as given

**The compact ox header (`.hero.dark.field-ox`) is a PAGE-HEADER IDENTITY:
chrome, not an in-flow band.** The band test, "does it ask?", still governs
bands in the page flow. It does not govern the page header field. The 3.54
comment in `/contact-us/` that justified ox "because this band asks" described
that instance, not the boundary of the rule.

**Scope:** this ruling covers `/contact-us/`, `/blog/` and the sixteen posts.
**It is not a standing ruling for future tiers**: areas, towns and privacy are
decided when they are built.
**AMENDED 2026-09-28, 3.62, on Greg's ruling: the compact ox header extends to
the areas tier, the hub and all twelve town pages.** Privacy is still decided
when it is built.

**Asked and ruled while building:** the index's own head comment, written by
`migrate-blog.py`, read "THE TOP IS COMPACT AND WHITE, not ox: this band
routes rather than asks, and the palette law keeps oxblood for asking." It
would have shipped false. Greg ruled to append a 3.61 line to it, as with the
contact comment, and accept a second hunk on `/blog/` beside the header's.

#### The change

```
BEFORE  <section class="hero band-panel" id="post-head">     16 posts
AFTER   <section class="hero dark field-ox" id="post-head">
BEFORE  <section class="hero band-panel" id="blog-head">     /blog/
AFTER   <section class="hero dark field-ox" id="blog-head">
```

- **Both ids are unchanged**, so `#post-head h1`, the 3.59 clamp, still binds.
  It was not touched.
- **Every header's contents are byte-identical.** The index keeps crumb,
  eyebrow, H1 and lead; the posts keep crumb, H1 and date line.
- **No call button was added.** The nav and the call bar carry the ask on
  every page.
- **The posts' `#faq` band-panel sections and the index's card grid are
  unchanged.**

#### Mechanism, not hand-edits

**The path taken: the template first, then regeneration.** The cached live
pages were intact, and that was proved before relying on them. With the
unmodified script at HEAD, all seventeen pages regenerated in a throwaway
copy **byte-identical to the shipped files**, each built under the record it
shipped with: 3.57 for right-to-choose, 3.58 for the other fifteen and the
index.

The template then changed in `migrate-blog.py`: the two class attributes, and
the appended index-comment line. The seventeen pages were regenerated in the
repo. **The script's 73 content pairs came out identical to the HEAD run.**

**The diff is the proof.** Every changed line, before the restamp:

```
  16  -    <section class="hero band-panel" id="post-head">
  16  +    <section class="hero dark field-ox" id="post-head">
   1  -    <section class="hero band-panel" id="blog-head">
   1  +    <section class="hero dark field-ox" id="blog-head">
   3  +    (the appended index-comment lines, below)
```

Nothing else moved on any of the seventeen pages. After the restamp, the
per-page count of non-stamp lines is:

- **each post:** 2, the header's class line;
- **`/blog/`:** 5, the class line and the three comment lines;
- **`/contact-us/`:** 1, its appended line;
- **home and the four service pages:** 0.

**The two appended comments, old text kept:**

```
/blog/ head comment, after "...The argument is in the record.":
       WIDENED 2026-09-28, proposed-changes.md 3.61: Greg ruled the compact
       ox header a page-header identity, chrome and not an in-flow band, so
       this top is now ox. The band test still governs bands in the flow.

/contact-us/ header comment, after "...Every text tone on it is measured in 3.54.":
         WIDENED 2026-09-28 (3.61): Greg ruled the compact ox header a page-header identity, chrome not an in-flow band; /blog/ and its posts now wear it too.
```

**`site.css` also gained one appended sentence**, on the `.hero.dark .cta-row`
comment, whose claim that it "reaches the one header and nothing else" was
about to go false. The blog headers wear `.hero.dark` and carry no `.cta-row`,
so the rule still reaches `/contact-us/` alone. The comment now says so. No old
text was removed; only its closing `*/` moved down a line.

#### The one new tone: the date line

```css
#post-head.field-ox > .wrap > p { color: var(--silver); }
```

**Before**, the date line was a plain `<p>` with no declaration. It inherited
`--ink` from the body and read on white. **On ox it would only have inherited
a tone from `.dark`.** It now declares `--silver` itself, the tone
`.field-ox .crumb ol` and `.field-ox .lead` already take, so the header's text
is one family. The comment names the constant, not the value. The rule is
scoped to the ox header, so a post header on any other ground would not pick
up a light tone meant for a dark one.

**Every tone in the new headers, measured on the render.** Glyph boxes come
from `Range.getClientRects()`. The ground comes from a second render with the
header's text, and the crumb separators, made transparent. The figure is the
worst composited pixel:

```
                         BEFORE, on white              AFTER, on the ox gradient
                         tone       worst              tone        worst (1440 / 390)
date line (posts)        --ink      17.33              --silver    11.51-11.72 / 10.50
H1                       --ink      17.33              --silver    10.50 / 10.50
crumb links              --ox-tx     8.95              --silver    11.80-12.52
crumb current page       --ink-2     9.80              --silver    10.50-12.30
crumb separator          --rule      1.64              --rule       8.39-8.53
eyebrow (/blog/)         --ox-tx     8.95              --silver    11.01-12.01
lead (/blog/)            --ink-2     9.80              --silver    10.50 / 10.50
```

**The date line reads 10.50 at its worst**, over the gradient's brightest
stop, `--ox` exactly. It reads better toward the band's darker ends, which is
where it sits at 1440. Every tone clears the 7:1 body target. These are the
same figures `/contact-us/` measures on the same probe: 10.50 for its lead and
H1, 8.44 to 8.53 for its separator.

**The separator improved rather than regressed.** `--rule` on white was
1.64, a hairline-grade grey. On ox it is 8.39.

#### The focus ring on these headers, confirmed (no new rule)

The crumb links in these headers take the 3.59 `.dark a:focus-visible` ring
through the `.dark` class. Nothing else could supply it, since these headers
are not `.nav`, `footer.site` or `.heroB`. Each link was focused in document
order and matched `:focus-visible`:

```
page                 link    width   ring            ground               ring px silver   silver vs ground, worst / median
/blog/               Home    1440    --silver 3px    ox gradient          100%             12.52 / 12.67
                             390                                           100%             12.52 / 12.95
after-the-unthinkable Home   1440                                          100%             12.45 / 12.67
                             390                                           100%             12.52 / 12.96
                     Blog    1440                                          100%             12.30 / 12.45
                             390                                           100%             11.87 / 12.20
your-right-to-choose Home    1440                                          100%             12.45 / 12.67
                             390                                           100%             12.45 / 12.89
                     Blog    1440                                          100%             12.30 / 12.42
                             390                                           100%             11.80 / 12.16
```

**One correction to the brief's wording: the ground is not flat ox.**
`.field-ox` is the sanctioned 104-degree gradient. The crumb sits on its
darker left, which is why the ring reads 11.80 to 12.52 rather than flat
`--ox`'s 10.50. Before, on white, the `--ox` ring read 11.80.

#### What moved, and nothing else did

Layout hash, HEAD against the finished tree, all 23 pages at 1440, 390 and
360, lane dashes left out:

- **Home, contact and the four service pages: identical** at all three widths
  (18 of 69 page-widths).
- **The seventeen blog pages** (51 page-widths): the header section is 2px
  shorter, because `.band-panel` drew a 1px border top and bottom and
  `.field-ox` draws none. Its contents rise 1px, and everything beneath rises
  2px. Only `MAIN` and the header `SECTION` change size.
- **Every H1's computed size and height is unchanged** on all 23 pages at all
  three widths.

**The header-to-body seam moves 177 to 176 at 1440, and 97 to 96 at 390**,
the border it lost. It stays inside the 3.46 baseline of 176 to 177 and 96 to
97, and **it now matches `/contact-us/`'s own header seam, 176 and 96.** Every
other seam on every page is unchanged.

#### The first screen of the worst post, on the new band

`after-the-unthinkable...` at 390x664, with the iframe equal to the viewport
and `innerHeight` 664. The call bar starts at 604:

```
                  nav    ox header   crumb      H1                 date       prose line 1 ends   against the bar
cutover  BEFORE   0-68   (white)     101-159    181-415, 7 lines   430-458    581                  +23
         AFTER    0-68   68-505      100-158    180-414, 7 lines   429-457    579                  +25
banner   AFTER    0-125  125-563     157-215    237-471            487-515    637                  -33
```

**The composition, cutover state:** the ink nav takes the top 68px. **The ox
header takes 68 to 505: 437 of the 604 usable pixels, 72% of the screen.** All
of the crumb, all seven H1 lines and the date line sit on ox. The silver
reading field starts at 505, and **the first prose line is fully on screen,
ending 25px above the bar.** One of the first paragraph's seven lines is
visible. The 2px lift is the lost border.

**Still short:** at 360x640 cutover, line 1 ends at 613 against 580 (it
starts at 587). With the staging banner showing at 390, it ends at 637.

#### Rendered and inspected

`/blog/`, `after-the-unthinkable...` and `your-right-to-choose` were rendered
at 1440 and 390, before and after, and inspected:

- The ox header runs edge to edge under the ink nav, with the nav's 4px `--ox`
  rule meeting it.
- The crumb truncates inside it as 3.60 left it.
- The post H1 keeps its 3.59 scale.
- The date line reads in silver.
- The index's cards begin on the silver ground below, unchanged.

#### The suite

- Both test scripts pass: 164 checks.
- `stamp-assets.py --check` and `build-sitemap.py --check` exit 0, and the
  sitemap is 23 pages. Every `lastmod` is unchanged, because no page's
  `dateModified` moved.
- `STAGING=1 audit.py --strict`: **23 pages, every one at 95, zero
  criticals, 454 passing, and 23 warnings, every one sameAs.** It exits 1 on
  the sameAs bar, as every run has.
- No em dash was added.

#### Not changed, and worth Greg's eye

- **CLAUDE.md still describes the contact header as "the one ox band on that
  page, because it asks"**, and the palette note in `site.css` lists ox's
  sanctioned extensions without this one. Neither was in the brief, and
  neither was edited. The ruling lives here, and in the two appended
  comments.

### 3.62 The town-page template, proven on Jamison. BUILT 2026-09-28

**This record is the template's home.** Part A defines the template for
the whole areas tier: the hub and the twelve town pages. Part B builds one
page with it, `/areas-served-collision-repair-jamison-pa/`, and its two
redirect stubs. **The hub and the eleven migrating towns follow in a later
run, only after Greg approves this page.** Nothing beyond Jamison and its
shared machinery ships here.

#### Greg's rulings, 2026-09-28

1. **The compact ox header extends to the areas tier:** the hub and all twelve
   town pages. It is appended to the 3.61 ruling's record.
2. **Jamison is the pilot.** Nothing beyond Jamison and its shared machinery
   ships in this run.

**Asked and ruled while building,** each on the recommended option:

3. **The neighbors are the served ones only.** The brief named Warwick and
   Warrington. **Neither appears anywhere on the live hub**, and Jamison is
   itself a village inside Warwick Township (OpenStreetMap). The page names
   Warminster, Richboro and Ivyland, which the hub already serves, and states
   as a map fact that Jamison is in Warwick Township. Whether the shop serves
   Warrington is owner question 30.
4. **The drive time is printed from the routing and flagged for the owner.**
   It is an OSRM routing with no traffic, not a promise. Owner question 29.
5. **Build now; the Search Console gate is read before cutover.** Doctrine
   rule 7 gates new town pages on Search Console evidence, and the page map
   gives Jamison "the same gate as the other towns". **No Search Console
   reading for Jamison exists anywhere in this repo.** Staging is noindexed,
   and the pilot proves the template. If the gate fails, Jamison folds into
   the hub and its URL 301s there, as the map says.
6. **The promise band carries home's promise, byte for byte**: "We will get
   you back on the road with your vehicle restored to its pre-accident
   condition." It is approved, so no new promise copy is invented.

**One premise corrected.** The brief allowed for stopping "if the crumb/schema
mirror check cannot pass against a pending span". **There is no such check**
(3.60, ruling 3: recorded, not added). The mirror was therefore proved by
probe: the visible crumb reads Home, Areas We Serve, Jamison, and the
BreadcrumbList names read the same, in the same order. The pending span is
not a check failure, because the pending-link inventory scores site-level
notes, not page warnings.

---

#### PART A: THE TEMPLATE

**Section order, top to bottom.** The ids are part of the template: the
variance check reads three of them.

```
 #   id              ground        what it carries
 1   #town-head      ox (.hero.dark.field-ox)
                                   crumb Home / Areas We Serve / [Town]; kicker naming the county;
                                   H1 "Collision Repair for [Town], PA"; a one-sentence lead; the Call button
 2   #proof          white         the service pages' stat band, BYTE FOR BYTE (the audit's constants)
 3   #for-[town]     silver        who the page is for; the served neighbors inside the first 100 words;
                                   the town's township and county as map fact; ends on the section-bottom
                                   ask (Call + Email), the service pages' #intro grammar
 4   #getting-here   panel         the route: one sentence of distance and time, a .numbered list of
                                   named roads and route numbers, the alternative, a link to the map
 5   #fix            silver        the four service pages as a.svc-card; an intro line inside .sec-head
 6   #start          ox            home's promise band, byte for byte (Call + Email)
 7   #faq            silver        the town's own FAQ; the geographic objection FIRST
 8   #nearby         panel         the four nearest sibling pages and the hub, .svc-card, pending until built
```

**The H1 says "for [Town]", never "in [Town]".** The shop is in Southampton,
and "Collision Repair in Jamison" would be the first false sentence on the
page. The live H1 was "Collision Repair Jamison PA".

**H2s.** Every substantive H2 carries the town's name: sections 3, 4, 5 and
7. The pattern H2s are the promise and "Nearby towns we serve", which the
variance check leaves out by section id.

**The fact discipline, for this section and the whole page:**

- **Allowed, because a map can check it:** road names and route numbers;
  the town's township and county; the distance; the drive time from an
  actual routing, recorded with its start point, its engine and its date.
- **Owner-supplied, or ABSENT:** anything a map cannot check, such as
  landmarks' character, local events, or what a town is "known for". None of
  it is invented, and today none of it is on the page.
- **Only the shop's own approved sentences carry claims.** The insurance
  line and the Pennsylvania-law line are the home page's existing text, word
  for word. The service cards restate only their own pages' meta
  descriptions. **No demand claims:** nothing says which repair a town's
  drivers ask for most.
- **The NAP's street rule governs the directions.** The street is "Jaymor
  Rd", never "Jaymor Road" and never "Jaymor Rd." at a sentence's end, both of
  which `audit.py` fails. The number appears only in the full canonical
  form, "995 Jaymor Rd, Southampton, PA 18966".

**The routing method, for every town:**

- **Start** at the town's OpenStreetMap place point (node or boundary), and
  record its id and coordinates.
- **End** at the shop's verified pin, `GEO_LAT` and `GEO_LON`.
- **Engine:** OSRM driving, alternatives on. Print the primary route's
  roads, route numbers and distances from its steps, and its bearings for
  every compass word.
- **Print** "about N miles and about M minutes without traffic". The time is
  free-flow and is flagged for the owner.

**The nearby rule, for every town:** the four sibling town pages nearest by
straight line from the town's place point, and the hub. It is computed, not
chosen, and the distances are recorded.

**The FAQ rule, for every town:**

- The town's name is in every question.
- **The first question is always "Is Tri-County Collision actually in
  [Town]?"** Its first sentence is the whole truth: not in [Town], in
  Southampton, the true distance and time.
- Then comes the Pennsylvania right-to-choose sentence, word for word, with
  a link to the post.
- Every opener passes the standalone test, and the visible text and the
  FAQPage node are generated from the same strings, so the mirror law holds
  by construction.

**Schema, for every town page:**

- the full AutoBodyShop node under the shared `@id`, byte-identical to every
  other page's;
- a WebPage;
- a Service whose `areaServed` is one `City` naming the town, contained in its
  county's `@id` node;
- a BreadcrumbList mirroring the crumb, with the hub's absolute production
  URL even while the hub is pending;
- the FAQPage.

**No per-town geo:** the town is where the reader is, not where the shop is.
**No review or rating markup.**

**Mechanics:**

- **The kind `town`, declared in the head, exempt from nothing:**
  `RUBRIC_EXEMPTIONS["town"] = ()`, written out. Section 19 now pins four
  ruled kinds and asserts that town's tuple is empty.
- **The variance gate, `check_town_variance_local`,** is a site-level
  critical, compared pairwise across every declared town page and the hub
  (`docs/areas-served/index.html`) when it exists. It is defined below.
- **Old URLs are redirect stubs**: kind `redirect-stub`, an absolute
  canonical, a meta refresh and a visible link, all at the same target, and
  `noindex` while staging. If the production host can answer with a real
  301, that replaces the stub at cutover.
- **Each page is listed in `llms.txt` and `sitemap.xml`,** and each stub is
  absent from both, as `audit.py` requires.
- **Titles to 60 and metas to 160,** machine-counted.

#### The variance measure, proposed and calibrated

The doctrine, rule 7: a town page exists only with "verified variance
against its hub and every sibling (<30% shared vocabulary, no shared
substantive H2s)". Both halves are now a check.

**The H2 half:** no substantive H2 may appear on two town pages, or on a town
page and the hub. The comparison is literal, ignoring case and spacing, with
no masking, because the template puts the town's name in every substantive
H2 on purpose. Empty H2s are skipped, since they are the empty-heading
check's critical.

**The vocabulary half, the exact measure:**

1. Take each page's **substantive text**: everything inside `<main>`
   except pattern text.
2. **Pattern text is defined in `audit.py`, never in markup.** It is any
   `<nav>` (the crumb), the sections `#proof`, `#start` and `#nearby`, and
   `.svc-card` elements. A page cannot mark its own shared prose as pattern,
   because the list is not the page's to write.
3. Lowercase it, and **mask every place name** (`TOWN_PLACE_NAMES`, plus the
   page's own town from its slug) to one token, so a renamed copy reads as
   the copy it is.
4. Cut it into **three-word shingles**, every run of three consecutive words.
5. For a pair, **shared = |A and B| / min(|A|, |B|)**: containment against
   the smaller page, so a short page inside a long one cannot be diluted
   away.
6. **Fail at 30% or more.** The doctrine's line is "under 30".

**Why this measure, measured with the shipped functions, min / median / max:**

```
                             single words (n=1)       three-word phrases (n=3), SHIPPED
our 4 service pages, 6 pairs   46% / 53% / 65%          7% / 8% / 10%
4 migrated posts, 6 pairs      28% / 36% / 42%          1% / 2% / 3%
11 live town pages, 55 pairs   76% / 79% / 87%         56% / 61% / 65%
Jamison vs each service page                            3% to 11%
```

- **Single words cannot carry a 30% line.** Two honest pages about one shop
  share *collision*, *insurance* and *estimate* by necessity, so our own
  genuinely different service pages would fail.
- **Three-word phrases separate the two cases** by a factor of six.

**What this finds, and it matters for run two: the eleven live town pages
are lookalikes by this measure, 56% to 65%.** The page map says to migrate
them faithfully, and this gate will stop that. The H2 half agrees: their
substantive H2s are unique, and they share only pattern headings
("Testimonials", "Get Your Free Estimate Today", "Frequently Asked
Questions"). But their prose is the same pages with the name changed. The
conflict between the map's "migrate faithfully" and rule 7 is **Greg's to
rule on before run two**: open item 1.

**Tests, `test-audit-checks.py` section 25,** 12 checks:

- **The ceiling:** pinned as the doctrine's, `TOWN_SHARED_MAX == 0.30` and
  `TOWN_SHINGLE == 3`.
- **Passes:** two genuinely different pages.
- **Caught:**
  - a copy with only the town's name swapped, written dense in place names,
    so only masking catches it;
  - a short page wholly inside a long one, which only containment catches;
  - a shared substantive H2 over different prose;
  - a town page that copies its hub;
  - a sibling reusing another's H2 (both as criticals through the real check
    on a temp tree).
- **Left alone:**
  - identical pattern text and pattern H2s;
  - an empty H2 on both pages;
  - one town with no hub, which compares nothing and reports a note.
- **On the shipped site:** no variance critical.

**Mutation-tested, in place,** and restored from a copy with the checksum
confirmed (`507e1f0619a6` before and after), run against the final code:

```
mutant                                   red
place-name masking switched off          1: the renamed copy
ceiling raised to 90%                    2: the pin, and the hub copy (which measures 83%)
ceiling raised to 35%                    1: the pin
three-word shingles made single words    3: the pin, and both "genuinely different" and "pattern" cases
pattern sections not excluded            5: pattern H2s count as shared, pattern text as shared phrasing
Jaccard in place of containment          1: the contained page
the H2 half switched off                 2: both shared-H2 cases
```

**The pin was added because of the mutation run.** The first 90% mutant
turned only the hub case red. Its fixture measures 83%, so it caught a 90%
ceiling legitimately, but a ceiling loosened to 80% would have passed every
fixture. The pin closes that.

---

#### PART B: JAMISON

**The route**, OSRM driving, 2026-09-28, from OpenStreetMap node 158375416
(Jamison, `place=village`, 40.2548297, -75.0893372, within about 15m of where
York Road meets Almshouse Road) to the shop's verified pin:

```
PRIMARY   8.42 mi, 14.8 min free-flow
  York Road (PA 263)          south (194 deg)       1.92 mi
  West Bristol Road           southeast (126 deg)   4.09 mi
  Second Street Pike (PA 232) south (177/189 deg)   2.10 mi
  Jaymor Road                 west (281 deg)        0.28 mi
ALTERNATIVE 8.05 mi, 14.9 min free-flow
  York Road (PA 263) 4.61 mi, East County Line Road 2.96 mi, James Way 0.40 mi, Jaymor Road
```

**Other map facts:**

- Jamison is in Warwick Township, Bucks County (OSM).
- **Sibling pages by straight line from the Jamison point:** Warminster
  3.36 mi, Richboro 5.05, Horsham 5.54, Hatboro 5.62. Next are Willow Grove
  7.33 and Feasterville 7.74.
- **Rule 7's three checkable local facts:** the township and county; the
  crossroads the town sits on; the route with its distance and time. All
  three are map facts. No owner-supplied fact exists yet.

**The pairs.** The live page is the source being rebuilt. It carried no
directions, no FAQ and no local fact, so **no sentence of it survives**:

| Where | Before (live, 2026-09-28) | After | Why |
|---|---|---|---|
| title | Collision Repair Jamison PA \| Tri County Collision | Collision Repair for Jamison, PA \| Tri-County Collision | 55; the NAP's name; "for", not "in" |
| meta | Looking for expert collision repair services at an affordable rate in Jamison, PA? Our skilled ASE/I-CAR® Gold technicians utilize cutting-edge equipment to meticulously restore your vehicle to its pristine pre-accident state. | Tri-County Collision in Southampton repairs cars for Jamison, PA drivers, about 15 minutes away. Directions from Jamison, free estimates, (215) 322-5350. | 153; the old one ran past 160 and implied the shop is in Jamison |
| H1 | Collision Repair Jamison PA | Collision Repair for Jamison, PA | the shop is not in Jamison |
| kicker | (none) | Bucks County, PA | the county, a map fact |
| lead | (none) | Tri-County Collision is a family-owned body shop in Southampton, about 15 minutes from Jamison. | "family owned" is the footer's existing claim |
| body | "your premier destination for top-notch collision repair services in Jamison, PA" and five paragraphs of generic claims: ASE/I-CAR Gold technicians, state-of-the-art equipment, a Trustindex widget reading 231 reviews | Sections 3 to 8 as built | held, not lost: the certification claims live on the service pages under the owner's review, and the widget's count is the one 4.4 retired |
| §3 | (none) | "This page is for anyone who lives or works in Jamison... we repair cars for drivers from Jamison and from its neighbors Warminster, Richboro and Ivyland." / "Jamison is in Warwick Township, Bucks County, where York Road (PA 263) crosses Almshouse Road..." / "...Estimates are free and there is no obligation." | served neighbors only (ruling 3); map facts; the promise band's sub-line, word for word |
| §4 | (none) | the route, as above | routing |
| §5 | (none) | four cards, each line from its page's meta | no new claim |
| FAQ 1 | (none) | Is Tri-County Collision actually in Jamison? / "Tri-County Collision is not in Jamison: the shop is at 995 Jaymor Rd, Southampton, PA 18966, about 8 miles and 15 minutes from Jamison without traffic." + the home page's right-to-choose sentences, word for word | the objection, whole truth first |
| FAQ 2 | (none) | How do I get to Tri-County Collision from Jamison? / the route in one sentence | routing |
| FAQ 3 | (none) | Does Tri-County Collision work with my insurance company if I live in Jamison? / "...works with all major insurance companies..." | the home page's claim |
| FAQ 4 | (none) | When is Tri-County Collision open for Jamison drivers? / the hours constants | constants |

**The redirects**, per the page map's Jamison row:

```
docs/body-shop-jamison/index.html              stub -> ../areas-served-collision-repair-jamison-pa/   100/100
docs/paintless-dent-repair-jamison/index.html  stub -> ../areas-served-collision-repair-jamison-pa/   100/100
```

The live site already sends both there. Neither is in the sitemap or
`llms.txt`.

**CSS: one rule, restamped** (`site.css ?v=46eadd5b`):
`.numbered + p { margin-top: 1.1em; }`. `.numbered` zeroes its own margin,
which is right when a CTA row follows, as on `/collision-repair/`, and wrong
when prose carries on beneath the list. The Jamison directions were the
only such case, found on the render with the second route flush against
step 4. Grepped first: it reaches that one list.

**Two changes made on the render, both recorded:**

- **The "What we fix" intro line moved into `.sec-head`**, `/contact-us/`'s
  precedent. In the prose column it began at x=404 while the cards began at
  x=160.
- **The opening section ends on a section-bottom ask**, the service pages'
  `#intro` grammar. As first built, the page ran **3,016px at 390** from the
  header's call to the promise band's, longer than any service page.
  Moving the promise band before "What we fix" was measured too: its
  longest run is 2,510, and it only moves the hole to after the band. The
  section-bottom ask keeps the brief's order exactly:

```
ask at 390          top    gap
header call          401
#for-jamison        1677   1214
#start              3643   1904    <- longest run: 1904 (service pages 1634 to 2684)
footer              5428   1723
```

#### Measured

**The fold, iframe equal to the viewport.** The call bar starts at 604 on
390x664 and at 580 on 360x640:

```
390x664 cutover  innerHeight 664  nav 0-68  ox header 68-511  H1 181-262 (2 lines)  lead 280-375 (3 lines)
                 CALL 401-463, clears the call bar by 141; trust band from 511, first figure 567-611 in full
390x664 banner   innerHeight 664  ox header 125-568  CALL 458-520, clears by 84
360x640 cutover  innerHeight 640  CALL 401-463, clears by 117
360x640 banner   innerHeight 640  CALL 458-520, clears by 60
1440x900         innerHeight 900  ox header 96-576, H1 on one line, CALL 426-488
```

**The first screen at 390x664, cutover.** The ink nav takes 0 to 68. **The ox
header fits whole, 68 to 511, 443px**: crumb, kicker, a two-line H1, a
three-line lead, and the Call button 141px above the call bar. The white
trust band starts at 511, and its first figure, "Lifetime", is fully on
screen. A reader sees whose page it is, where the shop really is, and how
to call, before scrolling.

**Nothing else moved.** Layout hash of every element: all 23 existing pages
at 1440, 390 and 360 are **identical to 3.61, 69 of 69 page-widths**. The new
CSS rule reaches only the new page.

**Every visible tone is an existing pair on an existing ground**: the ox
header is the blog's and contact's, measured in 3.61; the trust band, the
panels and the promise band are the service pages'. No new colour pair was
introduced.

**Rendered and inspected at 1440 and 390**, top to bottom, whole page.

**The suite:**

- Both test scripts pass, 177 checks, with sections 19, 20, 22 and 24
  touched and section 25 new.
- **The shipped-page sweeps now leave out declared special kinds.** Sections
  20, 22 and 24 glob every `index.html`, and the first stubs made them count
  26. A stub has no hours, geo or headings by design, and `audit.py` already
  scores it on its own rubric. Only a declared special kind is excluded, so
  a real page that forgot its markup is still swept.
- `stamp-assets.py --check` exits 0 (27 files), and `build-sitemap.py
  --check` exits 0 (24 pages; Jamison `lastmod` 2026-09-28 from its own
  `dateModified`).
- `STAGING=1 audit.py --strict`: **24 pages at 95, sameAs the only warning
  on each; 2 redirect stubs at 100; zero criticals; 483 passing.** The town
  variance gate reports one town and no hub, so nothing to compare. It exits
  1 on the sameAs bar, as every run has.
- No em dash was added to any file.

#### Open, for Greg, ranked

1. **Run two's conflict: the live town pages fail the variance gate.** They
   share 56% to 65% of their phrasing with each other against a line under
   30%. "Migrate faithfully" and rule 7 cannot both hold for them. The
   choices are to rewrite each to the template, to migrate and fold the
   weakest into the hub, or to rule that the gate applies only to rebuilt
   pages. The gate as built applies to all of them.
2. **The Search Console gate for Jamison**, and for every town: read before
   cutover.
3. **The business node's `areaServed` does not list Jamison.** It is the
   same 15 places on all 24 pages, and adding Jamison changes all 24. That
   belongs with the hub, which the page map already says gains Jamison in
   its county lists.
4. **CLAUDE.md's line that "area served" is still tokenized** is out of
   date: every page's business node carries it. It was not edited here.

### 3.63 Jamison round two: chips, the drawn map, the pairs, a centred opening. TEMPLATE AMENDMENTS. BUILT 2026-09-28

**Every item here amends the town template in 3.62, not just the Jamison
page.** Run two's eleven pages inherit each amendment exactly as written
under "The template, amended". One commit, one restamp (`site.css
?v=27fb8dc4`).

#### Greg's rulings, 2026-09-28, after the build stopped three times

1. **Chips: the service heroes' standard set, with their phone grammar.**
   The brief said home carries a chip row. **It does not, and the correction
   is recorded here.** Home's hero is eyebrow, H1, lead and Call/Email. The
   vetted chip row lives on the service heroes, and that is what the town
   template adopts: the collision/glass/dent set, not commercial's variant,
   because a town page speaks to every driver. In the header from 600px up;
   below that, in the strip after the header. **Option (b), chips in the
   header at every width, was not attempted:** 210px of chips against 141px
   of spare at 390 is arithmetic, not a judgement.
2. **The map: the primary route only, every road named or shielded.** The
   reason, in Greg's words: **this map is a directions DIAGRAM, not
   cartography for its own sake.** It shows exactly what the page's four
   numbered steps say, and the alternative route lives in prose, where it
   already is. A road drawn as the way through but left unnamed, as option
   A's County Line Road was, fails the diagram's own standard. **This is the
   template rule for run two: each town's map draws its page's primary
   route, so the steps and the map mirror each other.**
3. **The pairs go after the promise band, closing on the Call/Email row
   home's pairs already end on.** It was the only measured placement inside
   the site's range, and it adds no new copy: the ask is one the site
   already vetted.
4. **The opening is Greg's copy, verbatim, centred** (from the 3.63 brief).
   The old first sentence was also a T1 violation, copy about the copy.

---

#### The template, amended

The 3.62 section order becomes:

```
 #   id              ground   CHANGE IN 3.63
 1   #town-head      ox       + the chip row (.badges) after the Call button, shown from 600px up
 1a  .proofstrip     silver   NEW: the same four chips, shown below 600px only (the service pages' own grammar)
 2   #proof          white
 3   #for-[town]     silver   CENTRED: .prose style="text-align:center", the 3.52 intro shape; per-town prose
 4   #getting-here   panel    + the map: .split, steps left, figure.split-media.map-box right, ODbL credit
 5   #fix            silver
 6   #start          ox
 6a  #real-repairs   silver   NEW: three of home's five pairs, byte for byte, closing on home's own ask
 7   #faq            silver
 8   #nearby         panel
```

**A1, the chips.** Lift both lists from `/collision-repair/` byte for byte,
never retype them. They are the standard four: Free estimates, Insurance
paperwork handled, ASE and I-CAR Gold Class certified, Detailed after every
repair. They are pattern text.

**A2, the map.** Draw it with `scripts/prepare-map-image.py --frame [town]`
from one Overpass query and the town's recorded OSRM routing, both cached
outside the repo. **The primary route only.** Build order: the page first,
then the map, which draws between the page's `MAP:BEGIN`/`MAP:END` markers.
Rebuilding the page empties them. A frame entry in `FRAMES` names the
page, the viewBox, the scale, the centre, the query box and the town's
corner.

**A3, the pairs.** Three of home's five, chosen for visual variety, with
captions byte-identical. The section sits after the promise band and
closes on home's own Call/Email row. The cars are the shop's real work,
and the section makes no claim they came from the town. They are pattern
text.

**A4, the opening.** The SHAPE is the template's: centred; the served
neighbors in the first sentence; "not in [town]" said plainly; the town's
corner as a map fact; the distance, and the drive time **with its "without
traffic" qualifier, which is load-bearing**; and the section-bottom ask.
**The PROSE is per-town: run two writes each town's own opening to this
pattern, does not reuse these sentences, and the variance gate holds them
apart.**

---

#### A4, the opening: the pair

| Before (3.62) | After (3.63, Greg's copy) |
|---|---|
| This page is for anyone who lives or works in Jamison and needs a car fixed after an accident. We are not in Jamison, and we won't pretend to be: Tri-County Collision is a family-owned shop in Southampton, and we repair cars for drivers from Jamison and from its neighbors Warminster, Richboro and Ivyland. | Tri-County Collision is a family-owned body shop in Southampton, and we fix cars for drivers from Jamison, Warminster, Richboro and Ivyland. We are not in Jamison, and we won't pretend to be. We are about 8 miles down the road. |
| Jamison is in Warwick Township, Bucks County, where York Road (PA 263) crosses Almshouse Road. From there the shop is about 8 miles away by road, and about 15 minutes without traffic. | Jamison sits in Warwick Township, where York Road (PA 263) meets Almshouse Road. From that corner to our shop is about 15 minutes without traffic. |
| If your car has been in an accident, call before you decide where it goes. Estimates are free and there is no obligation. | (unchanged) |

**Every fact survives:** 8 miles; 15 minutes "without traffic"; the served
cluster; the township. "Bucks County" left this paragraph and stays in the
header's kicker. The section is centred by the 3.52 markup, and the Call/Email
row centres beneath it by the existing `.prose + .cta-row` rule.

#### A1, the chips

**Placed by the service grammar.** The header's `ul.badges` follows the
Call row; the `section.proofstrip`, with the same four chips, follows the
header. Exactly one list renders at any width: `.proofstrip` hides at 600px
and up, and the header's list hides below 600px.

**CSS: the four existing chip rules name `.hero.field-ox` beside `.heroB`,**
so there is one source and not a copy. They cover the margin, the outlined
pill, the icon and the phone hide. The scrim cap (`.heroB .badges {
max-width: 620px }`) does not apply: it exists to keep chips over a
photograph inside the scrim's strong zone, and the ox header has no
photograph. **Contact's and the blog's ox headers carry no chips, so the
rules reach only this page.**

**Measured on the ox ground, at the gradient's brightest stop, the worst
case:**

```
chip text and icons, --silver           10.50   (12.39 on --ox-dk, 13.68 at the deep end)
chip hairline, --silver at .55           4.17   (4.65, 5.02)   against 3:1 for a shape
```

#### A2, the map

**`scripts/prepare-map-image.py` now draws frames.** The "contact" frame is
the original and draws exactly what it always drew: **redrawn from its own
2026-09-24 Overpass cache, it is byte-identical to the SVG shipped on
`/contact-us/`** (22,210 bytes). That was re-proved after every change
below.

**The Jamison frame:**

```
viewBox 360 x 480 (portrait: the town and the shop lie nearly north and south), 24 m a unit,
centre 40.2104 -75.0703, frame 8,640 m x 11,520 m; type scaled to the frame (labels 11,
shields 10, pin name 12.5 units) so it renders at the contact map's size, about 16px at 1440
and 11px on a phone; road widths x 0.42
```

**The refusal rules.** The script draws from verified constants and data,
or it draws nothing:

- **The pin** must lie inside an OSM building footprint, as before. It lies
  in way 902318081.
- **New, the corner:** the town's corner must be a point the two named
  roads share in the data, within 60 m of the town's recorded place point.
  York Road meets Almshouse Road at 40.2548692, -75.0891801, **14 m from
  Jamison's recorded point.**
- **New, the route:** it must start within 60 m of the corner and end within
  60 m of the pin. It starts 8 m from the corner and ends 22 m from the pin.

**How it was drawn, and what each failed draft taught.** Recorded because
run two will meet the same things:

1. **The contact frame's settings at a wider scale were unreadable.** Every
   road was as wide as every other, there was no route, and PA 332 got a
   shield while PA 263 and PA 232 were refused. **Fix:** widths scaled to
   the frame; the route drawn with the major casing and everything else as
   quiet context. **No new colour:** the pin stays the map's one oxblood
   mark, and the corner is an ink ring with a silver core (`.map-corner`,
   the one new map class).
2. **OSM renames a road as it goes.** West Bristol Road becomes East
   Bristol Road at -75.066; York Road has North and South pieces; the Pike
   has three spellings. **A typed list of road names was wrong in exactly
   the places a driver turns. Fix: the ROUTING decides.** An OSM way is on
   the route when it runs along the recorded OSRM geometry, and its own
   names and route numbers are the labels and shields.
3. **Crossing roads were caught as on-route at junctions.** **Fix:** a way
   counts only where its segments run PARALLEL to the route (within 30
   degrees) for at least 15 m, and for half its length or 150 m. A road
   that crosses counts for nothing, however close it passes.
4. **A road that OSM splits at every junction never joined into a stretch
   long enough for a name.** **Fix:** the join tolerance scales with the
   frame (2 units here, about 48 m; 0.5 on contact, unchanged), so it is
   about the same distance on the ground.
5. **With both routes drawn, County Line Road could not be named** at this
   scale. Greg ruled option B, the primary route only.

**As shipped:**

- **Named:** York Rd, W Bristol Rd, E Bristol Rd.
- **Shielded:** PA 263 (York Road) and PA 232 (Second Street Pike).
- **Unlabeled: Jaymor Rd, 23 units long against a 51-unit name.** The pin's
  own label, "Tri-County Collision", marks the destination.

**The alt text is the route, in driving order**, from the routing's steps:
"Map of the drive from Jamison, at York Rd and Almshouse Rd, by York Rd (PA
263), W Bristol Rd, Second Street Pike (PA 232) and Jaymor Rd to
Tri-County Collision in Southampton. Opens directions in Google Maps."
**The first draft ended "...and Jaymor Rd."**, and `audit.py` failed the
page as a critical: that is the second-address spelling. The sentence now
ends on the shop's name, so no town's route can put a street before a full
stop. **The NAP check caught its first real slip.**

**The weight, seen and not missed: 120,119 bytes of inline SVG against
contact's 22,210.** It is text and compresses well, and a future sitting
that wants it smaller can drop the context roads outside the route's
corridor.

**Layout.** `#getting-here` is now a `.split`, the contact page's own grid.
A new rule keeps the steps one column inside it at 900px and up:
`.split .numbered { grid-template-columns: 1fr }`. Grepped first: the town
page's directions are the only `.numbered` inside a `.split`.

#### A3, the pairs

**The three, for variety:**

- the **Dodge Grand Caravan** (a minivan's front end);
- the **Mercedes CLE 300** (a coupe's rear end);
- the **Nissan Murano** (an SUV's door dents).

**Left out:** the BMW 5 Series (a second front end) and the Jeep Grand
Cherokee L (its caption carries the mid-repair caveat). The figures are
lifted from home byte for byte, with the image path gaining `../`. All three
captions compare byte-identical to home's. All six files exist and match
their declared sizes, and all carry home's `loading="lazy"`.

**The ask rhythm at 390, as measured to decide the placement:**

```
placement                                          longest run
before the promise band, as briefed                   3,781
after the band, no ask                                3,600
before the band, with home's ask                      3,501
after the band, with home's ask   (RULED)             1,979
```

**As shipped, with the map in the page:**

```
ask at 390          top    gap
header call          401
#for-jamison        1848   1385
#start              4360   2450    <- longest run: 2,450, inside the site's 1,634 to 2,684
#real-repairs       6401   1979
footer              8186   1723
```

**The longest run is 2,450, not the 1,979 quoted to Greg.** The map, which
landed after that measurement, stacks under the steps on a phone and added
about 550 px to the directions section. It is still inside the range.

#### The variance gate, amended

`TOWN_PATTERN_SECTIONS` gains **"real-repairs"** and `TOWN_PATTERN_CLASSES`
gains **"badges"**. Both are in code, never in markup. The chip class
covers both lists; the strip holds nothing else.

**Section 25 gains two fixtures, both directions, 14 checks now:**

- **Left alone:** two town pages carrying identical chip rows and identical
  pairs. The chip row sits inside the header, a substantive section, so
  only its class keeps it out. The pairs carry their own "Real Repairs"
  H2, so only their id keeps it from the H2 half.
- **Caught:** the same two pages with the same prose OUTSIDE the chips and
  pairs.

**Mutation-tested, all nine against the final code,** restored from a copy
with the checksum confirmed (`fa7d7ebfb10f` before and after):

```
place-name masking off                 1 red     ceiling to 35%                   1 red
single-word shingles                   4 red     pattern sections not excluded    6 red
3.63: "real-repairs" dropped           1 red     3.63: "badges" dropped           1 red
Jaccard for containment                1 red     the H2 half off                  2 red
```

#### Measured

**The fold, iframe equal to the viewport:**

```
390x664 cutover  innerHeight 664  ox header 68-511, CALL 401-463, clears the call bar by 141 (unchanged: chips hidden below 600)
                                  the chip strip 511-737, the trust band from 737
390x664 banner   innerHeight 664  CALL clears by 84
360x640 cutover  innerHeight 640  CALL clears by 117      360x640 banner  clears by 60
600x800          innerHeight 800  chips in the header; header 531px; strip hidden
1440x900         innerHeight 900  chips in the header; header 96-641 (545px, was 480)
```

**The first screen at 390x664, cutover.** The ink nav takes 0 to 68. The ox
header fits whole, 68 to 511: crumb, kicker, a two-line H1, a three-line
lead, and Call, 141 px above the bar. **The chip strip begins at 511: its
first chip, "Free estimates", is on screen whole, and the second is cut by
the call bar at 604.** In 3.62 the trust
band's first figure was on screen there; it now starts at 737.

**Nothing else moved:** all 23 other pages are **identical to 3.62, 69 of
69 page-widths**. The stub files are byte-unchanged in git. Their probe
readings vary, because their 0-second refresh fires mid-probe, so they are
recorded by their bytes and not by a layout hash.

**Rendered and inspected, 1440 and 390, whole page**: the header with chips
at 1440, the strip at 390, the map beside the steps at 1440 and under them
at 390, and the pairs.

**The pairs' grey boxes in a single tall headless render are lazy-loading,
not missing images.** A viewport-sized render scrolled to them shows the
photographs.

#### The suite

- Both test scripts pass, **179 checks**.
- `stamp-assets.py --check` exits 0 (27 files), and `build-sitemap.py
  --check` exits 0 (24 pages).
- `STAGING=1 audit.py --strict`: **24 pages at 95, sameAs the only warning
  on each; 2 stubs at 100; zero criticals; 483 passing.** The variance gate
  reports one town and no hub. It exits 1 on the sameAs bar, as every run
  has.
- No em dash was added.

#### Found, not changed

- **"There is a map on our contact page"** ends the directions' prose, and
  now sits beside a map on this page. It is approved copy and this brief
  changed only the opening, so it stands. **Proposed pair for Greg:** drop
  the sentence, or change it to "The map opens directions in Google Maps."
- **Step 2 says "follow it for about 4 miles".** OSM renames the road from
  West Bristol Road to East Bristol Road partway along, and the map labels
  both. "Follow it" is true; the rename is noted in case a reader looks for
  a sign that says West.

### 3.64 The case for the trip: "Why drivers pass closer shops". TEMPLATE AMENDMENT. BUILT 2026-09-28

A new band joins the town template directly after the opening, and the
opening gives up its own ask to it. **Run two's eleven pages inherit all of
it:** the band, byte-identical, on silver, closing on its ask; and no
separate opening ask. One commit. No CSS changed, so there was no restamp;
`stamp-assets.py --check` confirms it.

**Why the band exists.** A town-page reader always has closer options. The
3.63 opening conceded the distance honestly without arguing that the trip
is worth it. This band is the argument, placed where it lands while the
objection is forming. **Greg approved the copy on 2026-09-28 as
fact-checker of record, including the customer-behaviour claim in its
second paragraph.**

#### Greg's rulings, 2026-09-28, after the build stopped twice

1. **The opening's section-bottom ask is dropped; the band's ask replaces
   it.** In Greg's words, **the opening's ask was scaffolding.** 3.62 added
   it for one reason, a 3,016px askless run, and the band solves that
   problem with an ask its own copy argues for. **An ask added for rhythm
   yields to an ask with a reason.** Two identical Call/Email rows 668px
   apart would read as nagging, which is exactly what the range's floor
   exists to prevent. All four measured runs land in range.
2. **The band takes silver, sharing the opening's ground, and nothing else
   moves.** Strict alternation is a means, not a law. The separation it buys
   is already delivered by the band's `.sec-head` and its own spacing.
   **The precedent it leans on:** `/paintless-dent-repair/`'s
   `#real-repairs` and `#what-pdr-can-fix` are two silver neighbours
   already. Alternating would have re-decided two sections Greg approved by
   eye in the pilot, which is churn in service of a rule that was never
   written down.

#### The band, `#why-the-trip`

The copy is Greg's, verbatim, except the brief's instruction on its two
spaced hyphens. **Both introduce what follows, so they are recast as colons,
the house style's form** (the FAQ answers use it: "...is not in Jamison: the
shop is..."):

| The brief | As shipped |
|---|---|
| Everything between them is on us - the estimate, ... | Everything between them is on us: the estimate, ... |
| Call first - the estimate is free, ... | Call first: the estimate is free, ... |

- **The link** is on "the choice of shop is yours", to
  `/your-right-to-choose-a-body-shop/`, the page that proves it.
- **"12 brands" is `BRAND_COUNT`'s count, in the digit form.** The brand
  check reads it as 12, and it agrees everywhere: 3 strips of marks, **14**
  text mentions (was 13) and 1 in the schema, all saying 12. **It adds no new
  rendering.** "12" is the site's majority form. The site has carried four
  renderings since before this band ("12", "12+", "a dozen", "Twelve", in
  4.1's claims question), and the band uses the first.
- **It closes on the Call/Email row**, the section-bottom ask grammar, and
  centres by the existing `.prose + .cta-row` rule, on silver. It is not a
  promise band and takes no ox.
- **It is pattern text, by design.** The reasons do not change by town, and
  per-town paraphrases of one argument would be fake variance. It is
  byte-identical on every town page.

#### The pairs

| Where | Before | After |
|---|---|---|
| #for-jamison | the Call/Email section-bottom ask (3.62) | removed, ruling 1; the band's ask replaces it |
| (new) #why-the-trip | (none) | the band, as above |
| #getting-here | ...takes about the same time. There is a map on our contact page. | ...takes about the same time. |

**3.63's two leftovers are closed:**

- **(a) "There is a map on our contact page" is dropped**, approved by Greg:
  the map now sits beside it, and a page should not point at another page's
  map while showing its own.
- **(b) Step 2's "West Bristol Road" STANDS**, considered and kept, per
  Greg. The sign at the turn reads West Bristol, and the map labels both
  names where OSM renames the road.

#### The variance gate, amended

`TOWN_PATTERN_SECTIONS` gains **"why-the-trip"**. It lives in code, never in
markup.

**Section 25 gains two fixtures, 16 checks now:**

- **Left alone:** an identical band on two town pages. The band carries its
  own H2, so only its id keeps it from the H2 half as well as from the
  phrase measure.
- **Caught:** the same pages with shared prose OUTSIDE the band.

**Mutation-tested, ten mutants against the final code,** restored from a
copy with the checksum confirmed (`70b4d3c9e2ba` before and after):

```
3.64: "why-the-trip" dropped    1 red     3.63: "real-repairs" dropped    1 red
3.63: "badges" dropped          1 red     pattern sections not excluded   7 red
place-name masking off          1 red     ceiling to 35%                  1 red
single-word shingles            5 red     Jaccard for containment         1 red
the H2 half off                 2 red
```

#### Measured

**The ask rhythm at 390, every run, with the ruling applied:**

```
header call        ->  #why-the-trip ask     1,951    in range
#why-the-trip ask  ->  #start                2,422    in range  (the longest)
#start             ->  #real-repairs ask     1,979    in range
#real-repairs ask  ->  footer                1,723    in range
footer's own links                        426, 171    the footer's contact list, as on every page
```

**Every run between in-page asks is inside the site's 1,634 to 2,684.** With
both asks kept, the sequence was 1,385, **668**, 2,422, 1,979 and 1,723. The
668 was the two rows the ruling removed, and the 1,385 is the run the
opening's ask had shortened.

**The fold, iframe equal to the viewport:** unchanged, because the band
sits below the first screen.

```
390x664 cutover  innerHeight 664  CALL 401-463, clears the call bar by 141
390x664 banner   innerHeight 664  clears by 84
360x640 cutover  innerHeight 640  clears by 117      360x640 banner  clears by 60
```

**Rendered and inspected at 1440 and 390:** the opening without its ask; the
band on the same silver, set apart by its heading and spacing; the band's ask
centred under its prose; and the directions without the pointer to the
contact page.

**Nothing else moved:** the Jamison page, `audit.py` and the test file are
the only files this commit touches. No stylesheet or script changed, so the
other 23 pages are identical by construction.

#### The suite

- Both test scripts pass, **181 checks**.
- `stamp-assets.py --check` exits 0 (no CSS changed), and
  `build-sitemap.py --check` exits 0 (24 pages).
- `STAGING=1 audit.py --strict`: **24 pages at 95, sameAs the only warning
  on each; 2 stubs at 100; zero criticals; 483 passing.** It exits 1 on the
  sameAs bar, as every run has.
- No em dash was added.

### 3.65 The directions card, and directions that cannot drift. TEMPLATE AMENDMENT, and one contact-page change. BUILT 2026-09-28

**The directions section becomes a card, on the town pages and on
`/contact-us/`, and every route fact on a town page becomes a derivation of
one recorded routing, machine-checked.** Run two's eleven town pages inherit
the card with their own routed facts, and their own recorded routing in
`TOWN_ROUTES`. One commit, one restamp.

#### Greg's rulings, 2026-09-28

1. **The card:** map on top with a visible "Open in Google Maps" button, a
   routed drive-time chip, the address prominent, the numbered steps
   beneath, and the Call button closing it. The Ambler page's assembly,
   ours.
2. **The split:** contact carries Google's interactive embed inside its card;
   the twelve town pages carry the drawn route maps inside theirs.
3. **Accuracy is a gate, not a goal.** Every route fact on a page derives
   from one recorded routing and is machine-checked against it.

**Asked and ruled while building:**

4. **The label gate is judged against the roads DRIVEN, not the step names
   alone.** The drive genuinely runs along what OpenStreetMap calls East
   Bristol Road for half its length. A driver mid-leg is looking at E
   Bristol Rd signs, and a map that hid the name to satisfy a strictly read
   gate would be less accurate, not more. 3.64's labels-both premise stands,
   and the gate still refuses any label off the route, which is all it was
   ever for.
5. **The embed is centred on the verified pin by coordinates, from `GEO_LAT`
   and `GEO_LON`, never by the business's name.** A name-based embed would
   have rendered the Business Profile's card, carrying its unresolved name
   "Tri County Collision Center" and the unconfirmed (215) 999-3497, onto
   the contact page itself, from Google's side, where no check of ours can
   reach. That is the exact conflict rule 6 exists to prevent, injected by
   the embed rather than by our source. **Measured before the choice:** the
   name-query embed's response carries "Tri County Collision Center" twice
   and "999-3497" once; the coordinate embed carries neither. Owner question
   29a records the cost.
6. **Three readings, approved as read:**
   - compass words ("south") are checked against the maneuver's bearing,
     and turn words against its modifier, since OSRM has no compass
     modifier and step 1 begins at the corner facing the way;
   - step distances are route facts under the mandate;
   - contact's card keeps its address, phone, email and the 3.55 hours box
     inside it, with the embed on top and Call closing it.
7. **THE RANGE IS TWO RULES, NOT ONE.** The card's Call landed 1,120px
   before the promise band, below the floor, and 3.66's order adds a 1,431
   run. Greg named the distinction precisely so it cannot stretch:
   - **THE CEILING, 2,684, counts every call to action of any kind.** No
     reader scrolls that far without a way to act, and any call satisfies it.
   - **THE FLOOR, 1,634, governs REPEATED SECTION ASKS ONLY:** the things
     that read as the page asking again.
     - **Section asks, which the floor governs:** identical Call/Email rows
       (the opening's in 3.62, the band's, home's pairs' ask) and the
       promise band's ask.
     - **Furniture, which the floor does NOT govern:** a call embedded in a
       content unit as part of its function. That is the directions card's
       Call, the header's Call, the phone call bar, and the footer's contact
       links. The footer's links have sat 426 and 171px apart on every page
       since the footer shipped, and nobody ever read them as nagging,
       because they are furniture.
     - **This is 3.64's floor reasoning, restated.** Identical rows 668px
       apart read as nagging. **Furniture is never an excuse for stacking
       section asks:** a Call/Email row is a section ask wherever it sits,
       and a promise band is always one.
8. **The embed ships; Greg checks it in his real browser the moment it
   lands,** for a marker at the shop and any Business Profile label near
   the pin. **The fallback is pre-ruled:** if a real browser shows no
   marker, the builder proposes the keyless embed forms that DO draw a
   marker without bringing the Profile's card, renders what it can, and
   Greg picks by eye. **A map on the contact page must mark the shop,** so a
   confirmed markerless embed is a defect to fix, not a trade to accept.
9. **The ritual's expected line becomes "23 pages at 95, Jamison at 96, 2
   stubs at 100"** until sameAs closes the gap. Jamison reads 96 because
   the routing check adds a passing check to its denominator: it is 22 of
   23 with sameAs its one warning, and exactly as clean.

#### Item 1: the card, on Jamison

`#getting-here`, on the white panel. It holds a `.dir-card` (white, the
site's hairline and radius, 520px at most, one column at every width), with
these parts in order:

- **The drawn route map**, unchanged, with its ODbL credit.
- **The button, "Open in Google Maps".** It uses the site's canonical maps
  link, character for character. The drawing was already a link, and
  nothing said so; the button says so.
- **The chip, "~15 min from Jamison",** with a clock mark. **The qualifier
  reading, recorded so no future sitting strips the chip:** the tilde hedges
  the number, and the card's own prose two lines below carries the full
  "about 15 minutes without traffic". Together they satisfy the qualifier
  rule.
- **The address**, full canonical form, with the pin mark.
- **The prose, the four numbered steps, and the alternative route**,
  unchanged.
- **Call (215) 322-5350**, closing the card.

**Tones:** all existing pairs. Ink on white is 17.33 (chip text, address);
`--ox` on white is 11.80 (the ghost button, and the chip's and address's
marks as graphics).

| Where | Before (3.64) | After |
|---|---|---|
| #getting-here | a .split, steps left, map right | the card, stacked: map, button and chip, address, prose and steps, Call |
| (new) | nothing named the map a link | "Open in Google Maps" button |
| (new) | (none) | "~15 min from Jamison" chip |
| (new) | (none) | the address line with the pin mark |
| (new) | (none) | the card's closing Call |

#### Item 2: contact's `#find-us`

The same card shape, holding these parts in order:

- **The embed:** Google's keyless share embed (no API key, no account),
  `https://www.google.com/maps?q=40.1660232,-75.0512847&z=15&output=embed`
  from the constants, `loading="lazy"`, a `title` for accessibility, and a
  4:3 frame sized by the card.
- **The same "Open in Google Maps" button.**
- **The address, phone and email lines, and the hours box,** all unchanged.
- **Call, closing it.**

| Where | Before (3.54 to 3.64) | After |
|---|---|---|
| #find-us | a .split: details and hours left, the drawn map right | the card: embed, button, details, hours, Call |
| map | the drawn OSM map, inline SVG | Google's embed, by coordinates |
| credit | the ODbL figcaption | none needed: the embed carries Google's own attribution |

**The drawn contact map is kept** as `scripts/fixtures/contact-map-reference.svg`,
with a README carrying its ODbL credit, outside `docs/` and never served.
`prepare-map-image.py`'s contact frame no longer patches a page: it draws
only to `--out-dir`, and **`--check-against` compares the drawing with the
kept reference byte for byte and exits 1 on any difference.** Run from its
own 2026-09-24 cache, it matches, at 22,210 bytes. The proof that town
frames never disturb the contact frame survives the page no longer
shipping it.

**THE COSTS, as decided, not discovered:**

- **The weight** lands, lazily, on one page only.
- **Google's cookies** arrive with it at cutover, and the privacy page's
  planned disclosures gain the line. It is added to pagemap.md's Privacy
  row, the one place the privacy page's reasons are written.
- **Google decides which nearby businesses its tiles show,** seen and
  accepted for the one page where panning around the shop is the point.

**What a headless render shows, recorded because it changes an
instruction.** A full-page headless render DID paint the embed's tiles. Jaymor
Rd, James Way, Second Street Pike and I-276 sit where the drawn map put them,
with nearby businesses (Robin Hood Restaurant, GIANT, Bucks Lumber) and **no
Business Profile label.** **It also showed no marker at the shop.** Whether a
real browser adds one is Greg's check. If it does not, ruling 8's fallback
applies. **CLAUDE.md's line that headless Chrome "cannot run" the embed was
wrong and is corrected;** the real-browser check stays in the cutover list,
because painted tiles are not what a customer's browser shows.

**A new check makes the embed's centring a mechanism:** any Google Maps
iframe on any page must query exactly `GEO_LAT,GEO_LON`, carry a `title`,
and load lazily. A name query is called out as bringing the Profile's card.

#### Item 3: one routing, every rendering derived

**`TOWN_ROUTES` in `scripts/audit.py`**, beside the NAP, hours and geo
constants. It holds one entry per town, keyed by slug:

- **the whole route:** 8.42 mi, 14.8 min, free-flow;
- **the steps, one per numbered step, in driving order**, each as (road,
  ref, modifier, bearing, miles):
  - York Road, PA 263, right, 194 degrees, 1.92;
  - West Bristol Road, left, 126, 4.09;
  - Second Street Pike, PA 232, right, 177, 2.10;
  - Jaymor Road, right, 281, 0.28;
- **`roads_driven`:** every OSM name the route's ways carry, including
  East Bristol Road and 2nd Street Pike (ruling 4).

The steps drop the 0.00-mile depart, since the page starts at the corner,
and the unnamed final metres into the lot. A "new name" maneuver is not a
turn: 2nd Street Pike's 0.73 folds into Second Street Pike's 1.37.

**The derivations are the only renderings accepted:**

```
minutes         round(14.8) = 15          "about 15 minutes", "~15 min"
route miles     round(8.42) = 8, round(8.42, 1) = 8.4
step miles      under half a mile, to the nearest quarter ("a quarter mile"); otherwise round: "about 2 miles"
turn words      left/right against the maneuver's modifier
compass words   against the maneuver's bearing, eight points (ruling 6)
```

**The check, a critical, on every declared town page:**

- every drive-time and distance figure in the visible page, the meta
  description, the JSON-LD (the FAQ's schema twin), every `aria-label` (the
  map's alt text) and the page's `llms.txt` entry must be a derivation;
- the numbered steps must match the recorded steps in count and order, each
  step's road, route number, turn word, compass word and distance.

**A town page printing drive figures with no recorded routing behind it
fails too.**

**One bug in the first draft, caught by the check's own first run:** it read
the "West" in "West Bristol Road" as a compass word. A direction inside a
road's name is not a direction, so every routing road name is taken out of a
step's text before its turn and compass words are read.

**Tests, section 26, 26 checks, all against the SHIPPED page with exactly one
fact made wrong:**

- **The shipped page passes,** and its `llms.txt` entry is found and read.
- **Caught, in the steps:**
  - a wrong turn word;
  - a wrong compass word;
  - two steps swapped;
  - a step dropped;
  - a wrong route number;
  - a stale step distance;
  - a stale quarter mile;
  - **the wrong road on a step with its turn and distance untouched;**
  - **another step's distance on step 2**, a figure valid elsewhere on the
    route.
- **Caught, in the renderings:**
  - a stale minute count in the lead;
  - a stale minute count in the chip;
  - a stale total distance;
  - a stale meta description;
  - a stale figure in the map's alt text;
  - a stale `llms.txt` entry;
  - a town page with figures and no routing.
- **Left alone:** a post printing a drive time.
- **The embed:** the pin by coordinates passes. Caught: a name query, a pin
  one digit off, no title, eager loading.

**Mutation-tested, fifteen mutants, every one red**, restored from a copy
with the checksum confirmed (`314becf4d085` before and after):

```
turn words 1    compass words 1    road names 1    step count 1    route numbers 1
step distances 1    minute renderings 5    mile renderings 1    llms.txt read 1
aria-labels read 1    road names stripped before compass 1    no-routing pages 1
embed query 2    embed title 1    embed lazy 1
```

**Two mutants survived the first run: road names and step distances.** Every
fixture that should have caught them was also caught by another check. So the
two isolating fixtures (in bold in the list above) were added, and both
mutants now go red. **A check that no fixture can kill on its own is a check
nothing proves.**

#### Item 4: the drawing's own gates

`prepare-map-image.py`'s town frame names its recorded routing (`ROUTE_KEY`).
The existing refusals stay: the pin in its building, the corner a real
junction within 60 m, and the route's ends at the corner and the pin. The
new ones:

- **The routing file must BE the recorded routing:** its distance and time,
  to the recorded figures, or nothing is drawn.
- **Every road the route's OSM ways carry must be in `roads_driven`.**
- **Every label drawn must be a road the recorded routing drives.** It is
  judged against `roads_driven`, per ruling 4.

**Each proven to refuse, by hand** (its data lives outside the repo):

```
(a) the routing file doctored by one minute    "FAILED: this routing file measures 8.42 mi, 15.8 min; the recorded routing ... is 8.42 mi, 14.8 min"
(b) East Bristol Road taken out of roads_driven "FAILED: the route's OSM ways carry ['East Bristol Road'], which ... roads_driven does not"
(c) (b) with the stray-road gate off            "FAILED: the map would label ['East Bristol Road'], which the recorded routing does not drive"
restored, both files to their checksums; the clean run: "all 3 named roads are roads the recorded routing drives"
```

**The cutover checklist gains the re-verification**, in CLAUDE.md: re-fetch
OSM and re-run every town's routing within a week of cutover, update
`TOWN_ROUTES` first, re-derive every rendering, re-draw every map, and view
the contact embed in a real browser.

**Label legibility at phone size, measured.** The Jamison map's labels are
11 units in a 360-unit viewBox. At 390 the card draws the map about 350px
wide, so labels render at about 10.7px, against the contact map's former
11.7px. No label collides, and the 390 render was read by eye: York Rd, W
Bristol Rd, E Bristol Rd, PA 263 and PA 232 are all legible. **It is at the
small edge.** Run two should treat about 10.5px as the floor, and stop
rather than ship below it.

#### Measured

**The ask runs at 390, every one, by category (ruling 7):**

```
header Call (furniture)   -> band's Call/Email row (section ask)    1,951
band's row                -> card's Call (furniture)                1,636
card's Call               -> promise band (section ask)             1,120   furniture: the floor does not govern it
promise band              -> pairs' row (section ask)               1,979
pairs' row                -> footer (furniture)                     1,722
footer's own links                                             426, 171   furniture
section ask to section ask: band row -> promise band 2,818, promise band -> pairs' row 1,979
CEILING: longest run between ANY two calls 1,979     FLOOR: nearest two section asks 1,979
```

**The fold, 390x664, innerHeight 664:** CALL 401 to 463, clearing the call
bar by 141, unchanged. At 360x640 it clears by 117.

**Nothing else moved:** the 22 other pages are **identical to 3.63, 66 of 66
page-widths**. Only Jamison and contact changed; 3.64 touched only Jamison.
The stylesheet's new rules are the `.dir-card` family. The 3.63 `.split
.numbered` rule lost its only user when the steps moved into the card; it
was 3.63's own, so it is repurposed as `.dir-card .numbered` rather than
left standing.

**Rendered and inspected at 1440 and 390:** the Jamison card, and contact's
card with the embed painted. Both read top to bottom as ruled.

#### The suite

- Both test scripts pass, **205 checks**.
- `stamp-assets.py --check` exits 0, and `build-sitemap.py --check` exits 0
  (24 pages).
- `STAGING=1 audit.py --strict`: **23 pages at 95, Jamison at 96, 2 stubs at
  100; sameAs the only warning; zero criticals; 485 passing.**
- No em dash was added.

#### Open, for Greg

1. **VIEW THE CONTACT EMBED IN YOUR REAL BROWSER, NOW:** is there a marker at
   the shop, and is there any Business Profile label near the pin? No
   marker triggers ruling 8's fallback.
2. **Owner question 29a:** fixing the Business Profile's name and phone
   removes the embed's problem at its source.

### 3.66 The argument moves up and takes ox. TEMPLATE AMENDMENT. BUILT 2026-09-28

**Run two inherits all three changes:** the argument above the opening, on
ox, centred. One commit. **The copy changes by zero bytes.** Only order,
ground and alignment move. No stylesheet or script changed, so there was no
restamp.

#### Greg's rulings, 2026-09-28, after seeing 3.64 shipped

1. **ORDER:** "Why drivers pass closer shops" moves ABOVE "For drivers from
   Jamison", directly after the trust band, as the first body section on the
   page. The stat band's numbers flow straight into the argument they
   support, and the opening follows with the who-and-where.
2. **GROUND: the band takes OX. This SUPERSEDES 3.64's silver ruling.** Greg
   saw two silver bands back to back and overruled it; 3.64's text stands,
   struck by nothing, and this is the supersession. **The palette law is
   satisfied on its own terms:** the band ASKS, closing on the Call/Email
   row, so ox is its lawful ground, by the same band test the promise bands
   pass. The page's grounds now run ox header, white trust band, ox
   argument, silver opening, white directions card. **No ground repeats
   adjacently,** which was Greg's complaint.
3. **TEXT:** the band's copy centres, per the 3.52 centred-intro pattern, and
   the existing `.dark .cta-row` rule centres the ask with it.

#### The pairs

| Where | Before (3.64/3.65) | After |
|---|---|---|
| order | trust band, opening, band, directions | trust band, **band**, opening, directions |
| #why-the-trip | `<section id="why-the-trip">` on silver | `<section class="dark field-ox" id="why-the-trip">` |
| its prose | `<div class="prose">`, left | `<div class="prose" style="text-align:center">` |
| the copy | Greg's, verbatim | **unchanged**: the band's visible text hashes identically before and after (`3b73fb0b9c9b`, 597 characters), and its markup differs by the centring attribute only |

**The existing grammar only; no class was invented.** `.dark` and `.field-ox`
are the in-flow act bands' own. `.dark .prose p` gives the paragraphs
`--silver-2`, `.dark a` gives the link `--silver`, and the act-button rule
fills the Call ink with the silver hairline.

#### Every tone on ox, measured

This band is the first to put body PARAGRAPHS and an inline LINK on the ox
gradient; until now the promise bands carried only a headline and a CTA.
Measured on the render, each text node in its own computed colour, against
the ground rendered with the band's text and buttons made transparent. The
figure is **the worst pixel of the gradient**, at 1440 and 390:

```
                          tone        1440     390
H2                        --silver    10.50    10.50
paragraphs                --silver-2   7.34     7.34    (7:1 body target; 7.34 is --silver-2 on --ox exactly)
inline link               --silver    10.50    10.65    underlined
Call button label         --silver    10.50    10.50    against the band; on its own ink fill, 15.42
Call button edge          --silver    10.50    10.50    as a shape against the band, 3:1 floor
Email ghost label         --silver    11.01    10.79
Email ghost edge          --silver    10.93    10.58
```

**The link is told apart from its paragraph by its UNDERLINE, not its
colour:** silver against silver-2 is only 1.43, so the underline carries it,
as the non-colour cue requires. Its focus ring is 3.59's `.dark
a:focus-visible` silver, 10.50 on this ground.

#### Variance: unchanged, and position-independent

The band stays pattern text by its id, and nothing about the exclusion
changes with position or ground. **Section 25's fixtures pass without
edits.** Checked beyond them, and not committed: the identical-band fixture
placed FIRST in `<main>` and LAST, carrying `class="dark field-ox"`,
measures the same 0.06 either way and is left alone, while shared prose
outside it is still caught. **Position in the fixture markup does not
matter,** so there was no finding to record.

#### The ask runs at 390, every one, by 3.65's two rules

```
header Call (furniture)   -> band's Call/Email row (section ask)   1,431   the floor does not govern furniture
band's row                -> card's Call (furniture)               2,174
card's Call               -> promise band (section ask)            1,120   furniture
promise band              -> pairs' row (section ask)              1,979
pairs' row                -> footer (furniture)                    1,722
footer's own links                                            426, 171   furniture
CEILING, the longest run between ANY two calls:   2,174   (under 2,684)
FLOOR, the nearest two SECTION asks:              promise band -> pairs' row 1,979, band's row -> promise band 3,356   (over 1,634)
```

**Both rules hold, as 3.65's ruling predicted.**

**The fold, 390x664, innerHeight 664:** CALL 401 to 463, clearing the call
bar by 141, unchanged, because the band sits below the first screen.
360x640 clears by 117.

**Rendered and inspected at 1440 and 390:** the trust band flowing into the
ox argument, with the copy and the ask centred together, then the silver
opening and the white card. On a phone the silver chip strip sits between
the header and the trust band, as 3.63 placed it.

**Nothing else moved:** the Jamison page is the only file this commit
changes besides this record. With no stylesheet or script changed, the
other pages are identical by construction.

#### The suite

- Both test scripts pass, **205 checks**.
- `stamp-assets.py --check` exits 0 (no CSS changed), and
  `build-sitemap.py --check` exits 0 (24 pages).
- `STAGING=1 audit.py --strict`: **23 pages at 95, Jamison at 96, 2 stubs at
  100; sameAs the only warning; zero criticals; 485 passing.** It exits 1
  on the sameAs bar, as every run has.
- No em dash was added.

### 3.67 One proof section: "Why drivers pass closer shops", as cards. TEMPLATE AMENDMENT. BUILT 2026-09-29

**The town page's three stacked proof moments become one section.** Those
were the header's chip row, the stat band and the ox argument band. Run
two inherits it: the section, the chipless header, and the lists that
follow them. One commit, one restamp.

#### Greg's rulings, 2026-09-29, after seeing 3.66 shipped

1. The header chip row, the stat band and the argument band become ONE
   section, headed "Why drivers pass closer shops", built as cards. **The
   argument band AS CONSTRUCTED is gone;** its heading and its vetted claims
   survive inside the new section.
2. **The chip row leaves the TOWN header,** and the phone strip goes with it.
   Town headers return to crumb, kicker, H1, lead and Call. **A town-template
   call only:** the service pages' heroes and strips are untouched.

**Supersessions, striking nothing.** Each earlier record stands; this is the
supersession:

- **3.63's chips-in-the-town-header**, and its `.hero.field-ox` CSS;
- **the stat band as the town page's white band**, from 3.62;
- **3.64's and 3.66's argument band** as built.

#### The section, `#why-the-trip`

White, directly after the header: the one white band under the ox header.

- **H2:** "Why drivers pass closer shops".
- **Lead**, inside `.sec-head` (contact's `#options` grammar): "A collision
  repair is two drives: one to drop the car off, one to pick it up.
  Everything between them is on us." It is 3.64's approved first paragraph
  cut at "on us."; **Greg approved the new sentence boundary in the 3.67
  brief.**
- **Six cards, in `.grid3`** (one column on a phone, two from 700px, 3x2
  from 1000px). **Every line was already vetted, and nothing is newly
  written:**
  - **1 to 3, the figure cards, are the stat band's three stats, lifted from
    `/collision-repair/`'s band by the builder, byte for byte:** Lifetime /
    Warranty on all repair work / "If anything isn't right, we'll make it
    right."; the `REVIEW_COUNT` figure / Google reviews / the rating and
    counted date; 12 / Vehicle brands, factory-certified / the brand list.
  - **4, Your right to choose:** 3.64's two sentences, with the link still
    on "the choice of shop is yours".
  - **5, Insurance paperwork handled:** a headline card, with no support
    line, by ruling.
  - **6, Free estimates:** 3.64's close, "Call first: the estimate is free,
    and you'll know where you stand before the car goes anywhere."
- **Closing ask:** the Call/Email row, replacing the argument band's,
  centred by the existing section-bottom rule.

**One vetted phrase does not survive, named so it is not lost unnoticed:**
3.64's "a repair done to your manufacturer's own procedures". Greg's six
cards were listed exactly, "nothing newly written", and none carries it. The
factory certification it leaned on survives in card 3.

**THE ODOMETER IS KEPT, a default rather than a ruling.** The section keeps
the `.statband` class, so `site.js` still finds the three figures and they
count on arrival, as they did in the band. That also gives the section its
white ground. The brief was silent on motion; removing one class reverses
this.

#### The pairs

| Where | Before (3.66) | After |
|---|---|---|
| town header | crumb, kicker, H1, lead, Call, **chip row** | crumb, kicker, H1, lead, Call |
| after the header (phone) | `.proofstrip` with the four chips | (gone) |
| white band | `#proof`, the stat band (three stats) | `#why-the-trip`: H2, lead, six cards, Call/Email |
| ox band | `#why-the-trip`: H2, three paragraphs, Call/Email | (merged into the section above) |
| para 1 | "...Everything between them is on us: the estimate, the insurance paperwork, and a repair done to your manufacturer's own procedures by a shop factory-certified for 12 brands." | the lead, cut at "on us."; the list lives as the cards |
| para 2 | "Pennsylvania law says the choice of shop is yours..." | card 4, word for word |
| para 3 | "And you don't have to make the drive to find out. Call first: ..." | card 6 carries "Call first: ..."; its opening sentence is not in Greg's composition |

**The grounds:** ox header, **white proof section**, silver opening, white
directions card, silver "What we fix", ox promise band, silver pairs,
**silver FAQ**, white nearby. **No adjacent repeat in the part this brief
changed.** The silver pairs beside the silver FAQ date from 3.63's
placement, and are recorded here, not changed.

#### CSS: one rule pair added, one set removed

- **Added, `.card-figure`:** it centres the figure cards and sets their
  numeral to `clamp(2.6rem, 4.4vw, 3.6rem)`. At the band's own size,
  "Lifetime" runs about 320px wide into a card about 297px wide inside at
  1440. The line-height stays the band's .88em, which is the step the
  odometer rolls on.
- **Removed, the dead CSS:** 3.63's `.hero.field-ox .badges` extensions,
  from the four chip rules, served only the town header, and nothing wears
  them now. The service heroes' `.heroB .badges` rules are untouched.
  **3.66's `.dark` band tones stay:** contact and the blog still wear the ox
  header, and the promise bands still use the grammar.

#### The variance lists follow the template truthfully

- **`TOWN_PATTERN_SECTIONS` is now `("start", "nearby", "real-repairs",
  "why-the-trip")`:** `"proof"` died with the town stat band, and
  `why-the-trip` now carries the whole merged section.
- **`TOWN_PATTERN_CLASSES` is now `("svc-card",)`:** `"badges"` died with the
  town chip row.

**What ships is listed; what died, died.** A list naming what no town page
carries would excuse text the template no longer ships.

**Section 25, both directions, 19 checks:**

- the base fixture's pattern section is now `why-the-trip`;
- the pairs fixture stands alone ("left alone: identical pairs"), with shared
  prose outside it still caught;
- **new, the dead entries prove they left:** an identical chip row on two
  town pages is COUNTED, and so is an identical `#proof` band;
- **new, `svc-card` finally isolated.**

**Mutation-tested, seven list mutants, every one red**, restored from a
copy (`8b960593ad30` before and after):

```
"proof" re-added        1 red: the #proof band is counted       "badges" re-added     1 red: the chip row is counted
"why-the-trip" dropped  2 red                                   "real-repairs" dropped 1 red
"start" dropped         7 red                                   "nearby" dropped       7 red
"svc-card" dropped      1 red, ONLY after the new fixture
```

**Found by the mutation run, and fixed:** dropping `svc-card` turned nothing
red. The gap dates from 3.62, where the cards' shared text sat beside
several other pattern sections and no fixture isolated the class. The new
fixture, identical service cards alone, closes it.

#### The numbers still find their checks

- **Review count:** agrees everywhere, 274 and 4.9, counted 2026-09-10; the
  staleness warning clock reads it (18 days).
- **Brand count:** agrees everywhere at 12, with 3 strips, **13** text
  mentions (14 before: the band's "12 brands" merged into card 3's "12
  Vehicle brands") and 1 in the schema.
- **Routing:** Jamison's directions still derive from the recorded routing.

#### Measured

**The ask runs at 390, by 3.65's two rules:**

```
header Call (furniture)     -> the section's Call/Email row (section ask)   1,399
section's row               -> card's Call (furniture)                      2,176
card's Call                 -> promise band (section ask)                   1,119
promise band                -> pairs' row (section ask)                     1,979
pairs' row                  -> footer (furniture)                           1,723
footer's own links                                                     426, 170
CEILING, the longest run between ANY two calls:  2,176   (under 2,684)
FLOOR, the nearest two SECTION asks:             promise band -> pairs' row 1,979, section row -> promise band 3,357   (over 1,634)
```

**Both rules hold.**

**The fold, 390x664, innerHeight 664.** The header is unchanged on a phone,
because the chips were already hidden below 600px: crumb, kicker, a two-line
H1, a three-line lead, and CALL at 401 to 463, clearing the call bar by
141. **What now lands above the bar:** the whole ox header, then, from 511,
the white proof section's heading, "Why drivers pass closer" whole, with
"shops" cut by the bar at 604. Before, the silver chip strip sat there.
360x640 clears by 117.

**Nothing else moved:** every other page is **identical to 3.65, 69 of 69
page-widths**, and that includes **all four service pages, whose chips and
stat bands this brief does not touch.** The stubs are byte-unchanged.

**Rendered and inspected at 1440 and 390:** the six cards three across and
stacked, the figures centred and fitting, and the closing ask.

#### The suite

- Both test scripts pass, **208 checks**.
- `stamp-assets.py --check` exits 0, and `build-sitemap.py --check` exits 0
  (24 pages).
- `STAGING=1 audit.py --strict`: **23 pages at 95, Jamison at 96, 2 stubs at
  100; sameAs the only warning; zero criticals; 485 passing.**
- No em dash was added.

### 3.68 The proof section's second row matches the first. TEMPLATE AMENDMENT. BUILT 2026-09-29

**Run two inherits it.** Row two of "Why drivers pass closer shops" now
wears row one's figure-card grammar and carries the three chip claims:
Free estimates, Insurance paperwork handled, Detailed after every repair.
One commit, one restamp.

#### Greg's rulings, 2026-09-29, after seeing 3.67 shipped

1. **Row two becomes, in this order:** Free estimates, Insurance paperwork
   handled, Detailed after every repair. The fourth chip's claim returns to
   the town template as a card.
2. **Row two takes row one's treatment:** a big ox word, a bold label, and a
   support line where one exists. Greg's complaint was that the second row
   read all black against the first row's ox figures. **Wording may be
   adjusted to fit the grammar, by Greg's permission, recorded here, but only
   by SPLITTING vetted claims, never by writing new ones.**
3. **The "Your right to choose" card is DROPPED from this section.** It was
   Greg's explicit call, with the alternative offered and declined. **It is a
   move, not a loss:** the claim and its link survive in the page's own FAQ.
   The answer to "Is Tri-County Collision actually in Jamison?" carries
   "Pennsylvania law protects your right to choose your own collision shop
   for repairs." and links "your right to choose a body shop" to
   `/your-right-to-choose-a-body-shop/`. Both were confirmed present at this
   commit.
4. **The OEM-procedures phrase stays dropped,** Greg's explicit call,
   recorded the same way: the claim lives on in the service pages' copy.
   **Precisely: on `/collision-repair/`**, as "direct access to manufacturer
   repair procedures, tooling, and specifications". That is the claim, not
   3.64's exact words, and no other service page carries it.

**Supersession, striking nothing:** 3.67's row-two composition. 3.67's record
stands.

#### The pairs

| Card | Before (3.67) | After (3.68) | Source |
|---|---|---|---|
| 4 | **Your right to choose** / "Pennsylvania law says the choice of shop is yours..." | **Free** / Estimates / "Call first: the estimate is free, and you'll know where you stand before the car goes anywhere." | the chip "Free estimates", split; the line is 3.64's close, already in this section |
| 5 | **Insurance paperwork handled** (headline, no line) | **Handled** / Insurance paperwork / "We handle the paperwork and communication so you don't have to." | the chip, split; the line quoted byte for byte from `/collision-repair/` |
| 6 | **Free estimates** / "Call first: ..." | **Detailed** / After every repair / "Vehicles detailed inside and out after every repair." | the fourth chip, split; the line quoted byte for byte from `/collision-repair/` |

**The support lines for cards 5 and 6: the render decided,** as the brief
allowed. Both variants were built and rendered at 1440 and 390:

- **Without the lines,** cards 5 and 6 stand half-empty beside row one's full
  cards, which is the same imbalance, of a different kind, that Greg ruled
  against.
- **With them,** all six cards carry figure, label and line.

Both sentences ship today in `/collision-repair/`'s visible text, verified
byte for byte at this commit. **Nothing was written.**

**The standing scope question rides with the claim, unchanged.** "Detailed
after every repair" re-enters the town template carrying 4.2's question:
does "every" hold for glass-only jobs? It carries it exactly as it does on
the service pages. **Card 6's support line, "after every repair", carries
the same question,** and one answer settles both.

#### Mechanics

- **`.card-figure` is reused for all three,** and "Handled" and "Detailed"
  fit at the card's figure size with no new size step.
- **ROW TWO DOES NOT ROLL, a default rather than a ruling, flagged here.**
  `site.js`'s odometer rolls every `.stat-n` in the section, so the brief as
  written would have doubled the section's arrival motion from three
  figures to six. The motion law scopes the roll to the stat figures, and
  presumes more motion is a new ruling, "expected to be no". So row two's
  big words are `.fig-n`, which shares `.stat-n`'s look through one selector
  list in `site.css` (`.stat-n, .fig-n`), and not `.stat-n`, which the
  odometer finds. Lifetime, the review count and 12 still roll; Free,
  Handled and Detailed stand still. **Changing `fig-n` to `stat-n` on the
  three would make them roll, if Greg wants it.**
- **Variance: no list change, and the fixtures pass UNEDITED.** The section
  is still pattern text by its id, and the test file has no diff at this
  commit.

#### Measured, confirmed rather than assumed

**The ask runs at 390, by 3.65's two rules:**

```
header Call (furniture)   -> the section's Call/Email row (section ask)   1,541   was 1,399
section's row             -> card's Call (furniture)                      2,175   was 2,176
card's Call               -> promise band (section ask)                   1,120   was 1,119
promise band              -> pairs' row (section ask)                     1,979   unchanged
pairs' row                -> footer (furniture)                           1,722   was 1,723
CEILING 2,175 (under 2,684); FLOOR, the nearest two SECTION asks, 1,979 (over 1,634)
```

**One run moved,** because the support lines make the section 142px taller
on a phone. That run starts at the header's Call, which is furniture the
floor does not govern. Every other run moved by at most a pixel.

**The fold, 390x664, innerHeight 664:** CALL 401 to 463, clearing the call
bar by 141, unchanged, and the proof section still starts at 511. 360x640
clears by 117.

**Nothing else moved:** every other page is **identical to 3.67, 69 of 69
page-widths.** That matters because the `.stat-n` rule the service pages and
home use gained a selector here. The stubs are byte-unchanged.

**Rendered and inspected at 1440 and 390:** two rows of three ox figures,
each with its label and line.

#### The suite

- Both test scripts pass, **208 checks**.
- `stamp-assets.py --check` exits 0, and `build-sitemap.py --check` exits 0.
- `STAGING=1 audit.py --strict`: **23 pages at 95, Jamison at 96, 2 stubs at
  100; sameAs the only warning; zero criticals; 485 passing.** The review
  count and the brand count still agree everywhere.
- No em dash was added.

### 3.69 The Free card tells the truth about how estimates happen. TEMPLATE AMENDMENT, and a correction. BUILT 2026-09-28

**Run two inherits it.** The Free card's support line, and the opening's
closing paragraph, stop implying that a phone call produces an estimate.

#### The correction, from Greg as fact-checker of record

**Estimates are not done over the phone.** "Call first: the estimate is
free, and you'll know where you stand before the car goes anywhere." came
from 3.64's close, and 3.68 carried it onto the Free card. Read plainly, it
says a call tells you where you stand, and a call does not do that. **This
corrects 3.64's approved copy.** It is the fact-check working, not a strike
against the record, and 3.64 and 3.68 stand as written, superseded here.

#### The pairs

| Where | Before (3.68) | After (3.69) | Source |
|---|---|---|---|
| `#why-the-trip`, Free card, support line | "Call first: the estimate is free, and you'll know where you stand before the car goes anywhere." | "Estimates are free and there is no obligation." | byte for byte the sentence 3.68's opening already shipped, and the same words as the `#start` sub-line on home and every service page |
| `#for-jamison`, third paragraph | "If your car has been in an accident, call before you decide where it goes. Estimates are free and there is no obligation." | "If your car has been in an accident, call before you decide where it goes." | Greg's approval, via the brief. The second sentence moved to the card rather than being said twice in two screens |

**Nothing was written.** Both after-texts are strings that already ship.
The page now carries "Estimates are free and there is no obligation" twice,
on the Free card and in the promise band's sub-line, as it did before in
the opening and the band. The count did not change; only one of the two
places did.

#### TEMPLATE NOTE, for run two

**The pattern card now owns "Estimates are free and there is no
obligation."** The Free card sits in `#why-the-trip`, which is pattern text
by its id, so the variance gate does not count it. The per-town opening is
counted. **Run two's openings must NOT reuse that sentence:** it would say
the same thing twice on one page, and it is the kind of shared string the
opening exists to be free of. The Jamison opening now ends on the ask,
"call before you decide where it goes", and makes no estimate claim at all.

#### The sweep, ITEM 3: reported, NOT edited

The whole of `docs/` was read, every page's visible text, its JSON-LD
strings and meta description, plus `docs/llms.txt`, for any sentence
carrying "estimate" or "call first". Also grepped: `templates/`,
`scripts/`, `pagemap.md`.

**(a) The retired sentence appears nowhere else.** It was on the Jamison
Free card only, and it is gone. It was never in `llms.txt`, a schema string,
a meta, the template or another page.

**(b) Other copy that implies, or can be read as implying, an estimate by
phone.** None of these was touched, as the brief requires. **Each is for
Greg to rule on.** They are listed strongest first.

1. **`/collision-repair/`, `#why`, "Why Choose Tri-County Collision" list
   item.** Visible only.
   > Free estimates online and by phone.

   **The one explicit claim on the site.** It states a phone estimate
   outright, which is exactly what the correction says does not happen.
2. **`/collision-repair/`, `#insurance`, "Insurance Claims Assistance",
   closing paragraph.** Visible only.
   > Get a free estimate by calling (215) 322-5350 or requesting one online.

   "Get ... by calling" says the call yields the estimate.
3. **`/paintless-dent-repair/`, FAQ answer, visible AND FAQPage schema.**
   > Estimates are free, so the fastest way to a real number is to call (215) 322-5350 or stop by.

   "A real number" by calling. This is in the schema, so it is also what an
   assistant would quote.
4. **`/auto-glass-repair-replacement/`, FAQ "How do I get an estimate for
   auto glass work?", visible AND schema.**
   > To get an estimate for auto glass work, call us at (215) 322-5350 or request an estimate online.

   Softer: it can be read as "call to arrange one". The same page says
   elsewhere "When you bring your vehicle in, our technicians assess the
   damage and give you a precise estimate", which is the true process.
5. **`/commercial-collision-repair/`, FAQ "How do I get a commercial repair
   estimate?", visible AND schema.**
   > To get a commercial repair estimate, call (215) 322-5350 or request an estimate online.

   Same shape as 4. That page's process list gets it right: "Free estimate:
   Call us or request one online. We'll arrange to assess the damage and
   give you a detailed estimate".
6. **`/` and `/collision-repair/`, the cost FAQ answer, visible AND schema,
   same text on both.**
   > You can request an estimate online or call us at (215) 322-5350.

   **The weakest reading, and probably fine**: "request", then "or call us".
   Listed so the ruling covers it explicitly rather than by omission.

**Not flagged, read and cleared:** every "Free estimates" chip, meta and
schema description (a claim that estimates are free, silent on how); the
`#start` sub-line; `/contact-us/`'s "Free online estimate" card and meta,
which are CarWise and an online route, not a phone one; `llms.txt`'s three
lines ("Estimates are free.", "the shop quotes it from a free estimate",
and the CarWise line); Jamison's meta and schema description, "Directions
from Jamison, free estimates, (215) 322-5350.", where the number sits beside
the claim but says nothing about how an estimate is made; and every post's
use of "estimate" as a general noun.

**One adjacent question, raised and not ruled on:** items 1 and the
CarWise card both say "online". Whether an online submission produces an
estimate, or only a request for one, is the same class of question for the
owner. It is recorded here and not added to section 5 until Greg says so.

#### Mechanics

- **The builder** (scratch, not committed) changed the two strings. The page
  was rebuilt with `SUPPORT=1`, and the map was redrawn with the recorded
  jamison frame. **The page diff is exactly those two lines;** the redrawn
  inline SVG is byte-identical.
- **No CSS or JS was touched,** so there was no restamp. `stamp-assets.py
  --check` exits 0.
- **Variance: no list change,** and the test file has no diff.

#### Measured, confirmed rather than assumed

**Jamison is 53px shorter at both widths:** the proof section by 25 (the
Free card's line is one line shorter on a phone, and row two sets its own
height at 1440), and the opening by 28, one line.

**The ask runs at 390, by 3.65's two rules:**

```
header Call (furniture)   -> the section's Call/Email row (section ask)   1,516   was 1,541
section's row             -> card's Call (furniture)                      2,147   was 2,175
card's Call               -> promise band (section ask)                   1,119   was 1,120
promise band              -> pairs' row (section ask)                     1,979   unchanged
pairs' row                -> footer (furniture)                           1,723   was 1,722
CEILING 2,147 (under 2,684); FLOOR, the nearest two SECTION asks, 1,979 (over 1,634)
```

**The fold, 390x664:** CALL 401 to 463, clearing the call bar by 141,
unchanged, and the proof section still starts at 511. 360x640 is also
unchanged, at 401 to 463.

**Nothing else moved:** every other page is **identical to 3.68 in every
layout hash and map, 271 of 271 probe entries outside Jamison's seven.**
The stubs are byte-unchanged.

**Rendered and inspected at 1440 and 390:** the Free card reads "Free /
Estimates / Estimates are free and there is no obligation."; row two stays
level at 1440; and the opening ends on the ask.

#### The suite

- Both test scripts pass, **208 checks**.
- `stamp-assets.py --check` exits 0, and `build-sitemap.py --check` exits 0.
- `STAGING=1 audit.py --strict`: **23 pages at 95, Jamison at 96, 2 stubs at
  100; sameAs the only warning; zero criticals; 485 passing.** The report
  is identical to 3.68's except for one line, Jamison's word count, which
  went from ~849 to ~832.
- No em dash was added.

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
  **Checked 2026-09-24 (3.54): it does not.** The latitude matches Google's
  place pin to the digit, and the longitude is about 220m west of it, which is
  a Google Maps URL's viewport centre rather than its pin. The verified pin is
  40.1660232, -75.0512847: Google's place point, inside the OSM footprint of
  the building Google shows the shop in. ~~Not changed; section 5 item 26.~~
  **RULED 2026-09-25 and shipped, 3.56: every page's geo is now the verified
  pin, and `GEO_LAT`/`GEO_LON` in `scripts/audit.py` hold it.**
- **Hours**: Monday to Friday 8 a.m. to 6 p.m., Saturday by appointment only.
  Must match the Google Business Profile exactly. **It does not, as of 2026-09-24**: the
  profile says Saturday Closed and Sunday Closed (3.54). Now held by
  `HOURS_*` in `scripts/audit.py`, so when the answer lands it changes in one
  place and the build fails anywhere it did not.
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
- **"Free estimates in person or online."** ~~The online half waits on
  `/contact-us/`.~~ The online half is the shop's CarWise estimate, on
  `/contact-us/` since 3.53, and it is true while CarWise is in use.
- **The hero chip "Built to limit downtime"**, Greg's approved swap (3.51). A
  process claim, not a turnaround promise, but the chip is the strongest form
  the downtime claim takes on the page.

**`/contact-us/`** (3.53). **Four live claims are HELD rather than shipped.**
The page runs one line per card, and each of these is a promise a customer
would hold the shop to. Confirm any of them and it can come back:

- **"A real person answers, no phone tree."** The live page says it about
  (215) 515-4662, not about (215) 322-5350. Is it true of 322-5350?
- **"We reply the same business day"** to email.
- **"Takes about five minutes with photos of the damage"**, about the CarWise
  estimate.
- **"Pick your time online, and you're booked, with a confirmation to your
  inbox"**, about CarWise booking.

What the page does carry: "a thorough, in-person assessment at our Southampton
facility", which is what an appointment is, and "a quick, no-obligation idea of
repair costs", which is what the estimate is. Both need CarWise to still be in
use.

### 4.11 Claims the blog adds

Every claim below is migrated from the live post named, word for word unless
a pair says otherwise. **The posts' legal statements are the heaviest**: a
misstated law on the shop's own site is a real harm to a reader. They go to
Greg as well as the owner.

**`/your-right-to-choose-a-body-shop/`** (3.57)

- **Toyota factory certification, HELD** (removed by a pair). The live post
  says "factory-certified for brands our neighbors drive (Honda, Toyota,
  Subaru, Ford, GM, and more)", and Toyota is not among the twelve. Section 5
  item 27.
- **"your repairs carry a lifetime warranty"** (FAQ 3) and "a lifetime
  warranty on our work": the warranty question, 4.1.
- **"We coordinate directly with adjusters so inspections and supplements
  happen at our facility"** and "we also document OEM procedures and provide
  you with final paperwork."
- **The legal claims**, for a fact-check against the source:
  - "§146.8 of the PA Code prohibits requiring repairs at a specific shop or
    making you travel unreasonably";
  - the PA Insurance Department quote, "The choice of where your vehicle is
    repaired is up to you";
  - "If an insurer prepares an appraisal, they must give you a copy";
  - the first-party-claim "reasonable time" rule.
- **"family-owned, Southampton-based" and "ASE/I-CAR® Gold technicians"**:
  already on the list (4.1, 4.5).

**Batch 1** (3.58)

- **Post 1, the dashboard lights: the heaviest.**
  - "We are OEM certified collision repair facility for INFINITI, Nissan,
    Hyundai, Kia, Acura, Honda, GM, Chrysler, Ford, Dodge and Jeep". That is
    **eleven**, without Subaru, dated 2023, against the site's twelve. Was
    Subaru added since? The brand check reads counts, not lists, so this
    passes it; it is on this list instead.
  - "conveniently located near the PA turnpike, **route 95** and Street Road,
    County Line Road and Second Street Pike". I-95 is several miles from
    Jaymor Rd; does the shop want that landmark?
  - "Tri-County Collision also provides services for **tow, rental car**, and
    insurance claims assistance." A service-scope claim: does the shop
    arrange tows and rentals?
  - "We would be happy to supply you with an auto repair quote online or over
    the phone". Quotes by phone?
  - "ASE / I-CAR® GOLD certified": 4.1.
- **Post 2, the ultimate guide.** "Tri-County Collision offers a lifetime
  warranty on all repairs" (4.1). ASE/I-CAR Gold, repeated.
- **Post 3, OEM parts.** "prioritizes OEM parts" and "committed to OEM
  parts": always OEM, or OEM where available? 4.10 asks the same of the
  commercial page.
- **Post 4 and post 5.** The PDR and damage-assessment process claims mirror
  the service pages' (4.10); nothing new beyond ASE/I-CAR Gold.

**Batch 2** (3.58)

- **Post 9, critical questions: a warranty with terms.** "Reputable shops,
  including Tri-County Collision, offer a lifetime warranty on paint and
  workmanship for as long as you own [the vehicle]". This is the most
  specific warranty statement anywhere on the site, and it is exactly 4.1's
  question: lifetime of what, covering what, and transferable or not.
- **Posts 8, 9 and 10: "for decades"** and "family-owned and operated". The
  1974 and second-generation question, 4.5.
- **Post 10: "Certified technicians with expertise in all makes and models."**
  All makes?
- **Post 10: "a free professional assessment"**, and post 9's "fully-certified
  expertise".
- **Post 7**, in the body: "environmentally friendly". PDR does avoid paint
  and filler; the owner should be comfortable with the word.

**Batch 3** (3.58)

- **Post 16, ADAS: this bears on the ADAS page's gate.** "We perform many
  calibrations on site; for brand-specific targets or equipment, we
  coordinate with our vetted calibration partner or dealer." That answers
  section 5 item 4 partly, in the shop's own published words: some in-house,
  some partnered. The owner confirms which, and it settles the gate. Also
  "Same-day to 1-3 business days", "calibration certificates for each system
  addressed", and pre- and post-scan reports.
- **Post 14, deer: the legal and statistical claims.**
  - "Pennsylvania law requires immediate notice to police" when there is
    injury, death or a tow;
  - "a written report is required within five days" if police don't
    respond;
  - "Pennsylvania law prohibits raising your rate solely because you filed a
    claim unless you were at fault";
  - "Pennsylvania sees thousands of deer-related crashes each year". A
    statistic without a source.
- **Post 12, myths: "we maintain an I-CAR Gold Class certification, the
  highest standard in the industry."** 4.1, and "highest" is a superlative.
- **Post 11: "A family-owned shop with decades of local trust"** (4.5), and
  ASE/I-CAR Gold.
- **Post 13: "Our certified technicians."**

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
14. ~~**The glass page's closing promise**, Greg's to rule on~~ **Approved by
    Greg 2026-09-24 and shipped, 3.51.** The owner sees it as a claim like any
    other: "We will get you back on the road with quality glass, installed
    with the same care we bring to every repair." See 3.47.
15. **The dent page's scope** (4.10): PDR in house or sublet, hail taken or
    sublet, walk-ins, and whether the warranty and the detailing promise
    reach PDR-only jobs.
16. ~~**The dent page's closing promise**, Greg's first~~ **Approved by Greg
    2026-09-24 and shipped, 3.51.** The owner sees it as a claim like any other: "We will get you back on
    the road with the panel looking like nothing ever happened." See 3.48.
17. **The commercial page's scope** (4.10): tractor-trailers and buses above
    all, then on-site assessment, commercial insurance handling, the
    turnaround language, and whether the named customer types are real.
18. **Is CarWise still in use?** `/contact-us/` sends people to the shop's
    CarWise online estimate and appointment booking, and three service pages'
    "request an estimate online" sentences depend on it. If CarWise is retired,
    two cards come off, those sentences change, and the footer's "Send us your
    details online" label gets revisited. Also: CarWise names the shop
    "Tri-County Collision Center" (1.1). See 3.53.
19. **What is (215) 515-4662?** The live contact page prints it as its "Call Us"
    number, beside a promise that a real person answers. It is a third number,
    after 322-5350 and the CallRail line. Is it a line the shop wants
    published? Until the answer is yes, it ships nowhere. See 3.53.
20. **The four held contact-page promises** (4.10): a real person answers, a
    same-business-day email reply, a five-minute estimate, and a booking
    confirmation email.
21. **Sunday.** The live site's schema never says, and the site does not
    either. The Google Business Profile says Closed. Confirm, and it can be
    written, in one place: `HOURS_*` in `scripts/audit.py`. See 3.54.
22. **Saturday.** This site and the live schema say "by appointment only";
    the Google Business Profile says Closed. Both cannot be what a customer is
    told. Which is it, and which side moves? See 3.54.
23. **The profile's phone is (215) 999-3497**, a fourth number. Is it a
    tracking number on the profile, and is (215) 322-5350 on the profile at
    all, as an additional number? The site and the profile carrying different
    primary numbers is the NAP mismatch rule 6 exists to prevent, and the
    answer decides which side moves. See 3.54.
24. **The profile's name is "Tri County Collision Center"**; the site's is
    "Tri-County Collision", and CarWise also says "Center" (3.53). This is
    1.1's question, now with the profile's answer in hand.
25. **Optional: a parking or arrival note** on the contact page. The shop is
    one tenant in a multi-tenant building at Jaymor Rd, James Way and Knowles
    Ave, which is exactly when a line like "the entrance is on the Jaymor Rd
    side" helps. Only if the owner wants one, and only in their words.
26. ~~**The schema's geo is about 220m west of the shop** (4.7). For Greg first:
    correct it to the verified pin, 40.1660232, -75.0512847, on every page?~~
    **RULED by Greg 2026-09-25 and shipped, 3.56**: every page's geo is the
    verified pin. The owner's confirmation folds into his NAP sign-off
    (section 2), not a new question.
27. **Is the shop Toyota factory-certified?** The live right-to-choose post
    says so; the site's twelve do not include Toyota. The claim is held off
    the migrated post until the answer is yes, and a yes also moves
    BRAND_COUNT and the strip. See 3.57 and 4.11.
28. **The blog's claims, 4.11.** Sixteen migrated posts carry the shop's
    older statements: an eleven-brand certification list without Subaru, a
    warranty "on paint and workmanship for as long as you own" the vehicle,
    tow and rental-car services, I-95 as a nearby landmark, ADAS calibration
    "many on site", and PA legal statements. Each is live on the old site
    today; each needs the owner's yes before this site is the one serving it.
29. **The drive time from Jamison: "about 15 minutes".** It is an OSRM routing
    with no traffic, from the village's crossroads at York Road and Almshouse
    Road to the shop (3.62). Is it what a Jamison customer would say it takes?
29a. **The Google Business Profile's name and phone now have a concrete cost
    on this site (3.65).** A Google Maps embed queried by the business's name
    renders the Profile's own card: today "Tri County Collision Center" and
    (215) 999-3497, the unconfirmed fourth number (questions 23 and 24). The
    contact page's embed is centred on the pin by coordinates to keep that
    card off it, but Google's tiles may still label the pin with the
    Profile's name. **Fixing the Profile before cutover** removes the problem
    at its source, for every map and every search result, not just this page.
30. **Does the shop serve Warrington, and Warwick Township beyond Jamison?**
    Neither is named on the live hub, so neither is named on the Jamison page
    as a neighbor (3.62, ruling 3). A yes adds them.
