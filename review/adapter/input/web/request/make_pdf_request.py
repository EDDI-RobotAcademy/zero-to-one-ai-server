from pydantic import BaseModel

class MakePdfRequest(BaseModel):
    review_content: str