import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck } from "lucide-react";

export default function CTASection() {
  return (
    <section id="get-started" className="py-20 relative overflow-hidden mobile-py">
      <div className="container mx-auto px-6 sm:px-8 relative z-10 max-w-5xl mobile-px">
        <motion.div 
          className="glass digital-weave-bg rounded-2xl p-8 md:p-12 overflow-hidden relative"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          {/* Background accents inside the CTA */}
          <div className="absolute -top-20 -right-20 w-64 h-64 bg-[#7ED321]/20 rounded-full filter blur-3xl"></div>
          <div className="absolute -bottom-20 -left-20 w-64 h-64 bg-[#00BFFF]/10 rounded-full filter blur-3xl"></div>
          
          <div className="relative text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Stay Ahead of the Singularity</h2>
            <p className="text-lg text-[#FFFFFF]/80 max-w-3xl mx-auto mb-8">
              Transform your enterprise with grimOS, the unified intelligence layer that's reshaping 
              how forward-thinking organizations approach security, operations, and decision-making.
            </p>
            
            <div className="grid md:grid-cols-2 gap-8 mb-12 mobile-stack">
              <div className="glass-primary rounded-xl p-6 text-left">
                <div className="flex items-center mb-4">
                  <ShieldCheck className="text-[#7ED321] mr-3 h-6 w-6" />
                  <h3 className="text-xl font-semibold">Request Enterprise Access</h3>
                </div>
                <p className="text-[#FFFFFF]/70 mb-6">
                  Get personalized insights into how grimOS can transform your specific industry and use cases with a 
                  guided technical demo.
                </p>
                <Button 
                  asChild
                  className="btn-hover-effect bg-[#7ED321] hover:bg-[#7ED321]/90 text-white px-6 py-3 h-auto rounded-xl text-base font-semibold w-full"
                >
                  <a href="#contact">
                    Schedule a Demo
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </a>
                </Button>
              </div>

              <div className="glass-secondary rounded-xl p-6 text-left">
                <div className="flex items-center mb-4">
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
                    className="text-[#00BFFF] mr-3 h-6 w-6"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <path d="M12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12Z" />
                    <circle cx="12" cy="12" r="2" />
                  </svg>
                  <h3 className="text-xl font-semibold">Join the Grimoire Waitlist</h3>
                </div>
                <p className="text-[#FFFFFF]/70 mb-6">
                  Be among the first to access our exclusive early adopter program and shape the future of grimOS development. Warning: May cause your competitors to weep uncontrollably. (We're still working on that bug... or is it a feature? 🤔)
                </p>
                <form className="flex flex-col sm:flex-row gap-4" onSubmit={(e) => e.preventDefault()}>
                  <input 
                    type="email" 
                    placeholder="Enterprise email" 
                    className="glass-darker flex-grow px-4 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#00BFFF]/50 text-white placeholder-[#FFFFFF]/40 bg-[#121212]/30"
                    required
                  />
                  <Button 
                    type="submit" 
                    className="btn-hover-effect-secondary bg-[#00BFFF] hover:bg-[#00BFFF]/90 text-white px-6 py-3 h-auto rounded-xl text-base font-semibold whitespace-nowrap"
                  >
                    Join Waitlist
                  </Button>
                </form>
              </div>
            </div>
            
            <p className="text-[#FFFFFF]/60 text-sm">
              By submitting your information, you agree to our <a href="#" className="text-[#00BFFF] hover:underline">Privacy Policy</a> and 
              <a href="#" className="text-[#00BFFF] hover:underline"> Terms of Service</a>.
              Your data is secured with enterprise-grade encryption.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
