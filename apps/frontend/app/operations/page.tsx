'use client';

import { Button } from '@/components/ui/Button';
import {
    DashboardLayout,
    DashboardSection,
} from '@/components/ui/GlassmorphicDashboard';
import { GlassmorphicSidebar } from '@/components/ui/GlassmorphicSidebar';
import { GlassmorphicTable } from '@/components/ui/GlassmorphicTable';
import { GlassmorphicTabs } from '@/components/ui/GlassmorphicTabs';
import { useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

// Mock data for the operations workflows
const workflows = [
  { id: 101, name: 'Customer Onboarding', status: 'Active', version: '1.2', lastModified: '2025-05-10T07:30:00' },
  { id: 102, name: 'Data Synchronization', status: 'Active', version: '2.0', lastModified: '2025-05-12T14:15:00' },
  { id: 103, name: 'Invoice Processing', status: 'Draft', version: '0.5', lastModified: '2025-05-14T09:00:00' },
  { id: 104, name: 'Support Ticket Workflow', status: 'Active', version: '1.0', lastModified: '2025-05-13T11:45:00' },
];

// Mock data for the workflow instances
const workflow_instances = [
  { id: 201, definitionId: 101, name: 'Onboarding - Acme Corp', status: 'Running', progress: 75, started: '2025-05-15T07:30:00' },
  { id: 202, definitionId: 102, name: 'Data Sync - Daily Run', status: 'Running', progress: 45, started: '2025-05-15T08:15:00' },
  { id: 203, definitionId: 103, name: 'Invoice #INV-2025-042', status: 'Paused', progress: 30, started: '2025-05-15T09:00:00' },
  { id: 204, definitionId: 104, name: 'Ticket #5782 Processing', status: 'Completed', progress: 100, started: '2025-05-15T06:20:00' },
];

export default function OperationsPage() {
  const [active_tab, setActiveTab] = useState('workflows');
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
    { id: 'security', label: 'Security', icon: <span>🛡️</span>, href: '/security' },
    { id: 'operations', label: 'Operations', icon: <span>⚙️</span>, href: '/operations' },
    { id: 'cognitive', label: 'Cognitive', icon: <span>🧠</span>, href: '/cognitive' },
    { id: 'settings', label: 'Settings', icon: <span>⚙️</span>, href: '/settings' },
  ];
  
  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };
  
  // Get color class based on status
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
      case 'running':
        return 'text-primary-accent';
      case 'draft':
      case 'paused':
        return 'text-secondary-accent';
      case 'completed':
        return 'text-white';
      default:
        return 'text-white';
    }
  };
  
  if (!isLoaded || !isSignedIn) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }
  
  return (
    <DashboardLayout
      sidebar={
        <GlassmorphicSidebar
          items={sidebar_items}
          activeItemId="operations"
          userName={user?.fullName || 'User'}
          userEmail={user?.primaryEmailAddress?.emailAddress || 'email@example.com'}
        />
      }
      header={
        <div className="p-4 border-b border-white/10 bg-background">
          <h1 className="text-xl font-semibold text-white">Operations Module</h1>
        </div>
      }
    >
      <GlassmorphicTabs
        tabs={[
          {
            id: 'workflows',
            label: 'Workflow Definitions',
            content: (
              <DashboardSection title="Workflow Definitions">
                <div className="flex justify-end mb-4">
                  <Button onClick={() => router.push('/operations/runeforge')}>
                    Create New Workflow
                  </Button>
                </div>
                <GlassmorphicTable
                  data={workflows}
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
                      key: 'version',
                      header: 'Version',
                      cell: (item) => item.version,
                    },
                    {
                      key: 'lastModified',
                      header: 'Last Modified',
                      cell: (item) => formatDate(item.lastModified),
                    },
                    {
                      key: 'actions',
                      header: '',
                      cell: (item) => (
                        <div className="flex gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => router.push(`/operations/runeforge/${item.id}`)}
                          >
                            Edit
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => window.alert(`Starting workflow ${item.name}`)}
                          >
                            Run
                          </Button>
                        </div>
                      ),
                    },
                  ]}
                />
              </DashboardSection>
            ),
          },
          {
            id: 'instances',
            label: 'Workflow Instances',
            content: (
              <DashboardSection title="Workflow Instances">
                <GlassmorphicTable
                  data={workflow_instances}
                  columns={[
                    {
                      key: 'name',
                      header: 'Instance Name',
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
                        <div className="flex gap-2">
                          <Button variant="ghost" size="sm">
                            View
                          </Button>
                          {item.status.toLowerCase() === 'paused' && (
                            <Button variant="ghost" size="sm">
                              Resume
                            </Button>
                          )}
                          {item.status.toLowerCase() === 'running' && (
                            <Button variant="ghost" size="sm">
                              Pause
                            </Button>
                          )}
                        </div>
                      ),
                    },
                  ]}
                />
              </DashboardSection>
            ),
          },
        ]}
        activeTab={active_tab}
        onTabChange={setActiveTab}
      />
    </DashboardLayout>
  );
}
