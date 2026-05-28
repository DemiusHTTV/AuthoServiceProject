#!/bin/bash
# Запуск обоих сервисов
echo "🏭 Запуск микросервиса склада (порт 8001)..."
uvicorn warehouse_service.main:app --port 8001 &
sleep 1
echo "🚗 Запуск основного сервиса (порт 8000)..."
uvicorn app.main:app --reload --port 8000
