from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.database.connection import get_db
from app.core.config import settings
from app.core.dependencies import get_optional_admin
from app.models.article import Article, ArticleCategory
from app.models.faq import FAQ
from app.models.resource import Resource
from app.models.video import EducationalVideo
from app.models.announcement import Announcement
from app.models.user import AdminUser

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def _base_context(request: Request, current_admin: Optional[AdminUser] = None):
    return {
        "request": request,
        "app_name": settings.APP_NAME,
        "current_admin": current_admin,
    }


@router.get("/", response_model=None, response_class=HTMLResponse)
def page_home(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """GreenGrow Public Homepage."""
    ctx = _base_context(request, current_admin)
    ctx["featured_articles"] = (
        db.query(Article)
        .filter(Article.is_published == True)
        .order_by(desc(Article.is_featured), desc(Article.created_at))
        .limit(3)
        .all()
    )
    ctx["featured_videos"] = (
        db.query(EducationalVideo)
        .filter(EducationalVideo.is_published == True)
        .order_by(EducationalVideo.display_order)
        .limit(3)
        .all()
    )
    ctx["announcements"] = (
        db.query(Announcement)
        .filter(Announcement.is_active == True)
        .order_by(desc(Announcement.priority), desc(Announcement.created_at))
        .limit(3)
        .all()
    )
    return templates.TemplateResponse(request=request, name="index.html", context=ctx)


@router.get("/about", response_model=None, response_class=HTMLResponse)
def page_about(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """About Organic Farming & GreenGrow Mission."""
    return templates.TemplateResponse(request=request, name="about.html", context=_base_context(request, current_admin))


@router.get("/advantages", response_model=None, response_class=HTMLResponse)
def page_advantages(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """Advantages of Organic Farming & Soil Ecology."""
    return templates.TemplateResponse(request=request, name="advantages.html", context=_base_context(request, current_admin))


@router.get("/conventional-risks", response_model=None, response_class=HTMLResponse)
def page_conventional_risks(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """Potential Risks of Poorly Managed Conventional Farming (Balanced Educational View)."""
    return templates.TemplateResponse(request=request, name="conventional_risks.html", context=_base_context(request, current_admin))


@router.get("/techniques", response_model=None, response_class=HTMLResponse)
def page_techniques(
    request: Request,
    active_tab: Optional[str] = Query("composting"),
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
):
    """Detailed Organic Farming Techniques Guide."""
    ctx = _base_context(request, current_admin)
    ctx["active_tab"] = active_tab
    return templates.TemplateResponse(request=request, name="techniques.html", context=ctx)


@router.get("/comparison", response_model=None, response_class=HTMLResponse)
def page_comparison(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """Organic vs Conventional Farming Fair Comparison Table."""
    return templates.TemplateResponse(request=request, name="comparison.html", context=_base_context(request, current_admin))


@router.get("/guidance", response_model=None, response_class=HTMLResponse)
def page_guidance(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """Farmer Transition & Practice Guidance."""
    return templates.TemplateResponse(request=request, name="guidance.html", context=_base_context(request, current_admin))


@router.get("/calculator", response_model=None, response_class=HTMLResponse)
def page_calculator(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """Organic Input Estimation Calculator."""
    return templates.TemplateResponse(request=request, name="calculator.html", context=_base_context(request, current_admin))


@router.get("/resources", response_model=None, response_class=HTMLResponse)
def page_resources(
    request: Request,
    category: Optional[str] = None,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Resources & PDF Downloads Library."""
    ctx = _base_context(request, current_admin)
    query = db.query(Resource).filter(Resource.is_published == True)
    if category:
        query = query.filter(Resource.category == category)
    ctx["resources"] = query.order_by(desc(Resource.created_at)).all()
    ctx["selected_category"] = category
    ctx["categories"] = [r[0] for r in db.query(Resource.category).distinct().all()]
    return templates.TemplateResponse(request=request, name="resources.html", context=ctx)


@router.get("/faqs", response_model=None, response_class=HTMLResponse)
def page_faqs(
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Frequently Asked Questions."""
    ctx = _base_context(request, current_admin)
    ctx["faqs"] = db.query(FAQ).filter(FAQ.is_published == True).order_by(FAQ.display_order, FAQ.id).all()
    ctx["categories"] = [c[0] for c in db.query(FAQ.category).distinct().all()]
    return templates.TemplateResponse(request=request, name="faqs.html", context=ctx)


@router.get("/contact", response_model=None, response_class=HTMLResponse)
def page_contact(request: Request, current_admin: Optional[AdminUser] = Depends(get_optional_admin)):
    """Contact & Farmer Feedback Page."""
    return templates.TemplateResponse(request=request, name="contact.html", context=_base_context(request, current_admin))


@router.get("/videos", response_model=None, response_class=HTMLResponse)
def page_videos(
    request: Request,
    category: Optional[str] = None,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Educational Organic Farming Video Library."""
    ctx = _base_context(request, current_admin)
    query = db.query(EducationalVideo).filter(EducationalVideo.is_published == True)
    if category:
        query = query.filter(EducationalVideo.category == category)
    ctx["videos"] = query.order_by(EducationalVideo.display_order, desc(EducationalVideo.id)).all()
    ctx["selected_category"] = category
    ctx["categories"] = [c[0] for c in db.query(EducationalVideo.category).distinct().all()]
    return templates.TemplateResponse(request=request, name="videos.html", context=ctx)


@router.get("/articles/{slug}", response_model=None, response_class=HTMLResponse)
def page_article_detail(
    slug: str,
    request: Request,
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Article Reading Page."""
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        return templates.TemplateResponse(request=request, name="404.html", context=_base_context(request, current_admin), status_code=404)
    article.view_count += 1
    db.commit()
    ctx = _base_context(request, current_admin)
    ctx["article"] = article
    ctx["recent_articles"] = (
        db.query(Article)
        .filter(Article.is_published == True, Article.id != article.id)
        .order_by(desc(Article.created_at))
        .limit(4)
        .all()
    )
    return templates.TemplateResponse(request=request, name="article_detail.html", context=ctx)


@router.get("/search", response_model=None, response_class=HTMLResponse)
def page_search(
    request: Request,
    q: Optional[str] = Query(None),
    current_admin: Optional[AdminUser] = Depends(get_optional_admin),
    db: Session = Depends(get_db),
):
    """Global Portal Search across Articles, Techniques, Resources, and FAQs."""
    ctx = _base_context(request, current_admin)
    ctx["query"] = q or ""
    results = {"articles": [], "faqs": [], "resources": [], "videos": []}
    if q and q.strip():
        search_fmt = f"%{q.strip().lower()}%"
        results["articles"] = (
            db.query(Article)
            .filter(
                Article.is_published == True,
                or_(Article.title.ilike(search_fmt), Article.summary.ilike(search_fmt), Article.content.ilike(search_fmt)),
            )
            .limit(10)
            .all()
        )
        results["faqs"] = (
            db.query(FAQ)
            .filter(
                FAQ.is_published == True,
                or_(FAQ.question.ilike(search_fmt), FAQ.answer.ilike(search_fmt)),
            )
            .limit(10)
            .all()
        )
        results["resources"] = (
            db.query(Resource)
            .filter(
                Resource.is_published == True,
                or_(Resource.title.ilike(search_fmt), Resource.description.ilike(search_fmt)),
            )
            .limit(10)
            .all()
        )
        results["videos"] = (
            db.query(EducationalVideo)
            .filter(
                EducationalVideo.is_published == True,
                or_(EducationalVideo.title.ilike(search_fmt), EducationalVideo.description.ilike(search_fmt)),
            )
            .limit(10)
            .all()
        )
    ctx["results"] = results
    ctx["total_matches"] = sum(len(v) for v in results.values())
    return templates.TemplateResponse(request=request, name="search.html", context=ctx)
