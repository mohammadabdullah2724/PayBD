from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db


async def get_db_dependency() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for route dependencies."""
    async for session in get_db():
        yield session
