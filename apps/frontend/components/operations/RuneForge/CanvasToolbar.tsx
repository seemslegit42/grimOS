import { Button } from "@/components/ui/button";
import { useRuneForgeStore } from "@/lib/store/RuneForgeStore";
import { Minimize2 as FitView, Save, ZoomIn, ZoomOut } from "lucide-react";
import React from "react";
import { ReactFlowProvider, useReactFlow } from "reactflow";

export const CanvasToolbar: React.FC = () => {
  const { zoomIn, zoomOut, fitView } = useReactFlow();
  const initiateSaveCurrentSpell = useRuneForgeStore(
    (state) => state.initiateSaveCurrentSpell
  );

  const handleSaveSpell = () => {
    initiateSaveCurrentSpell();
  };

  return (
    <div className="flex items-center space-x-2 p-2 border-b border-gray-700 bg-[#121212] text-white">
      <Button
        variant="outline"
        size="sm"
        onClick={handleSaveSpell}
        className="border-lime-500 hover:bg-lime-500/20 hover:text-lime-400 text-lime-500"
      >
        <Save className="mr-2 h-4 w-4" />
        Save Spell
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={() => zoomIn({ duration: 300 })}
        className="border-cyan-500 hover:bg-cyan-500/20 hover:text-cyan-400 text-cyan-500"
      >
        <ZoomIn className="mr-2 h-4 w-4" />
        Zoom In
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={() => zoomOut({ duration: 300 })}
        className="border-cyan-500 hover:bg-cyan-500/20 hover:text-cyan-400 text-cyan-500"
      >
        <ZoomOut className="mr-2 h-4 w-4" />
        Zoom Out
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={() => fitView({ duration: 300 })}
        className="border-purple-500 hover:bg-purple-500/20 hover:text-purple-400 text-purple-500"
      >
        <FitView className="mr-2 h-4 w-4" />
        Fit View
      </Button>
    </div>
  );
};

export const CanvasToolbarWithProvider: React.FC = () => (
  <ReactFlowProvider>
    <CanvasToolbar />
  </ReactFlowProvider>
);