# GG HOOKAH v2 — Полная карта проекта

> Обновлено: 2026-02-20 | Коммит: `7680be1`

## АРХИТЕКТУРА

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Mini App    │     │  Admin Panel │     │  Telegram Bot│
│  React+Vite  │     │  Flask+Jinja │     │  aiogram 3   │
│  static SPA  │     │  :5002       │     │  polling     │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │  /api/*            │  /admin/*          │  :5003 /notify
       ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────┐
│                    Nginx (gghookah.delivery)              │
│  / → static    /api → :5001    /admin → :5002            │
└──────────────────────────┬───────────────────────────────┘
                           │
                    ┌──────▼───────┐
                    │  PostgreSQL  │
                    │  gg_hookah   │
                    └──────────────┘
```

**Сервер:** Ubuntu 24.04, Nginx, systemd, SSL Let's Encrypt
**БД:** PostgreSQL 16, SQLAlchemy ORM, Alembic migrations
**Python:** 3.12, venv: `/opt/gg-hookah-v2/venv/`
**Node:** для miniapp (React 19, Vite, Tailwind)

---

## РАБОЧИЕ URL

| URL | Назначение |
|-----|-----------|
| `https://gghookah.delivery` | Mini App (React SPA) |
| `https://gghookah.delivery/admin/` | Admin Panel |
| `https://gghookah.delivery/api/health` | API Health |
| `http://127.0.0.1:5001` | Backend API (internal) |
| `http://127.0.0.1:5002` | Admin Panel (internal) |
| `http://127.0.0.1:5003` | Bot Notification Server (internal) |
| `@OgHookahDelivery_bot` | Telegram Bot |

---

## СЕРВИСЫ (systemd)

| Сервис | Порт | Команда |
|--------|------|---------|
| `gg-hookah-api` | 5001 | `sudo systemctl restart gg-hookah-api` |
| `gg-hookah-admin` | 5002 | `sudo systemctl restart gg-hookah-admin` |
| `gg-hookah-bot` | polling + 5003 | `sudo systemctl restart gg-hookah-bot` |

Статус: все три **active (running)** ✅

---

## КАРТА ФАЙЛОВ

### `/opt/gg-hookah-v2/` — корень проекта

```
├── CLAUDE.md                    # Инструкции для Claude Code
├── CURRENT_TASK.md              # Текущая задача
├── GG_HOOKAH_CURRENT_STATE.md   # Этот файл
├── alembic.ini                  # Alembic config
├── .gitignore
│
├── .claude/
│   ├── settings.json            # Permissions для Claude Code
│   └── commands/
│       ├── deploy-miniapp.md    # /deploy-miniapp
│       ├── restart-all.md       # /restart-all
│       ├── check-health.md      # /check-health
│       └── end-of-day.md        # /end-of-day
│
├── migrations/
│   ├── env.py                   # Alembic environment
│   └── versions/
│       ├── 4ee508eaed82_initial_schema_all_tables.py
│       └── ffe00b36291f_add_discounts_used_order_fk.py
│
├── deploy/
│   ├── nginx/                   # Nginx конфиг
│   └── systemd/                 # Systemd unit files
│
├── backend/                     # Flask API (:5001)
├── admin/                       # Flask Admin (:5002)
├── bot/                         # Aiogram Bot
└── miniapp/                     # React Frontend
```

### `backend/` — REST API (Flask, порт 5001)

```
backend/
├── app.py                # Основное Flask-приложение, все API-эндпоинты
├── models.py             # SQLAlchemy модели (User, Guest, Mix, MenuItem, Order, ...)
├── seed_settings.py      # Seed начальных настроек в таблицу settings
├── requirements.txt      # Python зависимости
├── middleware/            # (пусто)
├── routes/               # (пусто — всё в app.py)
├── utils/                # (пусто)
└── static/               # Статика
```

### `admin/` — Admin Panel (Flask, порт 5002)

```
admin/
├── app.py                # Flask app + PrefixMiddleware + blueprints
├── auth.py               # Token auth: generate/verify, login_required decorator
├── routes/
│   ├── menu.py           # Mixes & Drinks CRUD (list/create/edit/toggle/featured)
│   ├── orders.py         # Orders list + detail + status transitions + _notify()
│   └── sessions.py       # Sessions list + detail + rebowl pipeline + _notify()
├── static/               # CSS/JS
└── templates/
    ├── base.html          # Общий layout: sidebar, topbar, dark theme
    ├── login.html         # Страница логина (без sidebar)
    ├── dashboard.html     # Redirect stub
    ├── orders_list.html   # Таблица заказов со статус-бейджами
    ├── order_detail.html  # Детали заказа + переходы статусов
    ├── sessions_list.html # Grid сессий с таймерами
    ├── session_detail.html# Детали сессии: таймер, rebowl, free extension
    ├── menu_mixes.html    # Список миксов
    ├── menu_mix_form.html # Форма создания/редактирования микса
    ├── menu_drinks.html   # Список напитков
    └── menu_drink_form.html # Форма создания/редактирования напитка
```

### `bot/` — Telegram Bot (aiogram 3.3.0)

```
bot/
├── bot_main.py              # Entry point: polling + notification server
├── config.py                # Env vars: BOT_TOKEN, DATABASE_URL, ADMIN_IDS
├── db.py                    # Async DB: get_user_language(), get_active_order(), ensure_user_exists()
├── templates.py             # RU/EN шаблоны сообщений (Spec 5.7)
├── notification_server.py   # aiohttp сервер на :5003 (POST /notify, GET /health)
├── requirements.txt
├── handlers/
│   └── start.py             # /start, /help, /language, /admin + persistent keyboard
├── keyboards/
│   └── main.py              # main_keyboard() — Open App, My Order, Support
├── middleware/               # (пусто)
└── services/
    ├── __init__.py
    └── notifications.py     # send_notification() — event→template, format, send
```

### `miniapp/` — React Frontend (React 19 + TypeScript + Vite + Tailwind)

```
miniapp/
├── package.json
├── vite.config.ts
├── tailwind.config.js       # Brand: orange #F28C18, green #2E7D32
├── tsconfig*.json
├── index.html               # Entry + Telegram SDK script
├── CLAUDE.md                # Miniapp-specific instructions
└── src/
    ├── main.tsx             # ReactDOM.createRoot
    ├── App.tsx              # React Router v7, 6 routes
    ├── index.css            # CSS custom properties for theming
    ├── types/
    │   ├── index.ts         # Mix, Drink, Order, OrderStatus, DepositType
    │   └── telegram.d.ts    # Telegram WebApp type declarations
    ├── api/
    │   ├── client.ts        # Axios instance, baseURL: '/api'
    │   ├── mixes.ts         # getAll(), getById(), getFeatured()
    │   ├── drinks.ts        # getAll()
    │   └── orders.ts        # createOrder(), getOrders()
    ├── contexts/
    │   └── LanguageContext.tsx  # RU/EN toggle, localStorage persist
    ├── components/
    │   ├── Layout.tsx       # Wrapper + bottom nav (Home/Menu/Orders/Support)
    │   ├── Header.tsx       # Top bar: logo, language toggle
    │   ├── MixCard.tsx      # Карточка микса с характеристиками
    │   └── Counter.tsx      # +/- selector
    ├── pages/
    │   ├── Home.tsx         # Featured mix, games, discount banner
    │   ├── Catalog.tsx      # Grid миксов
    │   ├── DrinksQuestion.tsx  # "Добавить напитки?" Yes/No
    │   ├── DrinksCatalog.tsx   # Grid напитков с counter
    │   ├── Checkout.tsx     # Адрес, телефон, deposit type, promo, submit
    │   └── Orders.tsx       # Активный заказ + история, таймер сессии
    └── utils/
        └── translations.ts  # t(key, lang) — строки перевода
```

---

## API ЭНДПОИНТЫ

### Backend (порт 5001)

| Метод | URL | Назначение |
|-------|-----|-----------|
| GET | `/health` | Health check (db) |
| GET | `/api/mixes` | Список активных миксов |
| GET | `/api/mixes/featured` | Featured микс |
| GET | `/api/drinks` | Список активных напитков |
| POST | `/api/orders` | Создать заказ |
| GET | `/api/orders?telegram_id=X` | Заказы пользователя |
| POST | `/api/discounts` | Применить скидку |
| POST | `/api/promo-codes` | Валидировать промокод |

### Admin (порт 5002, за `/admin/`)

| URL | Назначение |
|-----|-----------|
| `/auth/login?token=X` | Авторизация по токену |
| `/orders/` | Список заказов |
| `/orders/<id>` | Детали заказа |
| `/orders/<id>/transition` | POST: смена статуса |
| `/sessions/` | Список сессий |
| `/sessions/<id>` | Детали сессии |
| `/sessions/<id>/action` | POST: force_ending/complete/free_extend/adjust_timer |
| `/sessions/<id>/rebowl/<rid>/transition` | POST: rebowl статус |
| `/menu/mixes/` | Список миксов |
| `/menu/mixes/create` | Создать микс |
| `/menu/mixes/<id>/edit` | Редактировать микс |
| `/menu/mixes/<id>/toggle` | Вкл/выкл микс |
| `/menu/drinks/` | Список напитков |
| `/menu/drinks/create` | Создать напиток |
| `/menu/drinks/<id>/edit` | Редактировать напиток |

### Bot Notification Server (порт 5003)

| Метод | URL | Назначение |
|-------|-----|-----------|
| GET | `/health` | Health check |
| POST | `/notify` | Отправить уведомление пользователю |

---

## БАЗА ДАННЫХ

### Таблицы и данные

| Таблица | Строк | Назначение |
|---------|-------|-----------|
| `users` | 1 | Telegram пользователи |
| `guests` | 1 | Получатели доставки (phone, passport, trust_flag) |
| `mixes` | 4 | Кальянные миксы |
| `menu_items` | 6 | Напитки/снэки |
| `orders` | 4 | Заказы (2 SESSION_ENDING, 1 COMPLETED, 1 CANCELED) |
| `order_items` | 0 | Позиции заказов |
| `rebowl_requests` | 0 | Запросы замены чаши |
| `discounts` | 0 | Персональные скидки |
| `promo_codes` | 0 | Промокоды |
| `promo_code_usages` | 0 | Использования промокодов |
| `audit_logs` | 39 | Лог действий админов |
| `support_messages` | 0 | Сообщения поддержки |
| `settings` | 24 | Настройки приложения |

### Важные особенности колонок (gotchas)

- `orders`: **НЕТ** колонки `total_amount`
- `guests`: колонка `name` (НЕ `first_name`)
- `menu_items`: колонка `price_gel` (НЕ `price`)
- `rebowl_requests`: колонка `requested_at` (НЕ `created_at`)

### Стейт-машина заказов

```
NEW → CONFIRMED → ON_THE_WAY → DELIVERED → SESSION_ACTIVE → SESSION_ENDING → WAITING_FOR_PICKUP → COMPLETED
  ↓                                              ↕ free_extend                        ↕ rebowl DONE
CANCELED                                    SESSION_ACTIVE                       SESSION_ACTIVE
```

### Deposit types

`cash` | `passport` | `none`

---

## ЧТО СДЕЛАНО (по Milestones)

### Milestone 6: Telegram Bot Basic ✅
- `/start`, `/help`, `/language` commands
- Persistent keyboard (Open App, My Order, Support)
- SSL + WebApp URL

### Milestone 7: Admin Panel ✅
- M7.1-M7.2: Auth (bot token link) + base layout with sidebar
- M7.3: Orders list with status badges, deposit, timer, sorting
- M7.4: Order detail with status transitions, actions, confirm modals, audit
- M7.5: Sessions list + detail with timer, rebowl pipeline, free extension, adjust timer
- M7.6: Menu CRUD — mixes list/create/edit/toggle/featured + drinks list/create/edit/toggle

### Feature 1: Polish & Notifications ✅
- F1.1: Admin template inheritance — base.html + extends
- F1.2: Notification service — aiohttp server on :5003 + admin integration

### Mini App (Frontend) ✅
- Home page with featured mix
- Catalog — mix grid
- DrinksQuestion → DrinksCatalog flow
- Checkout form (address, deposit, promo)
- Orders page with session timer

---

## ИЗВЕСТНЫЕ БАГИ / TODO

- Нет тестов (ни Python, ни JS)
- `order_items` пустая — заказы создаются без item breakdown
- `routes/` и `utils/` в backend пустые — всё в `app.py`
- Bot middleware пустая папка

---

## Последний коммит

```
7680be1 Update CURRENT_TASK.md: F1.2 Notification Service complete
```

## Последние 10 коммитов

```
7680be1 Update CURRENT_TASK.md: F1.2 Notification Service complete
cdcfabb F1.2: Notification service (Admin → Bot → User) + Claude Code config
cf28483 F1.1: Admin template inheritance - base.html + extends, B22 sidebar fix
cfbeac0 M7.6: Menu CRUD - mixes list/create/edit/toggle/featured + drinks
f7050e4 Add CLAUDE.md with project guidance for Claude Code
ff6fcac M7.5: Sessions list + detail with timer, rebowl pipeline
95170cc M7.4: order detail with status transitions, actions, confirm modals
2a6f76c M7.3: orders list with status badges, deposit, timer, sorting
5242b5a M7.1-M7.2: admin auth via bot + base layout with sidebar
8c8f6e7 update nginx config with SSL
```

Всего коммитов: 24

---

## СЛЕДУЮЩИЙ ЧАТ — ПЛАН

Следующая задача: **F1.3** (по roadmap — уточнить у пользователя)

Возможные направления:
- Support chat (Spec 5.x) — двусторонний чат бот↔пользователь
- Session timer cron (автоматический SESSION_ENDING за 30 мин до конца)
- Discount system (выдача скидок после заказа)
- Order flow improvements (order_items заполнение)
