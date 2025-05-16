
import { motion } from "framer-motion";
import { HelpCircle } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { useEffect } from "react";

export default function FAQ() {
  useEffect(() => {
    document.title = "FAQ | BitBrew Inc.";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'Frequently asked questions about grimOS and BitBrew Inc. Learn more about our cognitive operating system and how it can transform your enterprise.');
    }
  }, []);

  return (
    <div className="bg-gradient-to-b from-[#121212] to-[#1A1A1A] text-[#FFFFFF] min-h-screen digital-weave-bg">
      <Navbar />
      
      <main className="container mx-auto px-6 py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto"
        >
          <div className="mb-12 text-center">
            <h1 className="text-4xl font-bold mb-6">Frequently Asked Questions</h1>
            <p className="text-[#FFFFFF]/80 text-lg">
              Get answers to common questions about grimOS and BitBrew Inc.
            </p>
          </div>

          <div className="glass-primary p-8 rounded-xl mb-10">
            <Accordion type="single" collapsible className="space-y-4">
              <AccordionItem value="item-1" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  What is grimOS?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  grimOS is an AI-powered cognitive operating system designed for enterprises. It integrates security, operations, and strategic decision-making into a self-optimizing platform. By providing a unified intelligence layer, grimOS enhances operational efficiency and security while enabling data-driven decision making.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-2" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  How does grimOS improve security?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  grimOS enhances security through its advanced threat intelligence capabilities, user behavior analytics, security orchestration (SOAR), and deception technology. These features work together to detect, analyze, and respond to potential security threats in real-time, providing comprehensive protection for your enterprise systems.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-3" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  What pricing plans are available?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  BitBrew offers three main pricing tiers: Essentials, Business, and Enterprise. Each plan includes different features and capabilities to meet the needs of organizations of various sizes. For detailed pricing information, please visit our Pricing page or contact our sales team for a customized quote.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-4" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  Can grimOS integrate with our existing systems?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  Yes, grimOS is designed with integration in mind. Our Universal API Fabric enables seamless connections with your existing enterprise systems, databases, and third-party applications. This allows you to leverage your current technology investments while enhancing them with grimOS's cognitive capabilities.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-5" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  How long does implementation take?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  Implementation timelines vary depending on the size and complexity of your organization. Typically, basic implementation can be completed in 4-6 weeks, with full enterprise integration taking 2-3 months. Our dedicated implementation team works closely with your IT staff to ensure a smooth and efficient deployment process.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-6" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  What kind of support does BitBrew provide?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  BitBrew offers various levels of support depending on your plan. All customers receive email support, while Business and Enterprise customers benefit from priority support with faster response times. Enterprise customers also receive a dedicated support team and SLA guarantees to ensure maximum system reliability and performance.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-7" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  Is grimOS suitable for small businesses?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  While grimOS was primarily designed for medium to large enterprises, our Essentials plan offers core functionality that can benefit smaller organizations looking to enhance their operations and security posture. We recommend contacting our sales team to discuss your specific needs and determine if grimOS is the right fit for your business.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-8" className="border-b border-[#7ED321]/20 pb-4">
                <AccordionTrigger className="text-xl font-medium hover:text-[#7ED321] transition-colors">
                  How does grimOS handle data privacy?
                </AccordionTrigger>
                <AccordionContent className="text-[#FFFFFF]/80 pt-2">
                  Data privacy is a top priority at BitBrew. grimOS incorporates advanced encryption, secure data storage, and comprehensive access controls to protect your sensitive information. We are compliant with major data protection regulations including GDPR and CCPA, and we continuously update our systems to address emerging privacy requirements and security standards.
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>

          <div className="glass-secondary p-8 rounded-xl text-center">
            <HelpCircle className="w-12 h-12 text-[#00BFFF] mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-4">Still have questions?</h3>
            <p className="text-[#FFFFFF]/70 mb-6 max-w-lg mx-auto">
              Our team is ready to help you with any additional questions you may have about grimOS and how it can benefit your organization.
            </p>
            <a href="/support" className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-[#00BFFF]/20 hover:bg-[#00BFFF]/30 text-white h-10 px-6 py-2">
              Contact Support
            </a>
          </div>
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}
