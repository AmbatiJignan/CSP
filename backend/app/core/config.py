import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from sqlalchemy.engine import URL


# Resolve workspace root and backend paths
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
WORKSPACE_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    # Application Configuration
    APP_NAME: str = "GreenGrow"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Oracle Database 23ai Configuration
    ORACLE_USER: str = Field(default="greengrow")
    ORACLE_PASSWORD: str = Field(default="greengrow")
    ORACLE_HOST: str = Field(default="localhost")
    ORACLE_PORT: int = Field(default=1521)
    ORACLE_SERVICE_NAME: str = Field(default="FREEPDB1")
    # Optional full connect string (for cloud DBs such as Oracle Autonomous, TLS).
    # When set, it is used instead of host/port/service name.
    ORACLE_DSN: Optional[str] = Field(default=None)

    # Security & JWT
    SECRET_KEY: str = Field(default="greengrow-organic-portal-super-secret-key-2026-production-ready")
    JWT_SECRET_KEY: str = Field(default="greengrow-jwt-token-signing-secret-key-2026-secure-vault")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Uploads
    UPLOAD_DIR: str = Field(default=str(WORKSPACE_ROOT / "uploads"))
    MAX_UPLOAD_SIZE_MB: int = 15

    # Static & Templates
    TEMPLATES_DIR: str = str(BACKEND_DIR / "app" / "templates")
    STATIC_DIR: str = str(BACKEND_DIR / "app" / "static")

    @property
    def sqlalchemy_database_url(self) -> URL:
        """
        Builds a safe, escaped SQLAlchemy URL using URL.create
        for python-oracledb Thin mode.
        """
        return URL.create(
            drivername="oracle+oracledb",
            username=self.ORACLE_USER,
            password=self.ORACLE_PASSWORD,
            host=self.ORACLE_HOST,
            port=self.ORACLE_PORT,
            query={"service_name": self.ORACLE_SERVICE_NAME},
        )

    @property
    def engine_kwargs(self) -> dict:
        """Extra create_engine() arguments. Uses ORACLE_DSN when provided."""
        if not self.ORACLE_DSN:
            return {}
        import oracledb

        def _connect():
            return oracledb.connect(
                user=self.ORACLE_USER,
                password=self.ORACLE_PASSWORD,
                dsn=self.ORACLE_DSN,
            )

        return {"creator": _connect}

    model_config = SettingsConfigDict(
        env_file=[
            str(WORKSPACE_ROOT / ".env"),
            str(BACKEND_DIR / ".env"),
            ".env",
        ],
        extra="ignore",
    )


settings = Settings()

# Ensure upload subdirectories exist
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.UPLOAD_DIR, "resources").mkdir(parents=True, exist_ok=True)
Path(settings.UPLOAD_DIR, "articles").mkdir(parents=True, exist_ok=True)