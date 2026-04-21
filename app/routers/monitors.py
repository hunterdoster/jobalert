from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Monitor, Job, RunLog
from sqlalchemy import func
from datetime import datetime

router = APIRouter(prefix="/monitors")
templates = Jinja2Templates(directory="templates")


@router.get("")
def monitors(request: Request, db: Session = Depends(get_db)):
    monitors_list = db.query(Monitor).order_by(Monitor.id).all()

    stats = []
    for m in monitors_list:
        total_found = db.query(func.count(Job.id)).filter(Job.monitor_id == m.id).scalar()
        last_log = (
            db.query(RunLog)
            .filter(RunLog.monitor_id == m.id)
            .order_by(RunLog.run_at.desc())
            .first()
        )
        keywords = [k.strip() for k in m.keywords.split("|") if k.strip()]
        stats.append({
            "monitor": m,
            "total_found": total_found,
            "last_log": last_log,
            "keywords": keywords,
            "last_run_ago": _ago(m.last_run_at),
        })

    scraper_labels = {
        "workday": "Workday API",
        "playwright-google": "Playwright (Google Careers)",
        "playwright-airbnb": "Playwright (Airbnb Careers)",
    }

    return templates.TemplateResponse("monitors.html", {
        "request": request,
        "page": "monitors",
        "stats": stats,
        "scraper_labels": scraper_labels,
    })


def _ago(dt: datetime | None) -> str:
    if not dt:
        return "Never"
    diff = datetime.utcnow() - dt
    minutes = int(diff.total_seconds() / 60)
    if minutes < 1:
        return "Just now"
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    return f"{diff.days}d ago"
