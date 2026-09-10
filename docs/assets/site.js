/* ===========================================================================
   TRI-COUNTY COLLISION, SHARED SCRIPT.

   Small, and it should stay that way. EVERY PAGE ON THIS SITE WORKS WITH
   JAVASCRIPT OFF: the FAQ is <details>/<summary>, the phone is a tel:
   link, the nav is a list, the stat band's numbers are text in the
   markup. Nothing here is load-bearing.

   WHAT IS HERE, AND WHY IT IS ALLOWED TO BE.

   Arrival motion, adopted 2026-09-10. The motion law in site.css's
   header was amended for it, and the amendment is narrow: an effect may
   fire ONCE, on a section's first arrival, and never again. A number
   counts because the number is real. A lane draws because the section it
   runs down is a road. Nothing loops, nothing re-triggers, nothing runs
   on load.

   THE RULE THAT SHAPES ALL OF THIS: NO ELEMENT IS EVER HIDDEN BY CSS
   ALONE. Every "from" state is added here, and only when the motion is
   actually going to run. So with JavaScript off, with
   prefers-reduced-motion set, or if this file throws on its first line,
   the page is complete and nothing is invisible waiting for a script
   that is not coming. The odometer in particular starts on the TRUE
   DIGITS and ends on them, so the number is right in every one of those
   cases.

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
     ARRIVAL MOTION
     --------------------------------------------------------------------- */

  var reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  var sections = [];

  /* ---------- The odometer ------------------------------------------
     IT READS ITS TARGET FROM THE MARKUP and nowhere else. Whoever
     refreshes the review count edits one number in the HTML; this
     follows it and needs no knowledge of the effect. There is no list of
     numbers in this file to keep in step, on purpose.

     The strip is [target, 0-9, target]: it starts on the true digit and
     lands on the true digit one revolution later. A wrong number is the
     cardinal sin on this site, and an odometer parked on 000 waiting to
     be scrolled to would be exactly the wrong kind of clever. */
  var ODO_STEP = 0.88;    /* .stat-n's line-height in site.css */
  var ODO_TRAVEL = 11;    /* cells from the armed digit to the landed one */

  function cell(d) {
    var s = document.createElement("span");
    s.textContent = String(d);
    return s;
  }

  function buildOdometer(el) {
    var value = el.textContent.trim();
    if (!/^\d+$/.test(value)) { return false; }
    var odo = document.createElement("span");
    odo.className = "odo";
    odo.setAttribute("aria-hidden", "true");
    for (var i = 0; i < value.length; i++) {
      var target = Number(value.charAt(i));
      var win = document.createElement("span");
      win.className = "odo-d";
      var strip = document.createElement("span");
      strip.className = "odo-strip";
      strip.appendChild(cell(target));
      for (var d = 0; d <= 9; d++) { strip.appendChild(cell(d)); }
      strip.appendChild(cell(target));
      strip.style.setProperty("--odo-end", (-ODO_TRAVEL * ODO_STEP).toFixed(3) + "em");
      strip.style.setProperty("--odo-delay", (i * 90) + "ms");
      win.appendChild(strip);
      odo.appendChild(win);
    }
    /* The rolling drum is decoration and is aria-hidden. The number
       itself still has to reach a screen reader, once, as a number. */
    var sr = document.createElement("span");
    sr.className = "sr-only";
    sr.textContent = value;
    el.textContent = "";
    el.appendChild(odo);
    el.appendChild(sr);
    return true;
  }

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
  var statband = document.querySelector(".statband");
  if (statband) {
    var numerals = statband.querySelectorAll(".stat-n");
    var rolled = false;
    for (var n = 0; n < numerals.length; n++) {
      if (buildOdometer(numerals[n])) { rolled = true; }
    }
    /* One of the three stats is a word rather than a number, by design.
       If none of them is a number there is nothing to roll. */
    if (rolled) { sections.push(statband); }
  }

  var steps = document.querySelector(".steps");
  if (steps) {
    buildLane(steps);
    sections.push(steps.closest("section") || steps);
    var t = null;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () { buildLane(steps); }, 150);
    });
  }

  if (!sections.length) { return; }

  /* THE FIRST OF THE TWO REDUCED-MOTION GUARDS. Nothing is armed, so
     nothing is ever in a "from" state: the number rests at its true
     value and the lane rests fully drawn. The second guard is the
     prefers-reduced-motion block in site.css. */
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
