RISKY_KEYWORDS = {
    # English keywords
    "confidential": 15,
    "urgent payment": 20,
    "bank account": 20,
    "password": 25,
    "fraud": 30,
    "fake": 20,
    "threat": 30,
    "blackmail": 35,
    "classified": 25,
    "do not disclose": 30,

    # Gujarati keywords
    "ગોપનીય": 15,
    "તાત્કાલિક ચુકવણી": 20,
    "બેંક ખાતું": 20,
    "પાસવર્ડ": 25,
    "છેતરપિંડી": 30,
    "નકલી": 20,
    "ધમકી": 30,
    "બ્લેકમેલ": 35,
    "જાહેર ન કરશો": 30,
}


def find_keyword_positions(text: str, keyword: str) -> list[tuple[int, int]]:
    positions = []
    text_lower = text.lower()
    keyword_lower = keyword.lower()

    start = 0

    while True:
        index = text_lower.find(keyword_lower, start)

        if index == -1:
            break

        end = index + len(keyword)
        positions.append((index, end))
        start = end

    return positions


def create_excerpt(text: str, start: int, end: int, window: int = 60) -> str:
    excerpt_start = max(start - window, 0)
    excerpt_end = min(end + window, len(text))

    return text[excerpt_start:excerpt_end].strip()


def detect_risky_keywords(text: str) -> dict:
    matched_keywords = []
    highlighted_sections = []
    risk_score = 0

    if not text:
        return {
            "matched_keywords": [],
            "keyword_count": 0,
            "keyword_risk_score": 0,
            "highlighted_sections": [],
        }

    for keyword, score in RISKY_KEYWORDS.items():
        positions = find_keyword_positions(text, keyword)

        if positions:
            matched_keywords.append(keyword)
            risk_score += score

            for start, end in positions:
                highlighted_sections.append(
                    {
                        "keyword": keyword,
                        "risk_points": score,
                        "start_index": start,
                        "end_index": end,
                        "excerpt": create_excerpt(text, start, end),
                    }
                )

    risk_score = min(risk_score, 100)

    return {
        "matched_keywords": matched_keywords,
        "keyword_count": len(matched_keywords),
        "keyword_risk_score": risk_score,
        "highlighted_sections": highlighted_sections,
    }