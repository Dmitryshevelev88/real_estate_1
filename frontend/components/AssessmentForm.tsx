"use client";

import { useState } from "react";

type Props = {
  onSubmit: (payload: {
    infrastructure: number;
    lighting: number;
    noise: number;
    insolation: number;
    development: number;
    notes?: string;
  }) => Promise<void>;
};

export default function AssessmentForm({ onSubmit }: Props) {
  const [form, setForm] = useState({
    infrastructure: 5,
    lighting: 5,
    noise: 5,
    insolation: 5,
    development: 5,
    notes: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await onSubmit({
        infrastructure: Number(form.infrastructure),
        lighting: Number(form.lighting),
        noise: Number(form.noise),
        insolation: Number(form.insolation),
        development: Number(form.development),
        notes: form.notes || undefined,
      });

      setForm({
        infrastructure: 5,
        lighting: 5,
        noise: 5,
        insolation: 5,
        development: 5,
        notes: "",
      });
    } catch (err: any) {
      setError(err.message || "Не удалось сохранить оценку");
    } finally {
      setLoading(false);
    }
  }

  const fields = [
    { key: "infrastructure", label: "Инфраструктура" },
    { key: "lighting", label: "Освещённость" },
    { key: "noise", label: "Шум" },
    { key: "insolation", label: "Инсоляция" },
    { key: "development", label: "Застройка" },
  ] as const;

  return (
    <form onSubmit={handleSubmit} className="rounded-xl border p-4 space-y-4 bg-white">
      <h2 className="text-lg font-semibold">Новая оценка</h2>

      {fields.map((field) => (
        <div key={field.key}>
          <label className="block text-sm mb-1">{field.label}</label>
          <input
            type="number"
            min={0}
            max={10}
            value={form[field.key]}
            onChange={(e) =>
              setForm((prev) => ({
                ...prev,
                [field.key]: Number(e.target.value),
              }))
            }
            className="w-full rounded-md border px-3 py-2"
          />
        </div>
      ))}

      <div>
        <label className="block text-sm mb-1">Комментарий</label>
        <textarea
          value={form.notes}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              notes: e.target.value,
            }))
          }
          className="w-full rounded-md border px-3 py-2"
          rows={4}
        />
      </div>

      {error ? <p className="text-sm text-red-600">{error}</p> : null}

      <button
        type="submit"
        disabled={loading}
        className="rounded-md bg-black text-white px-4 py-2 disabled:opacity-50"
      >
        {loading ? "Сохранение..." : "Сохранить оценку"}
      </button>
    </form>
  );
}