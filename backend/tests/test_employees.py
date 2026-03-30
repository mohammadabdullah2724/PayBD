import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_list_employees_route(monkeypatch):
    async def fake_get_db_dependency():
        yield None

    async def fake_list_employees(session):
        return []

    monkeypatch.setattr("app.api.v1.employees.get_db_dependency", fake_get_db_dependency)
    monkeypatch.setattr("app.api.v1.employees.list_employees", fake_list_employees)

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/api/v1/employees")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_employee_route(monkeypatch):
    async def fake_get_db_dependency():
        yield None

    async def fake_get_employee_by_employee_id(session, employee_id):
        return None

    async def fake_create_employee(session, payload):
        class EmployeeObject:
            def __init__(self, **values):
                for key, value in values.items():
                    setattr(self, key, value)

        return EmployeeObject(
            id="00000000-0000-0000-0000-000000000000",
            created_at="2026-01-01T00:00:00Z",
            updated_at=None,
            **payload.model_dump(),
        )

    monkeypatch.setattr("app.api.v1.employees.get_db_dependency", fake_get_db_dependency)
    monkeypatch.setattr("app.api.v1.employees.get_employee_by_employee_id", fake_get_employee_by_employee_id)
    monkeypatch.setattr("app.api.v1.employees.create_employee", fake_create_employee)

    payload = {
        "employee_id": "EMP001",
        "full_name": "Test User",
        "email": "test@example.com",
    }

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/v1/employees", json=payload)

    assert response.status_code == 201
    assert response.json()["employee_id"] == "EMP001"
    assert response.json()["email"] == "test@example.com"
