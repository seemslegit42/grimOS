'use client'

import { useState } from 'react'
import { Button } from './ui/Button'
import { GlassmorphicModal } from './ui/GlassmorphicModal'

export function GlassmorphicModalDemo() {
  const [is_modal_open, setIsModalOpen] = useState(false)

  const open_modal = () => setIsModalOpen(true)
  const close_modal = () => setIsModalOpen(false)

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <Button onClick={open_modal}>Open Glassmorphic Modal</Button>

      <GlassmorphicModal
        isOpen={is_modal_open}
        onClose={close_modal}
        title="Glassmorphic Modal"
        description="A beautiful glassmorphic modal with accessibility support"
      >
        <div className="space-y-4">
          <p>
            This modal features a glassmorphic design with a subtle blur effect and transparency. It's built with
            accessibility in mind and includes:
          </p>

          <ul className="list-disc list-inside space-y-1 text-sm">
            <li>Keyboard navigation support (Escape to close)</li>
            <li>Focus trapping within the modal</li>
            <li>Proper ARIA attributes</li>
            <li>Click outside to dismiss</li>
            <li>Smooth animations with Framer Motion</li>
          </ul>

          <div className="flex justify-end gap-2 mt-6">
            <Button variant="outline" onClick={close_modal}>
              Cancel
            </Button>
            <Button onClick={close_modal}>Confirm</Button>
          </div>
        </div>
      </GlassmorphicModal>
    </div>
  )
}
