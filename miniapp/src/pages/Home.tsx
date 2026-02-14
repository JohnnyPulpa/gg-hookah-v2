import { useNavigate } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';

export default function Home() {
  const navigate = useNavigate();
  const { language } = useLanguageContext();

  // TODO: load from API / settings
  const hasActiveDiscount = false;
  const discountPercent = 10;
  const discountValidUntil = '15.02';
  const boardGamesAvailable = true;

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      {/* Hero section with CTA */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
        <div className="mb-6">
          <div className="text-6xl mb-4">🌿</div>
          <h1 className="text-3xl font-bold text-orange-500 mb-2">
            {t('home_title', language)}
          </h1>
          <p className="text-gray-500">
            {t('home_working_hours', language)}
          </p>
        </div>
        <button
          onClick={() => navigate('/catalog')}
          className="bg-orange-500 hover:bg-orange-600 text-white font-bold text-lg px-8 py-4 rounded-xl transition-colors"
        >
          {t('home_order_button', language)}
        </button>
      </div>

      {/* Active discount banner */}
      {hasActiveDiscount && (
        <div className="bg-gradient-to-r from-orange-50 to-orange-100 border-2 border-orange-500 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="inline-block bg-orange-100 text-orange-700 text-xs font-semibold px-2 py-1 rounded mb-2">
                🎉 {language === 'ru' ? 'Активная скидка' : 'Active Discount'}
              </span>
              <p className="font-medium">
                {t('home_discount_banner', language)
                  .replace('{}', discountPercent.toString())
                  .replace('{}', discountValidUntil)}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {language === 'ru' ? 'Только для кальяна' : 'Hookah only'}
              </p>
            </div>
            <div className="text-4xl">🔥</div>
          </div>
        </div>
      )}

      {/* Mix of the Week */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-xl font-bold">
            {t('home_mix_of_week', language)}
          </h2>
          <span className="bg-green-100 text-green-700 text-xs font-semibold px-2 py-1 rounded">
            ⭐ Featured
          </span>
        </div>
        <div className="bg-gradient-to-br from-orange-50 to-green-50 rounded-lg p-4 mb-3">
          <div className="flex items-center gap-4">
            <div className="text-5xl">🍋🍃</div>
            <div className="flex-1">
              <h3 className="font-bold text-lg">Lemon Mint</h3>
              <p className="text-sm text-gray-500">
                {language === 'ru' ? 'Освежающий лимон с мятой' : 'Refreshing lemon with mint'}
              </p>
            </div>
          </div>
        </div>
        <button
          onClick={() => navigate('/catalog')}
          className="w-full border-2 border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-white font-semibold py-2 rounded-xl transition-colors"
        >
          {t('catalog_choose', language)}
        </button>
      </div>

      {/* Board games promo */}
      {boardGamesAvailable && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-100 border border-green-600 rounded-xl p-4">
          <div className="flex items-center gap-4">
            <div className="text-4xl">🎲</div>
            <div className="flex-1">
              <h3 className="font-semibold mb-1">
                {t('home_board_games', language)}
              </h3>
              <p className="text-sm text-gray-500">
                {language === 'ru'
                  ? 'Монополия, UNO, Мафия и другие'
                  : 'Monopoly, UNO, Mafia and more'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Navigation to orders */}
      <button
        onClick={() => navigate('/orders')}
        className="w-full text-gray-500 hover:text-orange-500 font-medium py-3 transition-colors"
      >
        {t('orders_title', language)} →
      </button>
    </div>
  );
}
