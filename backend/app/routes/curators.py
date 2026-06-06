from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Curator


router = APIRouter(prefix="/curators", tags=["curators"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[dict])
def list_curators(db: Session = Depends(get_db)):
    rows = db.execute(select(Curator).order_by(Curator.curator_id)).scalars().all()
    return [
        {
            "curator_id": r.curator_id,
            "name": r.name,
            "email": r.email,
            "phone": r.phone,
        }
        for r in rows
    ]

