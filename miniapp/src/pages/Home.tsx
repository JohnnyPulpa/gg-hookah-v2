import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Card from '../components/Card';
import Badge from '../components/Badge';
import { useLanguage } from '../hooks/useLanguage';
import { t } from '../utils/translations';

export default function Home() {
  const navigate = useNavigate();
  const { language } = useLanguage();

  // Mock data - в будущем будет из API
  const hasActiveDiscount = false;
  const discountPercent = 10;
  const discountValidUntil = '15.02';
  const boardGamesAvailable = true;

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      {/* Hero section with CTA */}
      <Card className="text-center py-8">
        <div className="mb-6">
          <div className="text-6xl mb-4">🌿</div>
          <h1 className="text-3xl font-bold text-brand-orange mb-2">
            {t('home_title', language)}
          </h1>
          <p className="text-light-text-secondary dark:text-dark-text-secondary">
            {t('home_working_hours', language)}
          </p>
        </div>

        <Button 
          variant="primary" 
          onClick={() => navigate('/catalog')}
          className="text-lg px-8 py-4"
        >
          {t('home_order_button', language)}
        </Button>
      </Card>

      {/* Active discount banner */}
      {hasActiveDiscount && (
        <Card className="bg-gradient-to-r from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 border-2 border-brand-orange">
          <div className="flex items-center justify-between">
            <div>
              <Badge variant="warning" className="mb-2">
                🎉 {language === 'ru' ? 'Активная скидка' : 'Active Discount'}
              </Badge>
              <p className="font-medium">
                {t('home_discount_banner', language)
                  .replace('{}', discountPercent.toString())
                  .replace('{}', discountValidUntil)}
              </p>
              <p className="text-xs text-light-text-secondary dark:text-dark-text-secondary mt-1">
                {language === 'ru' ? 'Только для кальяна' : 'Hookah only'}
              </p>
            </div>
            <div className="text-4xl">🔥</div>
          </div>
        </Card>
      )}

      {/* Mix of the Week */}
      <Card>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-xl font-bold">
            {t('home_mix_of_week', language)}
          </h2>
          <Badge variant="success">⭐ Featured</Badge>
        </div>
        
        <div className="bg-gradient-to-br from-brand-orange/10 to-brand-green/10 rounded-lg p-4 mb-3">
          <div className="flex items-center gap-4">
            <div className="text-5xl">🍋🍃</div>
            <div className="flex-1">
              <h3 className="font-bold text-lg">Lemon Mint</h3>
              <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
                {language === 'ru' ? 'Освежающий лимон с мятой' : 'Refreshing lemon with mint'}
              </p>
            </div>
          </div>
        </div>

        <Button 
          variant="secondary" 
          onClick={() => navigate('/catalog')}
          className="w-full"
        >
          {t('catalog_choose', language)}
        </Button>
      </Card>

      {/* Board games promo */}
      {boardGamesAvailable && (
        <Card className="bg-gradient-to-r from-green-50 to-emerald-100 dark:from-green-900/20 dark:to-emerald-800/20 border border-brand-green">
          <div className="flex items-center gap-4">
            <div className="text-4xl">🎲</div>
            <div className="flex-1">
              <h3 className="font-semibold mb-1">
                {t('home_board_games', language)}
              </h3>
              <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
                {language === 'ru' 
                  ? 'Монополия, UNO, Мафия и другие'
                  : 'Monopoly, UNO, Mafia and more'}
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* Navigation to orders */}
      <Button 
        variant="ghost" 
        onClick={() => navigate('/orders')}
        className="w-full"
      >
        {t('orders_title', language)} →
      </Button>
    </div>
  );
}
