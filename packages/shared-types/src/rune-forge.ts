
/**
 * RuneForge Node Data
 * Contains the data structure for nodes in the RuneForge canvas
 */
export interface RuneForgeNodeData {
  label: string;
  n8nNodeType: string;
  parameters: Record<string, any>;
  iconName?: string;
  status?: 'idle' | 'running' | 'success' | 'error';
  // Additional metadata specific to RuneForge
}

/**
 * Form Field Definition
 * Used to dynamically generate form fields for rune parameters
 */
export interface FormFieldDefinitionType {
  name: string;
  label: string;
  fieldType: 'text' | 'select' | 'textarea' | 'boolean' | 'json';
  options?: Array<{ value: string; label: string }>;
  defaultValue?: string | number | boolean | Record<string, any> | Array<any>;
  required?: boolean;
  description?: string;
  trueLabel?: string;
  falseLabel?: string;
}

/**
 * Available Rune Type
 * Defines the structure of available runes that can be used in the RuneForge
 */
export interface AvailableRuneType {
  id: string;
  displayName: string;
  category: string;
  iconName?: string;
  parametersSchema: FormFieldDefinitionType[];
  description?: string;
  name: string;
  parameters: any[];
}

/**
 * Spell Metadata
 * Contains metadata about a spell (workflow)
 */
export interface SpellMetadata {
  id: string | null;
  name: string;
  description: string;
  isPublic: boolean;
  isTemplate: boolean;
}

/**
 * N8N Type Definitions
 */

// N8N Node Type
export interface N8nNodeType {
  id: string;
  name: string;
  type: string;
  typeVersion: number;
  position: [number, number];
  parameters: Record<string, any>;
  credentials?: Record<string, any>;
  notes?: string;
  disabled?: boolean;
}

// N8N Connection Target
export interface N8nConnectionTarget {
  node: string;
  input: string;
}

// N8N Connection Entry
export interface N8nConnectionEntry {
  [outputPortName: string]: N8nConnectionTarget[];
}

// N8N Connections Type
export interface N8nConnectionsType {
  [sourceNodeId: string]: N8nConnectionEntry;
}

// N8N Workflow JSON Type
export interface N8nWorkflowJsonType {
  name: string;
  nodes: N8nNodeType[];
  connections: N8nConnectionsType;
  active: boolean;
  settings?: {
    executionOrder?: string[];
  };
  id?: string;
  tags?: string[];
}
