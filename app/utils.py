def classify_page_type(page_text: str) -> str:
    """
    Very simple heuristic classifier for page_type.
    You can improve this using better rules or an LLM if needed.
    """
    text_lower = page_text.lower()

    if "pharmacy" in text_lower or "drug" in text_lower or "medicine" in text_lower:
        return "Pharmacy"
    if "final bill" in text_lower or "grand total" in text_lower:
        return "Final Bill"
    return "Bill Detail"
