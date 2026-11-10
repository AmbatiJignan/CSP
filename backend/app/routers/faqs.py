from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.faq import FAQ
from app.models.user import AdminUser
from app.schemas.faq import FAQResponse, FAQCreate, FAQUpdate
from app.services.audit_service import log_admin_action

router = APIRouter(prefix="/faqs", tags=["FAQs"])


@router.get("", response_model=List[FAQResponse])
def list_faqs(
    category: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = True,
    db: Session = Depends(get_db),
):
    """Lists FAQs ordered by display order with optional category filtering and search."""
    query = db.query(FAQ)
    if published_only:
        query = query.filter(FAQ.is_published == True)
    if category:
        query = query.filter(FAQ.category == category)
    if search:
        search_fmt = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                FAQ.question.ilike(search_fmt),
                FAQ.answer.ilike(search_fmt),
            )
        )
    return query.order_by(FAQ.display_order, FAQ.id).all()


@router.post("", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
def create_faq(
    faq_in: FAQCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin creates a new FAQ."""
    faq = FAQ(
        category=faq_in.category,
        question=faq_in.question,
        answer=faq_in.answer,
        display_order=faq_in.display_order,
        is_published=faq_in.is_published,
    )
    db.add(faq)
    db.commit()
    db.refresh(faq)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="CREATE",
        target_entity="FAQS",
        target_id=str(faq.id),
        details=f"Created FAQ '{faq.question[:40]}'",
    )
    return faq


@router.put("/{faq_id}", response_model=FAQResponse)
def update_faq(
    faq_id: int,
    faq_update: FAQUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin updates an FAQ."""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAQ not found")

    update_dict = faq_update.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(faq, k, v)

    db.commit()
    db.refresh(faq)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPDATE",
        target_entity="FAQS",
        target_id=str(faq.id),
        details=f"Updated FAQ '{faq.question[:40]}'",
    )
    return faq


@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(
    faq_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin deletes an FAQ."""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAQ not found")

    q = faq.question
    db.delete(faq)
    db.commit()

    log_admin_action(
        db=db,
        admin=current_admin,
        action="DELETE",
        target_entity="FAQS",
        target_id=str(faq_id),
        details=f"Deleted FAQ '{q[:40]}'",
    )
    return None
