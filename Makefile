.PHONY: help setup run run-warehouse run-all test compose-up compose-down clean

help:
	@echo "Доступные команды:"
	@echo "  make setup          — установить зависимости"
	@echo "  make run            — запустить backend (порт 8000)"
	@echo "  make run-warehouse  — запустить склад (порт 8001)"
	@echo "  make run-all        — запустить оба сервиса"
	@echo "  make compose-up     — запуск через Docker Compose"
	@echo "  make compose-down   — остановить Docker Compose"
	@echo "  make clean          — удалить БД и кэш"

setup:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --port 8000

run-warehouse:
	uvicorn warehouse_service.main:app --reload --port 8001

run-all:
	@echo "Запуск склада (фон)..."
	uvicorn warehouse_service.main:app --port 8001 &
	@echo "Запуск основного сервиса..."
	uvicorn app.main:app --reload --port 8000

compose-up:
	docker compose up --build -d

compose-down:
	docker compose down -v

clean:
	rm -f autoservice.db warehouse.db
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
