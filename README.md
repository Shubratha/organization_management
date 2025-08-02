# Organization Management Service

A microservice for managing multi-tenant organizations with dynamic database creation.

## Features

- **Organization Management**
  - Create organizations with isolated databases
  - Manage organization admins
  - Dynamic database provisioning

- **Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Super Admin, Org Admin)
  - Secure password hashing

- **API Features**
  - RESTful endpoints
  - Async operations
  - Input validation
  - Error handling

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy
- **Authentication**: JWT
- **Container**: Docker
- **Testing**: Pytest
- **Documentation**: OpenAPI/Swagger

## Quick Start

```bash
# Clone the repository
git clone <repository-url>

# Set up environment
cp .env.example .env

# Start services
docker-compose up -d

# Run migrations
docker exec -it org_mgmnt bash -c "alembic upgrade head"

# Create first super admin
docker exec -it org_postgres psql -U admin -d central_org -c "INSERT INTO super_admins (email, password, is_active) VALUES ('admin@example.com', 'hashed_password', true);"
```

## API Overview

### Core Endpoints

```bash
POST /org/create      # Create new organization (Super Admin only)
GET  /org/get        # Get organization details
POST /admin/login    # Organization admin login
POST /auth/login     # Super admin login
```

## Development

See [Development Guide](docs/README.md) for detailed setup and contribution guidelines.

## Project Structure

```
├── app/                  # Application code
│   ├── core/            # Core functionality
│   ├── database/        # Database configuration
│   ├── organization/    # Organization management
│   └── auth/           # Authentication
├── tests/               # Test suite
├── docs/               # Detailed documentation
├── docker-compose.yml  # Docker configuration
└── requirements.txt    # Python dependencies
```

## Testing

```bash
# Run tests
docker exec -it org_mgmnt pytest

# With coverage
docker exec -it org_mgmnt pytest --cov=app
```

## Documentation

- [Detailed Documentation](docs/README.md)
- API Documentation: http://localhost:8000/docs (when running)
- [Development Guide](docs/README.md#development)
- [Docker Guide](docs/README.md#docker-development)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[MIT License](LICENSE)