// Runs blocking in the <head> of Spanish pages, before paint: a visitor
// who chose English (key "lang", set by lang.js on click) goes straight to
// the English alternate, so no flash and no analytics hit on this page.
(function () {
  try {
    if (location.hash || localStorage.getItem("lang") !== "en") return;
    var alt = document.querySelector('link[rel="alternate"][hreflang="en"]');
    // Path only, so previews and localhost stay on their own host.
    if (alt) location.replace(new URL(alt.href).pathname);
  } catch (e) {}
})();
