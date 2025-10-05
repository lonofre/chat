FROM python:3.13

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH" \
    CONNECTION_STRING="my connection string" \
    HUB="the hub"

WORKDIR /app

# Install Poetry 
RUN apt-get update && apt-get install -y curl build-essential git \
 && curl -sSL https://install.python-poetry.org | python3 - \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY python/message/ .

# Expose gRPC port
EXPOSE 50052

CMD ["python", "message_service.py"]
