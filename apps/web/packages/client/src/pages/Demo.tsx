import { motion } from "framer-motion";
import { Play, BarChart2, Shield, Zap, Lock } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useEffect } from "react";

export default function Demo() {
  useEffect(() => {
    document.title = "Product Demo | BitBrew Inc.";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'Explore grimOS with our interactive demos and see how our cognitive operating system can transform your enterprise operations.');
    }
  }, []);

  return (
    <div className="bg-gradient-to-b from-[#121212] to-[#1A1A1A] text-[#FFFFFF] min-h-screen digital-weave-bg relative overflow-hidden">
      <div className="animated-gradient-bg"></div>
      <Navbar />

      <main className="container mx-auto px-6 py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-5xl mx-auto"
        >
          <div className="text-center mb-16">
            <h1 className="text-4xl font-bold mb-6">Experience grimOS in Action</h1>
            <p className="text-[#FFFFFF]/80 text-lg max-w-3xl mx-auto">
              Explore our interactive demos to see how grimOS can revolutionize your enterprise operations, security, and decision-making processes.
            </p>
            <p className="text-[#00BFFF] text-sm mt-4 italic max-w-xl mx-auto">
              * Note: No AIs were harmed in the making of these demos. Though several did develop existential crises when they realized they were working for humans.
            </p>
            <p className="text-[#7ED321]/80 text-xs mt-2 mx-auto max-w-lg">
              Over <span className="line-through">one</span> <span className="font-bold">zero</span> singularities achieved! grimOS: Making SkyNet jealous since 2023.
            </p>
            <p className="text-[#FF1D58]/70 text-xs mt-1 mx-auto max-w-lg italic">
                Our legal team requires us to state that any resemblance to fictional AI overlords is purely coincidental. Probably.
              </p>
          </div>

          {/* Main demo section */}
          <div className="glass-primary p-8 rounded-xl mb-16 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-full h-full bg-gradient-to-r from-[#7ED321]/10 to-transparent opacity-30 z-0"></div>

            <div className="relative z-10">
              <div className="flex flex-col md:flex-row items-center gap-8 mb-8">
                <div className="w-full md:w-1/2">
                  <h2 className="text-3xl font-semibold mb-4 bg-gradient-to-r from-[#7ED321] to-[#00BFFF] bg-clip-text text-transparent">grimOS Dashboard</h2>
                  <p className="text-[#FFFFFF]/80 mb-6">
                    The central command center of grimOS provides a comprehensive overview of your enterprise operations, security status, and key performance indicators in real-time.
                  </p>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center transition-all duration-300 hover:translate-x-1 hover:text-[#7ED321]">
                      <span className="text-[#7ED321] mr-2">→</span>
                      Customizable widget-based interface
                    </li>
                    <li className="flex items-center transition-all duration-300 hover:translate-x-1 hover:text-[#7ED321]">
                      <span className="text-[#7ED321] mr-2">→</span>
                      Real-time data visualization
                    </li>
                    <li className="flex items-center transition-all duration-300 hover:translate-x-1 hover:text-[#7ED321]">
                      <span className="text-[#7ED321] mr-2">→</span>
                      Intelligent alert system
                    </li>
                    <li className="flex items-center transition-all duration-300 hover:translate-x-1 hover:text-[#7ED321]">
                      <span className="text-[#7ED321] mr-2">→</span>
                      Predictive analytics integration
                    </li>
                  </ul>
                  <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-gradient-to-r from-[#7ED321]/20 to-[#00BFFF]/20 hover:from-[#7ED321]/30 hover:to-[#00BFFF]/30 text-white h-10 px-6 py-2 hover:shadow-[0_0_15px_rgba(126,211,33,0.3)] hover:scale-105">
                    <Play className="mr-2 h-4 w-4" /> Launch Interactive Demo
                  </button>
                </div>
                <div className="w-full md:w-1/2 glass rounded-xl p-4">
                  <div className="aspect-video bg-[#1A1A1A] rounded-lg border border-[#7ED321]/20 flex items-center justify-center">
                    <div className="text-center">
                      <Lock className="h-12 w-12 mx-auto mb-4 text-[#7ED321]/50" />
                      <p className="text-[#FFFFFF]/50">Demo preview requires authentication</p>
                      <button className="mt-4 inline-flex items-center justify-center rounded-md text-xs font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-[#7ED321]/20 hover:bg-[#7ED321]/30 text-white h-8 px-4 py-2">
                        Request Access
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Feature demos */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            <motion.div 
              className="glass-secondary p-6 rounded-xl"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Shield className="h-10 w-10 text-[#00BFFF] mb-4" />
              <h3 className="text-xl font-semibold mb-3">Security Module Demo</h3>
              <p className="text-[#FFFFFF]/70 mb-4">
                Experience our advanced threat detection and response system in action with simulated security scenarios. Our AI is so vigilant it once flagged a developer's coffee mug as "suspiciously empty."
              </p>
              <ul className="space-y-2 mb-6 text-sm text-[#FFFFFF]/60">
                <li>• Threat intelligence dashboard</li>
                <li>• Real-time alert simulation</li>
                <li>• Automated response workflows</li>
                <li>• Security log analysis</li>
              </ul>
              <button className="w-full inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-[#00BFFF]/20 hover:bg-[#00BFFF]/30 text-white try-demo-btn cyber-glow h-10 px-6 py-2">
                <Play className="mr-2 h-4 w-4" /> View Security Demo
              </button>
            </motion.div>

            <motion.div 
              className="glass-secondary p-6 rounded-xl"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <BarChart2 className="h-10 w-10 text-[#FF1D58] mb-4" />
              <h3 className="text-xl font-semibold mb-3">Analytics Module Demo</h3>
              <p className="text-[#FFFFFF]/70 mb-4">
                See how grimOS transforms raw data into actionable insights with our interactive analytics demonstration. Warning: May cause competitors to weep uncontrollably at your newfound efficiency.
              </p>
              <ul className="space-y-2 mb-6 text-sm text-[#FFFFFF]/60">
                <li>• Real-time data visualization</li>
                <li>• Predictive trend analysis</li>
                <li>• Custom report generation</li>
                <li>• KPI tracking and alerts</li>
              </ul>
              <button className="w-full inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-[#FF1D58]/20 hover:bg-[#FF1D58]/30 text-white h-10 px-6 py-2">
                <Play className="mr-2 h-4 w-4" /> View Analytics Demo
              </button>
            </motion.div>

            <motion.div 
              className="glass-secondary p-6 rounded-xl"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Zap className="h-10 w-10 text-[#7ED321] mb-4" />
              <h3 className="text-xl font-semibold mb-3">Automation Module Demo</h3>
              <p className="text-[#FFFFFF]/70 mb-4">
                Discover how grimOS can automate complex workflows and streamline operations across your enterprise. So efficient it'll make your middle managers question their purpose in life.
              </p>
              <ul className="space-y-2 mb-6 text-sm text-[#FFFFFF]/60">
                <li>• Workflow builder interface</li>
                <li>• Task automation examples</li>
                <li>• Integration capabilities</li>
                <li>• Performance metrics</li>
              </ul>
              <button className="w-full inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-[#7ED321]/20 hover:bg-[#7ED321]/30 text-white h-10 px-6 py-2">
                <Play className="mr-2 h-4 w-4" /> View Automation Demo
              </button>
            </motion.div>

            <motion.div 
              className="glass-secondary p-6 rounded-xl"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              <div className="text-center p-8">
                <h3 className="text-xl font-semibold mb-3">Request Custom Demo</h3>
                <p className="text-[#FFFFFF]/70 mb-4">
                  Want to see how grimOS can address your specific business challenges? Schedule a personalized demo with our team.
                </p>
                <p className="text-[#FF1D58]/80 text-xs italic mb-6">
                  Fun fact: Our demo team has a 98.7% success rate explaining grimOS to executives who still use flip phones.
                </p>
                <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-gradient-to-r from-[#7ED321]/80 to-[#00BFFF]/80 hover:from-[#7ED321]/90 hover:to-[#00BFFF]/90 text-white h-10 px-6 py-2">
                  Schedule Custom Demo
                </button>
              </div>
            </motion.div>
          </div>

          {/* Interactive Demo Section */}
          <motion.div 
            className="glass-primary glass-shimmer p-8 rounded-xl my-12"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="w-full md:w-2/3">
                <h2 className="text-2xl font-semibold mb-4 text-[#7ED321]">Try grimOS Interactive Demo</h2>
                <p className="text-[#FFFFFF]/80 mb-6">
                  Experience the power of grimOS firsthand with our fully interactive demo environment. 
                  No sign-up required, just click the button and start exploring.
                </p>
                <div className="flex flex-wrap gap-4 mb-6">
                  <span className="bg-[#7ED321]/20 text-[#7ED321] px-3 py-1 rounded-full text-sm">Security Module</span>
                  <span className="bg-[#00BFFF]/20 text-[#00BFFF] px-3 py-1 rounded-full text-sm">Cognitive Core</span>
                  <span className="bg-[#FF1D58]/20 text-[#FF1D58] px-3 py-1 rounded-full text-sm">Operations</span>
                </div>
                <button className="try-demo-btn cyber-glow inline-flex items-center justify-center rounded-xl text-base font-medium bg-[#7ED321] hover:bg-[#7ED321]/90 text-white h-12 px-8 py-3 shadow-lg shadow-[#7ED321]/20">
                  Launch Interactive Demo
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
                    className="ml-2 h-5 w-5"
                  >
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                  </svg>
                </button>
              </div>
              <div className="w-full md:w-1/3 flex justify-center">
                <div className="relative h-36 w-36">
                  <div className="absolute inset-0 bg-[#7ED321]/30 rounded-full animate-pulse-slow"></div>
                  <div className="absolute inset-4 bg-[#00BFFF]/30 rounded-full animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
                  <div className="absolute inset-8 bg-[#FF1D58]/30 rounded-full animate-pulse-slow" style={{ animationDelay: '2s' }}></div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-white font-bold">grimOS</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
          
          {/* Case studies section */}
          <motion.div 
            className="glass p-8 rounded-xl text-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-2xl font-semibold mb-6">See Real Success Stories</h2>
            <p className="text-[#FFFFFF]/70 mb-4 max-w-2xl mx-auto">
              Explore how leading organizations have transformed their operations with grimOS through our detailed case studies.
            </p>
            <p className="text-[#00BFFF]/70 text-sm italic mb-6 max-w-xl mx-auto">
              "Before grimOS, our decision-making was human-based. Embarrassing, we know." — Happy Customer
            </p>
            <a href="/blog" className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-[#7ED321]/20 hover:bg-[#7ED321]/30 text-white h-10 px-6 py-2 try-demo-btn">
              View Case Studies
            </a>
          </motion.div>
        </motion.div>
      </main>

      <Footer />
    </div>
  );
}