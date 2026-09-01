import type { Metadata } from "next";
export const metadata: Metadata = { title: "Vira AI", description: "AI-native student decision operating system" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
