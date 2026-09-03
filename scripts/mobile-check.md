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
