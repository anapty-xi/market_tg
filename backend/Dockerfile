FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libc6-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend/

ENTRYPOINT ["/backend/entrypoint.sh"]

HEALTHCHECK --interval=90s --timeout=5s --start-period=20s --start-interval=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://127.0.0.1:8000/health_check/').raise_for_status()" || exit 1

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]