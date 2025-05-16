import { motion } from "framer-motion";

const testimonials = [
  {
    initials: "T",
    company: "TechForward Inc.",
    industry: "Enterprise Technology",
    quote: "grimOS has transformed our security posture and operational efficiency. The Cognitive Core anticipates cyber threats before they materialize and autonomously optimizes our resource allocation.",
    rating: 5,
    colorClass: "glass-primary",
    initialsColor: "#7ED321",
    starColor: "#7ED321"
  },
  {
    initials: "G",
    company: "Global Financial Services",
    industry: "Financial Technology",
    quote: "The predictive modeling capabilities in grimOS helped us identify market opportunities with 43% greater accuracy while maintaining stringent compliance with regulations across jurisdictions.",
    rating: 5,
    colorClass: "glass-secondary",
    initialsColor: "#00BFFF",
    starColor: "#00BFFF"
  },
  {
    initials: "M",
    company: "Medicorp Innovations",
    industry: "Healthcare Technology",
    quote: "Our data integration challenges seemed insurmountable until we implemented the Universal API Fabric. Now our systems communicate seamlessly, and the security module ensures HIPAA compliance at every touchpoint.",
    rating: 4.5,
    colorClass: "glass-accent",
    initialsColor: "#FF1D58",
    starColor: "#FF1D58"
  }
];

function StarRating({ rating, color }: { rating: number; color: string }) {
  return (
    <div className="flex" style={{ color }}>
      {[...Array(5)].map((_, i) => (
        <div key={i}>
          {i < Math.floor(rating) ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
          ) : rating - i > 0 && rating - i < 1 ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path d="M12 2L9.72 8.02 2 9.28l5 4.73L5.82 22 12 17.77 18.18 22 17 14.01l5-4.73-7.72-1.26z" />
              <path
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                d="M12 2L9.72 8.02 2 9.28l5 4.73L5.82 22 12 17.77 18.18 22 17 14.01l5-4.73-7.72-1.26z"
              />
              <path
                fill="none"
                d="M12 2v15.77"
                stroke="#121212"
                strokeWidth="2"
              />
              <path
                d="M12 2L9.72 8.02 2 9.28l5 4.73L5.82 22 12 17.77V2z"
                fill="currentColor"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-5 h-5"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
          )}
        </div>
      ))}
    </div>
  );
}

export default function TestimonialsSection() {
  return (
    <section id="testimonials" className="py-20 relative overflow-hidden mobile-py">
      <div className="container mx-auto px-6 sm:px-8 relative z-10 mobile-px">
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Trusted by Industry Leaders</h2>
          <p className="text-lg text-[#FFFFFF]/80 max-w-2xl mx-auto">
            See how enterprises are harnessing grimOS to drive transformation and secure their digital futures.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div 
              key={index}
              className={`${testimonial.colorClass} rounded-xl p-6 transition-all duration-300 hover:translate-y-[-4px] hover:shadow-lg hover:shadow-[${testimonial.starColor}]/10`}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className="flex items-start mb-4">
                <div className="mr-4">
                  <div className="w-14 h-14 rounded-full flex items-center justify-center" style={{ backgroundColor: `${testimonial.initialsColor}20` }}>
                    <span className="text-xl font-bold" style={{ color: testimonial.initialsColor }}>{testimonial.initials}</span>
                  </div>
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-white">{testimonial.company}</h4>
                  <p className="text-[#FFFFFF]/60 text-sm">{testimonial.industry}</p>
                </div>
              </div>
              <p className="text-[#FFFFFF]/80 italic">
                "{testimonial.quote}"
              </p>
              <div className="mt-4">
                <StarRating rating={testimonial.rating} color={testimonial.starColor} />
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div 
          className="mt-16 text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="glass digital-weave-bg p-6 rounded-xl max-w-3xl mx-auto">
            <p className="text-[#FFFFFF]/90 text-lg italic">
              "grimOS represents the next evolution in enterprise technology—a unified intelligence layer that truly 
              integrates strategic decision-making with operational execution."
            </p>
            <p className="mt-4 text-[#7ED321] font-medium">— Leading Industry Analyst</p>
          </div>
        </motion.div>
      </div>

      {/* Background accents */}
      <div className="absolute top-1/3 right-0 w-64 h-64 bg-[#00BFFF]/10 rounded-full filter blur-3xl"></div>
      <div className="absolute bottom-1/4 left-10 w-80 h-80 bg-[#7ED321]/10 rounded-full filter blur-3xl"></div>
    </section>
  );
}