'use client'

import { GlassmorphicCard } from "@/components/ui/GlassmorphicCard"
import { SignIn } from "@clerk/nextjs"

export default function SignInPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6">
      <GlassmorphicCard className="max-w-md w-full p-4">
        <div className="flex flex-col items-center">
          <h1 className="text-2xl font-bold text-primary-accent mb-6">Sign In</h1>
          <SignIn />
        </div>
      </GlassmorphicCard>
    </main>
  )
}
