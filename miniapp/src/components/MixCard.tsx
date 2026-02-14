import { Mix } from '../types';

interface MixCardProps {
  mix: Mix;
  onChoose: (mix: Mix) => void;
  buttonText: string;
}

export default function MixCard({ mix, onChoose, buttonText }: MixCardProps) {
  const characteristics = [
    { label: 'Strength', value: mix.characteristics.strength, emoji: '💪' },
    { label: 'Coolness', value: mix.characteristics.coolness, emoji: '❄️' },
    { label: 'Sweetness', value: mix.characteristics.sweetness, emoji: '🍬' },
    { label: 'Smokiness', value: mix.characteristics.smokiness, emoji: '💨' },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 overflow-hidden">
      {/* Image */}
      <div className="aspect-video bg-gray-200 rounded-lg overflow-hidden -mx-4 -mt-4 mb-4">
        {mix.image_url ? (
          <img src={mix.image_url} alt={mix.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-4xl">🌿</div>
        )}
      </div>

      {/* Content */}
      <div className="space-y-3">
        <div>
          <h3 className="text-lg font-bold text-orange-500">{mix.name}</h3>
          <p className="text-sm text-gray-500">{mix.flavors}</p>
        </div>

        {/* Characteristics */}
        <div className="grid grid-cols-2 gap-2">
          {characteristics.map((char) => (
            <div key={char.label} className="flex items-center gap-2">
              <span className="text-lg">{char.emoji}</span>
              <div className="flex-1">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-500">{char.label}</span>
                  <span className="font-medium">{char.value}/5</span>
                </div>
                <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-orange-500 rounded-full transition-all"
                    style={{ width: `${(char.value / 5) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Price & Button */}
        <div className="flex items-center justify-between pt-2">
          <span className="text-2xl font-bold text-orange-500">{mix.price}₾</span>
          <button
            onClick={() => onChoose(mix)}
            className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-4 py-2 rounded-xl transition-colors"
          >
            {buttonText}
          </button>
        </div>
      </div>
    </div>
  );
}
