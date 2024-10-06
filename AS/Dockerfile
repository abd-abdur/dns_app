# AS/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY as_server.py .
COPY records.json .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 53533/udp

CMD ["python", "as_server.py"]
