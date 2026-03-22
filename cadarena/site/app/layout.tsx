import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const geist = Geist({
  variable: "--font-geist",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CAD Arena — Open Benchmark for AI-Generated Parametric CAD",
  description:
    "The first open benchmark comparing text-to-CAD models. 20 curated prompts across 4 difficulty tiers. LLM baselines, academic models, and commercial tools — side by side.",
  openGraph: {
    title: "CAD Arena — Open Benchmark for AI-Generated Parametric CAD",
    description:
      "The first open benchmark comparing text-to-CAD models. 20 curated prompts across 4 difficulty tiers. LLM baselines, academic models, and commercial tools — side by side.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "CAD Arena — Open Benchmark for AI-Generated Parametric CAD",
    description:
      "The first open benchmark comparing text-to-CAD models. 20 curated prompts across 4 difficulty tiers. LLM baselines, academic models, and commercial tools — side by side.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geist.variable} ${geistMono.variable} font-[family-name:var(--font-geist)] antialiased`}
      >
        {children}
        <Analytics />
      </body>
    </html>
  );
}
