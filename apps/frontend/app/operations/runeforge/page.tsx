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

// For demo purposes, we're using a mock workflow definition
const defaultWorkflow: WorkflowDefinition = {
  id: '',
  name: 'New Workflow',
  description: 'A new workflow created with RuneForge',
  runes: [],
  version: 1,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  created_by: '',
};

export default function RuneForgePage() {
  const router = useRouter();
  const { isLoaded, isSignedIn, user } = useUser();
  const [workflowDefinition, setWorkflowDefinition] = useState<WorkflowDefinition>(defaultWorkflow);
  const [selectedRune, setSelectedRune] = useState<Rune | null>(null);
  const [isDirty, setIsDirty] = useState(false);
  
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
  
  const handleAddRune = (rune: Rune) => {
    const newRune = { ...rune, id: `rune-${Date.now()}` };
    setWorkflowDefinition(prev => ({
      ...prev,
      runes: [...prev.runes, newRune]
    }));
    setIsDirty(true);
  };
  
  const handleSelectRune = (rune: Rune | null) => {
    setSelectedRune(rune);
  };
  
  const handleUpdateRune = (updatedRune: Rune) => {
    setWorkflowDefinition(prev => ({
      ...prev,
      runes: prev.runes.map(rune => 
        rune.id === updatedRune.id ? updatedRune : rune
      )
    }));
    setSelectedRune(updatedRune);
    setIsDirty(true);
  };
  
  const handleRemoveRune = (runeId: string) => {
    setWorkflowDefinition(prev => ({
      ...prev,
      runes: prev.runes.filter(rune => rune.id !== runeId)
    }));
    if (selectedRune?.id === runeId) {
      setSelectedRune(null);
    }
    setIsDirty(true);
  };
  
  const handleSaveWorkflow = async () => {
    // For demo purposes, we're just showing an alert
    // In a real implementation, we would call the API to save the workflow
    console.log('Saving workflow:', workflowDefinition);
    alert('Workflow saved successfully!');
    setIsDirty(false);
  };
  
  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWorkflowDefinition(prev => ({
      ...prev,
      name: e.target.value
    }));
    setIsDirty(true);
  };
  
  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setWorkflowDefinition(prev => ({
      ...prev,
      description: e.target.value
    }));
    setIsDirty(true);
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
        <div className="p-4 border-b border-white/10 bg-background flex justify-between items-center">
          <div>
            <h1 className="text-xl font-semibold text-white">RuneForge</h1>
            <p className="text-sm text-white/70">Workflow Designer</p>
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
              value={workflowDefinition.name}
              onChange={handleNameChange}
              className="bg-white/5 text-white border border-white/20 rounded px-3 py-2 w-full mb-2"
              placeholder="Workflow Name"
            />
            <textarea
              value={workflowDefinition.description}
              onChange={handleDescriptionChange}
              className="bg-white/5 text-white border border-white/20 rounded px-3 py-2 w-full h-16 resize-none"
              placeholder="Workflow Description"
            ></textarea>
          </div>
          <RuneForgeCanvas
            workflow={workflowDefinition}
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
