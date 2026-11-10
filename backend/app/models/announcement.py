from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Identity, func
from app.database.base import Base


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, Identity(start=1), primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(1000), nullable=False)
    link_url = Column(String(500), nullable=True)
    priority = Column(String(20), default="Normal", nullable=False)  # 'Low', 'Normal', 'High'
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Announcement(id={self.id}, title='{self.title[:30]}')>"
