
import { motion } from "framer-motion";
import { Github, Linkedin, Twitter, Mail } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Badge } from "@/components/ui/badge";

export default function Team() {
  useEffect(() => {
    document.title = "Our Team | BitBrew Inc.";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'Meet Bryan Marlow, the visionary founder behind BitBrew Inc. and grimOS.');
    }
  }, []);

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
          <h1 className="text-4xl font-bold mb-8">Our Team</h1>
          <p className="text-[#FFFFFF]/80 text-lg mb-12">
            Behind BitBrew Inc.'s groundbreaking grimOS is a visionary leader dedicated to 
            transforming how enterprises harness AI for strategic advantage.
          </p>

          <div className="mb-16">
            <div className="glass p-8 rounded-xl mb-12">
              <div className="flex flex-col md:flex-row gap-8">
                <div className="flex-shrink-0">
                  {/* Replace with actual image when available */}
                  <div className="w-48 h-48 bg-gradient-to-br from-[#7ED321] to-[#00BFFF] rounded-xl flex items-center justify-center text-3xl font-bold">
                    BM
                  </div>
                </div>
                <div className="flex-grow">
                  <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
                    <div>
                      <h2 className="text-2xl font-bold">Bryan Marlow</h2>
                      <p className="text-[#7ED321] font-medium">Founder & CEO</p>
                    </div>
                    <div className="flex space-x-3 mt-4 md:mt-0">
                      <a href="#" className="text-[#FFFFFF]/70 hover:text-[#FFFFFF] transition-colors">
                        <Github className="w-5 h-5" />
                      </a>
                      <a href="#" className="text-[#FFFFFF]/70 hover:text-[#FFFFFF] transition-colors">
                        <Linkedin className="w-5 h-5" />
                      </a>
                      <a href="#" className="text-[#FFFFFF]/70 hover:text-[#FFFFFF] transition-colors">
                        <Twitter className="w-5 h-5" />
                      </a>
                      <a href="#" className="text-[#FFFFFF]/70 hover:text-[#FFFFFF] transition-colors">
                        <Mail className="w-5 h-5" />
                      </a>
                    </div>
                  </div>
                  <p className="text-[#FFFFFF]/70 mb-4">
                    Bryan is the visionary founder behind BitBrew Inc. and the creator of grimOS. 
                    With a background in enterprise AI and cybersecurity, Bryan saw the opportunity to 
                    unify fragmented business intelligence systems into a single, cognitive operating 
                    layer that could transform how organizations operate.
                  </p>
                  <p className="text-[#00BFFF]/90 text-sm mb-4 italic">
                    When not revolutionizing the future of AI, Bryan can be found explaining to his smart fridge 
                    why it shouldn't try to take over his apartment. So far, it's been a peaceful negotiation.
                  </p>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary" size="lg">AI Architecture</Badge>
                    <Badge variant="secondary" size="lg">Enterprise Security</Badge>
                    <Badge variant="secondary" size="lg">Systems Design</Badge>
                    <Badge variant="secondary" size="lg">Strategic Vision</Badge>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-center">
              <h3 className="text-2xl font-semibold mb-4">Join Our Team</h3>
              <p className="text-[#FFFFFF]/70 mb-6 max-w-2xl mx-auto">
                BitBrew Inc. is expanding. We're looking for talented individuals who share our 
                passion for AI, security, and transformative enterprise solutions.
              </p>
              <a href="/careers" className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2">
                View Open Positions
              </a>
            </div>
          </div>
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}
