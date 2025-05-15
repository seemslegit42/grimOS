import React from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      svg: React.SVGProps<SVGSVGElement>;
      path: React.SVGProps<SVGPathElement>;
      circle: React.SVGProps<SVGCircleElement>;
      rect: React.SVGProps<SVGRectElement>;
      line: React.SVGProps<SVGLineElement>;
      polyline: React.SVGProps<SVGPolylineElement>;
      polygon: React.SVGProps<SVGPolygonElement>;
      g: React.SVGProps<SVGGElement>;
      defs: React.SVGProps<SVGDefsElement>;
      filter: React.SVGProps<SVGFilterElement>;
      feGaussianBlur: React.SVGProps<SVGFEGaussianBlurElement>;
      feOffset: React.SVGProps<SVGFEOffsetElement>;
      feComponentTransfer: React.SVGProps<SVGFEComponentTransferElement>;
      feFuncA: React.SVGProps<SVGFEFuncAElement>;
      feBlend: React.SVGProps<SVGFEBlendElement>;
      feColorMatrix: React.SVGProps<SVGFEColorMatrixElement>;
    }
  }
}