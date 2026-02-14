import { useEffect, useState } from 'react';
import { Theme } from '../types';

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => {
    // Читаем из localStorage или используем 'light' по умолчанию
    const saved = localStorage.getItem('theme') as Theme;
    return saved || 'light';
  });

  useEffect(() => {
    // Применяем тему к document.documentElement
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    
    // Сохраняем в localStorage
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return { theme, toggleTheme };
}
