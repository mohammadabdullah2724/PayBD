from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


async def get_employee_by_id(session: AsyncSession, employee_id: UUID) -> Employee | None:
    """Return employee by primary key."""
    result = await session.execute(select(Employee).where(Employee.id == employee_id))
    return result.scalar_one_or_none()


async def get_employee_by_employee_id(session: AsyncSession, employee_id: str) -> Employee | None:
    """Return employee by business employee_id."""
    result = await session.execute(select(Employee).where(Employee.employee_id == employee_id))
    return result.scalar_one_or_none()


async def list_employees(session: AsyncSession) -> List[Employee]:
    """Return all active employees."""
    result = await session.execute(select(Employee).where(Employee.is_active.is_(True)))
    return result.scalars().all()


async def create_employee(session: AsyncSession, payload: EmployeeCreate) -> Employee:
    """Create a new employee record."""
    employee = Employee(**payload.model_dump())
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


async def update_employee(session: AsyncSession, employee: Employee, payload: EmployeeUpdate) -> Employee:
    """Update an existing employee record."""
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


async def soft_delete_employee(session: AsyncSession, employee: Employee) -> Employee:
    """Soft delete an employee record."""
    employee.is_active = False
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee
