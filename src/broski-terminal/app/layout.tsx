import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "HyperCode – Neurodivergent-First AI Coding Environment",
  description:
    "A neurodivergent-first IDE and agent swarm for ADHD, dyslexic, and autistic coders. HyperCode uses AI agents to plan, code, test, and deploy while you stay in hyperfocus.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
