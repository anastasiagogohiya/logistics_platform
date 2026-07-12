#!/bin/bash
set -e

# Проверяем, что сервис - это Django
if [ "$SERVICE" = "django" ]; then
    echo "⏳ Ожидание готовности базы данных..."
    while ! nc -z ${DB_HOST:-postgres} ${DB_PORT:-5432}; do
        sleep 1
    done
    echo "✅ База данных готова!"

  # Ожидание Elasticsearch не нужно так как depends on

    cd /app/src

    echo "🔄 Создание и применение миграций..."
    poetry run python manage.py makemigrations --noinput
    poetry run python manage.py migrate --noinput
    echo "✅ Миграции применены!"

    echo "👥 Создание ролей и суперпользователя..."
    poetry run python manage.py setup_admin_roles
    echo "Суперпользователь и роли созданы!"

    echo "Заливка перевозчиков..."
    poetry run python manage.py load_carriers
    echo "Успешная заливка перевозчиков!"

    echo "Заливка тарифов..."
    poetry run python manage.py load_tariffs
    echo "Успешная заливка тарифов!"

    echo "Индексация тарифов в Elasticsearch..."
    poetry run python manage.py index_tariffs
    echo "Успешно!"


    echo "🚀 Запуск Django сервера..."
    exec "$@"
else
    # Для всех остальных сервисов просто запускаем команду
    exec "$@"
fi