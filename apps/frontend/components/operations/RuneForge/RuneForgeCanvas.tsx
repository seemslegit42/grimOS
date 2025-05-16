import { FC, useCallback } from 'react';
import ReactFlow, {
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  Node,
  Edge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  MiniMap,
  Controls,
  Background,
  useReactFlow,
} from 'reactflow';

import 'reactflow/dist/style.css'; // Import default styles (will be overridden)

import { useRuneForgeStore } from '@/lib/store/RuneForgeStore';
import { shallow } from 'zustand/shallow';

interface RuneForgeCanvasProps {
  // Props related to the spell being edited, if any
  spellId?: string;
}

const selector = (state: any) => ({
  nodes: state.nodes,
  edges: state.edges,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
  onConnect: state.onConnect,
  // Add other state/actions you need here, e.g., setSelectedNode
});

export const RuneForgeCanvas: FC<RuneForgeCanvasProps> = ({ spellId }) => {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect } = useRuneForgeStore(selector, shallow);
  
  return (
    <div 
      className="relative w-full h-full bg-[#121212] border border-white/20 rounded-md"
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        // Add other react-flow props as needed
        // nodeTypes={{ grimOS: GrimOSRuneNode }} // Define custom node types later
        // edgeTypes={{ grimOS: GrimOSConnectionLine }} // Define custom edge types later
        fitView
      >
        <MiniMap nodeStrokeWidth={3} nodeColor="#7ED321" zoomable pannable />
        <Controls />
        <Background color="#7ED321" gap={16} /> {/* Apply grimOS background */}
      </ReactFlow>
    </div>
  );
};
