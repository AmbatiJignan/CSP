from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class EducationalVideoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(default="Composting", max_length=100)
    video_url: str = Field(..., max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    duration_minutes: Optional[int] = Field(None, ge=1)
    display_order: int = 0
    is_published: bool = True


class EducationalVideoCreate(EducationalVideoBase):
    pass


class EducationalVideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    display_order: Optional[int] = None
    is_published: Optional[bool] = None


class EducationalVideoResponse(EducationalVideoBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
