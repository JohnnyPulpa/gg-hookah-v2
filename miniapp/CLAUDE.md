# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Telegram Mini App for hookah delivery service (gghookah.delivery). Part of a monorepo with four services:
- **miniapp/** (this dir) — React frontend served as Telegram WebApp
- **backend/** — Flask API (port 5001)
- **admin/** — Flask admin panel with Jinja2 templates (port 5002)
- **bot/** — Aiogram 3 Telegram bot

## Common Commands

### Miniapp (frontend)
```bash
cd /opt/gg-hookah-v2/miniapp
npm run dev          # Vite dev server with HMR
npm run build        # TypeScript check + Vite production build (tsc -b && vite build)
npm run lint         # ESLint
npm run preview      # Preview production build locally
```

### Backend / Admin (Python)
```bash
source /opt/gg-hookah-v2/venv/bin/activate
python /opt/gg-hookah-v2/backend/app.py     # Run backend on :5001
python /opt/gg-hookah-v2/admin/app.py       # Run admin on :5002
```

### Database migrations
```bash
cd /opt/gg-hookah-v2
source venv/bin/activate
alembic upgrade head        # Apply migrations
alembic revision --autogenerate -m "description"  # Create migration
```

### No test framework is configured. There are no tests.

## Architecture

### Miniapp Frontend (React 19 + TypeScript + Vite)

**Routing** (`App.tsx`): React Router v7 with `Layout` wrapper providing bottom navigation.
Routes: `/` (Home), `/catalog`, `/drinks-question`, `/drinks`, `/checkout`, `/orders`.

**API layer** (`src/api/`): Axios client with `baseURL: '/api'` (Nginx proxies to backend:5001). Modules: `mixes.ts`, `drinks.ts`, `orders.ts`.

**State management**: React Context for language only (`LanguageContext`). All other state is local component state via hooks. No Redux/Zustand.

**i18n**: Two languages (ru/en). Translations in `src/utils/translations.ts`. Language preference persisted to localStorage.

**Telegram integration**: WebApp SDK loaded via `<script>` in `index.html`. User ID accessed from `window.Telegram.WebApp.initDataUnsafe.user.id`.

**Styling**: Tailwind CSS with custom brand colors (orange `#F28C18`, green `#2E7D32`) defined in `tailwind.config.js`. CSS custom properties in `index.css` for dynamic theming. Mix of inline styles and Tailwind utility classes.

### Order Flow

Home → Catalog (select mix) → DrinksQuestion → DrinksCatalog (optional) → Checkout (address, deposit type, promo) → Orders (tracking with live session timer).

### Backend (Flask + SQLAlchemy + PostgreSQL)

UUID primary keys throughout. Key models: User, Guest, Mix, MenuItem, Discount, Order, OrderItem. Order statuses: NEW → CONFIRMED → ON_THE_WAY → DELIVERED → SESSION_ACTIVE → SESSION_ENDING → WAITING_FOR_PICKUP → COMPLETED (or CANCELED). Deposit types: cash, passport, none.

### Deployment

Nginx reverse proxy on gghookah.delivery: `/` serves miniapp static build, `/api` proxies to backend:5001, `/admin/` proxies to admin:5002. SSL via Let's Encrypt. Systemd services for backend, admin, and bot. Environment variables in `/etc/gg-hookah/.env`.

## Key Type Definitions

Core interfaces are in `miniapp/src/types/index.ts`: Mix (with MixCharacteristics: strength/coolness/sweetness/smokiness 1-5), Drink, Order, OrderStatus, DepositType. Telegram WebApp types in `types/telegram.d.ts`.
