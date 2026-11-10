from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Identity, func
from app.database.base import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, Identity(start=1), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="admin", nullable=False)  # 'superadmin', 'admin', 'editor'
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<AdminUser(id={self.id}, username='{self.username}', role='{self.role}')>"
