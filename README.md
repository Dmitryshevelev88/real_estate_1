# MVP сервиса оценки недвижимости

Local-first, cloud-ready прототип сервиса оценки недвижимости.

## Что внутри
- **backend**: FastAPI + SQLAlchemy 2.0 + Alembic + JWT auth
- **frontend**: Next.js + Tailwind CSS
- **db**: PostgreSQL
- **infra**: Docker Compose

## Запуск
```bash
docker compose up --build
```

После запуска:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

## MVP scope
Сущности:
- users
- properties
- assessments
- score_profiles
- computed_scores
- attachments (заготовка)

Оценочные критерии:
- infrastructure
- lighting
- noise
- insolation
- development

## Логика
- Пользователь вручную проводит геоаналитику.
- `assessments` хранят ручные оценки и комментарии.
- `computed_scores` хранят отдельный расчетный итог.
- `score_profiles` задают веса критериев.

## Первые шаги
1. Поднять проект через Docker Compose.
2. Создать пользователя через `/api/v1/auth/register`.
3. Войти через `/api/v1/auth/login`.
4. Создать property.
5. Создать assessment.
6. Вызвать пересчет score.

## Cloud-ready идеи
- stateless backend
- конфиг через env
- reverse proxy / managed DB можно добавить без переработки приложения
- storage для attachments можно заменить на S3-compatible
