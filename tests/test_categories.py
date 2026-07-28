import pytest
from sqlalchemy import select

from app.models.user import User


@pytest.mark.anyio
async def test_list_categories(client, test_db):
    # Registrar admin y obtener token
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@test.com",
            "password": "secret123",
            "full_name": "Admin",
        },
    )
    result = await test_db.execute(select(User).where(User.email == "admin@test.com"))
    admin = result.scalars().first()
    admin.role = "admin"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear una categoría para listar
    await client.post("/api/v1/categories/", json={"name": "TestCat"}, headers=headers)

    # Listar categorías como cualquier usuario autenticado
    response = await client.get("/api/v1/categories/", headers=headers)
    assert response.status_code == 200
    cats = response.json()
    assert len(cats) >= 1
    assert cats[0]["name"] == "TestCat"


@pytest.mark.anyio
async def test_create_category_admin_only(client, test_db):
    # Preparar admin
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "catadmin@test.com",
            "password": "secret123",
            "full_name": "CatAdmin",
        },
    )
    result = await test_db.execute(
        select(User).where(User.email == "catadmin@test.com")
    )
    admin = result.scalars().first()
    admin.role = "admin"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "catadmin@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Admin crea categoría
    response = await client.post(
        "/api/v1/categories/", json={"name": "AdminOnly"}, headers=headers
    )
    assert response.status_code == 201

    # Usuario no admin no puede crear categoría
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "reader@test.com",
            "password": "secret123",
            "full_name": "Reader",
        },
    )
    reader_login = await client.post(
        "/api/v1/auth/login",
        data={"username": "reader@test.com", "password": "secret123"},
    )
    reader_token = reader_login.json()["access_token"]
    reader_headers = {"Authorization": f"Bearer {reader_token}"}

    resp = await client.post(
        "/api/v1/categories/", json={"name": "Fail"}, headers=reader_headers
    )
    assert resp.status_code == 403
