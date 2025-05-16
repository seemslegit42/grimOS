import { Square } from 'lucide-react';
import { memo } from 'react';
import { Handle, NodeProps, Position } from 'reactflow';

const EndNode = ({ data }: NodeProps) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-red-50 border-2 border-red-500 min-w-[150px]">
      <div className="flex items-center">
        <div className="rounded-full w-8 h-8 flex items-center justify-center bg-red-500 text-white">
          <Square size={16} />
        </div>
        <div className="ml-2">
          <div className="text-sm font-bold text-red-800">{data.label}</div>
          <div className="text-xs text-red-600">Workflow End</div>
        </div>
      </div>
      
      {/* Only input handle */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-red-500"
      />
    </div>
  );
};

export default memo(EndNode);