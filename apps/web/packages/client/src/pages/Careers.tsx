
import { motion } from "framer-motion";
import { BriefcaseIcon, MapPin, DollarSign, Clock, ArrowRight } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { useEffect } from "react";

export default function Careers() {
  useEffect(() => {
    document.title = "Careers | BitBrew Inc.";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'Join BitBrew Inc. and help build the future of enterprise intelligence with grimOS. Explore career opportunities.');
    }
  }, []);

  const positions = [
    {
      id: 1,
      title: "Senior AI Engineer",
      department: "Engineering",
      location: "Remote",
      type: "Full-time",
      salary: "$140,000 - $180,000",
      description: "As a Senior AI Engineer, you will be responsible for designing and implementing advanced AI systems for our grimOS platform, focusing on machine learning models, natural language processing, and cognitive computing."
    },
    {
      id: 2,
      title: "Enterprise Security Specialist",
      department: "Security",
      location: "San Francisco, CA",
      type: "Full-time",
      salary: "$130,000 - $160,000",
      description: "We're looking for an Enterprise Security Specialist to strengthen grimOS's security architecture, implement advanced threat detection systems, and ensure compliance with industry standards."
    },
    {
      id: 3,
      title: "Product Manager",
      department: "Product",
      location: "Remote",
      type: "Full-time",
      salary: "$120,000 - $150,000",
      description: "Join our product team to drive the strategic direction of grimOS features, work with cross-functional teams, and ensure our product meets enterprise client needs."
    },
    {
      id: 4,
      title: "Frontend Developer",
      department: "Engineering",
      location: "Remote",
      type: "Full-time",
      salary: "$100,000 - $130,000",
      description: "Help build intuitive, responsive interfaces for grimOS that make complex enterprise operations simple and efficient for users across various roles."
    },
    {
      id: 5,
      title: "Enterprise Solutions Architect",
      department: "Client Success",
      location: "New York, NY",
      type: "Full-time",
      salary: "$150,000 - $190,000",
      description: "Design and implement enterprise-scale grimOS deployments, working directly with our largest clients to ensure successful integration and adoption."
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
        >
          <div className="max-w-4xl mx-auto mb-16">
            <h1 className="text-4xl font-bold mb-6">Join the BitBrew Team</h1>
            <p className="text-[#FFFFFF]/80 text-lg mb-8">
              Help us build the future of enterprise intelligence with grimOS. We're looking for 
              talented individuals who are passionate about AI, security, and transformative technology.
            </p>
            
            <div className="glass p-8 rounded-xl mb-12">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-semibold mb-4">Why Work With Us</h2>
                <p className="text-[#FFFFFF]/70 mb-6 max-w-2xl mx-auto">
                  At BitBrew, you'll be working on cutting-edge technology that's transforming how enterprises operate. 
                  Join our team and help shape the future of business intelligence.
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="bg-gradient-to-br from-[#7ED321]/20 to-[#7ED321]/5 p-6 rounded-xl mb-4 flex items-center justify-center">
                    <BriefcaseIcon className="h-10 w-10 text-[#7ED321]" />
                  </div>
                  <h3 className="text-lg font-medium mb-2">Cutting-Edge Work</h3>
                  <p className="text-[#FFFFFF]/70 text-sm">
                    Work on advanced AI systems that are defining the future of enterprise operations.
                  </p>
                </div>
                
                <div className="text-center">
                  <div className="bg-gradient-to-br from-[#00BFFF]/20 to-[#00BFFF]/5 p-6 rounded-xl mb-4 flex items-center justify-center">
                    <Clock className="h-10 w-10 text-[#00BFFF]" />
                  </div>
                  <h3 className="text-lg font-medium mb-2">Flexible Schedule</h3>
                  <p className="text-[#FFFFFF]/70 text-sm">
                    We focus on results, not hours. Work when and where you're most productive.
                  </p>
                </div>
                
                <div className="text-center">
                  <div className="bg-gradient-to-br from-[#FF1D58]/20 to-[#FF1D58]/5 p-6 rounded-xl mb-4 flex items-center justify-center">
                    <DollarSign className="h-10 w-10 text-[#FF1D58]" />
                  </div>
                  <h3 className="text-lg font-medium mb-2">Competitive Compensation</h3>
                  <p className="text-[#FFFFFF]/70 text-sm">
                    Enjoy industry-leading pay, comprehensive benefits, and equity options.
                  </p>
                </div>
              </div>
            </div>
            
            <h2 className="text-2xl font-semibold mb-6">Open Positions</h2>
            <div className="space-y-6 mb-12">
              {positions.map((position) => (
                <Card key={position.id} className="bg-[#1E1E1E] border-[#2A2A2A] overflow-hidden">
                  <CardContent className="p-0">
                    <div className="p-6">
                      <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
                        <div>
                          <div className="flex items-center mb-2">
                            <h3 className="text-xl font-semibold">{position.title}</h3>
                            <Badge variant="outline" className="ml-3">
                              {position.department}
                            </Badge>
                          </div>
                          <div className="flex flex-wrap gap-4 text-sm text-[#FFFFFF]/70">
                            <div className="flex items-center">
                              <MapPin className="h-4 w-4 mr-1" />
                              <span>{position.location}</span>
                            </div>
                            <div className="flex items-center">
                              <Clock className="h-4 w-4 mr-1" />
                              <span>{position.type}</span>
                            </div>
                            <div className="flex items-center">
                              <DollarSign className="h-4 w-4 mr-1" />
                              <span>{position.salary}</span>
                            </div>
                          </div>
                        </div>
                        <div className="mt-4 md:mt-0">
                          <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 py-2">
                            Apply Now
                          </button>
                        </div>
                      </div>
                      <p className="text-[#FFFFFF]/70">
                        {position.description}
                      </p>
                      <div className="mt-4 pt-2">
                        <a href="#" className="inline-flex items-center text-[#7ED321] hover:text-[#7ED321]/80 transition-colors text-sm">
                          View Full Description <ArrowRight className="ml-1 w-3 h-3" />
                        </a>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
            
            <div className="glass p-8 rounded-xl text-center">
              <h3 className="text-xl font-semibold mb-4">Don't see a role that fits?</h3>
              <p className="text-[#FFFFFF]/70 mb-6 max-w-lg mx-auto">
                We're always looking for talented individuals. Send us your resume and let us know how you can contribute to BitBrew Inc.
              </p>
              <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-secondary text-secondary-foreground hover:bg-secondary/90 h-10 px-6 py-2">
                Submit General Application
              </button>
            </div>
          </div>
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}
