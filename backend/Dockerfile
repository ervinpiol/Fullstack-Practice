FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y

COPY --from=ghcr.io/astral-sh/uv:0.7.21 /uv /bin/uv

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml
ENV UV_HTTP_TIMEOUT=300
COPY . /app
RUN uv sync --no-dev

ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

