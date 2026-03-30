import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_register_route(monkeypatch):
    async def fake_get_db_dependency():
        yield None

    async def fake_get_user_by_email(session, email):
        return None

    async def fake_create_user(session, payload):
        class UserObj:
            email = payload.email
            is_active = True

        return UserObj()

    monkeypatch.setattr("app.api.v1.auth.get_db_dependency", fake_get_db_dependency)
    monkeypatch.setattr("app.api.v1.auth.get_user_by_email", fake_get_user_by_email)
    monkeypatch.setattr("app.api.v1.auth.create_user", fake_create_user)

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "securepass"},
        )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login_route(monkeypatch):
    async def fake_get_db_dependency():
        yield None

    async def fake_authenticate_user(session, email, password):
        class UserObj:
            id = "00000000-0000-0000-0000-000000000000"

        return UserObj()

    async def fake_create_tokens_for_user(user):
        return {"access_token": "access.token", "refresh_token": "refresh.token"}

    monkeypatch.setattr("app.api.v1.auth.get_db_dependency", fake_get_db_dependency)
    monkeypatch.setattr("app.api.v1.auth.authenticate_user", fake_authenticate_user)
    monkeypatch.setattr("app.api.v1.auth.create_tokens_for_user", fake_create_tokens_for_user)

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "securepass"},
        )

    assert response.status_code == 200
    assert response.json()["access_token"] == "access.token"
    assert response.json()["refresh_token"] == "refresh.token"
