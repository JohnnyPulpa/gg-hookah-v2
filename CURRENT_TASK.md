# CURRENT_TASK.md

## F2.5: Multi-hookah Orders (Cart) — DONE ✅

### What was done

1. **Backend: Settings + DB constraint**
   - Added settings: `total_hookahs=5`, `max_hookahs_regular=3`, `max_hookahs_event=5`
   - Relaxed DB constraint `ck_orders_hookah_count` from `BETWEEN 1 AND 3` → `BETWEEN 1 AND 10`
   - Updated model to match

2. **Backend: GET /api/availability**
   - Returns `{ available, max_per_order, total }`
   - Available = total_hookahs - SUM(hookah_count) from active orders
   - max_per_order = min(max_hookahs_regular, available)

3. **Backend: POST /api/orders — multi-item support**
   - Accepts `items: [{mix_id, quantity}]` array
   - Backward compatible: falls back to single `mix_id` if `items` absent
   - Validates each mix (exists, active), checks total vs availability
   - Sets `orders.hookah_count` = sum of quantities
   - Sets `orders.mix_id` = first item's mix_id (backward compat)
   - Inserts multiple hookah order_items
   - Discount applies per-hookah: `(base - discount%) * quantity`

4. **Frontend: CartContext** (new file)
   - Provides: items, drinks, addItem, removeItem, clearCart, setDrinks, clearDrinks
   - Fetches /api/availability on mount
   - Tracks totalHookahs, totalPrice, maxHookahs, availableHookahs, soldOut

5. **Frontend: FloatingCartBar** (new component)
   - Fixed above bottom nav (bottom: 76px)
   - Shows hookah count + price + "Next →"
   - Orange gradient, white text

6. **Frontend: MixCard** — [- qty +] counter
   - quantity=0: "Add" button
   - quantity>0: [- qty +] counter with orange border
   - maxReached disables + button

7. **Frontend: Catalog** — cart-aware
   - Uses CartContext, shows FloatingCartBar
   - Shows "All hookahs busy" when soldOut=true
   - Shows "Maximum reached" hint

8. **Frontend: DrinksQuestion, DrinksCatalog, Checkout** — all use CartContext
   - No more location.state passing
   - Checkout shows all hookah items with quantities
   - Sends `items[]` payload to API
   - Clears cart after success

9. **Frontend: Orders** — multi-hookah display
   - Active order shows all hookah items (not just primary mix)
   - History shows all hookah items per order

10. **Translations** — 5 new keys: cart_add, cart_next, cart_all_busy, cart_all_busy_sub, cart_max_reached

### Files created
- `miniapp/src/contexts/CartContext.tsx`
- `miniapp/src/components/FloatingCartBar.tsx`

### Files modified
- `backend/app.py` — availability endpoint + multi-item order creation
- `backend/models.py` — relaxed hookah_count constraint
- `backend/seed_settings.py` — 3 new settings
- `miniapp/src/App.tsx` — wrapped with CartProvider
- `miniapp/src/api/orders.ts` — getAvailability + updated payload
- `miniapp/src/components/MixCard.tsx` — quantity counter
- `miniapp/src/pages/Catalog.tsx` — cart integration
- `miniapp/src/pages/Checkout.tsx` — multi-item checkout
- `miniapp/src/pages/DrinksCatalog.tsx` — cart context
- `miniapp/src/pages/DrinksQuestion.tsx` — cart context
- `miniapp/src/pages/Orders.tsx` — multi-hookah display
- `miniapp/src/utils/translations.ts` — cart keys

### Verified
- `npm run build` ✅ — no errors
- Backend restarted ✅ — GET /api/availability returns correct data
- Miniapp deployed to production ✅
- Git committed and pushed ✅

## Статус: DONE

## Следующая задача: Фаза 3 — F3.1 Admin Dashboard (полный редизайн)
