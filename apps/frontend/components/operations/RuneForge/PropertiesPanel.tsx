import { GlassmorphicPanel } from '@/components/ui/GlassmorphicPanel';
import { Rune } from '@/types/workflow';
import { FC, useEffect, useState } from 'react';

interface PropertiesPanelProps {
  selectedRune: Rune | null;
  onUpdateRune: (rune: Rune) => void;
}

export const PropertiesPanel: FC<PropertiesPanelProps> = ({ selectedRune, onUpdateRune }) => {
  const [localRune, setLocalRune] = useState<Rune | null>(selectedRune);
  
  // Update local state when selected rune changes
  useEffect(() => {
    setLocalRune(selectedRune);
  }, [selectedRune]);
  
  // Handle changes to the rune properties
  const handleChange = (field: string, value: any) => {
    if (!localRune) return;
    
    if (field.startsWith('config.')) {
      const configKey = field.replace('config.', '');
      const newConfig = { ...(localRune.config || {}), [configKey]: value };
      
      setLocalRune({
        ...localRune,
        config: newConfig
      });
    } else {
      setLocalRune({
        ...localRune,
        [field]: value
      });
    }
  };
  
  // Apply changes to the parent component
  const handleApplyChanges = () => {
    if (localRune) {
      onUpdateRune(localRune);
    }
  };
  
  // Render fields based on rune type
  const renderTypeSpecificFields = () => {
    if (!localRune) return null;
    
    switch (localRune.type) {
      case 'MANUAL_TASK':
        return (
          <>
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-1">Assignee Role</label>
              <input 
                type="text" 
                className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white"
                value={(localRune.config?.assigneeRole || '')}
                onChange={(e) => handleChange('config.assigneeRole', e.target.value)}
                placeholder="e.g., Manager, Reviewer"
              />
            </div>
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-1">Instructions</label>
              <textarea 
                className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white h-24 resize-none"
                value={(localRune.config?.instructions || '')}
                onChange={(e) => handleChange('config.instructions', e.target.value)}
                placeholder="Task instructions..."
              />
            </div>
          </>
        );
        
      case 'SIMPLE_CONDITION':
        return (
          <div className="mb-4">
            <label className="block text-white text-sm font-medium mb-1">Condition</label>
            <textarea 
              className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white h-24 resize-none"
              value={(localRune.config?.condition || '')}
              onChange={(e) => handleChange('config.condition', e.target.value)}
              placeholder="e.g., data.amount > 1000"
            />
          </div>
        );
        
      case 'BASIC_API_CALL':
        return (
          <>
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-1">URL</label>
              <input 
                type="text" 
                className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white"
                value={(localRune.config?.url || '')}
                onChange={(e) => handleChange('config.url', e.target.value)}
                placeholder="https://api.example.com/endpoint"
              />
            </div>
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-1">Method</label>
              <select 
                className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white"
                value={(localRune.config?.method || 'GET')}
                onChange={(e) => handleChange('config.method', e.target.value)}
              >
                <option value="GET">GET</option>
                <option value="POST">POST</option>
                <option value="PUT">PUT</option>
                <option value="DELETE">DELETE</option>
                <option value="PATCH">PATCH</option>
              </select>
            </div>
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-1">Request Body (for POST/PUT)</label>
              <textarea 
                className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white h-24 resize-none"
                value={(localRune.config?.body || '')}
                onChange={(e) => handleChange('config.body', e.target.value)}
                placeholder="{ }"
              />
            </div>
          </>
        );
        
      case 'AGENT_TASK_STUB':
        return (
          <>
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-1">Agent ID</label>
              <input 
                type="text" 
                className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white"
                value={(localRune.config?.agentId || '')}
                onChange={(e) => handleChange('config.agentId', e.target.value)}
                placeholder="agent-123"
              />
            </div>
            <div className="mb-4">
              <label className="block text-white text-sm font-medium mb-1">Task Description</label>
              <textarea 
                className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white h-24 resize-none"
                value={(localRune.config?.task || '')}
                onChange={(e) => handleChange('config.task', e.target.value)}
                placeholder="Analyze data and create a summary..."
              />
            </div>
          </>
        );
      
      default:
        return (
          <div className="text-white/70 italic text-sm">
            No additional properties for this rune type.
          </div>
        );
    }
  };
  
  return (
    <GlassmorphicPanel className="h-full overflow-y-auto p-0">
      <div className="p-4 border-b border-white/10 bg-white/5">
        <h2 className="text-lg font-semibold text-white">Properties</h2>
        <p className="text-sm text-white/70">Configure selected rune</p>
      </div>
      
      {!localRune ? (
        <div className="p-4 text-white/70">
          Select a rune to view and edit its properties.
        </div>
      ) : (
        <div className="p-4 space-y-4">
          <div className="mb-4">
            <label className="block text-white text-sm font-medium mb-1">Name</label>
            <input 
              type="text" 
              className="w-full bg-white/5 border border-white/20 rounded px-3 py-2 text-white"
              value={localRune.name}
              onChange={(e) => handleChange('name', e.target.value)}
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-white text-sm font-medium mb-1">Type</label>
            <div className="text-white bg-white/5 border border-white/20 rounded px-3 py-2">
              {localRune.type}
            </div>
          </div>
          
          {renderTypeSpecificFields()}
          
          <div className="mt-6">
            <button 
              className="w-full bg-primary-accent text-black font-medium py-2 px-4 rounded hover:bg-primary-accent/90 transition-colors"
              onClick={handleApplyChanges}
            >
              Apply Changes
            </button>
          </div>
        </div>
      )}
    </GlassmorphicPanel>
  );
};
