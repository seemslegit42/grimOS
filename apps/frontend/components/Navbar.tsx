import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useLocation } from "wouter";

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [_, navigate] = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navigationItems = [
    { name: "Home", href: "/" },
    { name: "Features", href: "/features" },
    { name: "Demo", href: "/demo" },
    { name: "About", href: "/about" },
    { name: "Team", href: "/team" },
    { name: "Blog", href: "/blog" },
    { name: "FAQ", href: "/faq" },
    { name: "Careers", href: "/careers" },
    { name: "Support", href: "/support" },
    { name: "Pricing", href: "/#pricing" },
  ];

  return (
    <header className="fixed w-full z-50">
      <nav className={`glass mx-auto px-4 sm:px-6 lg:px-8 py-4 transition-all duration-300 ${scrolled ? "shadow-lg shadow-[#7ED321]/10" : ""}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2 transition-all duration-300 hover:scale-105">
              <span className="text-[#7ED321] text-2xl font-bold bg-gradient-to-r from-[#7ED321] to-[#00BFFF] bg-clip-text text-transparent">Grimoire</span>
              {/* <span className="text-[#FFFFFF] font-light">Inc.</span> */}
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-[#FFFFFF] hover:text-[#7ED321]"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>

          {/* Desktop menu */}
          <div className="hidden md:flex md:items-center md:space-x-10">
            {navigationItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-[#FFFFFF] hover:text-[#7ED321] transition-colors duration-300 font-medium"
              >
                {item.name}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex md:items-center md:space-x-4">
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="flex items-center space-x-4"
            >
              <Button 
                variant="ghost"
                className="text-[#FFFFFF] hover:text-[#00BFFF] hover:bg-transparent auth-transition"
                onClick={() => navigate("/sign-in")}
              >
                <span className="relative">
                  Sign In
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00BFFF] transition-all duration-300 group-hover:w-full"></span>
                </span>
              </Button>
              <Button 
                className="glass-primary btn-hover-effect text-white bg-[#7ED321]/80 hover:bg-[#7ED321]/90 rounded-xl auth-transition"
                onClick={() => navigate("/sign-up")}
              >
                <span>Get Access</span>
              </Button>
            </motion.div>
          </div>
        </div>
      </nav>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <motion.div 
          className="glass-darker md:hidden"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navigationItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="block px-3 py-2 rounded-md text-base font-medium text-white hover:bg-[#7ED321]/20 transition-colors duration-300"
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.name}
              </Link>
            ))}

            <motion.div
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.1 }}
            >
              <a 
                className="block px-3 py-2 rounded-md text-base font-medium text-[#FFFFFF] hover:bg-[#00BFFF]/20 transition-colors duration-300 auth-transition"
                onClick={() => {
                  setMobileMenuOpen(false);
                  navigate("/sign-in");
                }}
              >
                Sign In
              </a>
              <a 
                className="block px-3 py-2 mt-4 rounded-md text-base font-medium text-white bg-[#7ED321]/80 hover:bg-[#7ED321]/90 transition-colors duration-300 animate-pulse-slow"
                onClick={() => {
                  setMobileMenuOpen(false);
                  navigate("/sign-up");
                }}
              >
                Get Access
              </a>
            </motion.div>
          </div>
        </motion.div>
      )}
    </header>
  );
}