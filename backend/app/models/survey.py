from datetime import date, datetime
from sqlalchemy import Column, Integer, Float, String, Text, Boolean, Date, DateTime, Identity, func
from app.database.base import Base


class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, Identity(start=1), primary_key=True)
    respondent_code = Column(String(50), unique=True, nullable=False)
    village = Column(String(100), default="Tholukodu", nullable=False)
    farming_experience_years = Column(Integer, nullable=True)
    land_holding_acres = Column(Float, nullable=True)
    primary_crops = Column(String(255), nullable=True)
    farming_method = Column(String(50), nullable=False)  # 'Conventional', 'Partially Organic', 'Fully Organic', 'Natural Farming'
    organic_input_usage = Column(String(255), nullable=True)  # e.g., 'Farmyard Manure, Vermicompost'
    awareness_level = Column(String(50), nullable=False)  # 'High', 'Moderate', 'Basic', 'None'
    knowledge_of_advantages = Column(String(500), nullable=True)
    primary_challenges = Column(String(500), nullable=True)
    willingness_to_adopt = Column(String(50), nullable=False)  # 'Highly Willing', 'Willing with Support', 'Undecided', 'Reluctant'
    support_needed = Column(String(500), nullable=True)
    additional_comments = Column(Text, nullable=True)
    consent_confirmed = Column(Boolean, default=True, nullable=False)
    survey_date = Column(Date, default=func.current_date(), nullable=False)
    surveyor_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<SurveyResponse(code='{self.respondent_code}', village='{self.village}', method='{self.farming_method}')>"
