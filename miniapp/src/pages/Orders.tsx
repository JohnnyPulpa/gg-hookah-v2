import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { getOrders, OrderData } from '../api/orders';

const STATUS_LABELS: Record<string, { ru: string; en: string; color: string }> = {
  NEW: { ru: 'Новый', en: 'New', color: 'bg-blue-100 text-blue-700' },
  CONFIRMED: { ru: 'Подтверждён', en: 'Confirmed', color: 'bg-indigo-100 text-indigo-700' },
  ON_THE_WAY: { ru: 'В пути', en: 'On the way', color: 'bg-yellow-100 text-yellow-700' },
  DELIVERED: { ru: 'Доставлен', en: 'Delivered', color: 'bg-green-100 text-green-700' },
  SESSION_ACTIVE: { ru: 'Сессия активна', en: 'Session active', color: 'bg-green-100 text-green-700' },
  SESSION_ENDING: { ru: 'Сессия заканчивается', en: 'Session ending', color: 'bg-orange-100 text-orange-700' },
  WAITING_FOR_PICKUP: { ru: 'Ожидает забора', en: 'Waiting for pickup', color: 'bg-purple-100 text-purple-700' },
  COMPLETED: { ru: 'Завершён', en: 'Completed', color: 'bg-gray-100 text-gray-600' },
  CANCELED: { ru: 'Отменён', en: 'Canceled', color: 'bg-red-100 text-red-600' },
};

function SessionTimer({ endsAt }: { endsAt: string }) {
  const [remaining, setRemaining] = useState('');

  useEffect(() => {
    const update = () => {
      const diff = new Date(endsAt).getTime() - Date.now();
      if (diff <= 0) {
        setRemaining('00:00');
        return;
      }
      const h = Math.floor(diff / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      setRemaining(h > 0 ? `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}` : `${m}:${String(s).padStart(2, '0')}`);
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [endsAt]);

  return (
    <div className="text-center py-3">
      <div className="text-4xl font-mono font-bold text-orange-500">{remaining}</div>
      <div className="text-sm text-gray-500 mt-1">⏱</div>
    </div>
  );
}

function OrderCard({ order, language, isActive }: { order: OrderData; language: string; isActive: boolean }) {
  const status = STATUS_LABELS[order.status] || { ru: order.status, en: order.status, color: 'bg-gray-100 text-gray-600' };
  const showTimer = isActive && order.session_ends_at && ['SESSION_ACTIVE', 'SESSION_ENDING'].includes(order.status);

  return (
    <div className={`bg-white rounded-xl shadow-sm border ${isActive ? 'border-orange-300' : 'border-gray-200'} p-4 space-y-3`}>
      {/* Status + date */}
      <div className="flex items-center justify-between">
        <span className={`text-xs font-semibold px-2 py-1 rounded ${status.color}`}>
          {language === 'ru' ? status.ru : status.en}
        </span>
        <span className="text-xs text-gray-400">
          {new Date(order.created_at).toLocaleDateString(language === 'ru' ? 'ru-RU' : 'en-US', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>

      {/* Timer */}
      {showTimer && <SessionTimer endsAt={order.session_ends_at!} />}

      {/* Mix info */}
      <div className="flex items-center gap-3">
        {order.mix_image && <img src={order.mix_image} alt="" className="w-12 h-12 rounded-lg object-cover" />}
        <div>
          <div className="font-bold">{order.mix_name}</div>
          <div className="text-sm text-gray-500">{order.mix_flavors}</div>
        </div>
      </div>

      {/* Items */}
      {order.items.filter(i => i.type === 'drink').length > 0 && (
        <div className="text-sm text-gray-600">
          {order.items.filter(i => i.type === 'drink').map((item, idx) => (
            <span key={idx}>{item.name} ×{item.quantity}{idx < order.items.filter(i => i.type === 'drink').length - 1 ? ', ' : ''}</span>
          ))}
        </div>
      )}

      {/* Total + deposit */}
      <div className="flex items-center justify-between">
        <span className="font-bold text-lg text-orange-500">{order.total}₾</span>
        <span className="text-xs px-2 py-1 rounded bg-gray-100">
          {order.deposit_type === 'cash' ? '💵 100₾' : order.deposit_type === 'passport' ? '🪪' : '✓'}
        </span>
      </div>

      {/* Promised time */}
      {isActive && order.promised_eta_text && (
        <div className="text-sm text-gray-600">
          ⏰ {order.promised_eta_text}
        </div>
      )}
    </div>
  );
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
    const fetchOrders = async () => {
      try {
        const telegramId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || 0;
        const data = await getOrders(telegramId);
        setActive(data.active);
        setHistory(data.history);
      } catch (err) {
        console.error('Failed to fetch orders:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  // Auto-hide success message
  useEffect(() => {
    if (showSuccess) {
      const timer = setTimeout(() => setShowSuccess(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [showSuccess]);

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <div className="text-4xl mb-4 animate-pulse">🔄</div>
        <p className="text-gray-500">{language === 'ru' ? 'Загрузка...' : 'Loading...'}</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-orange-500 mb-2">
        {language === 'ru' ? 'Заказы' : 'Orders'}
      </h1>

      {/* Success message after order creation */}
      {showSuccess && (
        <div className="bg-green-50 border border-green-300 text-green-700 px-4 py-3 rounded-xl">
          <div className="font-bold">{language === 'ru' ? '✅ Заказ получен!' : '✅ Order received!'}</div>
          <div className="text-sm mt-1">{language === 'ru' ? 'Мы свяжемся по телефону, чтобы подтвердить детали.' : 'We will call you to confirm details.'}</div>
        </div>
      )}

      {/* Active order */}
      {active && (
        <div>
          <h2 className="text-lg font-semibold mb-2">{language === 'ru' ? 'Активный заказ' : 'Active order'}</h2>
          <OrderCard order={active} language={language} isActive={true} />
        </div>
      )}

      {/* History */}
      {history.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-2">{language === 'ru' ? 'История' : 'History'}</h2>
          <div className="space-y-3">
            {history.map(order => (
              <OrderCard key={order.id} order={order} language={language} isActive={false} />
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {!active && history.length === 0 && !showSuccess && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🫧</div>
          <h2 className="text-2xl font-bold mb-2">{language === 'ru' ? 'Пока пусто' : 'No orders yet'}</h2>
          <p className="text-gray-500 mb-6">{language === 'ru' ? 'Оформите первый заказ!' : 'Place your first order!'}</p>
          <button onClick={() => navigate('/catalog')} className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
            {language === 'ru' ? 'Заказать кальян' : 'Order hookah'}
          </button>
        </div>
      )}
    </div>
  );
}