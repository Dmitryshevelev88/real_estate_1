# CSV Import Specification

## Назначение

Этот файл описывает формат CSV для импорта объектов каталога и аналитики в Sprint 2.

Импортируемые данные раскладываются в следующие таблицы:
- `catalog_properties`
- `property_analytics`
- `import_batches` — используется как журнал запуска импорта, а не как прямой target для колонок CSV

---

## Таблица соответствия колонок CSV

| CSV column | Required | Target table | Target field | Описание |
|---|---:|---|---|---|
| `external_id` | no | `catalog_properties` | `external_id` | Внешний идентификатор объекта. Предпочтительный ключ для upsert. |
| `display_name` | yes | `catalog_properties` | `display_name` | Отображаемое имя объекта в каталоге. |
| `address_full` | no | `catalog_properties` | `address_full` | Полный адрес объекта. Используется как fallback для сопоставления. |
| `project_name` | no | `catalog_properties` | `project_name` | Название ЖК или проекта. |
| `city` | no | `catalog_properties` | `city` | Город объекта. |
| `property_type` | no | `catalog_properties` | `property_type` | Тип объекта, например `flat`, `apartment`, `house`. |
| `infrastructure` | yes | `property_analytics` | `infrastructure` | Оценка инфраструктуры, целое число в диапазоне `0..10`. |
| `lighting` | yes | `property_analytics` | `lighting` | Оценка освещенности, целое число в диапазоне `0..10`. |
| `noise` | yes | `property_analytics` | `noise` | Оценка шумовой среды, целое число в диапазоне `0..10`. |
| `insolation` | yes | `property_analytics` | `insolation` | Оценка инсоляции, целое число в диапазоне `0..10`. |
| `development` | yes | `property_analytics` | `development` | Оценка окружения/застройки, целое число в диапазоне `0..10`. |
| `version` | no | `property_analytics` | `version` | Версия аналитики. По умолчанию `1`. |
| `source_label` | no | `property_analytics` | `source_label` | Метка источника импорта, например имя файла или batch. |

---

## Обязательные поля

Для успешного импорта строка должна содержать:
- `display_name`
- `infrastructure`
- `lighting`
- `noise`
- `insolation`
- `development`

`external_id` не обязателен, но рекомендуется.

---

## Правила upsert для `catalog_properties`

### Приоритет сопоставления
1. Если заполнен `external_id`, объект ищется по `external_id`.
2. Если `external_id` отсутствует, используется fallback:
   - `display_name + address_full`

### Поведение
- если объект найден — запись в `catalog_properties` обновляется;
- если объект не найден — создается новая запись;
- при повторном импорте не должны создаваться дубликаты одного и того же объекта.

---

## Правила записи в `property_analytics`

Для каждой валидной строки CSV создается или обновляется аналитика объекта.

### Versioning
- новая импортированная аналитика создает новую версию записи;
- новая версия становится актуальной;
- предыдущие опубликованные версии переводятся в `is_published = false`;
- публичные endpoints (`/analytics`, `/evaluation`) должны использовать **последнюю опубликованную** запись.

---

## Правила валидации метрик

Поля:
- `infrastructure`
- `lighting`
- `noise`
- `insolation`
- `development`

должны:
- быть числовыми;
- быть целыми числами;
- попадать в диапазон `0..10`.

Если строка не проходит валидацию:
- она не должна валить весь импорт;
- ошибка должна быть записана в результат обработки batch;
- `import_batches.rows_failed` должен увеличиваться.

---

## Использование `import_batches`

CSV не маппится напрямую в поля `import_batches`, но каждый запуск импорта должен создавать запись batch со следующей информацией:
- `filename`
- `source_type = csv`
- `status`
- `rows_total`
- `rows_created`
- `rows_updated`
- `rows_failed`
- `error_message` при необходимости

### Жизненный цикл batch
- `pending`
- `processing`
- `done`
- `failed`

---

## Пример CSV

```csv
external_id,display_name,address_full,project_name,city,property_type,infrastructure,lighting,noise,insolation,development,version,source_label
ext-1,"ЖК Солнечный, кв 1","Москва, ул. Примерная, 1","ЖК Солнечный","Москва",flat,8,7,6,9,7,1,"test import"
ext-2,"ЖК Речной, кв 2","Москва, ул. Речная, 2","ЖК Речной","Москва",flat,6,8,7,8,6,1,"test import"
```

---

## Минимальный результат успешного импорта

После обработки CSV должно быть обеспечено:
- запись или обновление объекта в `catalog_properties`;
- создание новой версии аналитики в `property_analytics`;
- корректное обновление counters и статуса в `import_batches`.
