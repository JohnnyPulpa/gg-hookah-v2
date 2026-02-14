import { useEffect, useState } from 'react';
import { Language } from '../types';

export function useLanguage() {
  const [language, setLanguage] = useState<Language>(() => {
    // Читаем из localStorage или используем 'ru' по умолчанию
    const saved = localStorage.getItem('language') as Language;
    return saved || 'ru';
  });

  useEffect(() => {
    // Сохраняем в localStorage
    localStorage.setItem('language', language);
    
    // TODO: В будущем здесь будет синхронизация с backend API
    // для обновления users.language
  }, [language]);

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'ru' ? 'en' : 'ru');
  };

  return { language, toggleLanguage, setLanguage };
}
