from fastapi import FastAPI, HTTPException
from app.models import ExtractRequest, ExtractResponse
from app.ocr import load_document_and_get_pages_text
from app.llm import extract_items_from_page
from app.utils import classify_page_type
from typing import List, Dict, Any

app = FastAPI()


@app.post("/extract-bill-data", response_model=ExtractResponse)
async def extract_bill_data(request: ExtractRequest):
    try:
        pages_text = load_document_and_get_pages_text(request.document)

        pagewise_line_items = []
        total_tokens = {
            "total_tokens": 0,
            "input_tokens": 0,
            "output_tokens": 0,
        }

        for idx, page_text in enumerate(pages_text, start=1):
            items, usage = extract_items_from_page(page_text, idx)

            total_tokens["input_tokens"] += usage.get("input_tokens", 0)
            total_tokens["output_tokens"] += usage.get("output_tokens", 0)
            total_tokens["total_tokens"] += usage.get("total_tokens", 0)

            page_type = classify_page_type(page_text)

            pagewise_line_items.append(
                {
                    "page_no": str(idx),
                    "page_type": page_type,
                    "bill_items": items,
                }
            )

        total_item_count = sum(len(p["bill_items"]) for p in pagewise_line_items)

        return ExtractResponse(
            is_success=True,
            token_usage=total_tokens,
            data={
                "pagewise_line_items": pagewise_line_items,
                "total_item_count": total_item_count,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
