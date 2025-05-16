import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';
import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { JobDistributionData } from '../types';

interface JobDistributionChartProps {
  data: JobDistributionData[];
}

/**
 * Pie chart component showing job type distribution
 */
export function JobDistributionChart({ data }: JobDistributionChartProps) {
  // Colors for the pie chart segments
  const COLORS = ['#7ED321', '#00BFFF', '#FF1D58', '#FFBE0B'];
  
  // Animation variants
  const chartVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.6,
        delay: 0.4,
      }
    }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={chartVariants}
      className="h-full"
    >
      <Card className="h-full backdrop-blur-md bg-black/10 dark:bg-white/10 border-white/20 dark:border-white/20 shadow-[0_8px_16px_rgba(0,0,0,0.2)] relative overflow-hidden group">
        {/* Subtle glow effect */}
        <div className="absolute -inset-[1px] bg-gradient-to-r from-transparent via-[#FF1D58]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
        <CardHeader>
          <CardTitle className="text-lg text-[#7ED321]">Job Type Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value) => [`${value} jobs`, 'Count']}
                  contentStyle={{ 
                    backgroundColor: 'rgba(0, 0, 0, 0.8)', 
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}