import { motion } from "framer-motion";
import {
    FileCode,
    Github,
    Linkedin,
    Lock,
    Shield,
    Terminal,
    Twitter
} from "lucide-react";

export default function Footer() {
  return (
    <footer className="py-12 relative overflow-hidden">
      <div className="container mx-auto px-6 sm:px-8 relative z-10">
        <div className="text-center mb-8 text-sm text-[#FFFFFF]/60 p-4 border border-[#00BFFF]/20 rounded-lg bg-[#121212]/40 hover:border-[#00BFFF]/40 transition-all duration-500 hover:shadow-[0_0_15px_rgba(0,191,255,0.15)]">
          <p className="mb-2"><strong className="text-[#00BFFF]">WARNING:</strong> This site has been known to cause spontaneous enlightenment. We recommend you prepare yourself mentally and if possible be sitting down. Side effects may include increased productivity, feelings of cyber-omnipotence, and occasional digital euphoria.</p>
          <p>Grimoire is not responsible for any existential crises that may occur upon realizing your business decisions were inferior to what an AI would have made.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          <div>
            <a href="#" className="flex items-center space-x-2 mb-6">
              <span className="text-[#7ED321] text-2xl font-bold">Grimoire</span>
              {/* <span className="text-[#FFFFFF] font-light">Inc.</span> */}
            </a>
            <p className="text-[#FFFFFF]/70 mb-6">
              Pioneering the unified intelligence layer for enterprises with grimOS, the cognitive operating system reshaping security, operations, and decision-making.
            </p>
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

          <div>
            <h4 className="text-lg font-semibold mb-6 flex items-center">
              <Terminal className="mr-2 h-4 w-4 text-[#00BFFF]" />
              <span>Platform</span>
            </h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">grimOS Overview</a></li>
              <li><a href="/features" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Core Modules</a></li>
              <li><a href="/demo" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Product Demo</a></li>
              <li><a href="/features" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Security Features</a></li>
              <li><a href="/features" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Cognitive Core</a></li>
              <li><a href="/features" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Universal API Fabric</a></li>
              <li><a href="/#pricing" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Pricing Models</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold mb-6 flex items-center">
              <FileCode className="mr-2 h-4 w-4 text-[#00BFFF]" />
              <span>Resources</span>
            </h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Documentation</a></li>
              <li><a href="#" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">API Reference</a></li>
              <li><a href="#" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Developer Portal</a></li>
              <li><a href="#" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Case Studies</a></li>
              <li><a href="#" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Whitepapers</a></li>
              <li><a href="#" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300">Implementation Guide</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold mb-6 flex items-center">
              <Shield className="mr-2 h-4 w-4 text-[#FF1D58]" />
              <span>Company</span>
            </h4>
            <ul className="space-y-3">
              <li><a href="/about" className="text-[#FFFFFF]/70 hover:text-[#FF1D58] transition-colors duration-300">About Grimoire</a></li>
              <li><a href="/team" className="text-[#FFFFFF]/70 hover:text-[#FF1D58] transition-colors duration-300">Team</a></li>
              <li><a href="/faq" className="text-[#FFFFFF]/70 hover:text-[#FF1D58] transition-colors duration-300">FAQ</a></li>
              <li><a href="/#contact" className="text-[#FFFFFF]/70 hover:text-[#FF1D58] transition-colors duration-300">Contact</a></li>
              <li><a href="/careers" className="text-[#FFFFFF]/70 hover:text-[#FF1D58] transition-colors duration-300">Careers</a></li>
              <li><a href="/blog" className="text-[#FFFFFF]/70 hover:text-[#FF1D58] transition-colors duration-300">Blog</a></li>
            </ul>
          </div>
        </div>

        <motion.div 
          className="glass-secondary digital-weave-bg rounded-xl p-6 border border-[#00BFFF]/20"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center mb-4 md:mb-0">
              <Lock className="h-4 w-4 text-[#00BFFF] mr-2" />
              <p className="text-[#FFFFFF]/70">
                &copy; {new Date().getFullYear()} Grimoire. All rights reserved.
              </p>
            </div>
            <div className="flex flex-wrap justify-center md:justify-end gap-x-6 gap-y-2">
              <a href="/privacy" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300 text-sm">Privacy Policy</a>
              <a href="/privacy" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300 text-sm">Terms of Service</a>
              <a href="/support" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300 text-sm">Support</a>
              <a href="/privacy" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300 text-sm">Cookies</a>
              <a href="/privacy" className="text-[#FFFFFF]/70 hover:text-[#00BFFF] transition-colors duration-300 text-sm">Accessibility</a>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Background accents */}
      <div className="absolute bottom-0 left-0 w-full h-96 bg-gradient-to-t from-[#121212] to-transparent"></div>
      <div className="absolute bottom-1/2 left-1/4 w-64 h-64 bg-[#7ED321]/5 rounded-full filter blur-3xl"></div>
      <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-[#00BFFF]/5 rounded-full filter blur-3xl"></div>
    </footer>
  );
}