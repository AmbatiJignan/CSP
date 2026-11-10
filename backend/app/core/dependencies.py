from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import decode_access_token
from app.models.user import AdminUser

security_bearer = HTTPBearer(auto_error=False)


def get_token_from_request(
    request: Request,
    bearer_creds: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)
) -> Optional[str]:
    """
    Extracts JWT token from Authorization Bearer header, or falls back to
    'access_token' cookie for browser Jinja2 template sessions.
    """
    if bearer_creds and bearer_creds.credentials:
        return bearer_creds.credentials
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        if cookie_token.startswith("Bearer "):
            return cookie_token.split(" ", 1)[1]
        return cookie_token
    return None


def get_current_admin(
    token: Optional[str] = Depends(get_token_from_request),
    db: Session = Depends(get_db)
) -> AdminUser:
    """
    Authenticates the current admin user from JWT token.
    Raises 401 if missing, expired, or invalid.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = payload["sub"]
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with this token no longer exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin user account has been disabled.",
        )
    return user


def get_optional_admin(
    token: Optional[str] = Depends(get_token_from_request),
    db: Session = Depends(get_db)
) -> Optional[AdminUser]:
    """
    Returns current admin user if valid token exists, otherwise returns None without throwing 401.
    Useful for server-rendered HTML pages where guest access is permitted.
    """
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        if not payload or "sub" not in payload:
            return None
        user = db.query(AdminUser).filter(AdminUser.username == payload["sub"]).first()
        if user and user.is_active:
            return user
    except Exception:
        return None
    return None


def require_superadmin(
    current_admin: AdminUser = Depends(get_current_admin)
) -> AdminUser:
    """Restricts access to superadmin accounts only."""
    if current_admin.role.lower() != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires superadmin privileges.",
        )
    return current_admin
