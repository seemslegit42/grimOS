import { Globe } from 'lucide-react';
import { memo } from 'react';
import { Handle, NodeProps, Position } from 'reactflow';

const ApiCallNode = ({ data }: NodeProps) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-purple-50 border-2 border-purple-500 min-w-[180px]">
      <div className="flex items-center">
        <div className="rounded-full w-8 h-8 flex items-center justify-center bg-purple-500 text-white">
          <Globe size={16} />
        </div>
        <div className="ml-2">
          <div className="text-sm font-bold text-purple-800">{data.label}</div>
          <div className="text-xs text-purple-600">API Call</div>
        </div>
      </div>
      
      <div className="mt-2 text-xs">
        {data.method && data.url && (
          <div className="flex items-center">
            <span className="font-mono bg-gray-100 px-1 rounded text-gray-800">{data.method}</span>
            <span className="ml-1 font-mono text-gray-600 truncate max-w-[120px]">{data.url}</span>
          </div>
        )}
      </div>
      
      {/* Input and output handles */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-purple-500"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-purple-500"
      />
    </div>
  );
};

export default memo(ApiCallNode);