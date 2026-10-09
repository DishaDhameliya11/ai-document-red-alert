import re


INDIAN_COMPLIANCE_PATTERNS = {
    "pan_number": {
        "pattern": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "risk_points": 35,
    },
    "aadhaar_like_number": {
        "pattern": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "risk_points": 35,
    },
    "gstin": {
        "pattern": r"\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b",
        "risk_points": 35,
    },
    "ifsc_code": {
        "pattern": r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
        "risk_points": 25,
    },
    "upi_id": {
        "pattern": r"\b[A-Za-z0-9.\-_]{2,256}@[A-Za-z]{2,64}\b",
        "risk_points": 25,
    },
    "indian_phone_number": {
        "pattern": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
        "risk_points": 20,
    },
    "bank_account_like_number": {
        "pattern": r"\b\d{9,18}\b",
        "risk_points": 25,
    },
}


def mask_value(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)

    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def detect_indian_compliance_data(text: str) -> dict:
    findings = []
    total_risk_score = 0

    if not text:
        return {
            "compliance_items_found": 0,
            "compliance_risk_score": 0,
            "findings": [],
        }

    for label, config in INDIAN_COMPLIANCE_PATTERNS.items():
        matches = re.finditer(config["pattern"], text)

        for match in matches:
            raw_value = match.group()
            risk_points = config["risk_points"]

            findings.append(
                {
                    "type": label,
                    "masked_value": mask_value(raw_value),
                    "risk_points": risk_points,
                    "start_index": match.start(),
                    "end_index": match.end(),
                }
            )

            total_risk_score += risk_points

    total_risk_score = min(total_risk_score, 100)

    return {
        "compliance_items_found": len(findings),
        "compliance_risk_score": total_risk_score,
        "findings": findings,
    }