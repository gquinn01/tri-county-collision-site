/* ===========================================================================
   MOTION SAMPLER SCRIPT. CANDIDATES ONLY. NOTHING HERE SHIPS.

   docs/assets/site.js is deliberately almost empty and says so. This
   file is not a proposal to change that; it exists so the candidates in
   motion.css can be judged on the real page.

   THE ONE RULE THAT SHAPES ALL OF IT: NO ELEMENT IS EVER HIDDEN BY CSS
   ALONE. Every "from" state is applied here, by adding .mo-armed, and
   only when motion is actually going to run. So with JavaScript off, or
   with reduced motion set, or if this file throws on line one, the page
   is exactly the production page with nothing invisible waiting for a
   script that is not coming.

   NOTHING ANIMATES ON LOAD. Every entrance waits for an
   IntersectionObserver and runs once, then unobserves itself.
   =========================================================================== */

(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  var groups = [];

  function reduced() {
    return reduceMQ.matches || root.classList.contains("mo-force-reduce");
  }

  /* ---------- A. the odometer ---------------------------------------
     The strip is [target, 0..9, target]. It starts on the TRUE DIGIT and
     lands on the true digit, one full revolution later, so the page
     never displays a number that is not the real one, not even for a
     frame while it waits to be scrolled into view. On a site where a
     wrong number is the cardinal sin, an odometer parked on 000 would
     be exactly the wrong kind of clever. */
  var ODO_STEP = 0.88;          /* .stat-n's line-height in site.css */
  var ODO_TRAVEL = 11;          /* cells from the armed digit to the landed one */

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
      var window_ = document.createElement("span");
      window_.className = "odo-d";
      var strip = document.createElement("span");
      strip.className = "odo-strip";
      strip.appendChild(cell(target));
      for (var d = 0; d <= 9; d++) { strip.appendChild(cell(d)); }
      strip.appendChild(cell(target));
      strip.style.setProperty("--odo-end", (-ODO_TRAVEL * ODO_STEP).toFixed(3) + "em");
      strip.style.setProperty("--odo-delay", (i * 90) + "ms");
      window_.appendChild(strip);
      odo.appendChild(window_);
    }
    /* The rolling drum is decoration. The number itself still has to
       reach a screen reader, once, as a number. */
    var sr = document.createElement("span");
    sr.className = "mo-sr";
    sr.textContent = value;
    el.textContent = "";
    el.appendChild(odo);
    el.appendChild(sr);
    return true;
  }

  /* ---------- C. the lift layers ------------------------------------
     Two painted layers per card, because the shadow and the base rule
     both have to change without animating a shadow or a colour. Both
     are aria-hidden furniture. */
  function addLiftLayers(el) {
    el.classList.add("mo-lift");
    ["mo-shade", "mo-rule"].forEach(function (cls) {
      var layer = document.createElement("span");
      layer.className = cls;
      layer.setAttribute("aria-hidden", "true");
      el.appendChild(layer);
    });
  }

  /* ---------- D. the lane -------------------------------------------
     One dash per gap between steps, measured rather than guessed,
     because the gap's position depends on how tall each card wrapped.
     Single column only: above 720px .steps is two or three columns and
     a line from 01 to 06 is not a road, so nothing is drawn. */
  function buildLane(steps) {
    var lane = steps.querySelector(".mo-lane");
    if (!lane) {
      lane = document.createElement("span");
      lane.className = "mo-lane";
      lane.setAttribute("aria-hidden", "true");
      steps.classList.add("mo-lane-host");
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
      dash.className = "mo-dash";
      dash.style.top = (top + 3) + "px";
      dash.style.height = (height - 6) + "px";
      dash.style.setProperty("--dash-delay", (i * 110) + "ms");
      lane.appendChild(dash);
    }
  }

  /* ---------- arming, releasing, replaying --------------------------- */
  function moving(g) {
    return g.el.querySelectorAll(".odo-strip, .mo-stamp, .mo-dash");
  }

  function arm(g) {
    if (reduced()) { return; }
    g.el.classList.add("mo-armed");
  }

  function release(g) {
    g.el.classList.add("mo-in");
  }

  /* Replay has to put the "from" state back WITHOUT animating back to
     it, or every effect plays in reverse on the way to its own encore.
     Kill the transition, reset, force a reflow to commit it, restore. */
  function reset(g) {
    var parts = moving(g);
    for (var i = 0; i < parts.length; i++) { parts[i].style.transition = "none"; }
    g.el.classList.remove("mo-in", "mo-armed");
    void g.el.offsetHeight;
    for (var j = 0; j < parts.length; j++) { parts[j].style.transition = ""; }
  }

  function observe() {
    if (!("IntersectionObserver" in window)) {
      groups.forEach(release);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        var g = groups.filter(function (x) { return x.el === entry.target; })[0];
        if (g) { release(g); }
        io.unobserve(entry.target);
      });
    }, { threshold: 0.25 });
    groups.forEach(function (g) { io.observe(g.el); });
    return io;
  }

  /* ---------- wiring ------------------------------------------------- */
  var statband = document.querySelector(".statband");
  if (statband) {
    var numerals = statband.querySelectorAll(".stat-n");
    for (var i = 0; i < numerals.length; i++) {
      /* A number rolls. The one stat that is a word gets stamped. */
      if (!buildOdometer(numerals[i])) {
        numerals[i].classList.add("mo-stamp");
      }
    }
    groups.push({ el: statband, name: "A odometer + B stamp" });
  }

  var cards = document.querySelectorAll(".card, .step, .svc");
  for (var c = 0; c < cards.length; c++) { addLiftLayers(cards[c]); }

  var steps = document.querySelector(".steps");
  if (steps) {
    buildLane(steps);
    groups.push({ el: steps.closest("section") || steps, name: "D lane" });
    /* The gap positions move when the text rewraps. Rebuild on resize,
       debounced, and only ever five measurements. */
    var t = null;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        buildLane(steps);
        if (steps.closest("section").classList.contains("mo-in") && !reduced()) {
          var d = steps.querySelectorAll(".mo-dash");
          for (var k = 0; k < d.length; k++) { d[k].style.transition = "none"; }
          void steps.offsetHeight;
          for (var m = 0; m < d.length; m++) { d[m].style.transition = ""; }
        }
      }, 150);
    });
  }

  groups.forEach(arm);
  var io = observe();

  /* ---------- the sampler bar. Not a candidate. ---------------------- */
  var bar = document.querySelector(".mo-bar");
  if (!bar) { return; }
  var state = bar.querySelector(".mo-state");

  function say() {
    state.textContent = reduced()
      ? "reduced motion ON, nothing will animate"
      : groups.length + " groups armed";
  }

  bar.querySelector(".mo-replay").addEventListener("click", function () {
    groups.forEach(reset);
    if (steps) { buildLane(steps); }
    groups.forEach(arm);
    /* Two frames: one to commit the armed state, one to release from it. */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { groups.forEach(release); });
    });
    say();
  });

  bar.querySelector(".mo-reduce input").addEventListener("change", function () {
    root.classList.toggle("mo-force-reduce", this.checked);
    groups.forEach(reset);
    groups.forEach(arm);
    groups.forEach(release);
    say();
  });

  reduceMQ.addEventListener("change", say);
  say();
  void io;
})();
