import { Inter } from "next/font/google";
import { ThemeSwitcher } from "./components/ThemeSwitcher";
import { Flowbite } from "flowbite-react";
import type { Metadata } from "next";
import Header from "./components/layouts/Header";
import Footer from "./components/layouts/Footer";
import customTheme from "./flowBiteTheme";
import ToastComponent from "./components/ToastComponent";
import "./globals.css";
import "react-toastify/dist/ReactToastify.css";
import "react-loading-skeleton/dist/skeleton.css";
import Providers from "./Providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ToolShed",
  description: "The tool lending platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-slate-50 dark:bg-[#0d1117]`}>
        <Flowbite theme={{ theme: customTheme }}>
          <Providers attribute="class" defaultTheme="system" enableSystem>
            <Header />
            <ThemeSwitcher />
            <div className="flex min-h-screen flex-col items-center justify-between p-24 text-black dark:text-white">
              {children}
            </div>
            <ToastComponent />
            <Footer />
          </Providers>
        </Flowbite>
      </body>
    </html>
  );
}
