# drafts/ is throwaway

Three design directions for the hero, the proof band and the header, built
2026-09-06 for a direction pick. **When one is chosen, this whole folder is
deleted** and the winner is rebuilt into `docs/` properly, with its fonts moved
to `docs/assets/fonts/` and their licence files moved with them.

Nothing in here is part of the site. It sits outside `docs/` on purpose, so
`scripts/audit.py` never scores it and `scripts/build-sitemap.py` never lists
it. Each file carries `noindex`, no canonical, no Open Graph and no schema,
because it is a picture of a direction rather than a page.

## How to look at them

They are plain files. Open them from the repo:

```
open drafts/hero-a/index.html
open drafts/hero-b/index.html
open drafts/hero-c/index.html
```

**There are no URLs.** GitHub Pages is still off, and it stays off: turning it
on to preview a draft would publish a copy of the shop's site at a github.io
address while the real one is live, which is the thing the whole staging
exception exists to prevent.

Each draft is a **complete page**. Everything from "Our Collision Repair
Process" down is copied byte for byte out of `docs/collision-repair/index.html`,
so all three scroll end to end and can be compared as whole pages rather than
as three hero screenshots. **No content changed in any of them.** Below the
fold the only difference between the three is the typeface.

## Shared by all three

- **Ink sticky header** with the oxblood call button. The button keeps its
  oxblood fill, because oxblood means act, and gains a paper border: `--ox` on
  `--ink` measures **1.47**, so the shape would otherwise be invisible even
  though its paper label reads at 11.04.
- **The staging bar is a slim ink strip**, same ink as the header under it,
  small type, one hairline between them. It was a gold band, which read as a
  design decision instead of a notice.
- **Gold is gone from the palette**, on the client's call. Everything
  `#E5C549` used to do is now `--paper` or `--ox`. The palette table in the
  header of `docs/assets/site.css` is updated, and so are the measured
  contrast ratios.
- Solid colours only, no gradients and no glows. The shadow under the photo
  card in draft C is a neutral drop shadow, which is depth, not a glow.
- **Motion is zero.** Nothing animates in any of the three. The FAQ accordion
  is still the only moving part on the page.

## The three directions

| | Draft A | Draft B | Draft C |
|---|---|---|---|
| | **Photographic** | **Structural** | **Dark-first** |
| Hero | Full-bleed photograph with an opaque ink panel over it holding the copy | Split, with solid angled wedges in oxblood and ink; photo bleeds off the right edge | On ink, with the photograph floating on a paper card and a deep neutral shadow |
| Type | Set large | Set oversized and uppercase | Set at a normal display size |
| Proof band | Big-numeral stat band: 12, 231, Lifetime | Two heavy chip rows on ink | Four oxblood-ruled items on paper, then the brand chips |
| Oxblood does | The one filled button | The wedge and the brand chips | All the pointing: rules, slabs and the one filled button |

**The numbers in draft A are real and there are only three of them.** 12 is the
factory certification count, 231 is the Google review count **carrying the date
it was true**, and the third is the word "Lifetime" rather than a number,
because inventing a fourth statistic to balance a row is exactly how a made-up
number gets onto a client's site. See `proposed-changes.md` 4.4: the review
count is either a live widget, a dated number, or it comes off.

## The type, and the licences

All six faces are **self-hosted**. Nothing on any of these pages reaches a
webfont CDN at runtime, so there is no third-party request, no font-loading
flash from someone else's server, and nothing to break when a CDN changes.
The `.woff2` files are the **latin subsets** as served by Google Fonts, and the
three body faces are variable, so one file covers every weight the page uses.

| Draft | Display | Body | Files |
|---|---|---|---|
| A | **Archivo Black** | **Source Sans 3** | 9.8 KB + 28.8 KB |
| B | **Anton** | **IBM Plex Sans** | 12.0 KB + 40.2 KB |
| C | **Zilla Slab** | **Public Sans** | 16.8 KB + 26.6 KB |

**Every one is SIL Open Font License 1.1**, which permits redistribution and
self-hosting as long as the licence travels with the font. It does: the six
`OFL-*.txt` files in `drafts/fonts/` are the upstream licence texts, unedited.

| Face | Copyright |
|---|---|
| Archivo Black | 2017 The Archivo Black Project Authors |
| Source Sans 3 | 2010-2020 Adobe, Reserved Font Name "Source" |
| Anton | 2020 The Anton Project Authors |
| IBM Plex Sans | 2017 IBM Corp., Reserved Font Name "Plex" |
| Zilla Slab | 2017 The Mozilla Foundation |
| Public Sans | 2015 The Public Sans Project Authors |

Why each pairing, in one line:

- **A: Archivo Black over Source Sans 3.** Archivo Black has one weight and it
  is enormous, which is what you want set over a photograph. Source Sans 3 was
  drawn for interface text and stays comfortable at 17px underneath it.
- **B: Anton over IBM Plex Sans.** Anton is a single very heavy condensed face
  that survives being set huge and clipped by a diagonal. Plex was drawn for
  technical documentation and keeps the long paragraphs legible under it.
  Plex's variable range tops out at 700, so nothing in draft B asks for 800.
- **C: Zilla Slab over Public Sans.** A slab serif reads as machinery rather
  than as fashion, which is the register a body shop wants when the page goes
  dark. Public Sans is a plain wide-aperture grotesque drawn for government
  forms, so it holds up as light type on ink where a lighter face would smear.

## One asset finding, worth raising whichever draft wins

The logo is a light-background asset. On the ink header its silver "TRI-COUNTY"
wordmark reads fine at 9.96 against ink, but the red "COLLISION" measures
**3.91**, which is weak. It is brand art, and contrast rules exempt logos, so
none of the drafts puts it on a white plate: a plate in a sticky header reads
as a sticker.

**Ask the owner for a light-on-dark logo variant**, or for the vector source so
one can be derived from the real letterforms. The standards say brand assets
are derived, never guessed, so nobody here should be recolouring a PNG.
