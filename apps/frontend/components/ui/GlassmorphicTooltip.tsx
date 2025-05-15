import { glassmorphism } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

// Import from glasscn-ui
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from 'glasscn-ui/tooltip';

interface GlassmorphicTooltipProps {
  children: ReactNode;
  content: ReactNode;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
  className?: string;
  contentClassName?: string;
  delayDuration?: number;
}

export function GlassmorphicTooltip({
  children,
  content,
  side = 'top',
  align = 'center',
  className,
  contentClassName,
  delayDuration = 300,
}: GlassmorphicTooltipProps) {
  return (
    <TooltipProvider delayDuration={delayDuration}>
      <Tooltip>
        <TooltipTrigger asChild>
          <span className={className}>{children}</span>
        </TooltipTrigger>
        <TooltipContent
          side={side}
          align={align}
          sideOffset={4}
          className={cn(
            glassmorphism({ variant: 'heavy', border: 'thin' }),
            'z-50 overflow-hidden rounded-md px-3 py-1.5 text-xs text-white shadow-md animate-in fade-in-0 zoom-in-95',
            contentClassName
          )}
        >
          {content}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}