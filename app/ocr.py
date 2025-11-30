import io
import requests
from typing import List
from PIL import Image
import pytesseract


def download_file(url: str) -> bytes:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content


def ocr_image(image: Image.Image) -> str:
    text = pytesseract.image_to_string(image)
    return text


# ------------------------------------------------------------
# 1️⃣ OCR for documents coming from a URL (existing)
# ------------------------------------------------------------
def load_document_and_get_pages_text(url: str) -> List[str]:
    """
    Downloads document from URL and returns page texts.
    (Image files only: PNG/JPG)
    """
    raw = download_file(url)
    image = Image.open(io.BytesIO(raw))
    text = ocr_image(image)
    return [text]


# ------------------------------------------------------------
# 2️⃣ OCR for documents uploaded directly (new)
# ------------------------------------------------------------
def load_image_and_get_pages_text(image: Image.Image) -> List[str]:
    """
    Takes a PIL image directly (uploaded file) and returns page text.
    """
    text = ocr_image(image)
    return [text]
