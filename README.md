# AutoService Project

Учебный проект сети автосервисов, реализованный в микросервисной архитектуре.

## Структура проекта
- `frontend/` — статика сайта (Nginx)
- `app/` — основной бэкенд (FastAPI, SQLite)
- `warehouse/` — микросервис склада (FastAPI, SQLite)
- `lib/autoservice_core/` — общая библиотека доменной логики
- `docs/` — техническая документация

## Быстрый запуск (через Docker)
```bash
docker-compose up --build
```

- **Frontend:** http://localhost:80
- **Backend API:** http://localhost:8000
- **Warehouse API:** http://localhost:8001

Документацию по каждому сервису смотрите в папке `docs/`.
