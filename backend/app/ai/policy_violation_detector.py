POLICY_VIOLATION_PHRASES = {
    "bypass approval": 25,
    "hide this transaction": 30,
    "delete after reading": 25,
    "do not share with compliance": 30,
    "ignore audit": 25,
    "off the record": 20,
    "no paper trail": 30,
    "avoid detection": 35,
    "without approval":25,
    "do not keep evidence":30,
    # Gujarati policy violation phrases
    "ઓડિટ અવગણો": 25,
    "આ સંદેશ કાઢી નાખો": 25,
    "રેકોર્ડ બહાર": 20,
    "પુરાવો ન રાખો": 30,
    "મંજૂરી વગર": 25,
}


def detect_policy_violations(text: str) -> dict:
    violations = []
    total_risk_score = 0

    if not text:
        return {
            "policy_violations_found": 0,
            "policy_risk_score": 0,
            "violations": [],
        }

    text_lower = text.lower()

    for phrase, risk_points in POLICY_VIOLATION_PHRASES.items():
        if phrase in text_lower:
            start_index = text_lower.find(phrase)
            end_index = start_index + len(phrase)

            violations.append(
                {
                    "phrase": phrase,
                    "risk_points": risk_points,
                    "start_index": start_index,
                    "end_index": end_index,
                }
            )

            total_risk_score += risk_points

    total_risk_score = min(total_risk_score, 100)

    return {
        "policy_violations_found": len(violations),
        "policy_risk_score": total_risk_score,
        "violations": violations,
    }