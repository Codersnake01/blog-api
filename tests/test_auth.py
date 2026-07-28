import pytest


@pytest.mark.anyio
async def test_register_success(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "secret123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_register_duplicate_email(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "secret123",
            "full_name": "First",
        },
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "other456",
            "full_name": "Second",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.anyio
async def test_login_success(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@test.com",
            "password": "secret123",
            "full_name": "Login Test",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "login@test.com", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.anyio
async def test_login_invalid_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid@test.com",
            "password": "correct",
            "full_name": "Invalid",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "invalid@test.com", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
