import pytest
from sqlalchemy import select

from app.models.user import User


@pytest.mark.anyio
async def test_list_tags(client, test_db):
    # Preparar admin y token
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "tagadmin@test.com",
            "password": "secret123",
            "full_name": "TagAdmin",
        },
    )
    result = await test_db.execute(
        select(User).where(User.email == "tagadmin@test.com")
    )
    admin = result.scalars().first()
    admin.role = "admin"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "tagadmin@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear un tag
    await client.post("/api/v1/tags/", json={"name": "Tag1"}, headers=headers)

    # Listar tags
    response = await client.get("/api/v1/tags/", headers=headers)
    assert response.status_code == 200
    tags = response.json()
    assert len(tags) >= 1
    assert tags[0]["name"] == "Tag1"


@pytest.mark.anyio
async def test_create_tag_admin_only(client, test_db):
    # Admin setup
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "tagadmin2@test.com",
            "password": "secret123",
            "full_name": "TagAdmin2",
        },
    )
    result = await test_db.execute(
        select(User).where(User.email == "tagadmin2@test.com")
    )
    admin = result.scalars().first()
    admin.role = "admin"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "tagadmin2@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.post(
        "/api/v1/tags/", json={"name": "AdminTag"}, headers=headers
    )
    assert resp.status_code == 201

    # Reader
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "tagreader@test.com",
            "password": "secret123",
            "full_name": "TagReader",
        },
    )
    reader_login = await client.post(
        "/api/v1/auth/login",
        data={"username": "tagreader@test.com", "password": "secret123"},
    )
    reader_token = reader_login.json()["access_token"]
    reader_headers = {"Authorization": f"Bearer {reader_token}"}

    resp = await client.post(
        "/api/v1/tags/", json={"name": "Fail"}, headers=reader_headers
    )
    assert resp.status_code == 403
