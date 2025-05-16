typescriptreact
import React, { memo } from 'react';
import { Handle, Position, NodeProps } from 'react-flow-renderer'; // Assuming v9 or v10 syntax. Adjust if using v11+

const GrimOSRuneNode: React.FC<NodeProps> = memo(({ data }) => {
  return (
    <div
      className="
        bg-[#1A1A1A] border border-[#7ED321]/50 text-[#7ED321] rounded-md shadow-lg
        px-4 py-2
        flex items-center space-x-2 // Use flex and spacing for horizontal layout
        hover:border-[#7ED321] transition-colors
      "
    >
      {/* Input Handle (Left Side) */}
      {/* In a real implementation, you'd iterate over inputs defined in data.inputs */}

      {/* Placeholder Input Handle */}
      <Handle
        type="target"
        position={Position.Top}
        className="!bg-[#7ED321]"
        isConnectable={true}
      />

      {/* Icon Placeholder */}
      {/* Replace with an actual icon based on Rune type */}
      <div className="w-6 h-6 bg-[#7ED321] rounded-full flex items-center justify-center text-[#1A1A1A] font-bold text-xs">
        {/* Icon */}
      </div>

      {/* Node Content */}
      <div className="text-sm font-mono flex-grow text-center">{data.label}</div> {/* Allow text to grow */}

      {/* Output Handle (Right Side) */}
      <Handle
        type="source"
        position={Position.Bottom}
        className="!bg-[#7ED321]"
        isConnectable={true}
      />
    </div>
  );
);

GrimOSRuneNode.displayName = 'GrimOSRuneNode';

export default GrimOSRuneNode;