# Motion sampler

**Candidates only. Nothing in this folder ships, and nothing in `docs/`
changed to make it work.**

`docs/assets/site.css` says motion on this site is zero except the FAQ
disclosure, "because a person opened it". That law still stands. This is
where five candidate effects can be judged **on the real page**, at real
sizes, instead of argued about in the abstract.

```
python3 drafts/motion/build.py          # regenerate index.html
python3 drafts/motion/build.py --check  # exit 1 if it has gone stale
python3 -m http.server 8800             # from the repo root, then open
                                        # /drafts/motion/index.html
```

`index.html` is **generated**, not hand-maintained, so it cannot drift
away from the page it is supposed to be showing. Everything else is done
at runtime by `motion.js`: no odometer markup, no stamp markup, no lane
markup exists in the file. That is deliberate. The question is what these
effects cost on the page as built, not on a page rebuilt to flatter them.

## The sampler bar

Not a candidate, and it does not ship. **Replay entrances** re-runs
everything that runs once, because otherwise you reload to see it twice.
**Force reduced motion** switches on the reduced path without going into
System Settings, so the hard rule can be checked in place.

## The hard rules, and where each is enforced

| Rule | Where it is kept |
|---|---|
| Transform and opacity only | Nothing in `motion.css` animates a colour, width, height, shadow or background. Where a shadow has to change, a separate layer's **opacity** changes. |
| `prefers-reduced-motion` respected | Twice. `motion.js` never arms anything when it is set, and a block at the foot of `motion.css` neutralises the rest. |
| Hover only behind `(hover: hover)` | Every hover rule in section C sits inside that query. The `:active` press does not, because a press is not a hover and touch deserves the feedback. |
| Nothing loops | No `iteration-count`, no `infinite`. Every entrance releases once and unobserves itself. |
| No gradients, no glows | Solid colours only, per the palette law. |
| No library | Two files, no dependencies. |
| Phone cost near zero | Compositor-only properties, nothing on load, one `IntersectionObserver`, and the lane's five measurements happen once. |

**The one rule that shapes the code more than any other: no element is
ever hidden by CSS alone.** Every "from" state is applied by JavaScript,
and only when the motion is actually going to run. With JS off, with
reduced motion on, or if `motion.js` throws on its first line, the page
is the production page with nothing invisible waiting for a script that
is not coming.

## The differentiation rule, which outranks taste

*If an effect could appear unchanged on a generic SaaS landing page,
redesign it around this shop's world or drop it.*

Banned outright and not present: scroll fade-ups on everything, parallax,
mouse-tilt cards, floating shapes, particles, shimmer and skeletons,
typing animations, glassmorphism.

## The five

### A. The odometer

The stat band's **274** and **12** roll up like a mechanical odometer,
once, when the band enters view. ~880ms for a three-digit number.

*How it earns its place.* A counting number is the most generic effect on
the web, and on a SaaS page it is decoration over a figure nobody checked.
Two things make this one specific. The numbers **are** real and dated,
which is the only reason this site is allowed to move them at all under
"motion is evidence, not costume". And the metaphor is the one counting
instrument that belongs to a car: digits on a drum, through a window,
landing.

*Two decisions worth knowing.* Each strip is `[target, 0-9, target]`, so
the number on screen is **the true number before the roll and after it**.
An odometer parked on `000` waiting to be scrolled into view would put a
false number on a site whose whole discipline is that numbers are true.
And the step is `0.88em` because that is `.stat-n`'s line-height, so the
band does not change height: **measured at 390, the stat band is 594px
with and without the effect, and each numeral's box is 44 x 350 in both.**

*The measurement it rests on:* Archivo Black's digits are all exactly
0.667em wide, all ten identical. So the window needs no tabular-figures
hack and the number cannot jitter as it rolls. **If the display face
changes, measure again before trusting this.**

### B. The stamp

**Lifetime** arrives as a warranty stamp pressed onto the page: one
settle from 1.06 to rest, opacity snapping in at 90ms while the scale
takes 380ms. The gap between those two durations is what makes it read as
a press rather than a zoom.

