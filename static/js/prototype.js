/* PROTOTYPE ONLY - interactive behaviours for the design demo.
   Remove this file (and the PROTOTYPE sections in base.css and
   content/context_processors.py) when the redesign is merged into main.
   Every feature degrades gracefully without JavaScript. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Emergency quick-dial sheet ---------- */
  var dialog = document.querySelector("[data-emergency-dialog]");
  var openButton = document.querySelector("[data-emergency-open]");
  if (dialog && openButton && typeof dialog.showModal === "function") {
    openButton.addEventListener("click", function (event) {
      event.preventDefault(); /* without JS the link goes to the emergency page */
      dialog.showModal();
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
      backToTop.hidden = window.scrollY < 600;
    };
    window.addEventListener("scroll", updateBackToTop, { passive: true });
    updateBackToTop();
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* ---------- Side rail toggle (pins the labels open - meant for touch) ---------- */
  var rail = document.querySelector("[data-side-rail]");
  var railToggle = document.querySelector("[data-side-rail-toggle]");
  if (rail && railToggle) {
    railToggle.addEventListener("click", function () {
      var expanded = rail.classList.toggle("is-expanded");
      railToggle.setAttribute("aria-expanded", expanded ? "true" : "false");
    });
  }

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

  /* ---------- Page-section scrollspy ----------
     Drives both the sticky bar and the glass side rail: every link in a
     [data-spy] container points at a section id, and the first section in the
     reading band gets aria-current (all links to it, in both containers). */
  var spyLinks = document.querySelectorAll("[data-spy] a[href^='#']");
  if (spyLinks.length) {
    var spyTargets = {};
    var spyOrder = [];
    spyLinks.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      var section = id ? document.getElementById(id) : null;
      if (!section) { return; }
      if (!spyTargets[id]) {
        spyTargets[id] = { section: section, links: [] };
        spyOrder.push(id);
      }
      spyTargets[id].links.push(link);
    });

    var setCurrent = function (activeId) {
      spyOrder.forEach(function (id) {
        spyTargets[id].links.forEach(function (link) {
          if (id === activeId) { link.setAttribute("aria-current", "location"); }
          else { link.removeAttribute("aria-current"); }
        });
      });
    };

    if (spyOrder.length) {
      var inBand = {};
      var spyObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) { inBand[entry.target.id] = entry.isIntersecting; });
        var activeId = null;
        spyOrder.forEach(function (id) {
          if (activeId === null && inBand[id]) { activeId = id; }
        });
        setCurrent(activeId);
      }, { rootMargin: "-35% 0px -55% 0px" });
      spyOrder.forEach(function (id) { spyObserver.observe(spyTargets[id].section); });
      setCurrent(spyOrder[0]);
    }
  }
})();
