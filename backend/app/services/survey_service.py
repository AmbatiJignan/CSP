from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.models.survey import SurveyResponse
from app.schemas.survey import SurveyResponseCreate, SurveyResponseUpdate


def get_surveys(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    village: Optional[str] = None,
    farming_method: Optional[str] = None,
    awareness_level: Optional[str] = None,
    willingness: Optional[str] = None,
) -> Tuple[List[SurveyResponse], int]:
    """Retrieves paginated survey responses with optional filters."""
    query = db.query(SurveyResponse)

    if search:
        search_fmt = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                SurveyResponse.respondent_code.ilike(search_fmt),
                SurveyResponse.village.ilike(search_fmt),
                SurveyResponse.primary_crops.ilike(search_fmt),
                SurveyResponse.farming_method.ilike(search_fmt),
                SurveyResponse.surveyor_name.ilike(search_fmt),
            )
        )

    if village:
        query = query.filter(SurveyResponse.village == village)
    if farming_method:
        query = query.filter(SurveyResponse.farming_method == farming_method)
    if awareness_level:
        query = query.filter(SurveyResponse.awareness_level == awareness_level)
    if willingness:
        query = query.filter(SurveyResponse.willingness_to_adopt == willingness)

    total = query.count()
    items = query.order_by(desc(SurveyResponse.survey_date), desc(SurveyResponse.id)).offset(skip).limit(limit).all()
    return items, total


def get_survey_by_id(db: Session, survey_id: int) -> Optional[SurveyResponse]:
    """Finds a survey response by primary key ID."""
    return db.query(SurveyResponse).filter(SurveyResponse.id == survey_id).first()


def get_survey_by_code(db: Session, respondent_code: str) -> Optional[SurveyResponse]:
    """Finds a survey response by unique respondent code."""
    return db.query(SurveyResponse).filter(SurveyResponse.respondent_code == respondent_code.strip()).first()


def create_survey(db: Session, survey_in: SurveyResponseCreate) -> SurveyResponse:
    """Inserts a genuine field survey record into Oracle Database."""
    survey = SurveyResponse(
        respondent_code=survey_in.respondent_code.strip(),
        village=survey_in.village.strip(),
        farming_experience_years=survey_in.farming_experience_years,
        land_holding_acres=survey_in.land_holding_acres,
        primary_crops=survey_in.primary_crops,
        farming_method=survey_in.farming_method,
        organic_input_usage=survey_in.organic_input_usage,
        awareness_level=survey_in.awareness_level,
        knowledge_of_advantages=survey_in.knowledge_of_advantages,
        primary_challenges=survey_in.primary_challenges,
        willingness_to_adopt=survey_in.willingness_to_adopt,
        support_needed=survey_in.support_needed,
        additional_comments=survey_in.additional_comments,
        consent_confirmed=survey_in.consent_confirmed,
        survey_date=survey_in.survey_date,
        surveyor_name=survey_in.surveyor_name,
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey


def update_survey(
    db: Session,
    survey: SurveyResponse,
    survey_update: SurveyResponseUpdate
) -> SurveyResponse:
    """Updates fields of an existing survey record."""
    update_data = survey_update.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(survey, field, val)
    db.commit()
    db.refresh(survey)
    return survey


def delete_survey(db: Session, survey: SurveyResponse) -> None:
    """Deletes a survey record from Oracle Database."""
    db.delete(survey)
    db.commit()
