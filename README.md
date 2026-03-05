# Task Priority Server

A FastAPI-based REST API for intelligent task prioritization with user authentication, role-based access control, and comprehensive security features. The application uses machine learning algorithms to prioritize tasks based on urgency, importance, and deadlines.

## Features

### 🔐 Authentication & Authorization
- JWT-based authentication with secure token management
- Password hashing using bcrypt
- User registration and login endpoints
- Role-based access control (User/Admin roles)
- OAuth 2.0 integration placeholders (Google, etc.)

### 🛡️ Security Features
- CORS middleware for cross-origin requests
- Rate limiting (10 requests/minute for prioritize, 20/minute for validate)
- Security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- Request/response logging middleware
- Input validation and sanitization

### 📋 Task Management
- Task validation endpoint
- Intelligent task prioritization using ML algorithms
- Task data schemas with Pydantic validation

### 👥 User Management
- User registration and authentication
- User profile management
- Admin-only user listing and management

### 🏥 Health Monitoring
- Health check endpoint for monitoring

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Virtual environment (recommended)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd task-priority-server
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost/task_priority_db
   SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
   RATE_LIMIT_REQUESTS=100
   ```

5. **Set up the database:**
   The application uses SQLAlchemy with Alembic for migrations. Tables are created automatically on startup.

## Running the Application

1. **Activate virtual environment:**
   ```bash
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## Project Structure

```
task-priority-server/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API route handlers
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── tasks.py        # Task management endpoints
│   │   ├── users.py        # User management endpoints
│   │   ├── health.py       # Health check endpoint
│   │   ├── prioritize.py   # Task prioritization logic
│   │   └── validate.py     # Task validation logic
│   ├── core/               # Core functionality
│   │   ├── config.py       # Application configuration
│   │   ├── dependencies.py # Dependency injection
│   │   └── middleware.py   # Custom middleware
│   ├── db/                 # Database layer
│   │   ├── base.py         # Database base configuration
│   │   ├── session.py      # Database session management
│   │   └── models/         # SQLAlchemy models
│   │       ├── task.py     # Task model
│   │       └── users.py    # User model
│   ├── schemas/            # Pydantic schemas
│   │   ├── task.py         # Task schemas
│   │   ├── task_input.py   # Input validation schemas
│   │   ├── task_response.py # Response schemas
│   │   └── users.py        # User schemas
│   └── services/           # Business logic services
│       ├── auth.py         # Authentication service
│       └── prioritize_tasks.py # Task prioritization service
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `GET /auth/me` - Get current user information

### Tasks (Requires Authentication)
- `GET/POST/PUT/DELETE on /tasks` - CRUD on tasks

- `POST /tasks/validate` - Validate task data
- `POST /tasks/prioritize` - Prioritize tasks

### Users (Admin Only)
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get specific user details

### Health
- `GET /health` - Application health check (no authentication required)

## Configuration

The application uses the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | 30 |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | http://localhost:3000 |
| `RATE_LIMIT_REQUESTS` | Global rate limit per minute | 100 |

## Testing

Run the test suite:
```bash
pytest
```

## Future Enhancements

- Complete OAuth 2.0 integration (Google, GitHub, etc.)
- CSRF protection for web forms
- API versioning (v1, v2, etc.)
- More granular permission system
- Audit logging for security events
- Task categories and tags
- Priority history and analytics
- Email notifications
- Mobile app API support

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository or contact the development team.