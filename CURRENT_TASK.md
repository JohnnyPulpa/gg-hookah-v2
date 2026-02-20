# CURRENT_TASK.md

## F1.4: Users Table Integration + Language Sync — DONE ✅

### What was done
1. **Backend (`backend/app.py`)** — added 3 new endpoints:
   - `GET /api/user/language?telegram_id=X` — returns user's language preference (default: "ru")
   - `POST /api/user/language` — upserts user language (creates user if missing)
   - `POST /api/user/ensure` — upserts user record with telegram data
2. **Mini App (`miniapp/src/api/client.ts`)** — added `getTelegramId()` and `getTelegramUser()` shared helpers
3. **Mini App (`miniapp/src/api/user.ts`)** — new API module: `getUserLanguage()`, `setUserLanguage()`, `ensureUser()`
4. **Mini App (`miniapp/src/contexts/LanguageContext.tsx`)** — full server sync:
   - On mount: calls `ensureUser()` (fire-and-forget) + loads language from server
   - On toggle: persists to both localStorage and server (fire-and-forget)
5. **Mini App** — `Checkout.tsx` and `Orders.tsx` now use shared `getTelegramId()` helper

### Files created
- `miniapp/src/api/user.ts`

### Files modified
- `backend/app.py`
- `miniapp/src/api/client.ts`
- `miniapp/src/contexts/LanguageContext.tsx`
- `miniapp/src/pages/Checkout.tsx`
- `miniapp/src/pages/Orders.tsx`

### Verified
- API endpoints tested with curl ✅
- `GET /api/user/language?telegram_id=111222333` → `{"language":"ru"}` ✅
- `POST /api/user/language` with `{"telegram_id":111222333,"language":"en"}` → `{"ok":true,"language":"en"}` ✅
- `POST /api/user/ensure` → `{"ok":true}` ✅
- `npm run build` — no TypeScript errors ✅
- Deployed to production ✅
- API service restarted and active ✅

## Статус: DONE

## Следующая задача: уточнить у пользователя
