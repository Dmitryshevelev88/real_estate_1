# Contributing

Спасибо за интерес к проекту.

## Scope

Сейчас проект находится в стадии MVP и развивается backend-first вокруг сервиса оценки недвижимости на основе каталога объектов и предрасчитанной аналитики.

Приоритетные направления:
- catalog-based valuation flow
- import pipeline для аналитики
- scoring logic
- API consistency
- подготовка к интеграциям с внешними площадками

## Development setup

1. Склонируйте репозиторий.
2. Создайте локальный `.env` на основе `.env.example`.
3. Поднимите проект через Docker Compose.
4. Примените миграции.
5. Проверьте Swagger и основные endpoint'ы.

Пример:

```bash
git clone https://github.com/YOUR_USERNAME/real-estate-scoring-mvp.git
cd real-estate-scoring-mvp
cp .env.example .env
docker compose up --build
```

## Branching

Рекомендуемый формат веток:
- `feature/...`
- `fix/...`
- `refactor/...`
- `docs/...`
- `chore/...`

Примеры:
- `feature/catalog-property-search`
- `fix/scoring-null-handling`
- `docs/public-readme`

## Commit style

Желателен понятный commit message в одном из форматов:

```text
feat: add catalog property search endpoint
fix: handle missing analytics values in scoring
refactor: split evaluation schemas
docs: update public setup instructions
chore: clean up docker config
```

## Pull requests

Перед открытием PR желательно:
- убедиться, что приложение запускается локально
- убедиться, что миграции согласованы с моделями
- проверить Swagger для измененных endpoint'ов
- описать, что именно меняется и зачем
- приложить примеры запросов/ответов, если меняется API

Минимальный шаблон PR description:

```md
## What changed
- ...

## Why
- ...

## How to test
- ...
```

## Code guidelines

Предпочтения для проекта:
- явные Pydantic schema для request/response
- тонкие API endpoints, логика в services
- предсказуемые имена моделей и таблиц
- совместимость с будущим расширением под внешние платформы
- минимизация жесткой связности между import, analytics и scoring

## API principles

При добавлении новых endpoint'ов важно сохранять:
- понятные REST path'ы
- стабильные response schema
- аккуратную обработку `404`, `400`, `422`
- возможность дальнейшего версионирования API

## Security

Пожалуйста, не коммитьте:
- `.env`
- реальные ключи и токены
- чувствительные CSV/экспорты
- локальные дампы БД

Если вы случайно закоммитили секрет, удалите его из истории репозитория перед публикацией.

## Roadmap-aware contributions

Особенно полезны изменения, которые помогают подготовить проект к:
- массовому импорту данных по объектам
- подключению геоаналитики
- AI-assisted valuation flows
- упаковке решения для маркетплейсов недвижимости
