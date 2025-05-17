import React from 'react';
import { addEdge, Background, Controls, ReactFlow, ReactFlowProvider } from 'reactflow';

import 'reactflow/dist/style.css'; // Import default react-flow styles (can be overridden by Tailwind)
import GrimOSRuneNodeComponent from './components/GrimOSRuneNodeComponent';

const initialNodes = [
  {
    id: '1',
    type: 'default',
    position: { x: 250, y: 5 },
    data: { label: 'Start Node' },
  },
  {
    id: '2',
    type: 'custom',
    position: { x: 100, y: 100 },
    data: { label: 'Custom Rune', icon: <span>⚙️</span> },
  },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', type: 'smoothstep' },
];

const nodeTypes = {
  custom: GrimOSRuneNodeComponent,
};

const RuneForgeCanvasApp: React.FC = () => {
  const [nodes, setNodes] = React.useState(initialNodes);
  const [edges, setEdges] = React.useState(initialEdges);

  const onConnect = React.useCallback((params) => setEdges((eds) => addEdge(params, eds)), []);

  return (
    <ReactFlowProvider>
      <div className="flex h-screen w-screen bg-gray-900 text-gray-100">
        {/* Rune Palette Panel Area */}
        <div className="w-64 bg-gray-800 p-4">
          {/* Placeholder for Rune Palette Panel */}
          <h3 className="text-lg font-bold mb-4">Rune Palette</h3>
          {/* Draggable Rune elements will go here */}
        </div>

        {/* Main Canvas Area */}
        <div className="flex-1 relative">
          {/* Placeholder for Canvas Toolbar */}
          <div className="absolute top-2 left-1/2 transform -translate-x-1/2 z-10">
             {/* Placeholder for Canvas Toolbar */}
          </div>
          {/* React Flow Canvas will be rendered here */}
          <div className="h-full w-full">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onConnect={onConnect}
              nodeTypes={nodeTypes}
              fitView
            >
              <Background />
              <Controls />
            </ReactFlow>
          </div>
        </div>

        {/* Rune Properties Panel Area */}
        <div className="w-80 bg-gray-800 p-4">
          {/* Placeholder for Rune Properties Panel */}
          <h3 className="text-lg font-bold mb-4">Rune Properties</h3>
          {/* Properties form for selected Rune will go here */}
        </div>
      </div>
    </ReactFlowProvider>
  );
};

export default RuneForgeCanvasApp;