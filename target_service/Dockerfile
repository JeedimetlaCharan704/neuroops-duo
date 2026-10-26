# Multi-stage ultra-lightweight Dockerfile for Google Cloud Run deployment
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final minimal production image
FROM python:3.12-slim AS runner

WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY target_service /app/target_service

# Run as non-root unprivileged container for security
RUN useradd -m -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "target_service.app:app", "--host", "0.0.0.0", "--port", "8080"]
