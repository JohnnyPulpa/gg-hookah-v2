# CLAUDE.md — Project Context for Claude Code

## Project: GG HOOKAH v2
Telegram Mini App для доставки кальянов в Батуми.

## Architecture
- Backend API: Flask on port 5001 (gunicorn)
- Admin Panel: Flask on port 5002 (gunicorn)
- Telegram Bot: aiogram 3.3.0 (polling)
- Frontend: React + TypeScript + Vite + Tailwind
- DB: PostgreSQL 16
- Server: Ubuntu 24.04, Nginx, systemd

## Key Paths
- Project: /opt/gg-hookah-v2/
- Venv: source /opt/gg-hookah-v2/venv/bin/activate
- Secrets: /etc/gg-hookah/.env
- Mini App build: /var/www/gghokah.delivery/
- Passport storage: /var/lib/gg-hookah/passports/

## Services
- systemctl restart gg-hookah-api
- systemctl restart gg-hookah-admin
- systemctl restart gg-hookah-bot

## After Mini App changes
cd /opt/gg-hookah-v2/miniapp && npm run build
sudo rm -rf /var/www/gghokah.delivery/*
sudo cp -r dist/* /var/www/gghokah.delivery/
sudo chown -R www-data:www-data /var/www/gghokah.delivery

## DB Column Gotchas
- orders: NO total_amount column
- guests: column is "name" (NOT first_name)
- menu_items: column is "price_gel" (NOT price)
- rebowl_requests: column is "requested_at" (NOT created_at)

## Rules
- STRICTLY follow the spec (GG_HOOKAH_Spec_Master_v2_1.docx)
- Never invent features not in the spec
- Use placeholders for secrets: {{BOT_TOKEN}}, {{DB_PASSWORD}}
- Always activate venv before Python work
- Admin templates: currently standalone HTML (no extends)
- Git commit after each logical block of changes

## Контекст бизнеса

GG Hookah — сервис доставки и аренды кальянов в Батуми (Грузия).
Клиент заказывает кальян через Telegram Mini App → владелец доставляет сам →
клиент курит (сессия с таймером) → владелец забирает.

**Текущий этап:** Владелец работает один (доставка, сборка, поддержка).
**Будущее:** Найм курьеров, расширение зон доставки, event-направление.

Система должна быть спроектирована ДЛЯ МАСШТАБИРОВАНИЯ, но реализована
поэтапно — сначала минимум для соло-работы, потом модули для команды.

## Текущий план работы

Выполняй задачи по порядку внутри фазы. После каждой — коммит, обновление CURRENT_TASK.md и BUGS.md, краткий отчёт. Затем СПРОСИ пользователя: "Переходим к следующей задаче?"

### ФАЗА 1: ФУНДАМЕНТ ✅

- F1.1 ✅ Admin Template Inheritance
- F1.2 ✅ Notification Service (Admin → Bot)
- F1.3 ✅ Session Timer Cron
- F1.4 ✅ Users table + Language sync

### ФАЗА 2: КЛИЕНТСКИЙ ОПЫТ (~3-4 дня)

#### F2.1 — Bot Hot Actions: Cancel, Ready for Pickup
- Клиент нажимает inline кнопку в Telegram → статус меняется
- Cancel: только до DELIVERED (после — только через support)
- Ready for Pickup: клиент сигнализирует что закончил раньше
- Admin получает уведомление о действии клиента
- Файлы: `bot/handlers/order_actions.py`

#### F2.2 — Bot Hot Actions: Free +1h, Rebowl Request
- Free +1h: клиент нажимает → session_ends_at += 1 hour (доступно 1 раз)
- Rebowl: клиент запрашивает → создаётся rebowl_request → admin видит в панели
- Rebowl pipeline: REQUEST → CONFIRMED → IN_PROGRESS → DONE
- Время ограничение: недоступно после 02:00 (Asia/Tbilisi)
- Файлы: `bot/handlers/session_actions.py`

#### F2.3 — Support Routing
- Клиент пишет боту обычное сообщение → сохраняется в support_messages
- thread_type: order (привязан к заказу), session, general
- Бот отвечает: "Мы получили ваше сообщение, ответим в течение 15 минут"
- Admin видит в Support inbox
- Файлы: `bot/handlers/support.py`, `admin/routes/support.py`

#### F2.4 — Mini App: Active Order Actions
- В Mini App на странице Orders: кнопки Cancel, Ready for Pickup
- Вызывают API → API отправляет notify → бот уведомляет admin
- Файлы: `miniapp/src/pages/Orders.tsx`, `backend/routes/orders.py`

### ФАЗА 3: ADMIN ПАНЕЛЬ — ОПЕРАЦИИ (~3-4 дня)

#### F3.1 — Admin Dashboard (полный редизайн главной страницы)
- Live Orders, Today Revenue, Total Orders Today, Active Sessions виджеты
- Available Hookahs (пока hardcode, потом из inventory)
- Kanban-доска активных заказов (карточки по колонкам статусов)
- Quick actions прямо из карточек (Accept, Ship, Deliver и т.д.)
- Звуковое/визуальное уведомление при новом заказе
- Revenue chart за 7 дней, Top mixes pie chart, Alerts
- Файлы: `admin/routes/dashboard.py`, `admin/templates/dashboard.html`, `admin/static/js/dashboard.js`

#### F3.2 — Settings Editor
- CRUD для таблицы settings (24 записи)
- Группировка: Business Hours, Pricing, Delivery, Notifications
- Валидация типов (number, text, boolean, json)
- Файлы: `admin/routes/settings.py`, `admin/templates/settings.html`

#### F3.3 — Guests Management (CRM lite)
- Список гостей с поиском и фильтрами
- Карточка гостя: trust level, passport status, история заказов, total spend, любимый микс, notes
- Passport upload → `/var/lib/gg-hookah/passports/`
- Файлы: `admin/routes/guests.py`, `admin/templates/guests_*.html`

#### F3.4 — Discounts & Promo Codes
- Issue/withdraw скидки, create promo code
- Файлы: `admin/routes/discounts.py`, `admin/templates/discounts.html`

#### F3.5 — Support Inbox
- Priority (привязанные к заказу/сессии) и General
- Непрочитанные badge в sidebar, ответ через бота
- Файлы: `admin/routes/support.py`, `admin/templates/support_*.html`

#### F3.6 — Logs & System
- Audit log viewer с фильтрами, Service status page
- Файлы: `admin/routes/system.py`, `admin/templates/system.html`

### ФАЗА 4: ПОЛИРОВКА + PRODUCTION (~2-3 дня)

#### F4.1 — Telegram initData Validation
- Все API запросы из Mini App проверяют подпись Telegram, без подписи → 401
- Файлы: `backend/middleware/telegram_auth.py`

#### F4.2 — Mini App UX Polish
- Skeleton loader, маскот оптимизация, pull-to-refresh, haptic feedback

#### F4.3 — Dynamic Discount Banner
- Баннер на Home берёт данные из API вместо hardcoded -15%

#### F4.4 — Error Handling & Edge Cases
- Fallback если бот не отвечает, 0 кальянов, timeouts, graceful degradation

#### F4.5 — E2E Testing
- QA checklist: полный путь заказа, проверка уведомлений

### ФАЗА 5: ИНВЕНТАРЬ И ФИНАНСЫ (~4-5 дней) — POST-MVP

#### F5.1 — Inventory: Hookahs (Asset Tracking)
- Таблица `hookahs`, привязка к заказам, dashboard виджет "Available: 7/12"

#### F5.2 — Inventory: Consumables
- Таблица `consumables`, списание при заказе, alert при low_threshold

#### F5.3 — Financial Dashboard
- Revenue, средний чек, top mixes по выручке, расходы, P&L, export CSV

#### F5.4 — Delivery Zones
- Таблица `delivery_zones`, карта Батуми (Leaflet.js), зоны с разными тарифами

### ФАЗА 6: МАСШТАБИРОВАНИЕ — КОМАНДА (~5-7 дней)

#### F6.1 — Delivery Staff Management
- Таблица `delivery_staff`, назначение на заказ, уведомление курьеру

#### F6.2 — Courier Bot
- Отдельный flow: мои заказы, "Забрал", "Доставил", фото-подтверждение

#### F6.3 — Staff Analytics
- Заказов за смену, среднее время, рейтинг

#### F6.4 — Role-Based Access
- owner/manager/operator, middleware проверки

#### F6.5 — Multi-channel Notifications
- Firebase push, SMS fallback, email отчёты

### ФАЗА 7: GROWTH — НОВЫЕ КАНАЛЫ (~5-7 дней)

#### F7.1 — Event Booking
- Пакеты (3/5/10 кальянов), календарь, предоплата 50%

#### F7.2 — Loyalty Program
- Баллы, уровни Bronze/Silver/Gold, реферальный код

#### F7.3 — Hotel Partnerships
- Отдельный вход, комиссия 10-15%, QR для гостей

#### F7.4 — Payment Integration
- BOG iPay / TBC Pay, payment link в боте

#### F7.5 — Advanced Analytics
- Прогноз спроса, heatmap, CLV, churn prediction

### ФАЗА 8: МОНИТОРИНГ (параллельно)

#### F8.1 — UptimeRobot
#### F8.2 — Backup Verification
#### F8.3 — Sentry

**Текущая позиция:** Фаза 1 завершена ✅ → Следующая: F2.1

## Обязательные действия после каждой задачи

После завершения КАЖДОЙ задачи выполни:

1. GIT COMMIT + PUSH:
   cd /opt/gg-hookah-v2 && git add . && git commit -m "описание" && git push

2. ОБНОВИТЬ CURRENT_TASK.md:
   - Отметить выполненные подзадачи (✅)
   - Если задача завершена — статус DONE, предложить следующую

3. ОБНОВИТЬ BUGS.md (если актуально):
   - Новый баг обнаружен → добавить в "Открытые"
   - Баг исправлен → удалить из файла полностью

4. КРАТКИЙ ОТЧЁТ пользователю

Правила чистоты:
- НЕ создавать новые .md файлы в корне проекта без согласия пользователя
- НЕ хранить временные/отладочные файлы
- НЕ дублировать информацию между файлами
- Три файла документации: CLAUDE.md, CURRENT_TASK.md, BUGS.md — и ВСЁ
