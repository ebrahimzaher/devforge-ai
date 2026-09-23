FROM python:3.12-slim AS builder

WORKDIR /build

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --prefix=/install --no-cache-dir --no-deps -e .

FROM python:3.12-slim

RUN useradd --create-home appuser

WORKDIR /app

COPY --from=builder /install /usr/local

COPY src/ ./src/

RUN mkdir -p /app/output && chown appuser:appuser /app/output

USER appuser

EXPOSE 8000

ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1

CMD ["python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
