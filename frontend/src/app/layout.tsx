import "./styles.css";

export const metadata = {
  title: "Vira AI — Student Decision OS",
  description: "AI-native career, admissions and scholarship intelligence.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
