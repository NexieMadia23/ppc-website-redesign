/* Public-site enhancements.
   Voice search, the FAQ assistant, the anonymous toggle, the FAQ filter, and
   AJAX feedback. Everything degrades gracefully: without JavaScript voice
   search is absent and the feedback form still posts normally. */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(selector, scope) { return (scope || document).querySelector(selector); }
  function $$(selector, scope) {
    return Array.prototype.slice.call((scope || document).querySelectorAll(selector));
  }

  // Keep Tab inside an open panel. Not modal: the page behind stays readable,
  // but focus cannot wander away while the panel is open.
  function trapFocus(container) {
    container.addEventListener("keydown", function (event) {
      if (event.key !== "Tab") { return; }
      var items = $$(
        'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
        container
      ).filter(function (item) { return item.offsetParent !== null; });
      if (!items.length) { return; }
      var first = items[0];
      var last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* Chatbot (keyword FAQ matching, no AI service)                      */
  /* ------------------------------------------------------------------ */
  var chat = $("[data-chat-widget]");
  if (chat) {
    var chatOpen = $("[data-chat-open]", chat);
    var chatPanel = $("[data-chat-panel]", chat);
    var chatClose = $("[data-chat-close]", chat);
    var chatLog = $("[data-chat-log]", chat);
    var chatForm = $("[data-chat-form]", chat);
    var chatInput = $("[data-chat-input]", chat);
    var endpoint = chat.getAttribute("data-endpoint") || "/faq/ask/";
    var busy = false;

    function scrollChat() {
      if (chatLog) { chatLog.scrollTop = chatLog.scrollHeight; }
    }

    function addMessage(role, text, url, linkLabel) {
      var wrap = document.createElement("div");
      wrap.className = "chat-msg chat-msg--" + role;
      var p = document.createElement("p");
      p.textContent = text;
      wrap.appendChild(p);
      if (url) {
        var link = document.createElement("a");
        link.className = "chat-msg__link";
        link.href = url;
        link.textContent = linkLabel || "Open";
        wrap.appendChild(link);
      }
      chatLog.appendChild(wrap);
      scrollChat();
      return wrap;
    }

    function showTyping() {
      var wrap = document.createElement("div");
      wrap.className = "chat-msg chat-msg--bot chat-typing";
      wrap.setAttribute("aria-label", "Assistant is typing");
      wrap.innerHTML = "<span></span><span></span><span></span>";
      chatLog.appendChild(wrap);
      scrollChat();
      return wrap;
    }

    function ask(message) {
      var text = (message || "").trim();
      if (!text || busy) { return; }
      busy = true;
      addMessage("user", text);
      var typing = showTyping();

      fetch(endpoint + "?q=" + encodeURIComponent(text), {
        headers: { Accept: "application/json" },
      })
        .then(function (response) {
          if (!response.ok) { throw new Error("Request failed"); }
          return response.json();
        })
        .then(function (data) {
          typing.remove();
          addMessage("bot", data.answer, data.url, data.link_label);
        })
        .catch(function () {
          typing.remove();
          addMessage(
            "bot",
            "Sorry, I could not reach the help desk. Please browse the FAQ or file a request.",
            "/faq/",
            "Browse the FAQ"
          );
        })
        .then(function () { busy = false; });
    }

    function openChat() {
      chatPanel.hidden = false;
      chat.classList.add("is-open");
      chatOpen.setAttribute("aria-expanded", "true");
      chatInput.focus();
    }
    function closeChat() {
      chatPanel.hidden = true;
      chat.classList.remove("is-open");
      chatOpen.setAttribute("aria-expanded", "false");
      chatOpen.focus();
    }

    trapFocus(chatPanel);

    chatOpen.addEventListener("click", function () {
      if (chatPanel.hidden) { openChat(); } else { closeChat(); }
    });
    chatClose.addEventListener("click", closeChat);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !chatPanel.hidden) { closeChat(); }
    });

    chatForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var value = chatInput.value;
      chatInput.value = "";
      ask(value);
    });

    $$("[data-chat-suggest]", chat).forEach(function (button) {
      button.addEventListener("click", function () {
        ask(button.getAttribute("data-chat-suggest"));
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* Voice search (Web Speech API)                                      */
  /* ------------------------------------------------------------------ */
  var voiceButton = $("[data-voice-search]");
  var searchForm = $("[data-search-form]");
  var searchInput = $("[data-search-input]");
  var voiceStatus = $("[data-voice-status]");
  var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (voiceButton && Recognition && searchForm && searchInput) {
    voiceButton.hidden = false;
    var recognition = new Recognition();
    recognition.lang = "en-PH";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    var listening = false;

    function setVoiceStatus(text) {
      if (voiceStatus) { voiceStatus.textContent = text; }
    }

    voiceButton.addEventListener("click", function () {
      if (listening) { recognition.stop(); return; }
      try {
        recognition.start();
      } catch (error) {
        setVoiceStatus("Voice search is already starting.");
      }
    });

    recognition.addEventListener("start", function () {
      listening = true;
      voiceButton.classList.add("is-listening");
      setVoiceStatus("Listening… speak now.");
    });
    recognition.addEventListener("result", function (event) {
      var transcript = event.results[0][0].transcript;
      searchInput.value = transcript;
      setVoiceStatus("Searching for “" + transcript + "”…");
      window.setTimeout(function () { searchForm.submit(); }, 250);
    });
    recognition.addEventListener("error", function (event) {
      if (event.error === "not-allowed") {
        setVoiceStatus("Microphone access was blocked. Allow it in your browser settings.");
      } else if (event.error === "no-speech") {
        setVoiceStatus("I did not hear anything. Try again.");
      } else {
        setVoiceStatus("Voice search did not work. You can still type your question.");
      }
    });
    recognition.addEventListener("end", function () {
      listening = false;
      voiceButton.classList.remove("is-listening");
    });
  } else if (voiceStatus) {
    voiceStatus.textContent = "Voice search is not supported by this browser. Please type instead.";
  }

  /* ------------------------------------------------------------------ */
  /* Anonymous complaint toggle                                         */
  /* ------------------------------------------------------------------ */
  var anonymous = document.getElementById("id_is_anonymous");
  var contactFields = $("[data-contact-fields]");
  if (anonymous && contactFields) {
    var syncAnonymous = function () {
      var hide = anonymous.checked;
      contactFields.classList.toggle("is-disabled", hide);
      $$("input, select, textarea", contactFields).forEach(function (field) {
        field.disabled = hide;
      });
      var note = $(".form-fieldset__off", contactFields);
      if (note) { note.hidden = !hide; }
    };
    anonymous.addEventListener("change", syncAnonymous);
    syncAnonymous();
  }

  /* ------------------------------------------------------------------ */
  /* Stepped forms (Sumbungan request form)                              */
  /* ------------------------------------------------------------------ */
  // Splits a long form into chunks: one fieldset per step behind a
  // progress tracker. Without JavaScript every fieldset stays visible,
  // so the plain server-validated form still works - the wizard only
  // chunks the view, it never owns the validation.
  $$("form[data-steps]").forEach(function (form) {
    var steps = $$("[data-step]", form);
    var tabs = $$("[data-steps-progress] li", form);
    if (steps.length < 2) { return; }
    var current = -1;

    function activate(index, focus) {
      current = index;
      steps.forEach(function (step, i) {
        step.hidden = i !== index;
        step.classList.toggle("is-active", i === index);
      });
      tabs.forEach(function (tab, i) {
        tab.classList.toggle("is-current", i === index);
        tab.classList.toggle("is-done", i < index);
        if (i === index) { tab.setAttribute("aria-current", "step"); }
        else { tab.removeAttribute("aria-current"); }
      });
      if (focus) {
        // Land keyboard and screen reader focus on the new chunk instead
        // of leaving it on the button that was just pressed.
        steps[index].setAttribute("tabindex", "-1");
        steps[index].focus();
      }
    }

    // The step buttons mean nothing without JS, so the template ships
    // them hidden; turn them on now that the wizard owns navigation.
    $$("[data-step-next], [data-step-back]", form).forEach(function (button) {
      button.hidden = false;
    });

    // Open on the first chunk that carries a server-side error, so a
    // failed submit puts the visitor in front of what they must fix.
    var errored = steps.findIndex(function (step) {
      return !!step.querySelector(".field-error, .form-error");
    });
    activate(errored >= 0 ? errored : 0, false);

    form.addEventListener("click", function (event) {
      var forward = event.target.closest("[data-step-next]");
      var back = event.target.closest("[data-step-back]");
      if (!forward && !back) { return; }
      event.preventDefault();
      var next = forward ? Math.min(current + 1, steps.length - 1)
                         : Math.max(current - 1, 0);
      if (next !== current) { activate(next, true); }
    });

    // Friendly photo feedback: file inputs give no visible list by default.
    var fileInput = form.querySelector('input[type="file"][multiple]');
    var fileSummary = form.querySelector("[data-file-summary]");
    if (fileInput && fileSummary) {
      fileInput.addEventListener("change", function () {
        var files = Array.prototype.slice.call(fileInput.files || []);
        if (!files.length) {
          fileSummary.hidden = true;
          fileSummary.textContent = "";
          return;
        }
        var maxFiles = parseInt(fileInput.getAttribute("data-max-files"), 10) || 3;
        var maxBytes = 5 * 1024 * 1024;
        var problems = [];
        if (files.length > maxFiles) {
          problems.push("Choose up to " + maxFiles + " photos.");
        }
        files.forEach(function (file) {
          if (file.size > maxBytes) {
            problems.push(file.name + " is larger than 5 MB.");
          }
        });
        fileSummary.hidden = false;
        fileSummary.classList.toggle("is-warning", problems.length > 0);
        fileSummary.textContent = problems.length
          ? problems.join(" ")
          : files.length + " photo" + (files.length === 1 ? "" : "s") + " ready: " +
            files.map(function (file) { return file.name; }).join(", ");
      });
    }
  });

  /* ------------------------------------------------------------------ */
  /* FAQ filter                                                         */
  /* ------------------------------------------------------------------ */
  var faqFilter = $("[data-faq-filter]");
  if (faqFilter) {
    var faqItems = $$("[data-faq-item]");
    var faqGroups = $$("[data-faq-groups] .faq-group");
    var faqCount = $("[data-faq-count]");
    var faqEmpty = $("[data-faq-empty]");
    var total = faqItems.length;

    var filterFaqs = function () {
      var term = faqFilter.value.trim().toLowerCase();
      var visible = 0;
      faqItems.forEach(function (item) {
        var match = !term || item.textContent.toLowerCase().indexOf(term) > -1;
        item.hidden = !match;
        if (match) { visible += 1; }
      });
      faqGroups.forEach(function (group) {
        var any = $$("[data-faq-item]", group).some(function (item) { return !item.hidden; });
        group.hidden = !any;
      });
      if (faqCount) {
        faqCount.textContent = visible + " of " + total + " questions";
      }
      if (faqEmpty) { faqEmpty.hidden = visible > 0; }
    };
    faqFilter.addEventListener("input", filterFaqs);
    filterFaqs();
  }

  /* ------------------------------------------------------------------ */
  /* Feedback: live character counter                                    */
  /* ------------------------------------------------------------------ */
  // Separate from the AJAX block so the counter also works in browsers
  // without fetch. Stays silent for screen readers (aria-live off).
  $$("[data-feedback-form]").forEach(function (form) {
    var field = $("[data-feedback-comment]", form);
    var counter = $("[data-feedback-counter]", form);
    if (!field || !counter) { return; }
    var limit = parseInt(field.getAttribute("maxlength"), 10) || 2000;
    var NEAR = limit * 0.9;

    function syncCounter() {
      var used = field.value.length;
      counter.textContent = used + " / " + limit;
      counter.classList.toggle("is-near", used >= NEAR && used < limit);
      counter.hidden = used === 0 && document.activeElement !== field;
    }

    field.addEventListener("input", syncCounter);
    field.addEventListener("focus", syncCounter);
    field.addEventListener("blur", syncCounter);
    syncCounter();
  });

  /* ------------------------------------------------------------------ */
  /* Feedback: upgrade the normal POST to AJAX                          */
  /* ------------------------------------------------------------------ */
  $$("[data-feedback-form]").forEach(function (form) {
    if (!window.fetch) { return; }
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var status = $("[data-feedback-status]", form);
      var submitter = event.submitter;
      var data = new FormData(form);
      if (submitter && submitter.name) {
        data.set(submitter.name, submitter.value);
      }
      if (status) { status.textContent = "Sending…"; }

      fetch(form.action, {
        method: "POST",
        body: data,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          Accept: "application/json",
        },
      })
        .then(function (response) { return response.json(); })
        .then(function (result) {
          if (!result.ok) { throw new Error(result.error || "Could not save feedback"); }
          var field = $(".field", form);
          var actions = $(".page-feedback__actions", form);
          if (field) { field.hidden = true; }
          if (actions) { actions.hidden = true; }
          if (status) {
            status.textContent = result.message;
            status.classList.add("is-success");
          }
        })
        .catch(function () {
          if (status) {
            status.textContent = "Sorry, feedback could not be sent. Please try again.";
          }
        });
    });
  });

  /* ------------------------------------------------------------------ */
  /* Button click ripple                                                */
  /* ------------------------------------------------------------------ */
  // One listener on the document covers every current and future control,
  // including the quick-reply chips inside the chat panel. The span is
  // purely decorative, so it is aria-hidden and never announced.
  var RIPPLE_HOSTS =
    ".btn, .header-cta, .emergency-fab, .chat-fab, .back-to-top, .emergency-sheet__close";
  document.addEventListener("click", function (event) {
    var host = event.target.closest && event.target.closest(RIPPLE_HOSTS);
    if (!host || reduceMotion) { return; }
    var rect = host.getBoundingClientRect();
    var x = rect.width / 2;
    var y = rect.height / 2;
    // Keyboard-triggered clicks carry no pointer coordinates: centre them.
    if (event.detail > 0 && event.clientX) {
      x = event.clientX - rect.left;
      y = event.clientY - rect.top;
    }
    var size = Math.max(rect.width, rect.height) * 2;
    var ripple = document.createElement("span");
    ripple.className = "ripple";
    ripple.setAttribute("aria-hidden", "true");
    ripple.style.width = size + "px";
    ripple.style.height = size + "px";
    ripple.style.left = (x - size / 2) + "px";
    ripple.style.top = (y - size / 2) + "px";
    host.appendChild(ripple);
    ripple.addEventListener("animationend", function () { ripple.remove(); });
    // Safety net in case the animation is interrupted before it can end.
    window.setTimeout(function () { ripple.remove(); }, 700);
  });

  /* ------------------------------------------------------------------ */
  /* Main navigation dropdowns                                          */
  /* ------------------------------------------------------------------ */
  // The top-level link still opens its page. The button beside it opens a
  // short list of sections on the same page, so every route keeps working.
  var navMenus = $$(".site-nav__item--menu");

  function closeNavMenus(except) {
    navMenus.forEach(function (item) {
      if (item === except) { return; }
      item.classList.remove("is-open");
      var toggle = $("[data-nav-toggle]", item);
      if (toggle) { toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  navMenus.forEach(function (item) {
    var toggle = $("[data-nav-toggle]", item);
    var menu = $("[data-nav-menu]", item);
    if (!toggle || !menu) { return; }

    toggle.addEventListener("click", function () {
      var open = !item.classList.contains("is-open");
      closeNavMenus(item);
      item.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    item.addEventListener("keydown", function (event) {
      if (event.key !== "Escape" || !item.classList.contains("is-open")) { return; }
      item.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    });
  });

  if (navMenus.length) {
    document.addEventListener("click", function (event) {
      if (!event.target.closest(".site-nav__item--menu")) { closeNavMenus(); }
    });
    document.addEventListener("focusin", function (event) {
      if (!event.target.closest(".site-nav__item--menu")) { closeNavMenus(); }
    });
  }

  /* ------------------------------------------------------------------ */
  /* Small niceties                                                     */
  /* ------------------------------------------------------------------ */
  // Open a closed FAQ item when a hash points at it (e.g. from search).
  if (window.location.hash) {
    var target = document.querySelector(window.location.hash);
    if (target && target.tagName === "DETAILS") { target.open = true; }
  }

  // Reveal-on-scroll already lives in prototype.js; skip the animation when the
  // visitor prefers reduced motion.
  if (reduceMotion) {
    $$(".reveal").forEach(function (element) { element.classList.add("is-visible"); });
  }
})();
