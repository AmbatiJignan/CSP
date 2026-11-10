from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Identity, func
from app.database.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, Identity(start=1), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), default="Guides", nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size_bytes = Column(Integer, default=0, nullable=False)
    file_type = Column(String(50), default="pdf", nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Resource(id={self.id}, title='{self.title[:30]}')>"
