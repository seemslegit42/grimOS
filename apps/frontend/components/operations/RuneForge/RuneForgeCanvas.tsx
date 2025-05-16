import { Rune, WorkflowDefinition } from '@/types/workflow';
import { FC, useCallback, useEffect, useRef, useState } from 'react';

interface RuneForgeCanvasProps {
  workflow: WorkflowDefinition;
  selectedRune: Rune | null;
  onSelectRune: (rune: Rune | null) => void;
  onUpdateRune: (rune: Rune) => void;
  onRemoveRune: (runeId: string) => void;
}

export const RuneForgeCanvas: FC<RuneForgeCanvasProps> = ({
  workflow,
  selectedRune,
  onSelectRune,
  onUpdateRune,
  onRemoveRune
}) => {
  const canvasRef = useRef<HTMLDivElement>(null);
  const [draggingRune, setDraggingRune] = useState<Rune | null>(null);
  const [connections, setConnections] = useState<{ from: string, to: string, type?: string }[]>([]);
  const [connecting, setConnecting] = useState<{ fromRune: Rune, port: string } | null>(null);
  const [highlightTarget, setHighlightTarget] = useState<string | null>(null);
  
  // Calculate connections based on rune relationships
  useEffect(() => {
    const newConnections: { from: string, to: string, type?: string }[] = [];
    
    workflow.runes.forEach(rune => {
      if (rune.next_step_id) {
        newConnections.push({
          from: rune.id,
          to: rune.next_step_id
        });
      }
      
      if (rune.type === 'SIMPLE_CONDITION') {
        if (rune.condition_true_next_step_id) {
          newConnections.push({
            from: rune.id,
            to: rune.condition_true_next_step_id,
            type: 'true'
          });
        }
        
        if (rune.condition_false_next_step_id) {
          newConnections.push({
            from: rune.id,
            to: rune.condition_false_next_step_id,
            type: 'false'
          });
        }
      }
    });
    
    setConnections(newConnections);
  }, [workflow.runes]);
  
  // Handle drag over for dropping runes onto the canvas
  const handleDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);
  
  // Handle drop for adding runes to the canvas
  const handleDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    
    // Get the canvas bounds
    const canvasRect = canvasRef.current?.getBoundingClientRect();
    if (!canvasRect) return;
    
    // Calculate the drop position relative to the canvas
    const x = event.clientX - canvasRect.left;
    const y = event.clientY - canvasRect.top;
    
    try {
      const jsonData = event.dataTransfer.getData('application/reactflow');
      if (jsonData) {
        const runeType = JSON.parse(jsonData);
        
        // Create a new rune at the drop position
        const newRune: Rune = {
          id: `rune-${Date.now()}`,
          type: runeType.type,
          name: runeType.name,
          config: runeType.defaultConfig || {},
          position: { x, y }
        };
        
        // Add the rune to the workflow
        onUpdateRune(newRune);
      }
    } catch (err) {
      console.error('Error parsing drag data:', err);
    }
  }, [onUpdateRune]);
  
  // Handle starting to drag a rune within the canvas
  const handleRuneDragStart = (event: React.MouseEvent, rune: Rune) => {
    setDraggingRune(rune);
    event.stopPropagation();
  };
  
  // Handle dragging a rune within the canvas
  const handleMouseMove = (event: React.MouseEvent) => {
    if (!draggingRune || !canvasRef.current) return;
    
    const canvasRect = canvasRef.current.getBoundingClientRect();
    const x = event.clientX - canvasRect.left;
    const y = event.clientY - canvasRect.top;
    
    // Update the rune position
    const updatedRune = {
      ...draggingRune,
      position: { x, y }
    };
    
    onUpdateRune(updatedRune);
  };
  
  // Handle mouse up to end dragging
  const handleMouseUp = () => {
    setDraggingRune(null);
  };
  
  // Get position for a rune
  const getRunePosition = (rune: Rune) => {
    return {
      left: `${rune.position?.x || 100}px`,
      top: `${rune.position?.y || 100}px`
    };
  };
  
  // Handle selecting a rune
  const handleSelectRune = (event: React.MouseEvent, rune: Rune) => {
    event.stopPropagation();
    onSelectRune(rune);
  };
  
  // Handle deselecting all runes (clicking empty canvas)
  const handleCanvasClick = () => {
    onSelectRune(null);
  };
  
  // Handle deleting a rune
  const handleDeleteRune = (event: React.MouseEvent, runeId: string) => {
    event.stopPropagation();
    onRemoveRune(runeId);
  };
  
  // Draw the connecting lines between runes
  const drawConnections = () => {
    return connections.map((connection, index) => {
      const fromRune = workflow.runes.find(r => r.id === connection.from);
      const toRune = workflow.runes.find(r => r.id === connection.to);
      
      if (!fromRune || !toRune || !fromRune.position || !toRune.position) {
        return null;
      }
      
      // Calculate center points of the runes
      const fromX = fromRune.position.x + 75; // Half of rune width
      const fromY = fromRune.position.y + 40; // Half of rune height
      const toX = toRune.position.x + 75;
      const toY = toRune.position.y + 40;
      
      // Draw a simple straight line
      return (
        <svg
          key={`connection-${index}`}
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
            zIndex: 1
          }}
        >
          <line
            x1={fromX}
            y1={fromY}
            x2={toX}
            y2={toY}
            stroke={connection.type === 'true' ? '#34A853' : connection.type === 'false' ? '#EA4335' : '#00BFFF'}
            strokeWidth={2}
          />
          {/* Arrow head */}
          <polygon
            points={`${toX},${toY} ${toX-10},${toY-5} ${toX-10},${toY+5}`}
            fill={connection.type === 'true' ? '#34A853' : connection.type === 'false' ? '#EA4335' : '#00BFFF'}
            transform={`rotate(${Math.atan2(toY - fromY, toX - fromX) * (180 / Math.PI)}, ${toX}, ${toY})`}
          />
          
          {/* Connection label for condition branches */}
          {connection.type && (
            <text
              x={(fromX + toX) / 2}
              y={(fromY + toY) / 2 - 10}
              fill={connection.type === 'true' ? '#34A853' : '#EA4335'}
              fontSize="12"
              fontWeight="bold"
              textAnchor="middle"
              pointerEvents="none"
            >
              {connection.type.toUpperCase()}
            </text>
          )}
        </svg>
      );
    });
  };
  
  // Get the appropriate icon for each rune type
  const getRuneIcon = (type: string) => {
    switch (type) {
      case 'START':
        return '▶️';
      case 'END':
        return '⏹️';
      case 'MANUAL_TASK':
        return '👤';
      case 'SIMPLE_CONDITION':
        return '🔀';
      case 'BASIC_API_CALL':
        return '🌐';
      case 'AGENT_TASK_STUB':
        return '🤖';
      default:
        return '📦';
    }
  };
  
  return (
    <div 
      ref={canvasRef}
      className="relative w-full h-full overflow-auto bg-[#121212]"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onClick={handleCanvasClick}
    >
      {/* Grid background */}
      <div className="absolute inset-0" style={{
        backgroundImage: 'linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px)',
        backgroundSize: '20px 20px',
        width: '2000px',
        height: '2000px'
      }}></div>
      
      {/* Connection lines */}
      {drawConnections()}
      
      {/* Runes */}
      {workflow.runes.map(rune => (
        <div
          key={rune.id}
          className={`absolute w-[150px] p-3 rounded-md cursor-move select-none flex flex-col items-center
                     ${selectedRune?.id === rune.id ? 'border-2 border-primary-accent bg-white/10' : 'border border-white/20 bg-white/5'}
                     ${highlightTarget === rune.id ? 'border-secondary-accent border-2' : ''}`}
          style={getRunePosition(rune)}
          onMouseDown={(e) => handleRuneDragStart(e, rune)}
          onClick={(e) => handleSelectRune(e, rune)}
        >
          <div className="flex items-center mb-2 w-full">
            <div className="text-xl mr-2">{getRuneIcon(rune.type)}</div>
            <div className="flex-1 truncate text-white font-medium">{rune.name}</div>
            <button
              className="ml-1 text-white/60 hover:text-white/90 text-sm"
              onClick={(e) => handleDeleteRune(e, rune.id)}
            >
              ✕
            </button>
          </div>
          <div className="text-xs text-white/60 mb-1 w-full truncate">
            {rune.type}
          </div>
        </div>
      ))}
    </div>
  );
};
