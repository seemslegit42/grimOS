# grimOS Dashboard Feature

This feature provides an interactive dashboard for the grimOS platform, displaying key metrics and analytics.

## Components

- **GrimOSDashboard**: Main dashboard component that displays metrics and charts
- **MetricCard**: Card component for displaying individual metrics
- **WeeklyJobsChart**: Line chart showing AI jobs over time
- **JobDistributionChart**: Pie chart showing job type distribution

## Usage

```tsx
import { GrimOSDashboard } from '@/features/dashboard-grimos';

export default function DashboardPage() {
  return (
    <div className="container mx-auto py-6">
      <GrimOSDashboard />
    </div>
  );
}
```

## Data Structure

The dashboard expects data in the following format:

```typescript
interface DashboardData {
  metrics: {
    total_users: number;
    active_sessions: number;
    ai_jobs_completed: number;
    system_status: 'OK' | 'WARN' | 'ERROR';
  };
  charts: {
    weekly_jobs: Array<{
      date: string;
      nlp_jobs: number;
      vision_jobs: number;
      codegen_jobs: number;
    }>;
    job_distribution: Array<{
      name: string;
      value: number;
    }>;
  };
  updated_at: string;
}
```

## API Endpoints

The dashboard fetches data from the following endpoint:

- `/api/stats/demo`: Returns mock data for the dashboard

## Features

- Responsive layout that works on all screen sizes
- Dark mode support
- Loading and error states
- Animations using Framer Motion
- Real-time data updates (configurable polling interval)