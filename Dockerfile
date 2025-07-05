# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but good for building some packages)
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get clean

# Copy application code
COPY ./app /app/app
COPY ./app/main.py /app/main.py
COPY .env /app/.env
COPY requirements.txt /app/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
