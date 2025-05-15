import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Grimoire™ (grimOS)",
  description: "Corporate Cyberpunk UI with Digital Weave palette and Glassmorphism",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-pattern data-stream-bg">{children}</body>
    </html>
  )
}
