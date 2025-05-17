import { N8nWorkflowJsonType, SpellMetadata } from '@grimos/shared-types';

// Define the structure of the spell data as expected by/from the backend
export interface SpellData extends SpellMetadata {
  workflow_json: N8nWorkflowJsonType;
  // Potentially other fields like user_id, created_at, updated_at if returned by backend
}

/**
 * SpellApiServiceClient factory
 * Creates a client for interacting with the grimOS backend Spellbook API.
 * @param baseUrl Base URL for the API
 * @returns SpellApiService client instance
 */
export const createSpellApiServiceClient = (baseUrl: string = 'http://localhost:8000/api/v1') => {
  return {
    /**
     * Fetches a specific spell from the backend.
     * @param spell_id The ID of the spell to fetch.
     * @returns A Promise resolving to the SpellData.
     * @throws Error if the fetch operation fails.
     */
    async fetchSpellFromBackend(spell_id: string): Promise<SpellData> {
      const response = await fetch(`${baseUrl}/spells/${spell_id}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network response was not ok and failed to parse error JSON.' }));
        throw new Error(errorData.detail || `Failed to fetch spell ${spell_id}. Status: ${response.status}`);
      }

      return response.json() as Promise<SpellData>;
    },

    /**
     * Saves a spell (either new or existing) to the backend.
     * The backend should handle creation (if id is null or not found) or update.
     * @param spellData The complete spell data to save.
     * @returns A Promise resolving to the saved SpellData (which might include a new ID or updated timestamps).
     * @throws Error if the save operation fails.
     */
    async saveSpellToBackend(spellData: SpellData): Promise<SpellData> {
      const url = spellData.id ? `${baseUrl}/spells/${spellData.id}` : `${baseUrl}/spells/`;
      const method = spellData.id ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          // Add any necessary authentication headers here, e.g.,
          // 'Authorization': `Bearer ${your_auth_token}`,
        },
        body: JSON.stringify(spellData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network response was not ok and failed to parse error JSON.' }));
        throw new Error(errorData.detail || `Failed to save spell. Status: ${response.status}`);
      }

      return response.json() as Promise<SpellData>;
    },

    /**
     * Fetches all spells, potentially with pagination or filtering in the future.
     * @returns A Promise resolving to an array of SpellData.
     * @throws Error if the fetch operation fails.
     */
    async fetchAllSpells(): Promise<SpellData[]> {
      const response = await fetch(`${baseUrl}/spells/`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network response was not ok and failed to parse error JSON.' }));
        throw new Error(errorData.detail || `Failed to fetch all spells. Status: ${response.status}`);
      }
      return response.json() as Promise<SpellData[]>;
    }
  };
};
