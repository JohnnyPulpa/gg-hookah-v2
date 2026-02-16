import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';
import { Drink } from '../types';
import { drinksApi } from '../api/drinks';

const MAX_TOTAL_DRINKS = 8;

const drinkEmojis: Record<string, string> = {
  'coca-cola': '🥤',
  'fanta': '🍊',
  'sprite': '🍋',
  'water': '💧',
  'juice apple': '🍎',
  'juice orange': '🍊',
};

function getDrinkEmoji(name: string): string {
  return drinkEmojis[name.toLowerCase()] || '🥤';
}

interface DrinkSelection {
  drink: Drink;
  qty: number;
}

export default function DrinksCatalog() {
  const navigate = useNavigate();
  const location = useLocation();
  const { language } = useLanguageContext();
  const selectedMix = location.state?.selectedMix;

  const [drinks, setDrinks] = useState<Drink[]>([]);
  const [selections, setSelections] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!selectedMix) {
      navigate('/catalog');
      return;
    }
    drinksApi
      .getAll()
      .then(setDrinks)
      .catch((err) => console.error('Failed to load drinks:', err))
      .finally(() => setLoading(false));
  }, []);

  const totalQty = Object.values(selections).reduce((sum, q) => sum + q, 0);
  const totalPrice = Object.entries(selections).reduce((sum, [id, qty]) => {
    const drink = drinks.find((d) => d.id === id);
    return sum + (drink ? drink.price * qty : 0);
  }, 0);

  const updateQty = (drinkId: string, delta: number) => {
    setSelections((prev) => {
      const current = prev[drinkId] || 0;
      const next = current + delta;
      if (next < 0) return prev;
      if (totalQty + delta > MAX_TOTAL_DRINKS) return prev;
      const updated = { ...prev, [drinkId]: next };
      if (updated[drinkId] === 0) delete updated[drinkId];
      return updated;
    });
  };

  const handleContinue = () => {
    const selectedDrinks: DrinkSelection[] = Object.entries(selections)
      .filter(([, qty]) => qty > 0)
      .map(([id, qty]) => ({
        drink: drinks.find((d) => d.id === id)!,
        qty,
      }));
    navigate('/checkout', { state: { selectedMix, selectedDrinks } });
  };

  if (!selectedMix) return null;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center" style={{ paddingTop: 60 }}>
        <div style={{ fontSize: 40, marginBottom: 12 }}>⏳</div>
        <p style={{ color: 'var(--text-muted)', fontWeight: 600 }}>
          {language === 'ru' ? 'Загрузка...' : 'Loading...'}
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      {/* Max drinks hint */}
      <div
        style={{
          textAlign: 'center',
          fontSize: 12,
          color: 'var(--text-muted)',
          fontWeight: 600,
          marginBottom: 12,
        }}
      >
        {t('drinks_max', language)}
      </div>

      {/* Drinks list */}
      <div className="flex flex-col" style={{ gap: 10 }}>
        {drinks.map((drink) => {
          const qty = selections[drink.id] || 0;
          return (
            <div
              key={drink.id}
              style={{
                background: 'var(--bg-card)',
                borderRadius: 'var(--radius)',
                padding: '14px 16px',
                boxShadow: 'var(--shadow)',
                border: '1px solid var(--border)',
                display: 'flex',
                alignItems: 'center',
                gap: 12,
              }}
            >
              <div style={{ fontSize: 32, flexShrink: 0 }}>{getDrinkEmoji(drink.name)}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 15, fontWeight: 700, color: 'var(--text)' }}>
                  {drink.name}
                </div>
                <div style={{ fontSize: 13, color: 'var(--orange)', fontWeight: 800 }}>
                  {drink.price}₾
                </div>
              </div>
              {/* Qty control */}
              <div
                className="flex items-center"
                style={{
                  background: 'var(--bg-input)',
                  borderRadius: 'var(--radius-sm)',
                  border: '1.5px solid var(--border)',
                  overflow: 'hidden',
                }}
              >
                <button
                  onClick={() => updateQty(drink.id, -1)}
                  disabled={qty === 0}
                  style={{
                    width: 36,
                    height: 36,
                    background: 'transparent',
                    border: 'none',
                    fontSize: 18,
                    fontWeight: 800,
                    color: qty > 0 ? 'var(--orange)' : 'var(--text-muted)',
                    cursor: qty > 0 ? 'pointer' : 'default',
                    fontFamily: "'Nunito', sans-serif",
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  −
                </button>
                <span
                  style={{
                    width: 28,
                    textAlign: 'center',
                    fontSize: 15,
                    fontWeight: 800,
                    color: 'var(--text)',
                  }}
                >
                  {qty}
                </span>
                <button
                  onClick={() => updateQty(drink.id, 1)}
                  disabled={totalQty >= MAX_TOTAL_DRINKS}
                  style={{
                    width: 36,
                    height: 36,
                    background: 'transparent',
                    border: 'none',
                    fontSize: 18,
                    fontWeight: 800,
                    color: totalQty < MAX_TOTAL_DRINKS ? 'var(--orange)' : 'var(--text-muted)',
                    cursor: totalQty < MAX_TOTAL_DRINKS ? 'pointer' : 'default',
                    fontFamily: "'Nunito', sans-serif",
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  +
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Total */}
      {totalQty > 0 && (
        <div
          className="flex justify-between"
          style={{
            margin: '16px 0 12px',
            padding: '12px 16px',
            background: 'var(--bg-input)',
            borderRadius: 'var(--radius-sm)',
            fontSize: 14,
            fontWeight: 700,
            color: 'var(--text)',
          }}
        >
          <span>
            {t('drinks_total', language)} ({totalQty}{' '}
            {language === 'ru' ? 'шт' : 'pcs'})
          </span>
          <span style={{ color: 'var(--orange)', fontWeight: 800 }}>{totalPrice}₾</span>
        </div>
      )}

      {/* Next button */}
      <button
        className="btn-primary"
        onClick={handleContinue}
        style={{ marginTop: totalQty > 0 ? 0 : 16 }}
      >
        {t('drinks_next', language)}
      </button>
    </div>
  );
}