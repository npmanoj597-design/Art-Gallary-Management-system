from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr, Field


MembershipType = Literal["Regular", "Premium", "Student"]


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminSignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6)
    email: Optional[EmailStr] = None


class ArtistCreate(BaseModel):
    name: str
    nationality: str
    birth_year: int
    bio: str


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None
    birth_year: Optional[int] = None
    bio: Optional[str] = None


class ArtistOut(BaseModel):
    artist_id: int
    name: str
    nationality: str
    birth_year: int
    bio: str


class CategoryOut(BaseModel):
    category_id: int
    name: str
    description: str


class ArtworkCreate(BaseModel):
    title: str
    year_created: int
    medium: str
    price: float
    artist_id: int
    category_id: int


class ArtworkUpdate(BaseModel):
    title: Optional[str] = None
    year_created: Optional[int] = None
    medium: Optional[str] = None
    price: Optional[float] = None
    artist_id: Optional[int] = None
    category_id: Optional[int] = None


class ArtworkOut(BaseModel):
    artwork_id: int
    title: str
    year_created: int
    medium: str
    price: float
    artist_id: int
    category_id: int
    sold_count: int


class ExhibitionCreate(BaseModel):
    title: str
    start_date: date
    end_date: date
    theme: str
    curator_id: int
    ticket_price: float


class ExhibitionUpdate(BaseModel):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    theme: Optional[str] = None
    curator_id: Optional[int] = None
    ticket_price: Optional[float] = None


class ExhibitionOut(BaseModel):
    exhibition_id: int
    title: str
    start_date: date
    end_date: date
    theme: str
    curator_id: int
    ticket_price: float


class CuratorOut(BaseModel):
    curator_id: int
    name: str
    email: str
    phone: str


class VisitorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    membership_type: MembershipType


class VisitorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    membership_type: Optional[MembershipType] = None


class VisitorOut(BaseModel):
    visitor_id: int
    name: str
    email: str
    phone: str
    membership_type: MembershipType


class TicketCreate(BaseModel):
    visitor_id: int
    exhibition_id: int
    purchase_date: date
    price: float
    seat_type: str


class TicketUpdate(BaseModel):
    visitor_id: Optional[int] = None
    exhibition_id: Optional[int] = None
    purchase_date: Optional[date] = None
    price: Optional[float] = None
    seat_type: Optional[str] = None


class TicketOut(BaseModel):
    ticket_id: int
    visitor_id: int
    exhibition_id: int
    purchase_date: date
    price: float
    seat_type: str


class TicketBookRequest(BaseModel):
    visitor_id: int
    exhibition_id: int
    seat_type: str


class SaleOut(BaseModel):
    sale_id: int
    artwork_id: int
    visitor_id: int
    sale_date: date
    amount_paid: float


class TopArtworkItem(BaseModel):
    artwork_id: int
    title: str
    artist_name: str
    category_name: str
    sale_count: int
    total_revenue: float


class ExhibitionSummaryRow(BaseModel):
    exhibition_id: int
    title: str
    start_date: date
    end_date: date
    theme: str
    curator_name: Optional[str]
    artwork_count: int
    ticket_count: int
    total_ticket_revenue: float

