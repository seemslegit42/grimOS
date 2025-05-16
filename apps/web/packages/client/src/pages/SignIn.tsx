import { SignIn as ClerkSignIn } from "@clerk/clerk-react";
import { useLocation } from "wouter";
import { motion } from "framer-motion";

export default function SignIn() {
  const [_, navigate] = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#121212] to-[#1A1A1A] digital-weave-bg flex flex-col justify-center items-center px-4 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mb-8 text-center"
      >
        <a 
          href="/" 
          className="inline-flex items-center space-x-2 mb-8"
          onClick={(e) => {
            e.preventDefault();
            navigate("/");
          }}
        >
          <span className="text-[#7ED321] text-3xl font-bold">BitBrew</span>
          <span className="text-[#FFFFFF] font-light">Inc.</span>
        </a>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="glass rounded-xl p-4 md:p-8 max-w-md w-full backdrop-blur-[16px]"
      >
        <ClerkSignIn 
          routing="path" 
          path="/sign-in" 
          signUpUrl="/sign-up"
          redirectUrl="/dashboard"
          appearance={{
            elements: {
              rootBox: "w-full",
              card: "bg-transparent shadow-none w-full",
              headerTitle: "text-white",
              headerSubtitle: "text-[#FFFFFF]/70",
              socialButtonsBlockButton: "glass-darker text-white hover:glass-primary hover:bg-[#7ED321]/20",
              socialButtonsBlockButtonText: "text-white",
              dividerLine: "bg-[#FFFFFF]/20",
              dividerText: "text-[#FFFFFF]/60",
              formFieldLabel: "text-[#FFFFFF]/80",
              formFieldInput: "bg-[#121212]/60 text-white border-[#FFFFFF]/20 focus:border-[#7ED321]/70",
              formButtonPrimary: "bg-[#7ED321] text-white hover:bg-[#7ED321]/90 btn-hover-effect",
              footerActionText: "text-[#FFFFFF]/70",
              footerActionLink: "text-[#00BFFF] hover:text-[#00BFFF]/80",
              identityPreview: "glass-darker",
              identityPreviewText: "text-white",
              identityPreviewEditButton: "text-[#7ED321]",
              formFieldAction: "text-[#00BFFF]"
            }
          }}
        />
      </motion.div>
    </div>
  );
}