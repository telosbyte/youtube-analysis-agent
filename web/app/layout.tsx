import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "YouTube Analysis - AI 기반 영상 분석",
  description: "Gemini와 Claude를 활용한 YouTube 영상 심층 분석 서비스",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
