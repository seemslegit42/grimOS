import { glassmorphicCard, GlassmorphismBorderVariant, GlassmorphismVariant } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { forwardRef, ReactNode } from 'react';

// Import Card components from glasscn-ui
// Note: If these imports fail, you may need to adjust the import path based on your project setup
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from 'glasscn-ui/card';

interface GlassmorphicCardProps {
  children: ReactNode;
  className?: string;
  variant?: GlassmorphismVariant;
  border?: GlassmorphismBorderVariant;
  title?: string;
  description?: string;
  footer?: ReactNode;
  onClick?: () => void;
  headerClassName?: string;
  contentClassName?: string;
  footerClassName?: string;
}

export const GlassmorphicCard = forwardRef<HTMLDivElement, GlassmorphicCardProps>(
  ({ 
    children, 
    className, 
    variant = 'medium', 
    border = 'thin',
    title,
    description,
    footer,
    onClick,
    headerClassName,
    contentClassName,
    footerClassName
  }, ref) => {
    // Use glasscn-ui Card component with our custom glassmorphic styling
    return (
      <Card 
        ref={ref}
        className={cn(
          glassmorphicCard({ variant, border }),
          'text-white',
          onClick && 'cursor-pointer transition-all hover:bg-white/15 hover:shadow-lg',
          className
        )}
        onClick={onClick}
      >
        {(title || description) && (
          <CardHeader className={headerClassName}>
            {title && (
              <CardTitle className="text-xl font-semibold text-primary-accent">
                {title}
              </CardTitle>
            )}
            {description && (
              <CardDescription className="text-white/70">
                {description}
              </CardDescription>
            )}
          </CardHeader>
        )}
        
        <CardContent className={cn("flex-1", contentClassName)}>
          {children}
        </CardContent>
        
        {footer && (
          <CardFooter className={cn("border-t border-white/10 pt-4", footerClassName)}>
            {footer}
          </CardFooter>
        )}
      </Card>
    );
  }
);

GlassmorphicCard.displayName = 'GlassmorphicCard';