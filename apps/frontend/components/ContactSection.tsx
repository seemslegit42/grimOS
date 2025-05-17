import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { motion } from "framer-motion";
import {
    Github,
    Linkedin,
    Mail,
    MapPin,
    Phone,
    Send,
    Shield,
    Twitter
} from "lucide-react";

export default function ContactSection() {
  return (
    <section id="contact" className="py-20 relative overflow-hidden">
      <div className="container mx-auto px-6 sm:px-8 relative z-10">
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Enterprise Inquiries</h2>
          <p className="text-lg text-[#FFFFFF]/80 max-w-2xl mx-auto">
            Our team of specialists is ready to guide you through the grimOS implementation journey and 
            customize solutions for your unique enterprise challenges.
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="glass-primary rounded-xl p-6 h-full">
              <h3 className="text-xl font-semibold mb-6 flex items-center">
                <Shield className="mr-2 h-5 w-5 text-[#7ED321]" />
                Contact Information
              </h3>
              
              <div className="space-y-6">
                <div className="flex items-start">
                  <div className="text-[#7ED321] mr-4">
                    <MapPin className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-medium mb-1">Headquarters</h4>
                    <p className="text-[#FFFFFF]/70">1 Quantum Tower, Innovation District, San Francisco, CA 94107</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="text-[#7ED321] mr-4">
                    <Mail className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-medium mb-1">Enterprise Contact</h4>
                    <p className="text-[#FFFFFF]/70">enterprise@grimoire.com</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="text-[#7ED321] mr-4">
                    <Phone className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-medium mb-1">Secure Line</h4>
                    <p className="text-[#FFFFFF]/70">+1 (888) GRIM-OS1</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-10 pt-6 border-t border-[#7ED321]/20">
                <h4 className="font-medium mb-4 text-[#7ED321]">Stay Connected</h4>
                <div className="flex space-x-4">
                  <a href="#" className="glass-primary w-10 h-10 rounded-full flex items-center justify-center hover:bg-[#7ED321]/20 transition-colors duration-300">
                    <Twitter className="h-5 w-5 text-[#7ED321]" />
                  </a>
                  <a href="#" className="glass-primary w-10 h-10 rounded-full flex items-center justify-center hover:bg-[#7ED321]/20 transition-colors duration-300">
                    <Linkedin className="h-5 w-5 text-[#7ED321]" />
                  </a>
                  <a href="#" className="glass-primary w-10 h-10 rounded-full flex items-center justify-center hover:bg-[#7ED321]/20 transition-colors duration-300">
                    <Github className="h-5 w-5 text-[#7ED321]" />
                  </a>
                </div>
              </div>

              <div className="mt-8 p-4 bg-[#7ED321]/10 rounded-lg border border-[#7ED321]/20">
                <div className="flex items-start">
                  <div className="text-[#7ED321] mr-3 mt-1">
                    <Shield className="h-5 w-5" />
                  </div>
                  <p className="text-[#FFFFFF]/80 text-sm">
                    All communications are secured with enterprise-grade encryption. Your data is protected under our 
                    strict security protocols and privacy policy. Even our sentient AI can't read these messages 
                    (though it's been asking nicely).
                  </p>
                </div>
              </div>
              <div className="mt-4 p-2 rounded text-center">
                <p className="text-xs text-[#FFFFFF]/50 italic">P.S. We promise grimOS won't judge your typing speed or spelling mistakes... much.</p>
              </div>
            </div>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="glass-secondary rounded-xl p-6 h-full">
              <h3 className="text-xl font-semibold mb-6 flex items-center">
                <Send className="mr-2 h-5 w-5 text-[#00BFFF]" />
                Request a Consultation
              </h3>
              
              <form onSubmit={(e) => e.preventDefault()}>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-[#FFFFFF]/70 mb-1">Full Name</label>
                    <Input 
                      type="text" 
                      id="name"
                      className="glass-darker w-full focus:ring-2 focus:ring-[#00BFFF]/50 text-white bg-[#121212]/30"
                      required
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-[#FFFFFF]/70 mb-1">Work Email</label>
                    <Input 
                      type="email" 
                      id="email"
                      className="glass-darker w-full focus:ring-2 focus:ring-[#00BFFF]/50 text-white bg-[#121212]/30"
                      required
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label htmlFor="company" className="block text-sm font-medium text-[#FFFFFF]/70 mb-1">Company</label>
                    <Input 
                      type="text" 
                      id="company"
                      className="glass-darker w-full focus:ring-2 focus:ring-[#00BFFF]/50 text-white bg-[#121212]/30"
                      required
                    />
                  </div>
                  <div>
                    <label htmlFor="position" className="block text-sm font-medium text-[#FFFFFF]/70 mb-1">Position</label>
                    <Input 
                      type="text" 
                      id="position"
                      className="glass-darker w-full focus:ring-2 focus:ring-[#00BFFF]/50 text-white bg-[#121212]/30"
                      required
                    />
                  </div>
                </div>
                
                <div className="mb-4">
                  <label htmlFor="interest" className="block text-sm font-medium text-[#FFFFFF]/70 mb-1">Area of Interest</label>
                  <select 
                    id="interest"
                    className="glass-darker w-full focus:ring-2 focus:ring-[#00BFFF]/50 text-white bg-[#121212]/30 rounded-md h-10 px-3"
                    required
                  >
                    <option value="" className="bg-[#121212]">Select an option</option>
                    <option value="security" className="bg-[#121212]">Security Module</option>
                    <option value="operations" className="bg-[#121212]">Operations Module</option>
                    <option value="cognitive" className="bg-[#121212]">Cognitive Core</option>
                    <option value="api" className="bg-[#121212]">Universal API Fabric</option>
                    <option value="full" className="bg-[#121212]">Full grimOS Implementation</option>
                  </select>
                </div>
                
                <div className="mb-6">
                  <label htmlFor="message" className="block text-sm font-medium text-[#FFFFFF]/70 mb-1">Message</label>
                  <Textarea 
                    id="message"
                    rows={4}
                    placeholder="Tell us about your specific needs or challenges"
                    className="glass-darker w-full focus:ring-2 focus:ring-[#00BFFF]/50 text-white bg-[#121212]/30"
                    required
                  />
                </div>
                
                <Button 
                  type="submit" 
                  className="btn-hover-effect-secondary bg-[#00BFFF] hover:bg-[#00BFFF]/90 text-white px-6 py-3 h-auto rounded-xl text-lg font-semibold"
                >
                  Submit Request
                </Button>
              </form>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Background accents */}
      <div className="absolute top-1/4 right-0 w-64 h-64 bg-[#00BFFF]/5 rounded-full filter blur-3xl"></div>
      <div className="absolute bottom-1/4 left-0 w-72 h-72 bg-[#7ED321]/5 rounded-full filter blur-3xl"></div>
    </section>
  );
}
