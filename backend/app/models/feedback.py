from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Identity, func
from app.database.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), default="New", nullable=False)  # 'New', 'Reviewed', 'Resolved'
    admin_notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, subject='{self.subject[:25]}', status='{self.status}')>"
