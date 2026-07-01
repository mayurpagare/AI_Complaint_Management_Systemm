import json
import os

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


def classify_complaint(title, description, provided_category=None):
    if provided_category and provided_category in VALID_CATEGORIES:
        return {
            "category": provided_category,
            "priority": detect_priority(title, description),
            "source": "manual",
        }

    gemini_result = classify_with_gemini(title, description)
    if gemini_result:
        return gemini_result

    return {
        "category": detect_category(title, description),
        "priority": detect_priority(title, description),
        "source": "keywords",
    }


def classify_with_gemini(title, description):
    api_key = os.environ.get("GEMINI_API_KEY")
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
    if not api_key:
        return None

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        prompt = f"""
Classify this civic complaint.

Allowed categories: {", ".join(VALID_CATEGORIES)}, General
Allowed priorities: High, Medium, Low

Priority rules:
High means danger, accident, fire, explosion, or immediate public safety risk.
Medium means leak, broken infrastructure, blocked service, or significant disruption.
Low means suggestion, cleaning, minor inconvenience, or non-urgent issue.

Complaint title: {title}
Complaint description: {description}

Return only valid JSON with exactly these keys:
{{"category":"Road","priority":"Medium"}}
"""
        response = client.models.generate_content(model=model, contents=prompt)
        payload = _extract_json(response.text or "")
        category = payload.get("category")
        priority = payload.get("priority")
        if category not in [*VALID_CATEGORIES, "General"]:
            category = detect_category(title, description)
        if priority not in VALID_PRIORITIES:
            priority = detect_priority(title, description)
        return {"category": category, "priority": priority, "source": "gemini"}
    except Exception:
        return None


def _extract_json(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1:
        cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)
