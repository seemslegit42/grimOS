import { glassmorphism } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

// Try to import from glasscn-ui first, then fall back to radix-ui
// Note: If these imports fail, you may need to adjust the import path based on your project setup
let Tabs: any;
let TabsList: any;
let TabsTrigger: any;
let TabsContent: any;

try {
  // Try to import from glasscn-ui
  const glasscnTabs = require('glasscn-ui/tabs');
  Tabs = glasscnTabs.Tabs;
  TabsList = glasscnTabs.TabsList;
  TabsTrigger = glasscnTabs.TabsTrigger;
  TabsContent = glasscnTabs.TabsContent;
} catch (e) {
  // Fall back to radix-ui
  const TabsPrimitive = require('@radix-ui/react-tabs');
  Tabs = TabsPrimitive.Root;
  TabsList = TabsPrimitive.List;
  TabsTrigger = TabsPrimitive.Trigger;
  TabsContent = TabsPrimitive.Content;
}

interface GlassmorphicTabsProps {
  tabs: {
    id: string;
    label: ReactNode;
    content: ReactNode;
    icon?: ReactNode;
  }[];
  defaultValue?: string;
  onChange?: (value: string) => void;
  className?: string;
  tabsClassName?: string;
  contentClassName?: string;
}

export function GlassmorphicTabs({
  tabs,
  defaultValue,
  onChange,
  className,
  tabsClassName,
  contentClassName,
}: GlassmorphicTabsProps) {
  // Use the first tab as default if not specified
  const defaultTab = defaultValue || tabs[0]?.id;

  return (
    <Tabs
      defaultValue={defaultTab}
      onValueChange={onChange}
      className={cn('flex flex-col', className)}
    >
      <TabsList
        className={cn(
          glassmorphism({ variant: 'light', border: 'thin' }),
          'flex rounded-t-lg overflow-x-auto',
          tabsClassName
        )}
      >
        {tabs.map((tab) => (
          <TabsTrigger
            key={tab.id}
            value={tab.id}
            className={cn(
              'flex items-center px-4 py-2.5 text-sm font-medium',
              'border-b-2 border-transparent',
              'data-[state=active]:border-primary-accent data-[state=active]:text-primary-accent',
              'text-white/70 hover:text-white',
              'focus:outline-none focus-visible:ring-2 focus-visible:ring-white/20 focus-visible:ring-offset-2',
              'transition-colors'
            )}
          >
            {tab.icon && <span className="mr-2">{tab.icon}</span>}
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
      {tabs.map((tab) => (
        <TabsContent
          key={tab.id}
          value={tab.id}
          className={cn(
            glassmorphism({ variant: 'medium', border: 'thin' }),
            'rounded-b-lg p-4 border-t-0 flex-1',
            contentClassName
          )}
        >
          {tab.content}
        </TabsContent>
      ))}
    </Tabs>
  );
}