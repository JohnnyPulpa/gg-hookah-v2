import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';
import { t } from '../utils/translations';
import { DepositType } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';
import Checkbox from '../components/Checkbox';
import Badge from '../components/Badge';

export default function Checkout() {
  const navigate = useNavigate();
  const location = useLocation();
  const { language } = useLanguage();
  
  const selectedMix = location.state?.selectedMix;
  
  // Form state
  const [address, setAddress] = useState('');
  const [entrance, setEntrance] = useState('');
  const [floor, setFloor] = useState('');
  const [apartment, setApartment] = useState('');
  const [doorCode, setDoorCode] = useState('');
  const [phone, setPhone] = useState('');
  const [comment, setComment] = useState('');
  const [depositType, setDepositType] = useState<DepositType>('cash');
  const [promoCode, setPromoCode] = useState('');
  const [rulesAccepted, setRulesAccepted] = useState(false);
  
  // Mock: passport already on file
  const hasPassportOnFile = false;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!rulesAccepted) {
      alert(language === 'ru' ? 'Подтвердите согласие с правилами' : 'Please accept the rules');
      return;
    }
    
    // TODO: Send to backend API
    console.log('Order:', {
      mix: selectedMix,
      address,
      entrance,
      floor,
      apartment,
      doorCode,
      phone,
      comment,
      depositType,
      promoCode,
      rulesAccepted
    });
    
    // Navigate to success or orders
    alert(language === 'ru' ? 'Заказ создан!' : 'Order created!');
    navigate('/orders');
  };

  if (!selectedMix) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <div className="text-6xl mb-4">🤔</div>
        <h2 className="text-2xl font-bold mb-2">
          {language === 'ru' ? 'Микс не выбран' : 'No mix selected'}
        </h2>
        <p className="text-light-text-secondary dark:text-dark-text-secondary mb-6">
          {language === 'ru' 
            ? 'Пожалуйста, выберите микс из каталога'
            : 'Please choose a mix from the catalog'}
        </p>
        <Button onClick={() => navigate('/catalog')}>
          {language === 'ru' ? 'Перейти в каталог' : 'Go to catalog'}
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-brand-orange mb-2">
          {t('checkout_title', language)}
        </h1>
      </div>

      {/* Selected Mix Summary */}
      <Card>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold text-lg">{selectedMix.name}</h3>
            <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
              {selectedMix.flavors}
            </p>
          </div>
          <div className="text-2xl font-bold text-brand-orange">
            {selectedMix.price}₾
          </div>
        </div>
      </Card>

      {/* Checkout Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Address */}
        <Card>
          <h2 className="text-xl font-semibold mb-4">
            {t('checkout_address', language)}
          </h2>
          <div className="space-y-3">
            <Input
              label={language === 'ru' ? 'Адрес *' : 'Address *'}
              placeholder={language === 'ru' ? 'Улица, дом' : 'Street, building'}
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              required
            />
            <div className="grid grid-cols-2 gap-3">
              <Input
                label={language === 'ru' ? 'Подъезд' : 'Entrance'}
                placeholder="1"
                value={entrance}
                onChange={(e) => setEntrance(e.target.value)}
              />
              <Input
                label={language === 'ru' ? 'Этаж' : 'Floor'}
                placeholder="5"
                value={floor}
                onChange={(e) => setFloor(e.target.value)}
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Input
                label={language === 'ru' ? 'Квартира' : 'Apartment'}
                placeholder="42"
                value={apartment}
                onChange={(e) => setApartment(e.target.value)}
              />
              <Input
                label={language === 'ru' ? 'Код домофона' : 'Door code'}
                placeholder="1234"
                value={doorCode}
                onChange={(e) => setDoorCode(e.target.value)}
              />
            </div>
          </div>
        </Card>

        {/* Contact */}
        <Card>
          <h2 className="text-xl font-semibold mb-4">
            {language === 'ru' ? 'Контакты' : 'Contact'}
          </h2>
          <div className="space-y-3">
            <Input
              label={`${t('checkout_phone', language)} *`}
              type="tel"
              placeholder="+995 555 123 456"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
            <Input
              label={t('checkout_comment', language)}
              placeholder={language === 'ru' ? 'Дополнительная информация' : 'Additional info'}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
          </div>
        </Card>

        {/* Deposit */}
        <Card>
          <h2 className="text-xl font-semibold mb-4">
            {t('checkout_deposit', language)}
          </h2>
          
          {hasPassportOnFile ? (
            <div className="flex items-center gap-2 text-brand-green">
              <Badge variant="success">✓ {language === 'ru' ? 'Паспорт в базе' : 'Passport on file'}</Badge>
              <span className="text-sm">
                {language === 'ru' ? 'Залог не требуется' : 'No deposit required'}
              </span>
            </div>
          ) : (
            <div className="space-y-3">
              <label className="flex items-center gap-3 p-3 border border-light-border rounded-lg cursor-pointer hover:bg-light-surface dark:hover:bg-dark-surface transition-colors">
                <input
                  type="radio"
                  name="deposit"
                  value="cash"
                  checked={depositType === 'cash'}
                  onChange={() => setDepositType('cash')}
                  className="w-5 h-5 text-brand-orange focus:ring-brand-orange"
                />
                <div className="flex-1">
                  <div className="font-medium">{t('checkout_deposit_cash', language)}</div>
                  <div className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
                    {language === 'ru' ? 'Наличными курьеру' : 'Cash to courier'}
                  </div>
                </div>
                <span className="text-2xl">💵</span>
              </label>

              <label className="flex items-center gap-3 p-3 border border-light-border rounded-lg cursor-pointer hover:bg-light-surface dark:hover:bg-dark-surface transition-colors">
                <input
                  type="radio"
                  name="deposit"
                  value="passport"
                  checked={depositType === 'passport'}
                  onChange={() => setDepositType('passport')}
                  className="w-5 h-5 text-brand-orange focus:ring-brand-orange"
                />
                <div className="flex-1">
                  <div className="font-medium">{t('checkout_deposit_passport', language)}</div>
                  <div className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
                    {language === 'ru' ? 'Фото сделает курьер' : 'Courier will take photo'}
                  </div>
                </div>
                <span className="text-2xl">🪪</span>
              </label>
            </div>
          )}
        </Card>

        {/* Promo Code */}
        <Card>
          <Input
            label={t('checkout_promo_code', language)}
            placeholder={language === 'ru' ? 'Введите промокод' : 'Enter promo code'}
            value={promoCode}
            onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
          />
          <p className="text-xs text-light-text-secondary dark:text-dark-text-secondary mt-2">
            {language === 'ru' 
              ? 'Скидка применяется только к кальяну' 
              : 'Discount applies to hookah only'}
          </p>
        </Card>

        {/* Rules Agreement */}
        <Card>
          <Checkbox
            label={
              <span>
                {t('checkout_rules', language)}{' '}
                <a href="#" className="text-brand-orange underline">
                  {language === 'ru' ? 'Читать правила' : 'Read rules'}
                </a>
              </span>
            }
            checked={rulesAccepted}
            onChange={(e) => setRulesAccepted(e.target.checked)}
          />
        </Card>

        {/* Submit */}
        <Button 
          type="submit" 
          variant="primary" 
          className="w-full text-lg py-4"
          disabled={!rulesAccepted}
        >
          {t('checkout_place_order', language)}
        </Button>
      </form>
    </div>
  );
}
