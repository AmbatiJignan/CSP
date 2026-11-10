from collections import Counter
from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.survey import SurveyResponse
from app.models.article import Article
from app.models.resource import Resource
from app.models.faq import FAQ
from app.models.feedback import Feedback
from app.schemas.analytics import AnalyticsOverview, DistributionItem


def _to_distribution(counter: Counter, total_records: int) -> List[DistributionItem]:
    """Converts a Counter into sorted DistributionItem list with percentages."""
    items = []
    # If no records, return empty list
    if not counter or total_records <= 0:
        return items

    for label, count in counter.most_common():
        percentage = round((count / total_records) * 100, 1)
        items.append(DistributionItem(label=label, count=count, percentage=percentage))
    return items


def get_analytics_overview(db: Session) -> AnalyticsOverview:
    """
    Computes comprehensive analytics based STRICTLY on actual database records.
    Never fabricates or hardcodes percentages or survey responses.
    """
    # 1. System counts
    total_articles = db.query(Article).count()
    total_resources = db.query(Resource).count()
    total_faqs = db.query(FAQ).count()
    total_feedback = db.query(Feedback).count()
    feedback_new = db.query(Feedback).filter(Feedback.status == "New").count()
    feedback_reviewed = db.query(Feedback).filter(Feedback.status == "Reviewed").count()
    feedback_resolved = db.query(Feedback).filter(Feedback.status == "Resolved").count()

    # 2. Survey records
    surveys = db.query(SurveyResponse).all()
    total_surveys = len(surveys)
    has_real_survey_data = total_surveys > 0

    if not has_real_survey_data:
        return AnalyticsOverview(
            total_responses=0,
            total_articles=total_articles,
            total_resources=total_resources,
            total_faqs=total_faqs,
            total_feedback=total_feedback,
            feedback_new=feedback_new,
            feedback_reviewed=feedback_reviewed,
            feedback_resolved=feedback_resolved,
            farming_methods=[],
            awareness_levels=[],
            willingness_levels=[],
            organic_inputs=[],
            challenges=[],
            crops=[],
            villages=[],
            timeline=[],
            has_real_survey_data=False,
        )

    # 3. Aggregate survey statistics
    methods_counter = Counter()
    awareness_counter = Counter()
    willingness_counter = Counter()
    village_counter = Counter()
    timeline_counter = Counter()
    inputs_counter = Counter()
    challenges_counter = Counter()
    crops_counter = Counter()

    for s in surveys:
        if s.farming_method:
            methods_counter[s.farming_method.strip()] += 1
        if s.awareness_level:
            awareness_counter[s.awareness_level.strip()] += 1
        if s.willingness_to_adopt:
            willingness_counter[s.willingness_to_adopt.strip()] += 1
        if s.village:
            village_counter[s.village.strip()] += 1
        if s.survey_date:
            date_str = s.survey_date.strftime("%Y-%m-%d")
            timeline_counter[date_str] += 1

        # Multi-value comma-separated fields
        if s.organic_input_usage:
            for item in s.organic_input_usage.split(","):
                cleaned = item.strip()
                if cleaned:
                    inputs_counter[cleaned] += 1

        if s.primary_challenges:
            for item in s.primary_challenges.split(","):
                cleaned = item.strip()
                if cleaned:
                    challenges_counter[cleaned] += 1

        if s.primary_crops:
            for item in s.primary_crops.split(","):
                cleaned = item.strip()
                if cleaned:
                    crops_counter[cleaned] += 1

    # Format timeline chronologically
    sorted_timeline = sorted(timeline_counter.items(), key=lambda x: x[0])
    timeline_items = [
        DistributionItem(
            label=date_str,
            count=count,
            percentage=round((count / total_surveys) * 100, 1),
        )
        for date_str, count in sorted_timeline
    ]

    return AnalyticsOverview(
        total_responses=total_surveys,
        total_articles=total_articles,
        total_resources=total_resources,
        total_faqs=total_faqs,
        total_feedback=total_feedback,
        feedback_new=feedback_new,
        feedback_reviewed=feedback_reviewed,
        feedback_resolved=feedback_resolved,
        farming_methods=_to_distribution(methods_counter, total_surveys),
        awareness_levels=_to_distribution(awareness_counter, total_surveys),
        willingness_levels=_to_distribution(willingness_counter, total_surveys),
        organic_inputs=_to_distribution(inputs_counter, total_surveys),
        challenges=_to_distribution(challenges_counter, total_surveys),
        crops=_to_distribution(crops_counter, total_surveys),
        villages=_to_distribution(village_counter, total_surveys),
        timeline=timeline_items,
        has_real_survey_data=True,
    )
