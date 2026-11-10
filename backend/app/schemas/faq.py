from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class FAQBase(BaseModel):
    category: str = Field(default="General", max_length=50)
    question: str = Field(..., min_length=5, max_length=500)
    answer: str
    display_order: int = 0
    is_published: bool = True


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    category: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    display_order: Optional[int] = None
    is_published: Optional[bool] = None


class FAQResponse(FAQBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
