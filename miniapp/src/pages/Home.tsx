import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';
import { mixesApi } from '../api/mixes';
import { Mix } from '../types';

export default function Home() {
  const navigate = useNavigate();
  const { language } = useLanguageContext();
  const [featuredMix, setFeaturedMix] = useState<Mix | null>(null);
  const [showGames, setShowGames] = useState(false);

  useEffect(() => {
    mixesApi.getFeatured().then(setFeaturedMix).catch(() => {});
  }, []);

  // TODO: load from API settings
  const hasActiveDiscount = true;
  const discountPercent = 15;
  const discountValidUntil = '28.02';

  const charLabels = [
    { key: 'strength' as const, label: t('char_strength', language) },
    { key: 'coolness' as const, label: t('char_coolness', language) },
    { key: 'sweetness' as const, label: t('char_sweetness', language) },
    { key: 'smokiness' as const, label: t('char_smokiness', language) },
  ];

  const games = [
    { emoji: '♟️', name: t('games_chess', language), players: t('games_chess_players', language) },
    { emoji: '🎯', name: t('games_jenga', language), players: t('games_jenga_players', language) },
    { emoji: '🃏', name: t('games_uno', language), players: t('games_uno_players', language) },
    { emoji: '🎲', name: t('games_backgammon', language), players: t('games_backgammon_players', language) },
  ];

  const renderDots = (value: number) => (
    <div className="flex" style={{ gap: 3 }}>
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: i <= value ? 'var(--orange)' : 'var(--border)',
          }}
        />
      ))}
    </div>
  );

  return (
    <div className="flex flex-col">
      {/* Hero block with mascot */}
      <div
        style={{
          position: 'relative',
          overflow: 'hidden',
          minHeight: 300,
          padding: '12px 0',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            pointerEvents: 'none',
            zIndex: 0,
          }}
        >
          <img
            src="/FFF9F2.png"
            alt="GG HOOKAH"
            style={{
              height: '100%',
              width: 'auto',
              objectFit: 'contain',
              transform: 'scale(1.645)',
              transformOrigin: 'center',
              WebkitMaskImage:
                'radial-gradient(ellipse 80% 80% at center, black 70%, transparent 80%)',
              maskImage:
                'radial-gradient(ellipse 80% 80% at center, black 70%, transparent 80%)',
              animation: 'float 3s ease-in-out infinite',
            }}
          />
        </div>
      </div>

      {/* Subtitle */}
      <div
        style={{
          textAlign: 'center',
          fontSize: 15,
          color: 'var(--text-secondary)',
          fontWeight: 700,
          padding: '0 0 8px',
        }}
      >
        {t('home_subtitle', language)}
      </div>

      {/* CTA Button */}
      <button className="btn-primary" onClick={() => navigate('/catalog')}>
        {t('home_order_button', language)}
      </button>

      {/* Discount banner */}
      {hasActiveDiscount && (
        <div
          style={{
            background: 'linear-gradient(135deg, #FFF3E0, #FFF8F0)',
            border: '1.5px solid var(--orange)',
            borderRadius: 'var(--radius)',
            padding: '12px 16px',
            margin: '12px 0',
            display: 'flex',
            alignItems: 'center',
            gap: 10,
          }}
        >
          <div
            style={{
              background: 'var(--orange)',
              color: 'white',
              fontSize: 18,
              fontWeight: 900,
              padding: '6px 10px',
              borderRadius: 'var(--radius-sm)',
              whiteSpace: 'nowrap',
            }}
          >
            -{discountPercent}%
          </div>
          <div
            style={{
              fontSize: 13,
              color: 'var(--text)',
              fontWeight: 600,
              lineHeight: 1.3,
            }}
          >
            {t('home_discount_text', language)} {discountValidUntil}
          </div>
        </div>
      )}

      {/* Mix of the Week */}
      {featuredMix && (
        <div style={{ margin: '10px 0' }}>
          <div className="section-label">{t('home_mix_of_week', language)}</div>
          <div
            style={{
              background: 'var(--bg-card)',
              borderRadius: 'var(--radius)',
              overflow: 'hidden',
              boxShadow: 'var(--shadow-card)',
              border: '1px solid var(--border)',
            }}
          >
            {/* Image area */}
            <div
              style={{
                height: 140,
                background: 'linear-gradient(135deg, #2E7D32, #1B5E20)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  background:
                    'radial-gradient(circle at 70% 30%, rgba(242,140,24,0.3), transparent 60%)',
                }}
              />
              <span
                style={{
                  fontSize: 48,
                  zIndex: 1,
                  filter: 'drop-shadow(0 2px 8px rgba(0,0,0,0.3))',
                }}
              >
                🌿
              </span>
              <span
                style={{
                  position: 'absolute',
                  top: 10,
                  left: 10,
                  background: 'var(--orange)',
                  color: 'white',
                  fontSize: 10,
                  fontWeight: 800,
                  padding: '4px 10px',
                  borderRadius: 'var(--radius-full)',
                  zIndex: 1,
                  letterSpacing: 0.5,
                }}
              >
                ⭐ {language === 'ru' ? 'МИКС НЕДЕЛИ' : 'MIX OF THE WEEK'}
              </span>
            </div>
            {/* Body */}
            <div style={{ padding: '14px 16px' }}>
              <div style={{ fontSize: 18, fontWeight: 800, color: 'var(--text)' }}>
                {featuredMix.name}
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: 'var(--text-secondary)',
                  margin: '2px 0 10px',
                  fontWeight: 600,
                }}
              >
                {featuredMix.flavors}
              </div>
              {/* Characteristics */}
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '6px 16px',
                }}
              >
                {charLabels.map((c) => (
                  <div key={c.key} className="flex items-center" style={{ gap: 8 }}>
                    <span
                      style={{
                        fontSize: 11,
                        fontWeight: 700,
                        color: 'var(--text-muted)',
                        minWidth: 70,
                      }}
                    >
                      {c.label}
                    </span>
                    {renderDots(featuredMix.characteristics[c.key] || 0)}
                  </div>
                ))}
              </div>
              <button
                onClick={() => navigate('/catalog')}
                style={{
                  marginTop: 12,
                  width: '100%',
                  padding: 12,
                  background: 'var(--orange)',
                  color: 'white',
                  border: 'none',
                  borderRadius: 'var(--radius-sm)',
                  fontFamily: "'Nunito', sans-serif",
                  fontSize: 14,
                  fontWeight: 800,
                  cursor: 'pointer',
                }}
              >
                {t('catalog_choose', language)}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Board games promo */}
      <div
        onClick={() => setShowGames(true)}
        style={{
          background: 'linear-gradient(135deg, #E8F5E9, #F1F8E9)',
          border: '1.5px solid rgba(46,125,50,0.3)',
          borderRadius: 'var(--radius)',
          padding: '14px 16px',
          margin: '10px 0',
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          cursor: 'pointer',
          transition: 'all 0.2s',
        }}
      >
        <div style={{ fontSize: 32, flexShrink: 0 }}>🎲</div>
        <div
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: 'var(--green-dark)',
            lineHeight: 1.3,
            flex: 1,
            whiteSpace: 'pre-line',
          }}
        >
          {t('home_board_games', language)}
        </div>
        <div style={{ color: 'var(--green)', fontSize: 18, fontWeight: 800 }}>›</div>
      </div>

      {/* Working hours */}
      <div
        className="flex items-center justify-center"
        style={{
          padding: '8px 0',
          fontSize: 13,
          fontWeight: 700,
          color: 'var(--text-muted)',
          gap: 6,
        }}
      >
        🕖 {t('home_working_hours', language)}
      </div>

      {/* Channel link */}
      <div
        onClick={() => window.open('https://t.me/gghookah', '_blank')}
        style={{
          textAlign: 'center',
          padding: '12px 0 4px',
          fontSize: 13,
          color: 'var(--orange)',
          fontWeight: 700,
          cursor: 'pointer',
        }}
      >
        📢 {t('home_channel_link', language)}
      </div>

      {/* Games Popup (bottom sheet) */}
      {showGames && (
        <div
          onClick={(e) => {
            if (e.target === e.currentTarget) setShowGames(false);
          }}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.5)',
            zIndex: 100,
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'center',
          }}
        >
          <div
            style={{
              background: 'var(--bg)',
              borderRadius: '24px 24px 0 0',
              width: '100%',
              maxWidth: 480,
              maxHeight: '70%',
              overflowY: 'auto',
              padding: 20,
              animation: 'slideUp 0.3s ease',
            }}
          >
            {/* Handle */}
            <div
              style={{
                width: 40,
                height: 4,
                background: 'var(--border)',
                borderRadius: 2,
                margin: '0 auto 16px',
              }}
            />
            <div style={{ fontSize: 18, fontWeight: 800, color: 'var(--text)', marginBottom: 4 }}>
              {t('games_title', language)}
            </div>
            <div
              style={{
                fontSize: 13,
                color: 'var(--text-secondary)',
                fontWeight: 600,
                marginBottom: 16,
                lineHeight: 1.4,
              }}
            >
              {t('games_subtitle', language)}
            </div>

            {/* Game items */}
            {games.map((game) => (
              <div
                key={game.name}
                style={{
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '12px 14px',
                  marginBottom: 8,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                }}
              >
                <div style={{ fontSize: 28 }}>{game.emoji}</div>
                <div>
                  <div style={{ fontSize: 15, fontWeight: 700, color: 'var(--text)' }}>
                    {game.name}
                  </div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600 }}>
                    {game.players}
                  </div>
                </div>
              </div>
            ))}

            <button
              onClick={() => setShowGames(false)}
              style={{
                width: '100%',
                padding: 14,
                background: 'transparent',
                border: '2px solid var(--border)',
                borderRadius: 'var(--radius)',
                fontFamily: "'Nunito', sans-serif",
                fontSize: 15,
                fontWeight: 700,
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                marginTop: 8,
              }}
            >
              {t('games_close', language)}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}