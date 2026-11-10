from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Identity, func
from sqlalchemy.orm import relationship
from app.database.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, Identity(start=1), primary_key=True)
    admin_user_id = Column(Integer, ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True)
    admin_username = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)  # 'LOGIN', 'CREATE', 'UPDATE', 'DELETE', 'EXPORT'
    target_entity = Column(String(50), nullable=False)  # 'SURVEY_RESPONSES', 'ARTICLES', etc.
    target_id = Column(String(100), nullable=True)
    details = Column(String(1000), nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    admin_user = relationship("AdminUser")

    def __repr__(self) -> str:
        return f"<AuditLog(user='{self.admin_username}', action='{self.action}', entity='{self.target_entity}')>"
