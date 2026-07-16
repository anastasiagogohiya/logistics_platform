FROM python:3.12-slim

WORKDIR /app

# Устанавливаем netcat для проверки подключения к БД
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.8.5
ENV POETRY_VIRTUALENVS_CREATE=false


# Отладочный вывод: проверяем, что файлы существуют
RUN echo "=== Checking files ===" && \
    ls -la /app/services/fastapi_agent/pyproject.toml 2>&1 || echo "File not found in /app/services/fastapi_agent/" && \
    ls -la services/fastapi_agent/pyproject.toml 2>&1 || echo "File not found in services/fastapi_agent/"


# Копируем pyproject.toml для fastapi (без poetry.lock)
COPY services/fastapi_agent/pyproject.toml ./
COPY infra/logging/pyproject.toml ./infra/logging/
COPY infra/logging/src ./infra/logging/src/


# Устанавливаем зависимости (Poetry сам создаст lock файл)
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем код
COPY services/fastapi_agent/src/ ./src/

# Копируем entrypoint и даем права на выполнение
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/app:/app/src
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
