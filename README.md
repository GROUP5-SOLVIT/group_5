# Board's Cafe Management System - Backend

A Django REST Framework backend for the Board's Cafe Management System - an internal web-based cafe management and Point of Sale (POS) system.

## Overview

This backend provides a comprehensive API for managing cafe operations including:
- **Authentication & Authorization** - JWT-based auth with role-based access control (RBAC)
- **User Management** - Staff accounts, roles, and permissions
- **Menu Management** - Categories, products, and recipes
- **Inventory Management** - Items, batches, stock movements, and FEFO consumption
- **Sales & POS** - Orders, payments, and order processing
- **Purchasing** - Suppliers, purchases, and stock receiving
- **Finance** - Expenses and payments
- **Waste Management** - Waste recording and tracking
- **Reports & Dashboard** - Analytics and business insights
- **Notifications** - Alerts for low stock, expiring items, etc.
- **Audit Logging** - Comprehensive audit trail

## Architecture

```
Backend/
├── BoardsCafe/              # Django project configuration
│   ├── settings.py          # Main settings (environment-based)
│   ├── urls.py              # Root URL configuration
│   ├── core/                # Shared foundation components
│   │   ├── pagination.py    # Standard API pagination
│   │   ├── exceptions.py    # Global exception handling
│   │   ├── responses.py     # Standard response formats
│   │   ├── permissions.py   # Custom permissions
│   │   ├── throttling.py    # Rate limiting
│   │   ├── email.py         # Email utilities
│   │   └── views.py         # Health check endpoint
│   └── apps/                # Django applications
│       ├── users/           # Authentication & user management
│       ├── roles/           # Role & permission management
│       ├── otp/             # OTP infrastructure
│       ├── dashboard/       # Dashboard summaries
│       ├── menu/            # Menu products & categories
│       ├── recipes/         # Recipe management
│       ├── inventory/       # Inventory, batches, stock
│       ├── sales/           # POS orders & payments
│       ├── purchasing/      # Suppliers & purchases
│       ├── finance/         # Expenses & payments
│       ├── waste/           # Waste management
│       ├── reports/         # Reports & analytics
│       ├── notifications/   # Notifications & alerts
│       └── audit_logs/      # Audit logging
├── docs/                    # Project documentation
├── manage.py
└── requirements.txt
```

## Technology Stack

- **Framework**: Django 6.1.1 + Django REST Framework 3.18.1
- **Database**: PostgreSQL (psycopg3)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-spectacular (OpenAPI 3 / Swagger UI / ReDoc)
- **CORS**: django-cors-headers
- **Environment**: python-dotenv

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip / virtualenv

## Quick Start

### 1. Clone and Setup

