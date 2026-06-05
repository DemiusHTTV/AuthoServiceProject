# Архитектура проекта AutoService

Проект построен по микросервисной архитектуре с вынесением общей бизнес-логики в отдельную библиотеку.

## C4 Model (Component Level)

```mermaid
graph TD
    Client[Клиент/Браузер] -->|HTTP 80| Nginx[Nginx Фронтенд]
    Nginx -->|JS fetch| Backend[FastAPI Основной Бэкенд :8000]
    
    subgraph "Узел Бэкенда"
        Backend --> DB_App[(SQLite: app.db)]
        Backend -.->|Импорт| Core[autoservice-core library]
    end
    
    subgraph "Узел Склада"
        Warehouse[FastAPI Склад :8001] --> DB_Wh[(SQLite: warehouse.db)]
    end
    
    Backend -->|HTTP REST| Warehouse
```

## Паттерны проектирования
1. **API Gateway (Частично)**: Роль маршрутизации запросов к сервисам берет на себя клиент (JS), но запросы к складу проксируются через основной Backend.
2. **Shared Library**: Пакет `autoservice_core` используется для разделения чистой бизнес-логики (расчет стоимости заказов) от транспортного слоя (FastAPI).
