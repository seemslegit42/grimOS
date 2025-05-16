'use client';

// import N8nCanvas from '@/components/operations/RuneForge/N8nCanvas';
import { Input } from '@/components/ui/input';
// import N8nNodeProperties from '@/components/operations/RuneForge/N8nNodeProperties'; // Placeholder for properties panel
// import N8nNodeLibrary from '@/components/operations/RuneForge/N8nNodeLibrary';
import { Button } from '@/components/ui/Button';
import { DashboardLayout } from '@/components/ui/GlassmorphicDashboard';
import { GlassmorphicSidebar } from '@/components/ui/GlassmorphicSidebar';
import { useUser } from '@clerk/nextjs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useRouter } from 'next/navigation';
import { SearchIcon } from 'lucide-react';
import { PlusIcon } from '@radix-ui/react-icons';
import {
  fetchSpells, // Import fetchSpells from n8n-client
  triggerSpellExecution,
  deleteSpell,
  fetchSpellDefinition,
  createSpell,
} from '@/lib/n8n-client';
import { useEffect, useState, useCallback } from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

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
  const [spells, setSpells] = useState<any[]>([]); // State to hold list of spells (n8n workflows)
  const [workflowData, setWorkflowData] = useState<any>(null); // State to hold n8n workflow data
  const [searchTerm, setSearchTerm] = useState(''); // State for search input
  const [filteredSpells, setFilteredSpells] = useState<any[]>([]); // State for filtered spells
  // const [selectedNode, setSelectedNode] = useState<any>(null); // State to hold selected n8n node
  // const [selectedRune, setSelectedRune] = useState<any>(null);
  const [loadingSpells, setLoadingSpells] = useState(true);
  const [isDirty, setIsDirty] = useState(false);
  const [errorFetchingSpells, setErrorFetchingSpells] = useState(false);

  const { user, isLoaded, isSignedIn } = useUser();

  const router = useRouter();

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

  const loadSpells = useCallback(async () => {
    // TODO: Handle authentication/API key for n8n-client
    try {
      setLoadingSpells(true);
      setErrorFetchingSpells(false); // Reset error state
      // Call the actual fetchSpells function from n8n-client
      const fetchedSpells = await fetchSpells();
      setSpells(fetchedSpells);
      setFilteredSpells(fetchedSpells); // Initialize filtered list with all spells
    } catch (error) {
      console.error('Error fetching spells:', error);
      // Provide a more user-friendly error message
      setSpells([]); // Clear spells on error
      setFilteredSpells([]); // Clear filtered spells on error
      setErrorFetchingSpells(true);
    } finally {
      setLoadingSpells(false);
    }
  }, []);
  useEffect(() => {
    loadSpells();
  }, []); // Empty dependency array ensures this runs only once on mount
  const handleSaveWorkflow = async () => {
    // TODO: Implement saving to n8n API
    console.log('Saving workflow:', workflowData);
    try {
      // Placeholder for saving workflow using n8n-client
      // const response = await createSpell(workflowData); // Assuming createSpell returns the saved workflow or a success indicator
      // if (response) { // Adjust based on actual createSpell return value
      //   alert('Workflow saved successfully!');
      //   setIsDirty(false);
      //   // Refresh spell list after saving
      //   const fetchedSpells = await fetchSpells();
      //   setSpells(fetchedSpells);
      //   setFilteredSpells(fetchedSpells);
      // } else {
      //   alert('Failed to save workflow.');
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

  // Filter spells based on search term whenever spells or search term changes
  useEffect(() => {
    if (searchTerm === '') {
      setFilteredSpells(spells);
    } else {
      setFilteredSpells(
        spells.filter(spell =>
          spell.name.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }
  }, [spells, searchTerm]);

  const handleRunSpell = async (spellId: string) => {
    // TODO: Implement input parameter handling if required by the workflow
    const inputs = {}; // Placeholder for inputs
    try {
      // TODO: Add confirmation dialog
      console.log(`Attempting to run spell: ${spellId}`);
      const executionId = await triggerSpellExecution(spellId, inputs);
      console.log('Spell execution triggered, execution ID:', executionId);
      // TODO: Display a more sophisticated notification (e.g., toast)
      alert(`Spell execution triggered! Execution ID: ${executionId}`);
      // Optionally, navigate to the history page or poll for status update
    } catch (error: any) {
      console.error('Error triggering spell execution:', error);
      // TODO: Display a more sophisticated error notification
      alert(`Failed to trigger spell execution: ${error.message || 'Unknown error'}`);
    }
  };

  const handleDuplicateSpell = async (spell: any) => {
    try {
      console.log(`Attempting to duplicate spell: ${spell.id}`);
      // Fetch the full definition of the spell
      const spellDefinition = await fetchSpellDefinition(spell.id);

      // Create a new spell with the duplicated definition
      const newSpellData = {
        ...spellDefinition,
        name: `Copy of ${spellDefinition.name}`, // Modify the name
        // n8n's create endpoint might require specific fields or a different structure
        // You might need to adjust this based on the actual n8n API for creating workflows
        // e.g., removing 'id', 'createdAt', 'updatedAt', etc.
      };

      const newSpell = await createSpell(newSpellData);
      console.log('Spell duplicated successfully:', newSpell);
      // TODO: Display success notification
      alert(`Spell duplicated: ${newSpell.name}`);
      // Refresh the list of spells
      loadSpells();
    } catch (error: any) {
      console.error('Error duplicating spell:', error);
      // TODO: Display error notification
      alert(`Failed to duplicate spell: ${error.message || 'Unknown error'}`);
    }
  };

  const handleDeleteSpell = async (spellId: string) => {
    if (window.confirm('Are you sure you want to delete this spell? This action cannot be undone.')) {
      try {
        console.log(`Attempting to delete spell: ${spellId}`);
        await deleteSpell(spellId);
        console.log('Spell deleted successfully');
        // TODO: Display success notification
        alert('Spell deleted successfully!');
        // Refresh the list of spells
        loadSpells();
      } catch (error: any) {
        console.error('Error deleting spell:', error);
        // TODO: Display error notification
        alert(`Failed to delete spell: ${error.message || 'Unknown error'}`);
      }
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
    > {/* Placeholder for n8n workflow editor. Actual integration might involve embedding n8n or using their API to render/interact with a custom canvas. */}
      <div className="flex flex-grow">
        {/* Left Panel: Spell List */}
        <div className="w-1/4 p-4 border-r border-white/10 overflow-y-auto">
          <h2 className="text-lg font-semibold text-white mb-4">Your Spells</h2>

          {/* Search Input */}
          <div className="relative mb-4">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-white/70" />
            <Input
              placeholder="Search Spells..."
              className="pl-10 bg-background/50 border-white/20 text-white placeholder:text-white/70"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* "Create New Spell" button placed above the list */}
          <div className="mb-4">
            <Button className="w-full" onClick={() => router.push('/operations/runeforge/new')}>
              <PlusIcon className="mr-2 h-4 w-4" />
              Create New Spell
            </Button>
          </div>

          {loadingSpells && (
            <div className="flex justify-center items-center py-8">
              <div className="h-8 w-8 border-4 border-t-4 border-[#7ED321] border-gray-700 rounded-full animate-spin"></div>
            </div>
          )}

          {errorFetchingSpells && (
            <p className="text-red-500 text-center">Failed to load spells. Please try again.</p>
          )}

          {!loadingSpells && !errorFetchingSpells && filteredSpells.length === 0 && (
            <p className="text-white/70 text-center">No Spells found matching your criteria. Create a new one!</p>
          )}

          {!loadingSpells && !errorFetchingSpells && filteredSpells.length > 0 && (
            <ScrollArea className="h-[calc(100vh-220px)] pr-4"> {/* Adjust height based on header/padding and new button */}
              <Table className="text-white">
                <TableHeader>
                  <TableRow className="border-white/10 hover:bg-white/10">
                    <TableHead className="text-white/70">Name</TableHead>
                    <TableHead className="text-white/70">Description</TableHead>
                    <TableHead className="text-white/70">Last Modified</TableHead>
                    <TableHead className="text-white/70">Last Status</TableHead>
                    <TableHead className="text-white/70">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredSpells.map((spell) => (
                    <TableRow key={spell.id} className="border-white/10 hover:bg-white/10 data-[state=selected]:bg-white/[.05]">
                      <TableCell className="font-medium">{spell.name}</TableCell>
                      <TableCell>{spell.description || 'No description'}</TableCell>
                      <TableCell>{spell.updatedAt ? new Date(spell.updatedAt).toLocaleString() : 'N/A'}</TableCell>
                      {/* TODO: Fetch and display Status of Last Execution - This might require a separate API call or checking execution history */}
                      <TableCell>N/A {/* Placeholder */}</TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="outline" size="sm">Actions</Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent>
                            <DropdownMenuItem onClick={() => router.push(`/operations/runeforge/edit/${spell.id}`)}>Edit</DropdownMenuItem>
                            <DropdownMenuItem onClick={() => handleRunSpell(spell.id)}>Run</DropdownMenuItem>
                            <DropdownMenuItem onClick={() => router.push(`/operations/runeforge/history/${spell.id}`)}>View History</DropdownMenuItem>
                            <DropdownMenuItem onClick={() => handleDuplicateSpell(spell)}>Duplicate</DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem onClick={() => handleDeleteSpell(spell.id)} className="text-red-500">Delete</DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </ScrollArea>
          )}
        </div>
        {/* Center Area: Workflow Canvas (Placeholder) */}
      </div>
    </DashboardLayout>
  );
}
