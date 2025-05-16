import { UserCheck } from 'lucide-react';
import { memo } from 'react';
import { Handle, NodeProps, Position } from 'reactflow';

const ManualTaskNode = ({ data }: NodeProps) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-blue-50 border-2 border-blue-500 min-w-[180px]">
      <div className="flex items-center">
        <div className="rounded-full w-8 h-8 flex items-center justify-center bg-blue-500 text-white">
          <UserCheck size={16} />
        </div>
        <div className="ml-2">
          <div className="text-sm font-bold text-blue-800">{data.label}</div>
          <div className="text-xs text-blue-600">Manual Task</div>
        </div>
      </div>
      
      {data.assignee && (
        <div className="mt-2 text-xs">
          <span className="font-semibold">Assignee:</span> {data.assignee}
        </div>
      )}
      
      {data.instructions && (
        <div className="mt-1 text-xs max-h-20 overflow-y-auto">
          <span className="font-semibold">Instructions:</span>
          <p className="text-gray-600 mt-1">{data.instructions}</p>
        </div>
      )}
      
      {/* Input and output handles */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-blue-500"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-blue-500"
      />
    </div>
  );
};

export default memo(ManualTaskNode);