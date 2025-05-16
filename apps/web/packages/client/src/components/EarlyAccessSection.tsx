import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useToast } from "@/hooks/use-toast";
import { ArrowRight, Check, Loader2 } from "lucide-react";

// Define form schema
const earlyAccessSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  companyName: z.string().min(2, "Company name must be at least 2 characters"),
  companySize: z.string().min(1, "Please select a company size")
});

type EarlyAccessFormValues = z.infer<typeof earlyAccessSchema>;

export default function EarlyAccessSection() {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  
  const form = useForm<EarlyAccessFormValues>({
    resolver: zodResolver(earlyAccessSchema),
    defaultValues: {
      email: "",
      companyName: "",
      companySize: ""
    }
  });
  
  async function onSubmit(data: EarlyAccessFormValues) {
    setIsSubmitting(true);
    
    // Simulate API request
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setIsSubmitting(false);
    setIsSuccess(true);
    
    toast({
      title: "Early Access Request Sent",
      description: "We'll be in touch soon with details on your grimOS beta access.",
      variant: "default"
    });
    
    // Reset form after 2 seconds
    setTimeout(() => {
      form.reset();
      setIsSuccess(false);
    }, 2000);
  }
  
  return (
    <section id="early-access" className="py-20 relative overflow-hidden">
      <div className="container mx-auto px-6 sm:px-8 relative z-10">
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Request Early Access to grimOS Beta
          </h2>
          <p className="text-lg text-[#FFFFFF]/80 max-w-2xl mx-auto">
            Be among the first to experience the future of business intelligence. Limited beta slots available.
          </p>
        </motion.div>
        
        <motion.div 
          className="glass border border-[#00BFFF]/20 rounded-xl p-6 sm:p-8 max-w-3xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {isSuccess ? (
            <div className="flex flex-col items-center justify-center py-12">
              <div className="w-16 h-16 bg-[#7ED321]/20 rounded-full flex items-center justify-center mb-6 animate-fade-slide-up">
                <Check className="h-8 w-8 text-[#7ED321]" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4 animate-fade-slide-up" style={{ animationDelay: "0.1s" }}>
                Thank You!
              </h3>
              <p className="text-center text-[#FFFFFF]/80 max-w-md animate-fade-slide-up" style={{ animationDelay: "0.2s" }}>
                Your request for early access has been received. We'll review your application and be in touch soon with your exclusive grimOS beta access details.
              </p>
            </div>
          ) : (
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem className="col-span-2">
                        <FormLabel className="text-[#FFFFFF] text-sm font-medium">
                          Work Email
                        </FormLabel>
                        <FormControl>
                          <Input 
                            placeholder="your.name@company.com" 
                            {...field}
                            className="glass-darker border-[#00BFFF]/20 focus:border-[#00BFFF]/50 h-12"
                          />
                        </FormControl>
                        <FormMessage className="text-[#FF1D58]" />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={form.control}
                    name="companyName"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#FFFFFF] text-sm font-medium">
                          Company Name
                        </FormLabel>
                        <FormControl>
                          <Input 
                            placeholder="BitBrew Inc" 
                            {...field}
                            className="glass-darker border-[#00BFFF]/20 focus:border-[#00BFFF]/50 h-12"
                          />
                        </FormControl>
                        <FormMessage className="text-[#FF1D58]" />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={form.control}
                    name="companySize"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#FFFFFF] text-sm font-medium">
                          Company Size
                        </FormLabel>
                        <FormControl>
                          <select 
                            {...field}
                            className="w-full glass-darker border border-[#00BFFF]/20 focus:border-[#00BFFF]/50 h-12 rounded-md px-3 bg-transparent text-[#FFFFFF]/90"
                          >
                            <option value="" disabled>Select company size</option>
                            <option value="1-10">1-10 employees</option>
                            <option value="11-50">11-50 employees</option>
                            <option value="51-200">51-200 employees</option>
                            <option value="201-500">201-500 employees</option>
                            <option value="501+">501+ employees</option>
                          </select>
                        </FormControl>
                        <FormMessage className="text-[#FF1D58]" />
                      </FormItem>
                    )}
                  />
                </div>
                
                <div className="pt-4">
                  <Button 
                    type="submit"
                    className="w-full glass-secondary border-[#00BFFF]/20 bg-[#00BFFF]/20 hover:bg-[#00BFFF]/30 cyber-glow text-[#FFFFFF] h-14 rounded-xl text-lg font-semibold"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        Request Beta Access
                        <ArrowRight className="ml-2 h-5 w-5" />
                      </>
                    )}
                  </Button>
                </div>
                
                <p className="text-xs text-[#FFFFFF]/60 text-center">
                  By submitting this form, you agree to our <a href="#" className="text-[#00BFFF] hover:underline">Terms of Service</a> and <a href="#" className="text-[#00BFFF] hover:underline">Privacy Policy</a>.
                </p>
              </form>
            </Form>
          )}
        </motion.div>
        
        <motion.div 
          className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="glass-darker p-5 rounded-xl text-center">
            <div className="w-12 h-12 rounded-full bg-[#7ED321]/20 flex items-center justify-center mx-auto mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-[#7ED321]">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
            </div>
            <h3 className="text-lg font-bold text-[#FFFFFF] mb-2">Early Feature Access</h3>
            <p className="text-sm text-[#FFFFFF]/70">Be the first to access new grimOS features and modules before general release.</p>
          </div>
          
          <div className="glass-darker p-5 rounded-xl text-center">
            <div className="w-12 h-12 rounded-full bg-[#00BFFF]/20 flex items-center justify-center mx-auto mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-[#00BFFF]">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <h3 className="text-lg font-bold text-[#FFFFFF] mb-2">Direct Support Team</h3>
            <p className="text-sm text-[#FFFFFF]/70">Priority access to our support team and dedicated onboarding specialists.</p>
          </div>
          
          <div className="glass-darker p-5 rounded-xl text-center">
            <div className="w-12 h-12 rounded-full bg-[#FF1D58]/20 flex items-center justify-center mx-auto mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-[#FF1D58]">
                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
              </svg>
            </div>
            <h3 className="text-lg font-bold text-[#FFFFFF] mb-2">Exclusive Pricing</h3>
            <p className="text-sm text-[#FFFFFF]/70">Early adopters receive preferential pricing locked in for life.</p>
          </div>
        </motion.div>
      </div>
      
      {/* Background accents */}
      <div className="absolute top-1/4 -right-32 w-96 h-96 bg-[#00BFFF]/5 rounded-full filter blur-3xl"></div>
      <div className="absolute bottom-1/3 left-0 w-80 h-80 bg-[#7ED321]/5 rounded-full filter blur-3xl"></div>
    </section>
  );
}