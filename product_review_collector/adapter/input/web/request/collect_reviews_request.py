from pydantic import BaseModel, HttpUrl


class CollectReviewsRequest(BaseModel):
    product_url: HttpUrl
