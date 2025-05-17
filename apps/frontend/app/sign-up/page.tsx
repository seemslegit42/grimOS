'use client'

import { GlassmorphicCard } from "@/components/ui/GlassmorphicCard"

export default function SignUpPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6">
      <GlassmorphicCard className="max-w-md w-full p-4">
        <div className="flex flex-col items-center">
          <h1 className="text-2xl font-bold text-primary-accent mb-6">Sign Up</h1>
          <p className="text-center text-gray-400 mb-4">
            Authentication system has been upgraded from Clerk.
            New authentication system coming soon.
          </p>
        </div>
      </GlassmorphicCard>
    </main>
  )
}
