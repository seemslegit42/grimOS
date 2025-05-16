typescriptreact
import React from 'react';

interface RunePalettePanelProps {
  // Define props if needed
}

const placeholderRunes = [
  { id: 'placeholder-1', name: 'Placeholder Rune 1' },
  { id: 'placeholder-2', name: 'Placeholder Rune 2' },
  { id: 'placeholder-3', name: 'Placeholder Rune 3' },
  // Add more placeholders as needed
];

const RunePalettePanel: React.FC<RunePalettePanelProps> = () => {
  return (
    <div className="w-64 bg-[#121212] border-r border-[#7ED321]/50 p-4 flex flex-col overflow-y-auto">
      <h3 className="text-lg font-bold text-[#7ED321] mb-4">Rune Palette</h3>
      <div className="space-y-2">
        {placeholderRunes.map(rune => (
          <div
            key={rune.id}
            className="bg-[#1a1a1a] text-white border border-[#7ED321]/30 rounded-md p-3 text-sm cursor-grab hover:bg-[#7ED321]/10 transition-colors"
            // TODO: Implement drag and drop functionality
            onDragStart={(event) => {
              event.dataTransfer.setData('application/reactflow', rune.id);
              event.dataTransfer.effectAllowed = 'move';
            }}
            draggable
          >
            {rune.name}
          </div>
        ))}
      </div>
      {/* TODO: Implement search/filter for runes */}
      {/* TODO: Fetch real rune data from API */}
    </div>
  );
};

export default RunePalettePanel;