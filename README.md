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
7. [Detailed Component Descriptions](#detailed-component-descriptions)  
   - [OCR Module (`src/ocr.py`)](#ocr-module-srcocrpy)  
   - [Pipeline Module (`src/pipeline.py`)](#pipeline-module-srcpipelinepy)  
   - [Main Script (`src/main.py`)](#main-script-srcmainpy)  
   - [Prompt File (`prompts.yaml`)](#prompt-file-promptsyaml)  
8. [Example Run](#example-run)  
9. [Extending & Customizing](#extending--customizing)  
10. [Contributing](#contributing)  
11. [License](#license)  

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
