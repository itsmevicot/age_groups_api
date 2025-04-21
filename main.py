from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.routers.age_group_router import router as age_group_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown lifecycle events using FastAPI's lifespan handler.
    """
    print(f"Starting Age Groups API on port {settings.port}")
    yield
    print("Shutting down Age Groups API")

app = FastAPI(
    title="Age Groups API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(age_group_router)
