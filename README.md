# AutoSalon Pro — Production Telegram CRM

A production-ready starter for an auto dealership: Telegram Bot + Telegram Mini App + FastAPI + PostgreSQL + Admin CRM.

## Features
- Vehicle catalog with photos
- Search/filter by brand
- Lead capture with Telegram contact
- Test-drive requests
- Credit payment calculator
- Promotions
- Admin CRM with login
- Lead status management
- Vehicle CRUD
- Promotion CRUD
- Manager assignment
- Dashboard statistics
- CSV lead export
- SQLAlchemy + Alembic migrations
- Docker / Render deployment
- Health/readiness endpoints
- Security headers, CORS and rate limiting

## Deploy on Render
Create a PostgreSQL database and a Docker Web Service from this repository.

Environment variables:
- `BOT_TOKEN` — BotFather token
- `ADMIN_IDS` — comma-separated Telegram IDs allowed to receive bot notifications
- `DATABASE_URL` — Render internal PostgreSQL URL using `postgresql+asyncpg://`
- `ADMIN_USERNAME` — CRM username
- `ADMIN_PASSWORD` — strong CRM password
- `WEB_APP_URL` — public Render URL
- `CORS_ORIGINS` — same public URL, comma separated
- `SECRET_KEY` — long random secret

Start command is handled by Docker.

After first deploy:
```bash
python -m app.seed
```

For Render, run the seed command from the service shell if you want demo data.

## Important
Change demo credentials before production. Never commit `.env`.
