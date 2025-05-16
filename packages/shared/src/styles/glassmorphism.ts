import { cva } from 'class-variance-authority';
import { cn } from '../utils';

export type GlassmorphismVariant = 'light' | 'medium' | 'heavy';
export type GlassmorphismBorderVariant = 'none' | 'thin' | 'medium';

interface GlassmorphismOptions {
  variant?: GlassmorphismVariant;
  border?: GlassmorphismBorderVariant;
  className?: string;
}

/**
 * Glassmorphism variants using class-variance-authority for better integration with shadcn/ui
 */
export const glassmorphismVariants = cva(
  'backdrop-blur-md transition-all duration-200',
  {
    variants: {
      variant: {
        light: 'bg-white/5 backdrop-blur-sm',
        medium: 'bg-white/10 backdrop-blur-md',
        heavy: 'bg-white/15 backdrop-blur-xl',
      },
      border: {
        none: 'border-0',
        thin: 'border border-white/20',
        medium: 'border-2 border-white/30',
      },
      rounded: {
        none: 'rounded-none',
        sm: 'rounded-md',
        md: 'rounded-lg',
        lg: 'rounded-xl',
        full: 'rounded-full',
      },
      shadow: {
        none: 'shadow-none',
        sm: 'shadow-sm',
        md: 'shadow-md',
        lg: 'shadow-[0_8px_32px_rgba(0,0,0,0.1)]',
      },
    },
    defaultVariants: {
      variant: 'medium',
      border: 'thin',
      rounded: 'md',
      shadow: 'none',
    },
  }
);

/**
 * Utility function to generate glassmorphic effect classes
 * 
 * @param options - Configuration options for the glassmorphic effect
 * @returns Tailwind CSS classes for the glassmorphic effect
 */
export function glassmorphism({
  variant = 'medium',
  border = 'thin',
  className,
}: GlassmorphismOptions = {}): string {
  return cn(
    glassmorphismVariants({ variant, border }),
    className
  );
}

/**
 * Utility function to generate glassmorphic card effect classes
 * 
 * @param options - Configuration options for the glassmorphic card
 * @returns Tailwind CSS classes for the glassmorphic card
 */
export function glassmorphicCard(options: GlassmorphismOptions = {}): string {
  return cn(
    glassmorphismVariants({ 
      variant: options.variant, 
      border: options.border,
      rounded: 'lg',
      shadow: 'lg'
    }),
    options.className
  );
}

/**
 * Utility function to generate glassmorphic panel effect classes
 * 
 * @param options - Configuration options for the glassmorphic panel
 * @returns Tailwind CSS classes for the glassmorphic panel
 */
export function glassmorphicPanel(options: GlassmorphismOptions = {}): string {
  return cn(
    glassmorphismVariants({ 
      variant: options.variant, 
      border: options.border,
      rounded: 'md',
      shadow: 'none'
    }),
    options.className
  );
}