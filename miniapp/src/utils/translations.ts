import { Language } from '../types';

type TranslationKeys = {
  // Home
  home_title: string;
  home_order_button: string;
  home_mix_of_week: string;
  home_discount_banner: string;
  home_board_games: string;
  home_working_hours: string;
  
  // Catalog
  catalog_title: string;
  catalog_choose: string;
  
  // Checkout
  checkout_title: string;
  checkout_address: string;
  checkout_phone: string;
  checkout_comment: string;
  checkout_deposit: string;
  checkout_deposit_cash: string;
  checkout_deposit_passport: string;
  checkout_promo_code: string;
  checkout_rules: string;
  checkout_place_order: string;
  
  // Orders
  orders_title: string;
  orders_active: string;
  orders_history: string;
  orders_order_again: string;
  
  // Common
  support: string;
  cancel: string;
};

const translations: Record<Language, TranslationKeys> = {
  ru: {
    home_title: 'GG HOOKAH',
    home_order_button: 'Заказать кальян',
    home_mix_of_week: 'Микс недели',
    home_discount_banner: 'Скидка -{}% действует до {}',
    home_board_games: 'Настольные игры в подарок к заказу',
    home_working_hours: 'Ср-Вс: 18:00-02:00',
    
    catalog_title: 'Миксы кальяна',
    catalog_choose: 'Выбрать',
    
    checkout_title: 'Оформление заказа',
    checkout_address: 'Адрес доставки',
    checkout_phone: 'Телефон',
    checkout_comment: 'Комментарий',
    checkout_deposit: 'Залог',
    checkout_deposit_cash: '100₾ наличными',
    checkout_deposit_passport: 'Фото паспорта',
    checkout_promo_code: 'Промокод',
    checkout_rules: 'Мне есть 18+ и я согласен с правилами',
    checkout_place_order: 'Оформить заказ',
    
    orders_title: 'Мои заказы',
    orders_active: 'Активный заказ',
    orders_history: 'История',
    orders_order_again: 'Заказать снова',
    
    support: 'Поддержка',
    cancel: 'Отменить',
  },
  
  en: {
    home_title: 'GG HOOKAH',
    home_order_button: 'Order hookah',
    home_mix_of_week: 'Mix of the Week',
    home_discount_banner: '-{}% discount valid until {}',
    home_board_games: 'Free board game with hookah order',
    home_working_hours: 'Wed-Sun: 18:00-02:00',
    
    catalog_title: 'Hookah Mixes',
    catalog_choose: 'Choose',
    
    checkout_title: 'Checkout',
    checkout_address: 'Delivery address',
    checkout_phone: 'Phone',
    checkout_comment: 'Comment',
    checkout_deposit: 'Deposit',
    checkout_deposit_cash: '100₾ cash',
    checkout_deposit_passport: 'Passport photo',
    checkout_promo_code: 'Promo code',
    checkout_rules: 'I am 18+ and agree to the rules',
    checkout_place_order: 'Place order',
    
    orders_title: 'My Orders',
    orders_active: 'Active order',
    orders_history: 'History',
    orders_order_again: 'Order again',
    
    support: 'Support',
    cancel: 'Cancel',
  }
};

export function t(key: keyof TranslationKeys, lang: Language): string {
  return translations[lang][key];
}

export default translations;
