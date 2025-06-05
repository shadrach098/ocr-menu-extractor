# ocr-menu-extractor
A small Python project that:
1. Performs OCR on a provided image (via Pillow + pytesseract).
2. Sends the extracted text through a LangChain pipeline (using ChatOpenAI, function calling) to parse “menu items” (name, description, price).
3. Outputs a sorted Pandas DataFrame of menu entries.

**What’s new “bigger”**:
- Modular code in `src/` (separate OCR, pipeline, main logic).
- System prompt stored in `prompts.yaml` (so you can swap or version prompts without touching code).
- CLI-style invocation in `main.py`.
- A full `requirements.txt` for easy install.

---
