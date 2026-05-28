# Спецификация проекта «AutoService»

## 1. Описание целевой аудитории

### Кто пользуется системой

| Роль | Описание | Типовые задачи |
|------|----------|----------------|
| **Клиент** | Владелец автомобиля, обращающийся в автосервис | Подача заявки на обслуживание, просмотр статуса заявки, история обращений, бонусная программа |
| **Менеджер (Админ)** | Сотрудник автосервиса, управляющий заявками | Просмотр входящих заявок, принятие/отклонение, назначение мастеров, просмотр склада запчастей, статистика |
| **Мастер (Работник)** | Специалист, выполняющий ремонт | Просмотр назначенных задач, изменение статуса работ |

### Какие задачи решает БД

- Хранение данных клиентов и их обращений
- Учёт услуг и цен автосервиса
- Управление заявками (создание, статусы, назначения)
- Учёт работников и их специализаций
- Бонусная система для постоянных клиентов
- Складской учёт запчастей (отдельный микросервис)
- Отслеживание использования деталей в заявках

---

## 2. Существующие аналоги на рынке ПО

| Продукт | СУБД | Архитектура | Функциональные возможности |
|---------|------|-------------|---------------------------|
| **1С:Автосервис** | MS SQL / PostgreSQL | Клиент-сервер, толстый клиент | Полный учёт: заказ-наряды, склад, бухгалтерия, CRM |
| **AutoDealer** | MySQL | Веб-приложение (PHP) | Управление заявками, складом, клиентами, отчётность |
| **TurboService** | SQLite / PostgreSQL | Десктопное приложение | Запись клиентов, учёт работ, склад запчастей |
| **RemOnline** | PostgreSQL | SaaS (облачное решение) | CRM, управление заказами, склад, рассылки, аналитика |

### Наш проект

| Параметр | Значение |
|----------|----------|
| СУБД | SQLite (файловая, без сервера) |
| Архитектура | Микросервисная: FastAPI (backend) + FastAPI (warehouse) + Nginx (frontend) |
| Язык backend | Python 3.12 |
| Фронтенд | Vanilla JavaScript, HTML, CSS |
| Контейнеризация | Docker Compose (3 контейнера) |

---

## 3. Описание реализуемого процесса

Основной бизнес-процесс: **обработка заявки на обслуживание автомобиля**.

### Этапы:
1. Клиент заходит на сайт, выбирает услугу и подаёт заявку
2. Заявка попадает в систему со статусом «Новая»
3. Менеджер просматривает заявку и принимает или отклоняет её
4. При принятии менеджер назначает мастера (работника)
5. Мастер видит задачу в своей панели и меняет статус: Не начато → В работе → Выполнено
6. При необходимости менеджер запрашивает детали со склада (микросервис)
7. Когда все задания выполнены, заявка автоматически переходит в статус «Завершена»

### IDEF0 нотация

См. диаграммы в папке `docs/diagrams/`:
- `idef0_context.mmd` — контекстная диаграмма A-0
- `idef0_decomp.mmd` — декомпозиция A0

---

## 4. Схема данных

9 таблиц с взаимосвязями:

1. **specializations** — справочник специализаций работников
2. **services** — справочник услуг с ценами
3. **clients** — зарегистрированные клиенты
4. **workers** — работники автосервиса
5. **requests** — заявки на обслуживание
6. **request_assignments** — назначения работников на заявки
7. **bonuses** — начисление бонусов клиентам
8. **warehouse_parts** — детали на складе (отдельный микросервис)
9. **parts_usage** — использование деталей в заявках

ER-диаграмма: `docs/diagrams/data_schema.mmd`

---

## 5. Файл БД

- Основная БД: `autoservice.db` (SQLite, создаётся автоматически)
- БД склада: `warehouse.db` (SQLite, отдельный микросервис)
- Начальные данные: папка `data/*.csv`

---

## 7. SQL-запросы

### 7.1 Простой запрос — все заявки со статусом «В работе»
```sql
SELECT * FROM requests WHERE status = 'in_progress';
```

### 7.2 Простой запрос — все работники специализации «Моторист»
```sql
SELECT w.* FROM workers w
JOIN specializations sp ON w.specialization_id = sp.id
WHERE sp.name = 'Моторист';
```

### 7.3 Вычисляемый запрос — общая сумма услуг по каждому клиенту
```sql
SELECT r.client_name,
       COUNT(r.id) AS total_requests,
       SUM(s.base_price) AS total_sum
FROM requests r
JOIN services s ON r.service_id = s.id
GROUP BY r.client_name
ORDER BY total_sum DESC;
```

### 7.4 Вычисляемый запрос — количество заявок по статусам
```sql
SELECT status, COUNT(*) AS count
FROM requests
GROUP BY status
ORDER BY count DESC;
```

### 7.5 Запрос с параметром — заявки конкретного клиента
```sql
SELECT r.*, s.name AS service_name
FROM requests r
LEFT JOIN services s ON r.service_id = s.id
WHERE r.client_id = ?
ORDER BY r.created_at DESC;
```

### 7.6 Запрос с параметром — детали на складе с количеством меньше N
```sql
SELECT * FROM warehouse_parts
WHERE quantity < ?
ORDER BY quantity;
```

### 7.7 JOIN — заявки с именами клиентов и назначенными работниками
```sql
SELECT r.id, r.client_name, r.car_brand, r.car_model,
       s.name AS service_name, s.base_price,
       w.name AS worker_name, sp.name AS specialization,
       ra.status AS task_status
FROM requests r
LEFT JOIN services s ON r.service_id = s.id
LEFT JOIN request_assignments ra ON ra.request_id = r.id
LEFT JOIN workers w ON ra.worker_id = w.id
LEFT JOIN specializations sp ON w.specialization_id = sp.id
ORDER BY r.created_at DESC;
```

### 7.8 Агрегатный — топ-5 самых загруженных работников
```sql
SELECT w.name, sp.name AS specialization,
       COUNT(ra.id) AS total_tasks,
       SUM(CASE WHEN ra.status = 'done' THEN 1 ELSE 0 END) AS completed
FROM workers w
JOIN request_assignments ra ON ra.worker_id = w.id
LEFT JOIN specializations sp ON w.specialization_id = sp.id
GROUP BY w.id
ORDER BY total_tasks DESC
LIMIT 5;
```
