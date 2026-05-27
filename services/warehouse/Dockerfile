FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi
COPY warehouse ./warehouse
RUN mkdir -p /app/data
EXPOSE 8001
CMD ["uvicorn", "warehouse.main:app", "--host", "0.0.0.0", "--port", "8001"]
