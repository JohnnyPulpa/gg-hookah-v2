import { InputHTMLAttributes, ReactNode } from 'react';

interface CheckboxProps extends InputHTMLAttributes<HTMLInputElement> {
  label: ReactNode;
}

export default function Checkbox({ 
  label, 
  className = '',
  ...props 
}: CheckboxProps) {
  return (
    <label className={`flex items-start gap-3 cursor-pointer ${className}`}>
      <input
        type="checkbox"
        className="mt-1 w-5 h-5 rounded border-light-border text-brand-orange focus:ring-brand-orange focus:ring-2 cursor-pointer"
        {...props}
      />
      <span className="text-sm text-light-text dark:text-dark-text select-none">
        {label}
      </span>
    </label>
  );
}
