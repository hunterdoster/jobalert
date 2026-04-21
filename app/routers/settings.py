from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Monitor

router = APIRouter(prefix="/settings")
templates = Jinja2Templates(directory="templates")

DEMO_CONFIG = {
    "NOTIFY_EMAIL": "your@email.com",
    "CHECK_INTERVAL_SEC": "7200",
    "QUIET_HOURS_START": "21:30",
    "QUIET_HOURS_END": "07:00",
    "TIMEZONE": "America/New_York",
    "DAILY_SUMMARY_HOUR": "18:00",
}


@router.get("")
def settings(request: Request, db: Session = Depends(get_db)):
    monitors = db.query(Monitor).order_by(Monitor.id).all()
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "page": "settings",
        "config": DEMO_CONFIG,
        "monitors": monitors,
    })
