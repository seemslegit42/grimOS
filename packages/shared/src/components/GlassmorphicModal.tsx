import { AnimatePresence, motion } from 'framer-motion'
import { ReactNode } from 'react'
import { cn } from '../utils'
import { Button } from './Button'
import { CloseIcon } from './icons/CloseIcon'

// Import from glasscn-ui if available
// Note: If these imports fail, you may need to adjust the import path based on your project setup
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from 'glasscn-ui/dialog'

interface GlassmorphicModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  description?: string
  children: ReactNode
  className?: string
  trigger?: ReactNode
}

export function GlassmorphicModal({
  isOpen,
  onClose,
  title,
  description,
  children,
  className,
  trigger,
}: GlassmorphicModalProps) {
  // Try to use glasscn-ui Dialog if available
  try {
    return (
      <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
        {trigger && <DialogTrigger asChild>{trigger}</DialogTrigger>}
        <DialogContent 
          className={cn(
            'bg-white/15 backdrop-blur-xl border border-white/20',
            'shadow-[0_8px_32px_rgba(0,0,0,0.1)]',
            'text-white max-w-md',
            className
          )}
        >
          <DialogHeader>
            {title && <DialogTitle className="text-xl font-semibold">{title}</DialogTitle>}
            {description && <DialogDescription className="text-white/70">{description}</DialogDescription>}
          </DialogHeader>
          {children}
        </DialogContent>
      </Dialog>
    )
  } catch (e) {
    // Fallback to custom implementation if Dialog is not available
    return (
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            aria-modal="true"
            role="dialog"
            aria-labelledby={title ? 'modal-title' : undefined}
            aria-describedby={description ? 'modal-description' : undefined}
            onClick={(e) => {
              // Close when clicking the overlay
              if (e.target === e.currentTarget) {
                onClose()
              }
            }}
          >
            <motion.div
              className={cn(
                'relative max-w-md w-full max-h-[90vh] overflow-auto rounded-xl',
                'bg-white/15 backdrop-blur-xl border border-white/20',
                'shadow-[0_8px_32px_rgba(0,0,0,0.1)] p-6',
                'text-white',
                className
              )}
              initial={{ scale: 0.95, opacity: 0, y: 10 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.95, opacity: 0, y: 10 }}
              transition={{ duration: 0.2, ease: 'easeOut' }}
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close button */}
              <Button
                variant="ghost"
                size="sm"
                className="absolute top-2 right-2 p-1 h-8 w-8 rounded-full text-white/70 hover:text-white hover:bg-white/10"
                onClick={onClose}
                aria-label="Close modal"
              >
                <CloseIcon size={18} />
              </Button>

              {/* Modal header */}
              {(title || description) && (
                <div className="mb-4">
                  {title && (
                    <h2 id="modal-title" className="text-xl font-semibold">
                      {title}
                    </h2>
                  )}
                  {description && (
                    <p id="modal-description" className="text-sm text-white/70 mt-1">
                      {description}
                    </p>
                  )}
                </div>
              )}

              {/* Modal content */}
              <div>{children}</div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    )
  }
}