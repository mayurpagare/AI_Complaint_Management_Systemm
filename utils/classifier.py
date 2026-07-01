CATEGORY_KEYWORDS = {
    "Road": ["pothole", "road", "crack"],
    "Water": ["leak", "pipe", "water"],
    "Electricity": ["power", "electricity", "transformer"],
    "Garbage": ["trash", "garbage", "waste"],
    "Street Light": ["street light", "lamp"],
    "Noise": ["noise", "loud"],
    "Internet": ["wifi", "wi-fi", "internet"],
    "Parking": ["parking"],
    "Sewage": ["drain", "sewage"],
    "Public Transport": ["bus", "train", "transport", "metro"],
}

PRIORITY_KEYWORDS = {
    "High": ["danger", "accident", "fire", "explosion"],
    "Medium": ["leak", "broken"],
    "Low": ["suggestion", "cleaning"],
}

VALID_CATEGORIES = sorted(CATEGORY_KEYWORDS.keys())
VALID_STATUSES = ["Pending", "In Progress", "Resolved", "Rejected"]
VALID_PRIORITIES = ["High", "Medium", "Low"]


def _normalized_text(*parts):
    return " ".join(part or "" for part in parts).lower()


def detect_category(title, description, provided_category=None):
    if provided_category and provided_category in VALID_CATEGORIES:
        return provided_category

    text = _normalized_text(title, description)
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "General"


def detect_priority(title, description):
    text = _normalized_text(title, description)
    for priority in ("High", "Medium", "Low"):
        if any(keyword in text for keyword in PRIORITY_KEYWORDS[priority]):
            return priority
    return "Low"
