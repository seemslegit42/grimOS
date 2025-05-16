import { Card, CardContent, CardHeader } from '@/components/ui/card';

/**
 * Skeleton loading component for the dashboard
 */
export function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div className="h-9 w-64 bg-muted/30 rounded-md animate-pulse" />
      
      {/* Metrics Cards Skeleton */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="h-[120px] backdrop-blur-md bg-black/10 dark:bg-white/10 border-white/20 dark:border-white/20 shadow-[0_8px_16px_rgba(0,0,0,0.2)] relative overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <div className="h-4 w-24 bg-muted/30 rounded-md animate-pulse" />
              <div className="h-4 w-4 rounded-full bg-muted/30 animate-pulse" />
            </CardHeader>
            <CardContent>
              <div className="h-8 w-20 bg-muted/30 rounded-md animate-pulse" />
            </CardContent>
          </Card>
        ))}
      </div>
      
      {/* Charts Skeleton */}
      <div className="grid gap-4 md:grid-cols-2">
        {[...Array(2)].map((_, i) => (
          <Card key={i} className="h-[350px] backdrop-blur-md bg-black/10 dark:bg-white/10 border-white/20 dark:border-white/20 shadow-[0_8px_16px_rgba(0,0,0,0.2)] relative overflow-hidden">
            <CardHeader>
              <div className="h-6 w-32 bg-muted/30 rounded-md animate-pulse" />
            </CardHeader>
            <CardContent>
              <div className="h-[280px] w-full bg-muted/20 rounded-md animate-pulse flex items-center justify-center">
                <svg
                  className="w-10 h-10 text-muted/30"
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <line x1="3" y1="9" x2="21" y2="9" />
                  <line x1="9" y1="21" x2="9" y2="9" />
                </svg>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      
      {/* Last updated Skeleton */}
      <div className="flex justify-end">
        <div className="h-4 w-40 bg-muted/30 rounded-md animate-pulse" />
      </div>
    </div>
  );
}