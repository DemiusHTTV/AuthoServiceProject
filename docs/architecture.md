# Архитектура проекта «AutoService»

## Обзор

Проект использует микросервисную архитектуру из 3 компонентов:

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Frontend  │────▶│   Backend    │────▶│  Warehouse       │
│   (Nginx)   │     │   (FastAPI)  │     │  Microservice    │
│   :80       │     │   :8000      │     │  (FastAPI) :8001 │
└─────────────┘     └──────┬───────┘     └────────┬─────────┘
                           │                       │
                    ┌──────▼───────┐        ┌──────▼─────────┐
                    │ autoservice  │        │  warehouse.db  │
                    │    .db       │        │   (SQLite)     │
                    │  (SQLite)    │        └────────────────┘
                    └──────────────┘
```

## Компоненты

### 1. Frontend (Nginx)
- Раздаёт статические файлы (HTML, CSS, JS)
- Проксирует `/api/*` запросы на Backend
- Порт: 80

### 2. Backend (FastAPI)
- REST API для клиентов, админа, работников
- Управляет основной БД `autoservice.db`
- Проксирует запросы к складу
- Порт: 8000

### 3. Warehouse Microservice (FastAPI)
- Отдельный сервис для учёта запчастей
- Своя БД `warehouse.db`
- REST API для CRUD деталей
- Порт: 8001

## Стек технологий

| Компонент | Технология |
|-----------|-----------|
| Frontend | Vanilla JavaScript, HTML5, CSS3 |
| Backend | Python 3.12, FastAPI, Pydantic |
| Микросервис | Python 3.12, FastAPI |
| СУБД | SQLite (файловая) |
| Web-сервер | Nginx |
| Контейнеризация | Docker, Docker Compose |
| HTTP-клиент | httpx (для связи backend → warehouse) |

## API Endpoints

### Клиенты `/api/clients`
- `POST /register` — регистрация
- `POST /login` — вход
- `GET /{id}` — профиль + заявки + бонусы

### Заявки `/api/requests`
- `POST /` — создать заявку
- `GET /` — все заявки
- `GET /{id}` — детали заявки

### Админ `/api/admin`
- `POST /login` — вход
- `GET /requests` — все заявки
- `PUT /requests/{id}/accept` — принять
- `PUT /requests/{id}/reject` — отклонить
- `POST /assign` — назначить работника
- `GET /workers` — список работников
- `GET /stats` — статистика

### Работники `/api/workers`
- `POST /login` — вход
- `GET /{id}/tasks` — мои задачи
- `PUT /tasks/{id}/status` — сменить статус

### Склад `/api/warehouse`
- `GET /parts` — все детали
- `GET /parts/{id}` — деталь по ID
- `GET /parts/search/{query}` — поиск
