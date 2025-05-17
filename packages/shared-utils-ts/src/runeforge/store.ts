import { AvailableRuneType, RuneForgeNodeData, SpellMetadata } from '@grimos/shared-types';
import { applyEdgeChanges, applyNodeChanges, Connection, Edge, EdgeChange, Node, NodeChange, OnConnect, OnEdgesChange, OnNodesChange } from 'reactflow';
import { create } from 'zustand';
import { transformFromN8nJson, transformToN8nJson } from '../n8n/N8NJsonTransformerUtil';

/**
 * RuneForge State Interface
 * Defines the store state and actions for the RuneForge canvas
 */
export interface RuneForgeState {
  available_runes: AvailableRuneType[]; 
  spellMetadata: SpellMetadata;
  
  current_spell_id: string | null;
  current_spell_name: string;
  flow_nodes: Node<RuneForgeNodeData>[]; 
  flow_edges: Edge[]; 
  selected_node_id: string | null;
  is_loading_spell: boolean;
  is_saving_spell: boolean;
  canvas_error: string | null;

  // Actions
  setSpellMetadata: (metadata: SpellMetadata) => void;
  setSpellData: (data: { id: string; name: string; nodes: Node<RuneForgeNodeData>[]; edges: Edge[] }) => void;
  addFlowNode: (node: Node<RuneForgeNodeData>) => void;
  deleteFlowNode: (nodeId: string) => void;
  updateFlowNodePosition: (nodeId: string, position: { x: number; y: number }) => void;
  updateRuneParameters: (nodeId: string, parameters: Record<string, any>) => void;
  addFlowEdge: (edge: Edge | Connection) => void;
  deleteFlowEdge: (edgeId: string) => void;
  setSelectedNodeId: (nodeId: string | null) => void;
  setAvailableRunesList: (runes: AvailableRuneType[]) => void; 
  
  // Async actions
  initiateLoadSpell: (spellId: string) => Promise<void>; 
  initiateSaveCurrentSpell: () => Promise<void>; 

  // React Flow handlers
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
}

/**
 * Create a RuneForge store
 * @param config Optional configuration for customizing the store behavior
 * @returns A Zustand store with RuneForge state and actions
 */
