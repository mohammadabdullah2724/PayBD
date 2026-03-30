from datetime import timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_password_hash,
    create_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import UserCreate


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Return a user by email."""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    """Return a user by UUID."""
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, payload: UserCreate) -> User:
    """Create a new user with hashed password."""
    hashed_password = create_password_hash(payload.password)
    user = User(email=payload.email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    """Authenticate a user by email and password."""
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_tokens_for_user(user: User) -> dict[str, str]:
    """Create access and refresh tokens for a user."""
    access_token = create_token(
        {"sub": str(user.id), "type": "access"},
        timedelta(minutes=settings.access_token_expire_minutes),
    )
    refresh_token = create_token(
        {"sub": str(user.id), "type": "refresh"},
        timedelta(days=settings.refresh_token_expire_days),
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def validate_token(token: str, token_type: str = "access") -> dict[str, str] | None:
    """Validate a JWT token and verify its type."""
    payload = decode_token(token)
    if not payload or payload.get("type") != token_type:
        return None
    return payload
