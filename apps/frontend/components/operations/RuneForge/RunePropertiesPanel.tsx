import { Button } from '@/components/ui/button';
import { GlassmorphicPanel } from '@/components/ui/GlassmorphicPanel';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { AvailableRuneType, FormFieldDefinitionType, useRuneForgeStore } from '@/lib/store/RuneForgeStore';
import { motion } from 'framer-motion';
import React, { useEffect, useState } from 'react';
import { Node } from 'reactflow';

// Helper to determine input type for shadcn/ui components
const getShadcnInputType = (fieldType: FormFieldDefinitionType['fieldType']): string => {
  switch (fieldType) {
    case 'text':
    case 'json': // JSON can be edited as text initially
      return 'text';
    // Add other mappings if necessary, e.g., 'number', 'email', 'password'
    default:
      return 'text';
  }
};

export const RunePropertiesPanel: React.FC = () => {
  const selectedNodeId = useRuneForgeStore((state) => state.selected_node_id);
  const flowNodes = useRuneForgeStore((state) => state.flow_nodes);
  const availableRunes = useRuneForgeStore((state) => state.available_runes);
  const updateRuneParameters = useRuneForgeStore((state) => state.updateRuneParameters);

  const selectedNode: Node | undefined = flowNodes.find((node: Node) => node.id === selectedNodeId);
  // Ensure selectedNode and selectedNode.data exist before trying to access n8nNodeType
  const runeSchema: AvailableRuneType | undefined = selectedNode && selectedNode.data ? availableRunes.find(
    (r: AvailableRuneType) => r.id === selectedNode.data.n8nNodeType
  ) : undefined;

  const [formData, setFormData] = useState<Record<string, any>>({});
  const [jsonErrorFields, setJsonErrorFields] = useState<Record<string, boolean>>({});


  useEffect(() => {
    if (selectedNode?.data?.parameters) {
      setFormData(selectedNode.data.parameters);
      // Reset JSON errors when node changes
      const initialJsonErrors: Record<string, boolean> = {};
      if (runeSchema?.parametersSchema) {
        runeSchema.parametersSchema.forEach(param => {
          if (param.fieldType === 'json') {
            initialJsonErrors[param.name] = false;
          }
        });
      }
      setJsonErrorFields(initialJsonErrors);
    } else {
      setFormData({});
      setJsonErrorFields({});
    }
  }, [selectedNode, runeSchema]);

  const handleInputChange = (paramName: string, value: any, fieldType?: FormFieldDefinitionType['fieldType']) => {
    if (fieldType === 'json') {
      try {
        const parsedJson = JSON.parse(value);
        setFormData((prev: Record<string, any>) => ({ ...prev, [paramName]: parsedJson }));
        setJsonErrorFields(prev => ({ ...prev, [paramName]: false }));
      } catch (error) {
        // Store as string if invalid JSON, and mark as error
        setFormData((prev: Record<string, any>) => ({ ...prev, [paramName]: value }));
        setJsonErrorFields(prev => ({ ...prev, [paramName]: true }));
      }
    } else {
      setFormData((prev: Record<string, any>) => ({ ...prev, [paramName]: value }));
    }
  };

  const handleSaveChanges = () => {
    if (selectedNodeId) {
      // Filter out any fields that are marked as JSON errors before saving,
      // or ensure the store/backend can handle potentially malformed JSON strings.
      // For now, we send what's in formData. The user should fix JSON errors.
      let hasErrors = false;
      Object.values(jsonErrorFields).forEach(hasError => {
        if (hasError) {
          hasErrors = true;
        }
      });

      if (hasErrors) {
        // Optionally, alert the user or prevent saving
        // For now, we'll allow saving, but the invalid JSON will be a string.
        console.warn("Attempting to save with invalid JSON fields. These will be saved as strings.");
      }
      updateRuneParameters(selectedNodeId, formData);
    }
  };

  if (!selectedNode || !runeSchema) {
    return (
      <GlassmorphicPanel className="w-80 p-0 flex flex-col h-full overflow-y-auto border border-white/20 bg-opacity-10 backdrop-blur-md">
        <div className="p-4 border-b border-white/10 bg-black/20 sticky top-0 z-10 flex-shrink-0">
          <h2 className="text-lg font-semibold text-lime-400">Rune Properties</h2>
        </div>
        <div className="flex-grow flex items-center justify-center p-4">
          <p className="text-sm text-white/70 text-center">
            Select a Rune on the canvas to view and edit its properties.
          </p>
        </div>
      </GlassmorphicPanel>
    );
  }

  return (
    <GlassmorphicPanel className="w-80 p-0 flex flex-col h-full border border-white/20 bg-opacity-10 backdrop-blur-md">
      <div className="p-4 border-b border-white/10 bg-black/20 sticky top-0 z-10 flex-shrink-0">
        <h2 className="text-lg font-semibold text-lime-400">Rune Properties</h2>
        <p className="text-sm text-white/70 truncate" title={selectedNode.data.label || 'Selected Rune'}>
          Editing: {selectedNode.data.label || 'Unnamed Rune'} ({runeSchema.displayName})
        </p>
      </div>

      <motion.div
        key={selectedNodeId} 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="p-4 space-y-6 flex-grow overflow-y-auto"
      >
        {runeSchema.parametersSchema && runeSchema.parametersSchema.length > 0 ? (
          runeSchema.parametersSchema.map((param: FormFieldDefinitionType) => (
            <div key={param.name} className="space-y-2">
              <Label htmlFor={param.name} className="text-white/90 text-sm font-medium">
                {param.label}
                {param.required && <span className="text-red-400 ml-1">*</span>}
              </Label>
              {param.description && (
                <p className="text-xs text-white/60 mb-1">{param.description}</p>
              )}
              {param.fieldType === 'text' && (
                <Input
                  id={param.name}
                  type={getShadcnInputType(param.fieldType)}
                  value={formData[param.name] || ''}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleInputChange(param.name, e.target.value)}
                  placeholder={param.defaultValue?.toString() || `Enter ${param.label.toLowerCase()}`}
                  className="bg-black/30 border-lime-400/30 text-white placeholder:text-white/50 focus:border-lime-400 focus:ring-lime-400/50"
                />
              )}
              {param.fieldType === 'textarea' && (
                <Textarea
                  id={param.name}
                  value={formData[param.name] || ''}
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleInputChange(param.name, e.target.value)}
                  placeholder={param.defaultValue?.toString() || `Enter ${param.label.toLowerCase()}`}
                  className="bg-black/30 border-lime-400/30 text-white placeholder:text-white/50 focus:border-lime-400 focus:ring-lime-400/50 h-24"
                />
              )}
              {param.fieldType === 'json' && (
                <>
                  <Textarea
                    id={param.name}
                    value={typeof formData[param.name] === 'object' ? JSON.stringify(formData[param.name], null, 2) : formData[param.name] || ''}
                    onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleInputChange(param.name, e.target.value, 'json')}
                    placeholder={param.defaultValue ? JSON.stringify(param.defaultValue, null, 2) : `Enter JSON for ${param.label.toLowerCase()}`}
                    className={`bg-black/30 border-lime-400/30 text-white placeholder:text-white/50 focus:border-lime-400 focus:ring-lime-400/50 h-32 font-mono text-xs ${jsonErrorFields[param.name] ? 'border-red-500 focus:border-red-500 focus:ring-red-500/50' : ''}`}
                  />
                  {jsonErrorFields[param.name] && (
                    <p className="text-xs text-red-400">Invalid JSON format. Will be saved as a string.</p>
                  )}
                </>
              )}
              {param.fieldType === 'select' && param.options && (
                <Select
                  value={formData[param.name]?.toString() || param.defaultValue?.toString() || ''}
                  onValueChange={(value: string) => handleInputChange(param.name, value)}
                >
                  <SelectTrigger id={param.name} className="bg-black/30 border-lime-400/30 text-white focus:border-lime-400 focus:ring-lime-400/50">
                    <SelectValue placeholder={`Select ${param.label.toLowerCase()}`} />
                  </SelectTrigger>
                  <SelectContent className="bg-black/80 border-lime-400/50 text-white backdrop-blur-md">
                    {param.options.map((option) => (
                      <SelectItem key={option.value} value={option.value} className="hover:bg-lime-400/20 focus:bg-lime-400/30 cursor-pointer">
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
              {param.fieldType === 'boolean' && (
                <div className="flex items-center space-x-3 pt-1">
                  <Switch
                    id={param.name}
                    checked={!!formData[param.name]}
                    onCheckedChange={(checked: boolean) => handleInputChange(param.name, checked)}
                    className="data-[state=checked]:bg-lime-500 data-[state=unchecked]:bg-gray-700"
                  />
                  <Label htmlFor={param.name} className="text-white/80 text-sm cursor-pointer select-none">
                    {/* Display custom true/false labels if provided, otherwise default to Enabled/Disabled */}
                    {formData[param.name] 
                      ? (param.trueLabel || 'Enabled') 
                      : (param.falseLabel || 'Disabled')}
                  </Label>
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="flex-grow flex items-center justify-center p-6">
            <p className="text-sm text-white/70 italic text-center">
              This Rune has no configurable properties.
            </p>
          </div>
        )}
        {runeSchema.parametersSchema && runeSchema.parametersSchema.length > 0 && (
          <div className="pt-4 sticky bottom-0 bg-black/20 backdrop-blur-sm pb-4 px-4 -mx-4">
            <Button 
              onClick={handleSaveChanges} 
              className="w-full bg-lime-500 hover:bg-lime-600 text-black font-semibold transition-all duration-200 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-lime-400 focus:ring-opacity-75"
              disabled={Object.values(jsonErrorFields).some(err => err)}
            >
              Apply Changes
            </Button>
            {Object.values(jsonErrorFields).some(err => err) && (
              <p className="text-xs text-red-400 mt-2 text-center">
                Please fix invalid JSON fields before applying changes.
              </p>
            )}
          </div>
        )}
      </motion.div>
    </GlassmorphicPanel>
  );
};

export default RunePropertiesPanel;