// Filepath: /home/brylow/grimOS/apps/frontend/lib/authStore.ts
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  // Add other relevant user properties
}

interface AuthState {
  access_token: string | null;
  refresh_token: string | null;
  user: User | null;
  is_authenticated: boolean;
  setTokens: (access_token: string, refresh_token: string) => void;
  setUser: (user: User | null) => void;
  clearAuth: () => void;
  // Potentially add loading/error states for async operations
  is_loading: boolean;
  error: string | null;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      access_token: null,
      refresh_token: null,
      user: null,
      is_authenticated: false,
      is_loading: false,
      error: null,
      setTokens: (access_token, refresh_token) => {
        set({
          access_token,
          refresh_token,
          is_authenticated: !!access_token, // Considered authenticated if access token exists
        });
      },
      setUser: (user) => {
        set({ user });
      },
      clearAuth: () => {
        set({
          access_token: null,
          refresh_token: null,
          user: null,
          is_authenticated: false,
          error: null,
        });
        // Potentially clear other related storage or cookies if necessary
      },
      setLoading: (loading) => set({ is_loading: loading }),
      setError: (error) => set({ error }),
    }),
    {
      name: 'grimos-auth-storage', // Name for the persisted storage item
      storage: createJSONStorage(() => localStorage), // Use localStorage for persistence
      // Only persist specific parts of the store if needed
      // partialize: (state) => ({ 
      //   access_token: state.access_token, 
      //   refresh_token: state.refresh_token, 
      //   user: state.user,
      //   is_authenticated: state.is_authenticated
      // }),
    }
  )
);

// Selector for convenience
export const selectIsAuthenticated = (state: AuthState) => state.is_authenticated;
export const selectUser = (state: AuthState) => state.user;
export const selectAuthToken = (state: AuthState) => state.access_token;
