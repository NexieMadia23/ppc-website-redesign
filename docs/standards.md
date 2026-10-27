# Standards baseline

Every feature is reviewed against these three references before it is merged.
They are acceptance criteria, not background reading.

## Sources

1. Nielsen, J. (1994). *10 usability heuristics for user interface design.*
   Nielsen Norman Group. https://www.nngroup.com/articles/ten-usability-heuristics/
2. Republic Act No. 10173. (2012). *Data Privacy Act of 2012.*
   https://privacy.gov.ph/data-privacy-act/
3. World Wide Web Consortium. (2023). *Web Content Accessibility Guidelines
   (WCAG) 2.2.* https://www.w3.org/TR/WCAG22/

## Definition of done

A change ships only when all of these are true:

- keyboard-only pass (no mouse), sensible focus order, focus always visible
- works at 320 px wide and at 200 % zoom without horizontal scrolling
- every new image has `alt` (or `alt=""` when decorative) and `width`/`height`
- every new form field has a visible label, inline error text, and a status message
- no new third-party request fires before the user asks for it
- any new personal data has a stated purpose, retention period, and notice text
- Lighthouse accessibility stays at 100 and no new console errors appear

---

## 1. WCAG 2.2, Level AA

The accessibility statement on `/accessibility/` now targets **2.2 AA**.

| Criterion | Where it bites | Status |
| --- | --- | --- |
| 1.4.3 Contrast (minimum) | navy/gold tokens, links on tinted sections | pass |
| 1.4.10 Reflow (320 px) | all pages, section bar | pass |
| 1.4.12 Text spacing | body copy, cards | verify |
| 2.1.1 Keyboard | section bar, dialog, form | pass |
| 2.4.7 Focus visible | global `:focus-visible` | pass |
| 2.4.11 Focus not obscured | fixed UI stays clear of focused links at every width | pass |
| 2.5.7 Dragging movements | no drag interactions today | n/a |
| 2.5.8 Target size (minimum, 24x24) | standalone links, form controls, section bar | pass |
| 3.2.6 Consistent help | emergency FAB, contact links | pass |
| 3.3.7 Redundant entry | single-step forms today; multi-step requests must reuse answers | watch |
| 3.3.8 Accessible authentication | applies once accounts ship: no puzzles, allow paste and OTP | future |
| 4.1.3 Status messages | contact form `role="status"` | pass |

Rules for new work: nothing meaningful inside a `div` click handler; no
`aria-expanded` unless something actually shows/hides; test with NVDA before
shipping a dialog or a live region.

## 2. Nielsen's ten heuristics

| Heuristic | Check on this site | Status |
| --- | --- | --- |
| H1 Visibility of system status | search returns a real result page; forms confirm or explain | **fail** (search is a placeholder) |
| H2 Match the real world | task-based service finder, Filipino labels where used | partial |
| H3 User control and freedom | dialog closes on Esc, back-to-top, dismissible advisory | pass (add undo for advisory) |
| H4 Consistency and standards | one section rail, one button style, one breadcrumb pattern | pass |
| H5 Error prevention | required fields, input types, confirmation before destructive acts | partial |
| H6 Recognition over recall | directory, FOI steps, "I want to..." finder | partial |
| H7 Flexibility and efficiency | search, saved services, shortcuts for repeat visitors | **fail** (no search) |
| H8 Aesthetic and minimalist design | one job per section, no decorative clutter | pass |
| H9 Help users recover from errors | branded 404/500, inline form errors | **fail** (none) |
| H10 Help and documentation | accessibility statement, FOI guide, office hours | pass |

## 3. RA 10173 (Data Privacy Act of 2012)

The site collects personal data through the contact form and will collect more
once service requests and accounts exist. Minimum controls:

| Control | Requirement | Status |
| --- | --- | --- |
| Lawful basis + notice | say why each field is collected, before the field | partial (consent line only) |
| Data minimisation | ask only for what the office needs | pass today |
| Retention | state how long messages and uploads are kept | **missing** |
| Data-subject rights | access, correction, deletion, complaint route, DPO contact | **missing** |
| Third parties | no request to another domain before consent | **fail** (Google Maps embed: 15 requests on load) |
| Cookies | no non-essential cookie without consent | watch (currently CSRF only) |
| Breach response | named owner, 72-hour NPC notification path | **missing** |
| AI processing | disclose, get consent, never train on resident data | future |
| Security | TLS, least privilege admin, audit log, encrypted backups | partial |

Immediate fixes: click-to-load the map, self-host the images currently hotlinked
from `puertoprincesa.ph`, add retention + DPO details to `/privacy/`, and list
every processor (host, email, SMS, maps, any AI vendor).

## 4. How we verify

- keyboard only, then 200 % zoom, then 320 px width
- Lighthouse (a11y/BP/SEO) and axe DevTools on every changed page
- NVDA spot-check for dialogs, rails, and form status
- crawl every link and asset; fail on any non-200
- open DevTools Network and record third-party requests before interaction

## 5. Known deviations

Record any accepted gap here with an owner and a review date.

| Gap | Why accepted | Owner | Revisit |
| --- | --- | --- | --- |
| No deviations recorded | | | |
