import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { Drink } from '../types';
import { drinksApi } from '../api/drinks';

const MAX_TOTAL_DRINKS = 8;

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
    loadDrinks();
  }, []);

  const loadDrinks = async () => {
    try {
      const data = await drinksApi.getAll();
      setDrinks(data);
    } catch (err) {
      console.error('Failed to load drinks:', err);
    } finally {
      setLoading(false);
    }
  };

  const totalQty = Object.values(selections).reduce((sum, q) => sum + q, 0);

  const updateQty = (drinkId: string, delta: number) => {
    setSelections(prev => {
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
      .filter(([_, qty]) => qty > 0)
      .map(([id, qty]) => ({
        drink: drinks.find(d => d.id === id)!,
        qty,
      }));
    navigate('/checkout', { state: { selectedMix, selectedDrinks } });
  };

  if (!selectedMix) return null;

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">⏳</div>
        <p>{language === 'ru' ? 'Загрузка...' : 'Loading...'}</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-orange-500 mb-2">
          {language === 'ru' ? 'Напитки' : 'Drinks'}
        </h1>
        <p className="text-gray-500">
          {language === 'ru'
            ? `Выбрано: ${totalQty} из ${MAX_TOTAL_DRINKS} макс.`
            : `Selected: ${totalQty} of ${MAX_TOTAL_DRINKS} max.`}
        </p>
      </div>

      {/* Drinks list */}
      <div className="space-y-3">
        {drinks.map((drink) => {
          const qty = selections[drink.id] || 0;
          return (
            <div key={drink.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">🥤</span>
                  <div>
                    <h3 className="font-semibold">{drink.name}</h3>
                    <p className="text-orange-500 font-bold">{drink.price}₾</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => updateQty(drink.id, -1)}
                    disabled={qty === 0}
                    className="w-10 h-10 rounded-full border-2 border-gray-300 flex items-center justify-center font-bold text-lg disabled:opacity-30 hover:border-orange-500 hover:text-orange-500 transition-colors"
                  >
                    −
                  </button>
                  <span className="w-8 text-center font-bold text-lg">{qty}</span>
                  <button
                    onClick={() => updateQty(drink.id, 1)}
                    disabled={totalQty >= MAX_TOTAL_DRINKS}
                    className="w-10 h-10 rounded-full border-2 border-gray-300 flex items-center justify-center font-bold text-lg disabled:opacity-30 hover:border-orange-500 hover:text-orange-500 transition-colors"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Continue button */}
      <button
        onClick={handleContinue}
        className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold text-lg py-4 rounded-xl transition-colors"
      >
        {totalQty > 0
          ? (language === 'ru' ? `Продолжить (${totalQty} напитков)` : `Continue (${totalQty} drinks)`)
          : (language === 'ru' ? 'Продолжить без напитков' : 'Continue without drinks')}
      </button>
    </div>
  );
}
