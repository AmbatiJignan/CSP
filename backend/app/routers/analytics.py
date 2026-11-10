from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.user import AdminUser
from app.schemas.analytics import AnalyticsOverview
from app.services.analytics_service import get_analytics_overview

router = APIRouter(prefix="/analytics", tags=["Analytics & Chart Data"])


@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics(
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Returns aggregated analytics strictly computed from actual database records.
    Powers the Chart.js visualisations on the Admin Dashboard.
    """
    return get_analytics_overview(db)
