import { createSpellApiServiceClient, SpellData } from '@grimos/shared-utils-ts';

// Create and export the client instance
const API_BASE_URL = process.env.NEXT_PUBLIC_GRIMOS_API_URL || 'http://localhost:8000/api/v1';

// Using the factory from the shared package
const SpellApiServiceClient = createSpellApiServiceClient(API_BASE_URL);

export default SpellApiServiceClient;
export type { SpellData };
const API_BASE_URL = process.env.NEXT_PUBLIC_GRIMOS_API_URL || 'http://localhost:8000/api/v1';

/**
 * SpellApiServiceClient
 * 
 * Client for interacting with the grimOS backend Spellbook API.
 */
export const SpellApiServiceClient = {
  /**
   * Fetches a specific spell from the backend.
   * @param spell_id The ID of the spell to fetch.
   * @returns A Promise resolving to the SpellData.
   * @throws Error if the fetch operation fails.
   */
  async fetchSpellFromBackend(spell_id: string): Promise<SpellData> {
    const response = await fetch(`${API_BASE_URL}/spells/${spell_id}`);

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
    const url = spellData.id ? `${API_BASE_URL}/spells/${spellData.id}` : `${API_BASE_URL}/spells/`;
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
    const response = await fetch(`${API_BASE_URL}/spells/`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Network response was not ok and failed to parse error JSON.' }));
      throw new Error(errorData.detail || `Failed to fetch all spells. Status: ${response.status}`);
    }
    return response.json() as Promise<SpellData[]>;
  }
};

// Example usage (for testing or demonstration):
/*
async function testClient() {
  try {
    // Create a new spell
    const newSpell: SpellData = {
      id: null, // New spell
      name: 'My Awesome New Spell',
      description: 'This spell does amazing things!',
      isPublic: false,
      isTemplate: false,
      workflow_json: {
        nodes: [{
          parameters: {},
          name: 'Start',
          type: 'n8n-nodes-base.start',
          typeVersion: 1,
          position: [250, 300],
          id: 'e9e08801-1a96-400e-8a73-8606d49e6a09',
        }],
        connections: {},
      },
    };
    console.log('Attempting to save new spell:', newSpell);
    const savedSpell = await SpellApiServiceClient.saveSpellToBackend(newSpell);
    console.log('Saved spell:', savedSpell);

    if (savedSpell.id) {
      // Fetch the saved spell
      console.log(`Attempting to fetch spell: ${savedSpell.id}`);
      const fetchedSpell = await SpellApiServiceClient.fetchSpellFromBackend(savedSpell.id);
      console.log('Fetched spell:', fetchedSpell);

      // Update the spell
      fetchedSpell.description = 'This spell now does even MORE amazing things!';
      fetchedSpell.workflow_json.nodes.push({
        parameters: { command: 'echo \'Hello World!\'' },
        name: 'Execute Command',
        type: 'n8n-nodes-base.executeCommand',
        typeVersion: 1,
        position: [450, 300],
        id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
      });
      console.log('Attempting to update spell:', fetchedSpell);
      const updatedSpell = await SpellApiServiceClient.saveSpellToBackend(fetchedSpell);
      console.log('Updated spell:', updatedSpell);
    }
    
    // Fetch all spells
    console.log('Attempting to fetch all spells...');
    const allSpells = await SpellApiServiceClient.fetchAllSpells();
    console.log('All spells:', allSpells);

  } catch (error) {
    console.error('SpellApiServiceClient test failed:', error);
  }
}

// testClient(); 
*/
