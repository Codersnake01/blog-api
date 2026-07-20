# Blog API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139.0-009688)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/Codersnake01/blog-api/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Codersnake01/blog-api/branch/main/graph/badge.svg)](https://codecov.io/gh/Codersnake01/blog-api)

Professional blog API built with **FastAPI**, **SQLAlchemy 2.0** (async), **PostgreSQL**, **Docker**, and **JWT authentication**.

> **Status:** Production-ready – JWT with roles, full CRUD, image uploads, rate limiting, 86% test coverage.

## Features

- ✅ User registration and login with JWT
- ✅ Role-based permissions (admin, author, reader)
- ✅ Full CRUD for blog posts (soft delete, pagination, search)
- ✅ Categories and tags management
- ✅ Comments on posts
- ✅ Image upload for post covers (Cloudinary)
- ✅ Rate limiting on sensitive endpoints
- ✅ Health check endpoint with database verification
- ✅ Comprehensive test suite (86% coverage)
- ✅ CI/CD pipeline with GitHub Actions (lint, type check, tests, coverage)
- ✅ Deployed on Render with Supabase PostgreSQL
- ⬜ Advanced admin dashboard
- ⬜ Email notifications
- ⬜ Background tasks

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Database:** PostgreSQL 15 (local via Docker, production via Supabase)
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Authentication:** JWT (passlib, bcrypt)
- **Cloud Storage:** Cloudinary
- **Rate Limiting:** slowapi
- **Testing:** Pytest, HTTPX, coverage
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD)

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac)
- [Git](https://git-scm.com/)

### 1. Clone the repository
```bash
git clone https://github.com/Codersnake01/blog-api.git
cd blog-api
```

### 2. Configure environment variables
Copy the example file and adjust if needed:

```bash
cp .env.example .env
```
The default `.env` works out-of-the-box for local development with Docker.

### 3. Run with Docker
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8001`.

### 4. Apply database migrations (inside the container)
Open a second terminal while Docker is running:

```bash
docker-compose exec web alembic upgrade head
```

### 5. Verify the health endpoint
```bash
curl http://localhost:8001/api/v1/health
```
Expected response: `{"status":"ok","database":"connected"}`

## Running Tests
```bash
# Install dev dependencies
uv sync

# Run tests with coverage
uv run pytest --cov=app --cov-report=term-missing
```


## Code Quality & CI

- **Linting/Formatting:** Ruff
- **Static Typing:** MyPy
- **CI Pipeline:** GitHub Actions runs on every push:
  - `ruff check`
  - `mypy app`
  - `pytest` with coverage report
  - Coverage uploaded to Codecov (badge above)

## Deployment

The API is automatically deployed on [Render](https://render.com) whenever changes are pushed to `main`.  
The PostgreSQL database is hosted on [Supabase](https://supabase.com).  
A GitHub Actions **keep-alive** cron job pings the health endpoint every 6 hours to prevent cold starts on free tiers.

## Project Structure

```
blog-api/
├── app/
│   ├── api/
│   │   ├── deps.py                # Dependencies (get_current_user, etc.)
│   │   └── v1/
│   │       ├── endpoints/         # Route handlers (auth, posts, categories, tags, comments, health)
│   │       └── router.py
│   ├── core/
│   │   ├── config.py              # Pydantic Settings
│   │   ├── limiter.py             # Rate limiter configuration
│   │   ├── logger.py              # Structured logging
│   │   └── security.py            # JWT and password hashing
│   ├── db/
│   │   ├── base.py                # SQLAlchemy declarative base
│   │   └── session.py             # Async engine and session
│   ├── models/                    # SQLAlchemy models (User, Post, Category, Tag, Comment)
│   ├── schemas/                   # Pydantic schemas
│   ├── services/
│   │   └── cloudinary_service.py  # Image upload to Cloudinary
│   └── main.py
├── tests/                         # Test suite
├── alembic/                       # Database migrations
├── .github/workflows/             # CI/CD and keep-alive
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.