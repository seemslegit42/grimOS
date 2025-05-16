import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import FeaturesSection from "@/components/FeaturesSection";
import TestimonialsSection from "@/components/TestimonialsSection";
import PricingSection from "@/components/PricingSection";
import CTASection from "@/components/CTASection";
import ContactSection from "@/components/ContactSection";
import EarlyAccessSection from "@/components/EarlyAccessSection";
import Footer from "@/components/Footer";
import { useEffect } from "react";

export default function Home() {
  // Update document title for SEO
  useEffect(() => {
    document.title = "BitBrew Inc. — grimOS: The AI-Powered Cognitive Operating System";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'grimOS by BitBrew Inc. is the unified intelligence layer that integrates security, operations, and strategic decision-making into a self-optimizing platform for enterprises.');
    } else {
      const newMetaDesc = document.createElement('meta');
      newMetaDesc.name = 'description';
      newMetaDesc.content = 'grimOS by BitBrew Inc. is the unified intelligence layer that integrates security, operations, and strategic decision-making into a self-optimizing platform for enterprises.';
      document.head.appendChild(newMetaDesc);
    }

    // Add Open Graph tags for better social media sharing
    const ogTags = [
      { property: 'og:title', content: 'BitBrew Inc. — grimOS: The AI-Powered Cognitive Operating System' },
      { property: 'og:description', content: 'grimOS by BitBrew Inc. is the unified intelligence layer that integrates security, operations, and strategic decision-making into a self-optimizing platform for enterprises.' },
      { property: 'og:type', content: 'website' },
      { property: 'og:url', content: 'https://bitbrewinc.com' }
    ];

    ogTags.forEach(tag => {
      let ogTag = document.querySelector(`meta[property="${tag.property}"]`);
      if (ogTag) {
        ogTag.setAttribute('content', tag.content);
      } else {
        ogTag = document.createElement('meta');
        ogTag.setAttribute('property', tag.property);
        ogTag.setAttribute('content', tag.content);
        document.head.appendChild(ogTag);
      }
    });
  }, []);

  return (
    <div className="bg-gradient-to-b from-[#121212] to-[#1A1A1A] text-[#FFFFFF] min-h-screen digital-weave-bg relative overflow-hidden">
      <div className="animated-gradient-bg"></div>
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <TestimonialsSection />
      <PricingSection />
      <EarlyAccessSection />
      <CTASection />
      <ContactSection />
      <Footer />
    </main>
  )
}
import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import FeaturesSection from "@/components/FeaturesSection";
import TestimonialsSection from "@/components/TestimonialsSection";
import PricingSection from "@/components/PricingSection";
import CTASection from "@/components/CTASection";
import ContactSection from "@/components/ContactSection";
import EarlyAccessSection from "@/components/EarlyAccessSection";
import Footer from "@/components/Footer";
import { useEffect } from "react";

export default function Home() {
  // Update document title for SEO
  useEffect(() => {
    document.title = "BitBrew Inc. — grimOS: The AI-Powered Cognitive Operating System";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'grimOS by BitBrew Inc. is the unified intelligence layer that integrates security, operations, and strategic decision-making into a self-optimizing platform for enterprises.');
    } else {
      const newMetaDesc = document.createElement('meta');
      newMetaDesc.name = 'description';
      newMetaDesc.content = 'grimOS by BitBrew Inc. is the unified intelligence layer that integrates security, operations, and strategic decision-making into a self-optimizing platform for enterprises.';
      document.head.appendChild(newMetaDesc);
    }

    // Add Open Graph tags for better social media sharing
    const ogTags = [
      { property: 'og:title', content: 'BitBrew Inc. — grimOS: The AI-Powered Cognitive Operating System' },
      { property: 'og:description', content: 'grimOS by BitBrew Inc. is the unified intelligence layer that integrates security, operations, and strategic decision-making into a self-optimizing platform for enterprises.' },
      { property: 'og:type', content: 'website' },
      { property: 'og:url', content: 'https://bitbrewinc.com' }
    ];

    ogTags.forEach(tag => {
      let ogTag = document.querySelector(`meta[property="${tag.property}"]`);
      if (ogTag) {
        ogTag.setAttribute('content', tag.content);
      } else {
        ogTag = document.createElement('meta');
        ogTag.setAttribute('property', tag.property);
        ogTag.setAttribute('content', tag.content);
        document.head.appendChild(ogTag);
      }
    });
  }, []);

  return (
    <div className="bg-gradient-to-b from-[#121212] to-[#1A1A1A] text-[#FFFFFF] min-h-screen digital-weave-bg relative overflow-hidden">
      <div className="animated-gradient-bg"></div>
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <TestimonialsSection />
      <PricingSection />
      <EarlyAccessSection />
      <CTASection />
      <ContactSection />
      <Footer />
    </main>
  )
}
