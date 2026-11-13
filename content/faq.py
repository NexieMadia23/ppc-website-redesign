"""Prototype FAQ knowledge base.

Used by the FAQ page and the chatbot. Answers are written in plain language and
in a light Taglish tone where it helps. Nothing here calls an AI service: the
chatbot matches keywords against this list, so it works offline and can never
invent an answer.
"""

FAQS = [
    {
        "id": "sumbungan",
        "category": "Complaints",
        "question": "How do I file a complaint or request help?",
        "answer": (
            "Open the Sumbungan ng Bayan page and fill in the short form. Choose a "
            "category, describe what happened, and add a name plus an email or mobile "
            "number. You can also submit anonymously. You will get a reference number "
            "like PPC-2026-000123 so you can track the request."
        ),
        "keywords": [
            "complaint",
            "sumbong",
            "sumbungan",
            "reklamo",
            "request",
            "tulong",
            "report",
            "help",
            "serbisyo",
        ],
        "link": ("sumbungan", "File a complaint"),
    },
    {
        "id": "track",
        "category": "Complaints",
        "question": "How do I check the status of my complaint?",
        "answer": (
            "Go to Sumbungan ng Bayan, then choose “Track a request”. Enter the "
            "reference number you received. The tracking page shows the current "
            "status and every public update from the agency."
        ),
        "keywords": [
            "track",
            "status",
            "reference",
            "follow up",
            "follow-up",
            "update",
            "asikasuhin",
            "saan na",
        ],
        "link": ("complaint_track", "Track a request"),
    },
    {
        "id": "response-time",
        "category": "Complaints",
        "question": "How long does a complaint take?",
        "answer": (
            "Most requests are acknowledged within one working day. Resolution time "
            "depends on the agency and the issue. Simple concerns like a broken street "
            "light can be resolved quickly; cases that need inspection or procurement "
            "take longer. The tracking page shows every status change."
        ),
        "keywords": [
            "how long",
            "tagal",
            "response",
            "reply",
            "days",
            "oras",
            "resolution",
        ],
        "link": ("complaint_track", "Track a request"),
    },
    {
        "id": "permits",
        "category": "Services",
        "question": "Where do I get a business permit?",
        "answer": (
            "Business permits are handled by the City Treasurer's Office and the "
            "Business Permits and Licensing Office. Start with the online services "
            "section, or call the City Hall switchboard and ask for BPLO. Bring a "
            "valid ID, your lease or land title, and your previous permit if renewing."
        ),
        "keywords": [
            "business",
            "permit",
            "negosyo",
            "licence",
            "license",
            "bplo",
            "treasurer",
        ],
        "link": ("government", "Government offices"),
    },
    {
        "id": "documents",
        "category": "Services",
        "question": "How do I request a birth certificate or other civil document?",
        "answer": (
            "Civil registry documents are released by the City Civil Registrar's "
            "Office. The Philippine Statistics Authority also accepts online requests "
            "for PSA copies. Check the Directory for the office contact details and "
            "opening hours before going to City Hall."
        ),
        "keywords": [
            "birth",
            "certificate",
            "civil",
            "registrar",
            "psa",
            "document",
            "record",
            "nso",
        ],
        "link": ("directory", "Office directory"),
    },
    {
        "id": "emergency",
        "category": "Safety",
        "question": "Who do I call in an emergency?",
        "answer": (
            "For a life-threatening emergency, call the City Disaster Risk Reduction "
            "and Management Office or the nearest police station right away. The "
            "Emergency page lists the hotlines. Do not wait for an online form."
        ),
        "keywords": [
            "emergency",
            "urgent",
            "accident",
            "fire",
            "flood",
            "rescue",
            "police",
            "ambulance",
            "danger",
        ],
        "link": ("emergency", "Emergency contacts"),
    },
    {
        "id": "accessibility",
        "category": "Using this site",
        "question": "How do I make the text bigger or read the page aloud?",
        "answer": (
            "Use the accessibility button at the bottom-left of every page. You can "
            "increase text size, turn on high contrast, underline links, reduce motion, "
            "or have the page read aloud. The Accessibility statement explains what is "
            "supported."
        ),
        "keywords": [
            "accessibility",
            "font",
            "text size",
            "contrast",
            "read aloud",
            "screen reader",
            "zoom",
            "mata",
            "malaki",
        ],
        "link": ("accessibility", "Accessibility statement"),
    },
    {
        "id": "privacy",
        "category": "Using this site",
        "question": "Will my personal information be published?",
        "answer": (
            "No. Your name and contact details are only used to follow up on your "
            "request. The public tracking page shows the subject, category, status, and "
            "agency updates, not your contact information. Read the Privacy policy for "
            "the full details."
        ),
        "keywords": [
            "privacy",
            "personal",
            "data",
            "name",
            "anonymous",
            "private",
            "safe",
        ],
        "link": ("privacy", "Privacy policy"),
    },
    {
        "id": "transparency",
        "category": "Government",
        "question": "Where can I see the city budget and public documents?",
        "answer": (
            "The Transparency page groups budgets, bids and awards, ordinances, and "
            "reports. The Freedom of Information page explains how to request a "
            "document that is not published yet."
        ),
        "keywords": [
            "budget",
            "transparency",
            "document",
            "bids",
            "ordinance",
            "foi",
            "pera",
            "gastos",
        ],
        "link": ("transparency", "Transparency"),
    },
    {
        "id": "contact",
        "category": "Government",
        "question": "What are the City Hall office hours?",
        "answer": (
            "City Hall is open Mondays to Fridays, 8:00 AM to 5:00 PM, except on "
            "holidays. Some offices have a lunch break. Check the Directory for the "
            "specific office and its contact number."
        ),
        "keywords": [
            "hours",
            "open",
            "office hours",
            "oras",
            "bukas",
            "schedule",
            "weekend",
        ],
        "link": ("directory", "Office directory"),
    },
]


def find_answer(message):
    """Return the FAQ with the most keyword hits, or ``None``."""
    text = (message or "").lower()
    best = None
    best_score = 0
    for faq in FAQS:
        score = sum(1 for keyword in faq["keywords"] if keyword in text)
        if score > best_score:
            best = faq
            best_score = score
    return best


def suggestions(limit=4):
    """A few starter questions for the chatbot's quick replies."""
    return FAQS[:limit]
