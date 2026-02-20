import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

export function getTelegramId(): number {
  return window.Telegram?.WebApp?.initDataUnsafe?.user?.id || 0;
}

export function getTelegramUser() {
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  return {
    id: user?.id || 0,
    username: user?.username || '',
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
  };
}
