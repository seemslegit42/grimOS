// Inspired by shadcn/ui and grimOS frontend tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
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
        // grimOS Corporate Cyberpunk with Digital Weave palette
        background: "hsl(var(--background))", // Example: oklch(0.145 0 0) -> hsl(0 0% 14.5%)
        foreground: "hsl(var(--foreground))", // Example: 0 0% 100%
        card: "hsl(var(--card))", // Example: oklch(0.205 0 0) -> hsl(0 0% 20.5%)
        "card-foreground": "hsl(var(--card-foreground))", // Example: 0 0% 100%

        "primary-accent": "hsl(var(--primary-accent))", // #7ED321
        "secondary-accent": "hsl(var(--secondary-accent))", // #00BFFF
        "tertiary-accent": "hsl(var(--tertiary-accent))", // #FF1D58
        
        border: "hsl(var(--border))", // Example: rgba(255, 255, 255, 0.1) -> hsla(0, 0%, 100%, 0.1)
        input: "hsl(var(--input))", // Example: rgba(255, 255, 255, 0.1) -> hsla(0, 0%, 100%, 0.1)
        ring: "hsl(var(--ring))", // Example: rgba(255, 255, 255, 0.3) -> hsla(0, 0%, 100%, 0.3)
        
        primary: {
          DEFAULT: "hsl(var(--primary))", // #7ED321
          foreground: "hsl(var(--primary-foreground))", // #121212
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))", // #00BFFF
          foreground: "hsl(var(--secondary-foreground))", // #121212
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))", // #FF1D58
          foreground: "hsl(var(--destructive-foreground))", // #FFFFFF
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)", // from globals.css: 0.625rem
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
