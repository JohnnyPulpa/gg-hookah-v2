// Mix characteristics (1-5 scale)
export interface MixCharacteristics {
  strength: number;
  coolness: number;
  sweetness: number;
  smokiness: number;
}

// Hookah Mix
export interface Mix {
  id: string;
  name: string;
  flavors: string;
  description?: string;
  characteristics: MixCharacteristics;
  details?: string;
  image_url: string;
  is_active: boolean;
  is_featured: boolean;
  price: number;
}

// Drink item
export interface Drink {
  id: string;
  name: string;
  price: number;
  image_url?: string;
  is_active: boolean;
}

// Order status
export type OrderStatus = 
  | 'NEW'
  | 'CONFIRMED'
  | 'ON_THE_WAY'
  | 'DELIVERED'
  | 'SESSION_ACTIVE'
  | 'SESSION_ENDING'
  | 'WAITING_FOR_PICKUP'
  | 'COMPLETED'
  | 'CANCELED';

// Deposit type
export type DepositType = 'cash' | 'passport' | 'none';

// Order
export interface Order {
  id: string;
  status: OrderStatus;
  mix_id: string;
  mix_name: string;
  phone: string;
  address_text: string;
  total_price: number;
  deposit_type: DepositType;
  created_at: string;
  session_ends_at?: string;
}

// Language
export type Language = 'ru' | 'en';

// Theme
export type Theme = 'light' | 'dark';
