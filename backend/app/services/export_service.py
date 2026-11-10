import io
from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from app.models.survey import SurveyResponse


def export_surveys_to_csv(db: Session) -> io.StringIO:
    """
    Exports all actual survey responses from Oracle Database 23ai to a CSV buffer using Pandas.
    Does not invent survey results or percentages.
    """
    surveys = db.query(SurveyResponse).order_by(SurveyResponse.id).all()

    data = []
    for s in surveys:
        data.append({
            "Respondent Code": s.respondent_code,
            "Village": s.village,
            "Farming Experience (Years)": s.farming_experience_years if s.farming_experience_years is not None else "",
            "Land Holding (Acres)": s.land_holding_acres if s.land_holding_acres is not None else "",
            "Primary Crops": s.primary_crops or "",
            "Farming Method": s.farming_method or "",
            "Organic Input Usage": s.organic_input_usage or "",
            "Awareness Level": s.awareness_level or "",
            "Knowledge of Advantages": s.knowledge_of_advantages or "",
            "Primary Challenges": s.primary_challenges or "",
            "Willingness to Adopt": s.willingness_to_adopt or "",
            "Support Needed": s.support_needed or "",
            "Additional Comments": s.additional_comments or "",
            "Consent Confirmed": "Yes" if s.consent_confirmed else "No",
            "Survey Date": s.survey_date.strftime("%Y-%m-%d") if s.survey_date else "",
            "Surveyor Name": s.surveyor_name or "",
        })

    columns = [
        "Respondent Code",
        "Village",
        "Farming Experience (Years)",
        "Land Holding (Acres)",
        "Primary Crops",
        "Farming Method",
        "Organic Input Usage",
        "Awareness Level",
        "Knowledge of Advantages",
        "Primary Challenges",
        "Willingness to Adopt",
        "Support Needed",
        "Additional Comments",
        "Consent Confirmed",
        "Survey Date",
        "Surveyor Name",
    ]
    df = pd.DataFrame(data, columns=columns)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_buffer.seek(0)
    return csv_buffer
