import { GitBranch } from 'lucide-react';
import { memo } from 'react';
import { Handle, NodeProps, Position } from 'reactflow';

const ConditionNode = ({ data }: NodeProps) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-yellow-50 border-2 border-yellow-500 min-w-[180px]">
      <div className="flex items-center">
        <div className="rounded-full w-8 h-8 flex items-center justify-center bg-yellow-500 text-white">
          <GitBranch size={16} />
        </div>
        <div className="ml-2">
          <div className="text-sm font-bold text-yellow-800">{data.label}</div>
          <div className="text-xs text-yellow-600">Condition</div>
        </div>
      </div>
      
      {data.condition && (
        <div className="mt-2 text-xs">
          <span className="font-semibold">Expression:</span>
          <p className="text-gray-600 mt-1 font-mono bg-gray-100 p-1 rounded">{data.condition}</p>
        </div>
      )}
      
      <div className="flex justify-between mt-2 text-xs">
        <div className="bg-green-100 px-2 py-1 rounded text-green-800">
          {data.trueLabel || 'Yes'}
        </div>
        <div className="bg-red-100 px-2 py-1 rounded text-red-800">
          {data.falseLabel || 'No'}
        </div>
      </div>
      
      {/* Input handle */}
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-yellow-500"
      />
      
      {/* Output handles for true/false paths */}
      <Handle
        type="source"
        position={Position.Bottom}
        id="true"
        className="w-3 h-3 bg-green-500"
        style={{ left: '30%' }}
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="false"
        className="w-3 h-3 bg-red-500"
        style={{ left: '70%' }}
      />
    </div>
  );
};

export default memo(ConditionNode);