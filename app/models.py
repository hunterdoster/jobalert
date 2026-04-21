from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from app.database import Base
from datetime import datetime


class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    scraper_type = Column(String, nullable=False)  # workday | playwright-google | playwright-airbnb
    target_url = Column(String, nullable=False)
    keywords = Column(Text, nullable=False)         # pipe-separated
    is_active = Column(Boolean, default=True)
    last_run_at = Column(DateTime, nullable=True)
    status = Column(String, default="idle")         # idle | running | error
    color = Column(String, default="indigo")        # tailwind color name for card accent


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    monitor_id = Column(Integer, nullable=False)
    monitor_name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    external_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    job_url = Column(String, nullable=False)
    found_at = Column(DateTime, default=datetime.utcnow)
    is_new = Column(Boolean, default=True)


class RunLog(Base):
    __tablename__ = "run_logs"

    id = Column(Integer, primary_key=True, index=True)
    monitor_id = Column(Integer, nullable=False)
    monitor_name = Column(String, nullable=False)
    run_at = Column(DateTime, nullable=False)
    duration_sec = Column(Float, nullable=False)
    jobs_scraped = Column(Integer, default=0)
    jobs_matched = Column(Integer, default=0)
    jobs_new = Column(Integer, default=0)
    status = Column(String, default="success")      # success | error
    error_message = Column(String, nullable=True)
