
import { ClerkProvider, SignedIn, SignedOut } from "@clerk/clerk-react";
import { QueryClientProvider } from "@tanstack/react-query";
import { Route, Switch } from "wouter";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import queryClient from "@/lib/queryClient";
import { useEffect, useState } from "react";

// Pages
import Home from "@/pages/Home";
import About from "@/pages/About";
import Features from "@/pages/Features";
import Demo from "@/pages/Demo";
import Pricing from "@/pages/Pricing";
import Blog from "@/pages/Blog";
import SignIn from "@/pages/SignIn";
import SignUp from "@/pages/SignUp";
import NotFound from "@/pages/not-found";
import FAQ from "@/pages/FAQ";
import Team from "@/pages/Team";
import Careers from "@/pages/Careers";
import Privacy from "@/pages/Privacy";
import Support from "@/pages/Support";

// Dashboard components
import Dashboard from "@/pages/Dashboard";

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!clerkPubKey) {
  throw new Error("Missing Clerk Publishable Key");
}

// Protected route component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const [_, navigate] = useLocation();

  useEffect(() => {
    // Handled by Clerk SignedIn/SignedOut components
  }, [navigate]);

  return <>{children}</>;
}

// Type declaration for custom window property
declare global {
  interface Window {
    LiterallyCanvas: any;
  }
}

export default function App() {
  const [theme, setTheme] = useState("dark");

  useEffect(() => {
    // Set initial theme
    document.documentElement.classList.add("dark");
  }, []);

  return (
    <ClerkProvider publishableKey={clerkPubKey}>
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <div className="animated-gradient-bg"></div>
          <Switch>
            <Route path="/" component={Home} />
            <Route path="/about" component={About} />
            <Route path="/features" component={Features} />
            <Route path="/demo" component={Demo} />
            <Route path="/blog" component={Blog} />
            <Route path="/faq" component={FAQ} />
            <Route path="/team" component={Team} />
            <Route path="/careers" component={Careers} />
            <Route path="/privacy" component={Privacy} />
            <Route path="/support" component={Support} />

            {/* Auth Routes */}
            <Route path="/sign-in" component={SignIn} />
            <Route path="/sign-up" component={SignUp} />

            {/* Protected Routes */}
            <Route path="/dashboard">
              <ProtectedRoute>
                <SignedIn>
                  <Dashboard />
                </SignedIn>
                <SignedOut>
                  <SignIn />
                </SignedOut>
              </ProtectedRoute>
            </Route>

            {/* 404 Route */}
            <Route component={NotFound} />
          </Switch>
          <Toaster />
        </TooltipProvider>
      </QueryClientProvider>
    </ClerkProvider>
  );
}
