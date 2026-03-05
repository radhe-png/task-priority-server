from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.api.health import router as status_router
from app.api.validate import router as validate_router
from app.api.prioritize import router as prioritize_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.tasks import router as tasks_router
from app.db.base import Base
from app.db.session import engine
from app.db.models import users, task
from app.core.config import settings
from app.core.middleware import LoggingMiddleware, SecurityHeadersMiddleware

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

# Rate limiting
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Include routers
app.include_router(status_router)  # Health check - no auth
app.include_router(auth_router)    # Auth endpoints - no auth
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(validate_router)
app.include_router(prioritize_router)

# Create tables
Base.metadata.create_all(bind=engine)