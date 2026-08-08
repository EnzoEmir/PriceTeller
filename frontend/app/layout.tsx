import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";
import Header from "@/components/header/Header";
import Footer from "@/components/footer/Footer";

const bodyFont = Inter({
  variable: "--font-body",
  subsets: ["latin"],
});

const displayFont = Space_Grotesk({
  variable: "--font-heading",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "PriceTeller — Monte e compare preços de PC",
    template: "%s — PriceTeller",
  },
  description: "Monte a configuração do seu PC e compare os preços das peças em tempo real.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body
        className={`${bodyFont.variable} ${displayFont.variable} flex min-h-screen flex-col antialiased`}
      >
        <Header />
        {/* Segura o footer no rodapé da viewport quando a página é curta. */}
        <div className="flex-1">{children}</div>
        <Footer />
      </body>
    </html>
  );
}
