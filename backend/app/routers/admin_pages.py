from typing import Optional
from fastapi import APIRouter, Depends, Request, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.connection import get_db
from app.core.config import settings
from app.core.dependencies import get_optional_admin
from app.models.user import AdminUser
from app.models.article import Article, ArticleCategory
from app.models.faq import FAQ
from app.models.resource import Resource
from app.models.feedback import Feedback
from app.models.survey import SurveyResponse
from app.models.video import EducationalVideo
from app.models.audit import AuditLog
from app.services.analytics_service import get_analytics_overview

router = APIRouter(prefix="/admin", include_in_schema=False)
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def require_admin_html(admin: Optional[AdminUser]):
    """Redirects unauthenticated browsers to admin login page."""
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    return None


@router.get("/login", response_class=HTMLResponse)
def admin_login_page(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """Admin Login Portal Page."""
    if current_admin:
        return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={"request": request, "app_name": settings.APP_NAME},
    )


@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Main Admin Dashboard with Chart.js analytics and summary statistics."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    overview = get_analytics_overview(db)
    recent_surveys = db.query(SurveyResponse).order_by(desc(SurveyResponse.id)).limit(5).all()
    recent_feedback = db.query(Feedback).order_by(desc(Feedback.created_at)).limit(5).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "request": request,
            "current_admin": current_admin,
            "overview": overview,
            "recent_surveys": recent_surveys,
            "recent_feedback": recent_feedback,
            "app_name": settings.APP_NAME,
        },
    )


@router.get("/articles", response_class=HTMLResponse)
def admin_articles_list(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Manage Articles List."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    articles = db.query(Article).order_by(desc(Article.created_at)).all()
    categories = db.query(ArticleCategory).order_by(ArticleCategory.name).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/articles.html",
        context={"request": request, "current_admin": current_admin, "articles": articles, "categories": categories},
    )


@router.get("/articles/new", response_class=HTMLResponse)
def admin_article_create(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Create Article Form."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    categories = db.query(ArticleCategory).order_by(ArticleCategory.name).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/article_form.html",
        context={"request": request, "current_admin": current_admin, "article": None, "categories": categories},
    )


@router.get("/articles/edit/{article_id}", response_class=HTMLResponse)
def admin_article_edit(
    article_id: int,
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Edit Article Form."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    article = db.query(Article).filter(Article.id == article_id).first()
    categories = db.query(ArticleCategory).order_by(ArticleCategory.name).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/article_form.html",
        context={"request": request, "current_admin": current_admin, "article": article, "categories": categories},
    )


@router.get("/faqs", response_class=HTMLResponse)
def admin_faqs(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Manage FAQs."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    faqs = db.query(FAQ).order_by(FAQ.display_order, FAQ.id).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/faqs.html",
        context={"request": request, "current_admin": current_admin, "faqs": faqs},
    )


@router.get("/resources", response_class=HTMLResponse)
def admin_resources(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Manage Downloadable Resources & PDFs."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    resources = db.query(Resource).order_by(desc(Resource.created_at)).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/resources.html",
        context={"request": request, "current_admin": current_admin, "resources": resources},
    )


@router.get("/feedback", response_class=HTMLResponse)
def admin_feedback(
    request: Request,
    status_filter: Optional[str] = Query(None, alias="status"),
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Review & Respond to Farmer / User Feedback."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    query = db.query(Feedback)
    if status_filter:
        query = query.filter(Feedback.status == status_filter)
    feedback_items = query.order_by(desc(Feedback.created_at)).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/feedback.html",
        context={"request": request, "current_admin": current_admin, "feedback_items": feedback_items, "current_filter": status_filter},
    )


@router.get("/surveys", response_class=HTMLResponse)
def admin_surveys_list(
    request: Request,
    village: Optional[str] = None,
    farming_method: Optional[str] = None,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Manage Genuine Farmer Survey Records."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    query = db.query(SurveyResponse)
    if village:
        query = query.filter(SurveyResponse.village == village)
    if farming_method:
        query = query.filter(SurveyResponse.farming_method == farming_method)
    surveys = query.order_by(desc(SurveyResponse.id)).all()

    villages = [v[0] for v in db.query(SurveyResponse.village).distinct().all()]
    methods = [m[0] for m in db.query(SurveyResponse.farming_method).distinct().all()]

    return templates.TemplateResponse(
        request=request,
        name="admin/surveys.html",
        context={
            "request": request,
            "current_admin": current_admin,
            "surveys": surveys,
            "villages": villages,
            "methods": methods,
            "selected_village": village,
            "selected_method": farming_method,
        },
    )


@router.get("/surveys/new", response_class=HTMLResponse)
def admin_survey_create(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
):
    """Add New Genuine Field Survey Record."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    return templates.TemplateResponse(
        request=request,
        name="admin/survey_form.html",
        context={"request": request, "current_admin": current_admin, "survey": None},
    )


@router.get("/surveys/edit/{survey_id}", response_class=HTMLResponse)
def admin_survey_edit(
    survey_id: int,
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Edit Existing Survey Record."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    survey = db.query(SurveyResponse).filter(SurveyResponse.id == survey_id).first()
    return templates.TemplateResponse(
        request=request,
        name="admin/survey_form.html",
        context={"request": request, "current_admin": current_admin, "survey": survey},
    )


@router.get("/surveys/{survey_id}", response_class=HTMLResponse)
def admin_survey_detail(
    survey_id: int,
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """View Individual Survey Record."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    survey = db.query(SurveyResponse).filter(SurveyResponse.id == survey_id).first()
    return templates.TemplateResponse(
        request=request,
        name="admin/survey_detail.html",
        context={"request": request, "current_admin": current_admin, "survey": survey},
    )


@router.get("/videos", response_class=HTMLResponse)
def admin_videos(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Manage Educational Videos."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    videos = db.query(EducationalVideo).order_by(EducationalVideo.display_order, desc(EducationalVideo.id)).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/videos.html",
        context={"request": request, "current_admin": current_admin, "videos": videos},
    )


@router.get("/users", response_class=HTMLResponse)
def admin_users(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Manage Administrator Accounts."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    users = db.query(AdminUser).order_by(AdminUser.id).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/users.html",
        context={"request": request, "current_admin": current_admin, "users": users},
    )


@router.get("/audit-logs", response_class=HTMLResponse)
def admin_audit_logs(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """View System Audit Trail."""
    redirect = require_admin_html(current_admin)
    if redirect:
        return redirect

    logs = db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(100).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/audit_logs.html",
        context={"request": request, "current_admin": current_admin, "logs": logs},
    )
