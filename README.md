# Task Priority Server

A FastAPI application for task prioritization with authentication, authorization, and security features.

### Installation command
- cd path to '/task-priority-server'
`pip install -r requirements.txt`

## Features Implemented

### Authentication & Authorization
- **JWT Authentication**: Secure token-based authentication using python-jose
- **Password Hashing**: Bcrypt hashing with passlib
- **User Registration & Login**: Endpoints for user management
- **Role-Based Access Control (RBAC)**: User roles (user, admin) with different permissions

### Security Features
- **CORS Middleware**: Configurable Cross-Origin Resource Sharing
- **Rate Limiting**: Request rate limiting using slowapi (10/minute for prioritize, 20/minute for validate)
- **Security Headers**: HTTP security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- **Logging Middleware**: Request/response logging

### API Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info
- `GET /auth/oauth/google` - OAuth login placeholder
- `GET /auth/oauth/callback` - OAuth callback placeholder

#### Tasks (Authenticated)
- `POST /tasks/validate` - Validate task data
- `POST /tasks/prioritize` - Prioritize tasks

#### Admin Only
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get specific user

#### Health
- `GET /health` - Health check (no auth required)

### Configuration
Environment variables in `.env`:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration
- `ALLOWED_ORIGINS`: CORS allowed origins
- `RATE_LIMIT_REQUESTS`: Global rate limit

### Running the Application
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migration
The application uses SQLAlchemy with PostgreSQL. Tables are created automatically on startup.

### Future Enhancements
- OAuth 2.0 integration (Google, etc.)
- CSRF protection for forms
- API versioning
- More granular permissions
- Audit logging