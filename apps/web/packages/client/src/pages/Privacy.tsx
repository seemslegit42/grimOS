
import { motion } from "framer-motion";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function Privacy() {
  return (
    <div className="bg-gradient-to-b from-[#121212] to-[#1A1A1A] text-[#FFFFFF] min-h-screen digital-weave-bg">
      <Navbar />
      
      <main className="container mx-auto px-6 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto"
        >
          <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
          
          <div className="space-y-8 text-[#FFFFFF]/80">
            <section>
              <h2 className="text-2xl font-semibold mb-4 text-white">Data Collection</h2>
              <p className="mb-4">
                We collect information that you provide directly to us, including when you create an account,
                use our services, or communicate with us. This may include your name, email address,
                and usage data.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold mb-4 text-white">Data Usage</h2>
              <p className="mb-4">
                We use the collected data to provide and improve our services, communicate with you,
                and ensure the security of your account. Your data helps us enhance grimOS's
                cognitive capabilities while maintaining strict privacy standards.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold mb-4 text-white">Data Protection</h2>
              <p className="mb-4">
                BitBrew Inc. implements industry-leading security measures to protect your data.
                We use encryption, secure data storage, and regular security audits to ensure
                your information remains safe.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold mb-4 text-white">Your Rights</h2>
              <p className="mb-4">
                You have the right to access, correct, or delete your personal data. You can also
                request a copy of your data or object to its processing. Contact our support team
                for assistance with these requests.
              </p>
            </section>
          </div>
        </motion.div>
      </main>

      <Footer />
    </div>
  );
}
