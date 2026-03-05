from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db.session import get_db
from app.schemas.users import UserResponse
from app.services.auth import get_current_user
from app.db.models.users import UserModel, UserRole
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["User Management"])
limiter = Limiter(key_func=get_remote_address)

# Helper function to check if user is admin
def is_admin(user: UserModel) -> bool:
    return user.role == UserRole.ADMIN

@router.get("/", response_model=List[UserResponse])
@limiter.limit("20/minute")
def get_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Only admins can list all users"""
    if not is_admin(current_user):
        logger.error(f"User {current_user.user_id} attempted to list users without permission")
        raise HTTPException(status_code=403, detail="Admin access required")

    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("20/minute")
def get_user(
    request: Request,
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Only admins can view other users' details"""
    if not is_admin(current_user):
        logger.error(f"User {current_user.user_id} attempted to access user {user_id} details without permission")
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user