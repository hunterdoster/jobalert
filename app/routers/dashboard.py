from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Monitor, Job, RunLog

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    monitors = db.query(Monitor).order_by(Monitor.id).all()
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    total_jobs = db.query(func.count(Job.id)).scalar()
    jobs_today = db.query(func.count(Job.id)).filter(Job.found_at >= today_start).scalar()
    new_today = db.query(func.count(Job.id)).filter(Job.found_at >= today_start, Job.is_new == True).scalar()  # noqa: E712

    last_run = db.query(func.max(RunLog.run_at)).scalar()
    last_run_str = _ago(last_run) if last_run else "Never"

    recent_jobs = (
        db.query(Job)
        .order_by(Job.found_at.desc())
        .limit(10)
        .all()
    )

    monitor_stats = []
    for m in monitors:
        today_count = db.query(func.count(Job.id)).filter(
            Job.monitor_id == m.id, Job.found_at >= today_start
        ).scalar()
        last_log = (
            db.query(RunLog)
            .filter(RunLog.monitor_id == m.id)
            .order_by(RunLog.run_at.desc())
            .first()
        )
        monitor_stats.append({
            "monitor": m,
            "today_count": today_count,
            "last_log": last_log,
            "last_run_ago": _ago(m.last_run_at) if m.last_run_at else "Never",
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "page": "dashboard",
        "monitors": monitors,
        "monitor_stats": monitor_stats,
        "total_jobs": total_jobs,
        "jobs_today": jobs_today,
        "new_today": new_today,
        "last_run_str": last_run_str,
        "recent_jobs": recent_jobs,
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
