THREAT_PHRASES = {
    "pay or else": 35,
    "leak your data": 35,
    "release your information": 30,
    "blackmail": 35,
    "extortion": 35,
    "threaten": 25,
    "harm": 25,
    "legal action immediately": 20,
    "final warning": 20,

    # Gujarati threat phrases
    "પૈસા આપો નહીં તો": 35,
    "તમારો ડેટા લીક કરીશું": 35,
    "અંતિમ ચેતવણી": 20,
    "ધમકી": 25,
    "બ્લેકમેલ": 35,
}


def detect_threats(text: str) -> dict:
    threats = []
    total_risk_score = 0

    if not text:
        return {
            "threats_found": 0,
            "threat_risk_score": 0,
            "threats": [],
        }

    text_lower = text.lower()

    for phrase, risk_points in THREAT_PHRASES.items():
        search_start = 0

        while True:
            start_index = text_lower.find(phrase, search_start)

            if start_index == -1:
                break

            end_index = start_index + len(phrase)

            threats.append(
                {
                    "phrase": phrase,
                    "risk_points": risk_points,
                    "start_index": start_index,
                    "end_index": end_index,
                }
            )

            total_risk_score += risk_points
            search_start = end_index

    total_risk_score = min(total_risk_score, 100)

    return {
        "threats_found": len(threats),
        "threat_risk_score": total_risk_score,
        "threats": threats,
    }
