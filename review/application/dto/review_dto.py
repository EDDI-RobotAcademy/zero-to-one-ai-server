class ReviewDTO:
    def __init__(self, product_id: str, review_text: str, rating: float):
        self.product_id = product_id
        self.review_text = review_text
        # self.rating = rating

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            product_id=data.get("productId"),
            review_text=data.get("content"),
            # rating=data.get("rating", None)
        )
