'use client';

import { Button } from '@/components/ui/Button';
import { GlassmorphicAlert } from '@/components/ui/GlassmorphicAlert';
import {
    DashboardGrid,
    DashboardLayout,
    DashboardSection,
    DashboardWidget
} from '@/components/ui/GlassmorphicDashboard';
import { GlassmorphicPanel } from '@/components/ui/GlassmorphicPanel';
import { GlassmorphicSidebar } from '@/components/ui/GlassmorphicSidebar';
import { GlassmorphicTable } from '@/components/ui/GlassmorphicTable';
import { GlassmorphicTabs } from '@/components/ui/GlassmorphicTabs';
import { useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

// Mock data for the dashboard
const security_alerts = [
  { id: 1, severity: 'High', title: 'Unusual login attempt', source: 'Auth Service', timestamp: '2025-05-15T10:23:45' },
  { id: 2, severity: 'Medium', title: 'API rate limit exceeded', source: 'API Gateway', timestamp: '2025-05-15T09:17:32' },
  { id: 3, severity: 'Low', title: 'New device connected', source: 'Device Manager', timestamp: '2025-05-15T08:05:11' },
];

const active_workflows = [
  { id: 101, name: 'Customer Onboarding', status: 'Running', progress: 75, started: '2025-05-15T07:30:00' },
  { id: 102, name: 'Data Synchronization', status: 'Running', progress: 45, started: '2025-05-15T08:15:00' },
  { id: 103, name: 'Invoice Processing', status: 'Paused', progress: 30, started: '2025-05-15T09:00:00' },
];

export default function DashboardPage() {
  const [active_tab, setActiveTab] = useState('overview');
  const { isLoaded, isSignedIn, user } = useUser();
  const router = useRouter();
  
  // Redirect if not signed in
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push('/sign-in');
    }
  }, [isLoaded, isSignedIn, router]);
  
  // Define sidebar items (normally these would use actual icons from lucide-react)
  const sidebar_items = [
    { id: 'dashboard', label: 'Dashboard', icon: <span>📊</span>, href: '/dashboard' },
    { id: 'profile', label: 'Profile', icon: <span>👤</span>, href: '/profile' },
    { id: 'security', label: 'Security', icon: <span>🛡️</span>, href: '/security' },
    { id: 'operations', label: 'Operations', icon: <span>⚙️</span>, href: '/operations' },
    { id: 'cognitive', label: 'Cognitive', icon: <span>🧠</span>, href: '/cognitive' },
    { id: 'settings', label: 'Settings', icon: <span>⚙️</span>, href: '/settings' },
  ];

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  // Get severity color
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return 'text-tertiary-accent';
      case 'medium':
        return 'text-yellow-500';
      case 'low':
        return 'text-primary-accent';
      default:
        return 'text-white';
    }
  };

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'running':
        return 'text-primary-accent';
      case 'paused':
        return 'text-yellow-500';
      case 'failed':
        return 'text-tertiary-accent';
      default:
        return 'text-white';
    }
  };

  return (
    <DashboardLayout
      sidebar={
        <GlassmorphicSidebar 
          items={sidebar_items} 
          activeItemId="dashboard" 
          logo={<div className="text-xl font-bold text-white">grimOS</div>}
        />
      }
      header={
        <GlassmorphicPanel className="p-4 border-b border-white/10">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-semibold text-white">Dashboard</h1>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm">
                <span>🔔</span>
              </Button>
              <Button variant="ghost" size="sm">
                <span>👤</span>
              </Button>
            </div>
          </div>
        </GlassmorphicPanel>
      }
    >
      <GlassmorphicAlert 
        variant="info" 
        title="Welcome to grimOS" 
        className="mb-6"
        icon={<span>ℹ️</span>}
      >
        This is a demo of the glassmorphic UI components for grimOS.
      </GlassmorphicAlert>

      <GlassmorphicTabs
        tabs={[
          {
            id: 'overview',
            label: 'Overview',
            content: (
              <>
                <DashboardSection title="System Status" fullWidth>
                  <DashboardGrid>
                    <DashboardWidget title="Security Alerts" variant="accent">
                      <p className="text-3xl font-bold text-white">{security_alerts.length}</p>
                      <p className="text-sm text-white/70">Active alerts</p>
                    </DashboardWidget>
                    
                    <DashboardWidget title="Active Workflows" variant="highlight">
                      <p className="text-3xl font-bold text-white">{active_workflows.length}</p>
                      <p className="text-sm text-white/70">Running workflows</p>
                    </DashboardWidget>
                    
                    <DashboardWidget title="System Health">
                      <p className="text-sm text-primary-accent font-medium">All systems operational</p>
                      <div className="mt-2 w-full bg-white/10 rounded-full h-2.5">
                        <div className="bg-primary-accent h-2.5 rounded-full" style={{ width: '95%' }}></div>
                      </div>
                      <p className="text-xs text-white/70 mt-1">95% uptime</p>
                    </DashboardWidget>
                  </DashboardGrid>
                </DashboardSection>
                
                <DashboardSection title="Recent Security Alerts">
                  <GlassmorphicTable
                    data={security_alerts}
                    columns={[
                      {
                        key: 'severity',
                        header: 'Severity',
                        cell: (item) => (
                          <span className={getSeverityColor(item.severity)}>
                            {item.severity}
                          </span>
                        ),
                      },
                      {
                        key: 'title',
                        header: 'Title',
                        cell: (item) => item.title,
                      },
                      {
                        key: 'source',
                        header: 'Source',
                        cell: (item) => item.source,
                      },
                      {
                        key: 'timestamp',
                        header: 'Time',
                        cell: (item) => formatDate(item.timestamp),
                      },
                      {
                        key: 'actions',
                        header: '',
                        cell: () => (
                          <Button variant="ghost" size="sm">
                            View
                          </Button>
                        ),
                      },
                    ]}
                  />
                </DashboardSection>
              </>
            ),
          },
          {
            id: 'workflows',
            label: 'Workflows',
            content: (
              <DashboardSection title="Active Workflows">
                <GlassmorphicTable
                  data={active_workflows}
                  columns={[
                    {
                      key: 'name',
                      header: 'Workflow Name',
                      cell: (item) => item.name,
                    },
                    {
                      key: 'status',
                      header: 'Status',
                      cell: (item) => (
                        <span className={getStatusColor(item.status)}>
                          {item.status}
                        </span>
                      ),
                    },
                    {
                      key: 'progress',
                      header: 'Progress',
                      cell: (item) => (
                        <div className="w-full">
                          <div className="w-full bg-white/10 rounded-full h-2">
                            <div 
                              className="bg-primary-accent h-2 rounded-full" 
                              style={{ width: `${item.progress}%` }}
                            ></div>
                          </div>
                          <p className="text-xs text-white/70 mt-1">{item.progress}%</p>
                        </div>
                      ),
                    },
                    {
                      key: 'started',
                      header: 'Started',
                      cell: (item) => formatDate(item.started),
                    },
                    {
                      key: 'actions',
                      header: '',
                      cell: (item) => (
                        <div className="flex space-x-2">
                          {item.status === 'Paused' ? (
                            <Button variant="outline" size="sm">Resume</Button>
                          ) : (
                            <Button variant="outline" size="sm">Pause</Button>
                          )}
                          <Button variant="ghost" size="sm">View</Button>
                        </div>
                      ),
                    },
                  ]}
                />
              </DashboardSection>
            ),
          },
          {
            id: 'analytics',
            label: 'Analytics',
            content: (
              <DashboardSection title="Analytics">
                <p className="text-white">Analytics content will be displayed here.</p>
              </DashboardSection>
            ),
          },
        ]}
        defaultValue={active_tab}
        onChange={setActiveTab}
        className="mb-6"
      />
    </DashboardLayout>
  );
}