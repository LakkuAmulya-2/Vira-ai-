import { ButtonHTMLAttributes, ReactNode } from 'react';
import { cn } from '@/lib/cn';

export function Button({ className, children, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { children: ReactNode }) {
  return (
    <button className={cn('inline-flex items-center justify-center rounded-full px-5 py-3 text-sm font-semibold transition hover:-translate-y-0.5 active:translate-y-0', className)} {...props}>
      {children}
    </button>
  );
}

export function Pill({ children, className }: { children: ReactNode; className?: string }) {
  return <span className={cn('inline-flex items-center rounded-full border border-black/10 bg-white/70 px-3 py-1 text-xs font-semibold text-black/65 backdrop-blur', className)}>{children}</span>;
}
