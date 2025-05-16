/**
 * @file LoadingSpinner component
 * @description A customizable loading spinner component with cyberpunk styling
 */

import { motion } from 'framer-motion';
import React from 'react';
import { cn } from '../utils';

export interface LoadingSpinnerProps {
  /**
   * Size of the spinner
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  
  /**
   * Color variant of the spinner
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'accent' | 'success' | 'warning' | 'error';
  
  /**
   * Optional text to display below the spinner
   */
  text?: string;
  
  /**
   * Additional CSS classes
   */
  className?: string;
}

/**
 * A customizable loading spinner component with cyberpunk styling
 */
export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  variant = 'primary',
  text,
  className,
}) => {
  // Size mappings
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
    xl: 'w-16 h-16 border-4',
  };
  
  // Color variant mappings
  const variantClasses = {
    primary: 'border-t-primary',
    secondary: 'border-t-secondary',
    accent: 'border-t-accent',
    success: 'border-t-green-500',
    warning: 'border-t-yellow-500',
    error: 'border-t-red-500',
  };
  
  // Text size mappings
  const textSizeClasses = {
    sm: 'text-xs mt-1',
    md: 'text-sm mt-2',
    lg: 'text-base mt-2',
    xl: 'text-lg mt-3',
  };
  
  return (
    <div className={cn('flex flex-col items-center justify-center', className)}>
      <motion.div
        className={cn(
          'rounded-full border-transparent animate-spin',
          'border-b-gray-700/20 border-l-gray-700/20 border-r-gray-700/20',
          sizeClasses[size],
          variantClasses[variant]
        )}
        animate={{ rotate: 360 }}
        transition={{ 
          duration: 1.5, 
          repeat: Infinity, 
          ease: "linear" 
        }}
      />
      
      {text && (
        <p className={cn('text-foreground/80', textSizeClasses[size])}>
          {text}
        </p>
      )}
    </div>
  );
};

export default LoadingSpinner;