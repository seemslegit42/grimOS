// Export shared types here
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
}

export interface Permission {
  id: string;
  name: string;
  description?: string;
}

export interface UserRole {
  userId: string;
  roleId: string;
}

export interface RolePermission {
  roleId: string;
  permissionId: string;
}

// Export all RuneForge related types
export * from './rune-forge';
