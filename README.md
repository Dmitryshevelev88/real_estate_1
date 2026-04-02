# Real Estate Scoring MVP

MVP backend-first сервиса оценки недвижимости.

Проект решает задачу выбора объекта из каталога с заранее подготовленной аналитикой и расчетом итогового score. Пользователь ищет объект по адресу или названию ЖК, выбирает его из каталога и получает параметры оценки и результат скоринга.

## Product scope

Текущий продуктовый фокус:
- поиск объекта по адресу или названию ЖК
- выбор объекта из каталога
- получение предрасчитанной аналитики
- получение итоговой оценки `score`
- backend-first архитектура для дальнейшего масштабирования

Планируемое развитие:
- импорт аналитики через CSV и админ-интерфейс
- подключение геодвижка
- AI-агент для интерпретации и обогащения данных
- упаковка как модуля для маркетплейсов недвижимости

## Current status

Уже работает:
- auth
- properties
- assessments
- compute score
- frontend
- Docker / Docker Compose
- Swagger / OpenAPI
- migrations

Новый Sprint 1:
- `catalog_properties`
- `property_analytics`
- `import_batches`
- поиск объекта через каталог вместо ручного создания

## Architecture

Предполагаемая структура backend:

```text
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
```

Ключевые сущности Sprint 1:
- `catalog_properties` — карточка объекта каталога
- `property_analytics` — предрасчитанная аналитика объекта
- `import_batches` — импорт данных и аудит загрузок

## Main API

Планируемые / доступные ручки каталога:

```text
GET /api/v1/catalog-properties/search?q=...
GET /api/v1/catalog-properties/{id}
GET /api/v1/catalog-properties/{id}/analytics
GET /api/v1/catalog-properties/{id}/evaluation
```

## Local run

### 1. Clone repository

```bash
git clone git@github.com:YOUR_USERNAME/real-estate-scoring-mvp.git
cd real-estate-scoring-mvp
```

### 2. Configure environment

Создайте локальный `.env` на основе `.env.example`.

```bash
cp .env.example .env
```

Заполните переменные окружения своими локальными значениями.

### 3. Start services

```bash
docker compose up --build
```

### 4. Run migrations

Команда зависит от вашей текущей конфигурации проекта. Например:

```bash
docker compose exec backend alembic upgrade head
```

### 5. Open API docs

Swagger обычно доступен по адресу:

```text
http://localhost:8000/docs
```

## Example environment

```env
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=change_me
SECRET_KEY=change_me
```

## Tech stack

Примерный стек проекта:
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker / Docker Compose
- React frontend

## Roadmap

### Sprint 1
- каталог объектов
- аналитика объекта
- поиск по каталогу
- endpoint оценки на базе аналитики

### Sprint 2
- импорт CSV
- admin tools
- валидация и журнал загрузок

### Sprint 3+
- геообогащение
- AI-agent layer
- partner-ready integration module

## Notes for public repository

Перед публикацией убедитесь, что в репозиторий не попали:
- `.env`
- реальные ключи и токены
- дампы БД
- чувствительные CSV
- приватные credentials

## License

Проект публикуется под лицензией MIT, если вы не замените ее на другую модель лицензирования.
