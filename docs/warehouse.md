# Складской сервис `warehouse_service/`

## Назначение
Отдельный FastAPI-сервис, который:
- хранит каталог запчастей
- отдаёт список, поиск и просмотр деталей
- рассчитывает стоимость набора деталей через `autoservice_core`

## Запуск
Локально:
```bash
uv run uvicorn warehouse_service.main:app --reload --port 8001
```

Через Docker:
```bash
docker-compose up warehouse
```

## Стек
- `FastAPI`
- встроенный `sqlite3`
- `autoservice_core` для расчёта стоимости

## Данные
- файл БД: `warehouse.db` в корне проекта
- исходные CSV: `data/warehouse_parts.csv`
- таблица `warehouse_parts` создаётся автоматически на старте

## Маршруты
- `GET /api/parts`
- `GET /api/parts/{part_id}`
- `GET /api/parts/search/{query}`
- `GET /api/parts/low-stock/{threshold}`
- `POST /api/calculate`

## Интеграция с основным сервисом
Основной backend использует `WAREHOUSE_URL` и обращается к складу по HTTP. Для фронтенда эти вызовы доступны через прокси-маршруты `/api/warehouse/*` основного сервиса.
