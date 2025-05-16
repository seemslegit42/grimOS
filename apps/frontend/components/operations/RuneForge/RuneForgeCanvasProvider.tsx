typescriptreact
import React, { createContext, useContext, ReactNode } from 'react';
import { useStore, UseStore } from 'zustand'; // Assuming zustand store will be created separately
import { ReactFlowInstance } from 'react-flow-renderer'; // Assuming react-flow-renderer for now

// Define the type for the context value
interface RuneForgeCanvasContextType {
  store: UseStore<any> | null; // Placeholder for zustand store type
  reactFlowInstance: ReactFlowInstance | null; // Placeholder for react-flow instance
}

// Create the context with a default null value
const RuneForgeCanvasContext = createContext<RuneForgeCanvasContextType | null>(null);

// Custom hook to access the context
export const useRuneForgeCanvas = () => {
  const context = useContext(RuneForgeCanvasContext);
  if (context === null) {
    throw new Error('useRuneForgeCanvas must be used within a RuneForgeCanvasProvider');
  }
  return context;
};

// RuneForgeCanvasProvider component
interface RuneForgeCanvasProviderProps {
  children: ReactNode;
  // Add props for initial state or store if needed later
}

export const RuneForgeCanvasProvider: React.FC<RuneForgeCanvasProviderProps> = ({ children }) => {
  // Placeholder state and instance for now
  const placeholderStore = useStore(() => ({})); // Replace with actual store hook later
  const placeholderReactFlowInstance: ReactFlowInstance | null = null; // Replace with actual instance later

  const contextValue: RuneForgeCanvasContextType = {
    store: placeholderStore,
    reactFlowInstance: placeholderReactFlowInstance,
  };

  return (
    <RuneForgeCanvasContext.Provider value={contextValue}>
      {children}
    </RuneForgeCanvasContext.Provider>
  );
};