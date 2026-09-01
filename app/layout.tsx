import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Vira AI — Your next step, made clear',
  description: 'AI-native career, college, scholarship and admissions guidance for students.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
