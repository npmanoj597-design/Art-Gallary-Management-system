from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_raw_connection
from app.auth.deps import require_admin
from app.models import Artist
from app.schemas import ArtistCreate, ArtistOut, ArtistUpdate


router = APIRouter(prefix="/artists", tags=["artists"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[ArtistOut])
def list_artists(db: Session = Depends(get_db)):
    rows = db.execute(select(Artist).order_by(Artist.artist_id)).scalars().all()
    return rows


@router.get("/{artist_id}", response_model=ArtistOut)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.execute(select(Artist).where(Artist.artist_id == artist_id)).scalar_one_or_none()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.post("", response_model=ArtistOut)
def create_artist(payload: ArtistCreate, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    artist = Artist(**payload.model_dump())
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


@router.put("/{artist_id}", response_model=ArtistOut)
def update_artist(
    artist_id: int,
    payload: ArtistUpdate,
    _admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    artist = db.execute(select(Artist).where(Artist.artist_id == artist_id)).scalar_one_or_none()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(artist, k, v)
    db.commit()
    db.refresh(artist)
    return artist


@router.delete("/{artist_id}")
def delete_artist(artist_id: int, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    artist = db.execute(select(Artist).where(Artist.artist_id == artist_id)).scalar_one_or_none()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    db.delete(artist)
    db.commit()
    return {"deleted": artist_id}


@router.get("/{artist_id}/sales")
def artist_total_revenue(artist_id: int, db: Session = Depends(get_db)):
    # Correlated subquery: sale_count + total revenue bound to the outer Artist row
    correlated_sql = text(
        """
        SELECT
          a.artist_id,
          a.name,
          (SELECT COUNT(s2.sale_id)
             FROM sale s2
             JOIN artwork aw2 ON aw2.artwork_id = s2.artwork_id
            WHERE aw2.artist_id = a.artist_id
          ) AS sale_count,
          (SELECT COALESCE(SUM(s3.amount_paid), 0)
             FROM sale s3
             JOIN artwork aw3 ON aw3.artwork_id = s3.artwork_id
            WHERE aw3.artist_id = a.artist_id
          ) AS total_revenue_correlated
        FROM artist a
        WHERE a.artist_id = :artist_id
        """
    )
    row = db.execute(correlated_sql, {"artist_id": artist_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Artist not found")

    # Stored procedure call: GetArtistRevenue artist_id -> OUT total_revenue
    with get_raw_connection() as conn:
        cur = conn.cursor()
        params = [artist_id]  # callproc for a function: only IN params
        cur.callproc("getartistrevenue", params)
        # callproc with a function leaves the result in the cursor
        res = cur.fetchone()
        total_revenue_proc = res[0] if res is not None else 0

    return {
        "artist_id": row["artist_id"],
        "artist_name": row["name"],
        "sale_count": int(row["sale_count"]),
        "total_revenue": float(total_revenue_proc),
        "total_revenue_correlated": float(row["total_revenue_correlated"]),
    }

