
import { motion } from "framer-motion";
import { CalendarIcon, Clock, ArrowRight } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Badge } from "@/components/ui/badge";
import { useEffect } from "react";

export default function Blog() {
  useEffect(() => {
    document.title = "Blog | BitBrew Inc.";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'Explore the latest insights on AI, enterprise security, and strategic operations from BitBrew Inc.');
    }
  }, []);

  const blogPosts = [
    {
      id: 1,
      title: "The Future of Enterprise Intelligence with grimOS",
      excerpt: "Explore how grimOS is revolutionizing enterprise operations by unifying security, strategic decision-making, and operational efficiency.",
      date: "August 15, 2023",
      readTime: "8 min read",
      category: "Product",
      image: "/blog-1.jpg" // Placeholder - would need an actual image
    },
    {
      id: 2,
      title: "AI-Driven Security: Protecting Enterprise Assets",
      excerpt: "In today's threat landscape, AI-driven security systems like those in grimOS provide unprecedented protection for enterprise data and systems.",
      date: "July 28, 2023",
      readTime: "6 min read",
      category: "Security"
    },
    {
      id: 3,
      title: "Case Study: How Fortune 500 Companies Leverage grimOS",
      excerpt: "Learn how leading enterprises across various industries are implementing grimOS to drive efficiency and strategic advantage.",
      date: "June 12, 2023",
      readTime: "10 min read",
      category: "Case Study"
    },
    {
      id: 4,
      title: "The Technology Stack Behind grimOS",
      excerpt: "A deep dive into the cutting-edge technologies that power grimOS and make it the most sophisticated cognitive operating system available.",
      date: "May 30, 2023",
      readTime: "12 min read",
      category: "Technology"
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
          <div className="max-w-4xl mx-auto mb-12">
            <h1 className="text-4xl font-bold mb-8">Blog</h1>
            <p className="text-[#FFFFFF]/80 text-lg">
              Insights on AI, enterprise security, and strategic operations from BitBrew Inc.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            {blogPosts.map((post) => (
              <motion.div
                key={post.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: post.id * 0.1 }}
                className="glass p-6 rounded-xl hover:shadow-lg transition-shadow"
              >
                {post.image && (
                  <div className="mb-4 rounded-lg overflow-hidden h-48 bg-gradient-to-br from-[#7ED321]/20 to-[#00BFFF]/20 flex items-center justify-center">
                    <span className="text-[#FFFFFF]/30 text-sm">Image placeholder</span>
                  </div>
                )}
                <Badge variant={post.category === "Security" ? "destructive" : 
                         post.category === "Product" ? "default" : 
                         post.category === "Technology" ? "secondary" : "outline"} 
                       className="mb-3">
                  {post.category}
                </Badge>
                <h3 className="text-xl font-semibold mb-3">{post.title}</h3>
                <p className="text-[#FFFFFF]/70 mb-4">{post.excerpt}</p>
                <div className="flex items-center justify-between text-sm text-[#FFFFFF]/50">
                  <div className="flex items-center">
                    <CalendarIcon className="w-4 h-4 mr-1" />
                    <span>{post.date}</span>
                  </div>
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    <span>{post.readTime}</span>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-[#FFFFFF]/10">
                  <a href="#" className="inline-flex items-center text-[#7ED321] hover:text-[#7ED321]/80 transition-colors">
                    Read More <ArrowRight className="ml-2 w-4 h-4" />
                  </a>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="flex justify-center">
            <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2">
              Load More Articles
            </button>
          </div>
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}
