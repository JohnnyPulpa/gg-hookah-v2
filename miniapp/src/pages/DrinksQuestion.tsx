import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';

export default function DrinksQuestion() {
  const navigate = useNavigate();
  const location = useLocation();
  const { language } = useLanguageContext();
  const selectedMix = location.state?.selectedMix;

  if (!selectedMix) {
    navigate('/catalog');
    return null;
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Selected mix summary */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-500">{language === 'ru' ? 'Выбранный микс' : 'Selected mix'}</p>
            <h3 className="font-bold text-lg">{selectedMix.name}</h3>
            <p className="text-sm text-gray-500">{selectedMix.flavors}</p>
          </div>
          <div className="text-2xl font-bold text-orange-500">{selectedMix.price}₾</div>
        </div>
      </div>

      {/* Question */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
        <div className="text-5xl mb-4">🥤</div>
        <h1 className="text-2xl font-bold mb-2">
          {language === 'ru' ? 'Добавить напитки к заказу?' : 'Add drinks to your order?'}
        </h1>
        <p className="text-gray-500 mb-6">
          {language === 'ru'
            ? 'Напитки доставляются вместе с кальяном'
            : 'Drinks are delivered with the hookah'}
        </p>

        <div className="flex gap-4">
          <button
            onClick={() => navigate('/drinks', { state: { selectedMix } })}
            className="flex-1 bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 rounded-xl transition-colors text-lg"
          >
            {language === 'ru' ? 'Да' : 'Yes'}
          </button>
          <button
            onClick={() => navigate('/checkout', { state: { selectedMix, selectedDrinks: [] } })}
            className="flex-1 border-2 border-gray-300 hover:border-orange-500 text-gray-700 hover:text-orange-500 font-bold py-4 rounded-xl transition-colors text-lg"
          >
            {language === 'ru' ? 'Нет' : 'No'}
          </button>
        </div>
      </div>
    </div>
  );
}
