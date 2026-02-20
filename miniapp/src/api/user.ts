import apiClient from './client';

export async function getUserLanguage(telegramId: number): Promise<string> {
  const res = await apiClient.get('/user/language', {
    params: { telegram_id: telegramId },
  });
  return res.data.language;
}

export async function setUserLanguage(telegramId: number, language: string): Promise<void> {
  await apiClient.post('/user/language', {
    telegram_id: telegramId,
    language,
  });
}

export async function ensureUser(data: {
  telegram_id: number;
  username?: string;
  first_name?: string;
  last_name?: string;
}): Promise<void> {
  await apiClient.post('/user/ensure', data);
}
