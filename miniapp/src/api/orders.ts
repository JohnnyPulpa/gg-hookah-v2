import api from './client';

interface DrinkItem {
  drink_id: string;
  qty: number;
}

interface CreateOrderPayload {
  telegram_id: number;
  mix_id: string;
  drinks: DrinkItem[];
  address_text: string;
  entrance?: string;
  floor?: string;
  apartment?: string;
  door_code?: string;
  phone: string;
  comment?: string;
  deposit_type: string;
  promo_code?: string;
}

interface CreateOrderResponse {
  order_id: string;
  status: string;
  hookah_price: number;
  drinks_total: number;
  total: number;
  discount_applied: number;
  is_late_order: boolean;
}

interface OrderItem {
  type: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  name: string;
}

export interface OrderData {
  id: string;
  status: string;
  phone: string;
  address: string;
  hookah_count: number;
  deposit_type: string;
  promised_time: string | null;
  promised_eta_text: string | null;
  session_started_at: string | null;
  session_ends_at: string | null;
  free_extension_used: boolean;
  is_late_order: boolean;
  created_at: string;
  completed_at: string | null;
  canceled_at: string | null;
  promo_code: string | null;
  promo_percent: number | null;
  discount_percent: number | null;
  mix_name: string;
  mix_flavors: string;
  mix_image: string;
  items: OrderItem[];
  total: number;
}

interface OrdersResponse {
  active: OrderData | null;
  history: OrderData[];
}

export async function createOrder(payload: CreateOrderPayload): Promise<CreateOrderResponse> {
  const { data } = await api.post('/orders', payload);
  return data;
}

export async function getOrders(telegramId: number): Promise<OrdersResponse> {
  const { data } = await api.get('/orders', { params: { telegram_id: telegramId } });
  return data;
}

export async function cancelOrder(orderId: string, telegramId: number): Promise<{ ok: boolean; status: string }> {
  const { data } = await api.post(`/orders/${orderId}/cancel`, { telegram_id: telegramId });
  return data;
}

export async function readyForPickup(orderId: string, telegramId: number): Promise<{ ok: boolean; status: string }> {
  const { data } = await api.post(`/orders/${orderId}/ready-for-pickup`, { telegram_id: telegramId });
  return data;
}