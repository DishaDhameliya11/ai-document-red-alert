from pathlib import Path

from app.core.config import settings
import pytesseract
from fastapi import HTTPException
from PIL import Image, UnidentifiedImageError


def extract_text_from_image(file_path: Path) -> str:
    try:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(
        image,
        lang=settings.OCR_LANGUAGES,
        )

        return extracted_text.strip()

    except pytesseract.TesseractNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Tesseract OCR is not installed or not added to system PATH.",
        )

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image could not be opened. Please upload a valid image file.",
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(error)}",
        )