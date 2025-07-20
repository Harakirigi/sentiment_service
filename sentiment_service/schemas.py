from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)

class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str
