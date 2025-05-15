import { glassmorphism } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { ReactNode, useState } from 'react';
import { Button } from './Button';

// This component assumes you have lucide-react installed
// If not, you can replace the icons with your own implementation
// import { ChevronLeft, ChevronRight } from 'lucide-react';

interface SidebarItem {
  id: string;
  label: string;
  icon: ReactNode;
  href?: string;
}

interface GlassmorphicSidebarProps {
  items: SidebarItem[];
  activeItemId?: string;
  onItemClick?: (item: SidebarItem) => void;
  logo?: ReactNode;
  className?: string;
  collapsible?: boolean;
  defaultCollapsed?: boolean;
}

export function GlassmorphicSidebar({
  items,
  activeItemId,
  onItemClick,
  logo,
  className,
  collapsible = true,
  defaultCollapsed = false,
}: GlassmorphicSidebarProps) {
  const [collapsed, setCollapsed] = useState(defaultCollapsed);

  const toggleCollapsed = () => {
    if (collapsible) {
      setCollapsed(!collapsed);
    }
  };

  return (
    <div
      className={cn(
        glassmorphism({ variant: 'medium', border: 'thin' }),
        'flex flex-col h-full transition-all duration-300',
        collapsed ? 'w-16' : 'w-64',
        className
      )}
    >
      {/* Logo area */}
      <div className="p-4 flex items-center justify-between border-b border-white/10">
        {!collapsed && logo && <div className="flex-1">{logo}</div>}
        {collapsible && (
          <Button
            variant="ghost"
            size="sm"
            className="p-1 h-8 w-8 rounded-full text-white/70 hover:text-white hover:bg-white/10"
            onClick={toggleCollapsed}
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {/* Replace with actual icons if lucide-react is available */}
            {collapsed ? (
              <span>→</span> // Replace with <ChevronRight size={18} />
            ) : (
              <span>←</span> // Replace with <ChevronLeft size={18} />
            )}
          </Button>
        )}
      </div>

      {/* Navigation items */}
      <div className="flex-1 py-4 overflow-y-auto">
        <ul className="space-y-2 px-2">
          {items.map((item) => (
            <li key={item.id}>
              <a
                href={item.href || '#'}
                className={cn(
                  'flex items-center rounded-md px-3 py-2 transition-colors',
                  'hover:bg-white/10',
                  activeItemId === item.id
                    ? 'bg-primary-accent/20 text-primary-accent'
                    : 'text-white/80 hover:text-white',
                  collapsed && 'justify-center'
                )}
                onClick={(e) => {
                  if (!item.href || item.href === '#') {
                    e.preventDefault();
                  }
                  onItemClick?.(item);
                }}
              >
                <span className="flex-shrink-0">{item.icon}</span>
                {!collapsed && <span className="ml-3">{item.label}</span>}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}