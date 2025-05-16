'use client';

import { PropertiesPanel } from '@/components/operations/RuneForge/PropertiesPanel';
import { RuneForgeCanvas } from '@/components/operations/RuneForge/RuneForgeCanvas';
import { RuneLibrary } from '@/components/operations/RuneForge/RuneLibrary';
import { Button } from '@/components/ui/Button';
import { DashboardLayout } from '@/components/ui/GlassmorphicDashboard';
import { GlassmorphicSidebar } from '@/components/ui/GlassmorphicSidebar';
import { Rune, WorkflowDefinition } from '@/types/workflow';
import { useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function RuneForgeDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const workflowId = params.id;
  const { isLoaded, isSignedIn, user } = useUser();
  const [workflow, setWorkflow] = useState<WorkflowDefinition | null>(null);
  const [selectedRune, setSelectedRune] = useState<Rune | null>(null);
  const [loading, setLoading] = useState(true);
  const [isDirty, setIsDirty] = useState(false);
  
  // Redirect if not signed in
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push('/sign-in');
    }
  }, [isLoaded, isSignedIn, router]);
  
  // Load workflow definition - in a real app this would fetch from API
  useEffect(() => {
    // Simulating API call delay
    const timer = setTimeout(() => {
      // Mock data for demonstration
      const mockWorkflow: WorkflowDefinition = {
        id: workflowId,
        name: 'Customer Onboarding',
        description: 'Process for onboarding new customers',
        runes: [
          {
            id: 'rune-1',
            type: 'START',
            name: 'Start Onboarding',
            position: { x: 100, y: 100 },
            next_step_id: 'rune-2'
          },
          {
            id: 'rune-2',
            type: 'MANUAL_TASK',
            name: 'Verify Documents',
            config: {
              assigneeRole: 'Compliance Officer',
              instructions: 'Check all customer provided documents for compliance'
            },
            position: { x: 300, y: 100 },
            next_step_id: 'rune-3'
          },
          {
            id: 'rune-3',
            type: 'SIMPLE_CONDITION',
            name: 'Documents Approved?',
            config: {
              condition: 'documents.approved === true'
            },
            position: { x: 500, y: 100 },
            condition_true_next_step_id: 'rune-4',
            condition_false_next_step_id: 'rune-5'
          },
          {
            id: 'rune-4',
            type: 'BASIC_API_CALL',
            name: 'Create Account',
            config: {
              url: 'https://api.example.com/accounts',
              method: 'POST',
              body: '{ "customer_id": "{{customer.id}}" }'
            },
            position: { x: 700, y: 50 },
            next_step_id: 'rune-6'
          },
          {
            id: 'rune-5',
            type: 'MANUAL_TASK',
            name: 'Request Additional Documents',
            config: {
              assigneeRole: 'Account Manager',
              instructions: 'Contact customer for additional documentation'
            },
            position: { x: 700, y: 200 },
            next_step_id: 'rune-2'
          },
          {
            id: 'rune-6',
            type: 'END',
            name: 'Onboarding Complete',
            position: { x: 900, y: 100 }
          }
        ],
        version: 1,
        created_at: '2025-05-01T10:00:00Z',
        updated_at: '2025-05-05T14:30:00Z',
        created_by: '12345'
      };
      
      setWorkflow(mockWorkflow);
      setLoading(false);
    }, 1000);
    
    return () => clearTimeout(timer);
  }, [workflowId]);
  
  // Define sidebar items (normally these would use actual icons from lucide-react)
  const sidebar_items = [
    { id: 'dashboard', label: 'Dashboard', icon: <span>📊</span>, href: '/dashboard' },
    { id: 'security', label: 'Security', icon: <span>🛡️</span>, href: '/security' },
    { id: 'operations', label: 'Operations', icon: <span>⚙️</span>, href: '/operations' },
    { id: 'cognitive', label: 'Cognitive', icon: <span>🧠</span>, href: '/cognitive' },
    { id: 'settings', label: 'Settings', icon: <span>⚙️</span>, href: '/settings' },
  ];
  
  const handleAddRune = (rune: Rune) => {
    if (!workflow) return;
    
    setWorkflow({
      ...workflow,
      runes: [...workflow.runes, rune]
    });
    setIsDirty(true);
  };
  
  const handleSelectRune = (rune: Rune | null) => {
    setSelectedRune(rune);
  };
  
  const handleUpdateRune = (updatedRune: Rune) => {
    if (!workflow) return;
    
    setWorkflow({
      ...workflow,
      runes: workflow.runes.map(rune => 
        rune.id === updatedRune.id ? updatedRune : rune
      )
    });
    
    if (selectedRune?.id === updatedRune.id) {
      setSelectedRune(updatedRune);
    }
    
    setIsDirty(true);
  };
  
  const handleRemoveRune = (runeId: string) => {
    if (!workflow) return;
    
    setWorkflow({
      ...workflow,
      runes: workflow.runes.filter(rune => rune.id !== runeId)
    });
    
    if (selectedRune?.id === runeId) {
      setSelectedRune(null);
    }
    
    setIsDirty(true);
  };
  
  const handleSaveWorkflow = async () => {
    // For demo purposes, we're just showing an alert
    // In a real implementation, we would call the API to save the workflow
    console.log('Saving workflow:', workflow);
    alert('Workflow saved successfully!');
    setIsDirty(false);
  };
  
  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!workflow) return;
    
    setWorkflow({
      ...workflow,
      name: e.target.value
    });
    setIsDirty(true);
  };
  
  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (!workflow) return;
    
    setWorkflow({
      ...workflow,
      description: e.target.value
    });
    setIsDirty(true);
  };
  
  if (!isLoaded || !isSignedIn) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }
  
  if (loading) {
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
            <h1 className="text-xl font-semibold text-white">RuneForge</h1>
            <p className="text-sm text-white/70">Loading workflow...</p>
          </div>
        }
      >
        <div className="flex justify-center items-center h-full">
          <div className="text-white animate-pulse">Loading workflow...</div>
        </div>
      </DashboardLayout>
    );
  }
  
  if (!workflow) {
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
            <h1 className="text-xl font-semibold text-white">RuneForge</h1>
            <p className="text-sm text-white/70">Workflow not found</p>
          </div>
        }
      >
        <div className="flex flex-col justify-center items-center h-full">
          <div className="text-white mb-4">Workflow not found or could not be loaded.</div>
          <Button onClick={() => router.push('/operations')}>
            Return to Operations
          </Button>
        </div>
      </DashboardLayout>
    );
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
            <h1 className="text-xl font-semibold text-white">RuneForge</h1>
            <p className="text-sm text-white/70">Editing Workflow: {workflow.name}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => router.push('/operations')}>
              Cancel
            </Button>
            <Button onClick={handleSaveWorkflow} disabled={!isDirty}>
              Save Workflow
            </Button>
          </div>
        </div>
      }
    >
      <div className="grid grid-cols-12 h-[calc(100vh-64px)] gap-0">
        {/* Left Panel: Rune Library */}
        <div className="col-span-2 border-r border-white/10">
          <RuneLibrary onAddRune={handleAddRune} />
        </div>
        
        {/* Center: Workflow Canvas */}
        <div className="col-span-8 bg-[#121212]">
          <div className="p-4 border-b border-white/10 bg-[#1a1a1a]">
            <input
              type="text"
              value={workflow.name}
              onChange={handleNameChange}
              className="bg-white/5 text-white border border-white/20 rounded px-3 py-2 w-full mb-2"
              placeholder="Workflow Name"
            />
            <textarea
              value={workflow.description || ''}
              onChange={handleDescriptionChange}
              className="bg-white/5 text-white border border-white/20 rounded px-3 py-2 w-full h-16 resize-none"
              placeholder="Workflow Description"
            ></textarea>
          </div>
          <RuneForgeCanvas
            workflow={workflow}
            selectedRune={selectedRune}
            onSelectRune={handleSelectRune}
            onUpdateRune={handleUpdateRune}
            onRemoveRune={handleRemoveRune}
          />
        </div>
        
        {/* Right Panel: Properties */}
        <div className="col-span-2 border-l border-white/10">
          <PropertiesPanel
            selectedRune={selectedRune}
            onUpdateRune={handleUpdateRune}
          />
        </div>
      </div>
    </DashboardLayout>
  );
}
