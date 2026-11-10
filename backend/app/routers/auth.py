from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import verify_password, hash_password, create_access_token
from app.core.dependencies import get_current_admin, require_superadmin
from app.models.user import AdminUser
from app.schemas.auth import (
    LoginRequest,
    Token,
    AdminUserResponse,
    AdminUserCreate,
    AdminUserUpdate,
    PasswordChangeRequest,
)
from app.services.audit_service import log_admin_action

router = APIRouter(prefix="/auth", tags=["Authentication & Admin Users"])


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """Authenticates an administrator and returns a JWT access token."""
    user = db.query(AdminUser).filter(AdminUser.username == login_data.username.strip()).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This administrator account has been disabled",
        )

    # Update last login timestamp
    user.last_login = datetime.now()
    db.commit()

    token_payload = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role,
        "email": user.email,
    }
    access_token = create_access_token(token_payload)

    # Set HTTP-only secure cookie for seamless Jinja2 dashboard browsing
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        max_age=86400,
    )

    client_ip = request.client.host if request.client else "unknown"
    log_admin_action(
        db=db,
        admin=user,
        action="LOGIN",
        target_entity="ADMIN_USERS",
        target_id=str(user.id),
        details=f"Admin {user.username} logged in successfully",
        ip_address=client_ip,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=86400,
        user_id=user.id,
        username=user.username,
        role=user.role,
        full_name=user.full_name,
    )


@router.post("/logout")
def logout(response: Response, current_admin: Optional[AdminUser] = Depends(get_current_admin)):
    """Clears access token cookie and ends session."""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=AdminUserResponse)
def get_current_admin_profile(current_admin: AdminUser = Depends(get_current_admin)):
    """Returns the authenticated admin's profile."""
    return current_admin


@router.post("/change-password")
def change_password(
    pwd_data: PasswordChangeRequest,
    current_admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Allows an administrator to change their own password."""
    if not verify_password(pwd_data.current_password, current_admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password verification failed",
        )
    current_admin.hashed_password = hash_password(pwd_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}


@router.get("/users", response_model=List[AdminUserResponse])
def list_admin_users(
    current_admin: AdminUser = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    """Lists all admin accounts (Superadmin only)."""
    return db.query(AdminUser).order_by(AdminUser.id).all()


@router.post("/users", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
def create_admin_user(
    user_in: AdminUserCreate,
    current_admin: AdminUser = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    """Creates a new admin account (Superadmin only)."""
    existing_user = db.query(AdminUser).filter(AdminUser.username == user_in.username.strip()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user_in.username}' already exists",
        )
    existing_email = db.query(AdminUser).filter(AdminUser.email == user_in.email.strip()).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_in.email}' already registered",
        )

    new_user = AdminUser(
        username=user_in.username.strip(),
        email=user_in.email.strip(),
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role.lower(),
        is_active=user_in.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="CREATE",
        target_entity="ADMIN_USERS",
        target_id=str(new_user.id),
        details=f"Created admin account {new_user.username} with role {new_user.role}",
    )
    return new_user


@router.put("/users/{user_id}", response_model=AdminUserResponse)
def update_admin_user(
    user_id: int,
    user_update: AdminUserUpdate,
    current_admin: AdminUser = Depends(require_superadmin),
    db: Session = Depends(get_db),
):
    """Updates an admin account (Superadmin only)."""
    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_update.email and user_update.email != user.email:
        dup = db.query(AdminUser).filter(AdminUser.email == user_update.email).first()
        if dup:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        user.email = user_update.email

    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.role is not None:
        user.role = user_update.role.lower()
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(user)

    log_admin_action(
        db=db,
        admin=current_admin,
        action="UPDATE",
        target_entity="ADMIN_USERS",
        target_id=str(user.id),
        details=f"Updated admin account {user.username}",
    )
    return user
