# BUGS & TODO

Формат: добавляй новые баги сверху. Решённые — удаляй полностью.

## Открытые

### B17 — Скидка 15% hardcoded на Home
- Где: miniapp/src/pages/Home.tsx
- Нужно: подключить к API /api/settings/discount
- Когда: F4.3

### B19 — Маскот не идеально вписывается
- Где: miniapp/src/pages/Home.tsx
- Нужно: заменить на GIF или оптимизировать размер
- Когда: F4.2

### B20 — Маскот занимает много места в Telegram WebApp
- Где: miniapp/src/pages/Home.tsx
- Нужно: уменьшить или скрыть на маленьких экранах
- Когда: F4.2

### B21 — Видна страница "загрузка миксов"
- Где: miniapp/src/pages/Catalog.tsx
- Нужно: skeleton loader
- Когда: F4.2

### B15 — telegram_id=0 вне Telegram
- Где: miniapp/src/App.tsx
- Нужно: заказы только внутри Telegram Mini App
- Когда: F4.1
