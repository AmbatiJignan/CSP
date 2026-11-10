import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings

logger = logging.getLogger("greengrow.database")

# Initialize SQLAlchemy Engine with production-ready connection pool
engine = create_engine(
    settings.sqlalchemy_database_url,
    pool_size=10,
    max_overflow=5,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False,
    **settings.engine_kwargs,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a database session.
    Rolls back automatically on unhandled exception and closes session cleanly.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Database session exception encountered: {e}")
        raise
    finally:
        db.close()


def check_db_health() -> dict:
    """
    Health check query against Oracle Database 23ai:
    Executes SELECT 1 FROM DUAL.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM DUAL")).scalar()
            return {
                "status": "healthy" if result == 1 else "unhealthy",
                "database": "Oracle Database 23ai",
                "service": settings.ORACLE_SERVICE_NAME,
                "host": settings.ORACLE_HOST,
                "port": settings.ORACLE_PORT,
                "test_query_result": result,
            }
    except SQLAlchemyError as exc:
        logger.error(f"Oracle Database health check failed: {exc}")
        return {
            "status": "unhealthy",
            "database": "Oracle Database 23ai",
            "service": settings.ORACLE_SERVICE_NAME,
            "error": str(exc),
        }