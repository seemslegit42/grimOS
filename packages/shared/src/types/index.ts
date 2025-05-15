// Shared types between frontend and backend

export interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
}

// Add more shared types as needed
