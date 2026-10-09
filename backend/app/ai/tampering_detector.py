import re


def detect_tampering_suspicion(text: str) -> dict:
    findings = []
    total_score = 0

    def add_finding(finding_type: str, description: str, points: int) -> None:
        nonlocal total_score

        findings.append(
            {
                "type": finding_type,
                "description": description,
                "risk_points": points,
            }
        )
        total_score += points

    if not text:
        return {
            "tampering_suspicions_found": 0,
            "tampering_risk_score": 0,
            "findings": [],
        }

    if re.search(r"[\u200B-\u200D\uFEFF]", text):
        add_finding(
            "hidden_unicode_characters",
            "Invisible Unicode characters were detected.",
            30,
        )

    obfuscated_pattern = r"\b(passw0rd|pa55word|acc0unt|fr[a@]ud)\b"
    if re.search(obfuscated_pattern, text, flags=re.IGNORECASE):
        add_finding(
            "obfuscated_risky_words",
            "Possible character substitution was detected.",
            25,
        )

    if "\ufffd" in text:
        add_finding(
            "ocr_corruption",
            "Unreadable replacement characters were detected.",
            15,
        )

    if re.search(r"[ \t]{5,}", text):
        add_finding(
            "unusual_spacing",
            "Unusually large spaces were detected.",
            10,
        )

    lines = [line.strip().lower() for line in text.splitlines() if line.strip()]
    if len(lines) != len(set(lines)):
        add_finding(
            "duplicate_lines",
            "Duplicate text lines were detected.",
            15,
        )

    return {
        "tampering_suspicions_found": len(findings),
        "tampering_risk_score": min(total_score, 100),
        "findings": findings,
    }