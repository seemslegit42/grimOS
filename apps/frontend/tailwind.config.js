/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        // Corporate Cyberpunk with Digital Weave palette
        background: "#121212", // Near Black
        "primary-accent": "#7ED321", // Lime Green
        "secondary-accent": "#00BFFF", // Electric Blue
        "tertiary-accent": "#FF1D58", // Hot Pink
        
        // UI semantic colors
        border: "rgba(255, 255, 255, 0.1)",
        input: "rgba(255, 255, 255, 0.1)",
        ring: "rgba(255, 255, 255, 0.3)",
        
        // Shadcn/ui compatibility
        primary: {
          DEFAULT: "#7ED321", // Lime Green
          foreground: "#121212", // Near Black
        },
        secondary: {
          DEFAULT: "#00BFFF", // Electric Blue
          foreground: "#121212", // Near Black
        },
        destructive: {
          DEFAULT: "#FF1D58", // Hot Pink
          foreground: "#FFFFFF", // White
        },
        muted: {
          DEFAULT: "rgba(255, 255, 255, 0.1)",
          foreground: "rgba(255, 255, 255, 0.7)",
        },
        accent: {
          DEFAULT: "rgba(255, 255, 255, 0.1)",
          foreground: "#FFFFFF", // White
        },
        card: {
          DEFAULT: "rgba(255, 255, 255, 0.1)",
          foreground: "#FFFFFF", // White
        },
      },
      borderRadius: {
        lg: "0.75rem",
        md: "0.5rem",
        sm: "0.25rem",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '16px',
        '2xl': '24px',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
