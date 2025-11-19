FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY assets ./assets
COPY frontend ./frontend

EXPOSE 5000

CMD ["python", "src/app.py"]

