SHELL := /bin/sh

SETUP_CMD ?= ./scripts/setup.sh
APP_CMD ?= ./scripts/run-app.sh
TEST_CMD ?= ./scripts/run-tests.sh
COMPOSE_UP_CMD ?= docker compose up --build --wait
COMPOSE_DOWN_CMD ?= docker compose down -v

.PHONY: help setup run test check compose-up compose-down

help:
	@printf '%s\n' \
		'setup              Настроить локальное окружение (uv sync)' \
		'run                Запустить основное приложение локально' \
		'test               Запустить все тесты' \
		'compose-up         Поднять все микросервисы в Docker' \
		'compose-down       Остановить Docker контейнеры' \
		'check              Прогнать все проверки (тесты)'

setup:
	$(SETUP_CMD)

run:
	$(APP_CMD)

test:
	$(TEST_CMD)

compose-up:
	$(COMPOSE_UP_CMD)

compose-down:
	$(COMPOSE_DOWN_CMD)

check: test
