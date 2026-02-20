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
