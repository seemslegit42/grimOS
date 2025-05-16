import { create } from 'zustand';
import { Edge, Node } from 'react-flow-renderer';

export interface RuneDefinition {
  id: string;
  name: string;
  description?: string;
  category: string;
  // Add other properties relevant to an n8n node type
  // e.g., parameters, input/output types, icon
  parameters: any[]; // Placeholder for node parameters
}

export interface SpellMetadata {
  id: string | null;
  name: string;
  description: string;
  isPublic: boolean;
  isTemplate: boolean;
  // Add other spell-level metadata
}

export interface RuneForgeState {
  nodes: Node[];
  edges: Edge[];
  selectedElements: (Node | Edge)[];
  availableRunes: RuneDefinition[];
  spellMetadata: SpellMetadata;
  isLoading: boolean;
  isSaving: boolean;
  error: string | null;

  // Placeholder actions
  setNodes: (nodes: Node[]) => void;
  setEdges: (edges: Edge[]) => void;
  setSelectedElements: (elements: (Node | Edge)[]) => void;
  setAvailableRunes: (runes: RuneDefinition[]) => void;
  setSpellMetadata: (metadata: SpellMetadata) => void;
  setIsLoading: (isLoading: boolean) => void;
  setIsSaving: (isSaving: boolean) => void;
  setError: (error: string | null) => void;

  // Actions for canvas interactions (placeholders)
  addNode: (node: Node) => void;
  removeNode: (nodeId: string) => void;
  addEdge: (edge: Edge) => void;
  removeEdge: (edgeId: string) => void;
  updateNodeData: (nodeId: string, data: any) => void;
}

export const useRuneForgeStore = create<RuneForgeState>((set) => ({
  // Initial state
  nodes: [],
  edges: [],
  selectedElements: [],
  availableRunes: [],
  spellMetadata: {
    id: null,
    name: 'New Spell',
    description: '',
    isPublic: false,
    isTemplate: false,
  },
  isLoading: false,
  isSaving: false,
  error: null,

  // Placeholder actions implementation
  setNodes: (nodes) => set({ nodes }),
  setEdges: (edges) => set({ edges }),
  setSelectedElements: (selectedElements) => set({ selectedElements }),
  setAvailableRunes: (availableRunes) => set({ availableRunes }),
  setSpellMetadata: (spellMetadata) => set({ spellMetadata }),
  setIsLoading: (isLoading) => set({ isLoading }),
  setIsSaving: (isSaving) => set({ isSaving }),
  setError: (error) => set({ error }),

  addNode: (node) => set((state) => ({ nodes: [...state.nodes, node] })),
  removeNode: (nodeId) => set((state) => ({ nodes: state.nodes.filter(node => node.id !== nodeId) })),
  addEdge: (edge) => set((state) => ({ edges: [...state.edges, edge] })),
  removeEdge: (edgeId) => set((state) => ({ edges: state.edges.filter(edge => edge.id !== edgeId) })),
  updateNodeData: (nodeId, data) => set((state) => ({
    nodes: state.nodes.map(node => node.id === nodeId ? { ...node, data: { ...node.data, ...data } } : node)
  })),
}));