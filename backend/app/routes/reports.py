from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import SessionLocal


router = APIRouter(prefix="/reports", tags=["reports"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/top-artworks", response_model=list[dict])
def top_artworks(limit: int = Query(default=5, ge=1, le=50), db: Session = Depends(get_db)):
    # Non-correlated subquery: ranked set ordered in outer query.
    sql = text(
        """
        SELECT
          artwork_id,
          title,
          artist_name,
          category_name,
          sale_count,
          total_revenue
        FROM (
          SELECT
            aw.artwork_id,
            aw.title,
            ar.name AS artist_name,
            cat.name AS category_name,
            COUNT(s.sale_id) AS sale_count,
            SUM(s.amount_paid) AS total_revenue
          FROM artwork aw
          JOIN artist ar ON ar.artist_id = aw.artist_id
          JOIN category cat ON cat.category_id = aw.category_id
          JOIN sale s ON s.artwork_id = aw.artwork_id
          GROUP BY aw.artwork_id, aw.title, ar.name, cat.name
          HAVING COUNT(s.sale_id) >= 1
        ) ranked
        ORDER BY total_revenue DESC
        LIMIT :limit
        """
    )
    rows = db.execute(sql, {"limit": limit}).mappings().all()
    result = []
    for r in rows:
        result.append(
            {
                **dict(r),
                "sale_count": int(r["sale_count"]),
                "total_revenue": float(r["total_revenue"]),
            }
        )
    return result


@router.get("/exhibition-summary", response_model=list[dict])
def exhibition_summary(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM exhibitionsummary ORDER BY start_date DESC")).mappings().all()
    return [
        {
            **dict(r),
            "artwork_count": int(r["artwork_count"]),
            "ticket_count": int(r["ticket_count"]),
            "total_ticket_revenue": float(r["total_ticket_revenue"]),
        }
        for r in rows
    ]


@router.get("/visitor-attendance", response_model=list[dict])
def visitor_attendance(db: Session = Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM visitorticketattendance ORDER BY tickets_purchased DESC, total_spent DESC")
    ).mappings().all()
    return [
        {
            **dict(r),
            "tickets_purchased": int(r["tickets_purchased"]),
            "total_spent": float(r["total_spent"]),
        }
        for r in rows
    ]

