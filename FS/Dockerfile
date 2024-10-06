FROM python:3.9-slim

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9090

CMD ["python", "app.py"]
