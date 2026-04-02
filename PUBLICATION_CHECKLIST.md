# Public GitHub publication checklist

## 1. Cleanup before first public commit

Проверьте, что в репозитории отсутствуют:
- `.env`
- реальные пароли
- токены и API keys
- приватные сертификаты
- дампы БД
- чувствительные CSV и экспортированные данные
- локальные build-артефакты

Команды для быстрой проверки:

```bash
git status
git ls-files | grep -E '(^|/)(\.env|.*\.pem|.*\.key|.*\.p12|.*\.csv|.*\.sql|.*\.dump)$'
```

## 2. Verify git history

Если секреты уже были закоммичены раньше, простого удаления файла недостаточно. Нужно очищать историю отдельно.

Проверьте историю на чувствительные файлы:

```bash
git log --stat -- .env
git log --stat -- '*.csv'
git log --stat -- '*.sql'
```

## 3. Prepare public-facing metadata

Убедитесь, что есть:
- `README.md`
- `LICENSE`
- `.gitignore`
- `.env.example`

Опционально:
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `Makefile`

## 4. Initialize / verify remote

```bash
git remote -v
```

Если remote еще не настроен:

```bash
git init
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/real-estate-scoring-mvp.git
```

## 5. First public push

```bash
git add .
git commit -m "Initial public MVP release"
git push -u origin main
```

## 6. After push

Сразу проверьте:
- корректно ли отображается README
- нет ли секретов в файлах
- нет ли лишних данных в истории
- виден ли Swagger URL в документации
- можно ли поднять проект по инструкции из README

## 7. Good public repo hygiene

Рекомендуется:
- создать Issues / Project board
- описать roadmap
- добавить badges позже
- зафиксировать стабильные naming conventions
- держать migrations и schema changes синхронизированными
