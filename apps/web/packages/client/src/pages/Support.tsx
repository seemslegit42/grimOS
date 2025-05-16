
import { motion } from "framer-motion";
import { Mail, MessageSquare, FileQuestion, Clock, CheckCircle2 } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Card, CardContent } from "@/components/ui/card";
import { useEffect } from "react";

export default function Support() {
  useEffect(() => {
    document.title = "Support | BitBrew Inc.";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'Get help with grimOS and BitBrew products. Access FAQs, documentation, and contact our support team.');
    }
  }, []);

  const faqs = [
    {
      question: "What is grimOS?",
      answer: "grimOS is an AI-powered cognitive operating system that integrates security, operations, and strategic decision-making for enterprises. It provides a unified intelligence layer that helps businesses optimize workflows and increase profit margins."
    },
    {
      question: "How do I deploy grimOS in my organization?",
      answer: "Deploying grimOS begins with an initial consultation where we assess your organization's specific needs. Our team then creates a tailored implementation plan, including integration with your existing systems, data migration, and training for your team members."
    },
    {
      question: "What security measures does grimOS implement?",
      answer: "grimOS incorporates state-of-the-art security protocols including end-to-end encryption, continuous threat monitoring, anomaly detection, and automatic security patching. All data is stored with enterprise-grade encryption and follows compliance requirements for various industries."
    },
    {
      question: "Can grimOS integrate with our existing software solutions?",
      answer: "Yes, grimOS is designed with integration in mind. It features robust APIs and connectors for most major enterprise software systems, databases, and cloud services. Our implementation team will work with you to ensure smooth integration with your tech stack."
    },
    {
      question: "What kind of training do you provide for new users?",
      answer: "We offer comprehensive training programs for all levels of users, from basic operations to advanced administration. Training is delivered through a combination of interactive tutorials, live workshops, documentation, and on-demand video resources."
    },
    {
      question: "How does the pricing structure work?",
      answer: "grimOS follows a tiered subscription model based on organization size, feature requirements, and implementation scope. We offer packages designed for small businesses, mid-sized companies, and enterprise-level organizations. Contact our sales team for a customized quote."
    }
  ];

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
          <h1 className="text-4xl font-bold mb-8">Support</h1>
          <p className="text-[#FFFFFF]/80 text-lg mb-12">
            We're here to help you get the most out of grimOS. Browse our FAQs, 
            documentation, or reach out to our support team.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <Card className="bg-[#1E1E1E] border-[#2A2A2A] text-white">
              <CardContent className="p-6">
                <div className="mb-4">
                  <MessageSquare className="h-8 w-8 text-[#7ED321]" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Live Chat</h3>
                <p className="text-[#FFFFFF]/70 mb-4 text-sm">
                  Chat with our support team for immediate assistance.
                </p>
                <div className="flex items-center text-xs text-[#FFFFFF]/60">
                  <Clock className="h-3 w-3 mr-1" />
                  <span>Available 24/7</span>
                </div>
                <button className="mt-4 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 py-2 w-full">
                  Start Chat
                </button>
              </CardContent>
            </Card>

            <Card className="bg-[#1E1E1E] border-[#2A2A2A] text-white">
              <CardContent className="p-6">
                <div className="mb-4">
                  <Mail className="h-8 w-8 text-[#00BFFF]" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Email Support</h3>
                <p className="text-[#FFFFFF]/70 mb-4 text-sm">
                  Send us an email and we'll get back to you within 24 hours.
                </p>
                <div className="flex items-center text-xs text-[#FFFFFF]/60">
                  <CheckCircle2 className="h-3 w-3 mr-1" />
                  <span>Guaranteed response</span>
                </div>
                <button className="mt-4 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-secondary text-secondary-foreground hover:bg-secondary/90 h-9 px-4 py-2 w-full">
                  Email Us
                </button>
              </CardContent>
            </Card>

            <Card className="bg-[#1E1E1E] border-[#2A2A2A] text-white">
              <CardContent className="p-6">
                <div className="mb-4">
                  <FileQuestion className="h-8 w-8 text-[#FF1D58]" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Documentation</h3>
                <p className="text-[#FFFFFF]/70 mb-4 text-sm">
                  Browse our comprehensive docs and API references.
                </p>
                <div className="flex items-center text-xs text-[#FFFFFF]/60">
                  <CheckCircle2 className="h-3 w-3 mr-1" />
                  <span>Regularly updated</span>
                </div>
                <button className="mt-4 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2 w-full">
                  View Docs
                </button>
              </CardContent>
            </Card>
          </div>

          <div className="mb-16">
            <h2 className="text-2xl font-semibold mb-6">Frequently Asked Questions</h2>
            <Accordion type="single" collapsible className="w-full">
              {faqs.map((faq, index) => (
                <AccordionItem key={index} value={`item-${index}`} className="border-[#2A2A2A]">
                  <AccordionTrigger className="text-left font-medium">
                    {faq.question}
                  </AccordionTrigger>
                  <AccordionContent className="text-[#FFFFFF]/70">
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>

          <div className="glass p-8 rounded-xl text-center">
            <h3 className="text-xl font-semibold mb-4">Still need help?</h3>
            <p className="text-[#FFFFFF]/70 mb-6 max-w-lg mx-auto">
              Our team of product specialists is available for more complex inquiries and enterprise support needs. Yes, they're actual humans (we checked). 
            </p>
            <p className="text-[#7ED321]/80 text-sm mb-4 italic">
              Fun fact: Our support team has a 98.7% success rate at explaining grimOS to executives who still use flip phones.
            </p>
            <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-6 py-2">
              Schedule a Call
            </button>
          </div>
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}
