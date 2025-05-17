import { createRuneForgeStore, createSpellApiServiceClient, RuneForgeState } from '@grimos/shared-utils-ts';

// Create API client
const API_BASE_URL = process.env.NEXT_PUBLIC_GRIMOS_API_URL || 'http://localhost:8000/api/v1';
const spellApiClient = createSpellApiServiceClient(API_BASE_URL);

// Create store with API client
export const useRuneForgeStore = createRuneForgeStore({
  apiClient: spellApiClient,
  debug: process.env.NODE_ENV === 'development'
});

// Re-export for convenience
export { initialSpellMetadata } from '@grimos/shared-utils-ts';
export type { RuneForgeState };
