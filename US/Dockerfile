# US/Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Run the User Server
CMD ["python", "app.py"]
