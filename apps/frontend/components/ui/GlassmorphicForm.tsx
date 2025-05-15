import { glassmorphism } from '@/lib/glassmorphism';
import { cn } from '@/lib/utils';
import { FormEvent, ReactNode } from 'react';

interface GlassmorphicFormProps {
  children: ReactNode;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  className?: string;
  title?: string;
  description?: string;
  footer?: ReactNode;
}

export function GlassmorphicForm({
  children,
  onSubmit,
  className,
  title,
  description,
  footer,
}: GlassmorphicFormProps) {
  return (
    <form
      onSubmit={onSubmit}
      className={cn(
        glassmorphism({ variant: 'medium', border: 'thin' }),
        'rounded-lg p-6 text-white',
        className
      )}
    >
      {(title || description) && (
        <div className="mb-6">
          {title && <h2 className="text-xl font-semibold text-primary-accent">{title}</h2>}
          {description && <p className="mt-1 text-sm text-white/70">{description}</p>}
        </div>
      )}

      <div className="space-y-4">{children}</div>

      {footer && <div className="mt-6 pt-4 border-t border-white/10">{footer}</div>}
    </form>
  );
}

interface FormFieldProps {
  children: ReactNode;
  label?: string;
  htmlFor?: string;
  error?: string;
  className?: string;
}

export function FormField({ children, label, htmlFor, error, className }: FormFieldProps) {
  return (
    <div className={cn('space-y-2', className)}>
      {label && (
        <label htmlFor={htmlFor} className="block text-sm font-medium text-white/80">
          {label}
        </label>
      )}
      {children}
      {error && <p className="text-xs text-tertiary-accent">{error}</p>}
    </div>
  );
}

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

export function FormInput({ className, error, ...props }: FormInputProps) {
  return (
    <input
      className={cn(
        'w-full px-3 py-2 bg-white/5 border border-white/10 rounded-md text-white',
        'placeholder:text-white/40',
        'focus:outline-none focus:ring-2 focus:ring-primary-accent/50 focus:border-primary-accent/50',
        error && 'border-tertiary-accent focus:ring-tertiary-accent/50 focus:border-tertiary-accent/50',
        className
      )}
      {...props}
    />
  );
}

interface FormSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  error?: boolean;
  options: { value: string; label: string }[];
}

export function FormSelect({ className, error, options, ...props }: FormSelectProps) {
  return (
    <select
      className={cn(
        'w-full px-3 py-2 bg-white/5 border border-white/10 rounded-md text-white',
        'focus:outline-none focus:ring-2 focus:ring-primary-accent/50 focus:border-primary-accent/50',
        error && 'border-tertiary-accent focus:ring-tertiary-accent/50 focus:border-tertiary-accent/50',
        className
      )}
      {...props}
    >
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

interface FormTextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: boolean;
}

export function FormTextarea({ className, error, ...props }: FormTextareaProps) {
  return (
    <textarea
      className={cn(
        'w-full px-3 py-2 bg-white/5 border border-white/10 rounded-md text-white',
        'placeholder:text-white/40',
        'focus:outline-none focus:ring-2 focus:ring-primary-accent/50 focus:border-primary-accent/50',
        error && 'border-tertiary-accent focus:ring-tertiary-accent/50 focus:border-tertiary-accent/50',
        className
      )}
      {...props}
    />
  );
}