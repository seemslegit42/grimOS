import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'; // Assuming shadcn/ui Card
import { GlassmorphicPanel } from '@/components/ui/GlassmorphicPanel'; // Assuming glasscn-ui panel
import { AvailableRuneType, useRuneForgeStore } from '@/lib/store/RuneForgeStore'; // Assuming store path
import { motion } from 'framer-motion';
import { Package } from 'lucide-react'; // Example icon, replace with actual iconName from rune data
import React from 'react';

// Helper to get Lucide icon component by name
// This is a simplified example. In a real app, you might have a more robust icon mapping.
const LucideIcon = ({ name, ...props }: { name: string; [key: string]: any }) => {
  // For demo, using a default icon. Replace with dynamic import or a map.
  // Example: const IconComponent = await import('lucide-react')[name as keyof typeof import('lucide-react')];
  // This dynamic import approach has its own complexities (e.g., with bundlers, SSR).
  // A simpler approach for a known set of icons is a switch statement or a map.
  if (name === 'Package') return <Package {...props} />;
  // Add other icons as needed or implement a dynamic loading strategy
  return <Package {...props} />; // Default icon
};

const RunePalettePanel: React.FC = () => {
  const availableRunes = useRuneForgeStore((state) => state.available_runes);
  // const addFlowNode = useRuneForgeStore((state) => state.addFlowNode); // Action to add node to canvas

  const handleDragStart = (event: React.DragEvent<HTMLDivElement>, rune: AvailableRuneType) => {
    const nodePayload = {
      type: 'GrimOSRuneNode', // The custom node type for the canvas
      data: {
        label: rune.displayName,
        iconName: rune.iconName,
        n8nNodeType: rune.id, // Or a more specific n8n type if different from id
        parameters: rune.parametersSchema.reduce((acc, param) => {
          acc[param.name] = param.defaultValue;
          return acc;
        }, {} as Record<string, any>),
        // Any other initial data your GrimOSRuneNodeComponent expects
      },
      // Position will be set on drop by react-flow or custom drop handler
    };
    event.dataTransfer.setData('application/reactflow', JSON.stringify(nodePayload));
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <GlassmorphicPanel className="w-72 p-0 flex flex-col h-full overflow-y-auto border-r border-white/10 bg-opacity-10 backdrop-blur-md">
      <div className="p-4 border-b border-white/10 bg-white/5 sticky top-0 z-10">
        <h3 className="text-lg font-semibold text-white">Rune Palette</h3>
        <p className="text-sm text-white/70">Drag Runes to Canvas</p>
      </div>
      <div className="p-4 space-y-3 flex-grow">
        {availableRunes && availableRunes.length > 0 ? (
          availableRunes.map((rune) => (
            <motion.div
              key={rune.id}
              whileHover={{ scale: 1.03, boxShadow: "0px 0px 12px rgba(126, 211, 33, 0.5)" }}
              transition={{ type: 'spring', stiffness: 300 }}
              className="cursor-grab"
              onDragStart={(event) => handleDragStart(event, rune)}
              draggable
            >
              <Card className="bg-black/30 border-lime-400/30 hover:border-lime-400/70 transition-colors duration-200 text-white">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 p-4">
                  <CardTitle className="text-sm font-medium text-lime-400">
                    {rune.displayName}
                  </CardTitle>
                  <LucideIcon name={rune.iconName || 'Package'} className="h-5 w-5 text-lime-400/80" />
                </CardHeader>
                <CardContent className="p-4 pt-0">
                  <p className="text-xs text-white/70">
                    {rune.category} - (Drag me!)
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))
        ) : (
          <div className="text-center text-white/50 py-10">
            <p>No Runes available.</p>
            <p className="text-xs">Ensure Runes are loaded in the store.</p>
          </div>
        )}
      </div>
    </GlassmorphicPanel>
  );
};

export default RunePalettePanel;