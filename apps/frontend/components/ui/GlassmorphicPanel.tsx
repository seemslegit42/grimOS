import { glassmorphicPanel, GlassmorphismBorderVariant, GlassmorphismVariant } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { forwardRef, ReactNode } from 'react';

// Import from glasscn-ui if available
// Note: If these imports fail, you may need to adjust the import path based on your project setup

interface GlassmorphicPanelProps {
  children: ReactNode;
  className?: string;
  variant?: GlassmorphismVariant;
  border?: GlassmorphismBorderVariant;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  asChild?: boolean;
}

export const GlassmorphicPanel = forwardRef<HTMLDivElement, GlassmorphicPanelProps>(
  ({ 
    children, 
    className, 
    variant = 'medium', 
    border = 'thin',
    padding = 'md',
    asChild = false
  }, ref) => {
    const paddingClasses = {
      none: '',
      sm: 'p-2',
      md: 'p-4',
      lg: 'p-6'
    };
    
    return (
      <div 
        ref={ref}
        className={cn(
          glassmorphicPanel({ variant, border }),
          paddingClasses[padding],
          'text-white',
          className
        )}
      >
        {children}
      </div>
    );
  }
);

GlassmorphicPanel.displayName = 'GlassmorphicPanel';