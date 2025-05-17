import { motion } from 'framer-motion';

/**
 * A cyberpunk-themed background component with animated grid and effects
 */
export function CyberpunkBackground() {
  return (
    <div className="fixed inset-0 z-0 overflow-hidden">
      {/* Grid effect */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
      
      {/* Animated gradient orbs */}
      <motion.div
        className="absolute top-1/4 -left-20 w-80 h-80 bg-[#7ED321]/10 rounded-full filter blur-3xl"
        animate={{
          x: [0, 40, 0],
          opacity: [0.3, 0.5, 0.3],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          repeatType: "reverse",
        }}
      />
      <motion.div
        className="absolute bottom-1/4 -right-20 w-96 h-96 bg-[#00BFFF]/10 rounded-full filter blur-3xl"
        animate={{
          x: [0, -30, 0],
          opacity: [0.2, 0.4, 0.2],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          repeatType: "reverse",
        }}
      />
      <motion.div
        className="absolute top-3/4 left-1/3 w-64 h-64 bg-[#FF1D58]/10 rounded-full filter blur-3xl"
        animate={{
          y: [0, 30, 0],
          opacity: [0.2, 0.3, 0.2],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          repeatType: "reverse",
        }}
      />
      
      {/* Digital scanlines */}
      <div className="absolute inset-0 bg-scanline-pattern opacity-[0.03] pointer-events-none"></div>
    </div>
  );
}
