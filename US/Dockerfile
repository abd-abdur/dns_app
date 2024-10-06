# US/Dockerfile

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose HTTP port 8080
EXPOSE 8080

# Run the User Server
CMD ["python", "app.py"]
