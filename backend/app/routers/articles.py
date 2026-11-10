from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.database.connection import get_db
from app.core.dependencies import get_current_admin
from app.models.article import Article, ArticleCategory
from app.models.user import AdminUser
from app.schemas.article import (
    ArticleResponse,
    ArticleCreate,
    ArticleUpdate,
    ArticleCategoryResponse,
    ArticleCategoryCreate,
)
from app.services.audit_service import log_admin_action

router = APIRouter(prefix="/articles", tags=["Articles & Educational Content"])


@router.get("/categories/all", response_model=List[ArticleCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Public list of article categories ordered by display order."""
    return db.query(ArticleCategory).order_by(ArticleCategory.display_order, ArticleCategory.name).all()


@router.post("/categories", response_model=ArticleCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: ArticleCategoryCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin creates a new article category."""
    existing = db.query(ArticleCategory).filter(
        or_(ArticleCategory.name == cat_in.name, ArticleCategory.slug == cat_in.slug)
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name or slug already exists")

    cat = ArticleCategory(
        name=cat_in.name,
        slug=cat_in.slug,
        description=cat_in.description,
        display_order=cat_in.display_order,
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.get("", response_model=List[ArticleResponse])
def list_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    category_slug: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = True,
    db: Session = Depends(get_db),
):
    """Lists articles with search, category filtering and pagination."""
    query = db.query(Article)
    if published_only:
        query = query.filter(Article.is_published == True)

    if category_id:
        query = query.filter(Article.category_id == category_id)
    elif category_slug:
        query = query.join(Article.category).filter(ArticleCategory.slug == category_slug)

    if search:
        search_fmt = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                Article.title.ilike(search_fmt),
                Article.summary.ilike(search_fmt),
                Article.content.ilike(search_fmt),
            )
        )

    return query.order_by(desc(Article.created_at)).offset(skip).limit(limit).all()


@router.get("/{slug_or_id}", response_model=ArticleResponse)
def get_article(slug_or_id: str, db: Session = Depends(get_db)):
    """Retrieves an article by slug or ID and increments view count."""
    if slug_or_id.isdigit():
        article = db.query(Article).filter(Article.id == int(slug_or_id)).first()
    else:
        article = db.query(Article).filter(Article.slug == slug_or_id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    article.view_count += 1
    db.commit()
    db.refresh(article)
    return article


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article_in: ArticleCreate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin creates a new educational article."""
    existing = db.query(Article).filter(Article.slug == article_in.slug).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Article slug already exists")

    article = Article(
        category_id=article_in.category_id,
        title=article_in.title,
        slug=article_in.slug,
        summary=article_in.summary,
        content=article_in.content,
        author=article_in.author,
        image_url=article_in.image_url,
        is_published=article_in.is_published,
        is_featured=article_in.is_featured,
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="CREATE",
        target_entity="ARTICLES",
        target_id=str(article.id),
        details=f"Created article '{article.title}'",
    )
    return article


@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin updates an article."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    update_dict = article_update.model_dump(exclude_unset=True)
    if "slug" in update_dict and update_dict["slug"] != article.slug:
        dup = db.query(Article).filter(Article.slug == update_dict["slug"]).first()
        if dup:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slug already in use")

    for k, v in update_dict.items():
        setattr(article, k, v)

    db.commit()
    db.refresh(article)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPDATE",
        target_entity="ARTICLES",
        target_id=str(article.id),
        details=f"Updated article '{article.title}'",
    )
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin deletes an article."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    title = article.title
    db.delete(article)
    db.commit()

    log_admin_action(
        db=db,
        admin=current_admin,
        action="DELETE",
        target_entity="ARTICLES",
        target_id=str(article_id),
        details=f"Deleted article '{title}'",
    )
    return None
