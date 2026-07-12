FROM python:3.12.0-slim

# Устанавливаем netcat для проверки БД в entrypoint
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install poetry

WORKDIR /app

# Копируем только зависимости для кеширования
COPY services/django_core/pyproject.toml services/django_core/poetry.lock /app/

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root


# Копируем исходный код
COPY services/django_core/src /app/src

# Копируем локальную библиотеку логирования
COPY infra/logging ./infra/logging

# ⚠️ КОСТЫЛЬ: устанавливаем библиотеку через pip (Poetry не справился)
RUN pip install -e ./infra/logging

# КОПИРУЕМ ENTRYPOINT ИЗ КОРНЯ (добавь это!)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

# Открываем порт
EXPOSE 8001

# Entrypoint в docker compose