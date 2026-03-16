from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import tasks_controller
from app.database.connection import init_db, init_pool, close_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run on startup
    await init_pool()
    await init_db()
    yield
    # Run on shutdown
    await close_pool()

app = FastAPI(title="Task Management System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_controller.router, prefix="/api/v1")

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

