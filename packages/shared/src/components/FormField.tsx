/**
 * @file FormField component
 * @description A reusable form field component with label, input, and error handling
 */

import React, { ReactNode } from 'react';
import { cn } from '../utils';

export interface FormFieldProps {
  /**
   * Field label
   */
  label: string;
  
  /**
   * Field name (used for id and htmlFor attributes)
   */
  name: string;
  
  /**
   * Error message to display
   */
  error?: string;
  
  /**
   * Help text to display below the field
   */
  helpText?: string;
  
  /**
   * Whether the field is required
   * @default false
   */
  required?: boolean;
  
  /**
   * Whether the field is disabled
   * @default false
   */
  disabled?: boolean;
  
  /**
   * Input element or custom component
   */
  children: ReactNode;
  
  /**
   * Additional CSS classes for the container
   */
  className?: string;
  
  /**
   * Additional CSS classes for the label
   */
  labelClassName?: string;
  
  /**
   * Additional CSS classes for the input container
   */
  inputClassName?: string;
}

/**
 * A reusable form field component with label, input, and error handling
 */
export const FormField: React.FC<FormFieldProps> = ({
  label,
  name,
  error,
  helpText,
  required = false,
  disabled = false,
  children,
  className,
  labelClassName,
  inputClassName,
}) => {
  return (
    <div className={cn('space-y-2', className)}>
      <div className="flex justify-between">
        <label 
          htmlFor={name}
          className={cn(
            'block text-sm font-medium',
            disabled ? 'text-gray-400 dark:text-gray-500' : 'text-gray-700 dark:text-gray-200',
            labelClassName
          )}
        >
          {label}
          {required && <span className="ml-1 text-red-500">*</span>}
        </label>
      </div>
      
      <div className={cn('relative', inputClassName)}>
        {children}
      </div>
      
      {(error || helpText) && (
        <div className="mt-1">
          {error ? (
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          ) : helpText ? (
            <p className="text-sm text-gray-500 dark:text-gray-400">{helpText}</p>
          ) : null}
        </div>
      )}
    </div>
  );
};

export default FormField;