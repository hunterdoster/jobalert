from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Monitor, Job, RunLog
import random

ZILLOW_JOBS = [
    ("Senior Product Manager, Home Loans", "Seattle, WA / Remote", "https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External/job/Remote-USA/Senior-Product-Manager--Home-Loans_REQ-1001"),
    ("Technical Program Manager, Data Platform", "Remote, USA", "https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External/job/Remote-USA/Technical-Program-Manager--Data-Platform_REQ-1002"),
    ("Group Product Manager, Rentals", "Seattle, WA", "https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External/job/Seattle-WA/Group-Product-Manager--Rentals_REQ-1003"),
    ("Senior TPM, Mobile Engineering", "Remote, USA", "https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External/job/Remote-USA/Senior-TPM--Mobile-Engineering_REQ-1004"),
    ("Product Manager II, Search Experience", "Seattle, WA / Remote", "https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External/job/Remote-USA/Product-Manager-II--Search-Experience_REQ-1005"),
    ("Director of Product, New Construction", "Seattle, WA", "https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External/job/Seattle-WA/Director-of-Product--New-Construction_REQ-1006"),
    ("Staff TPM, Platform Infrastructure", "Remote, USA", "https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External/job/Remote-USA/Staff-TPM--Platform-Infrastructure_REQ-1007"),
]

GOOGLE_JOBS = [
    ("Technical Program Manager, YouTube", "Remote Eligible, USA", "https://careers.google.com/jobs/results/134567890-technical-program-manager-youtube/"),
    ("Senior Product Manager, Google Cloud", "Remote Eligible, USA", "https://careers.google.com/jobs/results/234567891-senior-product-manager-google-cloud/"),
    ("Program Manager, Google Workspace", "Remote Eligible, USA", "https://careers.google.com/jobs/results/334567892-program-manager-google-workspace/"),
    ("TPM, Infrastructure & Operations", "Remote Eligible, USA", "https://careers.google.com/jobs/results/434567893-tpm-infrastructure-operations/"),
    ("Product Manager, Google Maps", "Remote Eligible, USA", "https://careers.google.com/jobs/results/534567894-product-manager-google-maps/"),
    ("Senior TPM, Android Platform", "Remote Eligible, USA", "https://careers.google.com/jobs/results/634567895-senior-tpm-android-platform/"),
    ("Group Product Manager, Search", "Remote Eligible, USA", "https://careers.google.com/jobs/results/734567896-group-product-manager-search/"),
]

AIRBNB_JOBS = [
    ("Senior Product Manager, Payments", "Remote (US)", "https://careers.airbnb.com/positions/7649001/"),
    ("Engineering Manager, Trust & Safety", "Remote (US)", "https://careers.airbnb.com/positions/7649002/"),
    ("Senior Program Manager, Operations", "Remote (US)", "https://careers.airbnb.com/positions/7649003/"),
    ("Product Manager, Host Experience", "Remote (US)", "https://careers.airbnb.com/positions/7649004/"),
    ("Staff Technical Program Manager, Platform", "Remote (US)", "https://careers.airbnb.com/positions/7649005/"),
    ("Product Operations Lead, Stays", "Remote (US)", "https://careers.airbnb.com/positions/7649006/"),
    ("Senior Engineering Manager, Growth", "Remote (US)", "https://careers.airbnb.com/positions/7649007/"),
]


def seed_demo_data():
    db = SessionLocal()
    try:
        if db.query(Monitor).count() > 0:
            return  # already seeded

        now = datetime.utcnow()

        # --- Monitors ---
        zillow = Monitor(
            name="Zillow Monitor",
            company="Zillow",
            scraper_type="workday",
            target_url="https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External",
            keywords="Product Manager|TPM|Technical Program Manager|Group Product Manager|Director of Product|Staff TPM",
            is_active=True,
            last_run_at=now - timedelta(minutes=45),
            status="idle",
            color="blue",
        )
        google = Monitor(
            name="Google Monitor",
            company="Google",
            scraper_type="playwright-google",
            target_url="https://careers.google.com",
            keywords="Technical Program Manager|Program Manager|Product Manager|Technical Project Manager|Project Manager",
            is_active=True,
            last_run_at=now - timedelta(minutes=50),
            status="idle",
            color="green",
        )
        airbnb = Monitor(
            name="Airbnb Monitor",
            company="Airbnb",
            scraper_type="playwright-airbnb",
            target_url="https://careers.airbnb.com/positions/",
            keywords="Engineering Manager|Product Manager|Program Manager|Technical Program Manager|Staff TPM|Product Operations Lead",
            is_active=True,
            last_run_at=now - timedelta(minutes=55),
            status="idle",
            color="rose",
        )
        db.add_all([zillow, google, airbnb])
        db.flush()

        # --- Jobs ---
        job_rows = []
        offsets_days = [0, 0, 1, 1, 2, 3, 4]

        for i, (title, location, url) in enumerate(ZILLOW_JOBS):
            job_rows.append(Job(
                monitor_id=zillow.id,
                monitor_name="Zillow",
                company="Zillow",
                external_id=f"zillow-REQ-100{i+1}",
                title=title,
                location=location,
                job_url=url,
                found_at=now - timedelta(days=offsets_days[i], hours=random.randint(0, 8)),
                is_new=(i < 2),
            ))

        for i, (title, location, url) in enumerate(GOOGLE_JOBS):
            job_rows.append(Job(
                monitor_id=google.id,
                monitor_name="Google",
                company="Google",
                external_id=f"google-{134567890 + i}",
                title=title,
                location=location,
                job_url=url,
                found_at=now - timedelta(days=offsets_days[i], hours=random.randint(0, 8)),
                is_new=(i < 3),
            ))

        for i, (title, location, url) in enumerate(AIRBNB_JOBS):
            job_rows.append(Job(
                monitor_id=airbnb.id,
                monitor_name="Airbnb",
                company="Airbnb",
                external_id=f"airbnb-764900{i+1}",
                title=title,
                location=location,
                job_url=url,
                found_at=now - timedelta(days=offsets_days[i], hours=random.randint(0, 8)),
                is_new=(i < 2),
            ))

        db.add_all(job_rows)

        # --- Run logs (last 5 days, ~2 runs per monitor per day) ---
        log_rows = []
        monitors_meta = [
            (zillow, 181, 12),
            (google, 69, 18),
            (airbnb, 238, 26),
        ]
        for day in range(5):
            for hour_offset in [8, 16]:
                for monitor, scraped_base, matched_base in monitors_meta:
                    scraped = scraped_base + random.randint(-10, 10)
                    matched = matched_base + random.randint(-3, 3)
                    new = random.randint(0, 3) if day < 2 else 0
                    log_rows.append(RunLog(
                        monitor_id=monitor.id,
                        monitor_name=monitor.company,
                        run_at=now - timedelta(days=day, hours=hour_offset),
                        duration_sec=round(random.uniform(8.5, 45.0), 1),
                        jobs_scraped=scraped,
                        jobs_matched=matched,
                        jobs_new=new,
                        status="success",
                    ))

        db.add_all(log_rows)
        db.commit()
    finally:
        db.close()
