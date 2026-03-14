import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI for Engineering — Research Hub",
  description:
    "Open research hub tracking AI progress across engineering domains. Weekly digest, benchmark leaderboards, and deep research on AI for CAD, LEGO, and more.",
  openGraph: {
    title: "AI for Engineering — Research Hub",
    description: "Open research hub tracking AI progress across engineering domains.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AI for Engineering — Research Hub",
    description: "Open research hub tracking AI progress across engineering domains.",
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
