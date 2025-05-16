import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  description?: string;
  className?: string;
  valueClassName?: string;
  index?: number; // For staggered animation
}

/**
 * A card component for displaying a single metric with an icon
 */
export function MetricCard({
  title,
  value,
  icon: Icon,
  description,
  className,
  valueClassName,
  index = 0,
}: MetricCardProps) {
  // Animation variants for the card
  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.5,
        delay: index * 0.1, // Stagger the animations
      }
    }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={cardVariants}
      className="h-full"
    >
      <Card className={cn(
        "h-full backdrop-blur-md bg-black/10 dark:bg-white/10 border-white/20 dark:border-white/20 shadow-[0_8px_16px_rgba(0,0,0,0.2)] relative overflow-hidden group",
        className
      )}>
        {/* Subtle glow effect */}
        <div className="absolute -inset-[1px] bg-gradient-to-r from-transparent via-[#7ED321]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-[#7ED321]">{title}</CardTitle>
          <Icon className="h-4 w-4 text-white/70" />
        </CardHeader>
        <CardContent>
          <div className={cn("text-2xl font-bold", valueClassName)}>
            {value}
          </div>
          {description && (
            <p className="text-xs text-muted-foreground mt-1">
              {description}
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}