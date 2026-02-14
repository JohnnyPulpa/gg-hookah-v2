import { useLocation, useNavigate } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';

export default function Header() {
  const { language, toggleLanguage } = useLanguageContext();
  const location = useLocation();
  const navigate = useNavigate();
  const isHome = location.pathname === '/';

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-2">
          {isHome ? (
            <button
              onClick={toggleLanguage}
              className="px-3 py-1.5 rounded-md font-medium text-sm transition-colors bg-gray-100 hover:bg-orange-500 hover:text-white"
            >
              {language === 'ru' ? 'EN' : 'RU'}
            </button>
          ) : (
            <button
              onClick={() => navigate(-1)}
              className="px-3 py-1.5 rounded-md font-medium text-sm transition-colors bg-gray-100 hover:bg-gray-200"
            >
              ← {language === 'ru' ? 'Назад' : 'Back'}
            </button>
          )}
        </div>

        <h1
          className="text-xl font-bold text-orange-500 cursor-pointer"
          onClick={() => navigate('/')}
        >
          GG HOOKAH
        </h1>

        <div className="w-16" />
      </div>
    </header>
  );
}
