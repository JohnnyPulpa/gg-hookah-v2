import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';
import { DepositType } from '../types';
import { createOrder } from '../api/orders';

interface DrinkSelection {
  drink: { id: string; name: string; price: number };
  qty: number;
}

export default function Checkout() {
  const navigate = useNavigate();
  const location = useLocation();
  const { language } = useLanguageContext();

  const selectedMix = location.state?.selectedMix;
  const selectedDrinks: DrinkSelection[] = location.state?.selectedDrinks || [];

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
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const hookahPrice = selectedMix?.price || 70;
  const drinksTotal = selectedDrinks.reduce((sum: number, s: DrinkSelection) => sum + s.drink.price * s.qty, 0);
  const totalPrice = hookahPrice + drinksTotal;

  const handleSubmit = async () => {
    if (!rulesAccepted || isSubmitting || !selectedMix) return;
    setIsSubmitting(true);
    setError('');

    try {
      const telegramId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || 0;
      const result = await createOrder({
        telegram_id: telegramId,
        mix_id: selectedMix.id,
        drinks: selectedDrinks.map((s: DrinkSelection) => ({ drink_id: s.drink.id, qty: s.qty })),
        address_text: address,
        entrance,
        floor,
        apartment,
        door_code: doorCode,
        phone,
        comment,
        deposit_type: depositType,
        promo_code: promoCode || undefined,
      });
      navigate('/orders', { state: { justCreated: true, orderId: result.order_id } });
    } catch (err: any) {
      const msg = err.response?.data?.error || (language === 'ru' ? 'Ошибка создания заказа' : 'Failed to create order');
      setError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!selectedMix) {
    return (
      <div className="flex flex-col items-center justify-center" style={{ paddingTop: 60 }}>
        <div style={{ fontSize: 48, marginBottom: 12 }}>🤔</div>
        <div style={{ fontSize: 18, fontWeight: 800, color: 'var(--text)', marginBottom: 8 }}>
          {language === 'ru' ? 'Микс не выбран' : 'No mix selected'}
        </div>
        <button className="btn-primary" style={{ maxWidth: 280 }} onClick={() => navigate('/catalog')}>
          {language === 'ru' ? 'Перейти в каталог' : 'Go to catalog'}
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      {/* Error */}
      {error && (
        <div
          style={{
            background: '#FFEBEE',
            border: '1.5px solid #C62828',
            borderRadius: 'var(--radius-sm)',
            padding: '10px 14px',
            marginBottom: 12,
            fontSize: 13,
            fontWeight: 600,
            color: '#C62828',
          }}
        >
          {error}
        </div>
      )}

      {/* Order Summary */}
      <div
        style={{
          background: 'var(--bg-card)',
          borderRadius: 'var(--radius)',
          padding: '14px 16px',
          boxShadow: 'var(--shadow)',
          border: '1px solid var(--border)',
          marginBottom: 16,
        }}
      >
        <div className="section-label">{t('checkout_your_order', language)}</div>
        <div className="flex justify-between" style={{ padding: '6px 0', fontSize: 14 }}>
          <span style={{ color: 'var(--text)', fontWeight: 600 }}>🌿 {selectedMix.name}</span>
          <span style={{ color: 'var(--text)', fontWeight: 700 }}>{hookahPrice}₾</span>
        </div>
        {selectedDrinks.map((s: DrinkSelection) => (
          <div key={s.drink.id} className="flex justify-between" style={{ padding: '6px 0', fontSize: 14 }}>
            <span style={{ color: 'var(--text)', fontWeight: 600 }}>
              🥤 {s.drink.name} × {s.qty}
            </span>
            <span style={{ color: 'var(--text)', fontWeight: 700 }}>{s.drink.price * s.qty}₾</span>
          </div>
        ))}
        <hr style={{ border: 'none', borderTop: '1px dashed var(--border)', margin: '6px 0' }} />
        <div className="flex justify-between" style={{ padding: '6px 0 0', fontSize: 16, fontWeight: 800 }}>
          <span>{t('checkout_total', language)}</span>
          <span style={{ color: 'var(--orange)' }}>{totalPrice}₾</span>
        </div>
      </div>

      {/* Address */}
      <div className="form-group">
        <label className="form-label">{t('checkout_address', language)}</label>
        <input
          className="form-input"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder={language === 'ru' ? 'ул. Горгиладзе, 28' : 'Gorgiladze st., 28'}
        />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
        <div className="form-group">
          <label className="form-label">{t('checkout_entrance', language)}</label>
          <input className="form-input" value={entrance} onChange={(e) => setEntrance(e.target.value)} placeholder="—" />
        </div>
        <div className="form-group">
          <label className="form-label">{t('checkout_floor', language)}</label>
          <input className="form-input" value={floor} onChange={(e) => setFloor(e.target.value)} placeholder="—" />
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
        <div className="form-group">
          <label className="form-label">{t('checkout_apartment', language)}</label>
          <input className="form-input" value={apartment} onChange={(e) => setApartment(e.target.value)} placeholder="—" />
        </div>
        <div className="form-group">
          <label className="form-label">{t('checkout_door_code', language)}</label>
          <input className="form-input" value={doorCode} onChange={(e) => setDoorCode(e.target.value)} placeholder="—" />
        </div>
      </div>

      {/* Phone */}
      <div className="form-group">
        <label className="form-label">{t('checkout_phone', language)}</label>
        <input
          className="form-input"
          type="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="+995 555 123 456"
        />
      </div>

      {/* Comment */}
      <div className="form-group">
        <label className="form-label">{t('checkout_comment', language)}</label>
        <input
          className="form-input"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder={t('checkout_comment_placeholder', language)}
        />
      </div>

      {/* Deposit */}
      <div className="form-group">
        <label className="form-label">{t('checkout_deposit', language)}</label>
        <div className="flex" style={{ gap: 10 }}>
          {(['cash', 'passport'] as DepositType[]).map((type) => (
            <div
              key={type}
              onClick={() => setDepositType(type)}
              style={{
                flex: 1,
                padding: 12,
                background: depositType === type ? 'rgba(242,140,24,0.06)' : 'var(--bg-input)',
                border: `2px solid ${depositType === type ? 'var(--orange)' : 'var(--border)'}`,
                borderRadius: 'var(--radius-sm)',
                textAlign: 'center',
                cursor: 'pointer',
                fontFamily: "'Nunito', sans-serif",
              }}
            >
              <div style={{ fontSize: 24 }}>{type === 'cash' ? '💵' : '🪪'}</div>
              <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text)', marginTop: 4 }}>
                {type === 'cash' ? t('checkout_deposit_cash', language) : t('checkout_deposit_passport', language)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Promo code */}
      <div className="form-group">
        <label className="form-label">{t('checkout_promo_code', language)}</label>
        <div className="flex" style={{ gap: 8 }}>
          <input
            className="form-input"
            style={{ flex: 1 }}
            value={promoCode}
            onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
            placeholder={t('checkout_promo_placeholder', language)}
          />
          <button
            style={{
              padding: '12px 16px',
              background: 'var(--green)',
              color: 'white',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              fontFamily: "'Nunito', sans-serif",
              fontSize: 13,
              fontWeight: 800,
              cursor: 'pointer',
            }}
          >
            OK
          </button>
        </div>
      </div>

      {/* Rules checkbox */}
      <div
        className="flex items-start"
        style={{ gap: 10, margin: '16px 0', cursor: 'pointer' }}
        onClick={() => setRulesAccepted(!rulesAccepted)}
      >
        <div
          style={{
            width: 22,
            height: 22,
            border: `2px solid var(--orange)`,
            borderRadius: 6,
            flexShrink: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: rulesAccepted ? 'var(--orange)' : 'transparent',
            color: 'white',
            fontSize: 14,
            fontWeight: 800,
          }}
        >
          {rulesAccepted ? '✓' : ''}
        </div>
        <span style={{ fontSize: 13, color: 'var(--text-secondary)', fontWeight: 600, lineHeight: 1.4 }}>
          {t('checkout_rules', language)}{' '}
          <span style={{ color: 'var(--orange)', textDecoration: 'underline' }}>
            {t('checkout_rules_link', language)}
          </span>
        </span>
      </div>

      {/* Submit button */}
      <button
        className="btn-primary"
        disabled={!rulesAccepted || isSubmitting || !address || !phone}
        onClick={handleSubmit}
      >
        {isSubmitting
          ? (language === 'ru' ? 'Оформляем...' : 'Placing order...')
          : `${t('checkout_place_order', language)} • ${totalPrice}₾`}
      </button>
    </div>
  );
}