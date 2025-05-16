
import { motion } from "framer-motion";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { useLocation } from "wouter";

export default function Features() {
  const [_, navigate] = useLocation();

  return (
    <div className="bg-gradient-to-b from-[#121212] to-[#1A1A1A] text-[#FFFFFF] min-h-screen digital-weave-bg">
      <Navbar />
      
      <main className="container mx-auto px-6 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto"
        >
          <h1 className="text-4xl font-bold mb-8">grimOS Features</h1>
          
          <div className="space-y-12">
            <section className="glass-primary p-8 rounded-xl">
              <h2 className="text-2xl font-semibold mb-6 text-[#7ED321]">Security Module</h2>
              <ul className="space-y-4 text-[#FFFFFF]/80">
                <li>• Advanced threat detection and prevention</li>
                <li>• Real-time security monitoring</li>
                <li>• AI-powered intrusion detection</li>
                <li>• Automated incident response</li>
                <li>• Zero-trust architecture implementation</li>
              </ul>
            </section>

            <section className="glass-secondary p-8 rounded-xl">
              <h2 className="text-2xl font-semibold mb-6 text-[#00BFFF]">Operations Module</h2>
              <ul className="space-y-4 text-[#FFFFFF]/80">
                <li>• Dynamic resource allocation</li>
                <li>• Workflow automation</li>
                <li>• Performance optimization</li>
                <li>• Predictive maintenance</li>
                <li>• Integrated monitoring dashboard</li>
              </ul>
            </section>

            <section className="glass-accent p-8 rounded-xl">
              <h2 className="text-2xl font-semibold mb-6 text-[#FF1D58]">Cognitive Core</h2>
              <ul className="space-y-4 text-[#FFFFFF]/80">
                <li>• AI-driven decision support</li>
                <li>• Strategic recommendations</li>
                <li>• Autonomous operations</li>
                <li>• Machine learning pipeline</li>
                <li>• Natural language processing</li>
              </ul>
            </section>
          </div>

          <div className="mt-12 text-center">
            <Button
              className="bg-[#7ED321] hover:bg-[#7ED321]/90 text-white px-8 py-6 text-lg"
              onClick={() => navigate("/sign-up")}
            >
              Start Your Free Trial
            </Button>
          </div>
        </motion.div>
      </main>

      <Footer />
    </div>
  );
}
