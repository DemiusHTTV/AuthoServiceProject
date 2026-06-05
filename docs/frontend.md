# Фронтенд

## Назначение
Фронтенд представляет три пользовательских сценария:
- главная клиентская страница
- панель администратора
- панель сотрудника

## Запуск
```bash
docker-compose up frontend
```

Сервис поднимает Nginx на `80` порту и раздаёт файлы из `frontend/`.

## Стек
- HTML
- CSS
- Vanilla JS без фронтенд-фреймворков

## Основные файлы
- `frontend/index.html` — главная страница клиента
- `frontend/admin.html` — интерфейс администратора
- `frontend/worker.html` — интерфейс сотрудника
- `frontend/assets/` — локальные изображения для блока с мастерами
- `frontend/css/style.css` — общие стили
- `frontend/js/main.js` — клиентская логика
- `frontend/js/admin.js` — админская логика
- `frontend/js/worker.js` — логика сотрудника

## Какие API используются

### `main.js`
- `POST /api/clients/login`
- `POST /api/clients/register`
- `GET /api/services`
- `POST /api/requests/`
- `GET /api/clients/{client_id}`

### `admin.js`
- `POST /api/admin/login`
- `GET /api/admin/requests`
- `PUT /api/admin/requests/{request_id}/accept`
- `PUT /api/admin/requests/{request_id}/reject`
- `POST /api/admin/assign`
- `GET /api/admin/workers`
- `GET /api/admin/stats`
- `GET /api/requests/{request_id}`
- `GET /api/warehouse/parts`
- `GET /api/warehouse/parts/search/{query}`

### `worker.js`
- `POST /api/workers/login`
- `GET /api/workers/{worker_id}/tasks`
- `PUT /api/workers/tasks/{assignment_id}/status`

## Особенности
- `API` в скриптах задан как пустая строка, поэтому фронтенд ожидает same-origin запросы
- при запуске через Nginx фронтенд обращается к backend через общий origin
- при запуске через FastAPI статика может раздаваться напрямую основным сервисом
- изображения мастеров берутся из `frontend/assets/worker*.jpg`
- в форме заявки для авторизованного клиента доступен ползунок списания бонусов
- максимальное списание ограничено меньшим из двух значений: баланс клиента и базовая стоимость выбранной услуги
