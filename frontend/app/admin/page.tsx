'use client';

import { ChangeEvent, FormEvent, useEffect, useMemo, useState } from 'react';

type ImportBatch = {
  id: number;
  filename: string;
  source_type: string;
  status: string;
  rows_total: number;
  rows_created: number;
  rows_updated: number;
  rows_failed: number;
  created_at: string;
  updated_at: string;
  error_message: string | null;
};

type CatalogProperty = {
  id: number;
  external_id: string | null;
  display_name: string;
  address_full: string | null;
  project_name: string | null;
  city: string | null;
  street: string | null;
  house: string | null;
  building: string | null;
  property_type: string | null;
  status: string;
  latitude: number | null;
  longitude: number | null;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
};

type PropertyAnalytics = {
  id: number;
  catalog_property_id: number;
  infrastructure: number;
  lighting: number;
  noise: number;
  insolation: number;
  development: number;
  source_type: string;
  source_label: string | null;
  version: number;
  is_published: boolean;
  updated_at: string;
};

type UploadResult = {
  batch_id: number;
  status: string;
  rows_total: number;
  rows_created: number;
  rows_updated: number;
  rows_failed: number;
  errors: Array<{
    row_number: number;
    row_data: Record<string, unknown>;
    error: string;
  }>;
};

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, '') ||
  'http://localhost:8000/api/v1';

const inputClassName =
  'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-black';
const buttonClassName =
  'rounded-lg bg-black px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-50';
