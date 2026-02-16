import { useLocation, useNavigate } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';

export default function Header() {
  const { language, toggleLanguage } = useLanguageContext();
  const location = useLocation();
  const navigate = useNavigate();
  const isHome = location.pathname === '/';

  // Page titles for inner pages
  const pageTitles: Record<string, { ru: string; en: string }> = {
    '/catalog': { ru: 'Миксы', en: 'Mixes' },
    '/drinks-question': { ru: '', en: '' },
    '/drinks': { ru: 'Напитки', en: 'Drinks' },
    '/checkout': { ru: 'Оформление', en: 'Checkout' },
    '/orders': { ru: 'Мои заказы', en: 'My Orders' },
  };

  const currentTitle = pageTitles[location.pathname];

  return (
    <header className="flex-shrink-0" style={{ padding: '0 20px 12px' }}>
      <div className="flex items-center justify-between">
        {/* Left side: back button or spacer */}
        <div style={{ minWidth: 60 }}>
          {!isHome && (
            <button
              onClick={() => navigate(-1)}
              className="flex items-center gap-1 border-none cursor-pointer"
              style={{
                fontSize: 15,
                fontWeight: 700,
                color: 'var(--orange)',
                background: 'none',
                fontFamily: "'Nunito', sans-serif",
              }}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth={2.5}
                style={{ width: 20, height: 20 }}
              >
                <path d="M15 18l-6-6 6-6" />
              </svg>
              {language === 'ru' ? 'Назад' : 'Back'}
            </button>
          )}
        </div>

        {/* Center: page title */}
        <div
          style={{
            fontSize: 17,
            fontWeight: 800,
            color: 'var(--text)',
          }}
        >
          {!isHome && currentTitle ? currentTitle[language] : ''}
        </div>

        {/* Right side: language toggle */}
        <div style={{ minWidth: 60, display: 'flex', justifyContent: 'flex-end' }}>
          {(isHome || location.pathname === '/catalog') && (
            <div
              className="flex"
              style={{
                background: 'var(--bg-input)',
                borderRadius: 'var(--radius-full)',
                padding: 3,
                gap: 2,
                border: '1.5px solid var(--border)',
              }}
            >
              <button
                onClick={() => language !== 'ru' && toggleLanguage()}
                style={{
                  fontFamily: "'Nunito', sans-serif",
                  fontSize: 12,
                  fontWeight: 800,
                  padding: '4px 10px',
                  border: 'none',
                  borderRadius: 'var(--radius-full)',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  background: language === 'ru' ? 'var(--orange)' : 'transparent',
                  color: language === 'ru' ? 'white' : 'var(--text-muted)',
                  boxShadow: language === 'ru' ? '0 2px 8px var(--orange-glow)' : 'none',
                }}
              >
                RU
              </button>
              <button
                onClick={() => language !== 'en' && toggleLanguage()}
                style={{
                  fontFamily: "'Nunito', sans-serif",
                  fontSize: 12,
                  fontWeight: 800,
                  padding: '4px 10px',
                  border: 'none',
                  borderRadius: 'var(--radius-full)',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  background: language === 'en' ? 'var(--orange)' : 'transparent',
                  color: language === 'en' ? 'white' : 'var(--text-muted)',
                  boxShadow: language === 'en' ? '0 2px 8px var(--orange-glow)' : 'none',
                }}
              >
                EN
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}