// Language switch: remember the visitor's explicit choice (brand DESIGN.md
// §13). The redirect itself lives in lang-redirect.js, in the <head>.
// No automatic detection: both versions are first-class and crawlable.
(function () {
  var switcher = document.querySelector(".lang-switch");
  if (!switcher) return;
  switcher.addEventListener("click", function () {
    try { localStorage.setItem("lang", switcher.getAttribute("hreflang")); } catch (e) {}
  });
})();
