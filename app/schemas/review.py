from pydantic import BaseModel,Field
from datetime import datetime


class CreateReview(BaseModel):
    rating:int = Field(ge=1 ,le=5)
    comment:str
    reservation_id:int

class ReviewResponse(BaseModel):
    id: int
    reservation_id: int
    equipment_id: int
    reviewer_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True

class UpdateReview(BaseModel):
    rating:int |None=Field(default=None,ge=1,le=5)
    comment:str |None=None
    
    