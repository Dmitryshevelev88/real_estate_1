"use client";

import { useRouter } from "next/navigation";
import { logout } from "@/components/auth";

export default function LogoutButton() {
  const router = useRouter();

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  return (
    <button
      onClick={handleLogout}
      className="rounded-md border px-3 py-2 text-sm hover:bg-slate-50"
    >
      Выйти
    </button>
  );
}