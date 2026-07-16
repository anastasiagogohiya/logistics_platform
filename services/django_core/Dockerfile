FROM python:3.12-slim

WORKDIR /app

# Устанавливаем netcat для проверки подключения к БД
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==1.8.5

# Копируем pyproject.toml
COPY services/django_core/pyproject.toml ./
COPY infra/logging/pyproject.toml ./infra/logging/
COPY infra/logging/src ./infra/logging/src/

# Устанавливаем зависимости (ВСЕ, включая dev)
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем исходный код
COPY services/django_core/src/ ./src/

# Копируем entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8001
ENTRYPOINT ["/entrypoint.sh"]
CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8001"]
