# Blog API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139.0-009688)
![License](https://img.shields.io/badge/license-MIT-green)

Professional blog API built with **FastAPI**, **SQLAlchemy 2.0** (async), **PostgreSQL**, **Docker**, and **JWT authentication**.

> **Status:** Core infrastructure ready – DB connected, health endpoint working.

## Features (Current & Upcoming)

- ⬜ User registration and login with JWT
- ⬜ Role-based permissions (admin, writer, reader)
- ⬜ CRUD for blog posts, categories, tags
- ⬜ Comments on posts
- ⬜ File uploads (images for posts)
- ⬜ Rate limiting
- ✅ Health check endpoint with database verification
- ✅ PostgreSQL async with SQLAlchemy 2.0
- ✅ Alembic migrations
- ✅ Docker & Docker Compose for development

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Database:** PostgreSQL 15 (local via Docker, production via Supabase)
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Authentication:** JWT (passlib, bcrypt)
- **Testing:** Pytest, HTTPX (coming)
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD coming)

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
The default .env works out-of-the-box for local development with Docker.

### 3. Run with Docker
```bash
docker-compose up --build
The API will be available at http://localhost:8001.
```

### 4. Apply database migrations (inside the container)
Open a second terminal while Docker is running:

```bash
docker-compose exec web alembic upgrade head
```

### 5. Verify the health endpoint
```bash
curl http://localhost:8001/api/v1/health
```
Expected response: {"status":"ok","database":"connected"}

### 6. Project Structure

blog-api/
├── app/
│   ├── api/v1/endpoints/   # Route handlers
│   ├── core/               # Configuration (Pydantic Settings)
│   ├── db/                 # Async engine, session
│   └── models/             # SQLAlchemy models
├── tests/                  # Test suite
├── alembic/                # Database migrations
├── docker-compose.yml
├── Dockerfile
└── README.md

License

This project is licensed under the MIT License. See LICENSE file for details.