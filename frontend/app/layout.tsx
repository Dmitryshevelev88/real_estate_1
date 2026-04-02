import './globals.css'
import Link from 'next/link'
import type { ReactNode } from 'react'

export const metadata = {
  title: 'Real Estate MVP',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <div className="min-h-screen">
          <header className="border-b bg-white">
            <div className="mx-auto flex max-w-6xl items-center gap-6 px-6 py-4">
              <Link href="/" className="font-semibold">Real Estate MVP</Link>
              <nav className="flex gap-4 text-sm text-slate-600">
                <Link href="/login">Логин</Link>
                <Link href="/properties">Объекты</Link>
                <Link href="/properties/new">Новый объект</Link>
                <Link href="/assessments">Оценки</Link>
              </nav>
            </div>
          </header>
          <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
        </div>
      </body>
    </html>
  )
}
