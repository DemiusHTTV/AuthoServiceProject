FROM python:3.11-slim

# Устанавливаем Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем код
COPY . .

# Запускаем
CMD ["uvicorn", "autoservices.main:app", "--host", "0.0.0.0", "--port", "8000"]