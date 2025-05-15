# Glassmorphic Modal Component

A beautiful, accessible glassmorphic modal component built with React, Tailwind CSS, and Framer Motion for Next.js applications.

## Features

* Glassmorphic design with backdrop blur and subtle transparency
* Smooth animations using Framer Motion
* Fully accessible with keyboard navigation support
* Click outside to dismiss
* ESC key to close
* Focus trapping within the modal
* Proper ARIA attributes
* Responsive design
* Customizable through props and className

## Usage

```tsx
import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { GlassmorphicModal } from '@/components/ui/GlassmorphicModal'

export function MyComponent() {
  const [is_modal_open, setIsModalOpen] = useState(false)

  const open_modal = () => setIsModalOpen(true)
  const close_modal = () => setIsModalOpen(false)

  return (
    <div>
      <Button onClick={open_modal}>Open Modal</Button>

      <GlassmorphicModal
        isOpen={is_modal_open}
        onClose={close_modal}
        title="Modal Title"
        description="Optional description text"
      >
        <div>
          {/* Your modal content goes here */}
          <p>This is the modal content.</p>

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
```

## Props

| Prop          | Type              | Description                                  |
| ------------- | ----------------- | -------------------------------------------- |
| `isOpen`      | boolean           | Controls whether the modal is visible        |
| `onClose`     | () => void        | Function called when the modal should close  |
| `title`       | string (optional) | Modal title displayed at the top             |
| `description` | string (optional) | Description text displayed below the title   |
| `children`    | ReactNode         | Content to be displayed inside the modal     |
| `className`   | string (optional) | Additional CSS classes to apply to the modal |

## Accessibility

This component follows accessibility best practices:

* Uses proper ARIA roles and attributes
* Supports keyboard navigation
* Traps focus within the modal when open
* Provides clear visual focus indicators
* Includes proper labeling for screen readers

## Customization

You can customize the appearance of the modal by passing a `className` prop:

```tsx
<GlassmorphicModal isOpen={is_modal_open} onClose={close_modal} className="bg-purple-900/20 border-purple-500/30">
  {/* Content */}
</GlassmorphicModal>
```

## Dependencies

* React
* Framer Motion
* Tailwind CSS
* Class Variance Authority (for the Button component)
