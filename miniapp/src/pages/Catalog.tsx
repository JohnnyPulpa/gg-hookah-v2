import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mix } from '../types';
import MixCard from '../components/MixCard';
import { useLanguageContext } from '../contexts/LanguageContext';
import { mixesApi } from '../api/mixes';

export default function Catalog() {
  const navigate = useNavigate();
  const { language } = useLanguageContext();
  const [mixes, setMixes] = useState<Mix[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    mixesApi
      .getAll()
      .then(setMixes)
      .catch(() => setError('Failed to load mixes'))
      .finally(() => setLoading(false));
  }, []);

  const handleChooseMix = (mix: Mix) => {
    navigate('/drinks-question', { state: { selectedMix: mix } });
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center" style={{ paddingTop: 60 }}>
        <div style={{ fontSize: 40, marginBottom: 12 }}>⏳</div>
        <p style={{ color: 'var(--text-muted)', fontWeight: 600 }}>
          {language === 'ru' ? 'Загрузка миксов...' : 'Loading mixes...'}
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center" style={{ paddingTop: 60 }}>
        <div style={{ fontSize: 40, marginBottom: 12 }}>❌</div>
        <p style={{ color: '#C62828', fontWeight: 600 }}>{error}</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col" style={{ gap: 12, paddingBottom: 12 }}>
      {mixes.map((mix) => (
        <MixCard key={mix.id} mix={mix} onChoose={handleChooseMix} />
      ))}
      {mixes.length === 0 && (
        <div className="flex flex-col items-center" style={{ paddingTop: 60 }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>🌿</div>
          <p style={{ color: 'var(--text-muted)', fontWeight: 600 }}>
            {language === 'ru' ? 'Миксы скоро появятся' : 'Mixes coming soon'}
          </p>
        </div>
      )}
    </div>
  );
}