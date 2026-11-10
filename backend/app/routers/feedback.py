from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.feedback import Feedback
from app.models.user import AdminUser
from app.schemas.feedback import FeedbackResponse, FeedbackCreate, FeedbackUpdate
from app.services.audit_service import log_admin_action

router = APIRouter(prefix="/feedback", tags=["Contact & Feedback"])


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(feedback_in: FeedbackCreate, db: Session = Depends(get_db)):
    """Public submission of farmer/visitor contact and feedback."""
    feedback = Feedback(
        name=feedback_in.name.strip() if feedback_in.name else None,
        email=feedback_in.email.strip() if feedback_in.email else None,
        phone=feedback_in.phone.strip() if feedback_in.phone else None,
        subject=feedback_in.subject.strip(),
        message=feedback_in.message.strip(),
        status="New",
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("", response_model=List[FeedbackResponse])
def list_feedback(
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin retrieves all feedback messages with filtering."""
    query = db.query(Feedback)
    if status_filter:
        query = query.filter(Feedback.status == status_filter)
    if search:
        search_fmt = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                Feedback.name.ilike(search_fmt),
                Feedback.email.ilike(search_fmt),
                Feedback.subject.ilike(search_fmt),
                Feedback.message.ilike(search_fmt),
            )
        )
    return query.order_by(desc(Feedback.created_at)).all()


@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback_status(
    feedback_id: int,
    feedback_update: FeedbackUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin updates feedback status (New, Reviewed, Resolved) or notes."""
    item = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

    if feedback_update.status is not None:
        valid_statuses = {"New", "Reviewed", "Resolved"}
        if feedback_update.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status '{feedback_update.status}'. Allowed: {', '.join(valid_statuses)}",
            )
        item.status = feedback_update.status

    if feedback_update.admin_notes is not None:
        item.admin_notes = feedback_update.admin_notes

    db.commit()
    db.refresh(item)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPDATE",
        target_entity="FEEDBACK",
        target_id=str(item.id),
        details=f"Updated feedback #{item.id} status to '{item.status}'",
    )
    return item


@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(
    feedback_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin deletes a feedback message."""
    item = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

    db.delete(item)
    db.commit()

    log_admin_action(
        db=db,
        admin=current_admin,
        action="DELETE",
        target_entity="FEEDBACK",
        target_id=str(feedback_id),
        details=f"Deleted feedback #{feedback_id}",
    )
    return None
