# Stage 1: build dependencies in an isolated layer so they are cached separately
# from source code changes. Uses slim base to minimise image surface area.
FROM python:3.11-slim AS builder

WORKDIR /build

# System deps required by pdfplumber / pdfminer (libpoppler not needed for text extraction)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: lean runtime image — no build tools, no cache
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY main.py .
COPY app/ ./app/

# Non-root user for container security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
