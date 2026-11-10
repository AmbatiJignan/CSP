from typing import Dict, List, Optional
from pydantic import BaseModel


class DistributionItem(BaseModel):
    label: str
    count: int
    percentage: float


class MetricCard(BaseModel):
    label: str
    value: int
    subtitle: Optional[str] = None


class AnalyticsOverview(BaseModel):
    total_responses: int
    total_articles: int
    total_resources: int
    total_faqs: int
    total_feedback: int
    feedback_new: int
    feedback_reviewed: int
    feedback_resolved: int
    farming_methods: List[DistributionItem]
    awareness_levels: List[DistributionItem]
    willingness_levels: List[DistributionItem]
    organic_inputs: List[DistributionItem]
    challenges: List[DistributionItem]
    crops: List[DistributionItem]
    villages: List[DistributionItem]
    timeline: List[DistributionItem]
    has_real_survey_data: bool
