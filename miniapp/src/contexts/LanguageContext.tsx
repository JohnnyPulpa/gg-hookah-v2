import { createContext, useContext, useState, useEffect, useRef, ReactNode } from 'react';
import { Language } from '../types';
import { getTelegramId, getTelegramUser } from '../api/client';
import { getUserLanguage, setUserLanguage, ensureUser } from '../api/user';

interface LanguageContextType {
  language: Language;
  toggleLanguage: () => void;
  setLanguage: (lang: Language) => void;
}

const LanguageContext = createContext<LanguageContextType | null>(null);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>(() => {
    const saved = localStorage.getItem('gg_language') as Language;
    return saved === 'en' ? 'en' : 'ru';
  });
  const syncedRef = useRef(false);

  // On mount: ensure user exists + load server-side language preference
  useEffect(() => {
    if (syncedRef.current) return;
    syncedRef.current = true;

    const telegramId = getTelegramId();
    if (telegramId <= 0) return;

    // Ensure user record exists (fire-and-forget)
    const tgUser = getTelegramUser();
    ensureUser({
      telegram_id: tgUser.id,
      username: tgUser.username,
      first_name: tgUser.first_name,
      last_name: tgUser.last_name,
    }).catch(() => {});

    // Load language from server
    getUserLanguage(telegramId)
      .then((serverLang) => {
        const lang = serverLang === 'en' ? 'en' : 'ru';
        if (lang !== language) {
          setLanguageState(lang);
          localStorage.setItem('gg_language', lang);
        }
      })
      .catch(() => {});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    localStorage.setItem('gg_language', lang);

    // Sync to server (fire-and-forget)
    const telegramId = getTelegramId();
    if (telegramId > 0) {
      setUserLanguage(telegramId, lang).catch(() => {});
    }
  };

  const toggleLanguage = () => {
    setLanguage(language === 'ru' ? 'en' : 'ru');
  };

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguageContext(): LanguageContextType {
  const ctx = useContext(LanguageContext);
  if (!ctx) {
    throw new Error('useLanguageContext must be used inside LanguageProvider');
  }
  return ctx;
}
