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


def load_document_and_get_pages_text(url: str) -> List[str]:
    """
    Downloads document from URL and returns a list of page texts.
    This version assumes image files (PNG/JPG) only.
    """
    raw = download_file(url)

    image = Image.open(io.BytesIO(raw))
    text = ocr_image(image)

    return [text]
