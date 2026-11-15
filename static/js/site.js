/* Site behaviours: the emergency quick-dial sheet, mobile menu, FAQ chat
   assistant, scrollspy, count-up statistics, the Sumbungan form steps, and
   map consent. Every feature degrades gracefully without JavaScript. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Emergency quick-dial sheet ---------- */
  var dialog = document.querySelector("[data-emergency-dialog]");
  var openButtons = document.querySelectorAll("[data-emergency-open]");
  if (dialog && openButtons.length && typeof dialog.showModal === "function") {
    openButtons.forEach(function (openButton) {
      openButton.addEventListener("click", function (event) {
        event.preventDefault(); /* without JS the link goes to the emergency page */
        dialog.showModal();
      });
    });
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog || event.target.closest("[data-emergency-close]")) {
        dialog.close();
      }
    });
  }

  /* ---------- Dismissible advisory (remembered in this browser) ---------- */
  var advisory = document.querySelector("[data-advisory]");
  var advisoryClose = document.querySelector("[data-advisory-close]");
  if (advisory && advisoryClose) {
    try {
      if (localStorage.getItem("ppc-advisory-dismissed") === "1") {
        advisory.hidden = true;
      }
    } catch (error) { /* storage unavailable: banner just shows every visit */ }
    advisoryClose.addEventListener("click", function () {
      advisory.hidden = true;
      try { localStorage.setItem("ppc-advisory-dismissed", "1"); } catch (error) {}
    });
  }

  /* ---------- Back to top ---------- */
  var backToTop = document.querySelector("[data-back-to-top]");
  if (backToTop) {
    var updateBackToTop = function () {
      backToTop.hidden = window.scrollY < 1200;
    };
    window.addEventListener("scroll", updateBackToTop, { passive: true });
    updateBackToTop();
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* ---------- Google Map, loaded only on request ----------
     No iframe is in the HTML, so a page view sends nothing to Google. The
     button removes itself with the consent panel and inserts the map in the
     same space; keyboard focus moves to the iframe title. Without JS the
     button stays hidden and the "Open in Google Maps" link is the fallback. */
  document.querySelectorAll("[data-map-load]").forEach(function (button) {
    var panel = button.closest("[data-map-consent]");
    if (!panel) { return; }
    button.hidden = false;
    button.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.src = button.getAttribute("data-src");
      frame.title = button.getAttribute("data-title") || "Map";
      frame.loading = "eager";
      frame.referrerPolicy = "no-referrer";
      panel.replaceWith(frame);
      frame.focus();
    });
  });

  if (!("IntersectionObserver" in window)) {
    return; /* older browsers: skip animations, everything stays usable */
  }

  /* ---------- Count-up stats (Underground River facts) ---------- */
  var stats = document.querySelectorAll("[data-countup]");
  if (stats.length) {
    var animateStat = function (element) {
      var raw = element.getAttribute("data-value");
      var target = parseFloat(raw);
      var suffix = element.getAttribute("data-suffix") || "";
      var decimals = (raw.split(".")[1] || "").length;
      if (reduceMotion) { return; } /* leave the final value already rendered */
      var startTime = null;
      var duration = 1400;
      var tick = function (timestamp) {
        if (startTime === null) { startTime = timestamp; }
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3); /* ease-out cubic */
        element.textContent = (target * eased).toFixed(decimals) + suffix;
        if (progress < 1) {
          window.requestAnimationFrame(tick);
        } else {
          element.textContent = target.toFixed(decimals) + suffix;
        }
      };
      window.requestAnimationFrame(tick);
    };
    var statObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateStat(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.6 });
    stats.forEach(function (stat) { statObserver.observe(stat); });
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length) {
    if (reduceMotion) {
      reveals.forEach(function (element) { element.classList.add("is-visible"); });
    } else {
      var revealObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 });
      reveals.forEach(function (element) { revealObserver.observe(element); });
    }
  }

})();
