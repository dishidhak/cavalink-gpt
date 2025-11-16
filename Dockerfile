# ========================================
#   CAVALINK-GPT DOCKERFILE
# ========================================

# 1) Base Python image
FROM python:3.11-slim

# 2) Set working directory inside container
WORKDIR /app

# 3) Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the entire project
COPY . .

# 5) Expose Flask port
EXPOSE 5000

# 6) Start the Flask server
CMD ["python3", "src/app.py"]

