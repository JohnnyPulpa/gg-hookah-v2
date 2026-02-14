import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}

export default function Card({ children, className = '', onClick }: CardProps) {
  const baseStyles = 'bg-light-surface dark:bg-dark-surface border border-light-border rounded-lg p-4 transition-shadow';
  const hoverStyles = onClick ? 'cursor-pointer hover:shadow-lg' : '';

  return (
    <div 
      className={`${baseStyles} ${hoverStyles} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
}
