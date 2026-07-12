# Blog API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139.0-009688)
![License](https://img.shields.io/badge/license-MIT-green)

API profesional de blog construida con **FastAPI**, **SQLAlchemy 2.0** (asíncrono), **PostgreSQL**, **Docker** y **autenticación JWT**.

> **Estado:** Infraestructura principal lista – BD conectada, endpoint de salud funcionando.

## Funcionalidades (actuales y próximas)

- ⬜ Registro e inicio de sesión con JWT
- ⬜ Permisos basados en roles (admin, escritor, lector)
- ⬜ CRUD de publicaciones, categorías y etiquetas
- ⬜ Comentarios en publicaciones
- ⬜ Subida de archivos (imágenes para publicaciones)
- ⬜ Rate limiting
- ✅ Endpoint de salud con verificación de base de datos
- ✅ PostgreSQL asíncrono con SQLAlchemy 2.0
- ✅ Migraciones con Alembic
- ✅ Docker y Docker Compose para desarrollo

## Tecnologías

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Base de datos:** PostgreSQL 15 (local con Docker, producción con Supabase)
- **ORM:** SQLAlchemy 2.0 (async), Alembic
- **Autenticación:** JWT (passlib, bcrypt)
- **Testing:** Pytest, HTTPX (próximamente)
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD próximamente)

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

## Estructura del proyecto

```
blog-api/
├── app/
│   ├── api/v1/endpoints/   # Manejadores de rutas
│   ├── core/               # Configuración (Pydantic Settings)
│   ├── db/                 # Motor asíncrono, sesión
│   └── models/             # Modelos SQLAlchemy
├── tests/                  # Suite de tests
├── alembic/                # Migraciones de base de datos
├── docker-compose.yml
├── Dockerfile
└── README_ES.md
```

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.