"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createProperty } from "@/components/api";

export default function NewPropertyPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    title: "",
    address: "",
    description: "",
    city: "",
    property_type: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const created = await createProperty({
        title: form.title,
        address: form.address,
        description: form.description || undefined,
        city: form.city || undefined,
        property_type: form.property_type || undefined,
      });

      router.push(`/properties/${created.id}`);
    } catch (err: any) {
      setError(err.message || "Не удалось создать объект");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="mb-6 text-2xl font-bold">Новый объект</h1>

      <form onSubmit={handleSubmit} className="space-y-4 rounded-xl border p-4 bg-white">
        <div>
          <label className="block text-sm mb-1">Название</label>
          <input
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="w-full rounded-md border px-3 py-2"
            required
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Адрес</label>
          <input
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
            className="w-full rounded-md border px-3 py-2"
            required
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Описание</label>
          <textarea
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="w-full rounded-md border px-3 py-2"
            rows={4}
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Город</label>
          <input
            value={form.city}
            onChange={(e) => setForm({ ...form, city: e.target.value })}
            className="w-full rounded-md border px-3 py-2"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Тип объекта</label>
          <input
            value={form.property_type}
            onChange={(e) => setForm({ ...form, property_type: e.target.value })}
            className="w-full rounded-md border px-3 py-2"
          />
        </div>

        {error ? <p className="text-sm text-red-600">{error}</p> : null}

        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-black text-white px-4 py-2 disabled:opacity-50"
        >
          {loading ? "Создание..." : "Создать объект"}
        </button>
      </form>
    </main>
  );
}