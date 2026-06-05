# Техническое описание: Микросервис склада (Warehouse)

## Запуск
```bash
uv run uvicorn warehouse.app.main:app --port 8001
```
Или через Docker:
```bash
docker-compose up warehouse
```

## Стек
- **Фреймворк:** FastAPI
- **БД:** SQLite (`warehouse/app/data/warehouse.db`)

## Зона ответственности
Это изолированный микросервис. Его единственная задача — хранить информацию о наличии запчастей (Parts).
Основной бэкенд общается с этим сервисом по HTTP (REST).
