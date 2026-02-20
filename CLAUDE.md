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
Владелец пока работает один (доставка, сборка, поддержка). Система должна быть спроектирована для масштабирования (курьеры, партнёры), но реализована поэтапно.

## Текущий план работы

Выполняй задачи по порядку внутри фазы. После каждой — коммит, обновление CURRENT_TASK.md и CURRENT_STATE.md, краткий отчёт. Затем СПРОСИ пользователя: "Переходим к следующей задаче?"

### ФАЗА 1: ФУНДАМЕНТ ✅

- F1.1 ✅ Admin Template Inheritance
- F1.2 ✅ Notification Service (Admin → Bot)
- F1.3 ✅ Session Timer Cron
- F1.4 ✅ Users table + Language sync

### ФАЗА 2: КЛИЕНТСКИЙ ОПЫТ (~3-4 дня)

- F2.1 — Bot Hot Actions: Cancel, Ready for Pickup (inline кнопки в Telegram, admin получает уведомление)
- F2.2 — Bot Hot Actions: Free +1h, Rebowl Request (session_ends_at += 1h, rebowl pipeline: REQUEST→CONFIRMED→IN_PROGRESS→DONE, недоступно после 02:00)
- F2.3 — Support Routing (сообщения клиента → support_messages, thread_type: order/session/general)
- F2.4 — Mini App: Active Order Actions (кнопки Cancel, Ready for Pickup в Orders.tsx)

### ФАЗА 3: ADMIN ПАНЕЛЬ — ОПЕРАЦИИ (~3-4 дня)

- F3.1 — Admin Dashboard Redesign: виджеты (live orders, revenue today, active sessions, available hookahs), Kanban-доска заказов (карточки по колонкам статусов), quick actions из карточек, звук при новом заказе, revenue chart 7 дней, top mixes chart, alerts
- F3.2 — Settings Editor: CRUD для таблицы settings, группировка по категориям
- F3.3 — Guests Management (CRM): список с фильтрами, карточка гостя (trust level, history, total spend, любимый микс, notes, passport upload)
- F3.4 — Discounts & Promo Codes: issue/withdraw скидки, create promo code
- F3.5 — Support Inbox: Priority + General, непрочитанные badge, ответ через бота
- F3.6 — Logs & System: audit log viewer, service status page

### ФАЗА 4: ПОЛИРОВКА + PRODUCTION (~2-3 дня)

- F4.1 — Telegram initData Validation (проверка подписи, 401 без валидации)
- F4.2 — Mini App UX Polish (skeleton loader, маскот, pull-to-refresh, haptic feedback)
- F4.3 — Dynamic Discount Banner (из API вместо hardcoded -15%)
- F4.4 — Error Handling & Edge Cases
- F4.5 — E2E Testing (полный путь заказа по QA checklist)

### ФАЗА 5: ИНВЕНТАРЬ И ФИНАНСЫ (~4-5 дней) — POST-MVP

- F5.1 — Hookahs Asset Tracking: таблица hookahs (serial_number, status: available/rented/maintenance), привязка к заказам, dashboard виджет "Available: 7/12"
- F5.2 — Consumables: таблица consumables (табак, уголь, шланги), списание при заказе, alert при low_threshold
- F5.3 — Financial Dashboard: revenue (day/week/month), средний чек, top mixes по выручке, расходы (ручной ввод), profit P&L, export CSV
- F5.4 — Delivery Zones: таблица delivery_zones (polygon, fee, estimated_minutes), карта Батуми (Leaflet.js), Mini App показывает зону

### ФАЗА 6: МАСШТАБИРОВАНИЕ — КОМАНДА (~5-7 дней)

- F6.1 — Delivery Staff: таблица delivery_staff, назначение курьера на заказ, уведомление курьеру в Telegram
- F6.2 — Courier Bot: отдельный flow для курьера (мои заказы, "Забрал", "Доставил", фото-подтверждение)
- F6.3 — Staff Analytics: заказов за смену, среднее время, рейтинг
- F6.4 — Role-Based Access: owner/manager/operator, middleware проверки
- F6.5 — Multi-channel Notifications: Firebase push, SMS fallback, email отчёты

### ФАЗА 7: GROWTH — НОВЫЕ КАНАЛЫ (~5-7 дней)

- F7.1 — Event Booking: пакеты (3/5/10 кальянов), календарь, предоплата 50%
- F7.2 — Loyalty Program: баллы за заказы, уровни Bronze/Silver/Gold, реферальный код
- F7.3 — Hotel Partnerships: отдельный вход, комиссия 10-15%, QR для гостей
- F7.4 — Payment Integration: BOG iPay / TBC Pay, payment link в боте
- F7.5 — Advanced Analytics: прогноз спроса, heatmap, CLV, churn prediction

### ФАЗА 8: МОНИТОРИНГ (параллельно, по мере необходимости)

- F8.1 — UptimeRobot: мониторинг endpoints, alert в Telegram
- F8.2 — Backup Verification: проверка бэкапов, копия на Cloudflare R2
- F8.3 — Sentry: error logging для Python и JavaScript

**Текущая позиция:** Фаза 1 завершена ✅ → Следующая: F2.1

## Обязательные действия после каждой задачи

После завершения КАЖДОЙ задачи ты ОБЯЗАН выполнить эти шаги (даже если пользователь не просил):

1. GIT COMMIT + PUSH:
   cd /opt/gg-hookah-v2 && git add . && git commit -m "краткое описание изменений" && git push

2. ОБНОВИТЬ CURRENT_TASK.md:
   - Отметить выполненные подзадачи (✅)
   - Добавить заметки о том что было сделано
   - Если задача полностью завершена — написать "## Статус: DONE" и предложить следующую задачу

3. ОБНОВИТЬ GG_HOOKAH_CURRENT_STATE.md:
   - Добавить новые файлы в карту файлов
   - Обновить секцию "ЧТО СДЕЛАНО (по Milestones)"
   - Обновить список багов (исправленные — зачеркнуть)
   - Обновить "Последний коммит" и "Последние 10 коммитов"
   - Обновить секцию "РАБОЧИЕ URL" если добавились новые
   - Обновить "СЛЕДУЮЩИЙ ЧАТ — ПЛАН" с актуальным следующим шагом

4. КРАТКИЙ ОТЧЁТ пользователю:
   - Что сделано
   - Какие файлы созданы/изменены
   - Есть ли ошибки/warnings
   - Коммит хеш

Никогда не завершай работу без коммита и обновления документации!
