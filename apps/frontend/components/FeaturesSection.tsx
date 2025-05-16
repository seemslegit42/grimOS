import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

const features = [
  {
    icon: (
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
        className="text-[#7ED321] text-3xl"
      >
        <path d="M12 2c5.5 0 10 4.5 10 10s-4.5 10-10 10S2 17.5 2 12 6.5 2 12 2Z" />
        <path d="M12 7v10" />
        <path d="M7 12h10" />
      </svg>
    ),
    title: "Security Module",
    description: "Advanced threat intelligence, user behavior analytics, and security orchestration, automation, and response (SOAR) capabilities."
  },
  {
    icon: (
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
        className="text-[#00BFFF] text-3xl"
      >
        <path d="M3 3v18h18" />
        <path d="m19 9-5 5-4-4-3 3" />
      </svg>
    ),
    title: "Operations Module",
    description: "Workflow automation, data integration, and process mining to optimize operations and drive efficiency across your organization."
  },
  {
    icon: (
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
        className="text-[#7ED321] text-3xl"
      >
        <circle cx="12" cy="12" r="10" />
        <path d="M12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12Z" />
        <circle cx="12" cy="12" r="2" />
      </svg>
    ),
    title: "Cognitive Core",
    description: "AI-driven recommendations, predictive modeling, and specialized AI agents that continuously learn and adapt to your business needs."
  },
  {
    icon: (
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
        className="text-[#00BFFF] text-3xl"
      >
        <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </svg>
    ),
    title: "Universal API Fabric",
    description: "Extensible API architecture allowing seamless integration with existing enterprise systems and third-party applications."
  },
  {
    icon: (
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
        className="text-[#7ED321] text-3xl"
      >
        <circle cx="12" cy="12" r="10" />
        <path d="m4.9 4.9 14.2 14.2" />
      </svg>
    ),
    title: "Dynamic Resource Allocation",
    description: "Intelligently allocate and optimize computing resources based on real-time needs and priority workflows."
  },
  {
    icon: (
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
        className="text-[#00BFFF] text-3xl"
      >
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
      </svg>
    ),
    title: "Autonomous Decision-Making",
    description: "Enterprise-grade decision intelligence systems that operate within defined parameters to optimize business outcomes."
  }
];

export default function FeaturesSection() {
  return (
    <section id="features" className="py-20 relative overflow-hidden mobile-py">
      <div className="container mx-auto px-6 sm:px-8 relative z-10 mobile-px">
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Inside the Grimoire: Key Capabilities</h2>
          <p className="text-lg text-[#FFFFFF]/80 max-w-2xl mx-auto">
            Discover how grimOS unifies security, operations, and intelligence into a self-optimizing platform.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div 
              key={index}
              className={`glass ${index % 2 === 0 ? 'glass-primary' : 'glass-secondary'} rounded-xl p-6 h-full transition-all duration-300 hover:translate-y-[-4px] hover:shadow-lg ${index % 2 === 0 ? 'hover:shadow-[#7ED321]/10' : 'hover:shadow-[#00BFFF]/10'}`}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className={`${index % 2 === 0 ? 'text-[#7ED321]' : 'text-[#00BFFF]'} text-3xl mb-4`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
              <p className="text-[#FFFFFF]/70">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        <motion.div 
          className="mt-20 text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <Button 
            asChild
            variant="outline" 
            className="glass-secondary inline-flex items-center px-8 py-7 h-auto rounded-xl text-lg font-medium text-white hover:bg-[#00BFFF]/10 transition-all duration-300 btn-hover-effect-secondary"
          >
            <a href="#learn-more">
              Explore All Capabilities
              <ArrowRight className="ml-2 h-5 w-5" />
            </a>
          </Button>
        </motion.div>
      </div>

      {/* Background accents */}
      <div className="absolute top-20 right-0 w-72 h-72 bg-[#7ED321]/10 rounded-full filter blur-3xl"></div>
      <div className="absolute bottom-20 left-10 w-80 h-80 bg-[#00BFFF]/10 rounded-full filter blur-3xl"></div>
    </section>
  );
}