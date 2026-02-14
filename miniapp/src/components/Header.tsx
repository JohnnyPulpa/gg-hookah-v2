import { useTheme } from '../hooks/useTheme';
import { useLanguage } from '../hooks/useLanguage';

export default function Header() {
  const { theme, toggleTheme } = useTheme();
  const { language, toggleLanguage } = useLanguage();

  return (
    <header className="bg-light-surface dark:bg-dark-surface border-b border-light-border shadow-sm">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <button
            onClick={toggleLanguage}
            className="px-3 py-1.5 rounded-md font-medium text-sm transition-colors bg-light-bg dark:bg-dark-bg hover:bg-brand-orange hover:text-white"
          >
            {language.toUpperCase()}
          </button>
        </div>

        <div className="absolute left-1/2 transform -translate-x-1/2">
          <h1 className="text-xl font-bold text-brand-orange">
            GG HOOKAH
          </h1>
        </div>

        <div className="flex items-center">
          <button
            onClick={toggleTheme}
            className="p-2 rounded-md hover:bg-light-bg dark:hover:bg-dark-bg transition-colors"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </div>
      </div>
    </header>
  );
}
