FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY device.py .
ENV CERT_DIR=/app/certs
CMD ["python", "device.py"]
