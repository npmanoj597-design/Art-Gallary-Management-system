import os

from dotenv import load_dotenv

# Load repo-root .env before importing anything that depends on it (e.g. app.db)
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_ENV_PATH = os.path.join(_REPO_ROOT, ".env")
load_dotenv(dotenv_path=_ENV_PATH, override=False)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes.artists import router as artists_router
from app.routes.artworks import router as artworks_router
from app.routes.exhibitions import router as exhibitions_router
from app.routes.visitors import router as visitors_router
from app.routes.tickets import router as tickets_router
from app.routes.reports import router as reports_router
from app.routes.auth import router as auth_router
from app.routes.categories import router as categories_router
from app.routes.curators import router as curators_router

app = FastAPI(title="Art Gallery Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_PREFIX = "/api"
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(artists_router, prefix=API_PREFIX)
app.include_router(artworks_router, prefix=API_PREFIX)
app.include_router(exhibitions_router, prefix=API_PREFIX)
app.include_router(visitors_router, prefix=API_PREFIX)
app.include_router(tickets_router, prefix=API_PREFIX)
app.include_router(reports_router, prefix=API_PREFIX)
app.include_router(categories_router, prefix=API_PREFIX)
app.include_router(curators_router, prefix=API_PREFIX)


FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend")
FRONTEND_DIR = os.path.abspath(FRONTEND_DIR)

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

