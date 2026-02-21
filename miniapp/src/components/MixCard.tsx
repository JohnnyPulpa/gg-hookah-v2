import { Mix } from '../types';
import { useLanguageContext } from '../contexts/LanguageContext';
import { t } from '../utils/translations';

interface MixCardProps {
  mix: Mix;
  quantity: number;
  onAdd: (mix: Mix) => void;
  onRemove: (mixId: string) => void;
  maxReached: boolean;
}

// Color themes for mix cards based on name patterns
const mixColors: Record<string, string> = {
  lemon: 'linear-gradient(135deg, #2E7D32, #1B5E20)',
  mint: 'linear-gradient(135deg, #2E7D32, #1B5E20)',
  tropical: 'linear-gradient(135deg, #E65100, #BF360C)',
  paradise: 'linear-gradient(135deg, #E65100, #BF360C)',
  apple: 'linear-gradient(135deg, #C62828, #8E0000)',
  blueberry: 'linear-gradient(135deg, #1565C0, #0D47A1)',
  ice: 'linear-gradient(135deg, #1565C0, #0D47A1)',
  default: 'linear-gradient(135deg, #2E7D32, #1B5E20)',
};

function getMixGradient(name: string): string {
  const lower = name.toLowerCase();
  for (const [key, value] of Object.entries(mixColors)) {
    if (key !== 'default' && lower.includes(key)) return value;
  }
  return mixColors.default;
}

function getMixEmoji(name: string): string {
  const lower = name.toLowerCase();
  if (lower.includes('lemon') || lower.includes('mint')) return '🍋';
  if (lower.includes('tropical') || lower.includes('paradise')) return '🏝️';
  if (lower.includes('apple')) return '🍎';
  if (lower.includes('blueberry')) return '🫐';
  return '🌿';
}

export default function MixCard({ mix, quantity, onAdd, onRemove, maxReached }: MixCardProps) {
  const { language } = useLanguageContext();

  const chars = [
    { key: 'strength' as const, label: t('char_strength', language) },
    { key: 'coolness' as const, label: t('char_coolness', language) },
    { key: 'sweetness' as const, label: t('char_sweetness', language) },
    { key: 'smokiness' as const, label: t('char_smokiness', language) },
  ];

  const renderMiniDots = (value: number) => (
    <div className="flex" style={{ gap: 2 }}>
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          style={{
            width: 6,
            height: 6,
            borderRadius: '50%',
            background: i <= value ? 'var(--orange)' : 'var(--border)',
          }}
        />
      ))}
    </div>
  );

  return (
    <div
      style={{
        background: 'var(--bg-card)',
        borderRadius: 'var(--radius)',
        overflow: 'hidden',
        boxShadow: 'var(--shadow)',
        border: quantity > 0 ? '2px solid var(--orange)' : '1px solid var(--border)',
        display: 'flex',
        transition: 'transform 0.2s, box-shadow 0.2s',
      }}
    >
      {/* Left image area */}
      <div
        className="flex items-center justify-center flex-shrink-0"
        style={{
          width: 110,
          minHeight: 130,
          background: getMixGradient(mix.name),
          fontSize: 40,
        }}
      >
        {getMixEmoji(mix.name)}
      </div>

      {/* Right body */}
      <div
        className="flex flex-col flex-1"
        style={{ padding: '12px 14px' }}
      >
        <div style={{ fontSize: 16, fontWeight: 800, color: 'var(--text)' }}>
          {mix.name} {mix.is_featured ? '⭐' : ''}
        </div>
        <div
          style={{
            fontSize: 12,
            color: 'var(--text-secondary)',
            fontWeight: 600,
            margin: '2px 0 8px',
          }}
        >
          {mix.flavors}
        </div>

        {/* Mini characteristics grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '3px 10px',
            marginBottom: 10,
          }}
        >
          {chars.map((c) => (
            <div
              key={c.key}
              className="flex items-center"
              style={{ gap: 4, fontSize: 10, fontWeight: 700, color: 'var(--text-muted)' }}
            >
              <span>{c.label}</span>
              {renderMiniDots(mix.characteristics[c.key] || 0)}
            </div>
          ))}
        </div>

        {/* Price + Add/Counter */}
        <div
          className="flex items-center justify-between"
          style={{ marginTop: 'auto' }}
        >
          <span style={{ fontSize: 18, fontWeight: 900, color: 'var(--orange)' }}>
            {mix.price}₾
          </span>

          {quantity === 0 ? (
            <button
              onClick={() => onAdd(mix)}
              disabled={maxReached}
              style={{
                padding: '8px 20px',
                background: maxReached ? 'var(--text-muted)' : 'var(--orange)',
                color: 'white',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                fontFamily: "'Nunito', sans-serif",
                fontSize: 13,
                fontWeight: 800,
                cursor: maxReached ? 'not-allowed' : 'pointer',
                opacity: maxReached ? 0.5 : 1,
              }}
            >
              {t('cart_add', language)}
            </button>
          ) : (
            <div
              className="flex items-center"
              style={{
                background: 'var(--bg-input)',
                borderRadius: 'var(--radius-sm)',
                border: '1.5px solid var(--orange)',
                overflow: 'hidden',
              }}
            >
              <button
                onClick={() => onRemove(mix.id)}
                style={{
                  width: 36,
                  height: 36,
                  background: 'transparent',
                  border: 'none',
                  fontSize: 18,
                  fontWeight: 800,
                  color: 'var(--orange)',
                  cursor: 'pointer',
                  fontFamily: "'Nunito', sans-serif",
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                −
              </button>
              <span
                style={{
                  width: 28,
                  textAlign: 'center',
                  fontSize: 15,
                  fontWeight: 800,
                  color: 'var(--text)',
                }}
              >
                {quantity}
              </span>
              <button
                onClick={() => onAdd(mix)}
                disabled={maxReached}
                style={{
                  width: 36,
                  height: 36,
                  background: 'transparent',
                  border: 'none',
                  fontSize: 18,
                  fontWeight: 800,
                  color: maxReached ? 'var(--text-muted)' : 'var(--orange)',
                  cursor: maxReached ? 'not-allowed' : 'pointer',
                  fontFamily: "'Nunito', sans-serif",
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                +
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
