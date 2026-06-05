FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
COPY lib/autoservice_core/ ./lib/autoservice_core/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e ./lib/autoservice_core
COPY app/ ./app/
COPY data/ ./data/
COPY frontend/ ./frontend/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
