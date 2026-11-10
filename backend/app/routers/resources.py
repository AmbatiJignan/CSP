import os
import shutil
import uuid
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.database.connection import get_db
from app.core.config import settings
from app.core.dependencies import get_current_admin
from app.models.resource import Resource
from app.models.user import AdminUser
from app.schemas.resource import ResourceResponse, ResourceUpdate
from app.services.audit_service import log_admin_action

router = APIRouter(prefix="/resources", tags=["Resource Library & PDFs"])


@router.get("", response_model=List[ResourceResponse])
def list_resources(
    category: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = True,
    db: Session = Depends(get_db),
):
    """Lists downloadable resources and guides."""
    query = db.query(Resource)
    if published_only:
        query = query.filter(Resource.is_published == True)
    if category:
        query = query.filter(Resource.category == category)
    if search:
        search_fmt = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                Resource.title.ilike(search_fmt),
                Resource.description.ilike(search_fmt),
            )
        )
    return query.order_by(desc(Resource.created_at)).all()


@router.get("/{resource_id}/download")
def download_resource(resource_id: int, db: Session = Depends(get_db)):
    """Downloads a resource file and increments download count."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    file_path = Path(resource.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on server")

    resource.download_count += 1
    db.commit()

    media_type = "application/pdf" if resource.file_type == "pdf" else "application/octet-stream"
    return FileResponse(
        path=str(file_path),
        filename=resource.file_name,
        media_type=media_type,
    )


@router.post("/upload", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def upload_resource(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category: str = Form("Guides"),
    is_published: bool = Form(True),
    file: UploadFile = File(...),
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin uploads a PDF guide or educational document."""
    # Validate extension
    filename = file.filename or "document.pdf"
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    allowed_exts = {"pdf", "doc", "docx", "txt", "xlsx"}
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension '.{ext}'. Allowed: {', '.join(allowed_exts)}",
        )

    # Save file with safe UUID filename
    safe_name = f"{uuid.uuid4().hex}_{filename}"
    upload_dest = Path(settings.UPLOAD_DIR) / "resources" / safe_name
    upload_dest.parent.mkdir(parents=True, exist_ok=True)

    bytes_written = 0
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    with open(upload_dest, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            bytes_written += len(chunk)
            if bytes_written > max_bytes:
                upload_dest.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB",
                )
            buffer.write(chunk)

    resource = Resource(
        title=title.strip(),
        description=description.strip() if description else None,
        category=category.strip(),
        file_path=str(upload_dest),
        file_name=filename,
        file_size_bytes=bytes_written,
        file_type=ext,
        is_published=is_published,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPLOAD",
        target_entity="RESOURCES",
        target_id=str(resource.id),
        details=f"Uploaded resource '{resource.title}' ({filename}, {bytes_written} bytes)",
    )
    return resource


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    resource_update: ResourceUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin updates resource metadata."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    update_dict = resource_update.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(resource, k, v)

    db.commit()
    db.refresh(resource)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPDATE",
        target_entity="RESOURCES",
        target_id=str(resource.id),
        details=f"Updated resource metadata '{resource.title}'",
    )
    return resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin deletes a resource and its on-disk file."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    title = resource.title
    # Safely remove file on disk
    try:
        Path(resource.file_path).unlink(missing_ok=True)
    except Exception:
        pass

    db.delete(resource)
    db.commit()

    log_admin_action(
        db=db,
        admin=current_admin,
        action="DELETE",
        target_entity="RESOURCES",
        target_id=str(resource_id),
        details=f"Deleted resource '{title}'",
    )
    return None
