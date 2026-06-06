from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.auth.deps import require_admin
from app.models import Artwork
from app.schemas import ArtworkCreate, ArtworkOut, ArtworkUpdate


router = APIRouter(prefix="/artworks", tags=["artworks"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[ArtworkOut])
def list_artworks(db: Session = Depends(get_db)):
    rows = db.execute(select(Artwork).order_by(Artwork.artwork_id)).scalars().all()
    return rows


@router.get("/{artwork_id}", response_model=ArtworkOut)
def get_artwork(artwork_id: int, db: Session = Depends(get_db)):
    artwork = db.execute(select(Artwork).where(Artwork.artwork_id == artwork_id)).scalar_one_or_none()
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")
    return artwork


@router.post("", response_model=ArtworkOut)
def create_artwork(payload: ArtworkCreate, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    artwork = Artwork(**payload.model_dump())
    db.add(artwork)
    db.commit()
    db.refresh(artwork)
    return artwork


@router.put("/{artwork_id}", response_model=ArtworkOut)
def update_artwork(
    artwork_id: int,
    payload: ArtworkUpdate,
    _admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    artwork = db.execute(select(Artwork).where(Artwork.artwork_id == artwork_id)).scalar_one_or_none()
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(artwork, k, v)
    db.commit()
    db.refresh(artwork)
    return artwork


@router.delete("/{artwork_id}")
def delete_artwork(artwork_id: int, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    artwork = db.execute(select(Artwork).where(Artwork.artwork_id == artwork_id)).scalar_one_or_none()
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")
    db.delete(artwork)
    db.commit()
    return {"deleted": artwork_id}

