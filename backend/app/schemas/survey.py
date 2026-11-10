from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class SurveyResponseBase(BaseModel):
    respondent_code: str = Field(..., min_length=2, max_length=50)
    village: str = Field(default="Tholukodu", max_length=100)
    farming_experience_years: Optional[int] = Field(None, ge=0, le=100)
    land_holding_acres: Optional[float] = Field(None, ge=0.0)
    primary_crops: Optional[str] = Field(None, max_length=255)
    farming_method: str = Field(..., max_length=50)
    organic_input_usage: Optional[str] = Field(None, max_length=255)
    awareness_level: str = Field(..., max_length=50)
    knowledge_of_advantages: Optional[str] = Field(None, max_length=500)
    primary_challenges: Optional[str] = Field(None, max_length=500)
    willingness_to_adopt: str = Field(..., max_length=50)
    support_needed: Optional[str] = Field(None, max_length=500)
    additional_comments: Optional[str] = None
    consent_confirmed: bool = True
    survey_date: date = Field(default_factory=date.today)
    surveyor_name: Optional[str] = Field(None, max_length=100)


class SurveyResponseCreate(SurveyResponseBase):
    pass


class SurveyResponseUpdate(BaseModel):
    village: Optional[str] = None
    farming_experience_years: Optional[int] = None
    land_holding_acres: Optional[float] = None
    primary_crops: Optional[str] = None
    farming_method: Optional[str] = None
    organic_input_usage: Optional[str] = None
    awareness_level: Optional[str] = None
    knowledge_of_advantages: Optional[str] = None
    primary_challenges: Optional[str] = None
    willingness_to_adopt: Optional[str] = None
    support_needed: Optional[str] = None
    additional_comments: Optional[str] = None
    consent_confirmed: Optional[bool] = None
    survey_date: Optional[date] = None
    surveyor_name: Optional[str] = None


class SurveyResponseResponse(SurveyResponseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SurveyListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[SurveyResponseResponse]
