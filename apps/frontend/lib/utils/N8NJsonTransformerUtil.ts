import { RuneForgeNodeData } from '@grimos/shared-types/rune-forge';
import { Edge, Node } from 'reactflow';

// N8N type definitions based on common n8n workflow structure
// These types should be refined to match the exact n8n JSON schema used by the target n8n version.
export interface N8nNodeType {
  id: string;
  name: string; // User-defined name or label for the node instance
  type: string; // The actual n8n node type (e.g., 'n8n-nodes-base.httpRequest')
  typeVersion: number;
  position: [number, number]; // [x, y]
  parameters: Record<string, any>;
  credentials?: Record<string, any>;
  notes?: string;
  disabled?: boolean;
  // Potentially other n8n-specific fields like 'retryOnFail', 'continueOnFail'
}

export interface N8nConnectionTarget {
  node: string; // ID of the target node
  input: string; // Name of the input port (e.g., 'main', 'input_0')
}

export interface N8nConnectionEntry {
  [outputPortName: string]: N8nConnectionTarget[];
}

export interface N8nConnectionsType {
  [sourceNodeId: string]: N8nConnectionEntry;
}

export interface N8nWorkflowJsonType {
  name: string;
  nodes: N8nNodeType[];
  connections: N8nConnectionsType;
  active: boolean;
  settings?: {
    executionOrder?: string[]; // Example: if n8n uses this for ordering
    // Other workflow-level settings
  };
  id?: string; // Workflow ID, if applicable
  tags?: string[]; // Workflow tags
  // ... other workflow-level fields
}

/**
 * Transforms React Flow nodes and edges to n8n workflow JSON.
 */
export const transformToN8nJson = (
  flowNodes: Node<RuneForgeNodeData>[],
  flowEdges: Edge[],
  workflowName: string = 'My Spell',
  workflowIsActive: boolean = true,
): N8nWorkflowJsonType => {
  const n8nNodes: N8nNodeType[] = flowNodes.map((flowNode) => {
    const { data, position, id } = flowNode;
    return {
      id: id,
      name: data.label || data.n8nNodeType || 'Unnamed Rune',
      type: data.n8nNodeType || 'n8n-nodes-base.unknown',
      typeVersion: 1, // Default, might need to be dynamic based on actual node spec
      position: [position.x, position.y],
      parameters: data.parameters || {},
      // credentials, notes, disabled would come from flowNode.data if available and mapped
    };
  });

  const n8nConnections: N8nConnectionsType = {};
  flowEdges.forEach((edge) => {
    const sourceHandle = edge.sourceHandle || 'main'; // Default n8n output port
    const targetHandle = edge.targetHandle || 'main'; // Default n8n input port

    if (!n8nConnections[edge.source]) {
      n8nConnections[edge.source] = {};
    }
    if (!n8nConnections[edge.source][sourceHandle]) {
      n8nConnections[edge.source][sourceHandle] = [];
    }
    n8nConnections[edge.source][sourceHandle].push({
      node: edge.target,
      input: targetHandle,
    });
  });

  return {
    name: workflowName,
    nodes: n8nNodes,
    connections: n8nConnections,
    active: workflowIsActive,
    settings: {},
    // id and tags could be added if needed
  };
};

/**
 * Transforms n8n workflow JSON to React Flow nodes and edges.
 */
export const transformFromN8nJson = (
  n8nWorkflow: N8nWorkflowJsonType,
): { flowNodes: Node<RuneForgeNodeData>[]; flowEdges: Edge[] } => {
  const flowNodes: Node<RuneForgeNodeData>[] = n8nWorkflow.nodes.map((n8nNode) => {
    return {
      id: n8nNode.id,
      type: 'GrimOSRuneNode', // Custom node type for RuneForge canvas
      position: { x: n8nNode.position[0], y: n8nNode.position[1] },
      data: {
        label: n8nNode.name, 
        n8nNodeType: n8nNode.type,
        parameters: n8nNode.parameters,
        // iconName and status would need to be derived or defaulted if not in n8nNode
      },
    };
  });

  const flowEdges: Edge[] = [];
  Object.entries(n8nWorkflow.connections).forEach(([sourceNodeId, connectionEntry]) => {
    Object.entries(connectionEntry).forEach(([outputPortName, targets]) => {
      targets.forEach((target, index) => {
        const edgeId = `edge-${sourceNodeId}-${outputPortName}-${target.node}-${target.input}-${index}`;
        flowEdges.push({
          id: edgeId,
          source: sourceNodeId,
          target: target.node,
          sourceHandle: outputPortName,
          targetHandle: target.input,
          type: 'GrimOSConnectionLine', // Custom edge type for RuneForge canvas
        });
      });
    });
  });

  return {
    flowNodes,
    flowEdges,
  };
};

export const n8nJsonTransformer = {
  transformToN8nJson,
  transformFromN8nJson,
};
