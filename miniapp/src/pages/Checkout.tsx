import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';
import { DepositType } from '../types';

export default function Checkout() {
  const navigate = useNavigate();
  const location = useLocation();
  const { language } = useLanguageContext();

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

  // TODO: check from API by phone
  const hasPassportOnFile = false;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!rulesAccepted) {
      alert(language === 'ru' ? 'Подтвердите согласие с правилами' : 'Please accept the rules');
      return;
    }
    // TODO: POST /api/orders
    console.log('Order:', { mix: selectedMix, address, entrance, floor, apartment, doorCode, phone, comment, depositType, promoCode });
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
        <p className="text-gray-500 mb-6">
          {language === 'ru' ? 'Пожалуйста, выберите микс из каталога' : 'Please choose a mix from the catalog'}
        </p>
        <button onClick={() => navigate('/catalog')} className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
          {language === 'ru' ? 'Перейти в каталог' : 'Go to catalog'}
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-orange-500 mb-2">
        {t('checkout_title', language)}
      </h1>

      {/* Selected Mix Summary */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold text-lg">{selectedMix.name}</h3>
            <p className="text-sm text-gray-500">{selectedMix.flavors}</p>
          </div>
          <div className="text-2xl font-bold text-orange-500">{selectedMix.price}₾</div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Address */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 space-y-3">
          <h2 className="text-xl font-semibold">{t('checkout_address', language)}</h2>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">{language === 'ru' ? 'Адрес *' : 'Address *'}</label>
            <input type="text" required value={address} onChange={e => setAddress(e.target.value)} placeholder={language === 'ru' ? 'Улица, дом' : 'Street, building'} className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{language === 'ru' ? 'Подъезд' : 'Entrance'}</label>
              <input type="text" value={entrance} onChange={e => setEntrance(e.target.value)} placeholder="1" className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{language === 'ru' ? 'Этаж' : 'Floor'}</label>
              <input type="text" value={floor} onChange={e => setFloor(e.target.value)} placeholder="5" className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{language === 'ru' ? 'Квартира' : 'Apartment'}</label>
              <input type="text" value={apartment} onChange={e => setApartment(e.target.value)} placeholder="42" className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{language === 'ru' ? 'Код домофона' : 'Door code'}</label>
              <input type="text" value={doorCode} onChange={e => setDoorCode(e.target.value)} placeholder="1234" className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
            </div>
          </div>
        </div>

        {/* Contact */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 space-y-3">
          <h2 className="text-xl font-semibold">{language === 'ru' ? 'Контакты' : 'Contact'}</h2>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">{t('checkout_phone', language)} *</label>
            <input type="tel" required value={phone} onChange={e => setPhone(e.target.value)} placeholder="+995 555 123 456" className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">{t('checkout_comment', language)}</label>
            <input type="text" value={comment} onChange={e => setComment(e.target.value)} placeholder={language === 'ru' ? 'Дополнительная информация' : 'Additional info'} className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
          </div>
        </div>

        {/* Deposit */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <h2 className="text-xl font-semibold mb-4">{t('checkout_deposit', language)}</h2>
          {hasPassportOnFile ? (
            <div className="flex items-center gap-2 text-green-600">
              <span className="bg-green-100 text-green-700 text-xs font-semibold px-2 py-1 rounded">✓ {language === 'ru' ? 'Паспорт в базе' : 'Passport on file'}</span>
              <span className="text-sm">{language === 'ru' ? 'Залог не требуется' : 'No deposit required'}</span>
            </div>
          ) : (
            <div className="space-y-3">
              <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                <input type="radio" name="deposit" checked={depositType === 'cash'} onChange={() => setDepositType('cash')} className="w-5 h-5 text-orange-500" />
                <div className="flex-1">
                  <div className="font-medium">{t('checkout_deposit_cash', language)}</div>
                  <div className="text-sm text-gray-500">{language === 'ru' ? 'Наличными курьеру' : 'Cash to courier'}</div>
                </div>
                <span className="text-2xl">💵</span>
              </label>
              <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                <input type="radio" name="deposit" checked={depositType === 'passport'} onChange={() => setDepositType('passport')} className="w-5 h-5 text-orange-500" />
                <div className="flex-1">
                  <div className="font-medium">{t('checkout_deposit_passport', language)}</div>
                  <div className="text-sm text-gray-500">{language === 'ru' ? 'Фото сделает курьер' : 'Courier will take photo'}</div>
                </div>
                <span className="text-2xl">🪪</span>
              </label>
            </div>
          )}
        </div>

        {/* Promo Code */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">{t('checkout_promo_code', language)}</label>
          <input type="text" value={promoCode} onChange={e => setPromoCode(e.target.value.toUpperCase())} placeholder={language === 'ru' ? 'Введите промокод' : 'Enter promo code'} className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500" />
          <p className="text-xs text-gray-500 mt-2">{language === 'ru' ? 'Скидка применяется только к кальяну' : 'Discount applies to hookah only'}</p>
        </div>

        {/* Rules */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" checked={rulesAccepted} onChange={e => setRulesAccepted(e.target.checked)} className="w-5 h-5 rounded text-orange-500" />
            <span>{t('checkout_rules', language)}{' '}<a href="#" className="text-orange-500 underline">{language === 'ru' ? 'Читать правила' : 'Read rules'}</a></span>
          </label>
        </div>

        {/* Submit */}
        <button type="submit" disabled={!rulesAccepted} className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-bold text-lg py-4 rounded-xl transition-colors">
          {t('checkout_place_order', language)}
        </button>
      </form>
    </div>
  );
}
