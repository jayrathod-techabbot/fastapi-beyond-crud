from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional
from pydantic import Field

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    book_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    created_at: datetime
    update_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str


class ReviewUpdateModel(BaseModel):
    pass
