
import { motion } from "framer-motion";
import { Shield, Users, Building2, Award } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function About() {
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
          <h1 className="text-4xl font-bold mb-8">About BitBrew Inc.</h1>
          <p className="text-[#FFFFFF]/80 text-lg mb-12">
            BitBrew Inc. is pioneering the future of enterprise intelligence with grimOS, 
            our revolutionary cognitive operating system that seamlessly integrates security, 
            operations, and strategic decision-making.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            <div className="glass p-6 rounded-xl">
              <Shield className="w-10 h-10 text-[#7ED321] mb-4" />
              <h3 className="text-xl font-semibold mb-3">Our Mission</h3>
              <p className="text-[#FFFFFF]/70">
                To empower enterprises with intelligent systems that enhance security, 
                streamline operations, and drive strategic growth.
              </p>
            </div>

            <div className="glass p-6 rounded-xl">
              <Users className="w-10 h-10 text-[#00BFFF] mb-4" />
              <h3 className="text-xl font-semibold mb-3">Our Team</h3>
              <p className="text-[#FFFFFF]/70">
                A diverse group of experts in AI, cybersecurity, and enterprise software, 
                united by our passion for innovation.
              </p>
            </div>

            <div className="glass p-6 rounded-xl">
              <Building2 className="w-10 h-10 text-[#FF1D58] mb-4" />
              <h3 className="text-xl font-semibold mb-3">Our Vision</h3>
              <p className="text-[#FFFFFF]/70">
                To create a world where enterprises operate with unprecedented intelligence, 
                security, and efficiency.
              </p>
            </div>

            <div className="glass p-6 rounded-xl">
              <Award className="w-10 h-10 text-[#7ED321] mb-4" />
              <h3 className="text-xl font-semibold mb-3">Our Values</h3>
              <p className="text-[#FFFFFF]/70">
                Innovation, integrity, and customer success drive everything we do at BitBrew Inc.
              </p>
            </div>
          </div>
        </motion.div>
      </main>

      <Footer />
    </div>
  );
}
