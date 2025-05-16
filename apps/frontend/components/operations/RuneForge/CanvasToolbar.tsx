typescriptreact
import { Button } from "@/components/ui/button";
import React from "react";

export const CanvasToolbar: React.FC = () => {
  return (
    <div className="flex items-center space-x-2 p-2 border-b border-gray-700 bg-[#121212]">
      <Button variant="outline" size="sm">
        Save Spell
      </Button>
      {/* Placeholder for zoom controls */}
      <Button variant="outline" size="sm">
        Zoom In
      </Button>
      <Button variant="outline" size="sm">
        Zoom Out
      </Button>
      {/* Placeholder for other actions */}
      <Button variant="outline" size="sm">
        Run Spell
      </Button>
    </div>
  );
};