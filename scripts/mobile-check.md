# Checking mobile layout, without fooling yourself

Sits next to `audit.py` because it is the other half of "is this page
actually fine": the audit checks the markup, this checks the layout.

## The trap

Headless Chrome on macOS will not lay a page out below roughly 500px.
Ask for `--window-size=375,N` and it lays out at about 500px wide and
then crops the screenshot to 375px. What you get back is the left 375px
of a 500px page. Every section loses its right-hand padding, cards run
off the edge, and headings look clipped.

It looks exactly like a horizontal overflow bug. It is not one. On
2026-08-16 this cost most of a session: a site-wide mobile defect was
reported, a fix was attempted against the wrong cause, and the page had
been correct the whole time.

## The tell

Render the same page at several widths and compare the DOCUMENT HEIGHT.
A page that genuinely reflows gets taller as it gets narrower. If the
height is identical at 375, 420, 460 and 500, the layout viewport never
changed and you are looking at the clamp, not the page.

That was the actual evidence: 12680px at all four widths, changing only
at 560.

## The method that works

Load the page in an iframe of the width you want to test, inside a
window wide enough to escape the clamp. The iframe gets a real viewport
of exactly that width.

```html
<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>html,body{margin:0;background:#ff00ff}
iframe{width:375px;height:16000px;border:0;display:block}</style>
</head><body><iframe src="services/web-design/" scrolling="no"></iframe></body></html>
```

Save it into `docs/` as a temporary file, serve the repo, and shoot it
in a 600px window:

```
python3 -m http.server 8800 --bind 127.0.0.1 &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=4000 \
  --window-size=600,16000 --screenshot=out.png \
  "http://127.0.0.1:8800/docs/_probe.html"
```

The magenta background makes the iframe edge obvious: anything magenta
inside x < 375 means the frame is not the width you think it is. Delete
the probe file afterwards. It must never be committed, because a stray
page in `docs/` is a page the audit will score and a crawler can find.

## Reading the result

Cards and inputs sit inside `.wrap`, which carries 30px of side padding.
In a correct 375px render they span x=30 to x=344, so the insets are
30px on both sides. Symmetric insets mean the page fits. An inset of 0
on the right means content is being clipped.

Checked this way on 2026-08-16, the homepage, a service page and a town
page all came back 30/30 at 375px.

## Before calling anything a layout bug

1. Reproduce it with the iframe method, not a window screenshot.
2. Check the document height across widths, as above.
3. If it is real, bisect by removing one section at a time. If removing
   every section individually fails to change the result, the page is
   not the cause and the tooling is.

## The fold budget on a phone, and the 60px nobody counts

Added 2026-09-10, after the hero CTA pair was found sitting below the
fold on every phone.

**The usable height is 604px, not 664.** A 390x664 viewport is what an
iPhone 12, 13 or 14 shows in Safari with its own chrome around it. The
call bar is `position: fixed; bottom: 0` and 60px tall, and it covers
whatever is under it rather than pushing it up. So anything below 604
is not on screen, and tuning a hero against 664 is tuning against 60px
that are already spent.

The staging banner spends another 57px at 390, because its sentence
wraps to two lines. That comes off at cutover, so **measure both
states**: it is the only difference between what a reviewer sees today
and what a customer will see.

## Measuring it, rather than judging it by eye

Same iframe trick as above, plus same-origin measurement. The parent
window can read the iframe's DOM, so the probe reports numbers instead
of a picture:

```js
var d = f.contentDocument, w = f.contentWindow;
function box(el) {
  var r = el.getBoundingClientRect();
  return {t: Math.round(r.top + w.scrollY), b: Math.round(r.bottom + w.scrollY)};
}
box(d.querySelector('.hero .cta-row')).b <= 604   // the whole test
```

Run it once as the page stands, then inject
`.staging{display:none !important}` into the iframe's head and run it
again. That second number is the real one.

Read it back with `--dump-dom` and a marker string around the JSON,
not with `--screenshot`. A screenshot tells you something looks wrong;
these numbers tell you by how much, which is what you need to fix it.

**Shoot one picture at the end anyway**, with a 2px line absolutely
positioned at 604, and check that the line falls where the arithmetic
said it would. The numbers catch the bug and the picture catches a
wrong assumption in the numbers.

Delete every probe file afterwards. A stray page in `docs/` is a page
the audit scores and a crawler can find.
