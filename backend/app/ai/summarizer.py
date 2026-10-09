import re


def split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def generate_basic_summary(text: str, max_sentences: int = 2) -> dict:
    if not text:
        return {
            "summary_text": "No text was extracted from the document.",
            "word_count": 0,
            "sentence_count": 0,
        }

    sentences = split_into_sentences(text)
    word_count = len(text.split())

    summary_sentences = sentences[:max_sentences]
    summary_text = " ".join(summary_sentences)

    return {
        "summary_text": summary_text,
        "word_count": word_count,
        "sentence_count": len(sentences),
    }