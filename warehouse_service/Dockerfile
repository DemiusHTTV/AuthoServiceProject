FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
COPY lib/autoservice_core/ ./lib/autoservice_core/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e ./lib/autoservice_core
COPY warehouse_service/ ./warehouse_service/
COPY data/ ./data/
EXPOSE 8001
CMD ["uvicorn", "warehouse_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
