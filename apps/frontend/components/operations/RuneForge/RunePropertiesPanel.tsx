typescriptreact
import React from 'react';

interface RunePropertiesPanelProps {
  // This component will eventually receive selected node data
  // selectedNode?: YourNodeType; // Define YourNodeType based on your store/data structure
}

export const RunePropertiesPanel: React.FC<RunePropertiesPanelProps> = () => {
  // For now, display a placeholder message
  // In the future, check if selectedNode exists and render properties form

  return (
    <div className="w-80 p-4 bg-gray-900 text-gray-100 border-l border-[#7ED321]/30 h-full overflow-y-auto">
      <h2 className="text-lg font-bold mb-4 text-[#7ED321]">Rune Properties</h2>
      {/* {selectedNode ? (
        // TODO: Implement dynamic form rendering based on selectedNode properties
        <div>
          <p className="text-sm mb-2">{selectedNode.data.label} Properties</p>
          {/* Placeholder for form elements based on node data */}
      {/* <div className="space-y-4">
            {/* Example: Input field for a common property */}
      {/* <div>
              <label className="block text-sm font-medium text-gray-400">Name</label>
              <input
                type="text"
                value={selectedNode.data.label}
                className="mt-1 block w-full p-2 bg-gray-800 border border-gray-700 rounded-md text-gray-100"
                readOnly // Or add onChange handler for editing
              />
            </div>
            {/* More dynamic fields based on node type/parameters */}
      {/* </div>
        </div>
      ) : ( */}
      <p className="text-sm text-gray-400">Select a Rune to view properties.</p>
      {/* )} */}
    </div>
  );
};