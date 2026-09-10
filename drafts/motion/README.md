# Motion sampler

**Candidates only. Nothing in this folder ships, and nothing in `docs/`
changed to make it work.**

Five candidates were built here on 2026-09-10 and judged the same day.
**Two were cut, one was adopted, two are still open.** The verdict table
is below.

`docs/assets/site.css` no longer says motion is zero: adopting the lift
amended that, and the amendment is recorded there and in `CLAUDE.md`,
dated. What did not change is the reason the rule exists, that everything
which moves does so **because a person did something to it**. This folder
is where anything that wants to move gets judged **on the real page**, at
real sizes, before it goes anywhere near that sentence.

```
python3 drafts/motion/build.py          # regenerate index.html
python3 drafts/motion/build.py --check  # exit 1 if it has gone stale
python3 -m http.server 8800             # from the repo root, then open
                                        # /drafts/motion/index.html
```

`index.html` is **generated**, not hand-maintained, so it cannot drift
away from the page it is supposed to be showing. No lane markup exists in
it: `motion.js` builds that at runtime. That is deliberate. The question
is what an effect costs on the page as built, not on a page rebuilt to
flatter it.

**The adopted lift is not in this folder.** The sampler shows it anyway,
because the sampler loads `site.css`. What you see here is what ships.

## The sampler bar

Not a candidate, and it does not ship. **Replay entrances** re-runs
the lane, which runs once, because otherwise you reload to see it twice.
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

## The verdict, 2026-09-10

| | |
|---|---|
| **A. Odometer** | **CUT.** Deleted, not archived. |
| **B. Stamp** | **CUT.** Deleted, not archived. |
| **C. Lift** | **ADOPTED**, into `docs/assets/site.css` as design rule 7. |
| **D. Lane line** | **UNDECIDED.** Still here. |
| **E. Accordion** | **UNDECIDED.** Still here. |

The cut two were **deleted rather than commented out**. A second direction
sitting in the repo is a second direction someone builds from later.

### C, and what changed on the way in

The sampler's version injected its two layers with JavaScript. **The shipped
version is pure CSS**, `::before` for the shadow and `::after` for the rule,
so the lift works with JavaScript off. And the rule changed as directed: it is
now **present at rest** as a short quiet mark, and on hover it sharpens to
solid and **sweeps to the card's full width**. Solid `--ox`, no blur, no glow.

What may move is a short list: **transform, opacity, and the rule's width.**

Two costs, both paid rather than deferred:

- **The step numeral moved** from `.step::before` to `.step h3::after`. The
  lift needs both of a card's pseudo-elements and the numeral was sitting on
  one. It lands in the same place, because `h3` is static so its containing
  block is the positioned `.step`.
- **`.svc` gave up `overflow: hidden`**, with the photo's rounding moving onto
  the image. That was the adoption cost flagged when C was first built.

**It is not in this folder any more.** The sampler still shows it, because the
sampler loads `site.css` — which is the point: what you see here is what
ships. Hover any card.

## The two still undecided

### D. The lane line — **the flagged one**

The six process steps gain a dashed centre line down the gaps between them,
painting once, top to bottom, as the section enters view.

**Now that C has shipped, this is the only thing left that performs as a
reader ARRIVES rather than answering something they did.** `site.css`'s header
was amended on 2026-09-10 to say motion is no longer zero, and it was careful
to say that everything which moves does so because a person did something to
it. **D would break that sentence.** Keeping it is a second amendment, dated,
in `site.css` and `CLAUDE.md` both.

*It must read as a lane, not a progress bar.* No track behind the dashes, so
nothing is being filled. No state change once painted, so nothing is being
completed. Constant speed, because easing toward a stop is what a progress bar
does; a road has no finish, only a next dash.

*The colour is `--rule`, not oxblood, and that is the palette law talking.*
Oxblood means act, and **since C shipped it also means "you are pointing at
this"**. A decorative line that answers neither would be a third meaning,
which is how a palette stops meaning anything.

*Its real limitation: it is a single-column effect.* `.steps` is one column
below 720px, two to 1040, three above. **Above 720px it draws nothing at all**
rather than drawing something that is not a road. On a desktop this effect
does not exist.

### E. Accordion polish

The plus becomes a chevron, the chevron turns over on open, and the answer's
text arrives rather than appearing. Micro-feedback on a control the reader
just operated. The safest candidate here, and no signature attempted.

*One honest limitation.* **The panel's height still snaps.** Animating it
means animating a height, which rule 1 forbids, and the alternatives are a
library or `::details-content`, which is not reliable yet. So the text fades
and slides four pixels; the box does not glide. If a gliding box is the
requirement, this has to be **re-scoped against rule 1** rather than quietly
excepted from it.

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
