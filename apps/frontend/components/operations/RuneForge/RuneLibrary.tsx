import { GlassmorphicPanel } from '@/components/ui/GlassmorphicPanel';
import { Rune, RuneLibraryItem } from '@/types/workflow';
import { FC } from 'react';

// Define the available rune types for the library
const availableRunes: RuneLibraryItem[] = [
  {
    type: 'START',
    name: 'Start',
    description: 'Beginning of the workflow',
    icon: '▶️',
    defaultConfig: {},
  },
  {
    type: 'END',
    name: 'End',
    description: 'End of the workflow',
    icon: '⏹️',
    defaultConfig: {},
  },
  {
    type: 'MANUAL_TASK',
    name: 'Manual Task',
    description: 'Task requiring human intervention',
    icon: '👤',
    defaultConfig: {
      assigneeRole: '',
      instructions: ''
    },
  },
  {
    type: 'SIMPLE_CONDITION',
    name: 'Simple Condition',
    description: 'Basic if/else logic',
    icon: '🔀',
    defaultConfig: {
      condition: ''
    },
  },
  {
    type: 'BASIC_API_CALL',
    name: 'Basic API Call',
    description: 'Make an API request',
    icon: '🌐',
    defaultConfig: {
      url: '',
      method: 'GET',
      headers: {},
      body: ''
    },
  },
  {
    type: 'AGENT_TASK_STUB',
    name: 'Agent Task',
    description: 'Assign task to an AI agent',
    icon: '🤖',
    defaultConfig: {
      agentId: '',
      task: ''
    },
  },
];

interface RuneLibraryProps {
  onAddRune: (rune: Rune) => void;
}

export const RuneLibrary: FC<RuneLibraryProps> = ({ onAddRune }) => {
  const handleDragStart = (event: React.DragEvent, runeType: RuneLibraryItem) => {
    // Set the data to be transferred during drag
    event.dataTransfer.setData('application/reactflow', JSON.stringify(runeType));
    event.dataTransfer.effectAllowed = 'move';
  };
  
  const handleAddRune = (runeItem: RuneLibraryItem) => {
    // Create a new rune from the library item
    const newRune: Rune = {
      id: `rune-${Date.now()}`,
      type: runeItem.type,
      name: runeItem.name,
      config: runeItem.defaultConfig,
      position: {
        x: 100,
        y: 100
      }
    };
    
    onAddRune(newRune);
  };
  
  return (
    <GlassmorphicPanel className="h-full overflow-y-auto p-0">
      <div className="p-4 border-b border-white/10 bg-white/5">
        <h2 className="text-lg font-semibold text-white">Rune Library</h2>
        <p className="text-sm text-white/70">Drag runes to the canvas</p>
      </div>
      
      <div className="p-4 space-y-4">
        {availableRunes.map((rune) => (
          <div
            key={rune.type}
            className="bg-white/5 border border-white/10 rounded-md p-3 cursor-move flex items-center gap-3 hover:bg-white/10 transition-colors"
            draggable
            onDragStart={(e) => handleDragStart(e, rune)}
            onClick={() => handleAddRune(rune)}
          >
            <div className="text-2xl">{rune.icon}</div>
            <div>
              <div className="text-white font-medium">{rune.name}</div>
              <div className="text-xs text-white/70">{rune.description}</div>
            </div>
          </div>
        ))}
      </div>
    </GlassmorphicPanel>
  );
};
