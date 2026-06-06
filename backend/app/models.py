from datetime import date, datetime

from sqlalchemy import String, Integer, Text, Numeric, Date, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AdminUser(Base):
    __tablename__ = "adminuser"

    admin_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="admin")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())


class Artist(Base):
    __tablename__ = "artist"

    artist_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    nationality: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)


class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class Artwork(Base):
    __tablename__ = "artwork"

    artwork_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year_created: Mapped[int] = mapped_column(Integer, nullable=False)
    medium: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    sold_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.artist_id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id", ondelete="CASCADE"), nullable=False)


class Curator(Base):
    __tablename__ = "curator"

    curator_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)


class Exhibition(Base):
    __tablename__ = "exhibition"

    exhibition_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    theme: Mapped[str] = mapped_column(String(200), nullable=False)
    curator_id: Mapped[int] = mapped_column(ForeignKey("curator.curator_id", ondelete="CASCADE"), nullable=False)
    ticket_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)


class Visitor(Base):
    __tablename__ = "visitor"

    visitor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    membership_type: Mapped[str] = mapped_column(String(20), nullable=False)


class Ticket(Base):
    __tablename__ = "ticket"

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visitor_id: Mapped[int] = mapped_column(ForeignKey("visitor.visitor_id", ondelete="CASCADE"), nullable=False)
    exhibition_id: Mapped[int] = mapped_column(ForeignKey("exhibition.exhibition_id", ondelete="CASCADE"), nullable=False)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    seat_type: Mapped[str] = mapped_column(String(50), nullable=False)


class Sale(Base):
    __tablename__ = "sale"

    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    artwork_id: Mapped[int] = mapped_column(ForeignKey("artwork.artwork_id", ondelete="CASCADE"), nullable=False)
    visitor_id: Mapped[int] = mapped_column(ForeignKey("visitor.visitor_id", ondelete="CASCADE"), nullable=False)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)


class Staff(Base):
    __tablename__ = "staff"

    staff_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)


class TicketPurchaseLog(Base):
    __tablename__ = "ticketpurchaselog"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visitor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exhibition_id: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    seat_type: Mapped[str] = mapped_column(String(50), nullable=False)


class ArtworkSaleLog(Base):
    __tablename__ = "artworksalelog"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(Integer, nullable=False)
    artwork_id: Mapped[int] = mapped_column(Integer, nullable=False)
    visitor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
