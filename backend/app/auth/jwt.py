import os
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt


JWT_SECRET = os.environ.get("JWT_SECRET", "")
JWT_ALG = os.environ.get("JWT_ALG", "HS256")
JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "1440"))

if not JWT_SECRET:
    # Keep error explicit; env var required at runtime.
    raise RuntimeError("JWT_SECRET is not set. Create a .env file from .env.example.")


def create_access_token(subject: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

