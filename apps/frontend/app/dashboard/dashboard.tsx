import { motion } from 'framer-motion';
import { Activity, AlertCircle, AlertTriangle, CheckCircle, Cpu, Users } from 'lucide-react';
import { DashboardSkeleton } from './dashboard-skeleton';

// Mock data types and hooks for dashboard
interface Metrics {
  total_users: number;
  active_sessions: number;
  ai_jobs_completed: number;
  system_status: 'OK' | 'WARN' | 'ERROR';
}

interface DashboardData {
  metrics: Metrics;
  charts: {
    weekly_jobs: { day: string; count: number }[];
    job_distribution: { type: string; count: number }[];
  };
  updated_at: string;
}

// Mock hook to replace the missing useDashboardData
function useDashboardData() {
  // Mock dashboard data
  const data: DashboardData = {
    metrics: {
      total_users: 1278,
      active_sessions: 564,
      ai_jobs_completed: 156842,
      system_status: 'OK'
    },
    charts: {
      weekly_jobs: [
        { day: 'Mon', count: 120 },
        { day: 'Tue', count: 230 },
        { day: 'Wed', count: 310 },
        { day: 'Thu', count: 270 },
        { day: 'Fri', count: 350 },
        { day: 'Sat', count: 190 },
        { day: 'Sun', count: 140 }
      ],
      job_distribution: [
        { type: 'Analytics', count: 42 },
        { type: 'ML Training', count: 28 },
        { type: 'Image Gen', count: 18 },
        { type: 'Text Gen', count: 35 },
        { type: 'Other', count: 12 }
      ]
    },
    updated_at: new Date().toISOString()
  };

  return {
    data,
    isLoading: false,
    error: null,
    refetch: () => console.log('Refetching data...')
  };
}

/**
 * Main dashboard component that displays metrics and charts
 */
export function GrimOSDashboard() {
  const { data, isLoading, error, refetch } = useDashboardData();

  // Function to render the appropriate system status icon
  const getStatusIcon = (status: Metrics['system_status']) => {
    switch (status) {
      case 'OK':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'WARN':
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      case 'ERROR':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <AlertCircle className="h-5 w-5 text-gray-500" />;
    }
  };

  // Function to get the appropriate class for system status
  const getStatusClass = (status: Metrics['system_status']) => {
    switch (status) {
      case 'OK':
        return 'text-green-500';
      case 'WARN':
        return 'text-yellow-500';
      case 'ERROR':
        return 'text-red-500';
      default:
        return '';
    }
  };

  // Loading state
  if (isLoading && !data) {
    return <DashboardSkeleton />;
  }

  // Error state
  if (error || !data) {
    return (
      <div className="flex flex-col items-center justify-center h-[600px] text-center">
        <AlertTriangle className="h-12 w-12 text-red-500 mb-4" />
        <h3 className="text-xl font-bold mb-2">Failed to load dashboard data</h3>
        <p className="text-muted-foreground max-w-md mb-4">
          {error?.message || 'An unknown error occurred. Please try again later.'}
        </p>
        <button
          onClick={() => refetch()}
          className="px-4 py-2 bg-[#121212] text-white border border-[#7ED321]/50 rounded-md hover:bg-[#7ED321]/10 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  // Container animation
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="space-y-6"
    >
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">
          <span className="text-white">grim</span>
          <span className="text-[#7ED321]">OS</span>
          <span className="text-white"> Dashboard</span>
        </h1>
        <button
          onClick={() => refetch()}
          className="flex items-center gap-2 px-3 py-2 text-sm bg-[#121212] text-white border border-[#7ED321]/50 rounded-md hover:bg-[#7ED321]/10 transition-colors"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="h-4 w-4 border-t-2 border-b-2 border-current rounded-full animate-spin" />
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-4 w-4"
            >
              <path d="M21 2v6h-6" />
              <path d="M3 12a9 9 0 0 1 15-6.7L21 8" />
              <path d="M3 22v-6h6" />
              <path d="M21 12a9 9 0 0 1-15 6.7L3 16" />
            </svg>
          )}
          {isLoading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>
      
      {/* Metrics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Total Users"
          value={data.metrics.total_users.toLocaleString()}
          icon={Users}
          index={0}
        />
        <MetricCard
          title="Active Sessions"
          value={data.metrics.active_sessions.toLocaleString()}
          icon={Activity}
          index={1}
        />
        <MetricCard
          title="AI Jobs Completed"
          value={data.metrics.ai_jobs_completed.toLocaleString()}
          icon={Cpu}
          index={2}
        />
        <MetricCard
          title="System Status"
          value={data.metrics.system_status}
          icon={AlertTriangle}
          valueClassName={getStatusClass(data.metrics.system_status)}
          description={data.metrics.system_status === 'OK' ? 'All systems operational' : data.metrics.system_status === 'WARN' ? 'Some systems need attention' : 'Critical issues detected'}
          index={3}
        />
      </div>
      
      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <WeeklyJobsChart data={data.charts.weekly_jobs} />
        <JobDistributionChart data={data.charts.job_distribution} />
      </div>
      
      {/* Last updated */}
      <div className="text-xs text-muted-foreground text-right flex items-center justify-end gap-1">
        <span>Last updated:</span>
        <time dateTime={data.updated_at} className="font-medium">
          {new Date(data.updated_at).toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          })}
        </time>
      </div>
    </motion.div>
  );
}