from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Identity, func
from sqlalchemy.orm import relationship
from app.database.base import Base


class ArticleCategory(Base):
    __tablename__ = "article_categories"

    id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    articles = relationship("Article", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ArticleCategory(id={self.id}, name='{self.name}')>"


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, Identity(start=1), primary_key=True)
    category_id = Column(Integer, ForeignKey("article_categories.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    summary = Column(String(1000), nullable=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), default="GreenGrow Team", nullable=False)
    image_url = Column(String(500), nullable=True)
    is_published = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship("ArticleCategory", back_populates="articles")

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title='{self.title[:30]}', published={self.is_published})>"
