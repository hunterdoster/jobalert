from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import RunLog, Monitor

router = APIRouter(prefix="/logs")
templates = Jinja2Templates(directory="templates")


@router.get("")
def logs(
    request: Request,
    db: Session = Depends(get_db),
    company: str = Query(default=""),
    page: int = Query(default=1, ge=1),
):
    PAGE_SIZE = 30
    query = db.query(RunLog)

    if company:
        query = query.filter(RunLog.monitor_name == company)

    total = query.count()
    logs_list = (
        query.order_by(RunLog.run_at.desc())
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
        .all()
    )

    monitors = db.query(Monitor).order_by(Monitor.company).all()
    companies = [m.company for m in monitors]
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    return templates.TemplateResponse("logs.html", {
        "request": request,
        "page": "logs",
        "logs": logs_list,
        "companies": companies,
        "selected_company": company,
        "current_page": page,
        "total_pages": total_pages,
        "total": total,
    })
