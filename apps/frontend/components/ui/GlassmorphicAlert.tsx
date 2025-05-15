import { glassmorphism } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

type AlertVariant = 'info' | 'success' | 'warning' | 'error';

interface GlassmorphicAlertProps {
  children: ReactNode;
  variant?: AlertVariant;
  title?: string;
  icon?: ReactNode;
  className?: string;
  onClose?: () => void;
}

export function GlassmorphicAlert({
  children,
  variant = 'info',
  title,
  icon,
  className,
  onClose,
}: GlassmorphicAlertProps) {
  // Define variant-specific styles
  const variantStyles: Record<AlertVariant, { borderColor: string; iconColor: string }> = {
    info: {
      borderColor: 'border-secondary-accent',
      iconColor: 'text-secondary-accent',
    },
    success: {
      borderColor: 'border-primary-accent',
      iconColor: 'text-primary-accent',
    },
    warning: {
      borderColor: 'border-yellow-500',
      iconColor: 'text-yellow-500',
    },
    error: {
      borderColor: 'border-tertiary-accent',
      iconColor: 'text-tertiary-accent',
    },
  };

  const { borderColor, iconColor } = variantStyles[variant];

  return (
    <div
      className={cn(
        glassmorphism({ variant: 'medium', border: 'none' }),
        'rounded-lg p-4 border-l-4',
        borderColor,
        className
      )}
    >
      <div className="flex">
        {icon && <div className={cn('flex-shrink-0 mr-3', iconColor)}>{icon}</div>}
        <div className="flex-1">
          {title && <h3 className="text-sm font-medium text-white">{title}</h3>}
          <div className={cn('text-sm text-white/80', title && 'mt-1')}>{children}</div>
        </div>
        {onClose && (
          <button
            type="button"
            className="flex-shrink-0 ml-3 text-white/60 hover:text-white"
            onClick={onClose}
            aria-label="Close"
          >
            {/* Replace with actual icon if lucide-react is available */}
            <span aria-hidden="true">×</span>
          </button>
        )}
      </div>
    </div>
  );
}