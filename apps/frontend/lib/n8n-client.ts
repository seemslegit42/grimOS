// n8n-client.ts

import axios, { AxiosInstance, AxiosError } from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const N8N_API_KEY = process.env.N8N_API_KEY;
const N8N_BASE_URL = process.env.N8N_BASE_URL || 'http://localhost:5678/api/v1'; // Default local n8n URL

if (!N8N_API_KEY) {
  console.warn('N8N_API_KEY is not set in environment variables. n8n client may not function correctly.');
}

if (!N8N_BASE_URL) {
  console.warn('N8N_BASE_URL is not set in environment variables. Using default: http://localhost:5678/api/v1');
}

/**
 * Represents the structure of an n8n workflow (Spell).
 * This is a simplified type based on common n8n workflow structure.
 */
export interface Spell {
  id: string;
  name: string;
  active: boolean;
  nodes: any[]; // Simplified representation of nodes (Runes)
  settings: any; // Workflow settings
  // Add other relevant workflow properties as needed
}

/**
 * Represents the structure of an n8n execution.
 */
export interface Execution {
  id: string;
  workflowId: string;
  status: 'running' | 'completed' | 'failed' | 'stopped';
  startedAt: string;
  stoppedAt: string | null;
  data: any; // Execution data/output
  // Add other relevant execution properties as needed
}

/**
 * Represents the structure of an n8n node type (Rune).
 * Note: n8n API may not have a direct endpoint for listing all node types with full definitions.
 * This type is a placeholder and might need adjustment based on how Rune data is sourced.
 */
export interface Rune {
  name: string;
  description?: string;
  // Add other relevant node type properties as needed
}