*Where this went past the brief, and it is easy to undo.* A scale-down
settle with a fade is the SaaS modal entrance. A stamp is not square to
the paper, so this one carries **1.2 degrees of rotation** settling to
zero, with its origin at the left edge where a hand would press hardest.
That rotation is mine, not the brief's. **If it reads as a wobble rather
than as paperwork, delete the `rotate()` and what is left is exactly what
was asked for.**

### C. Lift, in house materials

Cards rise 3px, an ink shadow deepens beneath them, a 2px oxblood rule
sharpens along the base. Buttons and the call bar take a 1px press.

*How it earns its place.* The lift is the most generic gesture here and is
not trying to be otherwise: it is feedback to a hand, and feedback should
be familiar. **What is tuned is the material.** The default is a soft grey
glow that belongs to nobody. This shadow is `--ink` at low alpha, so a
card casts a shadow the colour of this site's own darkest value, and the
base rule is `--ox`.

*Adoption cost, stated plainly.* `.svc` clips its photo with
`overflow: hidden`, which would clip an outside shadow layer too. The
sampler moves the rounding onto the image instead. **Adopting C means
adopting that one-line change with it.**

### D. The lane line — **the flagged one**

The six process steps gain a dashed centre line down the gaps between
them, painting once, top to bottom, as the section enters view. The road
to road-ready, literally.

**THIS IS THE ONLY STAGING-TYPE MOTION IN THE SET.** Everything else
answers a reader: a hover, a tap, a disclosure. This one performs as the
reader arrives, which is precisely what `site.css`'s header rules out.
**If it is kept it is a deliberate amendment to that law and has to be
written down as one**, in `site.css`'s header and in `CLAUDE.md`, with the
date. Nobody should find it later and conclude the rule was always softer
than it reads.

*It must read as a lane, not a progress bar.* Three things hold that
line: **no track** behind the dashes, so nothing is being filled; **no
state change** once painted, so nothing is being completed; and it paints
at **constant speed**, because easing toward a stop is what a progress bar
does. A road has no finish, only a next dash.

*The colour is `--rule`, not oxblood, and that is the palette law
talking.* A real lane line is white or yellow, and oxblood is the obvious
"make it feel like us" choice. But **oxblood means act on this site and
nothing else**, and a decorative line nobody can click would be the first
thing to break that. `--rule` is what the step numerals already use. The
cost is that the lane is quiet. Look at it before deciding that is wrong.

*Its real limitation: it is a single-column effect.* `.steps` is one
column below 720px, two to 1040, three above. A line from 01 to 06 only
exists in the first of those, so **above 720px it renders nothing at
all** rather than drawing something that is not a road. On a desktop this
effect does not exist. That is not a detail to discover later.

### E. Accordion polish

The plus becomes a chevron, the chevron turns over on open, and the
answer's text arrives rather than appearing. Micro-feedback on a control
the reader just operated, on the one moving part the site already allows.
The safest candidate here, and no signature attempted.

*One honest limitation.* **The panel's height still snaps.** Animating it
means animating a height, which rule 1 forbids, and the alternatives are a
library or `::details-content`, which is not reliable yet. So the text
fades and slides four pixels; the box does not glide. If a gliding box is
the requirement, this candidate has to be **re-scoped against rule 1**
rather than quietly excepted from it.

## How this was verified, and what was not verified

Checked at 390 and 1440, with the console clean:

- the odometer builds 5 digit windows for 274 and 12, and the stat band
  measures **identically to production**, 594px, numerals 44 x 350;
- the true digits are on screen in the armed state, not zeroes;
- 11 cards get lift layers; the lane builds **5 dashes at 390 and 0 at
  1440**, as designed;
- the settled values are right: the stamp resolves to `opacity: 1;
  transform: none`, and the odometer strip to `-480.128px`, which is
  exactly 11 x 0.88em at the rendered font size.

**What was not verified: the motion itself, in flight.** Headless Chrome
with `--virtual-time-budget` pins CSS transitions at their start value, so
every animated property reads as though it never moved. That cost a
detour here: a stamp reading `opacity: 0` long after it should have
settled looked like a cascade bug, and it was the harness. **The end
states are proved by disabling transitions and reading the resolved
values; the timings and easings are declared in `motion.css` and have
been read, not watched.** Anyone deciding on these should open the page in
a real browser and use the replay button. That is what it is for.
