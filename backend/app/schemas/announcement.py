from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AnnouncementBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=5, max_length=1000)
    link_url: Optional[str] = Field(None, max_length=500)
    priority: str = Field(default="Normal", max_length=20)
    is_active: bool = True


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    link_url: Optional[str] = None
    priority: Optional[str] = None
    is_active: Optional[bool] = None


class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
