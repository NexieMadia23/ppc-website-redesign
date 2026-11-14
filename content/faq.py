"""FAQ knowledge base.

Used by the FAQ page and the assistant. Answers are written in plain language
and in a light Taglish tone where it helps. Nothing here calls an AI service:
the assistant matches words, synonyms, and near-miss spellings against this
list, so it works offline and can never invent an answer. Everything it cannot
answer is logged for the content team instead of being guessed.
"""

import re
from difflib import SequenceMatcher

# Words that carry no meaning for matching. Without this, "how do I" would match
# almost every answer.
STOPWORDS = {
    "a",
    "an",
    "and",
    "ang",
    "are",
    "ba",
    "can",
    "do",
    "does",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "ko",
    "kung",
    "ma",
    "mag",
    "may",
    "me",
    "my",
    "na",
    "ng",
    "nga",
    "of",
    "on",
    "or",
    "paano",
    "po",
    "sa",
    "saan",
    "the",
    "to",
    "what",
    "where",
    "who",
    "why",
    "with",
    "you",
}

# Groups of words residents use for the same thing, English and Filipino.
# The first word in each group is the canonical token.
SYNONYM_GROUPS = [
    ["complaint", "reklamo", "sumbong", "sumbungan", "report", "reklamong", "daing"],
    ["permit", "permiso", "licence", "license", "lisensya"],
    ["business", "negosyo", "enterprise"],
    ["birth", "kapanganakan", "panganganak"],
    ["certificate", "sertipiko", "sertipikasyon"],
    ["document", "dokumento", "papel", "record", "rekord"],
    ["emergency", "emerhensya", "aksidente", "accident", "urgent", "apurahan"],
    ["fire", "sunog"],
    ["flood", "baha"],
    ["police", "pulis"],
    ["rescue", "saklolo", "ligtas"],
    ["trash", "basura", "garbage", "kalat", "waste"],
    ["streetlight", "ilaw", "lamp", "light"],
    ["broken", "sira", "putol", "damaged"],
    ["water", "tubig"],
    ["electricity", "kuryente", "power"],
    ["office", "opisina", "tanggapan"],
    ["hours", "oras", "schedule", "iskedyul", "bukas"],
    ["tax", "buwis", "taxes"],
    ["payment", "bayad"],
    ["health", "kalusugan", "ospital", "hospital"],
    ["senior", "matanda", "elderly"],
    ["pwd", "disability", "kapansanan"],
    ["budget", "badyet", "pera", "gastos", "funds"],
    ["privacy", "pribado", "private"],
    ["status", "kalagayan", "asikaso", "followup"],
    ["track", "subaybayan", "trace", "tracking"],
]

CANONICAL = {}
for group in SYNONYM_GROUPS:
    canonical = group[0]
    for word in group:
        CANONICAL.setdefault(word, canonical)

# A second, direct map for Tagalog words that do not have a neat group above.
EXTRA_SYNONYMS = {
    "kumuha": "get",
    "kuha": "get",
    "kailangan": "need",
    "magkano": "cost",
    "bayaran": "payment",
    "tawag": "call",
    "numero": "number",
    "telepono": "phone",
    "salamat": "thanks",
    "opisyal": "official",
    "lungsod": "city",
    "bayan": "city",
    "barangay": "barangay",
}
CANONICAL.update(EXTRA_SYNONYMS)

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
            "Most browsers let you zoom the whole page (Ctrl and + on Windows, "
            "Command and + on a Mac) or set a larger default text size. A screen "
            "reader or your device's read-aloud feature can read the page. The "
            "Accessibility statement explains the standards the site follows and "
            "how to report a barrier."
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
    {
        "id": "garbage",
        "category": "Services",
        "question": "How do I report uncollected garbage or illegal dumping?",
        "answer": (
            "File a Sumbungan ng Bayan request under “Sanitation and waste” and "
            "include the barangay, the nearest landmark, and when you last saw the "
            "waste. If you can, attach a photo: it helps the sanitation team find "
            "the exact spot. You can track the request with the reference number."
        ),
        "keywords": [
            "garbage",
            "basura",
            "trash",
            "waste",
            "collection",
            "kolekta",
            "dumping",
            "kalat",
            "sanitation",
            "smell",
            "mabaho",
        ],
        "link": ("sumbungan", "File a complaint"),
    },
    {
        "id": "streetlight",
        "category": "Services",
        "question": "How do I report a broken street light or pothole?",
        "answer": (
            "Use the Sumbungan ng Bayan form and choose “Infrastructure”. Give the "
            "street, the nearest landmark, and a photo if you have one. Reports are "
            "routed to the city engineering office, and the tracking page shows every "
            "status change until the repair is closed."
        ),
        "keywords": [
            "street light",
            "streetlight",
            "ilaw",
            "lamp",
            "bulb",
            "pothole",
            "lubak",
            "road",
            "kalsada",
            "repair",
            "sira",
            "infrastructure",
        ],
        "link": ("sumbungan", "File a complaint"),
    },
]


def _tokens(text):
    """Lowercase words, folded through the synonym map and lightly stemmed."""
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    tokens = []
    for word in words:
        token = CANONICAL.get(word, word)
        if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
            token = token[:-1]
        tokens.append(token)
    return tokens


def _meaningful(tokens):
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def _near_miss(token, keywords):
    """True when a typed word is a small misspelling of a keyword."""
    for keyword in keywords:
        if abs(len(token) - len(keyword)) > 2:
            continue
        if SequenceMatcher(None, token, keyword).ratio() >= 0.8:
            return True
    return False


def _score(faq, text, tokens):
    """Blend exact keyword hits, Tagalog/English synonyms, and typo tolerance."""
    keyword_tokens = set()
    for keyword in faq["keywords"]:
        for word in keyword.split():
            keyword_tokens.add(_canonical_word(word))
    question_tokens = set(_meaningful(_tokens(faq["question"])))
    score = 0.0

    for keyword in faq["keywords"]:
        if " " in keyword and keyword in text:
            score += 2.0
        elif " " not in keyword and _canonical_word(keyword) in tokens:
            score += 1.0

    for token in tokens:
        if token in question_tokens:
            score += 0.25
        if token not in keyword_tokens and _near_miss(token, keyword_tokens):
            score += 1.0

    return score


def _canonical_word(word):
    token = CANONICAL.get(word.lower(), word.lower())
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        token = token[:-1]
    return token


def find_answer(message):
    """Return the FAQ with the strongest match, or ``None`` when unsure.

    A message needs a real signal (a keyword, a synonym, or a near-miss spelling)
    before an answer is returned. Guessing is worse than admitting the gap,
    because the caller logs misses for the content team.
    """
    text = (message or "").lower().strip()
    tokens = _meaningful(_tokens(text))
    best = None
    best_score = 0.0
    for faq in FAQS:
        score = _score(faq, text, tokens)
        if score > best_score:
            best = faq
            best_score = score
    if best_score < 1.0:
        return None
    return best


def suggestions(limit=4):
    """A few starter questions for the assistant's quick replies."""
    return FAQS[:limit]

