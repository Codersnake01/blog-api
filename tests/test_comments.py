import pytest
from sqlalchemy import select
from app.models.user import User


@pytest.mark.anyio
async def test_create_comment(client, test_db):
    # Crear usuario autor y otro usuario
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "commenter@test.com",
            "password": "secret123",
            "full_name": "Commenter",
        },
    )
    result = await test_db.execute(
        select(User).where(User.email == "commenter@test.com")
    )
    commenter = result.scalars().first()
    commenter.role = "author"
    await test_db.commit()

    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "commenter@test.com", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear categoría, tag y post necesarios
    # Para simplificar, promovamos al mismo usuario a admin para crear categorías/tags, luego lo dejamos como author.
    # Mejor: creamos un admin aparte para crear el post.
    # Vamos a reutilizar el mismo usuario dándole rol admin temporalmente, crear recursos, luego devolver a author.
    commenter.role = "admin"
    await test_db.commit()
    await client.post("/api/v1/categories/", json={"name": "Tech"}, headers=headers)
    await client.post("/api/v1/tags/", json={"name": "Python"}, headers=headers)
    # Crear post como admin
    post_resp = await client.post(
        "/api/v1/posts/",
        data={"title": "Post for comments", "content": "Content"},
        headers=headers,
    )
    assert post_resp.status_code == 201
    post_id = post_resp.json()["id"]
    # Devolver rol a author
    commenter.role = "author"
    await test_db.commit()

    # Crear comentario
    resp = await client.post(
        f"/api/v1/comments/posts/{post_id}/comments",
        json={"content": "Great post!"},
        headers=headers,
    )
    assert resp.status_code == 201
    comment = resp.json()
    assert comment["content"] == "Great post!"
    assert comment["author"]["id"] == commenter.id
    comment_id = comment["id"]

    # Intentar eliminar comentario con otro usuario (sin permisos)
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "other@test.com",
            "password": "secret123",
            "full_name": "Other",
        },
    )
    other_login = await client.post(
        "/api/v1/auth/login",
        data={"username": "other@test.com", "password": "secret123"},
    )
    other_token = other_login.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    del_resp = await client.delete(
        f"/api/v1/comments/comments/{comment_id}", headers=other_headers
    )
    assert del_resp.status_code == 403  # No es autor ni admin

    # El autor sí puede eliminar
    del_resp2 = await client.delete(
        f"/api/v1/comments/comments/{comment_id}", headers=headers
    )
    assert del_resp2.status_code == 204