import { useCallback, useEffect, useState } from 'react';
import { DashboardData } from '../types';

/**
 * Custom hook to fetch dashboard data from the API
 * 
 * @returns Object containing dashboard data, loading state, error state, and a refetch function
 */
export function useDashboardData() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // In a real app, this would be an environment variable or config
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      // Add a timeout to the fetch request
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      try {
        const response = await fetch(`${apiUrl}/api/stats/demo`, {
          signal: controller.signal,
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        
        const result = await response.json();
        
        // Validate the response data structure
        if (!result.metrics || !result.charts) {
          throw new Error('Invalid data format received from API');
        }
        
        setData(result);
      } catch (fetchErr) {
        if (fetchErr.name === 'AbortError') {
          throw new Error('Request timed out. Please try again.');
        }
        throw fetchErr;
      }
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error occurred'));
      // Log the error for debugging
      console.error('Dashboard data fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    
    // Optional: Set up polling for real-time updates
    // const intervalId = setInterval(fetchData, 30000);
    // return () => clearInterval(intervalId);
  }, [fetchData]);

  return { 
    data, 
    isLoading, 
    error,
    refetch: fetchData 
  };
}