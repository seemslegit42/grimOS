# Grimoire™ (grimOS) Glassmorphic UI Components

This directory contains a set of React components implementing the "Corporate Cyberpunk" with "Digital Weave" palette and Glassmorphism design as specified in the UI/UX Design Specification for MVP.

## Integration with shadcn/ui and glasscn-ui

These components are built on top of shadcn/ui and glasscn-ui libraries, providing a consistent and accessible design system with a glassmorphic aesthetic. The components attempt to use glasscn-ui components when available, with fallbacks to shadcn/ui or custom implementations when necessary.

## Components Overview

### Core Components

- **GlassmorphicCard**: A card component with glassmorphic styling, supporting titles, descriptions, and footers. Built on top of glasscn-ui/card.
- **GlassmorphicPanel**: A simple container with glassmorphic styling, useful for creating sections or panels. Uses glasscn-ui/panel when available.
- **GlassmorphicModal**: A modal dialog with glassmorphic styling, with animations and accessibility features. Built on top of glasscn-ui/dialog.
- **GlassmorphicSidebar**: A navigation sidebar with glassmorphic styling, supporting collapsible behavior.
- **GlassmorphicTable**: A table component with glassmorphic styling, supporting loading states and empty states. Built on top of glasscn-ui/table.
- **GlassmorphicTabs**: A tabs component with glassmorphic styling, supporting icons and custom content. Built on top of glasscn-ui/tabs.
- **GlassmorphicTooltip**: A tooltip component with glassmorphic styling. Built on top of glasscn-ui/tooltip.
- **GlassmorphicAlert**: An alert component with glassmorphic styling, supporting different variants (info, success, warning, error).
- **GlassmorphicForm**: A form component with glassmorphic styling, including form fields, inputs, selects, and textareas.

### Dashboard Components

- **DashboardWidget**: A card-like component for displaying data on a dashboard.
- **DashboardGrid**: A grid layout for arranging dashboard widgets.
- **DashboardSection**: A section component for grouping related dashboard content.
- **DashboardLayout**: A layout component for creating a dashboard with sidebar and header.

## Usage

### Basic Example

```tsx
import { GlassmorphicCard } from '@/components/ui/GlassmorphicCard';
import { GlassmorphicPanel } from '@/components/ui/GlassmorphicPanel';
import { Button } from '@/components/ui/Button';

export function MyComponent() {
  return (
    <GlassmorphicPanel className="p-6">
      <h1 className="text-2xl font-semibold text-white mb-4">My Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassmorphicCard 
          title="Security Status" 
          description="Current security alerts and status"
        >
          <p className="text-white">All systems operational</p>
          
          <div className="mt-4 flex justify-end">
            <Button>View Details</Button>
          </div>
        </GlassmorphicCard>
        
        <GlassmorphicCard 
          title="Active Workflows" 
          description="Currently running workflows"
        >
          <p className="text-white">3 workflows active</p>
          
          <div className="mt-4 flex justify-end">
            <Button>Manage Workflows</Button>
          </div>
        </GlassmorphicCard>
      </div>
    </GlassmorphicPanel>
  );
}
```

### Dashboard Example

```tsx
import { 
  DashboardLayout, 
  DashboardSection, 
  DashboardGrid, 
  DashboardWidget 
} from '@/components/ui/GlassmorphicDashboard';
import { GlassmorphicSidebar } from '@/components/ui/GlassmorphicSidebar';

export function Dashboard() {
  // Define sidebar items
  const sidebar_items = [
    { id: 'dashboard', label: 'Dashboard', icon: <HomeIcon /> },
    { id: 'security', label: 'Security', icon: <ShieldIcon /> },
    { id: 'operations', label: 'Operations', icon: <ActivityIcon /> },
    { id: 'cognitive', label: 'Cognitive', icon: <BrainIcon /> },
    { id: 'settings', label: 'Settings', icon: <SettingsIcon /> },
  ];

  return (
    <DashboardLayout
      sidebar={
        <GlassmorphicSidebar 
          items={sidebar_items} 
          activeItemId="dashboard" 
          logo={<Logo />}
        />
      }
      header={
        <div className="p-4 border-b border-white/10 bg-background">
          <h1 className="text-xl font-semibold text-white">Dashboard</h1>
        </div>
      }
    >
      <DashboardSection title="Overview" fullWidth>
        <DashboardGrid>
          <DashboardWidget title="Security Alerts" variant="accent">
            <p className="text-2xl font-bold text-white">3</p>
            <p className="text-sm text-white/70">Active alerts</p>
          </DashboardWidget>
          
          <DashboardWidget title="Active Workflows" variant="highlight">
            <p className="text-2xl font-bold text-white">7</p>
            <p className="text-sm text-white/70">Running workflows</p>
          </DashboardWidget>
          
          <DashboardWidget title="System Status">
            <p className="text-sm text-primary-accent">All systems operational</p>
          </DashboardWidget>
        </DashboardGrid>
      </DashboardSection>
      
      <DashboardSection title="Recent Activity">
        {/* Content here */}
      </DashboardSection>
    </DashboardLayout>
  );
}
```

## Customization

All components support customization through props, particularly through the `className` prop which allows adding additional Tailwind CSS classes.

The glassmorphic effect can be customized using the `variant` and `border` props on components that support them:

- **variant**: Controls the opacity and blur level ('light', 'medium', 'heavy')
- **border**: Controls the border style ('none', 'thin', 'medium')

## Accessibility

These components are designed with accessibility in mind:

- Proper ARIA attributes
- Keyboard navigation support
- Focus management
- Color contrast considerations

When using glassmorphic effects, always ensure sufficient contrast between text and the background for readability.

## Dependencies

- React
- Tailwind CSS
- Framer Motion (for animations)
- shadcn/ui (for base components)
- glasscn-ui (for glassmorphic variants of shadcn/ui components)
- Radix UI (for primitive components)
- Lucide React (for icons)

## Notes on Glassmorphism

Glassmorphism creates a frosted glass effect that adds depth and sophistication to the UI. However, it should be used judiciously:

1. Don't overuse it on small or numerous elements
2. Ensure sufficient contrast for text and interactive elements
3. Be mindful of performance implications, especially with many blurred elements
4. Consider providing a reduced-motion option for users who may be sensitive to visual effects

## Fallback Mechanism

These components are designed to gracefully degrade if glasscn-ui is not available:

1. First, they attempt to use glasscn-ui components
2. If not available, they fall back to shadcn/ui components
3. If neither is available, they use custom implementations with similar styling

This ensures that the components will work even if the dependencies change or are not fully available.