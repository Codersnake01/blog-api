# Blog API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139.0-009688)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/Codersnake01/blog-api/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Codersnake01/blog-api/branch/main/graph/badge.svg)](https://codecov.io/gh/Codersnake01/blog-api)
> **Demo en vivo (Swagger):** [https://blog-api-q3s5.onrender.com/docs](https://blog-api-q3s5.onrender.com/docs)  
> **Colección de Postman:** [Descargar](https://github.com/Codersnake01/blog-api/blob/main/Blog_API.postman_collection.json)

API profesional de blog construida con **FastAPI**, **SQLAlchemy 2.0** (asíncrono), **PostgreSQL**, **Docker** y **autenticación JWT**.

> **Estado:** Lista para producción – JWT con roles, CRUD completo, subida de imágenes, rate limiting, 86 % de cobertura de tests.

## Funcionalidades

- ✅ Registro e inicio de sesión con JWT
- ✅ Permisos basados en roles (admin, autor, lector)
- ✅ CRUD completo de publicaciones (borrado lógico, paginación, búsqueda)
- ✅ Gestión de categorías y etiquetas
- ✅ Comentarios en publicaciones
- ✅ Subida de imágenes para portadas (Cloudinary)
- ✅ Rate limiting en endpoints sensibles
- ✅ Endpoint de salud con verificación de base de datos
- ✅ Suite de tests completa (86 % de cobertura)
- ✅ Pipeline CI/CD con GitHub Actions (lint, verificación de tipos, tests, cobertura)
- ✅ Desplegada en Render con PostgreSQL en Supabase
- ⬜ Panel de administración avanzado
- ⬜ Notificaciones por correo electrónico
- ⬜ Tareas en segundo plano

## Tecnologías

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Base de datos:** PostgreSQL 15 (local con Docker, producción con Supabase)
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Autenticación:** JWT (passlib, bcrypt)
- **Almacenamiento en la nube:** Cloudinary
- **Rate Limiting:** slowapi
- **Testing:** Pytest, HTTPX, coverage
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD)

## Primeros pasos

### Requisitos previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac)
- [Git](https://git-scm.com/)

### 1. Clonar el repositorio
```bash
git clone https://github.com/Codersnake01/blog-api.git
cd blog-api
```

### 2. Configurar variables de entorno
Copia el archivo de ejemplo y ajústalo si es necesario:

```bash
cp .env.example .env
```
El archivo `.env` por defecto funciona para desarrollo local con Docker.

### 3. Ejecutar con Docker
```bash
docker-compose up --build
```
La API estará disponible en `http://localhost:8001`.

### 4. Aplicar migraciones de la base de datos (dentro del contenedor)
Abre una segunda terminal mientras Docker está corriendo:

```bash
docker-compose exec web alembic upgrade head
```

### 5. Verificar el endpoint de salud
```bash
curl http://localhost:8001/api/v1/health
```
Respuesta esperada: `{"status":"ok","database":"connected"}`

## Ejecutar tests
```bash
# Instalar dependencias de desarrollo
uv sync

# Ejecutar tests con cobertura
uv run pytest --cov=app --cov-report=term-missing
```

## Calidad de código e CI

- **Linting/Formateo:** Ruff
- **Tipado estático:** MyPy
- **Pipeline CI:** GitHub Actions se ejecuta en cada push:
  - `ruff check`
  - `mypy app`
  - `pytest` con informe de cobertura
  - Cobertura subida a Codecov (badge arriba)

## Despliegue

La API se despliega automáticamente en [Render](https://render.com) con cada push a `main`.  
La base de datos PostgreSQL está alojada en [Supabase](https://supabase.com).  
Un **keep-alive** de GitHub Actions hace ping al endpoint de salud cada 6 horas para evitar tiempos de arranque en los planes gratuitos.

## Estructura del proyecto

```
blog-api/
├── app/
│   ├── api/
│   │   ├── deps.py                # Dependencias (get_current_user, etc.)
│   │   └── v1/
│   │       ├── endpoints/         # Manejadores de rutas (auth, posts, categories, tags, comments, health)
│   │       └── router.py
│   ├── core/
│   │   ├── config.py              # Configuración (Pydantic Settings)
│   │   ├── limiter.py             # Configuración del rate limiter
│   │   ├── logger.py              # Logging estructurado
│   │   └── security.py            # JWT y hashing de contraseñas
│   ├── db/
│   │   ├── base.py                # Base declarativa de SQLAlchemy
│   │   └── session.py             # Motor asíncrono y sesión
│   ├── models/                    # Modelos SQLAlchemy (User, Post, Category, Tag, Comment)
│   ├── schemas/                   # Esquemas Pydantic
│   ├── services/
│   │   └── cloudinary_service.py  # Subida de imágenes a Cloudinary
│   └── main.py
├── tests/                         # Suite de tests
├── alembic/                       # Migraciones de base de datos
├── .github/workflows/             # CI/CD y keep-alive
├── docker-compose.yml
├── Dockerfile
└── README_ES.md
```

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.