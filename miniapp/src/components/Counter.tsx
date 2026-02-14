interface CounterProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  className?: string;
}

export default function Counter({ 
  value, 
  onChange, 
  min = 0, 
  max = 99,
  className = '' 
}: CounterProps) {
  const handleDecrement = () => {
    if (value > min) {
      onChange(value - 1);
    }
  };

  const handleIncrement = () => {
    if (value < max) {
      onChange(value + 1);
    }
  };

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <button
        onClick={handleDecrement}
        disabled={value <= min}
        className="w-8 h-8 rounded-full bg-light-surface dark:bg-dark-surface border border-light-border flex items-center justify-center text-lg font-bold hover:bg-brand-orange hover:text-white hover:border-brand-orange disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        −
      </button>
      <span className="min-w-[2rem] text-center font-medium text-lg">
        {value}
      </span>
      <button
        onClick={handleIncrement}
        disabled={value >= max}
        className="w-8 h-8 rounded-full bg-light-surface dark:bg-dark-surface border border-light-border flex items-center justify-center text-lg font-bold hover:bg-brand-orange hover:text-white hover:border-brand-orange disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        +
      </button>
    </div>
  );
}
