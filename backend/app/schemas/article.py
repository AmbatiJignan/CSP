from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ArticleCategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    display_order: int = 0


class ArticleCategoryCreate(ArticleCategoryBase):
    pass


class ArticleCategoryResponse(ArticleCategoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ArticleBase(BaseModel):
    category_id: Optional[int] = None
    title: str = Field(..., min_length=3, max_length=255)
    slug: str = Field(..., min_length=3, max_length=255)
    summary: Optional[str] = Field(None, max_length=1000)
    content: str
    author: str = Field(default="GreenGrow Team", max_length=100)
    image_url: Optional[str] = Field(None, max_length=500)
    is_published: bool = True
    is_featured: bool = False


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    slug: Optional[str] = Field(None, min_length=3, max_length=255)
    summary: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None


class ArticleResponse(ArticleBase):
    id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    category: Optional[ArticleCategoryResponse] = None
    model_config = ConfigDict(from_attributes=True)
