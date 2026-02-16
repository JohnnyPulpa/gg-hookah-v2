import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';

export default function DrinksQuestion() {
  const navigate = useNavigate();
  const location = useLocation();
  const { language } = useLanguageContext();
  const selectedMix = location.state?.selectedMix;

  if (!selectedMix) {
    navigate('/catalog');
    return null;
  }

  return (
    <div
      className="flex flex-col items-center justify-center text-center"
      style={{ flex: 1, padding: 20, minHeight: '60vh' }}
    >
      <div style={{ fontSize: 64, marginBottom: 16 }}>🥤</div>
      <div style={{ fontSize: 22, fontWeight: 800, color: 'var(--text)', marginBottom: 6 }}>
        {t('drinks_question', language)}
      </div>
      <div
        style={{
          fontSize: 14,
          color: 'var(--text-secondary)',
          fontWeight: 600,
          marginBottom: 28,
          whiteSpace: 'pre-line',
        }}
      >
        {t('drinks_question_sub', language)}
      </div>
      <div className="flex" style={{ gap: 12, width: '100%', maxWidth: 300 }}>
        <button
          onClick={() => navigate('/drinks', { state: { selectedMix } })}
          style={{
            flex: 1,
            padding: 14,
            background: 'var(--green)',
            color: 'white',
            border: 'none',
            borderRadius: 'var(--radius)',
            fontFamily: "'Nunito', sans-serif",
            fontSize: 16,
            fontWeight: 800,
            cursor: 'pointer',
          }}
        >
          {t('drinks_yes', language)}
        </button>
        <button
          onClick={() => navigate('/checkout', { state: { selectedMix, selectedDrinks: [] } })}
          style={{
            flex: 1,
            padding: 14,
            background: 'transparent',
            color: 'var(--text-secondary)',
            border: '2px solid var(--border)',
            borderRadius: 'var(--radius)',
            fontFamily: "'Nunito', sans-serif",
            fontSize: 16,
            fontWeight: 700,
            cursor: 'pointer',
          }}
        >
          {t('drinks_no', language)}
        </button>
      </div>
    </div>
  );
}