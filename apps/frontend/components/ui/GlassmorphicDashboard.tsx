import { cn } from '@/lib/utils';
import { ReactNode } from 'react';
import { GlassmorphicCard } from './GlassmorphicCard';
import { GlassmorphicPanel } from './GlassmorphicPanel';

interface DashboardWidgetProps {
  title: string;
  children: ReactNode;
  className?: string;
  variant?: 'default' | 'accent' | 'highlight';
  footer?: ReactNode;
  loading?: boolean;
}

export function DashboardWidget({
  title,
  children,
  className,
  variant = 'default',
  footer,
  loading = false,
}: DashboardWidgetProps) {
  const variantClasses = {
    default: '',
    accent: 'border-l-4 border-l-secondary-accent',
    highlight: 'border-l-4 border-l-primary-accent',
  };

  return (
    <GlassmorphicCard
      title={title}
      className={cn('h-full', variantClasses[variant], className)}
      footer={footer}
    >
      {loading ? (
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-white/10 rounded w-3/4"></div>
          <div className="h-4 bg-white/10 rounded"></div>
          <div className="h-4 bg-white/10 rounded w-5/6"></div>
        </div>
      ) : (
        children
      )}
    </GlassmorphicCard>
  );
}

interface DashboardGridProps {
  children: ReactNode;
  className?: string;
}

export function DashboardGrid({ children, className }: DashboardGridProps) {
  return (
    <div
      className={cn(
        'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6',
        className
      )}
    >
      {children}
    </div>
  );
}

interface DashboardSectionProps {
  title?: string;
  description?: string;
  children: ReactNode;
  className?: string;
  fullWidth?: boolean;
}

export function DashboardSection({
  title,
  description,
  children,
  className,
  fullWidth = false,
}: DashboardSectionProps) {
  return (
    <section className={cn('mb-8', className)}>
      {(title || description) && (
        <div className="mb-4">
          {title && <h2 className="text-2xl font-semibold text-white">{title}</h2>}
          {description && <p className="mt-1 text-white/70">{description}</p>}
        </div>
      )}
      {fullWidth ? (
        children
      ) : (
        <GlassmorphicPanel variant="light" className="p-6">
          {children}
        </GlassmorphicPanel>
      )}
    </section>
  );
}

interface DashboardLayoutProps {
  children: ReactNode;
  sidebar?: ReactNode;
  header?: ReactNode;
  className?: string;
}

export function DashboardLayout({
  children,
  sidebar,
  header,
  className,
}: DashboardLayoutProps) {
  return (
    <div className={cn('flex h-screen bg-background', className)}>
      {sidebar && (
        <div className="h-full w-64 flex-shrink-0">
          {sidebar}
        </div>
      )}
      <div className="flex-1 flex flex-col overflow-hidden">
        {header && (
          <header className="flex-shrink-0">
            {header}
          </header>
        )}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}