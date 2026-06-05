# Описание API контрактов

Так как проект использует FastAPI, OpenAPI документация генерируется автоматически.

## Основной Бэкенд (Core API)
Доступна по адресу: http://localhost:8000/docs
- **`POST /api/users/login`** — Авторизация
- **`POST /api/orders/public`** — Создание заявки с сайта
- **`POST /api/orders/calculate`** — Расчет стоимости заказа (Склад + Core)

## Микросервис склада (Warehouse API)
Доступна по адресу: http://localhost:8001/docs
- **`GET /api/parts`** — Получить список доступных запчастей
- **`POST /api/parts`** — Добавить деталь на склад
