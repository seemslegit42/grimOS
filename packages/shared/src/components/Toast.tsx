/**
 * @file Toast component
 * @description A customizable toast notification component with cyberpunk styling
 */

import { motion } from 'framer-motion';
import {
    AlertCircle,
    AlertTriangle,
    CheckCircle,
    Info,
    X
} from 'lucide-react';
import React from 'react';
import { cn } from '../utils';

export type ToastVariant = 'info' | 'success' | 'warning' | 'error';

export interface ToastProps {
  /**
   * Unique identifier for the toast
   */
  id: string;
  
  /**
   * Toast title
   */
  title: string;
  
  /**
   * Optional toast description
   */
  description?: string;
  
  /**
   * Toast variant
   * @default 'info'
   */
  variant?: ToastVariant;
  
  /**
   * Whether the toast is visible
   * @default true
   */
  visible?: boolean;
  
  /**
   * Function to close the toast
   */
  onClose: (id: string) => void;
  
  /**
   * Duration in milliseconds before auto-closing
   * Set to 0 to disable auto-closing
   * @default 5000
   */
  duration?: number;
  
  /**
   * Additional CSS classes
   */
  className?: string;
}

/**
 * A customizable toast notification component with cyberpunk styling
 */
export const Toast: React.FC<ToastProps> = ({
  id,
  title,
  description,
  variant = 'info',
  visible = true,
  onClose,
  duration = 5000,
  className,
}) => {
  // Auto-close timer
  React.useEffect(() => {
    if (duration > 0 && visible) {
      const timer = setTimeout(() => {
        onClose(id);
      }, duration);
      
      return () => clearTimeout(timer);
    }
  }, [duration, id, onClose, visible]);
  
  // Variant styles
  const variantStyles = {
    info: {
      container: 'border-blue-500 bg-blue-50 dark:bg-blue-900/20',
      icon: <Info className="h-5 w-5 text-blue-500" />,
      title: 'text-blue-800 dark:text-blue-200',
      description: 'text-blue-700 dark:text-blue-300',
    },
    success: {
      container: 'border-green-500 bg-green-50 dark:bg-green-900/20',
      icon: <CheckCircle className="h-5 w-5 text-green-500" />,
      title: 'text-green-800 dark:text-green-200',
      description: 'text-green-700 dark:text-green-300',
    },
    warning: {
      container: 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20',
      icon: <AlertTriangle className="h-5 w-5 text-yellow-500" />,
      title: 'text-yellow-800 dark:text-yellow-200',
      description: 'text-yellow-700 dark:text-yellow-300',
    },
    error: {
      container: 'border-red-500 bg-red-50 dark:bg-red-900/20',
      icon: <AlertCircle className="h-5 w-5 text-red-500" />,
      title: 'text-red-800 dark:text-red-200',
      description: 'text-red-700 dark:text-red-300',
    },
  };
  
  const styles = variantStyles[variant];
  
  if (!visible) return null;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ duration: 0.2 }}
      className={cn(
        'w-full max-w-sm rounded-lg border-l-4 p-4 shadow-md',
        'backdrop-blur-sm bg-opacity-90 dark:bg-opacity-90',
        'flex items-start gap-3',
        styles.container,
        className
      )}
    >
      <div className="flex-shrink-0">
        {styles.icon}
      </div>
      
      <div className="flex-1 pt-0.5">
        <h3 className={cn('text-sm font-medium', styles.title)}>
          {title}
        </h3>
        
        {description && (
          <p className={cn('mt-1 text-sm', styles.description)}>
            {description}
          </p>
        )}
      </div>
      
      <button
        type="button"
        className="flex-shrink-0 ml-4 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        onClick={() => onClose(id)}
      >
        <span className="sr-only">Close</span>
        <X className="h-5 w-5" />
      </button>
    </motion.div>
  );
};

export default Toast;