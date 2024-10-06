# FS/Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose HTTP port 9090
EXPOSE 9090

# Run the Fibonacci Server
CMD ["python", "app.py"]
