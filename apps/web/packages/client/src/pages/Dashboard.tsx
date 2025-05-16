import { UserButton, useUser } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { useLocation } from "wouter";

export default function Dashboard() {
  const { user } = useUser();
  const [_, navigate] = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#121212] to-[#1A1A1A] digital-weave-bg">
      {/* Header */}
      <header className="glass sticky top-0 z-50 px-6 py-4">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-[#7ED321] text-2xl font-bold">BitBrew</span>
            <span className="text-[#FFFFFF] font-light">Inc.</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              className="text-[#FFFFFF] hover:text-[#7ED321] hover:bg-transparent"
              onClick={() => navigate("/")}
            >
              Home
            </Button>
            <UserButton />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="glass-primary rounded-xl p-6 mb-8"
        >
          <h1 className="text-2xl font-bold mb-2">Welcome, {user?.firstName || "User"}!</h1>
          <p className="text-[#FFFFFF]/80">
            You're now logged into your grimOS dashboard. This is where you can manage your grimOS experience,
            view analytics, and customize your settings.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="glass rounded-xl p-6"
          >
            <h2 className="text-xl font-semibold mb-4 text-[#00BFFF]">Security Module</h2>
            <p className="text-[#FFFFFF]/70 mb-4">
              Your security systems are operating at optimal levels. No threats detected in the last 24 hours.
            </p>
            <div className="flex justify-end">
              <Button variant="outline" className="glass-secondary text-[#00BFFF] hover:bg-[#00BFFF]/10">
                View Details
              </Button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="glass rounded-xl p-6"
          >
            <h2 className="text-xl font-semibold mb-4 text-[#7ED321]">Operations Module</h2>
            <p className="text-[#FFFFFF]/70 mb-4">
              Workflow automation has saved 12.5 hours this week. Resource allocation is optimized at 97%.
            </p>
            <div className="flex justify-end">
              <Button variant="outline" className="glass-primary text-[#7ED321] hover:bg-[#7ED321]/10">
                View Details
              </Button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="glass rounded-xl p-6"
          >
            <h2 className="text-xl font-semibold mb-4 text-[#FF1D58]">Cognitive Core</h2>
            <p className="text-[#FFFFFF]/70 mb-4">
              3 new AI agent recommendations available. Strategic decision support ready for your review.
            </p>
            <div className="flex justify-end">
              <Button variant="outline" className="glass-accent text-[#FF1D58] hover:bg-[#FF1D58]/10">
                View Details
              </Button>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  );
}