# OCR-Driven Menu Extractor

A Python project that performs OCR on a menu image and uses a LangChain (ChatOpenAI) pipeline with function calling to extract structured menu items (name, description, prices). The system prompt is stored in YAML so you can tweak parsing logic without modifying code. The final output is a sorted Pandas DataFrame of menu entries.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Project Structure](#project-structure)  
6. [Usage](#usage)  
---

## Project Overview

Many restaurants publish menu images (JPEG, PNG) online, but to analyze or ingest them, you need to convert them into structured data. This project:

1. **Performs OCR** on a menu image  
   - Uses Pillow to load and grayscale‐convert  
   - Upscales by 2× for better recognition  
   - Runs Tesseract (via `pytesseract`) to extract raw text  

2. **Parses the OCR text** through a LangChain pipeline  
   - Loads a “system prompt” from a YAML file  
   - Feeds the raw OCR text into ChatOpenAI (GPT‐4o) with function calling  
   - Defines Pydantic models (`MenuItem`, `CombinedMenu`) to validate output JSON  

3. **Converts structured output** into a Pandas DataFrame  
   - Each row represents one menu item (name, description, price(s))  
   - Sorted alphabetically by food name  
   - Index starts at 1 for readability  

4. **Keeps prompts in YAML**  
   - You can modify parsing logic (e.g., how descriptions or prices are recognized) by editing `prompts.yaml`  
   - No need to touch Python code when updating prompt instructions  

---

## Features

- **Modular codebase**—separate modules for OCR, prompt loading, pipeline building, and CLI entry point.  
- **YAML‐driven prompt**—version control your system prompt without code changes.  
- **Structured output validation**—Pydantic ensures LLM returns valid JSON matching our schema.  
- **Interactive CLI**—run `main.py` with image path (and optional prompt file path).  
- **DataFrame output**—easily extend to CSV/Excel exports or further analysis.  
- **Pandas sorting**—menu items sorted by name for easy reading.  
- **Error handling**—clear error messages if OCR fails, prompt file missing, or LLM response invalid.  

---

## Prerequisites

- **Python 3.8+**  
- **Tesseract OCR** installed and accessible via your PATH.  
  - macOS (with Homebrew): `brew install tesseract`  
  - Ubuntu/Debian: `sudo apt update && sudo apt install tesseract-ocr`  
  - Windows: Download installer from [Tesseract‐OCR GitHub](https://github.com/tesseract-ocr/tesseract) and add `tesseract.exe` to your PATH.  
- **OpenAI API Key** with permission to call GPT-4o. Set as environment variable:  
  ```bash
  export OPENAI_API_KEY="sk-…"         # Linux/macOS
  $env:OPENAI_API_KEY="sk-…"           # Windows PowerShell
  ```
## Installation
- Clone the repository
  ``` bash
  git clone https://github.com/<your-username>/ocr-menu-extractor.git
  cd ocr-menu-extractor
  ```
- Create and activate a virtual environment
  ```bash
  python3 -m venv venv
  source venv/bin/activate          # macOS/Linux
  # or
  venv\Scripts\activate             # Windows (CMD/PowerShell)
  ```
- Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
- Verify Tesseract
  ```bash
  tesseract --version
  ```
## Project Structure
 ```paintext
ocr-menu-extractor/
├── README.md                ← This file (all in Markdown, detailed)
├── requirements.txt         ← All Python dependencies
├── prompts.yaml             ← YAML file containing the system prompt
└── src
    ├── __init__.py
    ├── ocr.py               ← OCR utility module
    ├── pipeline.py          ← Builds LangChain pipeline, loads YAML prompt, defines Pydantic models
    └── main.py              ← CLI entry point: runs OCR → pipeline → DataFrame
 ```
## Usage
 ```bash
   # Activate your virtual environment first (venv/bin/activate or venv\Scripts\activate)

   # Basic invocation (uses prompts.yaml by default)
   python -m src.main /path/to/your/menu_image.jpg

   # If you have a different prompt file, pass it with --prompt-yaml
   python -m src.main /path/to/your/menu_image.jpg --prompt-yaml custom_prompts.yaml
 ```
   - Arguments
      image_path (required): Path to the menu image (JPEG, PNG, etc.).
      --prompt-yaml (optional): Path to a YAML file containing system_prompt. Defaults to prompts.yaml.
   - Output
      Prints status messages as OCR and LLM pipeline succeed or fail.
      Displays a sorted DataFrame in the console, for example:
      ```bash
      ✅ OCR succeeded. Extracted text length: 1423
      ✅ LangChain pipeline succeeded.

      Extracted Menu Items:
             Food_name         Description           Price(s)
      1   Caesar Salad      Romaine, Parmesan et al.  (7.99,)
      2   Grilled Salmon    Served with lemon butter  (15.49,)
      3   Pepperoni Pizza   Extra cheese, hand-tossed (12.99, 15.99)

     ```
