import React, { ReactNode, useState } from 'react'
import { cn } from '@/lib/utils'

interface TooltipProps {
  content: string | ReactNode
  children: ReactNode
  position?: 'top' | 'bottom' | 'left' | 'right'
  delay?: number
  className?: string
}

export function Tooltip({ content, children, position = 'top', delay = 0, className = '' }: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false)

  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 transform -translate-y-1/2 ml-2',
  }

  const showTooltip = () => {
    setTimeout(() => {
      setIsVisible(true)
    }, delay)
  }

  const hideTooltip = () => {
    setIsVisible(false)
  }

  return (
    <div className="relative inline-block" onMouseEnter={showTooltip} onMouseLeave={hideTooltip}>
      {children}
      {isVisible && (
        <div
          className={cn(
            'absolute z-10 rounded-md bg-gray-900 px-3 py-2 text-sm font-medium text-white shadow-lg',
            positionClasses[position],
            className
          )}
        >
          {content}
          <div
            className={cn(
              'absolute h-2 w-2 rotate-45 transform bg-gray-900',
              position === 'top' && 'top-full left-1/2 -mt-1 -translate-x-1/2',
              position === 'bottom' && 'bottom-full left-1/2 -mb-1 -translate-x-1/2',
              position === 'left' && 'top-1/2 left-full -ml-1 -translate-y-1/2',
              position === 'right' && 'top-1/2 right-full -mr-1 -translate-y-1/2'
            )}
          />
        </div>
      )}
    </div>
  )
}
