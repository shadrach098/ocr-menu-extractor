# ocr.py

import os
from PIL import Image
import pytesseract as pt

def preprocess_and_ocr(img_path: str) -> str:
    """
    - Verify path exists.
    - Convert to grayscale.
    - Upscale (2×) to improve OCR accuracy.
    - Run pytesseract and return the extracted text.
    """
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"File not found: {img_path}")

    img = Image.open(img_path).convert("L")
    img = img.resize((img.width * 2, img.height * 2))
    text = pt.image_to_string(img)

    if not text.strip():
        raise ValueError("No text was extracted by OCR.")
    return text
