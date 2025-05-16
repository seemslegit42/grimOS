import { motion } from "framer-motion";
import { Check, HelpCircle, X } from "lucide-react";
import { useState } from "react";
import { useLocation } from "wouter";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { SignedIn, SignedOut } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";

// Define feature categories and their explanations
const categories = [
  { 
    name: "Security Module", 
    tooltip: "Comprehensive security features designed to protect your enterprise data and systems"
  },
  { 
    name: "Operations Module", 
    tooltip: "Workflow automation and process optimization tools to streamline business operations"
  },
  { 
    name: "Cognitive Core", 
    tooltip: "AI-powered decision support and predictive capabilities"
  },
  { 
    name: "API Fabric", 
    tooltip: "Integration capabilities with existing enterprise systems and third-party applications"
  },
  { 
    name: "Support", 
    tooltip: "Technical assistance and customer service options"
  }
];

// Define specific features per category
const features = [
  // Security Module
  { 
    category: "Security Module",
    name: "Basic Threat Intelligence",
    tooltip: "Fundamental threat detection and alerting capabilities",
    tiers: { essentials: true, business: true, enterprise: true }
  },
  { 
    category: "Security Module",
    name: "User Behavior Analytics",
    tooltip: "Analysis of user actions to detect anomalous behaviors",
    tiers: { essentials: "Limited", business: true, enterprise: true }
  },
  { 
    category: "Security Module",
    name: "Security Orchestration (SOAR)",
    tooltip: "Automated security incident response and remediation",
    tiers: { essentials: false, business: true, enterprise: true }
  },
  { 
    category: "Security Module",
    name: "Deception Technology",
    tooltip: "Advanced threat detection using honeypots and decoy systems",
    tiers: { essentials: false, business: false, enterprise: true }
  },
  
  // Operations Module
  {
    category: "Operations Module",
    name: "Workflow Automation",
    tooltip: "Automated business process execution",
    tiers: { essentials: "Standard", business: "Advanced", enterprise: "Custom" }
  },
  {
    category: "Operations Module",
    name: "Data Integration",
    tooltip: "Connect and unify data from multiple sources",
    tiers: { essentials: "Core", business: true, enterprise: true }
  },
  {
    category: "Operations Module",
    name: "Process Mining",
    tooltip: "Discover and analyze actual business processes from event logs",
    tiers: { essentials: false, business: true, enterprise: true }
  },
  {
    category: "Operations Module",
    name: "Dynamic Resource Allocation",
    tooltip: "Intelligent distribution of computing resources based on needs",
    tiers: { essentials: false, business: false, enterprise: true }
  },
  
  // Cognitive Core
  {
    category: "Cognitive Core",
    name: "Strategic Recommendations",
    tooltip: "AI-generated business strategy suggestions",
    tiers: { essentials: "Limited", business: true, enterprise: true }
  },
  {
    category: "Cognitive Core",
    name: "Predictive Modeling",
    tooltip: "Forecasting future trends and outcomes",
    tiers: { essentials: false, business: "Standard", enterprise: "Advanced" }
  },
  {
    category: "Cognitive Core",
    name: "AI Agents",
    tooltip: "Autonomous AI entities that perform specific tasks",
    tiers: { essentials: false, business: "Limited", enterprise: true }
  },
  {
    category: "Cognitive Core",
    name: "Autonomous Decision-Making",
    tooltip: "AI-powered decisions within defined parameters",
    tiers: { essentials: false, business: false, enterprise: "Scoped" }
  },
  
  // API Fabric
  {
    category: "API Fabric",
    name: "API Access",
    tooltip: "Programmatic access to grimOS capabilities",
    tiers: { essentials: false, business: "Limited", enterprise: true }
  },
  {
    category: "API Fabric",
    name: "Custom Integrations",
    tooltip: "Tailored connections to specific enterprise systems",
    tiers: { essentials: false, business: false, enterprise: true }
  },
  
  // Support
  {
    category: "Support",
    name: "Email Support",
    tooltip: "Technical assistance via email",
    tiers: { essentials: true, business: true, enterprise: true }
  },
  {
    category: "Support",
    name: "Priority Support",
    tooltip: "Faster response times and dedicated support channels",
    tiers: { essentials: false, business: true, enterprise: true }
  },
  {
    category: "Support",
    name: "Dedicated Support Team",
    tooltip: "Assigned support specialists for your organization",
    tiers: { essentials: false, business: false, enterprise: true }
  },
  {
    category: "Support",
    name: "SLA Guarantees",
    tooltip: "Contractual service level agreements",
    tiers: { essentials: false, business: false, enterprise: true }
  }
];

// Helper function to render feature availability
const FeatureAvailability = ({ availability }: { availability: boolean | string }) => {
  if (typeof availability === 'boolean') {
    return availability ? (
      <Check className="text-[#7ED321] w-5 h-5" />
    ) : (
      <X className="text-[#64748B] w-5 h-5" />
    );
  }
  
  return <span className="text-sm text-[#00BFFF]">{availability}</span>;
};

