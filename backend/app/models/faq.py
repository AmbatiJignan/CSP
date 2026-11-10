from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Identity, func
from app.database.base import Base


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, Identity(start=1), primary_key=True)
    category = Column(String(50), default="General", nullable=False)
    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<FAQ(id={self.id}, question='{self.question[:30]}')>"