```bash
cd Board-s-Cafe-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:

```env
# Django Security
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DATABASE_NAME=Board-s-Cafe-backend
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email (Development uses console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True

# OTP Configuration
OTP_LENGTH=6
OTP_EXPIRY_MINUTES=10
OTP_MAX_ATTEMPTS=3
OTP_RESEND_COOLDOWN_SECONDS=60

# JWT Configuration
JWT_ACCESS_TOKEN_MINUTES=15
JWT_REFRESH_TOKEN_DAYS=7
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb Board-s-Cafe-backend

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Server starts at: http://localhost:8000

## API Endpoints

All API endpoints are versioned under `/api/v1/`:

| Area | Base Path |
|------|-----------|
| Authentication | `/api/v1/auth/` |
| OTP | `/api/v1/auth/otp/` |
| Health Check | `/api/v1/health/` |
| API Schema | `/api/v1/schema/` |
| Swagger UI | `/api/v1/docs/` |
| ReDoc | `/api/v1/redoc/` |

### Authentication Endpoints

```
POST   /api/v1/auth/register/     - Register new user
POST   /api/v1/auth/login/        - Login (returns access + refresh tokens)
POST   /api/v1/auth/token/refresh/ - Refresh access token
GET    /api/v1/auth/me/           - Get current user profile
```

### OTP Endpoints

```
POST   /api/v1/auth/otp/request/  - Request OTP
POST   /api/v1/auth/otp/verify/   - Verify OTP
```

### Inventory Foundation

Inventory API routes are under `/api/v1/inventory/`. All routes require JWT authentication and the matching inventory role permission: reads require `inventory.view`, creates require `inventory.create`, and updates require `inventory.update`. No inventory access is granted by default; these permission codenames must be present in the existing role permission catalog and assigned to roles by an administrator.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET, POST | `/categories/` | List and create inventory categories |
| GET, PUT, PATCH | `/categories/{id}/` | Retrieve or update category details |
| GET, POST | `/units/` | List and create units of measure |
| GET, PUT, PATCH | `/units/{id}/` | Retrieve or update a unit |
| GET, POST | `/items/` | List and create items; filter with `category` and `is_active` |
| GET, PUT, PATCH | `/items/{id}/` | Retrieve or update item details |
| GET | `/stock-balances/` | List current balances; optionally filter with `item` |
| GET | `/stock-balances/{id}/` | Retrieve a current balance |

Category names and unit names/symbols are unique without regard to case. Item SKUs are optional and unique without regard to case. Items require a category and base unit; minimum stock and balance quantities use three decimal places and cannot be negative. Category and unit references are protected from deletion while in use. A new item receives a zero stock balance automatically. At this stage balances are read-only through the API; there is no stock movement ledger, so balances are not an auditable history and cannot yet be adjusted through an inventory workflow.

Apply the inventory migration with `python manage.py migrate` and run its tests with `python manage.py test BoardsCafe.apps.inventory.tests`.

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs/
- **ReDoc**: http://localhost:8000/api/v1/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/v1/schema/

The Swagger UI includes JWT authentication - click "Authorize" and enter your Bearer token to test protected endpoints.

## Standard API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

### List Response (with pagination)
```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Something went wrong.",
  "errors": {}
}
```

### Validation Error
```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

## Authentication

### JWT Tokens

The API uses JWT (JSON Web Tokens) for authentication:

- **Access Token**: Short-lived (default 15 minutes)
- **Refresh Token**: Long-lived (default 7 days), rotates on use

Include the access token in requests:
```
Authorization: Bearer <access_token>
```

### Role-Based Access Control (RBAC)

The system implements RBAC with the following roles:

| Role | Description |
|------|-------------|
| Administrator | Full system access, user/role management |
| Manager | Operational oversight, reports, approvals |
| Cashier | Orders, payments, customer-facing |
| Waiter | Order creation, order status |
| Kitchen Staff | Order preparation, kitchen operations |
| Storekeeper | Inventory, stock receiving, batches |

Permissions follow the format: `module.action` (e.g., `inventory.view`, `orders.create`, `users.manage`).

## Pagination

List endpoints support pagination:

```
GET /api/v1/endpoint/?page=2&page_size=20
```

- Default page size: 20
- Maximum page size: 100

## Rate Limiting

API endpoints are protected with throttling:

| Scope | Limit |
|-------|-------|
| Anonymous | 100 requests/minute |
| Authenticated Users | 1000 requests/minute |
| Auth Endpoints | 20 requests/minute |
| OTP Endpoints | 5 requests/minute |

## Security Features

- **Password Security**: Django's secure password hashing + validators
- **JWT Security**: Short-lived access tokens, refresh token rotation + blacklisting
- **CORS**: Configured via environment variables (no wildcard origins)
- **Security Headers**: XSS protection, content-type sniffing, clickjacking protection
- **HTTPS Ready**: Secure cookies, HSTS in production
- **Input Validation**: DRF serializers + custom validation
- **SQL Injection Protection**: Django ORM parameterized queries
- **Audit Logging**: Security-sensitive actions logged separately
- **Environment Secrets**: No hardcoded secrets, all via `.env`

## OTP Infrastructure

Reusable OTP system supporting:
- Email verification
- Password reset
- Account verification
- Two-factor authentication

Features:
- Secure random generation (cryptographically secure)
- Configurable length, expiry, max attempts
- Hashed storage (SHA-256)
- Resend cooldown protection
- One-time use enforcement

## Email Infrastructure

- **Development**: Console backend (emails printed to terminal)
- **Production**: SMTP backend via environment variables
- Template-based emails supported

## Logging

Structured logging with separate channels:
- **Application logs**: `logs/django.log`
- **Security logs**: `logs/security.log`
- Console output in development

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test BoardsCafe.apps.users.tests
python manage.py test BoardsCafe.core.tests

# Run with coverage (if installed)
coverage run --source='.' manage.py test
coverage report
```

## Code Quality

```bash
# Check for issues
python manage.py check

# Check migrations
python manage.py makemigrations --check --dry-run
```

## Development Workflow

1. Create feature branch from `main`
2. Implement changes with tests
3. Run `python manage.py check` and `python manage.py test`
4. Create/update migrations if models changed
5. Update documentation if needed
6. Submit PR for review

## Project Documentation

Comprehensive documentation in `docs/`:

| Category | Documents |
|----------|-----------|
| Requirements | Project overview, business/functional requirements, roles & permissions |
| Business Processes | Workflows |
| Products & Inventory | Products, recipes, inventory, batch/expiry management |
| Sales Operations | POS & order management |
| Finance & Purchasing | Purchases, suppliers, expenses, payments, waste |
| Monitoring | Reports, notifications, audit logging |
| Database | Database design, ERD |
| Application Design | API documentation, UI/UX, technical architecture |
| Security | Security requirements |

## Deployment Notes

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS` with your domain
3. Use strong `SECRET_KEY`
4. Set up PostgreSQL with dedicated user
5. Configure SMTP email settings
6. Use reverse proxy (nginx) with SSL
7. Set up database backups
8. Configure log rotation
9. Run `python manage.py collectstatic`

## License

Internal project for Board's Cafe Management System.
