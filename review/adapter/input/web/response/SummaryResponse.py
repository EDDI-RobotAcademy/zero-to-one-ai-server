from pydantic import BaseModel
from typing import List


class ProductSummary(BaseModel):
    name: str
    price: str
    summary: str
    positive_features: str
    negative_features: str
    keywords: List[str]


class SummaryResponse(BaseModel):
    product_summary: ProductSummary
    pdf_url: str
