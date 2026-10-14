
import csv
import re
from pathlib import Path

CSV_FILE = Path(__file__).with_name("schemes.csv")

REQUIRED_COLUMNS = {
    "scheme_name",
    "category",
    "description",
    "eligibility",
    "official_link",
    "education_levels",
    "states",
    "min_age",
    "max_age",
    "max_income",
    "categories",
    "genders",
}

BLANK_VALUES = {
    "", "not specified", "prefer not to say",
    "not applicable", "n/a", "none", "unknown"
}

WILDCARDS = {
    "all", "any", "all india", "india",
    "pan india", "nationwide", "not specified"
}


def normalise(value):
    return str(value or "").strip().casefold()


def is_blank(value):
    return normalise(value) in BLANK_VALUES


def split_values(value):
    return [
        item.strip()
        for item in str(value or "").split(",")
        if item.strip()
    ]


def matches_list(user_value, scheme_value):
    """Match a profile value against a CSV list."""

    if is_blank(user_value):
        return True

    allowed = {
        normalise(item) for item in split_values(scheme_value)
    }

    # A blank restriction means no restriction was recorded.
    if not allowed or allowed & WILDCARDS:
        return True

    user_values = {
        normalise(item) for item in split_values(user_value)
    }

    return bool(user_values & allowed)


def number_or_none(value):
    """Convert an age/income value to a number safely."""

    if is_blank(value):
        return None

    try:
        cleaned = re.sub(r"[^0-9.]", "", str(value))
        return float(cleaned) if cleaned else None
    except (TypeError, ValueError):
        return None


def load_schemes():
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find schemes.csv. Expected location: {CSV_FILE}"
        )

    with open(
        CSV_FILE, "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(
                "schemes.csv is empty or has no header row."
            )

        reader.fieldnames = [
            name.strip() if name else ""
            for name in reader.fieldnames
        ]

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing:
            raise ValueError(
                "Missing columns in schemes.csv: "
                + ", ".join(sorted(missing))
            )

        schemes = []

        for row in reader:
            scheme = {
                str(key).strip(): str(value or "").strip()
                for key, value in row.items()
                if key is not None
            }

            if scheme.get("scheme_name"):
                schemes.append(scheme)

    if not schemes:
        raise ValueError(
            "schemes.csv contains no scholarship records."
        )

    return schemes


def profile_matches(profile, scheme):
    """Return True when recorded eligibility restrictions match."""

    checks = [
        (profile.get("state"), scheme.get("states")),
        (
            profile.get("education_level"),
            scheme.get("education_levels"),
        ),
        (
            profile.get("social_category"),
            scheme.get("categories"),
        ),
        (profile.get("gender"), scheme.get("genders")),
    ]

    for user_value, scheme_value in checks:
        if not matches_list(user_value, scheme_value):
            return False

    age = number_or_none(profile.get("age"))
    min_age = number_or_none(scheme.get("min_age"))
    max_age = number_or_none(scheme.get("max_age"))

    if age is not None:
        if min_age is not None and age < min_age:
            return False
        if max_age is not None and age > max_age:
            return False

    income = number_or_none(profile.get("annual_income"))
    max_income = number_or_none(scheme.get("max_income"))

    if income is not None and max_income is not None:
        if income > max_income:
            return False

    return True


def keyword_score(query, scheme):
    """Rank matches by keywords; this is not an eligibility score."""

    words = set(re.findall(r"[a-z0-9]+", normalise(query)))

    if not words:
        return 0

    searchable_text = " ".join([
        scheme.get("scheme_name", ""),
        scheme.get("category", ""),
        scheme.get("description", ""),
        scheme.get("eligibility", ""),
    ])

    scheme_words = set(
        re.findall(r"[a-z0-9]+", normalise(searchable_text))
    )

    return len(words & scheme_words)


def recommend_schemes(user_query="", profile=None, limit=20):
    profile = profile or {}
    schemes = load_schemes()
    results = []

    for scheme in schemes:
        if profile_matches(profile, scheme):
            result = scheme.copy()
            result["match_score"] = keyword_score(
                user_query, scheme
            )
            results.append(result)

    results.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return results[:max(1, int(limit))]
