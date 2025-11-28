from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):
    name: str = Field(..., description="제품명")
    thumbnail_url: str = Field(..., description="제품 썸네일 이미지 URL")
    price: str = Field(..., description="제품 가격")
    info_url: str = Field(..., description="제품 정보 URL")
