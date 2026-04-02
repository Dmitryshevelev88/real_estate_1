"use client";

import { useEffect, useState } from "react";
import { getProperties, getAssessments } from "@/components/api";

type Property = {
  id: number;
  title: string;
};

type Assessment = {
  id: number;
  property_id: number;
  infrastructure: number;
  lighting: number;
  noise: number;
  insolation: number;
  development: number;
  notes?: string;
  created_at: string;
};

export default function AssessmentsPage() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedPropertyId, setSelectedPropertyId] = useState<string>("");
  const [items, setItems] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProperties() {
      try {
        const data = await getProperties();
        setProperties(data);

        if (data.length > 0) {
          setSelectedPropertyId(String(data[0].id));
        }
      } catch (err: any) {
        setError(err.message || "Не удалось загрузить объекты");
      }
    }

    loadProperties();
  }, []);

  useEffect(() => {
    if (!selectedPropertyId) return;

    async function loadAssessments() {
      try {
        setLoading(true);
        setError("");
        const data = await getAssessments(selectedPropertyId);
        setItems(data);
      } catch (err: any) {
        setError(err.message || "Не удалось загрузить оценки");
      } finally {
        setLoading(false);
      }
    }

    loadAssessments();
  }, [selectedPropertyId]);

  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="mb-6 text-2xl font-bold">Оценки</h1>

      {properties.length > 0 && (
        <div className="mb-6">
          <label className="mb-1 block text-sm">Объект</label>
          <select
            value={selectedPropertyId}
            onChange={(e) => setSelectedPropertyId(e.target.value)}
            className="rounded-md border px-3 py-2"
          >
            {properties.map((property) => (
              <option key={property.id} value={property.id}>
                {property.title}
              </option>
            ))}
          </select>
        </div>
      )}

      {loading && <p>Загрузка...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && !error && items.length === 0 && (
        <div className="rounded-xl border p-4 bg-white">
          <p className="text-slate-500">Оценок пока нет.</p>
        </div>
      )}

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.id} className="rounded-xl border p-4 bg-white">
            <p>Инфраструктура: {item.infrastructure}</p>
            <p>Освещённость: {item.lighting}</p>
            <p>Шум: {item.noise}</p>
            <p>Инсоляция: {item.insolation}</p>
            <p>Застройка: {item.development}</p>
            {item.notes ? <p className="mt-2 text-slate-600">{item.notes}</p> : null}
            <p className="mt-2 text-xs text-slate-400">{item.created_at}</p>
          </div>
        ))}
      </div>
    </main>
  );
}