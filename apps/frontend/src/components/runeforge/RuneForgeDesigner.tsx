import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Textarea } from '@/components/ui/textarea';
import { Play, Plus, Save, Trash2 } from 'lucide-react';
import React, { useCallback, useRef, useState } from 'react';
import ReactFlow, {
    Background,
    Connection,
    Controls,
    Edge,
    Node,
    NodeTypes,
    ReactFlowProvider,
    addEdge,
    useEdgesState,
    useNodesState,
} from 'reactflow';
import 'reactflow/dist/style.css';

// Import custom nodes
import ApiCallNode from './nodes/ApiCallNode';
import ConditionNode from './nodes/ConditionNode';
import EndNode from './nodes/EndNode';
import ManualTaskNode from './nodes/ManualTaskNode';
import StartNode from './nodes/StartNode';

// Define node types
const nodeTypes: NodeTypes = {
  startNode: StartNode,
  endNode: EndNode,
  manualTaskNode: ManualTaskNode,
  conditionNode: ConditionNode,
  apiCallNode: ApiCallNode,
};

// Initial nodes for a new workflow
const initialNodes: Node[] = [
  {
    id: 'start',
    type: 'startNode',
    position: { x: 250, y: 50 },
    data: { label: 'Start' },
  },
];

const RuneForgeDesigner: React.FC = () => {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [workflowName, setWorkflowName] = useState('New Workflow');
  const [workflowDescription, setWorkflowDescription] = useState('');
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);

  // Handle connections between nodes
  const onConnect = useCallback(
    (params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // Handle node selection
  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      setSelectedNode(node);
    },
    []
  );

  // Add a new node to the canvas
  const addNode = (type: string) => {
    const newNode: Node = {
      id: `node_${Date.now()}`,
      type: `${type}Node`,
      position: {
        x: Math.random() * 300 + 50,
        y: Math.random() * 300 + 50,
      },
      data: {
        label: type.charAt(0).toUpperCase() + type.slice(1),
        // Add default data based on node type
        ...(type === 'manualTask' && { assignee: '', instructions: '' }),
        ...(type === 'condition' && { condition: '', trueLabel: 'Yes', falseLabel: 'No' }),
        ...(type === 'apiCall' && { url: '', method: 'GET', headers: {}, body: '' }),
      },
    };

    setNodes((nds) => nds.concat(newNode));
  };

  // Save the workflow
  const saveWorkflow = async () => {
    const workflow = {
      name: workflowName,
      description: workflowDescription,
      definition: {
        nodes,
        edges,
      },
    };

    console.log('Saving workflow:', workflow);
    // In a real implementation, this would call an API to save the workflow
    alert('Workflow saved (mock)');
  };

  // Execute the workflow
  const executeWorkflow = async () => {
    console.log('Executing workflow');
    // In a real implementation, this would call an API to execute the workflow
    alert('Workflow execution started (mock)');
  };

  // Update node data when edited in the properties panel
  const updateNodeData = (id: string, newData: any) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              ...newData,
            },
          };
        }
        return node;
      })
    );
  };

  // Delete the selected node
  const deleteSelectedNode = () => {
    if (selectedNode && selectedNode.id !== 'start') {
      setNodes((nds) => nds.filter((node) => node.id !== selectedNode.id));
      setEdges((eds) =>
        eds.filter(
          (edge) => edge.source !== selectedNode.id && edge.target !== selectedNode.id
        )
      );
      setSelectedNode(null);
    }
  };

  // Render properties panel based on selected node type
  const renderPropertiesPanel = () => {
    if (!selectedNode) return <div className="p-4">Select a node to edit its properties</div>;

    const { id, type, data } = selectedNode;

    switch (type) {
      case 'startNode':
        return (
          <div className="p-4">
            <h3 className="text-lg font-medium">Start Node</h3>
            <p className="text-sm text-gray-500">This is the starting point of your workflow.</p>
          </div>
        );
      case 'endNode':
        return (
          <div className="p-4">
            <h3 className="text-lg font-medium">End Node</h3>
            <p className="text-sm text-gray-500">This is the ending point of your workflow.</p>
          </div>
        );
      case 'manualTaskNode':
        return (
          <div className="p-4 space-y-4">
            <h3 className="text-lg font-medium">Manual Task</h3>
            
            <div>
              <Label htmlFor="taskName">Task Name</Label>
              <Input
                id="taskName"
                value={data.label}
                onChange={(e) => updateNodeData(id, { label: e.target.value })}
              />
            </div>
            
            <div>
              <Label htmlFor="assignee">Assignee</Label>
              <Input
                id="assignee"
                value={data.assignee || ''}
                onChange={(e) => updateNodeData(id, { assignee: e.target.value })}
                placeholder="User or role name"
              />
            </div>
            
            <div>
              <Label htmlFor="instructions">Instructions</Label>
              <Textarea
                id="instructions"
                value={data.instructions || ''}
                onChange={(e) => updateNodeData(id, { instructions: e.target.value })}
                placeholder="Task instructions"
                rows={4}
              />
            </div>
          </div>
        );
      case 'conditionNode':
        return (
          <div className="p-4 space-y-4">
            <h3 className="text-lg font-medium">Condition</h3>
            
            <div>
              <Label htmlFor="conditionName">Condition Name</Label>
              <Input
                id="conditionName"
                value={data.label}
                onChange={(e) => updateNodeData(id, { label: e.target.value })}
              />
            </div>
            
            <div>
              <Label htmlFor="condition">Condition Expression</Label>
              <Textarea
                id="condition"
                value={data.condition || ''}
                onChange={(e) => updateNodeData(id, { condition: e.target.value })}
                placeholder="e.g., value > 100"
                rows={2}
              />
            </div>
            
            <div className="grid grid-cols-2 gap-2">
              <div>
                <Label htmlFor="trueLabel">True Label</Label>
                <Input
                  id="trueLabel"
                  value={data.trueLabel || 'Yes'}
                  onChange={(e) => updateNodeData(id, { trueLabel: e.target.value })}
                />
              </div>
              <div>
                <Label htmlFor="falseLabel">False Label</Label>
                <Input
                  id="falseLabel"
                  value={data.falseLabel || 'No'}
                  onChange={(e) => updateNodeData(id, { falseLabel: e.target.value })}
                />
              </div>
            </div>
          </div>
        );
      case 'apiCallNode':
        return (
          <div className="p-4 space-y-4">
            <h3 className="text-lg font-medium">API Call</h3>
            
            <div>
              <Label htmlFor="apiName">API Name</Label>
              <Input
                id="apiName"
                value={data.label}
                onChange={(e) => updateNodeData(id, { label: e.target.value })}
              />
            </div>
            
            <div className="grid grid-cols-2 gap-2">
              <div>
                <Label htmlFor="method">Method</Label>
                <select
                  id="method"
                  className="w-full p-2 border rounded"
                  value={data.method || 'GET'}
                  onChange={(e) => updateNodeData(id, { method: e.target.value })}
                >
                  <option value="GET">GET</option>
                  <option value="POST">POST</option>
                  <option value="PUT">PUT</option>
                  <option value="DELETE">DELETE</option>
                </select>
              </div>
              <div>
                <Label htmlFor="url">URL</Label>
                <Input
                  id="url"
                  value={data.url || ''}
                  onChange={(e) => updateNodeData(id, { url: e.target.value })}
                  placeholder="https://api.example.com"
                />
              </div>
            </div>
            
            <div>
              <Label htmlFor="headers">Headers (JSON)</Label>
              <Textarea
                id="headers"
                value={data.headers ? JSON.stringify(data.headers, null, 2) : '{}'}
                onChange={(e) => {
                  try {
                    const headers = JSON.parse(e.target.value);
                    updateNodeData(id, { headers });
                  } catch (error) {
                    // Handle invalid JSON
                  }
                }}
                placeholder='{"Content-Type": "application/json"}'
                rows={3}
              />
            </div>
            
            <div>
              <Label htmlFor="body">Body (JSON)</Label>
              <Textarea
                id="body"
                value={data.body || ''}
                onChange={(e) => updateNodeData(id, { body: e.target.value })}
                placeholder='{"key": "value"}'
                rows={4}
              />
            </div>
          </div>
        );
      default:
        return <div className="p-4">Unknown node type</div>;
    }
  };

  return (
    <div className="h-screen flex flex-col">
      <div className="border-b p-4 flex justify-between items-center">
        <div className="flex-1">
          <Input
            value={workflowName}
            onChange={(e) => setWorkflowName(e.target.value)}
            className="text-xl font-bold w-full max-w-md"
          />
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={saveWorkflow} className="flex items-center">
            <Save className="mr-2 h-4 w-4" />
            Save
          </Button>
          <Button onClick={executeWorkflow} className="flex items-center">
            <Play className="mr-2 h-4 w-4" />
            Execute
          </Button>
        </div>
      </div>

      <div className="flex-1 flex">
        <div className="w-64 border-r p-4 flex flex-col">
          <h2 className="text-lg font-medium mb-4">Runes</h2>
          <div className="space-y-2">
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => addNode('end')}
            >
              <Plus className="mr-2 h-4 w-4" /> End
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => addNode('manualTask')}
            >
              <Plus className="mr-2 h-4 w-4" /> Manual Task
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => addNode('condition')}
            >
              <Plus className="mr-2 h-4 w-4" /> Condition
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={() => addNode('apiCall')}
            >
              <Plus className="mr-2 h-4 w-4" /> API Call
            </Button>
          </div>
          
          <div className="mt-auto">
            {selectedNode && selectedNode.id !== 'start' && (
              <Button
                variant="destructive"
                className="w-full justify-start"
                onClick={deleteSelectedNode}
              >
                <Trash2 className="mr-2 h-4 w-4" /> Delete Node
              </Button>
            )}
          </div>
        </div>

        <div className="flex-1 flex flex-col">
          <div className="flex-1" ref={reactFlowWrapper}>
            <ReactFlowProvider>
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onNodeClick={onNodeClick}
                nodeTypes={nodeTypes}
                onInit={setReactFlowInstance}
                fitView
              >
                <Controls />
                <Background />
              </ReactFlow>
            </ReactFlowProvider>
          </div>
        </div>

        <div className="w-80 border-l">
          <Tabs defaultValue="properties">
            <TabsList className="w-full">
              <TabsTrigger value="properties" className="flex-1">Properties</TabsTrigger>
              <TabsTrigger value="workflow" className="flex-1">Workflow</TabsTrigger>
            </TabsList>
            <TabsContent value="properties">
              {renderPropertiesPanel()}
            </TabsContent>
            <TabsContent value="workflow" className="p-4 space-y-4">
              <div>
                <Label htmlFor="workflowDescription">Description</Label>
                <Textarea
                  id="workflowDescription"
                  value={workflowDescription}
                  onChange={(e) => setWorkflowDescription(e.target.value)}
                  placeholder="Describe the purpose of this workflow"
                  rows={4}
                />
              </div>
              
              <div>
                <Label>Statistics</Label>
                <div className="text-sm text-gray-500">
                  <p>Nodes: {nodes.length}</p>
                  <p>Connections: {edges.length}</p>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default RuneForgeDesigner;