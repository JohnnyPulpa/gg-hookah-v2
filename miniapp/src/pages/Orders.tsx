import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';
import { getOrders, OrderData } from '../api/orders';

function SessionTimer({ endsAt }: { endsAt: string }) {
  const [remaining, setRemaining] = useState('');

  useEffect(() => {
    const update = () => {
      const diff = new Date(endsAt).getTime() - Date.now();
      if (diff <= 0) {
        setRemaining('0:00:00');
        return;
      }
      const h = Math.floor(diff / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      setRemaining(`${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`);
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [endsAt]);

  return (
    <div
      style={{
        margin: '12px 0',
        background: 'linear-gradient(135deg, rgba(46,125,50,0.08), rgba(46,125,50,0.03))',
        border: '1.5px solid rgba(46,125,50,0.2)',
        borderRadius: 'var(--radius-sm)',
        padding: 12,
        textAlign: 'center',
      }}
    >
      <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--green)', textTransform: 'uppercase', letterSpacing: 1 }}>
        {/* Will be filled by parent */}
      </div>
      <div style={{ fontSize: 32, fontWeight: 900, color: 'var(--green-dark)', fontVariantNumeric: 'tabular-nums' }}>
        {remaining}
      </div>
    </div>
  );
}

function getStatusStyle(status: string): { bg: string; color: string } {
  switch (status) {
    case 'NEW': return { bg: '#FFF3E0', color: 'var(--orange-dark)' };
    case 'CONFIRMED':
    case 'ON_THE_WAY':
    case 'DELIVERED': return { bg: '#FFF3E0', color: 'var(--orange-dark)' };
    case 'SESSION_ACTIVE':
    case 'SESSION_ENDING': return { bg: '#E8F5E9', color: 'var(--green-dark)' };
    case 'COMPLETED': return { bg: '#F5F5F5', color: '#666' };
    case 'CANCELED': return { bg: '#FFEBEE', color: '#C62828' };
    default: return { bg: '#F5F5F5', color: '#666' };
  }
}

export default function Orders() {
  const navigate = useNavigate();
  const locationState = useLocation().state as { justCreated?: boolean } | null;
  const { language } = useLanguageContext();

  const [active, setActive] = useState<OrderData | null>(null);
  const [history, setHistory] = useState<OrderData[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSuccess, setShowSuccess] = useState(locationState?.justCreated || false);

  useEffect(() => {
    const telegramId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || 0;
    getOrders(telegramId)
      .then((data) => {
        setActive(data.active);
        setHistory(data.history);
      })
      .catch((err) => console.error('Failed to fetch orders:', err))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (showSuccess) {
      const timer = setTimeout(() => setShowSuccess(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [showSuccess]);

  const getStatusLabel = (status: string): string => {
    const key = `status_${status.toLowerCase().replace('_active', '').replace('_ending', '')}` as keyof typeof t;
    return t(key as any, language) || status;
  };

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

  /* ===== ORDER SUCCESS SCREEN ===== */
  if (showSuccess && !active && history.length === 0) {
    return (
      <div
        className="flex flex-col items-center justify-center text-center"
        style={{ flex: 1, padding: 20, minHeight: '60vh' }}
      >
        <div
          style={{
            width: 80,
            height: 80,
            background: 'linear-gradient(135deg, var(--green), var(--green-light))',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 40,
            color: 'white',
            marginBottom: 16,
            boxShadow: '0 4px 20px rgba(46,125,50,0.3)',
          }}
        >
          ✓
        </div>
        <div style={{ fontSize: 22, fontWeight: 800, color: 'var(--text)', marginBottom: 6 }}>
          {t('success_title', language)}
        </div>
        <div
          style={{
            fontSize: 14,
            color: 'var(--text-secondary)',
            fontWeight: 600,
            marginBottom: 32,
            whiteSpace: 'pre-line',
          }}
        >
          {t('success_subtitle', language)}
        </div>
        <button
          className="btn-primary"
          style={{ maxWidth: 280, marginBottom: 12 }}
          onClick={() => navigate('/')}
        >
          {t('success_home', language)}
        </button>
        <button
          className="btn-secondary"
          style={{ maxWidth: 280 }}
          onClick={() => window.open('https://t.me/gghookah_support', '_blank')}
        >
          {t('success_support', language)}
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      {/* Success banner (when there IS an active order) */}
      {showSuccess && (
        <div
          style={{
            background: '#E8F5E9',
            border: '1.5px solid var(--green)',
            borderRadius: 'var(--radius-sm)',
            padding: '10px 14px',
            marginBottom: 12,
            fontSize: 13,
            fontWeight: 700,
            color: 'var(--green-dark)',
          }}
        >
          ✅ {t('success_title', language)}
        </div>
      )}

      {/* Active order */}
      {active && (
        <>
          <div
            style={{
              fontSize: 12,
              fontWeight: 800,
              color: 'var(--orange)',
              textTransform: 'uppercase',
              letterSpacing: 1.5,
              margin: '4px 0 10px',
            }}
          >
            {t('orders_active', language)}
          </div>
          <div
            style={{
              background: 'var(--bg-card)',
              borderRadius: 'var(--radius)',
              padding: 16,
              boxShadow: 'var(--shadow-card)',
              border: '2px solid var(--orange)',
              marginBottom: 16,
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            {/* Top gradient bar */}
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: 3,
                background: 'linear-gradient(90deg, var(--orange), var(--green))',
              }}
            />

            {/* Header: order id + status */}
            <div className="flex justify-between items-center" style={{ marginBottom: 10 }}>
              <span style={{ fontSize: 14, fontWeight: 800, color: 'var(--text)' }}>
                {language === 'ru' ? 'Заказ' : 'Order'} #{active.id.slice(0, 4)}
              </span>
              <span
                style={{
                  padding: '4px 12px',
                  borderRadius: 'var(--radius-full)',
                  fontSize: 11,
                  fontWeight: 800,
                  textTransform: 'uppercase',
                  letterSpacing: 0.5,
                  background: getStatusStyle(active.status).bg,
                  color: getStatusStyle(active.status).color,
                }}
              >
                {getStatusLabel(active.status)}
              </span>
            </div>

            {/* Details */}
            <div className="flex flex-col" style={{ gap: 4, fontSize: 13, color: 'var(--text-secondary)', fontWeight: 600 }}>
              <span style={{ color: 'var(--text)', fontWeight: 700, fontSize: 15 }}>
                🌿 {active.mix_name}
                {active.items.filter((i) => i.type === 'drink').length > 0 &&
                  ` + 🥤 ×${active.items.filter((i) => i.type === 'drink').reduce((s, i) => s + i.quantity, 0)}`}
              </span>
              {active.address && <span>📍 {active.address}</span>}
              <span>
                {active.deposit_type === 'cash' ? '💵' : '🪪'}{' '}
                {language === 'ru' ? 'Залог:' : 'Deposit:'}{' '}
                {active.deposit_type === 'cash'
                  ? t('checkout_deposit_cash', language)
                  : t('checkout_deposit_passport', language)}
              </span>
            </div>

            {/* Timer */}
            {active.session_ends_at &&
              ['SESSION_ACTIVE', 'SESSION_ENDING'].includes(active.status) && (
                <>
                  <SessionTimer endsAt={active.session_ends_at} />
                  <div style={{ textAlign: 'center', fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, marginTop: -8 }}>
                    {t('orders_time_left', language)}
                  </div>
                </>
              )}

            {/* Support button */}
            <div className="flex" style={{ gap: 8, marginTop: 12 }}>
              <button
                onClick={() => window.open('https://t.me/gghookah_support', '_blank')}
                style={{
                  flex: 1,
                  padding: 10,
                  borderRadius: 'var(--radius-sm)',
                  fontFamily: "'Nunito', sans-serif",
                  fontSize: 12,
                  fontWeight: 800,
                  cursor: 'pointer',
                  background: 'transparent',
                  color: 'var(--orange)',
                  border: '1.5px solid var(--orange)',
                  textAlign: 'center',
                }}
              >
                💬 {t('support', language)}
              </button>
            </div>
          </div>
        </>
      )}

      {/* History */}
      {history.length > 0 && (
        <>
          <div
            style={{
              fontSize: 12,
              fontWeight: 800,
              color: 'var(--orange)',
              textTransform: 'uppercase',
              letterSpacing: 1.5,
              margin: '4px 0 10px',
            }}
          >
            {t('orders_history', language)}
          </div>
          {history.map((order) => {
            const sty = getStatusStyle(order.status);
            const drinkCount = order.items.filter((i) => i.type === 'drink').reduce((s, i) => s + i.quantity, 0);
            return (
              <div
                key={order.id}
                style={{
                  background: 'var(--bg-card)',
                  borderRadius: 'var(--radius)',
                  padding: '14px 16px',
                  boxShadow: 'var(--shadow)',
                  border: '1px solid var(--border)',
                  marginBottom: 10,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 700 }}>
                    {new Date(order.created_at).toLocaleDateString(language === 'ru' ? 'ru-RU' : 'en-US', {
                      day: 'numeric',
                      month: 'short',
                      year: 'numeric',
                    })}{' '}
                    •{' '}
                    <span
                      style={{
                        padding: '2px 8px',
                        fontSize: 9,
                        borderRadius: 'var(--radius-full)',
                        fontWeight: 800,
                        textTransform: 'uppercase',
                        background: sty.bg,
                        color: sty.color,
                      }}
                    >
                      {getStatusLabel(order.status)}
                    </span>
                  </div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: 'var(--text)' }}>
                    🌿 {order.mix_name}
                    {drinkCount > 0 && ` + 🥤 ×${drinkCount}`}
                  </div>
                  <div style={{ fontSize: 12, color: 'var(--text-secondary)', fontWeight: 600 }}>
                    {order.total}₾
                  </div>
                </div>
                <button
                  onClick={() => navigate('/catalog')}
                  style={{
                    padding: '8px 14px',
                    background: 'transparent',
                    border: '1.5px solid var(--orange)',
                    color: 'var(--orange)',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: "'Nunito', sans-serif",
                    fontSize: 12,
                    fontWeight: 800,
                    cursor: 'pointer',
                  }}
                >
                  {t('orders_order_again', language)}
                </button>
              </div>
            );
          })}
        </>
      )}

      {/* Empty state */}
      {!active && history.length === 0 && !showSuccess && (
        <div className="flex flex-col items-center justify-center text-center" style={{ paddingTop: 60 }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>🫧</div>
          <div style={{ fontSize: 18, fontWeight: 800, color: 'var(--text)', marginBottom: 8 }}>
            {language === 'ru' ? 'Пока пусто' : 'No orders yet'}
          </div>
          <div style={{ fontSize: 14, color: 'var(--text-secondary)', fontWeight: 600, marginBottom: 24 }}>
            {language === 'ru' ? 'Оформите первый заказ!' : 'Place your first order!'}
          </div>
          <button className="btn-primary" style={{ maxWidth: 280 }} onClick={() => navigate('/catalog')}>
            {t('home_order_button', language)}
          </button>
        </div>
      )}
    </div>
  );
}