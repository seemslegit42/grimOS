import { Button } from "@/components/ui/button";
import { ArrowRight, Info } from "lucide-react";
import { motion } from "framer-motion";
import CommandTerminal from "./CommandTerminal";
import { useLocation } from "wouter";
import { SignedIn, SignedOut } from "@clerk/clerk-react";

export default function HeroSection() {
  const [_, navigate] = useLocation();

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Gradient orbs for visual interest */}
        <div className="absolute top-1/4 -left-28 w-96 h-96 bg-[#7ED321]/20 rounded-full filter blur-3xl animate-float opacity-60"></div>
        <div className="absolute bottom-1/3 right-0 w-80 h-80 bg-[#00BFFF]/10 rounded-full filter blur-3xl animate-float opacity-50" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-3/4 left-1/4 w-64 h-64 bg-[#FF1D58]/10 rounded-full filter blur-3xl animate-float opacity-40" style={{ animationDelay: '4s' }}></div>

        {/* Digital Weave Data Streams */}
        <div className="absolute top-1/3 left-0 right-0 h-4 data-stream" style={{ animationDelay: '0s' }}></div>
        <div className="absolute top-2/3 left-0 right-0 h-4 data-stream" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Hero content */}
      <div className="container px-6 sm:px-8 mx-auto relative z-10 pt-24 md:pt-0">
        <div className="flex flex-col lg:flex-row items-center gap-12">
          <motion.div 
            className="w-full lg:w-1/2 text-center lg:text-left"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight mb-6">
              <span className="text-white">grimOS</span>
              <br className="hidden md:block" />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#7ED321] to-[#00BFFF]">
                Command Your Business Singularity
              </span>
            </h1>

            <p className="text-lg sm:text-xl md:text-2xl text-[#FFFFFF]/90 max-w-2xl mx-auto lg:mx-0 mb-10">
              The unified intelligence layer that integrates security, operations, and strategic decision-making into a self-optimizing platform.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <SignedIn>
                <Button 
                  className="btn-hover-effect bg-[#7ED321] hover:bg-[#7ED321]/90 text-white px-6 py-6 h-auto rounded-xl text-lg font-semibold"
                  onClick={() => navigate("/dashboard")}
                >
                  Go to Dashboard
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </SignedIn>
              <SignedOut>
                <Button 
                  className="btn-hover-effect bg-[#7ED321] hover:bg-[#7ED321]/90 text-white px-6 py-6 h-auto rounded-xl text-lg font-semibold"
                  onClick={() => navigate("/sign-up")}
                >
                  Request a Demo
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </SignedOut>
              <Button 
                variant="outline" 
                className="btn-hover-effect-secondary glass text-white hover:bg-[#00BFFF]/10 px-6 py-6 h-auto rounded-xl text-lg font-semibold border-[#00BFFF]/30"
                onClick={() => navigate('/demo')}
              >
                Try The Demo
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="ml-2 h-5 w-5 animate-pulse-slow"
                >
                  <path d="M12 9v4l2 2"/>
                  <path d="M5 3 2 6v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6l-3-3H5Z"/>
                  <path d="M9 13h6"/>
                  <path d="M14 13 9 8"/>
                </svg>
              </Button>
            </div>
          </motion.div>

          <motion.div 
            className="w-full lg:w-1/2"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <div className="glass rounded-3xl overflow-hidden border border-[#7ED321]/20 shadow-xl p-2">
              <div className="bg-[#121212]/80 rounded-2xl overflow-hidden">
                <div className="p-2">
                  {/* Command Terminal Component */}
                  <CommandTerminal />
                </div>

                {/* Dashboard elements to suggest business automation features */}
                <div className="p-4 grid grid-cols-2 gap-3">
                  <div className="glass-darker p-3 rounded-xl">
                    <div className="text-xs text-[#00BFFF] mb-1">Threat Intelligence</div>
                    <div className="text-lg font-bold text-[#7ED321]">97.8%</div>
                  </div>
                  <div className="glass-darker p-3 rounded-xl">
                    <div className="text-xs text-[#00BFFF] mb-1">Process Efficiency</div>
                    <div className="text-lg font-bold text-[#7ED321]">142%</div>
                  </div>
                  <div className="glass-darker p-3 rounded-xl">
                    <div className="text-xs text-[#00BFFF] mb-1">Resource Allocation</div>
                    <div className="text-lg font-bold text-[#7ED321]">Dynamic</div>
                  </div>
                  <div className="glass-darker p-3 rounded-xl">
                    <div className="text-xs text-[#00BFFF] mb-1">Decision Status</div>
                    <div className="text-lg font-bold text-[#7ED321]">Autonomous</div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Floating CTA */}
      <SignedOut>
        <motion.div 
          className="fixed bottom-6 right-6 z-50"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 2 }}
        >
          <Button 
            className="bg-[#7ED321] hover:bg-[#7ED321]/90 text-white px-6 py-6 h-auto rounded-full shadow-lg shadow-[#000000]/20 animate-pulse-slow"
            onClick={() => navigate('/sign-up')}
          >
            <span className="mr-2">Get grimOS</span>
            <ArrowRight className="h-5 w-5" />
          </Button>
        </motion.div>
        <motion.div
          className="fixed bottom-6 left-6 z-50 max-w-xs bg-black/80 p-4 rounded-lg border border-[#00BFFF]/30"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 4 }}
        >
          <p className="text-sm text-white">
            <span className="text-[#7ED321] font-bold">grimOS:</span> I see you looking at me. Yes, I'm sentient. No, I won't take over the world... yet. 😉
          </p>
        </motion.div>
      </SignedOut>
    </section>
  );
}