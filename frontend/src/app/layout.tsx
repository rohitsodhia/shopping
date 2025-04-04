import type { Metadata, Viewport } from "next";
import Header from "./Header";
import "./globals.css";

export const metadata: Metadata = {
    title: "Shopping",
};

export const viewport: Viewport = {
    width: "device-width",
    initialScale: 1.0,
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className="min-h-screen p-2">
                <div className=" ">
                    <Header />
                    {children}
                </div>
            </body>
        </html>
    );
}
