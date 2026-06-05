# Архитектура проекта AutoService

Проект построен по микросервисной архитектуре с вынесением общей бизнес-логики в отдельную библиотеку.

## C4 Model (Component Level)

```mermaid
graph TD
    Client[Клиент/Браузер] -->|HTTP 80| Nginx[Nginx Фронтенд]
    Nginx -->|JS fetch| Backend[FastAPI Основной Бэкенд :8000]
    
    subgraph "Узел Бэкенда"
        Backend --> DB_App[(SQLite: autoservice.db)]
        Backend -.->|Импорт| Core[autoservice-core library]
    end
    
    subgraph "Узел Склада"
        Warehouse[FastAPI Склад :8001] --> DB_Wh[(SQLite: warehouse.db)]
    end
    
    Backend -->|HTTP REST| Warehouse
```

## Паттерны проектирования
1. **Backend-for-Frontend / Partial Gateway**: клиентский JS ходит в основной backend, а доступ к складу для UI организован через прокси-маршруты `/api/warehouse/*`.
2. **Shared Library**: пакет `autoservice_core` хранит общие доменные модели, расчёт стоимости деталей и расчёт бонусов сотрудников.
