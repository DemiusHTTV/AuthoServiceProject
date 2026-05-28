# AutoService — Автосервис

Учебный проект автоматизации деятельности автосервиса.  
**Стек:** FastAPI · SQLite · Vanilla JS · Docker Compose

---

## 🚀 Быстрый старт

### Локально (без Docker)

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Запустить микросервис склада (в отдельном терминале)
uvicorn warehouse_service.main:app --port 8001

# 3. Запустить основной сервис (раздаёт и фронтенд)
uvicorn app.main:app --reload --port 8000

# 4. Открыть http://localhost:8000
```

### Через Docker Compose

```bash
docker compose up --build -d
# Открыть http://localhost
```

### Через Makefile

```bash
make setup         # установить зависимости
make run-all       # запустить оба сервиса
make compose-up    # или через Docker
make help          # все команды
```

---

## 📁 Структура проекта

```
auto/
├── app/                      # Backend (FastAPI) — порт 8000
│   ├── main.py               # Точка входа
│   ├── config.py              # Конфигурация
│   ├── database.py            # SQLite + seed из CSV
│   ├── models.py              # Pydantic-модели
│   ├── Dockerfile
│   └── routers/               # API роутеры
│       ├── clients.py         # Клиенты: регистрация, логин, ЛК
│       ├── requests.py        # Заявки: CRUD
│       ├── admin.py           # Админ-панель
│       ├── workers.py         # Панель работника
│       └── warehouse.py       # Прокси к складу
├── warehouse_service/         # Микросервис склада — порт 8001
│   ├── main.py
│   └── Dockerfile
├── frontend/                  # Фронтенд (Vanilla JS)
│   ├── index.html             # Главная + ЛК (гамбургер)
│   ├── admin.html             # Админ-панель
│   ├── worker.html            # Панель работника
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── css/style.css
│   └── js/
│       ├── main.js            # Логика главной
│       ├── admin.js           # Логика админки
│       └── worker.js          # Логика работника
├── data/                      # CSV с начальными данными
│   ├── clients.csv            # 15 клиентов
│   ├── workers.csv            # 7 работников
│   ├── services.csv           # 8 услуг
│   ├── requests.csv           # 15 заявок
│   ├── specializations.csv    # 5 специализаций
│   ├── bonuses.csv            # Бонусы (3000 каждому)
│   ├── warehouse_parts.csv    # 20 деталей на складе
│   ├── request_assignments.csv
│   ├── parts_usage.csv
│   └── admin.csv              # Логин/пароль админа
├── docs/                      # Документация
│   ├── specification.md       # Спецификация + SQL запросы
│   ├── architecture.md        # Архитектура
│   └── diagrams/              # Mermaid-диаграммы
│       ├── idef0_context.mmd  # IDEF0 контекстная
│       ├── idef0_decomp.mmd   # IDEF0 декомпозиция
│       └── data_schema.mmd    # ER-схема
├── tests/                     # Тесты (placeholder)
├── scripts/                   # Скрипты автоматизации
├── docker-compose.yaml
├── Makefile
├── requirements.txt
└── README.md
```

---

## 🔑 Тестовые учётные записи

| Роль | Логин | Пароль |
|------|-------|--------|
| Админ | admin | admin123 |
| Работник | smirnov | worker123 |
| Клиент | ivanov@mail.ru | client123 |

---

## 📊 База данных

- **9 таблиц** с внешними ключами
- Данные загружаются из CSV при первом запуске
- Основная БД: `autoservice.db` (SQLite)
- БД склада: `warehouse.db` (SQLite, отдельный микросервис)

---

## 📋 SQL-запросы

Все SQL-запросы описаны в [docs/specification.md](docs/specification.md#7-sql-запросы):
- Простые, вычисляемые, с параметрами, JOIN, агрегатные
