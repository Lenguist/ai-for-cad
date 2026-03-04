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
    "The first open leaderboard comparing text-to-CAD models. Enter a prompt, compare outputs from 13+ models side by side, vote for the best result. Living leaderboard. Reproducible metrics.",
  openGraph: {
    title: "CAD Arena — Open Benchmark for AI-Generated Parametric CAD",
    description:
      "The first open leaderboard comparing text-to-CAD models side by side. Arena-style voting. 13+ models. Reproducible metrics.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "CAD Arena — Open Benchmark for AI-Generated Parametric CAD",
    description:
      "The first open leaderboard comparing text-to-CAD models side by side. 13+ models, arena-style voting, reproducible metrics.",
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
