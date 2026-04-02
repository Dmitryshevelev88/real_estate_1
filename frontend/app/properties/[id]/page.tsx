"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  getProperty,
  getAssessments,
  createAssessment,
  computeScore,
  getComputedScores,
} from "@/components/api";
import AssessmentForm from "@/components/AssessmentForm";
import ScoreBreakdown from "@/components/ScoreBreakdown";

export default function PropertyDetailsPage() {
  const params = useParams<{ id: string }>();
  const propertyId = params.id;

  const [property, setProperty] = useState<any>(null);
  const [assessments, setAssessments] = useState<any[]>([]);
  const [scores, setScores] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [computeLoading, setComputeLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadAll() {
    try {
      setLoading(true);
      setError("");

      const [propertyRes, assessmentsRes, scoresRes] = await Promise.all([
        getProperty(propertyId),
        getAssessments(propertyId),
        getComputedScores(propertyId),
      ]);

      setProperty(propertyRes);
      setAssessments(assessmentsRes);
      setScores(scoresRes);
    } catch (err: any) {
      setError(err.message || "Ошибка загрузки");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!propertyId) return;
    loadAll();
  }, [propertyId]);

  async function handleCreateAssessment(payload: any) {
    await createAssessment(propertyId, payload);
    await loadAll();
  }

  async function handleCompute() {
    try {
      setComputeLoading(true);
      await computeScore(propertyId);
      await loadAll();
    } catch (err: any) {
      setError(err.message || "Не удалось рассчитать score");
    } finally {
      setComputeLoading(false);
    }
  }

  if (loading) {
    return <main className="p-6">Загрузка...</main>;
  }

  if (error && !property) {
    return <main className="p-6 text-red-600">{error}</main>;
  }

  if (!property) {
    return <main className="p-6">Объект не найден.</main>;
  }

  const latestScore = scores[0] || null;

  return (
    <main className="mx-auto max-w-6xl p-6 space-y-6">
      <div className="rounded-xl border p-4 bg-white">
        <h1 className="text-2xl font-bold">{property.title}</h1>
        <p className="mt-2 text-slate-700">{property.address}</p>
        {property.description ? (
          <p className="mt-3 text-slate-600">{property.description}</p>
        ) : null}
        <p className="mt-3 text-sm text-slate-500">
          {property.city || "—"} / {property.property_type || "—"}
        </p>
      </div>

      {error ? <p className="text-red-600">{error}</p> : null}

      <div className="grid gap-6 md:grid-cols-2">
        <AssessmentForm onSubmit={handleCreateAssessment} />

        <div className="space-y-4">
          <div className="rounded-xl border p-4 bg-white">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Оценки</h2>
              <button
                onClick={handleCompute}
                disabled={computeLoading}
                className="rounded-md bg-blue-600 text-white px-4 py-2 disabled:opacity-50"
              >
                {computeLoading ? "Считаем..." : "Рассчитать score"}
              </button>
            </div>

            {assessments.length === 0 ? (
              <p className="mt-3 text-sm text-slate-500">Оценок пока нет.</p>
            ) : (
              <div className="mt-4 space-y-3">
                {assessments.map((item) => (
                  <div key={item.id} className="rounded-lg border p-3 text-sm">
                    <p>Инфраструктура: {item.infrastructure}</p>
                    <p>Освещённость: {item.lighting}</p>
                    <p>Шум: {item.noise}</p>
                    <p>Инсоляция: {item.insolation}</p>
                    <p>Застройка: {item.development}</p>
                    {item.notes ? (
                      <p className="mt-2 text-slate-600">{item.notes}</p>
                    ) : null}
                    <p className="mt-2 text-xs text-slate-400">{item.created_at}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <ScoreBreakdown score={latestScore} />
        </div>
      </div>
    </main>
  );
}