# BUGS & TODO

Формат: новые баги добавляй сверху. Решённые — удаляй полностью.

## Открытые

### B17 — Скидка 15% hardcoded на Home
- Где: miniapp/src/pages/Home.tsx
- Нужно: подключить к API /api/settings/discount
- Когда: F4.11

### B19 — Маскот не идеально вписывается
- Где: miniapp/src/pages/Home.tsx
- Когда: F5.5

### B20 — Маскот занимает много места в Telegram WebApp
- Где: miniapp/src/pages/Home.tsx
- Когда: F4.7

### B21 — Видна страница "загрузка миксов"
- Где: miniapp/src/pages/Catalog.tsx
- Нужно: skeleton loader или splash screen
- Когда: F4.9

### B15 — telegram_id=0 вне Telegram
- Где: miniapp/src/App.tsx
- Нужно: заказы только внутри Telegram Mini App
- Когда: F4.1
