import { Play } from 'lucide-react';
import { memo } from 'react';
import { Handle, NodeProps, Position } from 'reactflow';

const StartNode = ({ data }: NodeProps) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-green-50 border-2 border-green-500 min-w-[150px]">
      <div className="flex items-center">
        <div className="rounded-full w-8 h-8 flex items-center justify-center bg-green-500 text-white">
          <Play size={16} />
        </div>
        <div className="ml-2">
          <div className="text-sm font-bold text-green-800">{data.label}</div>
          <div className="text-xs text-green-600">Workflow Start</div>
        </div>
      </div>
      
      {/* Only output handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-green-500"
      />
    </div>
  );
};

export default memo(StartNode);