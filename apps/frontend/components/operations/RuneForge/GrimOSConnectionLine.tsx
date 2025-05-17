import { motion } from 'framer-motion';
import React from 'react';
import { EdgeProps, getBezierPath } from 'reactflow'; // Corrected import for reactflow

// Removed twMerge import as it's not used in the corrected version of the component

interface GrimOSConnectionLineProps extends EdgeProps {
  // Custom properties for the edge can be added here
}

const GrimOSConnectionLine: React.FC<GrimOSConnectionLineProps> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
}) => {
  const [edgePath] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const gradientId = `grimOSGradient-${id}`;

  // grimOS styling for the connection line
  const grimOSStyle = {
    strokeWidth: 2,
    stroke: `url(#${gradientId})`,
    fill: 'none',
    ...style,
  };

  return (
    <>
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style={{ stopColor: '#7ED321', stopOpacity: 1 }} /> {/* Lime Green */}
          <stop offset="100%" style={{ stopColor: '#00BFFF', stopOpacity: 1 }} /> {/* Electric Blue */}
        </linearGradient>
      </defs>
      <motion.path
        className="react-flow__edge-path" // Standard React Flow class for paths
        d={edgePath}
        markerEnd={markerEnd}
        style={grimOSStyle}
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 1 }}
        transition={{ duration: 0.7, ease: "easeInOut" }}
      />
      {/* EdgeLabelRenderer and related logic for labels can be added here if needed */}
    </>
  );
};

export default GrimOSConnectionLine;