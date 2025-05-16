import React from 'react';

/**
 * Layout component for the dashboard section
 * 
 * This layout wraps all dashboard pages and provides consistent styling
 */
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      {children}
    </div>
  );
}