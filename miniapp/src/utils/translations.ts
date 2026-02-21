import { Language } from '../types';

type TranslationKeys = {
  // Home
  home_subtitle: string;
  home_order_button: string;
  home_mix_of_week: string;
  home_discount_text: string;
  home_board_games: string;
  home_board_games_sub: string;
  home_working_hours: string;
  home_channel_link: string;

  // Games popup
  games_title: string;
  games_subtitle: string;
  games_close: string;
  games_chess: string;
  games_jenga: string;
  games_uno: string;
  games_backgammon: string;
  games_chess_players: string;
  games_jenga_players: string;
  games_uno_players: string;
  games_backgammon_players: string;

  // Catalog
  catalog_title: string;
  catalog_choose: string;

  // Mix characteristics
  char_strength: string;
  char_coolness: string;
  char_sweetness: string;
  char_smokiness: string;

  // Drinks
  drinks_question: string;
  drinks_question_sub: string;
  drinks_yes: string;
  drinks_no: string;
  drinks_title: string;
  drinks_max: string;
  drinks_total: string;
  drinks_next: string;

  // Checkout
  checkout_title: string;
  checkout_your_order: string;
  checkout_total: string;
  checkout_address: string;
  checkout_entrance: string;
  checkout_floor: string;
  checkout_apartment: string;
  checkout_door_code: string;
  checkout_phone: string;
  checkout_comment: string;
  checkout_comment_placeholder: string;
  checkout_deposit: string;
  checkout_deposit_cash: string;
  checkout_deposit_passport: string;
  checkout_promo_code: string;
  checkout_promo_placeholder: string;
  checkout_rules: string;
  checkout_rules_link: string;
  checkout_place_order: string;

  // Order success
  success_title: string;
  success_subtitle: string;
  success_home: string;
  success_support: string;

  // Orders
  orders_title: string;
  orders_active: string;
  orders_history: string;
  orders_order_again: string;
  orders_session_end: string;
  orders_time_left: string;

  // Statuses
  status_new: string;
  status_confirmed: string;
  status_delivering: string;
  status_session: string;
  status_completed: string;
  status_cancelled: string;

  // Order actions
  action_cancel_order: string;
  action_ready_pickup: string;
  action_confirm_cancel: string;
  action_confirm_cancel_yes: string;
  action_confirm_cancel_no: string;
  action_cancel_success: string;
  action_pickup_success: string;
  action_error: string;

  // Cart
  cart_add: string;
  cart_next: string;
  cart_all_busy: string;
  cart_all_busy_sub: string;
  cart_max_reached: string;

  // Common
  support: string;
  cancel: string;
  back: string;
};

