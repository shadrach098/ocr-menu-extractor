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

##  Project Structure 

├── README.md ← This file
├── requirements.txt ← Python dependencies
├── prompts.yaml ← YAML file containing the system prompt
└── src
├── init.py
├── ocr.py ← OCR utility (Pillow + pytesseract)
├── pipeline.py ← Builds and invokes the LangChain pipeline, loading prompt from YAML
└── main.py ← CLI entry point: takes image path, runs OCR → pipeline → shows DataFrame