class N8nClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: N8N_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
        'X-N8N-API-KEY': N8N_API_KEY,
      },
    });

    // Add a response interceptor for basic error logging
    this.client.interceptors.response.use(
      response => response,
      (error: AxiosError) => {
        console.error('n8n API Error:', error.message);
        if (error.response) {
          console.error('Status:', error.response.status);
          console.error('Data:', error.response.data);
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * Fetches all available workflows (Spells) from n8n.
   * @returns A promise that resolves with a list of Spells.
   */
  async fetchSpells(): Promise<Spell[]> {
    try {
      const response = await this.client.get('/workflows');
      // n8n API typically returns { data: [...] } for lists
      return response.data.data as Spell[];
    } catch (error) {
      console.error('Error fetching Spells:', error);
      throw error;
    }
  }

  /**
   * Fetches the JSON definition of a specific workflow (Spell) by its ID.
   * @param spellId The ID of the Spell (n8n workflow ID).
   * @returns A promise that resolves with the Spell definition.
   */
  async fetchSpellDefinition(spellId: string): Promise<Record<string, any>> {
    try {
      const response = await this.client.get(`/workflows/${spellId}`);
      return response.data as Record<string, any>; // n8n returns the workflow object directly
    } catch (error) {
      console.error(`Error fetching Spell definition for ID ${spellId}:`, error);
      throw error;
    }
  }

  /**
   * Fetches the available node types (Runes) from n8n.
   * Note: This might need adjustment based on actual n8n API capabilities for listing node types.
   * As of now, there isn't a direct public API endpoint for this.
   * A potential approach could be to list credentials, or rely on known node types, or a custom endpoint.
   * For this implementation, we'll return a placeholder or adapt if an endpoint becomes available.
   * @returns A promise that resolves with a list of Rune types.
   */
  async fetchRunes(): Promise<Rune[]> {
    // NOTE: n8n public API does not currently have a direct endpoint to list all node types (Runes).
    // This method is a placeholder. You might need a custom solution or alternative data source.
    console.warn('Fetching Runes (n8n node types) is not directly supported by the standard n8n API.');
    console.warn('This method returns a placeholder list.');
    return Promise.resolve([
      { name: 'http', description: 'Make HTTP requests' },
      { name: 'function', description: 'Execute custom JavaScript code' },
      { name: 'set', description: 'Set values on items' },
      // Add more known node types as placeholders if useful
    ] as Rune[]);
  }

  /**
   * Triggers the execution of a specific workflow (Spell) with given inputs.
   * Note: n8n API execution endpoint expects the workflow definition, not just the ID for some trigger types.
   * For simplicity, this assumes a workflow that can be triggered via an external API call (like a Webhook).
   * A more robust implementation might require fetching the definition first or using specific trigger nodes.
   * This implementation assumes a Webhook trigger and sends data to it.
   * @param spellId The ID of the Spell (n8n workflow ID) to trigger.
   * @param inputs The data inputs for the workflow.
   * @returns A promise that resolves with the execution result or confirmation.
   */
  async triggerSpellExecution(spellId: string, inputs: Record<string, any>): Promise<any> {
    try {
      // NOTE: Triggering workflows in n8n depends heavily on the trigger node used.
      // This assumes a Webhook node setup to receive data via a POST request to its unique URL.
      // A typical n8n webhook URL format is: N8N_WEBHOOK_BASE_URL/webhook/YOUR_WEBHOOK_PATH
      // You would need the webhook path associated with the workflow.
      // The standard `/executions` endpoint is often for managing executions, not triggering by ID with arbitrary data.
      // A more common pattern is to call the specific webhook URL.
      // This implementation is simplified and assumes a mechanism to trigger via spellId, which
      // might require a custom endpoint or logic on the n8n side (e.g., a workflow triggered by HTTP Request node
      // that then runs another workflow by ID).

      // A direct trigger endpoint like this is not standard in n8n public API by default:
      // const response = await this.client.post(`/workflows/${spellId}/execute`, inputs);

      // A more realistic scenario for triggering with external data is using a webhook:
      // You would need the webhook URL for the specific workflow. This often requires knowing the webhook path.
      // Example (replace with actual webhook URL logic):
      // const webhookResponse = await axios.post(`${process.env.N8N_WEBHOOK_BASE_URL}/webhook/${webhookPathForSpellId}`, inputs);
      // return webhookResponse.data;

      console.warn(`Triggering Spell execution for ID ${spellId}: This implementation assumes a non-standard direct trigger mechanism.`);
      console.warn('A typical n8n workflow is triggered via a specific trigger node (e.g., Webhook).');

      // Placeholder or adapted implementation based on available API or custom setup:
      // If n8n is configured to allow triggering by ID via the API with input data,
      // the endpoint and payload might look different. Check your n8n setup/docs.
      // As a fallback or alternative if direct triggering isn't available via standard /workflows endpoint:
      // You might need to implement a workflow in n8n that is triggered by a webhook
      // and then uses the "Execute Workflow" node to run the target spellId with the provided inputs.
      // Then, this client would call that "triggering" workflow's webhook.

      // Let's assume a hypothetical or custom endpoint for demonstration:
      const response = await this.client.post(`/workflows/${spellId}/trigger`, inputs);
       return response.data;

    } catch (error) {
      console.error(`Error triggering Spell execution for ID ${spellId}:`, error);
      throw error;
    }
  }


  /**
   * Retrieves the status and logs of a workflow execution by its ID.
   * @param executionId The ID of the workflow execution.
   * @returns A promise that resolves with the Execution details.
   */
  async getExecutionStatus(executionId: string): Promise<Execution> {
    try {
      const response = await this.client.get(`/executions/${executionId}`);
      return response.data as Execution; // n8n returns the execution object directly
    } catch (error) {
      console.error(`Error fetching Execution status for ID ${executionId}:`, error);
      throw error;
    }
  }

  /**
   * Creates a new workflow (Spell) in n8n.
   * @param spellDefinition The JSON definition of the Spell (n8n workflow).
   * @returns A promise that resolves with the created Spell object.
   */
  async createSpell(spellDefinition: Record<string, any>): Promise<Spell> {
    try {
      const response = await this.client.post('/workflows', spellDefinition);
      return response.data as Spell; // n8n returns the created workflow object
    } catch (error) {
      console.error('Error creating Spell:', error);
      throw error;
    }
  }

  /**
   * Updates an existing workflow (Spell) in n8n by its ID.
   * @param spellId The ID of the Spell (n8n workflow) to update.
   * @param spellDefinition The updated JSON definition of the Spell.
   * @returns A promise that resolves with the updated Spell object.
   */
  async updateSpell(spellId: string, spellDefinition: Record<string, any>): Promise<Spell> {
    try {
      const response = await this.client.put(`/workflows/${spellId}`, spellDefinition);
      return response.data as Spell; // n8n returns the updated workflow object
    } catch (error) {
      console.error(`Error updating Spell with ID ${spellId}:`, error);
      throw error;
    }
  }

  /**
   * Deletes a workflow (Spell) in n8n by its ID.
   * @param spellId The ID of the Spell (n8n workflow) to delete.
   * @returns A promise that resolves when the deletion is successful.
   */
  async deleteSpell(spellId: string): Promise<void> {
    try {
      await this.client.delete(`/workflows/${spellId}`);
    } catch (error) {
      console.error(`Error deleting Spell with ID ${spellId}:`, error);
      throw error;
    }
  }
}

// Export an instance of the client for easy use
const n8nClient = new N8nClient();
export default n8nClient;