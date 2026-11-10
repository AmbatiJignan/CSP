import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.models.user import AdminUser

logger = logging.getLogger("greengrow.audit")


def log_admin_action(
    db: Session,
    admin: AdminUser,
    action: str,
    target_entity: str,
    target_id: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> AuditLog:
    """Records an administrative action in the Oracle AUDIT_LOGS table."""
    try:
        log_entry = AuditLog(
            admin_user_id=admin.id if admin else None,
            admin_username=admin.username if admin else "system",
            action=action.upper(),
            target_entity=target_entity.upper(),
            target_id=str(target_id) if target_id is not None else None,
            details=details,
            ip_address=ip_address,
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to record audit log: {exc}")
        return None
