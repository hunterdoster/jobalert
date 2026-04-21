# JobAlert

A self-hosted job monitoring dashboard that scrapes career sites on a schedule, detects new matching roles, and sends email alerts. Built with Python, FastAPI, and Playwright.

**Live demo:** [your-app.railway.app](https://your-app.railway.app)

---

## Features

- **Three scrapers out of the box:** Workday API (Zillow), Playwright/Google Careers, Playwright/Airbnb
- **Keyword-based title matching** — configurable per monitor
- **Email alerts** via Gmail SMTP on every new match
- **Daily 6 PM summary email** — all new roles found that day
- **Quiet hours** — no alerts 9:30 PM – 7:00 AM ET
- **Web dashboard** — live run status, job table, run logs, settings reference
- **Demo mode** — ships with pre-seeded sample data; no credentials required to explore

---

## Quick Start (local)

```bash
git clone https://github.com/yourusername/jobalert
cd jobalert/jobalert-web
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) — demo data seeds automatically on first run.

---

## Deploy to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select `jobalert-web/` as the root directory (or point Railway at this folder)
4. Railway auto-detects the `Dockerfile` and deploys
5. Add a **Volume** at `/app/data` so the SQLite database persists across deploys
6. Set `DATABASE_URL=sqlite:////app/data/jobalert.db` in Railway environment variables

Cost: ~$5/month on the Hobby plan.

---

## Run the CLI monitors (separate from the web UI)

The web dashboard is display-only. The actual scrapers live in the parent directory and run from the command line:

```bash
# From the project root (not jobalert-web/)
py zillow_job_monitor.py --loop
py google_job_monitor.py --loop
py airbnb_job_monitor.py --loop
```

See the parent `README.md` for full CLI documentation.

---

## Project Structure

```
jobalert-web/
├── app/
│   ├── main.py          # FastAPI app + lifespan (DB init, demo seed)
│   ├── database.py      # SQLAlchemy engine + session
│   ├── models.py        # Monitor, Job, RunLog ORM models
│   ├── demo_data.py     # Pre-seeded sample data
│   └── routers/         # dashboard, jobs, monitors, logs, settings
├── templates/           # Jinja2 + Tailwind CSS
├── static/              # Static assets (served at /static)
├── Dockerfile
├── docker-compose.yml
├── railway.toml
└── requirements.txt
```

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.12 + FastAPI |
| Templating | Jinja2 |
| Styling | Tailwind CSS (CDN) |
| Database | SQLite via SQLAlchemy |
| Scrapers | Playwright (headless Chromium) + direct API |
| Email | Gmail SMTP |
| Hosting | Railway |

---

## Built by

Hunter Doster — [hunterdoster.com](https://hunterdoster.com)
