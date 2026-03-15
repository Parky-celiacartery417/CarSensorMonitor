import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CarSensor Monitor",
  description: "Japanese used car market monitoring dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  );
}
