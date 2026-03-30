import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from app.core.config import settings

ALGORITHM = "HS256"
PASSWORD_HASH_ITERATIONS = 100_000
PASSWORD_HASH_SALT_SIZE = 16


def create_password_hash(password: str) -> str:
    """Return a salted PBKDF2 password hash."""
    salt = secrets.token_bytes(PASSWORD_HASH_SALT_SIZE)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS)
    return f"pbkdf2_sha256${salt.hex()}${hash_bytes.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a stored hash."""
    try:
        algorithm, salt_hex, hash_hex = hashed_password.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        computed_hash = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt,
            PASSWORD_HASH_ITERATIONS,
        )
        return hmac.compare_digest(computed_hash, expected_hash)
    except ValueError:
        return False


def create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    """Create a signed JWT token."""
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire, "type": data.get("type", "access")})
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode a JWT token and validate its signature."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
