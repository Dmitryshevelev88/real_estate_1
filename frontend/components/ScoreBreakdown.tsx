type Score = {
  id: number;
  total_score: number;
  details_json?: {
    infrastructure_score?: number;
    lighting_score?: number;
    noise_score?: number;
    insolation_score?: number;
    development_score?: number;
  };
  calculation_version?: string;
  computed_at: string;
};

type Props = {
  score: Score | null;
};

export default function ScoreBreakdown({ score }: Props) {
  if (!score) {
    return (
      <div className="rounded-xl border p-4 bg-white">
        <h2 className="text-lg font-semibold">Результат расчёта</h2>
        <p className="mt-2 text-sm text-slate-500">Score ещё не рассчитан.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border p-4 bg-white">
      <h2 className="text-lg font-semibold">Результат расчёта</h2>

      <p className="mt-3 text-3xl font-bold">{score.total_score}</p>

      <div className="mt-4 space-y-1 text-sm text-slate-700">
        <p>Инфраструктура: {score.details_json?.infrastructure_score ?? "-"}</p>
        <p>Освещённость: {score.details_json?.lighting_score ?? "-"}</p>
        <p>Шум: {score.details_json?.noise_score ?? "-"}</p>
        <p>Инсоляция: {score.details_json?.insolation_score ?? "-"}</p>
        <p>Застройка: {score.details_json?.development_score ?? "-"}</p>
      </div>

      <div className="mt-4 text-xs text-slate-500 space-y-1">
        <p>Профиль: {score.calculation_version || "-"}</p>
        <p>Рассчитан: {score.computed_at}</p>
      </div>
    </div>
  );
}