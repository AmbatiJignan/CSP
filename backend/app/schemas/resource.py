from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ResourceBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(default="Guides", max_length=100)
    file_path: str = Field(..., max_length=500)
    file_name: str = Field(..., max_length=255)
    file_size_bytes: int = 0
    file_type: str = Field(default="pdf", max_length=50)
    is_published: bool = True


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_published: Optional[bool] = None


class ResourceResponse(ResourceBase):
    id: int
    download_count: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
