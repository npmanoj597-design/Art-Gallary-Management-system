# Art Gallery Management System (DBMS Mini Project)

Full-stack project built with:
- Backend: Python + FastAPI
- Database: PostgreSQL
- Frontend: Vanilla HTML/CSS/JS (served by FastAPI)

## Features
- 3NF normalized schema with required tables
- DDL (CREATE/ALTER/DROP) + constraints (PK/FK/NOT NULL/UNIQUE/CHECK)
- DML (INSERT/UPDATE/DELETE) with cascades + transaction example
- Views (at least 2): `ExhibitionSummary`, `ArtworkSalesReport` (+ `VisitorTicketAttendance`)
- Stored procedures:
  - `BookTicket` (used by `POST /api/tickets/book`)
  - `GetArtistRevenue` (used by `GET /api/artists/{id}/sales`)
- Triggers:
  - Log ticket purchases into `TicketPurchaseLog`
  - Enforce `Sale.amount_paid` matches `Artwork.price`
  - Auto-increment `Artwork.sold_count` + log into `ArtworkSaleLog`
- JWT admin auth (admin users stored in DB)

## Setup (Local with Docker Postgres)

### 1) Start PostgreSQL
From the project root:
```powershell
docker-compose up -d
```

### 2) Configure environment
Create `.env`:
```powershell
copy .env.example .env
```
Edit `JWT_SECRET` to a strong random string.

### 3) Create database objects + seed data
Assuming Docker is on and Postgres is reachable on `localhost:5432`:

```powershell
$env:PGPASSWORD="art_gallery"
psql -h localhost -U art_gallery -d art_gallery -f sql/schema.sql
psql -h localhost -U art_gallery -d art_gallery -f sql/indexes.sql

# routines
psql -h localhost -U art_gallery -d art_gallery -f sql/procedures/GetArtistRevenue.sql
psql -h localhost -U art_gallery -d art_gallery -f sql/procedures/BookTicket.sql

# triggers (before seeding so logs/sold_count get populated)
psql -h localhost -U art_gallery -d art_gallery -f sql/triggers/LogTicketPurchase.sql
psql -h localhost -U art_gallery -d art_gallery -f sql/triggers/EnforceSaleAmountMatchArtworkPrice.sql
psql -h localhost -U art_gallery -d art_gallery -f sql/triggers/UpdateArtworkSoldCount.sql

# views
psql -h localhost -U art_gallery -d art_gallery -f sql/views/ExhibitionSummary.sql
psql -h localhost -U art_gallery -d art_gallery -f sql/views/ArtworkSalesReport.sql
psql -h localhost -U art_gallery -d art_gallery -f sql/views/VisitorTicketAttendance.sql
psql -h localhost -U art_gallery -d art_gallery -f sql/views/ArtistSalesStats.sql

# seed
psql -h localhost -U art_gallery -d art_gallery -f sql/seed.sql
```

### 4) Run the backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:
- `http://localhost:8000/`
- API base: `http://localhost:8000/api`

## Admin auth
- Seeded admin user exists from `sql/seed.sql`:
  - username: `admin`
  - password: `admin123`
- Admin dashboard: `http://localhost:8000/admin.html`

## REST API Endpoints

CRUD:
- `GET /api/artists`
- `GET /api/artists/{id}`
- `POST /api/artists` (admin)
- `PUT /api/artists/{id}` (admin)
- `DELETE /api/artists/{id}` (admin)

- `GET /api/artworks`
- `GET /api/artworks/{id}`
- `POST /api/artworks` (admin)
- `PUT /api/artworks/{id}` (admin)
- `DELETE /api/artworks/{id}` (admin)

- `GET /api/exhibitions?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD`
- `GET /api/exhibitions/{id}`
- `POST /api/exhibitions` (admin)
- `PUT /api/exhibitions/{id}` (admin)
- `DELETE /api/exhibitions/{id}` (admin)

- `GET /api/visitors`
- `GET /api/visitors/{id}`
- `POST /api/visitors` (admin)
- `PUT /api/visitors/{id}` (admin)
- `DELETE /api/visitors/{id}` (admin)

- `GET /api/tickets`
- `GET /api/tickets/{id}`
- `POST /api/tickets` (admin)
- `PUT /api/tickets/{id}` (admin)
- `DELETE /api/tickets/{id}` (admin)

Special endpoints:
- `GET /api/exhibitions/{id}/artworks`
- `GET /api/artists/{id}/sales`
- `GET /api/reports/top-artworks`
- `GET /api/reports/exhibition-summary`
- `GET /api/reports/visitor-attendance`
- `POST /api/tickets/book` (transaction + calls `BookTicket`)

Auth:
- `POST /api/auth/login`
- `POST /api/auth/signup`

## ER Diagram
- Mermaid ER diagram: [`docs/erd.mmd`](docs/erd.mmd)

