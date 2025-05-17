import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/toaster";
import { cn } from "@/lib/utils";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "grimOS",
  description: "grimOS - A Unified Intelligence Layer",
};

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased",
          inter.variable
        )}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="relative flex min-h-screen flex-col">
            <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
              <div className="container flex h-14 max-w-screen-2xl items-center">
                <div className="mr-4 hidden md:flex">
                  <a className="mr-6 flex items-center space-x-2" href="/">
                    <span className="hidden font-bold sm:inline-block">
                      grimOS
                    </span>
                  </a>
                  <nav className="flex items-center space-x-6 text-sm font-medium">
                    <a
                      className="transition-colors hover:text-foreground/80 text-foreground/60"
                      href="/dashboard"
                    >
                      Dashboard
                    </a>
                  </nav>
                </div>
                <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
                </div>
              </div>
            </header>

            <div className="container flex-1 items-start md:grid md:grid-cols-[220px_minmax(0,1fr)] md:gap-6 lg:grid-cols-[240px_minmax(0,1fr)] lg:gap-10">
              <aside className="fixed top-14 z-30 -ml-2 hidden h-[calc(100vh-3.5rem)] w-full shrink-0 md:sticky md:block overflow-y-auto py-6 pr-6 lg:py-8">
                <nav className="flex flex-col space-y-2">
                  <p className="text-sm font-semibold text-primary">Navigation</p>
                  <a href="/dashboard/settings" className="text-muted-foreground hover:text-foreground">Settings</a>
                  <a href="/runeforge" className="text-muted-foreground hover:text-foreground">RuneForge</a>
                </nav>
              </aside>
              <main className="flex w-full flex-col overflow-hidden py-6 lg:py-8">
                {children}
              </main>
            </div>
            <footer className="py-6 md:px-8 md:py-0 border-t">
              <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
                <p className="text-balance text-center text-sm leading-loose text-muted-foreground md:text-left">
                  Built by grimOS Team.
                </p>
              </div>
            </footer>
          </div>
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
