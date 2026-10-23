// Language switch: remember the visitor's explicit choice (brand DESIGN.md
// §13) and send them back to it when they land on a Spanish page again.
// The target is the page's own switch link, so it works on every page.
// No automatic detection: both versions are first-class and crawlable.
(function () {
  var KEY = "lang";
  var switcher = document.querySelector(".lang-switch");
  if (!switcher) return;
  switcher.addEventListener("click", function () {
    try { localStorage.setItem(KEY, switcher.getAttribute("hreflang")); } catch (e) {}
  });
  var onSpanish = document.documentElement.lang === "es";
  if (onSpanish && !location.hash) {
    try {
      if (localStorage.getItem(KEY) === "en") location.replace(switcher.href);
    } catch (e) {}
  }
})();
