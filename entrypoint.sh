#!/bin/bash
set -e

# Проверяем, что сервис - это Django
if [ "$SERVICE" = "django" ]; then
    echo "⏳ Ожидание готовности базы данных..."
    while ! nc -z ${DB_HOST:-postgres} ${DB_PORT:-5432}; do
        sleep 1
    done
    echo "✅ База данных готова!"

    cd /app/src

    echo "🔄 Создание и применение миграций..."
    poetry run python manage.py makemigrations --noinput
    poetry run python manage.py migrate --noinput
    echo "✅ Миграции применены!"

    # Проверяем, была ли уже выполнена инициализация
    echo "🔍 Проверка инициализации данных..."
    INIT_FLAG=$(poetry run python manage.py shell -c "from django.core.cache import cache; print(cache.get('db_initialized', 'False'))" 2>/dev/null || echo "False")

    if [ "$INIT_FLAG" != "True" ]; then
        echo "📦 Первичная инициализация данных..."

        echo "👥 Создание ролей и суперпользователя..."
        poetry run python manage.py setup_admin_roles
        echo "✅ Суперпользователь и роли созданы!"

        echo "🚛 Заливка перевозчиков..."
        poetry run python manage.py load_carriers
        echo "✅ Заливка перевозчиков выполнена!"

        echo "📊 Заливка тарифов..."
        poetry run python manage.py load_tariffs
        echo "✅ Заливка тарифов выполнена!"

        echo "🔍 Индексация тарифов в Elasticsearch..."
        poetry run python manage.py index_tariffs
        echo "✅ Индексация выполнена!"

        # Устанавливаем флаг, что инициализация выполнена
        poetry run python manage.py shell -c "from django.core.cache import cache; cache.set('db_initialized', 'True', timeout=None)"
        echo "✅ Инициализация завершена!"
    else
        echo "⏭️ Данные уже инициализированы, пропускаем..."
    fi

    echo "🚀 Запуск Django сервера..."
    exec poetry run python manage.py runserver 0.0.0.0:8001
else
    # Для всех остальных сервисов просто запускаем команду
    exec "$@"
fi