from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Category


router = APIRouter(prefix="/categories", tags=["categories"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[dict])
def list_categories(db: Session = Depends(get_db)):
    rows = db.execute(select(Category).order_by(Category.category_id)).scalars().all()
    return [
        {
            "category_id": r.category_id,
            "name": r.name,
            "description": r.description,
        }
        for r in rows
    ]

