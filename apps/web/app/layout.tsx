import { ClerkProvider } from "@clerk/nextjs";
import type { Metadata } from "next";
import "../packages/client/src/index.css"; // Import client CSS

export const metadata: Metadata = {
  title: "BitBrew - grimOS Web Interface",
  description: "Corporate Cyberpunk UI with Digital Weave palette and Glassmorphism",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="bg-[#121212] digital-weave-bg min-h-screen">
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}