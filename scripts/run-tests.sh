#!/bin/sh
echo "=> Запуск тестов (smoke + unit)..."
uv run python -m pytest test/
