# Organization Management API

## Overview
This API provides functionality for managing organizations and their databases.

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Docker and Docker Compose

### Installation

#### Local Development
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # for development
   ```
4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

#### Docker Development
1. Clone the repository
2. Update env variables if required
3. Build and start the containers:
   ```bash
   # Build containers
   docker-compose build

   # Start services
   docker-compose up -d

   # View logs
   docker-compose logs -f

   # Stop services
   docker-compose down
   ```

4. Access the API at `http://localhost:8000`

### Docker Commands for Development

#### Running Commands Inside Containers
```bash
# Access the API container shell
docker exec -it org_mgmnt bash

# Access the database
docker exec -it org_postgres psql -U admin -d central_org

# Run migrations
docker exec -it org_mgmnt bash -c "alembic upgrade head"

# Create a new migration
docker exec -it org_mgmnt bash -c "alembic revision --autogenerate -m 'description'"
```

#### Database Operations
```bash
# Backup database
docker exec org_postgres pg_dump -U admin central_org > backup.sql

# Restore database
docker exec -i org_postgres psql -U admin central_org < backup.sql

# View database logs
docker-compose logs -f db
```

#### Development Workflow
1. Make code changes locally
2. Changes are automatically reflected in the container (via volume mount)
3. API server will auto-reload (uvicorn reload is enabled)
4. Run tests in container:
   ```bash
   docker exec -it org_mgmnt pytest
   ```

#### Rebuilding After Dependencies Change
```bash
# Rebuild containers after updating requirements.txt
docker-compose build --no-cache
docker-compose up -d
```

### Configuration (For venv dev)
1. Copy `.env.example` to `.env`
2. Update the environment variables in `.env`

Example `.env` file:
```env
# Database
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_password
POSTGRES_DB=central_org
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Super Admin
FIRST_SUPERADMIN_EMAIL=admin@example.com
FIRST_SUPERADMIN_PASSWORD=secure_password
```

### Running Tests
```bash
# Local
pytest

# In Docker
docker exec -it org_mgmnt pytest

# With coverage
docker exec -it org_mgmnt pytest --cov=app --cov-report=term-missing
```

## Development

### Code Style
This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

### Making Changes
1. Create a new branch
2. Make your changes
3. Run tests
4. Submit a pull request

## API Documentation

### Authentication
All protected endpoints require a JWT token in the Authorization header:
```bash
Authorization: Bearer <token>
```

### Endpoints

#### Create Organization (Super Admin Only)
```http
POST /org/create
Authorization: Bearer <super_admin_token>

{
    "organization_name": "string",
    "email": "string",
    "password": "string"
}
```

#### Get Organization
```http
GET /org/get?organization_name=string
```

#### Admin Login
```http
POST /admin/login

{
    "email": "string",
    "password": "string"
}
```

## Architecture

### Components
- FastAPI for API framework
- SQLAlchemy for ORM
- Alembic for migrations
- PostgreSQL for database
- JWT for authentication

### Project Structure
```
app/
├── core/          # Core functionality
│   ├── config.py  # Configuration management
│   ├── security.py # Security utilities
│   └── logging.py # Logging configuration
├── database/      # Database configuration
│   ├── base.py    # Base models
│   ├── session.py # Database session management
│   └── dao.py     # Data Access Objects
├── organization/  # Organization management
│   ├── models.py  # Organization models
│   ├── schemas.py # Pydantic schemas
│   ├── router.py  # API routes
│   ├── services.py # Business logic
│   └── dao.py     # Organization-specific database operations
└── auth/         # Authentication
    ├── models.py  # Auth models
    ├── schemas.py # Auth schemas
    ├── router.py  # Auth routes
    └── services.py # Auth services
```

### Database Migrations
```bash
# Create a new migration
docker exec -it org_mgmnt bash -c "alembic revision --autogenerate -m 'description'"

# Run migrations
docker exec -it org_mgmnt bash -c "alembic upgrade head"

# Rollback one migration
docker exec -it org_mgmnt bash -c "alembic downgrade -1"
```

### Troubleshooting

#### Common Issues
1. Database connection issues:
   ```bash
   # Check database status
   docker-compose ps
   # Check database logs
   docker-compose logs db
   ```

2. Migration issues:
   ```bash
   # Check current migration state
   docker exec -it org_mgmnt bash -c "alembic current"
   ```

3. Permission issues:
   ```bash
   # Reset database permissions
   docker exec -it org_postgres psql -U admin -d central_org -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;"
   ```