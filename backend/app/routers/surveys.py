from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.survey import SurveyResponse
from app.models.user import AdminUser
from app.schemas.survey import (
    SurveyResponseResponse,
    SurveyResponseCreate,
    SurveyResponseUpdate,
    SurveyListResponse,
)
from app.services import survey_service
from app.services.export_service import export_surveys_to_csv
from app.services.pdf_service import generate_survey_pdf_report
from app.services.audit_service import log_admin_action

router = APIRouter(prefix="/surveys", tags=["Farmer Survey Management"])


@router.get("", response_model=SurveyListResponse)
def list_surveys(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    village: Optional[str] = None,
    farming_method: Optional[str] = None,
    awareness_level: Optional[str] = None,
    willingness: Optional[str] = None,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin retrieves paginated list of farmer survey records with filters."""
    items, total = survey_service.get_surveys(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        village=village,
        farming_method=farming_method,
        awareness_level=awareness_level,
        willingness=willingness,
    )
    return SurveyListResponse(
        total=total,
        page=(skip // limit) + 1,
        per_page=limit,
        items=items,
    )


@router.get("/export/csv")
def export_csv(
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Exports genuine farmer survey responses to CSV using Pandas."""
    csv_stream = export_surveys_to_csv(db)
    filename = f"greengrow_tholukodu_survey_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    log_admin_action(
        db=db,
        admin=current_admin,
        action="EXPORT_CSV",
        target_entity="SURVEY_RESPONSES",
        details="Exported survey records to CSV",
    )

    return StreamingResponse(
        iter([csv_stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/export/pdf")
def export_pdf(
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Generates and downloads a complete ReportLab PDF field report."""
    pdf_stream = generate_survey_pdf_report(db)
    filename = f"greengrow_survey_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    log_admin_action(
        db=db,
        admin=current_admin,
        action="EXPORT_PDF",
        target_entity="SURVEY_RESPONSES",
        details="Generated ReportLab PDF survey report",
    )

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/{survey_id}", response_model=SurveyResponseResponse)
def get_survey(
    survey_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin retrieves a single farmer survey record."""
    survey = survey_service.get_survey_by_id(db, survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey record not found")
    return survey


@router.post("", response_model=SurveyResponseResponse, status_code=status.HTTP_201_CREATED)
def create_survey_response(
    survey_in: SurveyResponseCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin records a genuine farmer survey response into Oracle 23ai."""
    existing = survey_service.get_survey_by_code(db, survey_in.respondent_code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Respondent code '{survey_in.respondent_code}' already exists",
        )

    survey = survey_service.create_survey(db, survey_in)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="CREATE",
        target_entity="SURVEY_RESPONSES",
        target_id=str(survey.id),
        details=f"Entered survey record for {survey.respondent_code} ({survey.village})",
    )
    return survey


@router.put("/{survey_id}", response_model=SurveyResponseResponse)
def update_survey_response(
    survey_id: int,
    survey_update: SurveyResponseUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin updates an existing survey record."""
    survey = survey_service.get_survey_by_id(db, survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey record not found")

    updated = survey_service.update_survey(db, survey, survey_update)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPDATE",
        target_entity="SURVEY_RESPONSES",
        target_id=str(survey.id),
        details=f"Updated survey record for {survey.respondent_code}",
    )
    return updated


@router.delete("/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_survey_response(
    survey_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin deletes a survey record."""
    survey = survey_service.get_survey_by_id(db, survey_id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey record not found")

    code = survey.respondent_code
    survey_service.delete_survey(db, survey)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="DELETE",
        target_entity="SURVEY_RESPONSES",
        target_id=str(survey_id),
        details=f"Deleted survey record {code}",
    )
    return None
