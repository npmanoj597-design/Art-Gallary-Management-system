from fastapi import APIRouter, HTTPException
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from app.db import SessionLocal
from app.auth.jwt import create_access_token
from app.models import AdminUser
from app.schemas import AdminLoginRequest, AdminSignupRequest


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: AdminSignupRequest):
    with SessionLocal() as db:
        existing = db.execute(
            select(AdminUser).where(AdminUser.username == payload.username)
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="Username already exists")

        try:
            row = db.execute(
                text(
                    """
                    INSERT INTO adminuser (username, password_hash, role)
                    VALUES (:username, crypt(:password, gen_salt('bf')), 'admin')
                    RETURNING admin_id, username
                    """
                ),
                {"username": payload.username, "password": payload.password},
            ).mappings().one()
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Signup failed: {exc}") from exc

        return {"admin_id": row["admin_id"], "username": row["username"]}


@router.post("/login")
def login(payload: AdminLoginRequest):
    with SessionLocal() as db:
        try:
            row = db.execute(
                text(
                    """
                    SELECT admin_id, username, role
                    FROM adminuser
                    WHERE username = :username
                      AND crypt(:password, password_hash) = password_hash
                    """
                ),
                {"username": payload.username, "password": payload.password},
            ).mappings().first()
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=500, detail=f"Login failed: {exc}") from exc

        if not row:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token(subject=row["username"], role=row["role"])
        return {"access_token": token, "token_type": "bearer"}
