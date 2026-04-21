from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Job, Monitor

router = APIRouter(prefix="/jobs")
templates = Jinja2Templates(directory="templates")


@router.get("")
def jobs(
    request: Request,
    db: Session = Depends(get_db),
    company: str = Query(default=""),
    q: str = Query(default=""),
    page: int = Query(default=1, ge=1),
):
    PAGE_SIZE = 20
    query = db.query(Job)

    if company:
        query = query.filter(Job.company == company)
    if q:
        query = query.filter(Job.title.ilike(f"%{q}%"))

    total = query.count()
    jobs_list = (
        query.order_by(Job.found_at.desc())
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
        .all()
    )

    monitors = db.query(Monitor).order_by(Monitor.company).all()
    companies = [m.company for m in monitors]
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    return templates.TemplateResponse("jobs.html", {
        "request": request,
        "page": "jobs",
        "jobs": jobs_list,
        "companies": companies,
        "selected_company": company,
        "q": q,
        "current_page": page,
        "total_pages": total_pages,
        "total": total,
    })
