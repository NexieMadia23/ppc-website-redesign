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

  /* ---------- Side rail expand/collapse/hide toggle ----------
     Mobile: start collapsed, auto-collapse on scroll, collapse after jumping to section, cycle expanded->collapsed->hidden->expanded
     Desktop: keep hover/keyboard preview with manual pinning */
  var rail = document.querySelector("[data-side-rail]");
  var railToggle = document.querySelector("[data-side-rail-toggle]");
  if (rail && railToggle) {
    var railList = rail.querySelector(".side-rail__list");
    var mqMobile = window.matchMedia("(max-width: 63.99rem)");
    var lastScrollY = window.scrollY || 0;
    var scrollTicking = false;

    function updateToggleAria() {
      if (rail.classList.contains("is-hidden")) {
        railToggle.setAttribute("aria-expanded", "false");
        railToggle.setAttribute("aria-label", "Show section navigation");
        return;
      }
      if (rail.classList.contains("is-expanded")) {
        railToggle.setAttribute("aria-expanded", "true");
        railToggle.setAttribute("aria-label", "Hide section labels");
        return;
      }
      railToggle.setAttribute("aria-expanded", "false");
      railToggle.setAttribute("aria-label", "Show section navigation");
    }

    if (mqMobile.matches) {
      if (!rail.classList.contains("is-expanded") && !rail.classList.contains("is-collapsed") && !rail.classList.contains("is-hidden")) {
        rail.classList.add("is-collapsed");
      }
    }

    railToggle.addEventListener("click", function () {
      if (mqMobile.matches) {
        if (rail.classList.contains("is-expanded")) {
          rail.classList.remove("is-expanded");
          rail.classList.add("is-collapsed");
          rail.classList.remove("is-hidden");
        } else if (rail.classList.contains("is-collapsed")) {
          rail.classList.remove("is-expanded");
          rail.classList.remove("is-collapsed");
          rail.classList.add("is-hidden");
        } else if (rail.classList.contains("is-hidden")) {
          rail.classList.remove("is-hidden");
          rail.classList.add("is-collapsed");
          rail.classList.remove("is-expanded");
        } else {
          rail.classList.add("is-expanded");
          rail.classList.remove("is-collapsed");
          rail.classList.remove("is-hidden");
        }
        updateToggleAria();
        return;
      }

      var shown = rail.classList.contains("is-expanded") ||
        (!rail.classList.contains("is-collapsed") &&
          (rail.matches(":hover") || (railList && railList.matches(":focus-within"))));
      rail.classList.toggle("is-expanded", !shown);
      rail.classList.toggle("is-collapsed", shown);
      railToggle.setAttribute("aria-expanded", shown ? "false" : "true");
      railToggle.removeAttribute("aria-label");
    });

    if (mqMobile.matches && railList) {
      railList.querySelectorAll(".side-rail__link").forEach(function (link) {
        link.addEventListener("click", function () {
          window.setTimeout(function () {
            if (mqMobile.matches && rail.classList.contains("is-expanded")) {
              rail.classList.remove("is-expanded");
              rail.classList.add("is-collapsed");
              rail.classList.remove("is-hidden");
              updateToggleAria();
            }
          }, 150);
        });
      });

      window.addEventListener("scroll", function () {
        if (scrollTicking) { return; }
        scrollTicking = true;
        window.requestAnimationFrame(function () {
          var currentY = window.scrollY || 0;
          if (Math.abs(currentY - lastScrollY) > 8) {
            if (mqMobile.matches && rail.classList.contains("is-expanded")) {
              rail.classList.remove("is-expanded");
              rail.classList.add("is-collapsed");
              rail.classList.remove("is-hidden");
              updateToggleAria();
            }
            lastScrollY = currentY;
          }
          scrollTicking = false;
        });
      }, { passive: true });
    }

    updateToggleAria();
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

  /* ---------- Prototype contact form ----------
     There is no backend yet, so the form never leaves the page: the browser
     validates it, then we show a confirmation. Without JavaScript the POST
     simply re-renders the page, so nothing errors either way. */
  document.querySelectorAll("[data-prototype-form]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var status = form.querySelector("[data-form-status]");
      if (!status) { return; }
      var nameField = form.querySelector("#contact-name");
      var firstName = nameField ? nameField.value.trim().split(/\s+/)[0] : "";
      status.textContent = "";
      var strong = document.createElement("strong");
      strong.textContent = firstName ? "Thanks, " + firstName + "." : "Thanks.";
      status.appendChild(strong);
      status.appendChild(document.createTextNode(
        " On the live site this message would be routed to the right office. " +
        "This is a prototype, so nothing was sent."
      ));
      status.hidden = false;
      status.focus();
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

  /* ---------- Page-section scrollspy ----------
     Drives the glass side rail (the only section navigation at every width):
     every link in a [data-spy] container points at a section id, and the first
     section in the reading band gets aria-current. */
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
