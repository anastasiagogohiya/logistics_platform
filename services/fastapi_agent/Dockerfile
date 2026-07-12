FROM python:3.12.0-slim

# Устанавливаем Poetry
RUN pip install poetry

WORKDIR /app

# Копируем файлы зависимостей (пути от корня проекта)
COPY services/fastapi_agent/pyproject.toml services/fastapi_agent/poetry.lock* ./

# Копируем БИБЛИОТЕКУ в ту же папку, где лежит pyproject.toml
COPY infra/logging ./infra/logging

# КОСТЫЛЬ: устанавливаем библиотеку через pip (Poetry не справился)
RUN pip install -e ./infra/logging

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем исходный код
COPY services/fastapi_agent/src/ ./src/


# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

# Открываем порт
EXPOSE 8000

# Запускаем с --reload для разработки
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "port", "8000", "--reload"]