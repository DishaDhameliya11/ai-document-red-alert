import re


SENSITIVE_PATTERNS = {
    "email_address": {
        "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "risk_points": 15,
    },
    "phone_number": {
        "pattern": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
        "risk_points": 20,
    },
    "credit_card_number": {
        "pattern": r"\b(?:\d[ -]*?){13,16}\b",
        "risk_points": 40,
    },
    "aadhaar_like_number": {
        "pattern": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "risk_points": 35,
    },
    "pan_like_number": {
        "pattern": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "risk_points": 35,
    },
}


def mask_sensitive_value(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)

    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def detect_sensitive_information(text: str) -> dict:
    findings = []
    total_risk_score = 0

    if not text:
        return {
            "sensitive_items_found": 0,
            "sensitive_risk_score": 0,
            "findings": [],
        }

    for label, config in SENSITIVE_PATTERNS.items():
        matches = re.finditer(config["pattern"], text)

        for match in matches:
            raw_value = match.group()
            risk_points = config["risk_points"]

            findings.append(
                {
                    "type": label,
                    "masked_value": mask_sensitive_value(raw_value),
                    "risk_points": risk_points,
                    "start_index": match.start(),
                    "end_index": match.end(),
                }
            )

            total_risk_score += risk_points

    total_risk_score = min(total_risk_score, 100)

    return {
        "sensitive_items_found": len(findings),
        "sensitive_risk_score": total_risk_score,
        "findings": findings,
    }