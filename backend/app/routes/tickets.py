from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.db import get_raw_connection
from app.auth.deps import require_admin
from app.models import Ticket
from app.schemas import TicketBookRequest, TicketCreate, TicketOut, TicketUpdate


router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[TicketOut])
def list_tickets(db: Session = Depends(get_db)):
    rows = db.execute(select(Ticket).order_by(Ticket.ticket_id)).scalars().all()
    return rows


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id)).scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.post("", response_model=TicketOut)
def create_ticket(payload: TicketCreate, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    ticket = Ticket(**payload.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    _admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    ticket = db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id)).scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(ticket, k, v)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, _admin=Depends(require_admin), db: Session = Depends(get_db)):
    ticket = db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id)).scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(ticket)
    db.commit()
    return {"deleted": ticket_id}


@router.post("/book")
def book_ticket(payload: TicketBookRequest):
    """
    Books a ticket via the stored procedure `BookTicket`.
    Requirement: explicit transaction keywords COMMIT/ROLLBACK are present here.
    """
    with get_raw_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("BEGIN;")
            params = [payload.visitor_id, payload.exhibition_id, payload.seat_type]
            cur.callproc("bookticket", params)
            res = cur.fetchone()
            ticket_id = res[0] if res is not None else None

            cur.execute("COMMIT;")
        except Exception as e:
            cur.execute("ROLLBACK;")
            raise HTTPException(status_code=400, detail=f"Booking failed: {e}")

    # Fetch created ticket (outside the explicit BEGIN/COMMIT block).
    with SessionLocal() as db:
        ticket = db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id)).scalar_one_or_none()
        if not ticket:
            raise HTTPException(status_code=404, detail="Booked ticket not found after commit")
        return ticket

