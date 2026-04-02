"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getProperties } from "@/components/api";

type Property = {
  id: number;
  title: string;
  address: string;
  description?: string;
  city?: string;
  property_type?: string;
};

export default function PropertiesPage() {
  const [items, setItems] = useState<Property[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError("");
        const data = await getProperties();
        setItems(data);
      } catch (err: any) {
        setError(err.message || "Не удалось загрузить объекты");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return (
    <main className="mx-auto max-w-5xl p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Объекты</h1>
        <Link
          href="/properties/new"
          className="rounded-md bg-black px-4 py-2 text-white"
        >
          Создать объект
        </Link>
      </div>

      {loading && <p>Загрузка...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && !error && items.length === 0 && (
        <div className="rounded-xl border p-6 bg-white">
          <p className="text-slate-500">Объектов пока нет.</p>
        </div>
      )}

      <div className="grid gap-4">
        {items.map((item) => (
          <Link
            key={item.id}
            href={`/properties/${item.id}`}
            className="rounded-xl border p-4 bg-white hover:bg-slate-50"
          >
            <h2 className="text-lg font-semibold">{item.title}</h2>
            <p className="mt-1 text-sm text-slate-700">{item.address}</p>
            {item.description ? (
              <p className="mt-2 text-sm text-slate-600">{item.description}</p>
            ) : null}
            <p className="mt-2 text-xs text-slate-500">
              {item.city || "—"} / {item.property_type || "—"}
            </p>
          </Link>
        ))}
      </div>
    </main>
  );
}