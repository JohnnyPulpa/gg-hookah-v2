import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import Header from './Header';

export default function Layout() {
  const navigate = useNavigate();
  const location = useLocation();
  const { language } = useLanguageContext();

  const navItems = [
    {
      id: 'home',
      path: '/',
      label: { ru: 'Главная', en: 'Home' },
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
          <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1" />
        </svg>
      ),
    },
    {
      id: 'menu',
      path: '/catalog',
      label: { ru: 'Меню', en: 'Menu' },
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
          <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      ),
    },
    {
      id: 'orders',
      path: '/orders',
      label: { ru: 'Заказы', en: 'Orders' },
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
          <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        </svg>
      ),
    },
    {
      id: 'support',
      path: null,
      label: { ru: 'Поддержка', en: 'Support' },
      icon: (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
          <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      ),
    },
  ];

  const isActive = (path: string | null) => {
    if (!path) return false;
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  const handleNavClick = (item: typeof navItems[0]) => {
    if (item.path) {
      navigate(item.path);
    } else {
      // Support — TODO: open Telegram support chat
      window.open('https://t.me/gghookah_support', '_blank');
    }
  };

  return (
    <div
      className="flex flex-col h-screen"
      style={{ background: 'var(--bg)', color: 'var(--text)' }}
    >
      <Header />
      <main className="flex-1 overflow-y-auto content-scroll px-5 pb-5">
        <Outlet />
      </main>
      {/* Bottom Navigation */}
      <nav
        className="flex-shrink-0 flex justify-around"
        style={{ padding: '8px 24px 28px', background: 'var(--bg)' }}
      >
        {navItems.map((item) => {
          const active = isActive(item.path);
          return (
            <button
              key={item.id}
              onClick={() => handleNavClick(item)}
              className="flex flex-col items-center gap-1 border-none cursor-pointer"
              style={{
                padding: '6px 14px',
                borderRadius: '14px',
                background: active ? 'rgba(242, 140, 24, 0.1)' : 'transparent',
                fontFamily: "'Nunito', sans-serif",
                transition: 'all 0.2s',
              }}
            >
              <span
                className="flex items-center justify-center"
                style={{ width: 24, height: 24 }}
              >
                <span
                  style={{
                    width: 22,
                    height: 22,
                    display: 'flex',
                    color: active ? 'var(--orange)' : 'var(--text-muted)',
                  }}
                >
                  {item.icon}
                </span>
              </span>
              <span
                style={{
                  fontSize: 10,
                  fontWeight: active ? 800 : 700,
                  color: active ? 'var(--orange)' : 'var(--text-muted)',
                }}
              >
                {item.label[language]}
              </span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}