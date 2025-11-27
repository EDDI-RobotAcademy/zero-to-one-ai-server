from datetime import datetime
from typing import List

class PdfDocument:
    def __init__(
        self,
        summary: str,
        positive_features: str,
        negative_features: str,
        category: str,
        price: str,
        product_name: str,
        keywords: List[str],
        title: str = "리뷰 요약 보고서",
        created_at: datetime | None = None
    ):

        self.title = title
        self.summary = summary
        self.positive_features = positive_features
        self.negative_features = negative_features
        self.category = category
        self.price = price
        self.product_name = product_name
        self.keywords = keywords
        self.created_at = created_at or datetime.utcnow()

    def to_plain_text(self) -> str:
        text = (
            f"{self.title}\n"
            f"생성일: {self.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
            f"[상품명]\n{self.product_name}\n\n"
            f"[카테고리]\n{self.category}\n\n"
            f"[가격]\n{self.price}\n\n원"
            f"[요약]\n{self.summary}\n\n"
            f"[긍정 요인]\n{self.positive_features}\n\n"
            f"[부정 요인]\n{self.negative_features}\n\n"
            f"[키워드]\n{', '.join(self.keywords)}\n"
        )
        return text