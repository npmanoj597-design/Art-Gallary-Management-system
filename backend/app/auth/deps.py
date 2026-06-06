from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.auth.jwt import decode_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing Authorization token")

    token_data = decode_token(credentials.credentials)
    if token_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return token_data

