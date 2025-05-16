typescriptreact
import React from 'react';
import { BaseEdge, EdgeLabelRenderer, EdgeProps, getBezierPath } from 'react-flow-renderer'; // Adjust import based on your react-flow version or use @react-flow/core
import { twMerge } from 'tailwind-merge';

// Define prop types if needed, based on your edge data structure
interface GrimOSConnectionLineProps extends EdgeProps {
  // Add any custom properties for your edge
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
  data, // Access custom edge data here
  markerEnd,
}) => {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  // Apply grimOS styling
  const grimOSStyle = {
    strokeWidth: 2,
    stroke: 'url(#grimOSGradient)', // Example: Use a gradient defined in SVG defs
    // Add other grimOS specific styles
    ...style, // Allow overriding with inline styles if necessary
  };

  return (
    <>
      {/* Define SVG gradient in your main SVG element or a Defs component */}
      {/* <defs>
        <linearGradient id="grimOSGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#7ED321" />
          <stop offset="100%" stopColor="#00AEEF" />
        </linearGradient>
      </defs> */}
      <BaseEdge path={edgePath} markerEnd={markerEnd} style={grimOSStyle} />
      {/* Optional: Edge Label Renderer for displaying text on the edge */}
      {/* <EdgeLabelRenderer
        x={labelX}
        y={labelY}
        // You can adjust the position of the label here
        transform={`translate(-50%, -50%) translate(${labelX},${labelY})`}
        className="nodrag nopan" // Prevent dragging/panning when interacting with the label
      >
        <div
          style={{
            pointerEvents: 'all',
          }}
          className={twMerge(
            'px-2 py-1 text-xs font-bold text-white bg-black rounded-md',
            data?.labelClassName // Allow custom class from edge data
          )}
        >
          {data?.label} {/* Access label from edge data */}
        </div>
      </EdgeLabelRenderer> */}
    </>
  );
};

export default GrimOSConnectionLine;