const translations: Record<Language, TranslationKeys> = {
  ru: {
    home_subtitle: 'Доставка кальяна в Батуми',
    home_order_button: 'Заказать кальян',
    home_mix_of_week: 'Микс недели',
    home_discount_text: 'Скидка на кальян действует до',
    home_board_games: 'Бесплатная настольная игра\nна время сессии',
    home_board_games_sub: '',
    home_working_hours: 'Ср-Вс: 18:00–02:00',
    home_channel_link: 'Новости и акции в Telegram-канале →',

    games_title: '🎲 Настольные игры',
    games_subtitle: 'Выбор игры подтверждается по телефону при оформлении заказа. Игра предоставляется бесплатно на время сессии.',
    games_close: 'Закрыть',
    games_chess: 'Шахматы',
    games_jenga: 'Дженга',
    games_uno: 'UNO',
    games_backgammon: 'Нарды',
    games_chess_players: '2 игрока',
    games_jenga_players: '2-6 игроков',
    games_uno_players: '2-10 игроков',
    games_backgammon_players: '2 игрока',

    catalog_title: 'Миксы кальяна',
    catalog_choose: 'Выбрать',

    char_strength: 'Крепость',
    char_coolness: 'Холод',
    char_sweetness: 'Сладость',
    char_smokiness: 'Дымность',

    drinks_question: 'Добавить напитки?',
    drinks_question_sub: 'Напитки можно заказать только\nвместе с кальяном',
    drinks_yes: 'Да',
    drinks_no: 'Нет',
    drinks_title: 'Напитки',
    drinks_max: 'Максимум 8 напитков в заказе',
    drinks_total: 'Итого напитки',
    drinks_next: 'Далее',

    checkout_title: 'Оформление',
    checkout_your_order: 'Ваш заказ',
    checkout_total: 'Итого',
    checkout_address: '📍 Адрес доставки',
    checkout_entrance: 'Подъезд',
    checkout_floor: 'Этаж',
    checkout_apartment: 'Квартира',
    checkout_door_code: 'Код двери',
    checkout_phone: '📞 Телефон',
    checkout_comment: '💬 Комментарий',
    checkout_comment_placeholder: 'Пожелания к заказу (необязательно)',
    checkout_deposit: '🔒 Залог',
    checkout_deposit_cash: '100₾ наличными',
    checkout_deposit_passport: 'Фото паспорта',
    checkout_promo_code: '🎁 Промокод',
    checkout_promo_placeholder: 'Введите промокод',
    checkout_rules: 'Мне есть 18+ и я согласен с',
    checkout_rules_link: 'правилами сервиса',
    checkout_place_order: 'Оформить заказ',

    success_title: 'Заказ принят!',
    success_subtitle: 'Мы свяжемся по телефону, чтобы\nподтвердить детали и время.',
    success_home: '🏠 На главную',
    success_support: '💬 Написать в поддержку',

    orders_title: 'Мои заказы',
    orders_active: 'Активный заказ',
    orders_history: 'История',
    orders_order_again: 'Повторить',
    orders_session_end: 'До окончания сессии',
    orders_time_left: 'Осталось более 30 мин',

    status_new: 'НОВЫЙ',
    status_confirmed: 'ПОДТВЕРЖДЁН',
    status_delivering: 'ДОСТАВКА',
    status_session: 'СЕССИЯ',
    status_completed: 'ЗАВЕРШЁН',
    status_cancelled: 'ОТМЕНЁН',

    action_cancel_order: 'Отменить заказ',
    action_ready_pickup: 'Готов отдать кальян',
    action_confirm_cancel: 'Вы уверены, что хотите отменить заказ?',
    action_confirm_cancel_yes: 'Да, отменить',
    action_confirm_cancel_no: 'Нет',
    action_cancel_success: 'Заказ отменён',
    action_pickup_success: 'Запрос принят, скоро будем!',
    action_error: 'Не удалось выполнить действие',

    cart_add: 'Добавить',
    cart_next: 'Далее',
    cart_all_busy: 'Все кальяны заняты',
    cart_all_busy_sub: 'Попробуйте позже',
    cart_max_reached: 'Максимум достигнут',

    support: 'Поддержка',
    cancel: 'Отменить',
    back: 'Назад',
  },

  en: {
    home_subtitle: 'Hookah delivery in Batumi',
    home_order_button: 'Order hookah',
    home_mix_of_week: 'Mix of the Week',
    home_discount_text: 'Hookah discount valid until',
    home_board_games: 'Free board game\nduring session',
    home_board_games_sub: '',
    home_working_hours: 'Wed-Sun: 18:00–02:00',
    home_channel_link: 'News & promos in Telegram channel →',

    games_title: '🎲 Board Games',
    games_subtitle: 'Game choice is confirmed by phone when placing an order. The game is provided free during the session.',
    games_close: 'Close',
    games_chess: 'Chess',
    games_jenga: 'Jenga',
    games_uno: 'UNO',
    games_backgammon: 'Backgammon',
    games_chess_players: '2 players',
    games_jenga_players: '2-6 players',
    games_uno_players: '2-10 players',
    games_backgammon_players: '2 players',

    catalog_title: 'Hookah Mixes',
    catalog_choose: 'Choose',

    char_strength: 'Strength',
    char_coolness: 'Coolness',
    char_sweetness: 'Sweetness',
    char_smokiness: 'Smokiness',

    drinks_question: 'Add drinks?',
    drinks_question_sub: 'Drinks can only be ordered\nwith a hookah',
    drinks_yes: 'Yes',
    drinks_no: 'No',
    drinks_title: 'Drinks',
    drinks_max: 'Maximum 8 drinks per order',
    drinks_total: 'Drinks total',
    drinks_next: 'Next',

    checkout_title: 'Checkout',
    checkout_your_order: 'Your order',
    checkout_total: 'Total',
    checkout_address: '📍 Delivery address',
    checkout_entrance: 'Entrance',
    checkout_floor: 'Floor',
    checkout_apartment: 'Apartment',
    checkout_door_code: 'Door code',
    checkout_phone: '📞 Phone',
    checkout_comment: '💬 Comment',
    checkout_comment_placeholder: 'Order notes (optional)',
    checkout_deposit: '🔒 Deposit',
    checkout_deposit_cash: '100₾ cash',
    checkout_deposit_passport: 'Passport photo',
    checkout_promo_code: '🎁 Promo code',
    checkout_promo_placeholder: 'Enter promo code',
    checkout_rules: 'I am 18+ and agree to the',
    checkout_rules_link: 'service rules',
    checkout_place_order: 'Place order',

    success_title: 'Order placed!',
    success_subtitle: 'We will call you to confirm\nthe details and time.',
    success_home: '🏠 Back to home',
    success_support: '💬 Contact support',

    orders_title: 'My Orders',
    orders_active: 'Active order',
    orders_history: 'History',
    orders_order_again: 'Reorder',
    orders_session_end: 'Session ends in',
    orders_time_left: 'More than 30 min left',

    status_new: 'NEW',
    status_confirmed: 'CONFIRMED',
    status_delivering: 'DELIVERING',
    status_session: 'SESSION',
    status_completed: 'COMPLETED',
    status_cancelled: 'CANCELLED',

    action_cancel_order: 'Cancel order',
    action_ready_pickup: 'Ready for pickup',
    action_confirm_cancel: 'Are you sure you want to cancel the order?',
    action_confirm_cancel_yes: 'Yes, cancel',
    action_confirm_cancel_no: 'No',
    action_cancel_success: 'Order canceled',
    action_pickup_success: 'Request received, we\'ll be there soon!',
    action_error: 'Action failed',

    cart_add: 'Add',
    cart_next: 'Next',
    cart_all_busy: 'All hookahs are busy',
    cart_all_busy_sub: 'Please try again later',
    cart_max_reached: 'Maximum reached',

    support: 'Support',
    cancel: 'Cancel',
    back: 'Back',
  },
};

export function t(key: keyof TranslationKeys, lang: Language): string {
  return translations[lang][key];
}

export default translations;