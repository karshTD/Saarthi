export const metadata = {
  title: "Saarthi",
  description: "AI Volunteer Copilot",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
