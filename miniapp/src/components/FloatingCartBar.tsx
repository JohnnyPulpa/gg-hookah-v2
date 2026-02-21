import { useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';

export default function FloatingCartBar() {
  const navigate = useNavigate();
  const { totalHookahs, totalPrice } = useCart();
  const { language } = useLanguageContext();

  if (totalHookahs === 0) return null;

  const hookahWord =
    language === 'ru'
      ? totalHookahs === 1
        ? 'кальян'
        : totalHookahs < 5
          ? 'кальяна'
          : 'кальянов'
      : totalHookahs === 1
        ? 'hookah'
        : 'hookahs';

  return (
    <div
      onClick={() => navigate('/drinks-question')}
      style={{
        position: 'fixed',
        bottom: 76,
        left: 12,
        right: 12,
        zIndex: 50,
        background: 'linear-gradient(135deg, #F28C18, #E67A00)',
        borderRadius: 'var(--radius)',
        padding: '14px 18px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 4px 20px rgba(242,140,24,0.4)',
        cursor: 'pointer',
      }}
    >
      <span style={{ color: 'white', fontSize: 15, fontWeight: 800 }}>
        {totalHookahs} {hookahWord} · {totalPrice}₾
      </span>
      <span
        style={{
          color: 'white',
          fontSize: 14,
          fontWeight: 800,
          background: 'rgba(255,255,255,0.2)',
          padding: '6px 16px',
          borderRadius: 'var(--radius-sm)',
        }}
      >
        {t('cart_next', language)} →
      </span>
    </div>
  );
}