export default function TierComparison() {
  const [selectedTier, setSelectedTier] = useState<'essentials' | 'business' | 'enterprise'>('business');
  const [_, navigate] = useLocation();
  
  // Animation for switching between tiers
  const switchTier = (tier: 'essentials' | 'business' | 'enterprise') => {
    // Add a glitch/cyberpunk effect when switching tiers
    const container = document.getElementById('tier-comparison');
    if (container) {
      container.classList.add('animate-pulse-fast');
      setTimeout(() => {
        container.classList.remove('animate-pulse-fast');
      }, 300);
    }
    
    setSelectedTier(tier);
  };

  return (
    <div id="tier-comparison" className="w-full max-w-6xl mx-auto my-16">
      {/* Tier selector tabs */}
      <div className="flex justify-center mb-10">
        <div className="glass rounded-xl p-1 flex">
          <button 
            onClick={() => switchTier('essentials')} 
            className={`py-2 px-4 sm:px-6 rounded-lg text-sm sm:text-base font-medium transition-all duration-300 ${
              selectedTier === 'essentials' 
                ? 'bg-[#7ED321]/20 text-[#7ED321] shadow-inner' 
                : 'text-[#FFFFFF]/70 hover:text-[#7ED321]'
            }`}
          >
            Essentials
          </button>
          <button 
            onClick={() => switchTier('business')} 
            className={`py-2 px-4 sm:px-6 rounded-lg text-sm sm:text-base font-medium transition-all duration-300 ${
              selectedTier === 'business' 
                ? 'bg-[#00BFFF]/20 text-[#00BFFF] shadow-inner' 
                : 'text-[#FFFFFF]/70 hover:text-[#00BFFF]'
            }`}
          >
            Business
          </button>
          <button 
            onClick={() => switchTier('enterprise')} 
            className={`py-2 px-4 sm:px-6 rounded-lg text-sm sm:text-base font-medium transition-all duration-300 ${
              selectedTier === 'enterprise' 
                ? 'bg-[#FF1D58]/20 text-[#FF1D58] shadow-inner' 
                : 'text-[#FFFFFF]/70 hover:text-[#FF1D58]'
            }`}
          >
            Enterprise
          </button>
        </div>
      </div>

      {/* Main comparison section */}
      <motion.div
        key={selectedTier}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className={`glass ${
          selectedTier === 'essentials' 
            ? 'glass-primary' 
            : selectedTier === 'business' 
              ? 'glass-secondary' 
              : 'glass-accent'
        } rounded-xl overflow-hidden border ${
          selectedTier === 'essentials' 
            ? 'border-[#7ED321]/20' 
            : selectedTier === 'business' 
              ? 'border-[#00BFFF]/20' 
              : 'border-[#FF1D58]/20'
        }`}
      >
        {/* Header */}
        <div className="p-6 text-center border-b border-white/10">
          <h3 className="text-2xl font-bold mb-2">
            grimOS {selectedTier === 'essentials' ? 'Essentials' : selectedTier === 'business' ? 'Business' : 'Enterprise'}
          </h3>
          <p className="text-[#FFFFFF]/70 mb-4">
            {selectedTier === 'essentials' 
              ? 'Core security and operations' 
              : selectedTier === 'business' 
                ? 'Advanced automation and AI' 
                : 'Autonomous capabilities and dynamic resource allocation'}
          </p>
          <div className="flex justify-center">
            <SignedIn>
              <Button 
                className={`${
                  selectedTier === 'essentials' 
                    ? 'bg-[#7ED321] hover:bg-[#7ED321]/90 btn-hover-effect' 
                    : selectedTier === 'business' 
                      ? 'bg-[#00BFFF] hover:bg-[#00BFFF]/90 btn-hover-effect-secondary' 
                      : 'bg-[#FF1D58] hover:bg-[#FF1D58]/90 btn-hover-effect-accent'
                } text-white px-6 py-2 rounded-xl`}
                onClick={() => navigate('/dashboard')}
              >
                My Dashboard
              </Button>
            </SignedIn>
            <SignedOut>
              <Button 
                className={`${
                  selectedTier === 'essentials' 
                    ? 'bg-[#7ED321] hover:bg-[#7ED321]/90 btn-hover-effect' 
                    : selectedTier === 'business' 
                      ? 'bg-[#00BFFF] hover:bg-[#00BFFF]/90 btn-hover-effect-secondary' 
                      : 'bg-[#FF1D58] hover:bg-[#FF1D58]/90 btn-hover-effect-accent'
                } text-white px-6 py-2 rounded-xl`}
                onClick={() => navigate('/sign-up')}
              >
                Get Started
              </Button>
            </SignedOut>
          </div>
        </div>

        {/* Features */}
        <div className="p-6">
          <TooltipProvider>
            {categories.map((category, categoryIndex) => (
              <div key={categoryIndex} className="mb-8">
                <div className="flex items-center mb-4">
                  <h4 className="text-lg font-semibold">{category.name}</h4>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <HelpCircle className="w-4 h-4 ml-2 text-[#FFFFFF]/50 cursor-help" />
                    </TooltipTrigger>
                    <TooltipContent 
                      side="top" 
                      className="bg-[#121212] border border-white/10 text-white max-w-xs"
                    >
                      {category.tooltip}
                    </TooltipContent>
                  </Tooltip>
                </div>

                <div className="space-y-3">
                  {features
                    .filter(feature => feature.category === category.name)
                    .map((feature, featureIndex) => (
                      <div 
                        key={featureIndex} 
                        className={`flex justify-between items-center py-2 px-4 rounded-lg ${
                          feature.tiers[selectedTier] ? 'glass-darker' : 'bg-transparent'
                        }`}
                      >
                        <div className="flex items-center">
                          <span className="text-[#FFFFFF]/80 mr-2">{feature.name}</span>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <HelpCircle className="w-3.5 h-3.5 text-[#FFFFFF]/40 cursor-help" />
                            </TooltipTrigger>
                            <TooltipContent 
                              side="right" 
                              className="bg-[#121212] border border-white/10 text-white max-w-xs"
                            >
                              {feature.tooltip}
                            </TooltipContent>
                          </Tooltip>
                        </div>
                        <div>
                          <FeatureAvailability availability={feature.tiers[selectedTier]} />
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            ))}
          </TooltipProvider>
        </div>
      </motion.div>
    </div>
  );
}