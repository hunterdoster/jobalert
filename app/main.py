from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.database import init_db
from app.demo_data import seed_demo_data
from app.routers import dashboard, jobs, monitors, logs, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_demo_data()
    yield


app = FastAPI(title="JobAlert", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(dashboard.router)
app.include_router(jobs.router)
app.include_router(monitors.router)
app.include_router(logs.router)
app.include_router(settings.router)
