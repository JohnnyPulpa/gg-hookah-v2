import { useNavigate } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';
import type { Order, OrderStatus } from '../types';

export default function Orders() {
  const navigate = useNavigate();
  const { language } = useLanguageContext();

  // TODO: load from API — GET /api/orders
  const activeOrder = null as Order | null;

  const orderHistory: Order[] = [
    {
      id: '1',
      status: 'COMPLETED',
      mix_id: '1',
      mix_name: 'Lemon Mint',
      phone: '+995555123456',
      address_text: 'ул. Руставели, 15',
      total_price: 70,
      deposit_type: 'cash',
      created_at: '2026-02-05T20:30:00Z'
    }
  ];

  const statusLabels: Record<OrderStatus, { color: string; label: string }> = {
    NEW: { color: 'bg-blue-100 text-blue-700', label: language === 'ru' ? 'Новый' : 'New' },
    CONFIRMED: { color: 'bg-blue-100 text-blue-700', label: language === 'ru' ? 'Подтвержден' : 'Confirmed' },
    ON_THE_WAY: { color: 'bg-yellow-100 text-yellow-700', label: language === 'ru' ? 'В пути' : 'On the way' },
    DELIVERED: { color: 'bg-green-100 text-green-700', label: language === 'ru' ? 'Доставлен' : 'Delivered' },
    SESSION_ACTIVE: { color: 'bg-green-100 text-green-700', label: language === 'ru' ? 'Сессия' : 'Session' },
    SESSION_ENDING: { color: 'bg-yellow-100 text-yellow-700', label: language === 'ru' ? 'Завершается' : 'Ending' },
    WAITING_FOR_PICKUP: { color: 'bg-yellow-100 text-yellow-700', label: language === 'ru' ? 'Ждем возврата' : 'Pickup' },
    COMPLETED: { color: 'bg-gray-100 text-gray-700', label: language === 'ru' ? 'Завершен' : 'Completed' },
    CANCELED: { color: 'bg-red-100 text-red-700', label: language === 'ru' ? 'Отменен' : 'Canceled' },
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat(language === 'ru' ? 'ru-RU' : 'en-US', {
      day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
    }).format(date);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-orange-500 mb-2">
        {t('orders_title', language)}
      </h1>

      {/* Active order or empty state */}
      {activeOrder ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">{t('orders_active', language)}</h2>
            <span className={`text-xs font-semibold px-2 py-1 rounded ${statusLabels[activeOrder.status].color}`}>
              {statusLabels[activeOrder.status].label}
            </span>
          </div>
          <div className="space-y-3">
            <div>
              <div className="text-sm text-gray-500">{language === 'ru' ? 'Микс' : 'Mix'}</div>
              <div className="font-medium">{activeOrder.mix_name}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">{language === 'ru' ? 'Адрес' : 'Address'}</div>
              <div className="font-medium">{activeOrder.address_text}</div>
            </div>
            {activeOrder.session_ends_at && (
              <div>
                <div className="text-sm text-gray-500 mb-2">{language === 'ru' ? 'Осталось времени' : 'Time remaining'}</div>
                <div className="text-3xl font-bold text-orange-500">01:45:30</div>
              </div>
            )}
            <div className="pt-3">
              <button className="w-full border-2 border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-white font-semibold py-2 rounded-xl transition-colors">
                {t('support', language)}
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
          <div className="text-5xl mb-4">🌿</div>
          <h2 className="text-xl font-semibold mb-2">
            {language === 'ru' ? 'Нет активных заказов' : 'No active orders'}
          </h2>
          <p className="text-gray-500 mb-4">
            {language === 'ru' ? 'Закажите кальян прямо сейчас!' : 'Order a hookah right now!'}
          </p>
          <button onClick={() => navigate('/catalog')} className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
            {t('home_order_button', language)}
          </button>
        </div>
      )}

      {/* Order history */}
      {orderHistory.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">{t('orders_history', language)}</h2>
          {orderHistory.map((order) => (
            <div key={order.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium">{order.mix_name}</span>
                    <span className={`text-xs font-semibold px-2 py-1 rounded ${statusLabels[order.status].color}`}>
                      {statusLabels[order.status].label}
                    </span>
                  </div>
                  <div className="text-sm text-gray-500">{formatDate(order.created_at)}</div>
                </div>
                <div className="text-lg font-bold text-orange-500">{order.total_price}₾</div>
              </div>
              <button onClick={() => navigate('/catalog')} className="w-full text-gray-500 hover:text-orange-500 font-medium py-2 transition-colors">
                {t('orders_order_again', language)}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
