'use client'

import { Button } from '@/components/ui/Button'
import { GlassmorphicCard } from '@/components/ui/GlassmorphicCard'
import { GlassmorphicModal } from '@/components/ui/GlassmorphicModal'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function Home() {
  const router = useRouter()
  const [health, setHealth] = useState<{ status: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    async function checkHealth() {
      try {
        const response = await fetch('/api/health')
        const data = await response.json()
        setHealth(data)
      } catch (error) {
        console.error('Error checking health:', error)
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6">
      <GlassmorphicCard className="max-w-2xl w-full text-center">
        <div className="py-8">
          <h1 className="text-4xl font-bold text-primary-accent mb-4">
            Grimoire™ (grimOS)
          </h1>
          <p className="text-white/70 mb-8 text-lg">
            Corporate Cyberpunk UI with Digital Weave palette and Glassmorphism
          </p>
          
          <div className="mb-8 p-4 rounded-lg bg-white/5">
            <h2 className="mb-3 text-xl font-semibold text-white">Backend Status</h2>
            <p className="text-white/80">
              {loading ? 'Checking...' : health ? `Status: ${health.status}` : 'Unable to connect to backend'}
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button onClick={() => router.push('/dashboard')}>
              Go to Dashboard
            </Button>
            <Button variant="outline" onClick={() => setShowModal(true)}>
              View UI Demo
            </Button>
          </div>
        </div>
      </GlassmorphicCard>
      
      <GlassmorphicModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Glassmorphic UI Components"
        description="This project implements the Corporate Cyberpunk with Digital Weave palette and Glassmorphism design."
      >
        <div className="space-y-4">
          <p className="text-white/80">
            The UI components in this project follow the design specifications outlined in the 
            "Grimoire™ (grimOS) - UI/UX Design Specification for MVP" document.
          </p>
          
          <p className="text-white/80">
            Key features of the glassmorphic design include:
          </p>
          
          <ul className="list-disc list-inside text-white/80 space-y-1">
            <li>Frosted glass effect with backdrop blur</li>
            <li>Semi-transparent surfaces</li>
            <li>Subtle borders to define edges</li>
            <li>Neon accent colors (Lime Green, Electric Blue, Hot Pink)</li>
            <li>Dark background with subtle patterns</li>
          </ul>
          
          <div className="pt-4">
            <Button onClick={() => setShowModal(false)} className="w-full">
              Close
            </Button>
          </div>
        </div>
      </GlassmorphicModal>
    </main>
  )
}
