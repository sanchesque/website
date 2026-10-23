// Language switch: remember the visitor's explicit choice (brand DESIGN.md
// §13) and send them back to it when they land on the Spanish home again.
// No automatic detection: both versions are first-class and crawlable.
(function () {
  var KEY = "lang";
  var switcher = document.querySelector(".lang-switch");
  if (switcher) {
    switcher.addEventListener("click", function () {
      try { localStorage.setItem(KEY, switcher.getAttribute("hreflang")); } catch (e) {}
    });
  }
  var onSpanishHome = document.documentElement.lang === "es";
  if (onSpanishHome && !location.hash) {
    try {
      if (localStorage.getItem(KEY) === "en") location.replace("en/");
    } catch (e) {}
  }
})();
