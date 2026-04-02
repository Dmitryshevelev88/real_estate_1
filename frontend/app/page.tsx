export default function HomePage() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-semibold">MVP сервиса оценки недвижимости</h1>
      <p className="max-w-3xl text-slate-600">
        Local-first, cloud-ready заготовка: FastAPI + PostgreSQL + Alembic + Next.js + Tailwind.
      </p>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border bg-white p-5">
          <h2 className="font-medium">1. Аутентификация</h2>
          <p className="mt-2 text-sm text-slate-600">Регистрация и логин через JWT.</p>
        </div>
        <div className="rounded-xl border bg-white p-5">
          <h2 className="font-medium">2. Объекты</h2>
          <p className="mt-2 text-sm text-slate-600">Создание и просмотр объектов недвижимости.</p>
        </div>
        <div className="rounded-xl border bg-white p-5">
          <h2 className="font-medium">3. Оценки</h2>
          <p className="mt-2 text-sm text-slate-600">Ручные критерии и отдельный расчетный score.</p>
        </div>
      </div>
    </div>
  )
}
