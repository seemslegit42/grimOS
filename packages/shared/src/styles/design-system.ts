/**
 * Shared Design System for BitBrew Inc.
 * 
 * This file contains shared design tokens, colors, and styles that can be used
 * across both the web (React/Vite) and frontend (Next.js) applications.
 */

export const colors = {
  // Primary palette
  background: {
    primary: '#121212',
    secondary: '#1A1A1A',
    tertiary: '#1E1E1E',
  },
  
  // Digital Weave Palette
  accent: {
    primary: '#7ED321',    // Neon Green
    secondary: '#00BFFF',  // Cyan Blue
    tertiary: '#FF1D58',   // Magenta Red
  },
  
  // Text colors
  text: {
    primary: '#FFFFFF',
    secondary: 'rgba(255, 255, 255, 0.8)',
    tertiary: 'rgba(255, 255, 255, 0.6)',
    disabled: 'rgba(255, 255, 255, 0.4)',
  },
  
  // Border colors
  border: {
    primary: 'rgba(255, 255, 255, 0.1)',
    secondary: 'rgba(255, 255, 255, 0.05)',
    accent: {
      primary: 'rgba(126, 211, 33, 0.3)',
      secondary: 'rgba(0, 191, 255, 0.3)',
      tertiary: 'rgba(255, 29, 88, 0.3)',
    },
  },
};

export const glassmorphism = {
  // Glassmorphism variables
  background: {
    light: 'rgba(18, 18, 18, 0.1)',
    medium: 'rgba(18, 18, 18, 0.2)',
    heavy: 'rgba(18, 18, 18, 0.3)',
  },
  border: {
    light: 'rgba(255, 255, 255, 0.05)',
    medium: 'rgba(255, 255, 255, 0.1)',
    heavy: 'rgba(255, 255, 255, 0.15)',
  },
  blur: {
    light: '5px',
    medium: '10px',
    heavy: '15px',
  },
};

export const shadows = {
  primary: '0 8px 32px rgba(0, 0, 0, 0.2)',
  accent: {
    primary: '0 0 15px rgba(126, 211, 33, 0.3)',
    secondary: '0 0 15px rgba(0, 191, 255, 0.3)',
    tertiary: '0 0 15px rgba(255, 29, 88, 0.3)',
  },
};

export const typography = {
  fontFamily: {
    primary: 'Inter, system-ui, sans-serif',
    mono: 'JetBrains Mono, monospace',
  },
  fontSize: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
    '4xl': '2.25rem',
    '5xl': '3rem',
  },
  fontWeight: {
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
};

export const spacing = {
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  '2xl': '3rem',
  '3xl': '4rem',
  '4xl': '6rem',
};

export const borderRadius = {
  sm: '0.25rem',
  md: '0.5rem',
  lg: '0.75rem',
  xl: '1rem',
  '2xl': '1.5rem',
  full: '9999px',
};

export const animations = {
  transition: {
    fast: 'all 0.2s ease',
    medium: 'all 0.3s ease',
    slow: 'all 0.5s ease',
  },
  keyframes: {
    pulse: `
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
    `,
    glow: `
      @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(126, 211, 33, 0.5); }
        50% { box-shadow: 0 0 20px rgba(126, 211, 33, 0.8); }
      }
    `,
    borderGlow: `
      @keyframes borderGlow {
        0% {
          border-image-source: linear-gradient(
            45deg, 
            rgba(126, 211, 33, 1), 
            rgba(0, 191, 255, 0.5)
          );
        }
        50% {
          border-image-source: linear-gradient(
            45deg, 
            rgba(0, 191, 255, 0.5), 
            rgba(255, 29, 88, 1)
          );
        }
        100% {
          border-image-source: linear-gradient(
            45deg, 
            rgba(255, 29, 88, 1), 
            rgba(126, 211, 33, 0.5)
          );
        }
      }
    `,
  },
};

// CSS class utilities for common patterns
export const cssUtilities = {
  glassmorphic: `
    background: rgba(18, 18, 18, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
  `,
  digitalWeaveBackground: `
    position: relative;
    &::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: 
        linear-gradient(rgba(126, 211, 33, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(126, 211, 33, 0.05) 1px, transparent 1px);
      background-size: 40px 40px;
      background-position: -1px -1px;
      z-index: -1;
    }
  `,
  neonText: {
    primary: `
      color: #7ED321;
      text-shadow: 0 0 5px rgba(126, 211, 33, 0.5);
    `,
    secondary: `
      color: #00BFFF;
      text-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
    `,
    tertiary: `
      color: #FF1D58;
      text-shadow: 0 0 5px rgba(255, 29, 88, 0.5);
    `,
  },
  gradientBorder: `
    border: 2px solid;
    border-image-slice: 1;
    border-image-source: linear-gradient(
      45deg, 
      rgba(126, 211, 33, 1), 
      rgba(0, 191, 255, 0.5)
    );
    animation: borderGlow 8s infinite alternate;
  `,
};

// Export glassmorphism utilities
export * from './glassmorphism';

// Export everything as a design system object
export const designSystem = {
  colors,
  glassmorphism,
  shadows,
  typography,
  spacing,
  borderRadius,
  animations,
  cssUtilities,
};

export default designSystem;