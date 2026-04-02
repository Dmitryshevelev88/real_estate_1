"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { logout } from "@/components/auth";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  const linkClass = (href: string) =>
    `rounded-md px-3 py-2 text-sm ${
      pathname === href
        ? "bg-black text-white"
        : "text-slate-700 hover:bg-slate-100"
    }`;

  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between p-4">
        <div className="font-semibold">Оценка недвижимости</div>

        <nav className="flex items-center gap-2">
          <Link href="/properties" className={linkClass("/properties")}>
            Объекты
          </Link>

          <Link href="/assessments" className={linkClass("/assessments")}>
            Оценки
          </Link>

          <button
            onClick={handleLogout}
            className="rounded-md border px-3 py-2 text-sm hover:bg-slate-50"
          >
            Выйти
          </button>
        </nav>
      </div>
    </header>
  );
}