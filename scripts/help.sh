#!/bin/sh

echo "Доступные команды:"
echo "  make setup          — установить зависимости"
echo "  make run            — запустить backend (порт 8000)"
echo "  make run-warehouse  — запустить склад (порт 8001)"
echo "  make run-all        — запустить оба сервиса"
echo "  make test           — запустить тесты"
echo "  make up             — запуск через Docker Compose"
echo "  make down           — остановить Docker Compose"
echo "  make clean          — удалить БД и кэш"
