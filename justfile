
up:
	docker compose up -d

down:
	docker compose down

delete:
    docker compose down -v

delete_all:
	@echo "🧹 Очистка Docker контейнеров, томов и образов..."
	docker compose down -v --rmi all --remove-orphans
	docker system prune -af --volumes
	docker builder prune -af

	@echo "🔓 Высвобождение портов..."
	sudo fuser -k 5432/tcp 2>/dev/null || true  # PostgreSQL
	sudo fuser -k 6379/tcp 2>/dev/null || true  # Redis Cache
	sudo fuser -k 6380/tcp 2>/dev/null || true  # Redis Storage
	sudo fuser -k 9200/tcp 2>/dev/null || true  # Elasticsearch
	sudo fuser -k 9300/tcp 2>/dev/null || true  # Elasticsearch
	sudo fuser -k 8000/tcp 2>/dev/null || true  # FastAPI
	sudo fuser -k 8001/tcp 2>/dev/null || true  # Django
	sudo fuser -k 5173/tcp 2>/dev/null || true  # Frontend

	@echo "🗑️ Удаление миграций..."
	# Удаляем только .py файлы (не трогаем __pycache__)
	find services/django_core/src -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null || true
	# Удаляем .pyc файлы
	find services/django_core/src -path "*/migrations/*.pyc" -delete 2>/dev/null || true
	# Удаляем папки __pycache__ в migrations
	find services/django_core/src -path "*/migrations/__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

	@echo "🗑️ Удаление SQLite..."
	rm -f services/django_core/src/db.sqlite3 2>/dev/null || true

	@echo "✅ Полная очистка завершена!"

logs:
    docker compose logs -f

django:
    cd services/django_core/src && \
    poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate && \
    poetry run python manage.py createsuperuser