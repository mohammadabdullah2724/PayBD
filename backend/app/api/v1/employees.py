from typing import List
from uuid import UUID

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.dependencies import get_db_dependency
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.services.employee_service import (
    create_employee,
    get_employee_by_employee_id,
    get_employee_by_id,
    list_employees,
    soft_delete_employee,
    update_employee,
)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
async def create_employee_endpoint(
    payload: EmployeeCreate,
    session: AsyncSession = Depends(get_db_dependency),
    current_user=Depends(get_current_user),
) -> EmployeeRead:
    """Create a new employee with a unique employee_id."""
    existing = await get_employee_by_employee_id(session, payload.employee_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this employee_id already exists.",
        )
    employee = await create_employee(session, payload)
    return employee


@router.get("", response_model=List[EmployeeRead])
async def list_employee_endpoint(
    session: AsyncSession = Depends(get_db_dependency),
    current_user=Depends(get_current_user),
) -> List[EmployeeRead]:
    """List active employees."""
    return await list_employees(session)


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee_endpoint(
    employee_id: UUID,
    session: AsyncSession = Depends(get_db_dependency),
    current_user=Depends(get_current_user),
) -> EmployeeRead:
    """Get an employee by UUID."""
    employee = await get_employee_by_id(session, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")
    return employee


@router.put("/{employee_id}", response_model=EmployeeRead)
async def update_employee_endpoint(
    employee_id: UUID,
    payload: EmployeeUpdate,
    session: AsyncSession = Depends(get_db_dependency),
    current_user=Depends(get_current_user),
) -> EmployeeRead:
    """Update an employee record."""
    employee = await get_employee_by_id(session, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")
    updated = await update_employee(session, employee, payload)
    return updated


@router.delete("/{employee_id}", response_model=EmployeeRead)
async def delete_employee_endpoint(
    employee_id: UUID,
    session: AsyncSession = Depends(get_db_dependency),
    current_user=Depends(get_current_user),
) -> EmployeeRead:
    """Soft delete an employee."""
    employee = await get_employee_by_id(session, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")
    deleted = await soft_delete_employee(session, employee)
    return deleted
