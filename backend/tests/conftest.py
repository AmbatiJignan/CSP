import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.database.connection import SessionLocal
from app.core.security import create_access_token


@pytest.fixture(scope="function")
def client():
    """Provides a fresh TestClient for each test function."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def db_session():
    """Yields a database session connected directly to Oracle Database 23ai."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def admin_headers():
    """Provides Authorization headers for an authenticated superadmin."""
    token = create_access_token({
        "sub": "admin",
        "user_id": 1,
        "role": "superadmin",
        "email": "admin@greengrow.org",
    })
    return {"Authorization": f"Bearer {token}"}
