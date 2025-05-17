import React from 'react';
import { Handle, Position } from 'react-flow-renderer';

interface GrimOSRuneNodeProps {
  data: {
    label: string;
    icon?: React.ReactNode;
  };
}

const GrimOSRuneNodeComponent: React.FC<GrimOSRuneNodeProps> = ({ data }) => {
  return (
    <div className="bg-gray-800 text-white p-4 rounded-lg shadow-md border border-gray-600">
      <div className="flex items-center space-x-2">
        {data.icon && <div className="text-xl">{data.icon}</div>}
        <span className="font-bold text-lg">{data.label}</span>
      </div>
      <Handle type="target" position={Position.Top} className="bg-blue-500" />
      <Handle type="source" position={Position.Bottom} className="bg-green-500" />
    </div>
  );
};

export default GrimOSRuneNodeComponent;
