import { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export default function Input({ 
  label, 
  error, 
  className = '',
  ...props 
}: InputProps) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-light-text dark:text-dark-text">
          {label}
        </label>
      )}
      <input
        className={`w-full px-4 py-2 rounded-lg border bg-light-bg dark:bg-dark-bg text-light-text dark:text-dark-text ${
          error 
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-light-border focus:ring-brand-orange'
        } focus:outline-none focus:ring-2 transition-colors ${className}`}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}
