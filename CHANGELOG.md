# Changelog

Все заметные изменения в проекте рекомендуется фиксировать в этом файле.

Формат вдохновлен Keep a Changelog, версия проекта может следовать SemVer по мере взросления продукта.

## [Unreleased]

### Added
- catalog-based valuation direction for Sprint 1
- models for `catalog_properties`, `property_analytics`, `import_batches`
- search and retrieval flow for catalog properties
- evaluation endpoint based on precomputed analytics

### Changed
- product flow shifted from manual property creation to catalog selection
- backend architecture is being prepared for external marketplace integrations

### Planned
- CSV import/admin editing workflow hardening
- analytics enrichment
- geospatial engine integration
- AI-agent assisted evaluation scenarios

## [0.1.0] - Initial MVP

### Added
- authentication flow
- properties CRUD for original MVP scenario
- assessments flow
- score computation foundation
- frontend application
- Docker / Compose setup
- Swagger documentation
- migrations and working backend environment
