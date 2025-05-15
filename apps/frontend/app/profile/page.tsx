'use client'

import { GlassmorphicCard } from "@/components/ui/GlassmorphicCard"
import { useUser } from "@clerk/nextjs"
import { useRouter } from "next/navigation"
import { useEffect } from "react"

export default function ProfilePage() {
  const { user, isLoaded, isSignedIn } = useUser()
  const router = useRouter()
  
  // Redirect if not signed in
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push('/sign-in')
    }
  }, [isLoaded, isSignedIn, router])

  if (!isLoaded || !isSignedIn) {
    return <div>Loading...</div>
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6">
      <GlassmorphicCard className="max-w-2xl w-full text-center">
        <div className="py-8">
          <h1 className="text-4xl font-bold text-primary-accent mb-4">
            User Profile
          </h1>
          
          <div className="flex flex-col items-center gap-4 mt-6">
            {user.imageUrl && (
              <img 
                src={user.imageUrl} 
                alt={user.fullName || user.username || "User"} 
                className="w-24 h-24 rounded-full border-2 border-primary-accent"
              />
            )}
            <h2 className="text-2xl font-semibold">{user.fullName || user.username}</h2>
            <p className="text-white/70">{user.primaryEmailAddress?.emailAddress}</p>
          </div>
          
          <div className="mt-8 p-4 rounded-lg bg-white/5">
            <h3 className="text-xl font-semibold mb-4">Account Information</h3>
            <ul className="space-y-2 text-left">
              <li><span className="font-semibold">User ID:</span> {user.id}</li>
              <li><span className="font-semibold">Created:</span> {new Date(user.createdAt).toLocaleDateString()}</li>
              <li><span className="font-semibold">Last Updated:</span> {new Date(user.updatedAt).toLocaleDateString()}</li>
            </ul>
          </div>
        </div>
      </GlassmorphicCard>
    </main>
  )
}
