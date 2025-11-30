from pydantic import BaseModel
from typing import List, Dict, Any


class ExtractRequest(BaseModel):
    document: str  # URL of the document to process


class TokenUsage(BaseModel):
    total_tokens: int
    input_tokens: int
    output_tokens: int


class BillItem(BaseModel):
    item_name: str
    item_amount: float
    item_rate: float
    item_quantity: float


class PageLineItems(BaseModel):
    page_no: str
    page_type: str  # "Bill Detail" | "Final Bill" | "Pharmacy"
    bill_items: List[BillItem]


class ExtractData(BaseModel):
    pagewise_line_items: List[PageLineItems]
    total_item_count: int


class ExtractResponse(BaseModel):
    is_success: bool
    token_usage: Dict[str, int]
    data: ExtractData
