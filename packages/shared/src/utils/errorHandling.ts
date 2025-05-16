/**
 * @file Error handling utilities for grimOS
 * @description Standardized error handling utilities for frontend applications
 */

import { toast } from 'sonner';

/**
 * Standard error types used across the application
 */
export enum ErrorType {
  NETWORK = 'NETWORK',
  AUTHENTICATION = 'AUTHENTICATION',
  AUTHORIZATION = 'AUTHORIZATION',
  VALIDATION = 'VALIDATION',
  SERVER = 'SERVER',
  NOT_FOUND = 'NOT_FOUND',
  TIMEOUT = 'TIMEOUT',
  UNKNOWN = 'UNKNOWN',
}

/**
 * Standard error interface
 */
export interface AppError {
  type: ErrorType;
  message: string;
  code?: string;
  details?: Record<string, unknown>;
  originalError?: unknown;
}

/**
 * Create a standardized application error
 */
export function createAppError(
  type: ErrorType,
  message: string,
  options?: {
    code?: string;
    details?: Record<string, unknown>;
    originalError?: unknown;
  }
): AppError {
  return {
    type,
    message,
    code: options?.code,
    details: options?.details,
    originalError: options?.originalError,
  };
}

/**
 * Handle API errors in a standardized way
 */
export function handleApiError(error: unknown): AppError {
  // Handle axios or fetch errors
  if (error instanceof Error) {
    if (error.message.includes('network') || error.message.includes('connection')) {
      return createAppError(
        ErrorType.NETWORK,
        'Network error occurred. Please check your connection.',
        { originalError: error }
      );
    }

    if (error.message.includes('timeout')) {
      return createAppError(
        ErrorType.TIMEOUT,
        'Request timed out. Please try again.',
        { originalError: error }
      );
    }

    // Handle other specific error types based on message or properties
    // ...

    return createAppError(
      ErrorType.UNKNOWN,
      'An unexpected error occurred.',
      { originalError: error }
    );
  }

  // Default unknown error
  return createAppError(
    ErrorType.UNKNOWN,
    'An unexpected error occurred.',
    { originalError: error }
  );
}

/**
 * Display error toast with standardized styling
 */
export function showErrorToast(error: AppError): void {
  toast.error(error.message, {
    description: error.code ? `Error code: ${error.code}` : undefined,
    duration: 5000,
  });
}

/**
 * Log error to monitoring service (can be configured to use different services)
 */
export function logError(error: AppError): void {
  // In development, log to console
  if (process.env.NODE_ENV === 'development') {
    console.error('[ERROR]', {
      type: error.type,
      message: error.message,
      code: error.code,
      details: error.details,
      originalError: error.originalError,
    });
  }

  // In production, this would send to error monitoring service
  // Example: Sentry.captureException(error.originalError || error);
}

/**
 * Utility to safely parse JSON with error handling
 */
export function safeJsonParse<T>(json: string, fallback: T): T {
  try {
    return JSON.parse(json) as T;
  } catch (error) {
    logError(
      createAppError(
        ErrorType.VALIDATION,
        'Failed to parse JSON data',
        { originalError: error }
      )
    );
    return fallback;
  }
}