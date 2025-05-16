// Types for Workflow and Rune components

export type RuneType = 'START' | 'END' | 'MANUAL_TASK' | 'SIMPLE_CONDITION' | 'BASIC_API_CALL' | 'AGENT_TASK_STUB';

export interface RuneConfig {
  [key: string]: any;
}

export interface Rune {
  id: string;
  type: RuneType;
  name: string;
  config?: RuneConfig;
  next_step_id?: string;
  condition_true_next_step_id?: string;
  condition_false_next_step_id?: string;
  position?: {
    x: number;
    y: number;
  };
}

export interface WorkflowDefinition {
  id: string;
  name: string;
  description?: string;
  runes: Rune[];
  version: number;
  created_at: string;
  updated_at: string;
  created_by: string;
}

export interface WorkflowInstance {
  id: string;
  definition_id: string;
  definition_name: string;
  name?: string;
  status: string;
  current_step_id?: string;
  payload?: any;
  result?: any;
  error?: string;
  start_time?: string;
  end_time?: string;
  created_at: string;
  execution_log: ExecutionLogEntry[];
}

export interface ExecutionLogEntry {
  step_id: string;
  status: string;
  message: string;
  timestamp: string;
}

export interface RuneLibraryItem {
  type: RuneType;
  name: string;
  description: string;
  icon: string;
  defaultConfig?: RuneConfig;
}

export interface Connection {
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
}
