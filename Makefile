.PHONY: help setup run run-warehouse run-all test up down clean

SCRIPTS_DIR := scripts

help:
	sh $(SCRIPTS_DIR)/help.sh

setup:
	sh $(SCRIPTS_DIR)/setup.sh

run:
	sh $(SCRIPTS_DIR)/run-app.sh

run-warehouse:
	uv run uvicorn warehouse_service.main:app --host 0.0.0.0 --port 8001 --reload

run-all:
	@echo "Запуск склада (фон)..."
	uv run uvicorn warehouse_service.main:app --host 0.0.0.0 --port 8001 &
	@echo "Запуск основного сервиса..."
	sh $(SCRIPTS_DIR)/run-app.sh

test:
	sh $(SCRIPTS_DIR)/run-tests.sh

up:
	docker compose up --build -d

down:
	docker compose down -v

clean:
	rm -f autoservice.db warehouse.db
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
