import { CyberpunkBackground } from '@/components/CyberpunkBackground';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { Metadata } from 'next';
import { GrimOSDashboard } from './dashboard';

export const metadata: Metadata = {
  title: 'grimOS Dashboard',
  description: 'Interactive dashboard for grimOS platform metrics and analytics',
};

/**
 * Dashboard page component for grimOS
 * 
 * This page displays an interactive dashboard with metrics and charts
 * showing key performance indicators for the grimOS platform.
 * Includes a cyberpunk-themed background to enhance the glassmorphic UI.
 */
export default function DashboardPage() {
  return (
    <>
      <CyberpunkBackground />
      <div className="container mx-auto py-6 relative z-10">
        <ErrorBoundary>
          <GrimOSDashboard />
        </ErrorBoundary>
      </div>
    </>
  );
}