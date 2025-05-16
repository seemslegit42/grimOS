/**
 * @file ErrorBoundary component
 * @description A React error boundary component to catch and display errors gracefully
 */

import { AlertTriangle } from 'lucide-react';
import { Component, ErrorInfo, ReactNode } from 'react';
import { cn } from '../utils';

export interface ErrorBoundaryProps {
  /**
   * Children components to render
   */
  children: ReactNode;
  
  /**
   * Custom fallback component to render when an error occurs
   * If not provided, a default error UI will be shown
   */
  fallback?: ReactNode | ((error: Error, resetError: () => void) => ReactNode);
  
  /**
   * Callback function called when an error is caught
   */
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  
  /**
   * Additional CSS classes for the default error UI
   */
  className?: string;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

/**
 * A React error boundary component to catch and display errors gracefully
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
    };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log the error to an error reporting service
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
    
    // Call the onError callback if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  resetError = (): void => {
    this.setState({
      hasError: false,
      error: null,
    });
  };

  render(): ReactNode {
    const { hasError, error } = this.state;
    const { children, fallback, className } = this.props;

    if (hasError && error) {
      // If a custom fallback is provided, use it
      if (fallback) {
        if (typeof fallback === 'function') {
          return fallback(error, this.resetError);
        }
        return fallback;
      }

      // Default error UI
      return (
        <div 
          className={cn(
            'p-4 rounded-md bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800',
            'flex flex-col items-center justify-center text-center space-y-4',
            'min-h-[200px] w-full max-w-md mx-auto my-4',
            className
          )}
        >
          <AlertTriangle className="h-12 w-12 text-red-500" />
          <div>
            <h3 className="text-lg font-medium text-red-800 dark:text-red-200">
              Something went wrong
            </h3>
            <div className="mt-2 text-sm text-red-700 dark:text-red-300">
              <p>
                {error.message || 'An unexpected error occurred'}
              </p>
            </div>
          </div>
          <button
            onClick={this.resetError}
            className={cn(
              'px-4 py-2 text-sm font-medium rounded-md',
              'bg-red-100 dark:bg-red-800 text-red-800 dark:text-red-100',
              'hover:bg-red-200 dark:hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500'
            )}
          >
            Try again
          </button>
        </div>
      );
    }

    return children;
  }
}

export default ErrorBoundary;