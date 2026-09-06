/* ===========================================================================
   TRI-COUNTY COLLISION, SHARED SCRIPT.

   Deliberately almost empty, and it should stay that way. Every page on this
   site works with JavaScript off: the FAQ is <details>/<summary>, the phone
   is a tel: link, the nav is a list. Nothing here is load-bearing.

   WHAT IS NOT HERE, on purpose:

   - No animation. Motion is evidence, not costume, and this page has no
     evidence that needs moving. See the header of site.css.
   - No CallRail snippet. It gets added at cutover, in the same pass as the
     GA4 property. CallRail swaps numbers into the rendered page at runtime,
     which is why the tracking number is not in this repo's source and must
     never be pasted into it.
   - No form handler yet. The form's fields, its endpoint and what it says
     after a send are all still with the owner, and the endpoint will be in
     the CLIENT'S account. When it lands, the submit handler goes here and
     calls preventDefault(), which is exactly why the GA4 form_submit event
     has to be sent explicitly: enhanced measurement cannot see a submit that
     never navigates.
   =========================================================================== */

(function () {
  "use strict";

  /* The footer year, so the site never tells a visitor it stopped being
     maintained in a year that has passed. The markup carries a real year as
     its fallback, so a reader with JavaScript off still sees one. */
  var y = document.querySelector("[data-year]");
  if (y) { y.textContent = String(new Date().getFullYear()); }
})();
