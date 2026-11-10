from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Identity, func
from app.database.base import Base


class EducationalVideo(Base):
    __tablename__ = "educational_videos"

    id = Column(Integer, Identity(start=1), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), default="Composting", nullable=False)
    video_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<EducationalVideo(id={self.id}, title='{self.title[:30]}')>"
