# Техническое описание: Основной Бэкенд (Core API)

## Запуск
```bash
uv run uvicorn app.main:app --reload
```
или через Docker:
```bash
docker-compose up backend
```
Доступен на порту `8000`.

## Стек технологий
- **Фреймворк:** FastAPI
- **ОРМ:** SQLAlchemy
- **БД:** SQLite (`app/data/autoservice.db`)
- **Пакетный менеджер:** `uv`

## Роутеры (`app/api/`)
- `/api/users/` — Авторизация и ЛК.
- `/api/orders/` — Работа с заявками. Метод `/calculate` вызывает библиотеку `autoservice-core` и делает HTTP-запрос к микросервису Склада.
- `/api/cars/`, `/api/services/` — CRUD операции.

## Особенности
Бэкенд использует библиотеку доменной логики `lib/autoservice_core`, подключенную через механизм workspaces в `uv`.
