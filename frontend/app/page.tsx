import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-10">
        <section className="rounded-3xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
          <div className="max-w-3xl">
            <p className="text-sm font-medium uppercase tracking-wide text-gray-500">
              MVP сервиса оценки недвижимости
            </p>
            <h1 className="mt-3 text-4xl font-semibold tracking-tight text-gray-900">
              Backend Sprint 2 готов к ручной проверке через UI
            </h1>
            <p className="mt-4 text-base leading-7 text-gray-600">
              Сейчас с фронта можно быстро проверить основные сценарии:
              импорт CSV, просмотр import batches, поиск объектов каталога,
              историю analytics и ручное обновление объекта или аналитики.
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              <Link
                href="/admin"
                className="rounded-xl bg-black px-5 py-3 text-sm font-medium text-white"
              >
                Открыть админку
              </Link>
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noreferrer"
                className="rounded-xl border border-gray-300 bg-white px-5 py-3 text-sm font-medium text-gray-900"
              >
                Открыть Swagger
              </a>
            </div>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Импорт CSV</h2>
            <p className="mt-2 text-sm leading-6 text-gray-600">
              Загрузка CSV через admin endpoint и проверка counters:
              created, updated, failed.
            </p>
            <p className="mt-4 text-xs text-gray-500">
              Проверяется в разделе Admin Sprint 2.
            </p>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Каталог объектов</h2>
            <p className="mt-2 text-sm leading-6 text-gray-600">
              Поиск по ЖК или адресу, просмотр карточки объекта и ручное
              редактирование полей объекта.
            </p>
            <p className="mt-4 text-xs text-gray-500">
              Используются admin catalog endpoints.
            </p>
          </div>

          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">История analytics</h2>
            <p className="mt-2 text-sm leading-6 text-gray-600">
              Просмотр версий аналитики, проверка published-версии и ручное
              обновление source label.
            </p>
            <p className="mt-4 text-xs text-gray-500">
              Нужна для проверки versioning после повторного импорта.
            </p>
          </div>
        </section>

        <section className="rounded-3xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
          <h2 className="text-2xl font-semibold text-gray-900">
            Что проверить руками
          </h2>

          <div className="mt-6 grid gap-6 md:grid-cols-2">
            <div>
              <h3 className="text-base font-semibold text-gray-900">
                Через фронт
              </h3>
              <ul className="mt-3 space-y-2 text-sm leading-6 text-gray-600">
                <li>Загрузить CSV в админке</li>
                <li>Убедиться, что import batch завершился со status=done</li>
                <li>Найти импортированный объект по названию ЖК</li>
                <li>Открыть историю analytics</li>
                <li>Изменить project_name или source_label и сохранить</li>
              </ul>
            </div>

            <div>
              <h3 className="text-base font-semibold text-gray-900">
                Через backend
              </h3>
              <ul className="mt-3 space-y-2 text-sm leading-6 text-gray-600">
                <li>Проверить public search</li>
                <li>Проверить /catalog-properties/{'{id}'}/analytics</li>
                <li>Проверить /catalog-properties/{'{id}'}/evaluation</li>
                <li>Повторно импортировать тот же CSV</li>
                <li>Убедиться, что rows_updated растет без дублей</li>
              </ul>
            </div>
          </div>

          <div className="mt-8 rounded-2xl bg-gray-50 p-5">
            <p className="text-sm text-gray-700">
              Основной экран для тестирования новых функций:
            </p>
            <Link
              href="/admin"
              className="mt-3 inline-flex rounded-xl bg-black px-5 py-3 text-sm font-medium text-white"
            >
              Перейти в /admin
            </Link>
          </div>
        </section>
      </div>
    </main>
  );
}