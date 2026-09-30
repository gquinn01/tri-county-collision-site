/* ===========================================================================
   TRI-COUNTY COLLISION, SHARED SCRIPT.

   Small, and it should stay that way. EVERY PAGE ON THIS SITE WORKS WITH
   JAVASCRIPT OFF: the FAQ is <details>/<summary>, the phone is a tel:
   link, the nav is a list, the stat band's numbers are text in the
   markup and nothing here touches them. Nothing here is load-bearing.

   WHAT IS HERE, AND WHY IT IS ALLOWED TO BE.

   Arrival motion, adopted 2026-09-10. The motion law in site.css's
   header was amended for it, and the amendment is narrow: an effect may
   fire ONCE, on a section's first arrival, and never again. A lane draws
   because the section it runs down is a road. Nothing loops, nothing
   re-triggers, nothing runs on load. The lane is the only arrival effect
   left: the stat band's counting effect was withdrawn on Greg's ruling
   (proposed-changes.md 3.85), and its figures stand still as the text
   they are in the markup.

   THE RULE THAT SHAPES ALL OF THIS: NO ELEMENT IS EVER HIDDEN BY CSS
   ALONE. Every "from" state is added here, and only when the motion is
   actually going to run. So with JavaScript off, with
   prefers-reduced-motion set, or if this file throws on its first line,
   the page is complete and nothing is invisible waiting for a script
   that is not coming.

   WHAT IS STILL NOT HERE, on purpose:

   - No CallRail snippet. It gets added at cutover, in the same pass as
     the GA4 property. CallRail swaps numbers into the rendered page at
     runtime, which is why the tracking number is not in this repo's
     source and must never be pasted into it.
   - No form handler yet. The form's fields, its endpoint and what it
     says after a send are all still with the owner, and the endpoint
     will be in the CLIENT'S account. When it lands, the submit handler
     goes here and calls preventDefault(), which is exactly why the GA4
     form_submit event has to be sent explicitly: enhanced measurement
     cannot see a submit that never navigates.
   =========================================================================== */

