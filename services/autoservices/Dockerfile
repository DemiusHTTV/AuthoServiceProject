FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi
COPY autoservices ./autoservices
RUN mkdir -p /app/data
EXPOSE 8000
CMD ["uvicorn", "autoservices.main:app", "--host", "0.0.0.0", "--port", "8000"]
