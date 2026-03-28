import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BrickGPT — AI LEGO Assembly Demo",
  description:
    "Describe a LEGO structure in plain English. BrickGPT plans, places, and validates the assembly in real time.",
  openGraph: {
    title: "BrickGPT — AI LEGO Assembly Demo",
    description: "Describe a LEGO structure. BrickGPT builds it.",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${geist.variable} ${geistMono.variable}`}>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
