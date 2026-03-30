from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    employee_id: str = Field(..., max_length=20)
    full_name: str = Field(..., max_length=200)
    email: EmailStr
    is_active: bool = True

    model_config = {"extra": "forbid"}


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    model_config = {"extra": "forbid"}


class EmployeeRead(EmployeeBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
