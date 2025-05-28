FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync

COPY . .

EXPOSE 8000

CMD [ "uv", "run", "main.py" ]