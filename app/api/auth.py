from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.users import UserCreate, UserResponse, UserLogin, Token
from app.services.auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from app.db.models.users import UserModel
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

# @router.get("/oauth/google")
# def oauth_google_login():
#     """Basic OAuth placeholder - redirect to Google OAuth"""
#     # This is a placeholder for OAuth implementation
#     # In a real implementation, you'd redirect to Google's OAuth URL
#     return {"message": "OAuth login not implemented yet", "url": "https://accounts.google.com/oauth/authorize?..."}

# @router.get("/oauth/callback")
# def oauth_callback(code: str):
#     """OAuth callback endpoint"""
#     # Placeholder for handling OAuth callback
#     return {"message": "OAuth callback received", "code": code}