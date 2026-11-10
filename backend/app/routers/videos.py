from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.video import EducationalVideo
from app.models.user import AdminUser
from app.schemas.video import (
    EducationalVideoResponse,
    EducationalVideoCreate,
    EducationalVideoUpdate,
)
from app.services.audit_service import log_admin_action

router = APIRouter(prefix="/videos", tags=["Video Library"])


@router.get("", response_model=List[EducationalVideoResponse])
def list_videos(
    category: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = True,
    db: Session = Depends(get_db),
):
    """Lists educational videos with optional category and search filters."""
    query = db.query(EducationalVideo)
    if published_only:
        query = query.filter(EducationalVideo.is_published == True)
    if category:
        query = query.filter(EducationalVideo.category == category)
    if search:
        search_fmt = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                EducationalVideo.title.ilike(search_fmt),
                EducationalVideo.description.ilike(search_fmt),
            )
        )
    return query.order_by(EducationalVideo.display_order, desc(EducationalVideo.id)).all()


@router.post("", response_model=EducationalVideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(
    video_in: EducationalVideoCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin adds an educational video."""
    video = EducationalVideo(
        title=video_in.title.strip(),
        description=video_in.description.strip() if video_in.description else None,
        category=video_in.category.strip(),
        video_url=video_in.video_url.strip(),
        thumbnail_url=video_in.thumbnail_url.strip() if video_in.thumbnail_url else None,
        duration_minutes=video_in.duration_minutes,
        display_order=video_in.display_order,
        is_published=video_in.is_published,
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="CREATE",
        target_entity="EDUCATIONAL_VIDEOS",
        target_id=str(video.id),
        details=f"Added video '{video.title}'",
    )
    return video


@router.put("/{video_id}", response_model=EducationalVideoResponse)
def update_video(
    video_id: int,
    video_update: EducationalVideoUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin updates an educational video."""
    video = db.query(EducationalVideo).filter(EducationalVideo.id == video_id).first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    update_dict = video_update.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(video, k, v)

    db.commit()
    db.refresh(video)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPDATE",
        target_entity="EDUCATIONAL_VIDEOS",
        target_id=str(video.id),
        details=f"Updated video '{video.title}'",
    )
    return video


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(
    video_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin deletes an educational video."""
    video = db.query(EducationalVideo).filter(EducationalVideo.id == video_id).first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    title = video.title
    db.delete(video)
    db.commit()

    log_admin_action(
        db=db,
        admin=current_admin,
        action="DELETE",
        target_entity="EDUCATIONAL_VIDEOS",
        target_id=str(video_id),
        details=f"Deleted video '{title}'",
    )
    return None
