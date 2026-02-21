import { useState, useEffect } from 'react';
import { Mix } from '../types';
import MixCard from '../components/MixCard';
import FloatingCartBar from '../components/FloatingCartBar';
import { useLanguageContext } from '../contexts/LanguageContext';
import { useCart } from '../contexts/CartContext';
import { mixesApi } from '../api/mixes';
import { t } from '../utils/translations';

export default function Catalog() {
  const { language } = useLanguageContext();
  const cart = useCart();
  const [mixes, setMixes] = useState<Mix[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    mixesApi
      .getAll()
      .then(setMixes)
      .catch(() => setError('Failed to load mixes'))
      .finally(() => setLoading(false));
  }, []);

  const maxReached = cart.totalHookahs >= Math.min(cart.maxHookahs, cart.availableHookahs);

  if (loading || cart.isLoading) {
    return (
      <div className="flex flex-col items-center justify-center" style={{ paddingTop: 60 }}>
        <div style={{ fontSize: 40, marginBottom: 12 }}>⏳</div>
        <p style={{ color: 'var(--text-muted)', fontWeight: 600 }}>
          {language === 'ru' ? 'Загрузка миксов...' : 'Loading mixes...'}
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center" style={{ paddingTop: 60 }}>
        <div style={{ fontSize: 40, marginBottom: 12 }}>❌</div>
        <p style={{ color: '#C62828', fontWeight: 600 }}>{error}</p>
      </div>
    );
  }

  if (cart.soldOut) {
    return (
      <div className="flex flex-col items-center justify-center text-center" style={{ paddingTop: 60 }}>
        <div style={{ fontSize: 48, marginBottom: 12 }}>😔</div>
        <div style={{ fontSize: 20, fontWeight: 800, color: 'var(--text)', marginBottom: 6 }}>
          {t('cart_all_busy', language)}
        </div>
        <div style={{ fontSize: 14, color: 'var(--text-secondary)', fontWeight: 600 }}>
          {t('cart_all_busy_sub', language)}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col" style={{ gap: 12, paddingBottom: cart.totalHookahs > 0 ? 76 : 12 }}>
      {/* Max hint when items in cart */}
      {cart.totalHookahs > 0 && maxReached && (
        <div
          style={{
            textAlign: 'center',
            fontSize: 12,
            color: 'var(--orange)',
            fontWeight: 700,
            padding: '6px 12px',
            background: 'rgba(242,140,24,0.08)',
            borderRadius: 'var(--radius-sm)',
          }}
        >
          {t('cart_max_reached', language)}
        </div>
      )}

      {mixes.map((mix) => {
        const cartItem = cart.items.find((i) => i.mix.id === mix.id);
        return (
          <MixCard
            key={mix.id}
            mix={mix}
            quantity={cartItem?.quantity || 0}
            onAdd={cart.addItem}
            onRemove={cart.removeItem}
            maxReached={maxReached}
          />
        );
      })}

      {mixes.length === 0 && (
        <div className="flex flex-col items-center" style={{ paddingTop: 60 }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>🌿</div>
          <p style={{ color: 'var(--text-muted)', fontWeight: 600 }}>
            {language === 'ru' ? 'Миксы скоро появятся' : 'Mixes coming soon'}
          </p>
        </div>
      )}

      <FloatingCartBar />
    </div>
  );
}
