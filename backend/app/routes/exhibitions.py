from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select, text
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.auth.deps import require_admin
from app.models import Artwork, Exhibition
from app.schemas import ExhibitionCreate, ExhibitionOut, ExhibitionUpdate, ArtworkOut


router = APIRouter(prefix="/exhibitions", tags=["exhibitions"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[ExhibitionOut])
def list_exhibitions(
    from_date: Optional[date] = Query(default=None),
    to_date: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Exhibition).order_by(Exhibition.start_date)
    if from_date and to_date:
        # Overlap condition
        stmt = stmt.where(and_(Exhibition.start_date <= to_date, Exhibition.end_date >= from_date))
    elif from_date:
        stmt = stmt.where(Exhibition.end_date >= from_date)
    elif to_date:
        stmt = stmt.where(Exhibition.start_date <= to_date)

    rows = db.execute(stmt).scalars().all()
    return rows


@router.get("/{exhibition_id}", response_model=ExhibitionOut)
def get_exhibition(exhibition_id: int, db: Session = Depends(get_db)):
    exhibition = db.execute(select(Exhibition).where(Exhibition.exhibition_id == exhibition_id)).scalar_one_or_none()
    if not exhibition:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    return exhibition


@router.post("", response_model=ExhibitionOut)
def create_exhibition(payload: ExhibitionCreate, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    exhibition = Exhibition(**payload.model_dump())
    db.add(exhibition)
    db.commit()
    db.refresh(exhibition)
    return exhibition


@router.put("/{exhibition_id}", response_model=ExhibitionOut)
def update_exhibition(
    exhibition_id: int,
    payload: ExhibitionUpdate,
    _admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    exhibition = db.execute(select(Exhibition).where(Exhibition.exhibition_id == exhibition_id)).scalar_one_or_none()
    if not exhibition:
        raise HTTPException(status_code=404, detail="Exhibition not found")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(exhibition, k, v)

    db.commit()
    db.refresh(exhibition)
    return exhibition


@router.delete("/{exhibition_id}")
def delete_exhibition(exhibition_id: int, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    exhibition = db.execute(select(Exhibition).where(Exhibition.exhibition_id == exhibition_id)).scalar_one_or_none()
    if not exhibition:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    db.delete(exhibition)
    db.commit()
    return {"deleted": exhibition_id}


@router.get("/{exhibition_id}/artworks", response_model=list[ArtworkOut])
def artworks_in_exhibition(exhibition_id: int, db: Session = Depends(get_db)):
    # Join Artwork + Artwork_Exhibition (junction). We only return Artwork fields to match ArtworkOut.
    sql = text(
        """
      SELECT aw.*
        FROM artwork_exhibition ae
        JOIN artwork aw ON aw.artwork_id = ae.artwork_id
       WHERE ae.exhibition_id = :exhibition_id
       ORDER BY aw.artwork_id
        """
    )
    rows = db.execute(sql, {"exhibition_id": exhibition_id}).mappings().all()
    if not rows:
        return []

    # Map into dicts compatible with ArtworkOut
    # (SQLAlchemy mappings() returns column names matching the table)
    return [
        {
            "artwork_id": r["artwork_id"],
            "title": r["title"],
            "year_created": r["year_created"],
            "medium": r["medium"],
            "price": float(r["price"]),
            "artist_id": r["artist_id"],
            "category_id": r["category_id"],
            "sold_count": r["sold_count"],
        }
        for r in rows
    ]

