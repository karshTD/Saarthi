import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Saarthi — AI Volunteer Copilot",
  description:
    "Saarthi helps NGO volunteers turn limited prep time into personalized lessons for every child's level.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
