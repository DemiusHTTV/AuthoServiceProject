# API проекта

Проект использует FastAPI, поэтому полные схемы запросов и ответов доступны через OpenAPI:
- основной сервис: `http://localhost:8000/docs`
- складской сервис: `http://localhost:8001/docs`

## Основной сервис

### Клиенты
- `POST /api/clients/register` — регистрация клиента
- `POST /api/clients/login` — вход клиента
- `GET /api/clients/{client_id}` — профиль клиента, заявки и бонусы

### Заявки
- `POST /api/requests/` — создание новой заявки, в том числе со списанием бонусов
- `GET /api/requests/` — список всех заявок
- `GET /api/requests/{request_id}` — детали заявки и назначенные сотрудники

Пример важных полей для `POST /api/requests/`:
- `service_id` — выбранная услуга
- `client_id` — ID клиента, если пользователь авторизован
- `bonus_to_spend` — сколько бонусов списать при создании заявки

В ответе на создание заявки возвращаются:
- `estimated_price` — базовая стоимость услуги
- `bonus_spent` — фактически списанные бонусы
- `final_price` — остаток к оплате
- `bonus_balance` — обновлённый бонусный баланс клиента

### Публичные данные
- `GET /api/services` — список услуг

### Администратор
- `POST /api/admin/login` — вход администратора
- `GET /api/admin/requests` — список заявок для админ-панели
- `PUT /api/admin/requests/{request_id}/accept` — принять заявку
- `PUT /api/admin/requests/{request_id}/reject` — отклонить заявку
- `POST /api/admin/assign` — назначить сотрудника на заявку
- `GET /api/admin/workers` — список сотрудников
- `GET /api/admin/services` — список услуг
- `GET /api/admin/stats` — агрегированная статистика

### Сотрудники
- `POST /api/workers/login` — вход сотрудника
- `GET /api/workers/{worker_id}/tasks` — список назначенных задач
- `PUT /api/workers/tasks/{assignment_id}/status` — смена статуса задачи

### Прокси к складу
Основной сервис проксирует часть запросов к складскому сервису:
- `GET /api/warehouse/parts`
- `GET /api/warehouse/parts/{part_id}`
- `GET /api/warehouse/parts/search/{query}`

## Складской сервис
- `GET /api/parts` — получить все детали
- `GET /api/parts/{part_id}` — получить деталь по ID
- `GET /api/parts/search/{query}` — поиск по названию или артикулу
- `GET /api/parts/low-stock/{threshold}` — детали с остатком ниже порога
- `POST /api/calculate` — расчёт стоимости набора деталей по списку `items`
