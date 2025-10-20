FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY app ./app

EXPOSE 9000

CMD ["uvicorn", "app.mock_payments:app", "--host", "0.0.0.0", "--port", "9000", "--loop", "asyncio"]