(function () {
  "use strict";

  /* The footer year, so the site never tells a visitor it stopped being
     maintained in a year that has passed. The markup carries a real year
     as its fallback, so a reader with JavaScript off still sees one. */
  var y = document.querySelector("[data-year]");
  if (y) { y.textContent = String(new Date().getFullYear()); }

  /* ---------------------------------------------------------------------
     THE NAV, 2026-09-29, proposed-changes.md 3.83
     ---------------------------------------------------------------------
     Without this block the nav still works: a dropdown opens on hover and
     on focus-within, and a phone reader reaches every page from the
     footer's Explore column. With it, each dropdown is a true disclosure
     that says whether it is open (aria-expanded), Escape closes whatever
     is open and hands focus back to its button, a click or a focus move
     outside closes it, and the Menu button opens the phone menu. Nothing
     animates, so reduced motion has nothing to turn off. */
  document.documentElement.classList.add("js");
  var nav = document.querySelector("header.nav");
  if (nav) {
    var menuBtn = nav.querySelector(".navtoggle");
    var subBtns = Array.prototype.slice.call(nav.querySelectorAll(".nav-sub-toggle"));
    var wide = window.matchMedia("(min-width: 1100px)");

    var setSub = function (btn, open) { btn.setAttribute("aria-expanded", open ? "true" : "false"); };
    var closeSubs = function (except) {
      subBtns.forEach(function (b) { if (b !== except) { setSub(b, false); } });
    };
    var setMenu = function (open) {
      if (!menuBtn) { return; }
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      nav.classList.toggle("is-open", open);
      if (!open) { closeSubs(null); }
    };

    subBtns.forEach(function (btn) {
      var item = btn.closest(".nav-item");
      btn.addEventListener("click", function () {
        var open = btn.getAttribute("aria-expanded") !== "true";
        closeSubs(btn);
        setSub(btn, open);
      });
      /* A desktop pointer opens on hover, as the live site's does; a touch
         or a keyboard uses the button. */
      item.addEventListener("pointerenter", function (e) {
        if (e.pointerType === "mouse" && wide.matches) { closeSubs(btn); setSub(btn, true); }
      });
      item.addEventListener("pointerleave", function (e) {
        if (e.pointerType === "mouse" && wide.matches) { setSub(btn, false); }
      });
      item.addEventListener("focusout", function (e) {
        if (wide.matches && !item.contains(e.relatedTarget)) { setSub(btn, false); }
      });
    });

    if (menuBtn) {
      menuBtn.addEventListener("click", function () {
        setMenu(menuBtn.getAttribute("aria-expanded") !== "true");
      });
    }

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") { return; }
      var openSub = subBtns.filter(function (b) { return b.getAttribute("aria-expanded") === "true"; })[0];
      if (openSub) { setSub(openSub, false); openSub.focus(); return; }
      if (menuBtn && menuBtn.getAttribute("aria-expanded") === "true") { setMenu(false); menuBtn.focus(); }
    });
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target)) { closeSubs(null); setMenu(false); }
    });
    /* Crossing the breakpoint closes everything, so a menu opened on a
       narrow window never lingers as a stray panel on a wide one. */
    var onWide = function () { closeSubs(null); setMenu(false); };
    if (wide.addEventListener) { wide.addEventListener("change", onWide); } else if (wide.addListener) { wide.addListener(onWide); }
  }

  /* ---------------------------------------------------------------------
     ARRIVAL MOTION
     --------------------------------------------------------------------- */

  var reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  var sections = [];

  /* ---------- The lane ----------------------------------------------
     One dash per gap between steps, measured rather than guessed,
     because where a gap falls depends on how the text wrapped.

     BELOW 720px ONLY. .steps is one column there, two to 1040, three
     above, and a line from 01 to 06 is only a road in the first of
     those. Above 720px this draws nothing at all. */
  function buildLane(steps) {
    var lane = steps.querySelector(".lane");
    if (!lane) {
      lane = document.createElement("span");
      lane.className = "lane";
      lane.setAttribute("aria-hidden", "true");
      steps.classList.add("lane-host");
      steps.appendChild(lane);
    }
    lane.textContent = "";
    var cards = steps.querySelectorAll(".step");
    if (window.innerWidth >= 720 || cards.length < 2) { return; }
    for (var i = 0; i < cards.length - 1; i++) {
      var top = cards[i].offsetTop + cards[i].offsetHeight;
      var height = cards[i + 1].offsetTop - top;
      if (height <= 6) { continue; }
      var dash = document.createElement("span");
      dash.className = "lane-dash";
      dash.style.top = (top + 3) + "px";
      dash.style.height = (height - 6) + "px";
      dash.style.setProperty("--dash-delay", (i * 110) + "ms");
      lane.appendChild(dash);
    }
  }

  /* ---------- Build, then arm, then watch ---------------------------- */
  var steps = document.querySelector(".steps");
  if (steps) {
    buildLane(steps);
    /* MEASURED AGAIN ONCE THE FONTS HAVE LANDED, 2026-09-28,
       proposed-changes.md 3.60. The first build can run before Source
       Sans 3 swaps in, and a step that rewraps then moves its gap out
       from under the dash. One promise, settled once: no listener, no
       polling. */
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(function () { buildLane(steps); }); }
    sections.push(steps.closest("section") || steps);
    var t = null;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () { buildLane(steps); }, 150);
    });
  }

  if (!sections.length) { return; }

  /* THE FIRST OF THE TWO REDUCED-MOTION GUARDS. Nothing is armed, so
     nothing is ever in a "from" state: the lane rests fully drawn. The
     second guard is the prefers-reduced-motion block in site.css. */
  if (reduceMQ.matches) { return; }

  sections.forEach(function (el) { el.classList.add("motion-armed"); });

  if (!("IntersectionObserver" in window)) {
    sections.forEach(function (el) { el.classList.add("motion-in"); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) { return; }
      entry.target.classList.add("motion-in");
      /* UNOBSERVED IMMEDIATELY. "Once, and never again" is a property of
         this line, not a promise in a comment. */
      io.unobserve(entry.target);
    });
  }, { threshold: 0.25 });

  sections.forEach(function (el) { io.observe(el); });
})();

/* ===========================================================================
   REAL REPAIRS: NOTHING RUNS HERE ANY MORE. Tombstone, 2026-09-17.

   A tap-to-crossfade lived at this line for one day. It stacked each
   pair, faded the after over the before on a tap, click or drag, and
   carried the role, tabindex, aria-pressed and aria-hidden machinery
   that a two-state control needs.

   RETIRED THE SAME DAY ON THE CLIENT'S RULING: a pair now shows both
   frames at once, before beside after, and the comparison is made by
   the layout instead of by a reader finding a control.

   THE SECTION NEEDS NO JS-OFF FALLBACK NOW, because it never leaves
   normal flow. The ten frames are ten images in the flow of the page,
   each with its own chip; there is no enhanced state for a reader
   without JavaScript to miss, and nothing here is hidden waiting for a
   script. It went with the CSS that stacked the frames and with the
   note's middle sentence, which was the instruction to tap.
   =========================================================================== */
