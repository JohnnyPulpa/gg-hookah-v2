import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mix } from '../types';
import MixCard from '../components/MixCard';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';
import { mixesApi } from '../api/mixes';

export default function Catalog() {
  const navigate = useNavigate();
  const { language } = useLanguageContext();
  const [mixes, setMixes] = useState<Mix[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadMixes();
  }, []);

  const loadMixes = async () => {
    try {
      setLoading(true);
      const data = await mixesApi.getAll();
      setMixes(data);
    } catch (err) {
      console.error('Failed to load mixes:', err);
      setError('Failed to load mixes');
    } finally {
      setLoading(false);
    }
  };

  const handleChooseMix = (mix: Mix) => {
    navigate('/checkout', { state: { selectedMix: mix } });
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">⏳</div>
        <p>{language === 'ru' ? 'Загрузка миксов...' : 'Loading mixes...'}</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">❌</div>
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-orange-500 mb-2">
          {t('catalog_title', language)}
        </h1>
        <p className="text-gray-500">
          {language === 'ru'
            ? 'Выберите микс кальяна для вашего заказа'
            : 'Choose your hookah mix for the order'}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mixes.map((mix) => (
          <MixCard
            key={mix.id}
            mix={mix}
            onChoose={handleChooseMix}
            buttonText={t('catalog_choose', language)}
          />
        ))}
      </div>

      {mixes.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🌿</div>
          <p className="text-gray-500">
            {language === 'ru'
              ? 'Миксы скоро появятся'
              : 'Mixes coming soon'}
          </p>
        </div>
      )}
    </div>
  );
}
