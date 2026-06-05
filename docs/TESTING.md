# Тестирование

## Текущее состояние
В репозитории есть каталоги:
- `test/unit/`
- `test/smoke/`

Основные smoke- и unit-тесты уже приведены к текущим маршрутам, но тестовый набор всё ещё не завершён полностью.

Что остаётся проблемным:
- в `test/unit/` лежит посторонний workspace-файл, не относящийся к тестам
- покрытие ещё не закрывает все сценарии `admin` и `workers`

## Что сейчас имеет смысл проверять
- unit-логику библиотеки `autoservice_core`
- клиентские API: регистрация, логин, профиль, бонусы
- сценарии создания заявки и списания бонусов
- smoke-проверки основного сервиса и склада
- интеграцию основного сервиса со складом при запуске через Docker Compose

## Запуск тестов
Общий запуск:
```bash
uv run python -m pytest test/
```

Только unit-тесты библиотеки:
```bash
uv run python -m pytest test/unit/test_inventory.py
```

Быстрая проверка текущего актуального набора:
```bash
./.venv/bin/python -m pytest test/smoke/test_smoke_main.py test/smoke/test_whare_house.py test/unit/test_api.py test/unit/test_clients.py test/unit/test_bonus_payments.py test/unit/test_inventory.py
```

## Что стоит актуализировать дальше
- добавить тесты для `admin` и `workers`
- проверить начисление бонусов сотрудникам отдельным тестом
- удалить из `test/unit/` лишние не-тестовые файлы
