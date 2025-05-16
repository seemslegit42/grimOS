/**
 * @file Testing utilities for grimOS frontend applications
 * @description Shared testing utilities to standardize testing across the application
 */

import { render, RenderOptions } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ReactElement } from 'react';

/**
 * Custom render function that includes common providers
 * This can be extended to include any providers needed for testing
 */
export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return {
    user: userEvent.setup(),
    ...render(ui, {
      // Add any providers here (ThemeProvider, StoreProvider, etc.)
      // wrapper: ({ children }) => (
      //   <ThemeProvider>
      //     <StoreProvider>{children}</StoreProvider>
      //   </ThemeProvider>
      // ),
      ...options,
    }),
  };
}

/**
 * Mock response generator for API testing
 */
export function mockApiResponse<T>(data: T, status = 200, headers = {}) {
  return {
    data,
    status,
    headers,
    config: {},
    statusText: status === 200 ? 'OK' : 'Error',
  };
}

/**
 * Mock error response generator for API testing
 */
export function mockApiError(
  status = 500,
  message = 'Internal Server Error',
  code = 'INTERNAL_SERVER_ERROR'
) {
  const error = new Error(message) as Error & {
    response: {
      status: number;
      data: {
        message: string;
        code: string;
      };
    };
  };
  
  error.response = {
    status,
    data: {
      message,
      code,
    },
  };
  
  return error;
}

/**
 * Wait for a condition to be true
 * Useful for testing async operations
 */
export async function waitForCondition(
  condition: () => boolean,
  timeout = 1000,
  interval = 50
): Promise<void> {
  const startTime = Date.now();
  
  return new Promise((resolve, reject) => {
    const check = () => {
      if (condition()) {
        resolve();
        return;
      }
      
      if (Date.now() - startTime > timeout) {
        reject(new Error(`Condition not met within ${timeout}ms`));
        return;
      }
      
      setTimeout(check, interval);
    };
    
    check();
  });
}

/**
 * Create a mock for window.matchMedia
 * Useful for testing responsive components
 */
export function setupMatchMediaMock(matches: boolean) {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
      matches,
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });
}

/**
 * Mock IntersectionObserver for testing components that use it
 */
export function setupIntersectionObserverMock() {
  class IntersectionObserverMock {
    readonly root: Element | null = null;
    readonly rootMargin: string = '';
    readonly thresholds: ReadonlyArray<number> = [];
    
    constructor(private callback: IntersectionObserverCallback) {}
    
    observe = jest.fn();
    unobserve = jest.fn();
    disconnect = jest.fn();
    takeRecords = jest.fn();
    
    // Helper to trigger the callback
    triggerCallback(entries: IntersectionObserverEntry[]) {
      this.callback(entries, this);
    }
  }
  
  Object.defineProperty(window, 'IntersectionObserver', {
    writable: true,
    value: IntersectionObserverMock,
  });
  
  return IntersectionObserverMock;
}