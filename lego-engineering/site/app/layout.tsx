import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MechE-Claude — AI LEGO Assembly Demo",
  description:
    "Describe a LEGO structure in plain English. MechE-Claude plans, places, and validates the assembly in real time.",
  openGraph: {
    title: "MechE-Claude — AI LEGO Assembly Demo",
    description: "Describe a LEGO structure. MechE-Claude builds it.",
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
