from io import BytesIO

import pytest
from sqlalchemy import select

from app.models.user import User


@pytest.mark.anyio
async def test_create_post_with_image(client, test_db, mock_cloudinary):
    # Registrar usuario
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "author@test.com",
            "password": "secret123",
            "full_name": "Author",
        },
    )
    # Convertirlo en autor (cambio directo en la BD de prueba)
    result = await test_db.execute(select(User).where(User.email == "author@test.com"))
    user = result.scalars().first()
    user.role = "author"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "author@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear categoría y tag necesarios
    await client.post("/api/v1/categories/", json={"name": "Tech"}, headers=headers)
    await client.post("/api/v1/tags/", json={"name": "Python"}, headers=headers)

    # Crear post con imagen simulada
    image = BytesIO(b"fake image data")
    files = {"cover_image_file": ("test.jpg", image, "image/jpeg")}
    data = {
        "title": "Post with image",
        "content": "Test content",
        "is_published": "true",
        "category_id": "1",
        "tag_ids": "1",
    }
    response = await client.post(
        "/api/v1/posts/", data=data, files=files, headers=headers
    )
    assert response.status_code == 201
    post = response.json()
    assert post["cover_image"] == "http://fake.cloud/url.jpg"
    assert post["title"] == "Post with image"


@pytest.mark.anyio
async def test_reader_cannot_create_post(client):
    # Registro normal → rol reader
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "reader@test.com",
            "password": "secret123",
            "full_name": "Reader",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "reader@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {"title": "Should fail", "content": "fail"}
    response = await client.post("/api/v1/posts/", data=data, headers=headers)
    assert response.status_code == 403


@pytest.mark.anyio
async def test_soft_delete_post(client, test_db):
    # Registrar y promocionar a autor
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "softdelete@test.com",
            "password": "secret123",
            "full_name": "Deleter",
        },
    )
    result = await test_db.execute(
        select(User).where(User.email == "softdelete@test.com")
    )
    user = result.scalars().first()
    user.role = "author"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "softdelete@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear post
    data = {"title": "To be deleted", "content": "Will disappear"}
    response = await client.post("/api/v1/posts/", data=data, headers=headers)
    assert response.status_code == 201
    post_id = response.json()["id"]

    # Soft delete
    del_resp = await client.delete(f"/api/v1/posts/{post_id}", headers=headers)
    assert del_resp.status_code == 204

    # Verificar que no aparece en listado
    list_resp = await client.get("/api/v1/posts/", headers=headers)
    assert list_resp.status_code == 200
    posts = list_resp.json()
    assert not any(p["id"] == post_id for p in posts)

    # Verificar que GET directo da 404
    get_resp = await client.get(f"/api/v1/posts/{post_id}", headers=headers)
    assert get_resp.status_code == 404
