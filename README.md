# WiFi Billing System

A comprehensive WiFi billing and management system designed for ISPs and Hotspot providers. This system integrates a Django backend with a React frontend and targets FreeRADIUS for AAA to manage users, plans, vouchers, and payments.

## Overview

This repository contains a full-stack application:

- Backend API (Django + DRF) exposing authentication and billing endpoints, configured for JWT-based auth.
- Frontend SPA (React + Vite + Tailwind CSS) providing an admin dashboard and related views.
- Integrations planned/used: M-Pesa for payments, FreeRADIUS for authentication/accounting.

Entry points:

- Backend: manage.py (Django) with settings module config.settings.development by default; WSGI/ASGI in config/wsgi.py and config/asgi.py.
- Frontend: Vite dev server (npm run dev) serving React app in frontend/.

## Features

- User Management: Create and manage customer accounts.
- Plan Management: Define pricing plans with speed and data limits.
- Voucher System: Generate and sell vouchers for internet access.
- Billing & Payments: Integration with M-Pesa (via REST APIs).
- RADIUS Integration: Targeted integration with FreeRADIUS for authentication and accounting.
- Reporting: Detailed usage and sales reports.
- Responsive Frontend: Modern React-based dashboard for administrators and users.

## Stack Detection

- Backend: Python, Django 5.x, Django REST Framework, SimpleJWT, Celery, Redis, decouple
- Frontend: React 19, Vite 7, Tailwind CSS 4, React Router
- Database: MySQL/MariaDB (default in settings); others possible (psycopg2 included if using Postgres)
- Package managers: pip (requirements/base.txt), npm (frontend/package.json)

## Requirements

- Python 3.10+ (Django 5 requires Python >= 3.10)
- Node.js 18+ (Vite 7 requires Node >= 18)
- MySQL or MariaDB server (default configuration) or PostgreSQL (optional)
- Redis (for Celery tasks)
- FreeRADIUS server (for AAA) — TODO: document required schema/queries

## Environment Variables

Environment variables are loaded via python-decouple. Create a .env file in the project root (same directory as manage.py):

Example .env
SECRET_KEY=change-me
DB_ENGINE=mysql # optional; defaults from settings/base.py use mysql backend
DB_NAME=wifi_billing
DB_USER=wifi_user
DB_PASSWORD=strong-password
DB_HOST=127.0.0.1
DB_PORT=3306

# JWT and time zone are configured in code; adjust as needed

# M-Pesa

MPESA_CONSUMER_KEY=...
MPESA_CONSUMER_SECRET=...
MPESA_PASSKEY=...
MPESA_SHORTCODE=...
MPESA_CALLBACK_URL=https://example.com/mpesa/callback

# Redis/Celery

REDIS_URL=redis://localhost:6379/0

Notes:

- The database ENGINE is set to django.db.backends.mysql in config/settings/base.py and reads DB\_\* values from the environment.
- Time zone is set to Africa/Nairobi.

## Setup and Run

### Backend (Django)

1. Create and activate a virtual environment
   python -m venv .venv
   source .venv/bin/activate # Windows: .venv\\Scripts\\activate

2. Install dependencies
   pip install -r requirements/base.txt

3. Apply migrations
   python manage.py migrate

4. Create a superuser (optional)
   python manage.py createsuperuser

5. Run the development server
   python manage.py runserver

Optional (Celery Worker) — requires Redis
celery -A config worker --loglevel=info

### Frontend (React + Vite)

1. Navigate to the frontend directory
   cd frontend

2. Install dependencies
   npm install

3. Run the dev server
   npm run dev

4. Additional scripts

- Build: npm run build
- Preview build: npm run preview
- Lint: npm run lint

The frontend dev server typically runs on http://localhost:5173.

## Scripts (utilities)

Helper scripts are available in the scripts/ directory. Examples:

- Password reset: python scripts/reset_password.py
- Verification tools (ad hoc checks):
  - python scripts/verify_login.py
  - python scripts/verify_network.py
  - python scripts/verify_fraud.py
  - python scripts/verify_pricing.py
  - python scripts/verify_rbac.py
  - python scripts/verify_portal.py
  - python scripts/verify_social_billing.py
  - python scripts/verify_integrations.py
  - python scripts/verify_support.py
  - python scripts/verify_playbooks.py
  - python scripts/verify_customer_import.py
  - python scripts/verify_churn.py (also available at repo root as verify_churn.py)

Note: These scripts are intended for development and diagnostics. Review their source before use in production.

## Tests

- Django tests: use the built-in runner.
  python manage.py test

- Frontend linting: npm run lint (from frontend/)

TODOs:

- Add unit/integration tests under tests/ and apps/\*/tests.py as needed (folders exist but are placeholders).
- Define and document any E2E test tooling.

## Project Structure (top-level)

- apps/ — Django apps (accounts, billing, customers, radius, etc.)
- config/ — Django project (settings, urls, wsgi/asgi)
- deployment/ — deployment-related files (TODO: document)
- docs/ — documentation (TODO: expand)
- frontend/ — React + Vite app
- libs/ — shared Python libraries for the project
- logs/ — log files (gitignored in most setups)
- media/ — user-uploaded files
- requirements/ — pinned Python dependencies (base.txt)
- scripts/ — helper/verification scripts
- static/ — static files
- templates/ — Django templates
- tests/ — test scaffolding (e2e/, integration/)
- manage.py — Django management entry point
- verify_churn.py — convenience script (duplicate of scripts/ one)

## Configuration and Deployment

- Settings profiles: default DJANGO_SETTINGS_MODULE is config.settings.development (set in manage.py, wsgi.py, asgi.py).
- Production settings: TODO — add a production settings module and document environment-specific overrides.
- RADIUS/FreeRADIUS: TODO — document schema/queries and NAS configuration.
- Celery/Redis: Configured in `config/celery.py`. Run worker with `celery -A config worker -l info`.

## License

No license file was found at the repository root.
TODO: Add a LICENSE file and state the project’s license here.
