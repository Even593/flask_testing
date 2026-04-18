FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

RUN mkdir -p /app/instance && \
    useradd --create-home appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "run.py"]
