# pipeline.py

import yaml
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough,RunnableSerializable
from pydantic import BaseModel, Field
from typing import List
import pandas as pd

class MenuItem(BaseModel):
    name: str
    description: str
    prices: List[float] | float

class CombinedMenu(BaseModel):
    menu: List[MenuItem]


def load_system_prompt(yaml_path: str) -> str:
    """
    Load the 'system_prompt' field from the given YAML file.
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    prompt_text = config.get("system_prompt", "").strip()
    if not prompt_text:
        raise ValueError(f"No 'system_prompt' found in {yaml_path}")
    return prompt_text


def build_pipeline(system_prompt: str) -> RunnableSerializable:
    """
    Given a system_prompt (string), build and return a LangChain pipeline
    that:
      1) Accepts raw OCR text as input.
      2) Sends it to ChatOpenAI with function calling to parse a 'CombinedMenu'.
    """
    # We want to feed the OCR text into the system prompt
    # The prompt template uses {ocr_text} as the variable placeholder.
    prompt_template = ChatPromptTemplate.from_template(system_prompt.replace("{text}", "{ocr_text}"))

    llm = ChatOpenAI(model="gpt-4o")

    # The pipeline: 
    #  {'ocr_text': RunnablePassthrough()} | prompt_template | llm.with_structured_output(...)
    Pipeline = {"ocr_text": RunnablePassthrough()} | prompt_template | llm.with_structured_output(CombinedMenu, method="function_calling")
    return Pipeline


def to_dataframe(combined: CombinedMenu) -> pd.DataFrame:
    """
    Convert a CombinedMenu object into a sorted Pandas DataFrame.
    Columns: [Food_name, Description, Price(s)].
    """
    rows = []
    for item in combined.menu:
        price_field = tuple(item.prices) if isinstance(item.prices, list) else item.prices
        rows.append({
            "Food_name": item.name,
            "Description": item.description,
            "Price(s)": price_field
        })

    df = pd.DataFrame(rows).sort_values(by="Food_name", ascending=True).reset_index(drop=True)
    df.index += 1  # Start index at 1 instead of 0
    return df