const secondaryButtonClassName =
  'rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-900';

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export default function AdminPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
  const [uploadLoading, setUploadLoading] = useState(false);

  const [batches, setBatches] = useState<ImportBatch[]>([]);
  const [batchesLoading, setBatchesLoading] = useState(false);

  const [search, setSearch] = useState('Солнечный');
  const [properties, setProperties] = useState<CatalogProperty[]>([]);
  const [propertiesLoading, setPropertiesLoading] = useState(false);

  const [selectedPropertyId, setSelectedPropertyId] = useState<number | null>(null);
  const [selectedProperty, setSelectedProperty] = useState<CatalogProperty | null>(null);
  const [analyticsHistory, setAnalyticsHistory] = useState<PropertyAnalytics[]>([]);
  const [detailsLoading, setDetailsLoading] = useState(false);

  const [propertyForm, setPropertyForm] = useState({
    project_name: '',
    status: '',
    is_active: true,
  });

  const [analyticsForm, setAnalyticsForm] = useState({
    analytics_id: '',
    source_label: '',
    is_published: false,
  });

  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');

  const selectedAnalytics = useMemo(
    () =>
      analyticsHistory.find(
        (item) => String(item.id) === analyticsForm.analytics_id
      ) || null,
    [analyticsHistory, analyticsForm.analytics_id]
  );

  async function loadBatches() {
    setBatchesLoading(true);
    setError('');
    try {
      const data = await fetchJson<ImportBatch[]>('/admin/import-batches');
      setBatches(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось загрузить batch list');
    } finally {
      setBatchesLoading(false);
    }
  }

  async function searchProperties() {
    setPropertiesLoading(true);
    setError('');
    try {
      const query = encodeURIComponent(search);
      const data = await fetchJson<CatalogProperty[]>(
        `/admin/catalog-properties?q=${query}`
      );
      setProperties(data);
      if (data.length > 0 && !selectedPropertyId) {
        setSelectedPropertyId(data[0].id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось выполнить поиск');
    } finally {
      setPropertiesLoading(false);
    }
  }

  async function loadPropertyDetails(propertyId: number) {
    setDetailsLoading(true);
    setError('');
    try {
      const [property, history] = await Promise.all([
        fetchJson<CatalogProperty>(`/admin/catalog-properties/${propertyId}`),
        fetchJson<PropertyAnalytics[]>(
          `/admin/catalog-properties/${propertyId}/analytics`
        ),
      ]);

      setSelectedProperty(property);
      setAnalyticsHistory(history);
      setPropertyForm({
        project_name: property.project_name || '',
        status: property.status || '',
        is_active: property.is_active,
      });

      const firstAnalytics = history[0];
      setAnalyticsForm({
        analytics_id: firstAnalytics ? String(firstAnalytics.id) : '',
        source_label: firstAnalytics?.source_label || '',
        is_published: firstAnalytics?.is_published || false,
      });
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Не удалось загрузить объект и аналитику'
      );
    } finally {
      setDetailsLoading(false);
    }
  }

  useEffect(() => {
    loadBatches();
  }, []);

  useEffect(() => {
    searchProperties();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selectedPropertyId) {
      loadPropertyDetails(selectedPropertyId);
    }
  }, [selectedPropertyId]);

  useEffect(() => {
    if (selectedAnalytics) {
      setAnalyticsForm({
        analytics_id: String(selectedAnalytics.id),
        source_label: selectedAnalytics.source_label || '',
        is_published: selectedAnalytics.is_published,
      });
    }
  }, [selectedAnalytics]);

  async function handleUpload(event: FormEvent) {
    event.preventDefault();
    if (!file) {
      setError('Выбери CSV файл');
      return;
    }

    setUploadLoading(true);
    setError('');
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE}/admin/import-batches/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = (await response.json()) as UploadResult;

      if (!response.ok) {
        throw new Error(JSON.stringify(data));
      }

      setUploadResult(data);
      setMessage('Импорт завершен');
      await loadBatches();
      await searchProperties();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка загрузки CSV');
    } finally {
      setUploadLoading(false);
    }
  }

  async function handlePropertyPatch(event: FormEvent) {
    event.preventDefault();
    if (!selectedPropertyId) return;

    setError('');
    setMessage('');

    try {
      const payload = {
        project_name: propertyForm.project_name,
        status: propertyForm.status,
        is_active: propertyForm.is_active,
      };

      const updated = await fetchJson<CatalogProperty>(
        `/admin/catalog-properties/${selectedPropertyId}`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload),
        }
      );

      setSelectedProperty(updated);
      setMessage('Объект обновлен');
      await searchProperties();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка обновления объекта');
    }
  }

  async function handleAnalyticsPatch(event: FormEvent) {
    event.preventDefault();
    if (!analyticsForm.analytics_id) return;

    setError('');
    setMessage('');

    try {
      await fetchJson<PropertyAnalytics>(
        `/admin/property-analytics/${analyticsForm.analytics_id}`,
        {
          method: 'PATCH',
          body: JSON.stringify({
            source_label: analyticsForm.source_label,
            is_published: analyticsForm.is_published,
          }),
        }
      );

      setMessage('Аналитика обновлена');
      if (selectedPropertyId) {
        await loadPropertyDetails(selectedPropertyId);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка обновления аналитики');
    }
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-6">
        <div>
          <h1 className="text-3xl font-semibold text-gray-900">
            Admin Sprint 2
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Тестовый фронт для CSV import, import batches, каталога и истории analytics.
          </p>
          <p className="mt-1 text-xs text-gray-500">API: {API_BASE}</p>
        </div>

        {message ? (
          <div className="rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-800">
            {message}
          </div>
        ) : null}

        {error ? (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        ) : null}

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-gray-200">
            <h2 className="text-lg font-semibold">Импорт CSV</h2>
            <form onSubmit={handleUpload} className="mt-4 space-y-4">
              <input
                type="file"
                accept=".csv"
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  setFile(e.target.files?.[0] || null)
                }
                className={inputClassName}
              />
              <button type="submit" className={buttonClassName} disabled={uploadLoading}>
                {uploadLoading ? 'Загружаем...' : 'Загрузить CSV'}
              </button>
            </form>

            {uploadResult ? (
              <div className="mt-4 rounded-xl bg-gray-50 p-4 text-sm text-gray-800">
                <div>batch_id: {uploadResult.batch_id}</div>
                <div>status: {uploadResult.status}</div>
                <div>rows_total: {uploadResult.rows_total}</div>
                <div>rows_created: {uploadResult.rows_created}</div>
                <div>rows_updated: {uploadResult.rows_updated}</div>
                <div>rows_failed: {uploadResult.rows_failed}</div>

                {uploadResult.errors.length > 0 ? (
                  <pre className="mt-3 overflow-auto rounded-lg bg-white p-3 text-xs">
                    {JSON.stringify(uploadResult.errors, null, 2)}
                  </pre>
                ) : null}
              </div>
            ) : null}
          </div>

          <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-gray-200">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-lg font-semibold">Import batches</h2>
              <button
                type="button"
                className={secondaryButtonClassName}
                onClick={loadBatches}
                disabled={batchesLoading}
              >
                Обновить
              </button>
            </div>

            <div className="mt-4 max-h-96 space-y-3 overflow-auto">
              {batches.map((batch) => (
                <div
                  key={batch.id}
                  className="rounded-xl border border-gray-200 p-4 text-sm"
                >
                  <div className="font-medium">
                    Batch #{batch.id} — {batch.filename}
                  </div>
                  <div className="mt-1 text-gray-600">
                    status={batch.status}, created={batch.rows_created}, updated=
                    {batch.rows_updated}, failed={batch.rows_failed}
                  </div>
                  <div className="mt-1 text-xs text-gray-500">
                    {new Date(batch.created_at).toLocaleString()}
                  </div>
                  {batch.error_message ? (
                    <div className="mt-2 text-xs text-red-600">
                      {batch.error_message}
                    </div>
                  ) : null}
                </div>
              ))}

              {batches.length === 0 && !batchesLoading ? (
                <div className="text-sm text-gray-500">Пока нет batch-ей</div>
              ) : null}
            </div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[360px_1fr]">
          <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-gray-200">
            <div className="flex items-center gap-2">
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Поиск по ЖК или адресу"
                className={inputClassName}
              />
              <button
                type="button"
                className={buttonClassName}
                onClick={searchProperties}
                disabled={propertiesLoading}
              >
                Найти
              </button>
            </div>

            <div className="mt-4 space-y-3">
              {properties.map((property) => (
                <button
                  key={property.id}
                  type="button"
                  onClick={() => setSelectedPropertyId(property.id)}
                  className={`w-full rounded-xl border p-4 text-left transition ${
                    selectedPropertyId === property.id
                      ? 'border-black bg-gray-50'
                      : 'border-gray-200 bg-white'
                  }`}
                >
                  <div className="font-medium">{property.display_name}</div>
                  <div className="mt-1 text-sm text-gray-600">
                    {property.address_full || 'Без адреса'}
                  </div>
                  <div className="mt-2 text-xs text-gray-500">
                    id={property.id}, status={property.status}
                  </div>
                </button>
              ))}

              {properties.length === 0 && !propertiesLoading ? (
                <div className="text-sm text-gray-500">Ничего не найдено</div>
              ) : null}
            </div>
          </div>

          <div className="space-y-6">
            <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-gray-200">
              <h2 className="text-lg font-semibold">Объект</h2>

              {selectedProperty ? (
                <form onSubmit={handlePropertyPatch} className="mt-4 grid gap-4 md:grid-cols-2">
                  <div className="md:col-span-2">
                    <label className="mb-1 block text-sm text-gray-600">Display name</label>
                    <input
                      value={selectedProperty.display_name}
                      disabled
                      className={`${inputClassName} bg-gray-100`}
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="mb-1 block text-sm text-gray-600">Project name</label>
                    <input
                      value={propertyForm.project_name}
                      onChange={(e) =>
                        setPropertyForm((prev) => ({
                          ...prev,
                          project_name: e.target.value,
                        }))
                      }
                      className={inputClassName}
                    />
                  </div>

                  <div>
                    <label className="mb-1 block text-sm text-gray-600">Status</label>
                    <input
                      value={propertyForm.status}
                      onChange={(e) =>
                        setPropertyForm((prev) => ({
                          ...prev,
                          status: e.target.value,
                        }))
                      }
                      className={inputClassName}
                    />
                  </div>

                  <label className="flex items-center gap-2 pt-7 text-sm text-gray-700">
                    <input
                      type="checkbox"
                      checked={propertyForm.is_active}
                      onChange={(e) =>
                        setPropertyForm((prev) => ({
                          ...prev,
                          is_active: e.target.checked,
                        }))
                      }
                    />
                    is_active
                  </label>

                  <div className="md:col-span-2">
                    <button type="submit" className={buttonClassName}>
                      Сохранить объект
                    </button>
                  </div>
                </form>
              ) : (
                <div className="mt-4 text-sm text-gray-500">
                  Выбери объект слева
                </div>
              )}
            </div>

            <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">История analytics</h2>
                {detailsLoading ? (
                  <span className="text-sm text-gray-500">Загрузка...</span>
                ) : null}
              </div>

              <div className="mt-4 grid gap-6 lg:grid-cols-[1fr_320px]">
                <div className="space-y-3">
                  {analyticsHistory.map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() =>
                        setAnalyticsForm({
                          analytics_id: String(item.id),
                          source_label: item.source_label || '',
                          is_published: item.is_published,
                        })
                      }
                      className={`w-full rounded-xl border p-4 text-left ${
                        String(item.id) === analyticsForm.analytics_id
                          ? 'border-black bg-gray-50'
                          : 'border-gray-200'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-3">
                        <div className="font-medium">
                          Version {item.version} #{item.id}
                        </div>
                        <div
                          className={`rounded-full px-2 py-1 text-xs ${
                            item.is_published
                              ? 'bg-green-100 text-green-700'
                              : 'bg-gray-100 text-gray-600'
                          }`}
                        >
                          {item.is_published ? 'published' : 'draft/old'}
                        </div>
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        infra={item.infrastructure}, lighting={item.lighting}, noise=
                        {item.noise}, insolation={item.insolation}, development=
                        {item.development}
                      </div>
                      <div className="mt-1 text-xs text-gray-500">
                        source_label={item.source_label || '—'}
                      </div>
                    </button>
                  ))}

                  {analyticsHistory.length === 0 ? (
                    <div className="text-sm text-gray-500">
                      Для объекта пока нет analytics
                    </div>
                  ) : null}
                </div>

                <form onSubmit={handleAnalyticsPatch} className="rounded-xl border border-gray-200 p-4">
                  <h3 className="text-base font-semibold">Редактировать analytics</h3>

                  <div className="mt-4">
                    <label className="mb-1 block text-sm text-gray-600">Analytics ID</label>
                    <select
                      value={analyticsForm.analytics_id}
                      onChange={(e) =>
                        setAnalyticsForm((prev) => ({
                          ...prev,
                          analytics_id: e.target.value,
                        }))
                      }
                      className={inputClassName}
                    >
                      <option value="">Выбери запись</option>
                      {analyticsHistory.map((item) => (
                        <option key={item.id} value={item.id}>
                          #{item.id} / version {item.version}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="mt-4">
                    <label className="mb-1 block text-sm text-gray-600">Source label</label>
                    <input
                      value={analyticsForm.source_label}
                      onChange={(e) =>
                        setAnalyticsForm((prev) => ({
                          ...prev,
                          source_label: e.target.value,
                        }))
                      }
                      className={inputClassName}
                    />
                  </div>

                  <label className="mt-4 flex items-center gap-2 text-sm text-gray-700">
                    <input
                      type="checkbox"
                      checked={analyticsForm.is_published}
                      onChange={(e) =>
                        setAnalyticsForm((prev) => ({
                          ...prev,
                          is_published: e.target.checked,
                        }))
                      }
                    />
                    is_published
                  </label>

                  <button
                    type="submit"
                    className="mt-4 w-full rounded-lg bg-black px-4 py-2 text-sm font-medium text-white"
                    disabled={!analyticsForm.analytics_id}
                  >
                    Сохранить analytics
                  </button>
                </form>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}