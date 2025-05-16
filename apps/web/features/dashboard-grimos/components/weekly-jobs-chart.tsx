import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { WeeklyJobData } from '../types';

interface WeeklyJobsChartProps {
  data: WeeklyJobData[];
}

/**
 * Line chart component showing AI jobs over time (weekly)
 */
export function WeeklyJobsChart({ data }: WeeklyJobsChartProps) {
  // Format dates for better display
  const formattedData = data.map(item => ({
    ...item,
    date: new Date(item.date).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    })
  }));

  // Animation variants
  const chartVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.6,
        delay: 0.3,
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
        <div className="absolute -inset-[1px] bg-gradient-to-r from-transparent via-[#00BFFF]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
        <CardHeader>
          <CardTitle className="text-lg text-[#7ED321]">Weekly AI Jobs</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={formattedData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis 
                  dataKey="date" 
                  stroke="currentColor" 
                  fontSize={12} 
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis 
                  stroke="currentColor" 
                  fontSize={12} 
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(0, 0, 0, 0.8)', 
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }} 
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="nlp_jobs"
                  name="NLP"
                  stroke="#7ED321"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="vision_jobs"
                  name="Vision"
                  stroke="#00BFFF"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="codegen_jobs"
                  name="Codegen"
                  stroke="#FF1D58"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}