# CLAUDE.md

Руководство для Claude Code при работе с кодом в этом репозитории.

## Project Overview

GG Hookah v2 — Telegram Mini App для доставки и аренды кальянов в Батуми, Грузия.
Домен: gghookah.delivery. Репо: github.com/JohnnyPulpa/gg-hookah-v2

## Контекст бизнеса

Владелец работает ОДИН (доставка, сборка, поддержка). 5 кальянов на старте.
Система проектируется для масштабирования (курьеры, партнёры), но реализуется поэтапно.
Два типа заказов: regular (1-3 кальяна, сразу) и event (3-5 кальянов, предзаказ).

## Architecture

Четыре сервиса в монорепо:

| Service | Stack | Port | Path |
|---------|-------|------|------|
| Flask API | Python/Flask | 5001 | /opt/gg-hookah-v2/backend/ |
| Admin Panel | Flask/Jinja2 | 5002 | /opt/gg-hookah-v2/admin/ |
| Telegram Bot | Python/aiogram | polling | /opt/gg-hookah-v2/bot/ |
| Mini App | React/TypeScript/Vite | — | /opt/gg-hookah-v2/miniapp/ |

Nginx reverse proxy: API → /api/*, Admin → /admin/*, Mini App → /app/*
PostgreSQL: БД gg_hookah, доступ через sudo -u postgres psql -d gg_hookah
Secrets: /etc/gg-hookah/.env (НЕ читать, НЕ коммитить)
Deploy Mini App: npm run build → /var/www/gghookah.delivery/app/
Venv: /opt/gg-hookah-v2/venv/

## URL структура
gghookah.delivery          → Landing page (сайт-витрина, F5.6)
gghookah.delivery/app      → Telegram Mini App (только через TG)
gghookah.delivery/admin    → Admin Panel

## БД — Ключевые таблицы и gotchas

Существующие: orders, menu_items, drinks, guests, sessions, settings, audit_log, support_messages, users
- orders: НЕТ колонки total_amount (считать через menu_items.price_gel)
- guests: колонка name (НЕ first_name)
- menu_items: колонка price_gel (НЕ price)

Новые таблицы (создавать через alembic миграции):
- order_items: order_id, mix_id, quantity, price_gel
- hookahs: id, name, status (available/rented/maintenance), current_order_id, notes
- reviews: id, order_id, telegram_id, rating (1-5), comment, created_at

Новые поля в orders:
- hookah_count INTEGER DEFAULT 1
- order_type VARCHAR(20) DEFAULT 'regular' (regular/event)
- event_type VARCHAR(30) (birthday/corporate/party/other)
- event_date TIMESTAMP
- event_guest_count INTEGER
- prepayment_amount NUMERIC(10,2)
- prepayment_status VARCHAR(20) DEFAULT 'none' (none/pending/paid/refunded)

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

---

## ТЕКУЩИЙ ПЛАН РАБОТЫ

Выполняй задачи по порядку внутри фазы. После каждой — коммит, обновление CURRENT_TASK.md и BUGS.md, краткий отчёт. Затем СПРОСИ: "Переходим к следующей задаче?"

---

### ФАЗА 1: ФУНДАМЕНТ ✅
- F1.1 ✅ Admin Template Inheritance
- F1.2 ✅ Notification Service (Admin → Bot)
- F1.3 ✅ Session Timer Cron
- F1.4 ✅ Users table + Language sync

---

### ФАЗА 2: КЛИЕНТСКИЙ ОПЫТ

**F2.1 — Bot Hot Actions: Cancel, Ready for Pickup**
- Inline кнопки в Telegram под сообщением о заказе
- Cancel: только до DELIVERED (после — через support)
- Ready for Pickup: клиент сигнализирует что закончил раньше
- Admin получает уведомление через notification service
- Файлы: bot/handlers/order_actions.py

**F2.2 — Bot Hot Actions: Free +1h, Rebowl Request**
- Free +1h: session_ends_at += 1 hour (доступно 1 раз за сессию)
- Rebowl: REQUEST → CONFIRMED → IN_PROGRESS → DONE
- Недоступно после 02:00 (Asia/Tbilisi)
- Файлы: bot/handlers/session_actions.py

**F2.3 — Support Routing**
- Клиент пишет боту → сохраняется в support_messages
- thread_type: order, session, general
- Автоответ: "Получили, ответим в течение 15 минут"
- Файлы: bot/handlers/support.py

**F2.4 — Mini App: Active Order Actions**
- На странице Orders: кнопки Cancel, Ready for Pickup
- Вызывают API → notify → бот уведомляет admin
- Файлы: miniapp/src/pages/Orders.tsx

**F2.5 — Multi-hookah Orders (корзина)**
- Новая таблица order_items (order_id, mix_id, quantity, price_gel)
- Новые поля в orders: hookah_count, order_type
- Убрать ограничение 1 кальян — счётчик [- 1 +] на странице микса
- Корзина поддерживает разные миксы
- Floating cart bar внизу экрана: "🛒 2 кальяна • ₾150 [Далее →]"
- Checkout показывает все позиции с ценами
- API: GET /api/availability → { available: N, max_per_order: N }
- Лимит из settings.max_hookahs_regular (default 3)
- Если available = 0 → показать "Все кальяны заняты"
- Файлы: миграция, backend/routes/orders.py, miniapp (Catalog, Cart, Checkout)

---

### ФАЗА 3: ADMIN ПАНЕЛЬ — ОПЕРАЦИИ

**F3.1 — Admin Dashboard (полный редизайн главной)**
- Виджеты: Live Orders, Today Revenue (₾), Total Orders Today, Active Sessions, Available Hookahs (X/5)
- Kanban-доска активных заказов (карточки по колонкам статусов: NEW → CONFIRMED → ON_WAY → DELIVERED → SESSION → PICKUP)
- Quick actions прямо из карточек (Accept, Ship, Deliver)
- Звуковое уведомление при новом заказе (JS Audio + browser notification)
- Revenue bar chart за 7 дней
- Top mixes pie chart
- Alerts: overdue sessions, low trust guests, events завтра
- Файлы: admin/routes/dashboard.py, admin/templates/dashboard.html, admin/static/js/dashboard.js

**F3.2 — Settings Editor**
- CRUD для таблицы settings
- Группировка: Business Hours, Pricing, Delivery, Inventory, Events, Notifications
- Новые settings:
  - total_hookahs: 5
  - max_hookahs_regular: 3
  - max_hookahs_event: 5
  - event_min_hookahs: 3
  - event_min_advance_hours: 24
  - event_prepayment_percent: 50
  - delivery_estimate_min: 30
  - delivery_estimate_max: 60
  - delivery_estimate_busy: 90
  - first_order_discount: 15
  - first_order_promo_code: "WELCOME"
- Валидация типов (number, text, boolean, json)
- Файлы: admin/routes/settings.py, admin/templates/settings.html

**F3.3 — Guests Management (CRM)**
- Список с поиском и фильтрами
- Карточка гостя: имя, telegram, trust level (🟢🟡🔴), passport status
- История заказов гостя, total spend, количество заказов, любимый микс
- Notes (заметки от admin)
- Файлы: admin/routes/guests.py, admin/templates/guests_*.html

**F3.4 — Discounts & Promo Codes**
- Issue/withdraw скидку гостю
- CRUD промокодов: код, тип скидки (% или фикс), срок действия, лимит использований
- Файлы: admin/routes/discounts.py

**F3.5 — Support Inbox**
- Priority (привязанные к заказу/сессии) и General
- Непрочитанные — badge в sidebar
- Ответ из admin → уходит клиенту через бота
- Файлы: admin/routes/support.py

**F3.6 — Logs & System**
- Audit log viewer с фильтрами
- Service status (api, admin, bot)
- Файлы: admin/routes/system.py

**F3.7 — Reviews Management**
- Таблица reviews (order_id, telegram_id, rating 1-5, comment, created_at)
- После статуса COMPLETED → бот отправляет запрос оценки (inline ⭐1-5)
- Опционально текстовый отзыв
- Admin: страница с отзывами, фильтр по рейтингу
- Dashboard виджет: "Средний рейтинг: 4.8 ⭐ (47 оценок)"
- Файлы: миграция, bot/handlers/reviews.py, admin/routes/reviews.py

**F3.8 — Event Orders Management**
- Фильтр Regular / Event в списке заказов
- Детали event: дата, тип, кол-во гостей, предоплата
- Calendar view (или простой список предстоящих events)
- Alert за 4 часа до event в Telegram
- Статусы event: EVENT_PENDING → EVENT_CONFIRMED → EVENT_PREPAID → обычный flow
- Файлы: admin/routes/events.py, admin/templates/events.html

---

### ФАЗА 4: ПОЛИРОВКА + PRODUCTION

**F4.1 — Telegram initData Validation**
- Все API запросы из Mini App проверяют подпись Telegram
- Без валидной подписи → 401
- Файлы: backend/middleware/telegram_auth.py

**F4.2 — Mini App UX Polish**
- Skeleton loader вместо "загрузка миксов"
- Pull-to-refresh
- Haptic feedback (Telegram WebApp API)
- Файлы: miniapp компоненты

**F4.3 — Dynamic Discount Banner**
- Баннер берёт данные из API /api/settings/discount

**F4.4 — Error Handling & Edge Cases**
- Fallback если бот не отвечает
- Если available = 0 → блокировать заказ
- Timeout на все HTTP запросы
- Graceful degradation

**F4.5 — E2E Testing**
- QA checklist: заказ → подтверждение → доставка → сессия → pickup → завершение

**F4.6 — UX Flow Simplification**
- УБРАТЬ экран "Drinks question" — перенести напитки в Checkout (chip buttons: Cola +₾5, Sprite +₾5, Вода free)
- Home: горизонтальный scroll популярных миксов (swipe карточки)
- Home: "Повторить последний заказ" для пользователей с историей (GET /api/user/last-order)
- Checkout: автозаполнение имени/телефона из Telegram WebApp.initDataUnsafe.user
- Checkout: сохранение адреса в users.last_address (заполняется автоматически в следующий раз)
- Промокод спрятать за "Есть промокод? →"
- Catalog: фильтры-tabs (Все, Сладкие, Свежие, Крепкие) — на основе тегов миксов

**F4.7 — Visual Upgrade**
- Gradient blobs для каждого микса (CSS linear-gradient по цветам вкуса, не картинки)
- Уменьшить маскот на Home до 30%, интегрировать в hero section
- Fade-in анимации при скролле (Intersection Observer)
- Шрифт заголовков: Outfit (Google Fonts), body остаётся Nunito
- Subtle smoke effect в hero (CSS animation)
- Empty states для Orders, Support (маскот + CTA)
- Social proof: "340+ сессий в Батуми" (или реальное число из БД)

**F4.8 — Dark Theme**
- CSS variables для light/dark
- Auto-detect: window.Telegram.WebApp.colorScheme
- Тёмные тона: #1A0F0A bg, #2C1810 cards, amber glow accents

**F4.9 — Splash Screen**
- SplashScreen.tsx: маскот + "GG HOOKAH" + loading dots
- Показывать минимум 1.5 секунды (даже если данные загружены)
- Фон: brand color (тёмно-зелёный или кремовый)
- После загрузки: window.Telegram.WebApp.ready()

**F4.10 — Dynamic Delivery Estimate**
- API: GET /api/delivery-estimate
- Логика: считает активные заказы (CONFIRMED + ON_THE_WAY + DELIVERED + SESSION_ACTIVE)
  - 0 активных → settings.delivery_estimate_min — delivery_estimate_max мин
  - 1-2 активных → delivery_estimate_busy мин
  - 3+ активных → "Ближайшее окно: ~XX:XX"
- Показывать в Checkout: "🚗 Доставим за ~30-60 мин"
- НЕ показывать на Home (там "Вечер начинается здесь" без времени)

**F4.11 — First Order Discount**
- Если у пользователя 0 completed orders → автоприменить скидку из settings.first_order_discount (15%)
- Промокод WELCOME: можно ввести вручную, результат тот же
- Баннер на Home: "🎁 -15% на первый заказ • WELCOME" — видим ТОЛЬКО если 0 заказов
- Файлы: backend (проверка), miniapp (баннер, checkout)

**F4.12 — /app Route Protection**
- Nginx: если запрос к /app не из Telegram (нет tgWebAppData) → показать страницу:
  "Это приложение работает только в Telegram"
  + кнопка "Открыть в Telegram" → t.me/gghookah_bot?start=app
- Простая HTML-страница, не React

---

### ФАЗА 5: ИНВЕНТАРЬ, ФИНАНСЫ, ЛЕНДИНГ (POST-MVP)

**F5.1 — Hookahs Asset Tracking**
- Таблица hookahs: 5 записей (Hookah #1...#5)
- Status: available / rented / maintenance
- При CONFIRMED → автоназначить N свободных кальянов (hookah.status='rented', hookah.current_order_id=order.id)
- При COMPLETED → освободить (status='available', current_order_id=NULL)
- Admin: список кальянов, история аренд, кнопка "На обслуживание"
- Dashboard виджет: "🎯 Кальяны: 3/5 доступно"
- API /api/availability использует реальные данные из hookahs

**F5.2 — Consumables (расходники)**
- Таблица consumables (name, unit, quantity, low_threshold, category)
- Категории: Табак (по вкусам), Уголь, Шланги, Чаши, Мундштуки
- Alert при low_threshold
- Admin: CRUD, списание

**F5.3 — Financial Dashboard**
- Revenue: today / week / month / custom range
- Средний чек, заказов в день, revenue per hookah
- Top mixes по выручке
- Расходы (ручной ввод)
- Profit = Revenue - Expenses
- Export CSV

**F5.4 — Delivery Zones**
- Таблица delivery_zones (name, polygon_coords, delivery_fee, estimated_minutes)
- Зона 1 центр: 0₾, 20 мин. Зона 2: 5₾, 30 мин. Зона 3: 10₾, 45 мин
- Admin: карта Батуми (Leaflet.js)
- Mini App: показывать зону и стоимость

**F5.5 — Mascot v2**
- Маленькая версия для header (24px icon)
- Hero section, Splash screen, Empty states, Error states
- Брендинг: favicon, Telegram bot avatar

**F5.6 — Landing Page**
- Одностраничник на gghookah.delivery (без /app)
- Цель: SEO + конверсия в Telegram
- Содержание: hero с атмосферой, "Как это работает" (3 шага), меню миксов (без заказа), отзывы, FAQ, часы работы
- Одна CTA: "Заказать в Telegram" → t.me/gghookah_bot?start=web
- Мультиязычность: RU / EN / KA
- SEO: "кальян доставка Батуми", "hookah delivery Batumi"
- Технически: статический HTML/CSS или простой React, deploy в /var/www/gghookah.delivery/

**F5.7 — Google Maps Review Flow**
- После оценки 4-5 ⭐ в боте → сообщение: "Спасибо! Оставьте отзыв на Google Maps 🙏" + ссылка
- Не навязывать, показывать 1 раз после каждого хорошего отзыва

---

### ФАЗА 6: МАСШТАБИРОВАНИЕ — КОМАНДА

**F6.1 — Delivery Staff Management**
- Таблица delivery_staff (telegram_id, name, phone, status: active/on_delivery/offline)
- Назначение курьера на заказ (order.assigned_staff_id)
- Уведомление курьеру в Telegram

**F6.2 — Courier Bot Flow**
- Курьер видит свои заказы, кнопки: "Забрал", "Доставил", "Забрал обратно"
- Фото-подтверждение доставки

**F6.3 — Staff Analytics**
- Заказов за смену, среднее время, рейтинг

**F6.4 — Role-Based Access**
- Роли: owner / manager / operator
- Middleware проверки в admin routes

**F6.5 — Multi-channel Notifications**
- Firebase push для курьеров
- SMS fallback
- Email ежедневная сводка

---

### ФАЗА 7: GROWTH — НОВЫЕ КАНАЛЫ

**F7.1 — Event Booking (полный flow)**
- Кнопка "🎉 Кальян на мероприятие" на Home
- Event flow в Mini App:
  1. Тип (день рождения / корпоратив / вечеринка / другое)
  2. Дата + время (минимум за 24ч, DatePicker)
  3. Адрес, кол-во гостей
  4. Кол-во кальянов (3-5, settings.max_hookahs_event)
  5. Выбор микса для каждого кальяна
  6. Итого + предоплата 50%
  7. "Отправить заявку"
- Статусы: EVENT_PENDING → EVENT_CONFIRMED → EVENT_PREPAID → далее обычный flow
- Admin подтверждает/отклоняет заявку
- При подтверждении → клиент получает payment link
- Calendar в admin с предстоящими events
- Alert за 4 часа до event

**F7.2 — Loyalty Program**
- Баллы: 1₾ = 1 point. Уровни: Bronze/Silver/Gold
- Реферальный код

**F7.3 — Hotel Partnerships**
- Отдельный вход /partner, комиссия 10-15%, QR для гостей

**F7.4 — Payment Integration**
- BOG iPay / TBC Pay, payment link в боте

**F7.5 — Advanced Analytics**
- Прогноз спроса, heatmap, CLV, churn prediction

---

### ФАЗА 8: МОНИТОРИНГ (параллельно)

**F8.1 — UptimeRobot** — мониторинг endpoints, alert в Telegram
**F8.2 — Backup Verification** — проверка бэкапов, копия на Cloudflare R2
**F8.3 — Sentry** — error logging Python + JavaScript

---

## Текущая позиция: Фаза 1 завершена ✅ → Следующая: F2.1
