from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.auth.deps import require_admin
from app.models import Visitor
from app.schemas import VisitorCreate, VisitorOut, VisitorUpdate


router = APIRouter(prefix="/visitors", tags=["visitors"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[VisitorOut])
def list_visitors(db: Session = Depends(get_db)):
    rows = db.execute(select(Visitor).order_by(Visitor.visitor_id)).scalars().all()
    return rows


@router.get("/{visitor_id}", response_model=VisitorOut)
def get_visitor(visitor_id: int, db: Session = Depends(get_db)):
    visitor = db.execute(select(Visitor).where(Visitor.visitor_id == visitor_id)).scalar_one_or_none()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor


@router.post("", response_model=VisitorOut)
def create_visitor(payload: VisitorCreate, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    visitor = Visitor(**payload.model_dump())
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor


@router.put("/{visitor_id}", response_model=VisitorOut)
def update_visitor(
    visitor_id: int,
    payload: VisitorUpdate,
    _admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    visitor = db.execute(select(Visitor).where(Visitor.visitor_id == visitor_id)).scalar_one_or_none()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(visitor, k, v)
    db.commit()
    db.refresh(visitor)
    return visitor


@router.delete("/{visitor_id}")
def delete_visitor(visitor_id: int, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    visitor = db.execute(select(Visitor).where(Visitor.visitor_id == visitor_id)).scalar_one_or_none()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    db.delete(visitor)
    db.commit()
    return {"deleted": visitor_id}

