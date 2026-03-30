import inspect

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_dependency
from app.schemas.auth import Token, UserCreate, UserLogin, UserRead
from app.services.auth_service import (
    authenticate_user,
    create_tokens_for_user,
    create_user,
    get_user_by_email,
    validate_token,
)
from app.services.auth_service import get_user_by_id

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_db_dependency),
) -> UserRead:
    """Register a new user."""
    existing = await get_user_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")
    user = await create_user(session, payload)
    return user


@router.post("/login", response_model=Token)
async def login_user(
    payload: UserLogin,
    session: AsyncSession = Depends(get_db_dependency),
) -> Token:
    """Authenticate user and return access and refresh tokens."""
    user = await authenticate_user(session, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    tokens = create_tokens_for_user(user)
    if inspect.isawaitable(tokens):
        tokens = await tokens
    return Token(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
    session: AsyncSession = Depends(get_db_dependency),
):
    """Return the current user when a valid bearer token is provided."""
    if credentials is None:
        return None

    token = credentials.credentials
    payload = validate_token(token, token_type="access")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
    user = await get_user_by_id(session, payload["sub"])
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    return user


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user=Depends(get_current_user)) -> UserRead:
    """Return current authenticated user profile."""
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")
    return current_user
