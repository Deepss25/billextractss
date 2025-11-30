import json
from typing import Tuple, List, Dict, Any
import litellm


def extract_items_from_page(page_text: str, page_no: int) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Calls LLM to extract line items from a page.
    Returns (items, usage_dict).
    """
    prompt = f"""
You are an expert invoice parser.

TASK:
From the following bill page text, extract only the actual line items (products/services).
Ignore headers, subtotals, discounts, taxes, totals, round-off, and other non-line items.

For each line item, return:
- item_name: string (exact as in text, or as close as OCR allows)
- item_quantity: float
- item_rate: float
- item_amount: float (net amount for that line)

Return JSON in the format:
{{
  "items": [
    {{
      "item_name": "string",
      "item_quantity": 0.0,
      "item_rate": 0.0,
      "item_amount": 0.0
    }}
  ]
}}

PAGE NUMBER: {page_no}
PAGE TEXT:
\"\"\"{page_text}\"\"\""""

    response = litellm.completion(
        model="gpt-4o-mini",  # use any OpenAI-compatible small model
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    usage = {
        "input_tokens": getattr(response, "usage", {}).get("prompt_tokens", 0) if hasattr(response, "usage") else 0,
        "output_tokens": getattr(response, "usage", {}).get("completion_tokens", 0) if hasattr(response, "usage") else 0,
        "total_tokens": getattr(response, "usage", {}).get("total_tokens", 0) if hasattr(response, "usage") else 0,
    }

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except Exception:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            data = json.loads(content[start : end + 1])
        else:
            data = {"items": []}

    items = data.get("items", [])
    cleaned_items = []
    for it in items:
        try:
            cleaned_items.append(
                {
                    "item_name": str(it.get("item_name", "")).strip(),
                    "item_amount": float(it.get("item_amount", 0) or 0),
                    "item_rate": float(it.get("item_rate", 0) or 0),
                    "item_quantity": float(it.get("item_quantity", 0) or 0),
                }
            )
        except Exception:
            continue

    return cleaned_items, usage
