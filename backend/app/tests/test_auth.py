import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_email() -> str:
    return f"test-{uuid.uuid4()}@example.com"


def test_register_user():
    email = unique_email()

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "specialty": "backend",
            "level": "junior",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["specialty"] == "backend"
    assert data["level"] == "junior"
    assert data["is_active"] is True
    assert "password" not in data
    assert "password_hash" not in data


def test_login_user():
    email = unique_email()

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "specialty": "backend",
            "level": "junior",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "secret123",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
    email = unique_email()

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "specialty": "backend",
            "level": "junior",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "secret123",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email
    assert data["specialty"] == "backend"
    assert data["level"] == "junior"


def test_invalid_password_fails():
    email = unique_email()

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "specialty": "backend",
            "level": "junior",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "wrongpassword",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"