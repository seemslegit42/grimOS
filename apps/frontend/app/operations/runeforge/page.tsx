'use client';

// import N8nCanvas from '@/components/operations/RuneForge/N8nCanvas';
// import N8nNodeProperties from '@/components/operations/RuneForge/N8nNodeProperties';
// import N8nNodeLibrary from '@/components/operations/RuneForge/N8nNodeLibrary';
import { Button } from '@/components/ui/Button';
import { DashboardLayout } from '@/components/ui/GlassmorphicDashboard';
import { GlassmorphicSidebar } from '@/components/ui/GlassmorphicSidebar';
import { WorkflowDefinition, Rune } from '@/types/workflow';
import { useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

// For demo purposes, we're using a mock workflow definition
const defaultWorkflow: WorkflowDefinition = {
  id: 'new-workflow',
  name: 'New Workflow',
  description: 'A new workflow created with RuneForge',
  runes: [],
  version: 1,
  created_at: new Date().toISOString(),
  // Corrected typo: 'updated_at' instead of 'updated_at:'
  updated_at: new Date().toISOString(),
  created_by: '',
};

export default function RuneForgePage() {
  const [workflowData, setWorkflowData] = useState<any>(null); // State to hold n8n workflow data
  const [selectedNode, setSelectedNode] = useState<any>(null); // State to hold selected n8n node
  const [selectedRune, setSelectedRune] = useState<any>(null);
  const [isDirty, setIsDirty] = useState(false);
  
  const { user, isLoaded, isSignedIn } = useUser();
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push('/sign-in');
    }
  }, [isLoaded, isSignedIn, router]);
  
  // Define sidebar items (normally these would use actual icons from lucide-react)
  const router = useRouter();
  const sidebar_items = [
    { id: 'dashboard', label: 'Dashboard', icon: <span>📊</span>, href: '/dashboard' },
    { id: 'security', label: 'Security', icon: <span>🛡️</span>, href: '/security' },
    { id: 'operations', label: 'Operations', icon: <span>⚙️</span>, href: '/operations' },
    { id: 'cognitive', label: 'Cognitive', icon: <span>🧠</span>, href: '/cognitive' },
    { id: 'settings', label: 'Settings', icon: <span>⚙️</span>, href: '/settings' },
  ];
  const handleSaveWorkflow = async () => {
    // TODO: Implement saving to n8n API
    console.log('Saving workflow:', workflowData);
    try {
      const response = await fetch('/api/n8n/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(workflowData),
      });
      if (response.ok) {
        alert('Workflow saved successfully!');
        setIsDirty(false);
      } else {
        alert('Failed to save workflow.');
      }
    } catch (error) {
      console.error('Error saving workflow:', error);
      alert('An error occurred while saving the workflow.');
    }
  };
  
  useEffect(() => {
    // Initialize workflowData with the default workflow on component mount
    setWorkflowData(defaultWorkflow);
  }, []); // Empty dependency array ensures this runs only once on mount


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
        <div className="p-4 border-b border-white/10 bg-background flex justify-between items-center">
          <div>
            <h1 className="text-xl font-semibold text-white">{workflowData?.name || 'RuneForge'}</h1>
            <p className="text-sm text-white/70">Workflow Designer</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => router.push('/operations')}>
              Cancel
            </Button>
            <Button onClick={handleSaveWorkflow} disabled={!workflowData || !isDirty}>
              Save Workflow
            </Button>
          </div>
        </div>
      }
    >
 {/* Placeholder for n8n workflow editor. Actual integration might involve embedding n8n or using their API to render/interact with a custom canvas. */}
 <div className="flex flex-grow">
 {/* You would integrate or embed the n8n workflow editor here */}
 </div>
    </DashboardLayout>
  );
}
