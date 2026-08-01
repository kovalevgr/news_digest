# One image, run as web / bot / poller / migrate with different commands.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command; each compose service overrides it.
CMD ["uvicorn", "app.web:app", "--host", "0.0.0.0", "--port", "8000"]
