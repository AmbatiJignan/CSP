import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from app.core.config import settings
from app.database.connection import check_db_health
from app.routers import (
    pages,
    admin_pages,
    auth,
    articles,
    faqs,
    resources,
    feedback,
    surveys,
    analytics,
    videos,
    calculator,
    admin,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("greengrow.app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown events."""
    logger.info("Initializing GreenGrow Organic Farming Portal...")
    # Verify Oracle Database 23ai health check on startup
    db_status = check_db_health()
    if db_status.get("status") == "healthy":
        logger.info(f"Oracle Database 23ai connection established ({settings.ORACLE_SERVICE_NAME} on {settings.ORACLE_HOST}:{settings.ORACLE_PORT})")
    else:
        logger.warning(f"Oracle Database 23ai health check reported: {db_status}")
    yield
    logger.info("Shutting down GreenGrow application cleanly.")


app = FastAPI(
    title=settings.APP_NAME,
    description="GreenGrow – Organic Farming Awareness & Farmer Guidance Portal with Oracle Database 23ai backend.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files & Uploads
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


# Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic validation errors cleanly."""
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": jsonable_encoder(exc.errors())},
        )
    return HTMLResponse(
        content=f"<h3>Input Validation Error</h3><p>{jsonable_encoder(exc.errors())}</p>",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


# Health Check Endpoint
@app.get("/health", tags=["System Health"])
def health_check():
    """System and Oracle Database 23ai connection health endpoint."""
    db_health = check_db_health()
    overall_status = "ok" if db_health.get("status") == "healthy" else "degraded"
    return {
        "status": overall_status,
        "app_name": settings.APP_NAME,
        "database": db_health,
        "version": "1.0.0",
    }


# Include Public & Admin Page Routers (HTML templates)
app.include_router(pages.router)
app.include_router(admin_pages.router)

# Include REST API Routers under /api/v1
app.include_router(auth.router, prefix="/api/v1")
app.include_router(articles.router, prefix="/api/v1")
app.include_router(faqs.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")
app.include_router(surveys.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(videos.router, prefix="/api/v1")
app.include_router(calculator.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