export const createRuneForgeStore = ({ 
  // Optional API client for backend communication
  apiClient = null,
  // Debug mode for logging store actions
  debug = false 
} = {}) => {
  return create<RuneForgeState>((set, get) => ({
    // Initial state
    available_runes: [],
    spellMetadata: {
      id: null,
      name: 'New Spell',
      description: '',
      isPublic: false,
      isTemplate: false,
    },

    current_spell_id: null,
    current_spell_name: 'New Spell',
    flow_nodes: [],
    flow_edges: [],
    selected_node_id: null,
    is_loading_spell: false,
    is_saving_spell: false,
    canvas_error: null,

    // Actions
    setSpellMetadata: (metadata: SpellMetadata) => {
      if (debug) console.log('[RuneForgeStore] setSpellMetadata', metadata);
      set({ spellMetadata: metadata });
    },

    setSpellData: (data: { id: string; name: string; nodes: Node<RuneForgeNodeData>[]; edges: Edge[] }) => {
      if (debug) console.log('[RuneForgeStore] setSpellData', data);
      set({
        current_spell_id: data.id,
        current_spell_name: data.name,
        flow_nodes: data.nodes,
        flow_edges: data.edges,
        selected_node_id: null, 
        canvas_error: null,
      });
    },

    addFlowNode: (node: Node<RuneForgeNodeData>) => {
      if (debug) console.log('[RuneForgeStore] addFlowNode', node);
      set((state: RuneForgeState) => ({
        flow_nodes: [...state.flow_nodes, node],
      }));
    },

    deleteFlowNode: (nodeId: string) => {
      if (debug) console.log('[RuneForgeStore] deleteFlowNode', nodeId);
      set((state: RuneForgeState) => ({
        flow_nodes: state.flow_nodes.filter(node => node.id !== nodeId),
        selected_node_id: state.selected_node_id === nodeId ? null : state.selected_node_id, 
      }));
    },

    updateFlowNodePosition: (nodeId: string, position: { x: number; y: number }) => {
      if (debug) console.log('[RuneForgeStore] updateFlowNodePosition', nodeId, position);
      set((state: RuneForgeState) => ({
        flow_nodes: state.flow_nodes.map(node =>
          node.id === nodeId ? { ...node, position } : node
        ),
      }));
    },

    updateRuneParameters: (nodeId: string, parameters: Record<string, any>) => {
      if (debug) console.log('[RuneForgeStore] updateRuneParameters', nodeId, parameters);
      set((state: RuneForgeState) => ({
        flow_nodes: state.flow_nodes.map(node =>
          node.id === nodeId ? { ...node, data: { ...node.data, parameters } } : node
        ),
      }));
    },

    addFlowEdge: (edgeParams: Edge | Connection) => {
      if (debug) console.log('[RuneForgeStore] addFlowEdge', edgeParams);
      set((state: RuneForgeState) => ({
        flow_edges: [...state.flow_edges, edgeParams as Edge], 
      }));
    },

    deleteFlowEdge: (edgeId: string) => {
      if (debug) console.log('[RuneForgeStore] deleteFlowEdge', edgeId);
      set((state: RuneForgeState) => ({
        flow_edges: state.flow_edges.filter(edge => edge.id !== edgeId),
      }));
    },

    setSelectedNodeId: (nodeId: string | null) => {
      if (debug) console.log('[RuneForgeStore] setSelectedNodeId', nodeId);
      set({ selected_node_id: nodeId });
    },

    setAvailableRunesList: (runes: AvailableRuneType[]) => {
      if (debug) console.log('[RuneForgeStore] setAvailableRunesList', runes);
      set({ available_runes: runes });
    },

    // Async actions that use apiClient if provided
    initiateLoadSpell: async (spellId: string) => {
      if (debug) console.log('[RuneForgeStore] initiateLoadSpell', spellId);
      set({ is_loading_spell: true, canvas_error: null });

      try {
        if (apiClient && apiClient.fetchSpellFromBackend) {
          const spellData = await apiClient.fetchSpellFromBackend(spellId);
          
          if (spellData && spellData.workflow_json) {
            const { flowNodes, flowEdges } = transformFromN8nJson(spellData.workflow_json);
            
            get().setSpellData({ 
              id: spellData.id || null, 
              name: spellData.name || 'Untitled Spell', 
              nodes: flowNodes, 
              edges: flowEdges 
            });
            
            get().setSpellMetadata({
              id: spellData.id,
              name: spellData.name,
              description: spellData.description,
              isPublic: spellData.isPublic,
              isTemplate: spellData.isTemplate
            });
          } else {
            throw new Error('Invalid spell data received');
          }
        } else {
          console.warn('No API client provided for loading spells');
          // Simulate API delay for testing
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error loading spell';
        console.error('[RuneForgeStore] Error loading spell:', errorMessage);
        set({ canvas_error: errorMessage });
      } finally {
        set({ is_loading_spell: false });
      }
    },

    initiateSaveCurrentSpell: async () => {
      if (debug) console.log('[RuneForgeStore] initiateSaveCurrentSpell');
      set({ is_saving_spell: true, canvas_error: null });
      
      try {
        const { current_spell_id, current_spell_name, flow_nodes, flow_edges, spellMetadata } = get();
        
        const workflowJson = transformToN8nJson(
          flow_nodes,
          flow_edges,
          current_spell_name,
          true // isActive
        );
        
        if (apiClient && apiClient.saveSpellToBackend) {
          const spellData = {
            ...spellMetadata,
            id: current_spell_id,
            name: current_spell_name,
            workflow_json: workflowJson
          };
          
          const savedSpell = await apiClient.saveSpellToBackend(spellData);
          
          if (savedSpell && savedSpell.id) {
            // Update with the returned ID if it's a new spell
            if (!current_spell_id) {
              set({ current_spell_id: savedSpell.id });
            }
            
            get().setSpellMetadata({
              id: savedSpell.id,
              name: savedSpell.name,
              description: savedSpell.description,
              isPublic: savedSpell.isPublic,
              isTemplate: savedSpell.isTemplate
            });
          }
        } else {
          console.warn('No API client provided for saving spells');
          // Simulate API delay for testing
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error saving spell';
        console.error('[RuneForgeStore] Error saving spell:', errorMessage);
        set({ canvas_error: errorMessage });
      } finally {
        set({ is_saving_spell: false });
      }
    },

    // React Flow handlers
    onNodesChange: (changes: NodeChange[]) => {
      set((state: RuneForgeState) => ({
        flow_nodes: applyNodeChanges(changes, state.flow_nodes),
      }));
    },
    
    onEdgesChange: (changes: EdgeChange[]) => {
      set((state: RuneForgeState) => ({
        flow_edges: applyEdgeChanges(changes, state.flow_edges),
      }));
    },
    
    onConnect: (connection: Edge | Connection) => { 
      set((state: RuneForgeState) => ({
        flow_edges: [...state.flow_edges, connection as Edge],
      }));
    },
  }));
};

// Export an initial spell metadata object for convenience
export const initialSpellMetadata: SpellMetadata = {
  id: null,
  name: 'New Spell',
  description: '',
  isPublic: false,
  isTemplate: false,
};
