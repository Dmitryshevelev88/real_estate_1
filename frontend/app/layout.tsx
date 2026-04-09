import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'Real Estate MVP',
  description: 'MVP сервиса оценки недвижимости',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <div className="min-h-screen">
          <header className="border-b border-gray-200 bg-white">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
              <Link href="/" className="text-lg font-semibold">
                Real Estate MVP
              </Link>

              <nav className="flex items-center gap-3 text-sm">
                <Link
                  href="/"
                  className="rounded-lg px-3 py-2 text-gray-700 hover:bg-gray-100"
                >
                  Главная
                </Link>
                <Link
                  href="/admin"
                  className="rounded-lg px-3 py-2 text-gray-700 hover:bg-gray-100"
                >
                  Админка
                </Link>
              </nav>
            </div>
          </header>

          <div>{children}</div>
        </div>
      </body>
    </html>
  );
}