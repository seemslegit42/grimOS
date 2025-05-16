# grimOS Shared Components and Utilities

This package contains shared UI components, utilities, and types for grimOS frontend applications.

## Installation

```bash
pnpm add @bitbrew/shared
```

## Components

### Core UI Components

- **Button**: A customizable button component with various styles and variants.
- **CyberpunkBackground**: A cyberpunk-themed background component with animated elements.
- **ErrorBoundary**: A React error boundary component to catch and display errors gracefully.
- **FormField**: A reusable form field component with label, input, and error handling.
- **GlassmorphicCard**: A card component with glassmorphic styling.
- **GlassmorphicModal**: A modal component with glassmorphic styling.
- **LoadingSpinner**: A customizable loading spinner component with cyberpunk styling.
- **Toast**: A customizable toast notification component with cyberpunk styling.

### Usage Examples

#### ErrorBoundary

```tsx
import { ErrorBoundary } from '@bitbrew/shared';

function App() {
  return (
    <ErrorBoundary
      fallback={(error, resetError) => (
        <div>
          <h2>Something went wrong!</h2>
          <p>{error.message}</p>
          <button onClick={resetError}>Try again</button>
        </div>
      )}
      onError={(error, errorInfo) => {
        // Log error to monitoring service
        console.error('Error caught by ErrorBoundary:', error, errorInfo);
      }}
    >
      <YourComponent />
    </ErrorBoundary>
  );
}
```

#### LoadingSpinner

```tsx
import { LoadingSpinner } from '@bitbrew/shared';

function LoadingState() {
  return (
    <div className="flex items-center justify-center h-screen">
      <LoadingSpinner 
        size="lg" 
        variant="primary" 
        text="Loading data..." 
      />
    </div>
  );
}
```

#### Toast

```tsx
import { Toast } from '@bitbrew/shared';
import { useState } from 'react';

function ToastExample() {
  const [toasts, setToasts] = useState([
    { id: '1', title: 'Success', description: 'Operation completed successfully', variant: 'success' },
  ]);

  const closeToast = (id) => {
    setToasts(toasts.filter(toast => toast.id !== id));
  };

  return (
    <div className="fixed top-4 right-4 space-y-4 z-50">
      {toasts.map(toast => (
        <Toast
          key={toast.id}
          id={toast.id}
          title={toast.title}
          description={toast.description}
          variant={toast.variant}
          onClose={closeToast}
        />
      ))}
    </div>
  );
}
```

## Utilities

### Error Handling

The package provides standardized error handling utilities:

```tsx
import { createAppError, ErrorType, handleApiError, showErrorToast } from '@bitbrew/shared';

// Create a standardized error
const error = createAppError(
  ErrorType.VALIDATION,
  'Invalid input data',
  { code: 'INVALID_INPUT', details: { field: 'email' } }
);

// Handle API errors
try {
  // API call
} catch (err) {
  const appError = handleApiError(err);
  showErrorToast(appError);
  logError(appError);
}
```

### Testing Utilities

The package provides testing utilities to standardize testing across the application:

```tsx
import { renderWithProviders, mockApiResponse, waitForCondition } from '@bitbrew/shared';

// Render a component with providers
const { user, ...result } = renderWithProviders(<YourComponent />);

// Mock API response
const mockResponse = mockApiResponse({ id: 1, name: 'Test' }, 200);

// Wait for a condition to be true
await waitForCondition(() => screen.queryByText('Loaded') !== null);
```

### Other Utilities

- **cn**: Utility function to merge Tailwind CSS classes
- **formatDate**: Format a date to YYYY-MM-DD
- **generateRandomString**: Generate a random string with specified length
- **debounce**: Debounce a function call
- **throttle**: Throttle a function call
- **deepClone**: Deep clone an object
- **formatBytes**: Format bytes to human-readable string

## Types

The package provides shared types for use across the application:

```tsx
import { User, ApiResponse, PaginationParams } from '@bitbrew/shared';

// Use the types in your components
const fetchUsers = async (params: PaginationParams): Promise<ApiResponse<User[]>> => {
  // Implementation
};
```

## Contributing

When adding new components or utilities to this package, please follow these guidelines:

1. Use PascalCase for component names and camelCase for utility functions
2. Add proper JSDoc comments to document the component or utility
3. Export the component or utility from the appropriate index.ts file
4. Update this README.md with documentation for the new component or utility
5. Add tests for the new component or utility

## License

MIT