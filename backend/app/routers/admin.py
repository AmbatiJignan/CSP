from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.user import AdminUser
from app.models.audit import AuditLog
from app.schemas.audit import AuditLogResponse
from app.services.analytics_service import get_analytics_overview

router = APIRouter(prefix="/admin", tags=["Admin Portal & Audit Logs"])


@router.get("/stats")
def get_admin_dashboard_stats(
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Returns summary count statistics for the admin dashboard header."""
    overview = get_analytics_overview(db)
    return {
        "total_articles": overview.total_articles,
        "total_resources": overview.total_resources,
        "total_faqs": overview.total_faqs,
        "total_feedback": overview.total_feedback,
        "feedback_new": overview.feedback_new,
        "feedback_reviewed": overview.feedback_reviewed,
        "feedback_resolved": overview.feedback_resolved,
        "total_surveys": overview.total_responses,
        "has_real_survey_data": overview.has_real_survey_data,
    }


@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    action: Optional[str] = None,
    target_entity: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin views recent audit logs for security and compliance."""
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action.upper())
    if target_entity:
        query = query.filter(AuditLog.target_entity == target_entity.upper())
    return query.order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
