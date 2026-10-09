from pathlib import Path

import pdfplumber


def extract_text_from_pdf(file_path: Path) -> str:
    extracted_pages = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""

            if page_text.strip():
                extracted_pages.append(page_text.strip())

    return "\n\n".join(extracted_pages)