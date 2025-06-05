# main.py

import argparse
from ocr import preprocess_and_ocr
from pipeline import load_system_prompt, build_pipeline, to_dataframe

def main():
    parser = argparse.ArgumentParser(description="OCR-Driven Menu Extractor")
    parser.add_argument(
        "image_path",
        type=str,
        help="Path to the image file containing a menu (JPEG, PNG, etc.)"
    )
    parser.add_argument(
        "--prompt-yaml",
        type=str,
        default="prompts.yaml",
        help="Path to prompts.yaml (default: prompts.yaml)"
    )

    args = parser.parse_args()

    try:
        # 1. Run OCR on the image
        raw_text = preprocess_and_ocr(args.image_path)
        print("✅ OCR succeeded. Extracted text length:", len(raw_text))
    except Exception as e:
        print(f"❌ OCR error: {e}")
        return

    try:
        # 2. Load system prompt from YAML
        system_prompt = load_system_prompt(args.prompt_yaml)
    except Exception as e:
        print(f"❌ Failed to load system prompt: {e}")
        return

    try:
        # 3. Build & run the LangChain pipeline
        pipeline = build_pipeline(system_prompt)
        combined_result = pipeline.invoke(raw_text)
        print("✅ LangChain pipeline succeeded.")
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        return

    try:
        # 4. Convert the structured output to a DataFrame
        df = to_dataframe(combined_result)
        print("\nExtracted Menu Items:")
        print(df.to_string())
    except Exception as e:
        print(f"❌ Failed to convert result into DataFrame: {e}")
        return

if __name__ == "__main__":
    main()
