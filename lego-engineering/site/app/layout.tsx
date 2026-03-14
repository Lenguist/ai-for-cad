import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Lego Engineering — Open Benchmark for AI-Generated Brick Assemblies",
  description:
    "The first open benchmark comparing AI models on LEGO and brick assembly generation. Reproduce academic results, test frontier models, track progress.",
  openGraph: {
    title: "Lego Engineering — Open Benchmark for AI-Generated Brick Assemblies",
    description: "Open benchmark comparing AI models on LEGO and brick assembly generation.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Lego Engineering — Open Benchmark for AI-Generated Brick Assemblies",
    description: "Open benchmark comparing AI models on LEGO and brick assembly generation.",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${geist.variable} ${geistMono.variable} font-[family-name:var(--font-geist)] antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
