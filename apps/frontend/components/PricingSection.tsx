import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import TierComparison from "./TierComparison";
import { useLocation } from "wouter";
import { SignedOut, SignedIn } from "@clerk/clerk-react";

const pricingPlans = [
  {
    name: "grimOS Essentials",
    description: "Core security and operations",
    price: "Contact",
    period: " for pricing",
    features: [
      "Security Module: Basic Threat Intelligence",
      "User Behavior Analytics (UBA essentials)",
      "Operations Module: Standard Workflow Automation",
      "Core Data Integration",
      "Limited Cognitive Core capabilities",
      "Standard support"
    ],
    ctaText: "Get Access",
    ctaLink: "/sign-up",
    highlighted: false,
    colorClass: "glass-primary",
    checkColor: "#7ED321"
  },
  {
    name: "grimOS Business",
    description: "Advanced automation and AI",
    price: "Contact",
    period: " for pricing",
    features: [
      "Full Security Module: Advanced Threat Intelligence",
      "Complete UBA and SOAR capabilities",
      "Advanced Workflow Automation",
      "Process Mining & Optimization",
      "Strategic Recommendations",
      "Predictive Modeling (standard)",
      "Universal API Fabric access (with limits)",
      "Priority support"
    ],
    ctaText: "Request a Demo",
    ctaLink: "/sign-up",
    highlighted: true,
    badge: "Recommended",
    colorClass: "glass-secondary",
    checkColor: "#00BFFF"
  },
  {
    name: "grimOS Enterprise",
    description: "Autonomous capabilities",
    price: "Contact",
    period: " for pricing",
    features: [
      "All modules with full capabilities",
      "Autonomous Decision-Making (scoped)",
      "Advanced Predictive Modeling",
      "Full AI Agent deployment and management",
      "Dynamic Resource Allocation",
      "Advanced Security: Deception Technology",
      "Full Universal API Fabric access",
      "Premium support with dedicated SLAs"
    ],
    ctaText: "Contact Sales",
    ctaLink: "#contact",
    highlighted: false,
    colorClass: "glass-accent",
    checkColor: "#FF1D58"
  }
];

export default function PricingSection() {
  const [_, navigate] = useLocation();

  return (
    <section id="pricing" className="py-20 relative overflow-hidden mobile-py">
      <div className="container mx-auto px-6 sm:px-8 relative z-10 mobile-px">
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Tiered Subscription Model</h2>
          <p className="text-lg text-[#FFFFFF]/80 max-w-2xl mx-auto">
            Scale your business singularity with the appropriate grimOS tier for your enterprise.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {pricingPlans.map((plan, index) => (
            <motion.div 
              key={index}
              className={`${plan.colorClass} rounded-xl overflow-hidden transition-all duration-300 hover:-translate-y-2 ${
                plan.highlighted ? `border border-[${plan.checkColor}]/50 relative shadow-lg shadow-[${plan.checkColor}]/20` : ""
              }`}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              {plan.badge && (
                <div className="absolute top-0 right-0">
                  <Badge className="bg-[#00BFFF] text-white px-4 py-1 text-sm font-medium rounded-bl-lg rounded-tr-xl">
                    {plan.badge}
                  </Badge>
                </div>
              )}
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">{plan.name}</h3>
                <p className="text-[#FFFFFF]/60 mb-4">{plan.description}</p>
                <div className="mb-6">
                  <span className="text-3xl font-bold">{plan.price}</span>
                  <span className="text-[#FFFFFF]/60">{plan.period}</span>
                </div>
                <ul className="space-y-3 mb-6">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start">
                      <Check className={`text-[${plan.checkColor}] mr-2 h-5 w-5 mt-1`} style={{color: plan.checkColor}} />
                      <span className="text-[#FFFFFF]/80">{feature}</span>
                    </li>
                  ))}
                </ul>

                <SignedIn>
                  <Button 
                    className={
                      plan.highlighted
                        ? `w-full bg-[${plan.checkColor}] hover:bg-[${plan.checkColor}]/90 text-white px-6 py-3 h-auto rounded-xl text-lg font-medium`
                        : `w-full ${plan.colorClass} hover:bg-[${plan.checkColor}]/10 text-white px-6 py-3 h-auto rounded-xl text-lg font-medium`
                    }
                    style={
                      plan.highlighted 
                        ? {backgroundColor: plan.checkColor} 
                        : {}
                    }
                    onClick={() => navigate("/dashboard")}
                  >
                    <span className={
                      plan.highlighted ? "" : `btn-hover-effect${index === 2 ? '-accent' : index === 0 ? '' : '-secondary'}`
                    }>
                      Go to Dashboard
                    </span>
                  </Button>
                </SignedIn>

                <SignedOut>
                  <Button 
                    className={
                      plan.highlighted
                        ? `w-full bg-[${plan.checkColor}] hover:bg-[${plan.checkColor}]/90 text-white px-6 py-3 h-auto rounded-xl text-lg font-medium`
                        : `w-full ${plan.colorClass} hover:bg-[${plan.checkColor}]/10 text-white px-6 py-3 h-auto rounded-xl text-lg font-medium`
                    }
                    style={
                      plan.highlighted 
                        ? {backgroundColor: plan.checkColor} 
                        : {}
                    }
                    onClick={() => index === 2 ? null : navigate(plan.ctaLink)}
                  >
                    <span className={
                      plan.highlighted ? "" : `btn-hover-effect${index === 2 ? '-accent' : index === 0 ? '' : '-secondary'}`
                    }>
                      {plan.ctaText}
                    </span>
                  </Button>
                </SignedOut>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Detailed feature comparison */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <TierComparison />
        </motion.div>

        <motion.div 
          className="text-center max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <p className="text-[#FFFFFF]/60 text-sm">
            Additional monetization options available through API Usage Fees, Ecosystem Revenue Share,
            AI-as-a-Service offerings, and ethically sourced Data Monetization for industry benchmarks.
            Contact our sales team for detailed information.
          </p>
        </motion.div>
      </div>

      {/* Background accents */}
      <div className="absolute top-1/4 -left-20 w-80 h-80 bg-[#7ED321]/5 rounded-full filter blur-3xl"></div>
      <div className="absolute bottom-1/3 right-0 w-96 h-96 bg-[#00BFFF]/5 rounded-full filter blur-3xl"></div>
    </section>
  );
}