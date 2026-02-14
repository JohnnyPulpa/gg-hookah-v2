import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';
import { t } from '../utils/translations';
import type { Order, OrderStatus } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';

export default function Orders() {
  const navigate = useNavigate();
  const { language } = useLanguage();

  // Mock data - в будущем из API
  const activeOrder: Order | null = null;
  
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

  const getStatusBadge = (status: OrderStatus) => {
    const statusMap: Record<OrderStatus, { variant: 'default' | 'success' | 'warning' | 'error' | 'info', label: string }> = {
      NEW: { variant: 'info', label: language === 'ru' ? 'Новый' : 'New' },
      CONFIRMED: { variant: 'info', label: language === 'ru' ? 'Подтвержден' : 'Confirmed' },
      ON_THE_WAY: { variant: 'warning', label: language === 'ru' ? 'В пути' : 'On the way' },
      DELIVERED: { variant: 'success', label: language === 'ru' ? 'Доставлен' : 'Delivered' },
      SESSION_ACTIVE: { variant: 'success', label: language === 'ru' ? 'Сессия' : 'Session' },
      SESSION_ENDING: { variant: 'warning', label: language === 'ru' ? 'Завершается' : 'Ending' },
      WAITING_FOR_PICKUP: { variant: 'warning', label: language === 'ru' ? 'Ждем возврата' : 'Pickup' },
      COMPLETED: { variant: 'default', label: language === 'ru' ? 'Завершен' : 'Completed' },
      CANCELED: { variant: 'error', label: language === 'ru' ? 'Отменен' : 'Canceled' }
    };
    
    const { variant, label } = statusMap[status];
    return <Badge variant={variant}>{label}</Badge>;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat(language === 'ru' ? 'ru-RU' : 'en-US', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const renderActiveOrder = (order: Order) => (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">
          {t('orders_active', language)}
        </h2>
        {getStatusBadge(order.status)}
      </div>
      
      <div className="space-y-3">
        <div>
          <div className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
            {language === 'ru' ? 'Микс' : 'Mix'}
          </div>
          <div className="font-medium">{order.mix_name}</div>
        </div>
        
        <div>
          <div className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
            {language === 'ru' ? 'Адрес' : 'Address'}
          </div>
          <div className="font-medium">{order.address_text}</div>
        </div>

        {order.session_ends_at && (
          <div>
            <div className="text-sm text-light-text-secondary dark:text-dark-text-secondary mb-2">
              {language === 'ru' ? 'Осталось времени' : 'Time remaining'}
            </div>
            <div className="text-3xl font-bold text-brand-orange">
              01:45:30
            </div>
          </div>
        )}

        <div className="pt-3 flex gap-3">
          <Button variant="secondary" className="flex-1">
            {t('support', language)}
          </Button>
        </div>
      </div>
    </Card>
  );

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-brand-orange mb-2">
          {t('orders_title', language)}
        </h1>
      </div>

      {activeOrder ? renderActiveOrder(activeOrder) : (
        <Card className="text-center py-8">
          <div className="text-5xl mb-4">🌿</div>
          <h2 className="text-xl font-semibold mb-2">
            {language === 'ru' ? 'Нет активных заказов' : 'No active orders'}
          </h2>
          <p className="text-light-text-secondary dark:text-dark-text-secondary mb-4">
            {language === 'ru' 
              ? 'Закажите кальян прямо сейчас!'
              : 'Order a hookah right now!'}
          </p>
          <Button onClick={() => navigate('/catalog')}>
            {t('home_order_button', language)}
          </Button>
        </Card>
      )}

      {orderHistory.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">
            {t('orders_history', language)}
          </h2>
          
          {orderHistory.map((order) => (
            <Card key={order.id}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium">{order.mix_name}</span>
                    {getStatusBadge(order.status)}
                  </div>
                  <div className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
                    {formatDate(order.created_at)}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-brand-orange">
                    {order.total_price}₾
                  </div>
                </div>
              </div>
              
              <Button 
                variant="ghost" 
                onClick={() => navigate('/catalog')}
                className="w-full"
              >
                {t('orders_order_again', language)}
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
