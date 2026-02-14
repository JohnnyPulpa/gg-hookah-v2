import { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  children: ReactNode;
}

export default function Button({ 
  variant = 'primary', 
  children, 
  className = '',
  disabled,
  ...props 
}: ButtonProps) {
  const baseStyles = 'px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-brand-orange text-white hover:bg-orange-600 active:bg-orange-700',
    secondary: 'border-2 border-brand-orange text-brand-orange hover:bg-brand-orange hover:text-white',
    ghost: 'text-brand-orange hover:bg-orange-50 dark:hover:bg-dark-surface'
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
