/* ===========================================================================
   MOTION SAMPLER SCRIPT. TWO CANDIDATES LEFT, BOTH UNDECIDED.

   A and B were cut and deleted. C was adopted into docs/assets/site.css
   and is PURE CSS THERE, with no script at all: the sampler's version
   used JavaScript to inject its two layers, and the shipped version uses
   ::before and ::after instead, so the lift works with JavaScript off.
   Nothing in this file touches it.

   What is left needs script for one reason only: the lane's dashes sit
   in the gaps between step cards, and where those gaps fall depends on
   how the text wrapped. Five measurements, once, plus a debounced
   recount on resize.

   NO ELEMENT IS EVER HIDDEN BY CSS ALONE. The "from" state is applied
   here, and only when the motion will actually run.
   =========================================================================== */

(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  var groups = [];

  function reduced() {
    return reduceMQ.matches || root.classList.contains("mo-force-reduce");
  }

  /* ---------- D. the lane -------------------------------------------
     One dash per gap, measured rather than guessed. Single column only:
     above 720px .steps is two or three columns and a line from 01 to 06
     is not a road, so nothing is drawn. */
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
  function moving(g) { return g.el.querySelectorAll(".mo-dash"); }

  function arm(g) {
    if (reduced()) { return; }
    g.el.classList.add("mo-armed");
  }

  function release(g) { g.el.classList.add("mo-in"); }

  /* Replay has to put the "from" state back WITHOUT animating back to
     it, or the lane un-paints itself on the way to its own encore. Kill
     the transition, reset, force a reflow to commit it, restore. */
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
      return null;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        groups.forEach(function (g) { if (g.el === entry.target) { release(g); } });
        io.unobserve(entry.target);
      });
    }, { threshold: 0.25 });
    groups.forEach(function (g) { io.observe(g.el); });
    return io;
  }

  /* ---------- wiring ------------------------------------------------- */
  var steps = document.querySelector(".steps");
  if (steps) {
    buildLane(steps);
    groups.push({ el: steps.closest("section") || steps, name: "D lane" });
    var t = null;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () { buildLane(steps); }, 150);
    });
  }

  groups.forEach(arm);
  observe();

  /* ---------- the sampler bar. Not a candidate. ---------------------- */
  var bar = document.querySelector(".mo-bar");
  if (!bar) { return; }
  var state = bar.querySelector(".mo-state");

  function say() {
    state.textContent = reduced()
      ? "reduced motion ON, nothing will animate"
      : "D armed. C ships from site.css, hover a card. E is CSS only.";
  }

  bar.querySelector(".mo-replay").addEventListener("click", function () {
    groups.forEach(reset);
    if (steps) { buildLane(steps); }
    groups.forEach(arm);
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
})();
