/**
 * Types for the grimOS dashboard data
 */

export interface Metrics {
  total_users: number;
  active_sessions: number;
  ai_jobs_completed: number;
  system_status: 'OK' | 'WARN' | 'ERROR';
}

export interface WeeklyJobData {
  date: string;
  nlp_jobs: number;
  vision_jobs: number;
  codegen_jobs: number;
}

export interface JobDistributionData {
  name: string;
  value: number;
}

export interface DashboardData {
  metrics: Metrics;
  charts: {
    weekly_jobs: WeeklyJobData[];
    job_distribution: JobDistributionData[];
  };
  updated_at: string;
}