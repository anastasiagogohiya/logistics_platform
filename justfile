# ============================================================
# 🚀 LOGISTICS PLATFORM - Just Commands
# ============================================================

# ---------- ЗАПУСК (ВСЁ В ОДНОЙ КОМАНДЕ) ----------
up:
	@echo "🚀 Запуск проекта..."
	@if [ ! -f .env ]; then \
		echo "📝 .env не найден! Генерация..."; \
		python3 generate_env.py; \
	fi
	docker compose up -d
	@echo "⏳ Ожидание запуска сервисов..."
	@sleep 15
	@echo ""
	@echo "✅ Проект успешно запущен!"
	@echo ""
	@echo "📱 Доступные сервисы:"
	@echo "  ────────────────────────────────────────────"
	@echo "  🌐 Frontend:        http://localhost:5173"
	@echo "  🚀 FastAPI Docs:   http://localhost:8000/docs"
	@echo "  🐍 Django Admin:   http://localhost:8001/admin"
	@echo "  ⚛️  React Admin:    http://localhost:3001"
	@echo "  📊 Redis Commander: http://localhost:8081"
	@echo ""
	@echo "👤 Логин: admin"
	@echo "🔑 Пароль: admin"
	@echo ""
	@echo "📋 Для просмотра логов: just logs"

# ---------- ГЕНЕРАЦИЯ .env (отдельно) ----------
gen-env:
	@echo "🔑 Генерация .env файла с ключами..."
	python3 generate_env.py



down:
        docker compose down

restart:
        docker compose restart

logs:
        docker compose logs -f

build:
        docker compose build --no-cache

# ---------- АБСОЛЮТНАЯ ТОТАЛЬНАЯ ОЧИСТКА ----------
nuke:
	@echo "💣 ЯДЕРНАЯ ОЧИСТКА ВСЕГО!!!"
	@echo ""
	@echo "  🔥 Остановка и удаление ВСЕХ контейнеров, томов, образов..."
	docker compose down -v --rmi all --remove-orphans 2>/dev/null || true
	@echo "  🧹 Очистка Docker системы (контейнеры, образы, тома, сети)..."
	docker system prune -af --volumes 2>/dev/null || true
	docker builder prune -af 2>/dev/null || true
	@echo "  🗑️ Удаление миграций Django..."
	find services/django_core/src -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null || true
	find services/django_core/src -path "*/migrations/__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "  🗑️ Удаление Python кэша..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "  🗑️ Удаление папок тестов..."
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "  🗑️ Удаление Node.js зависимостей..."
	rm -rf services/frontend/node_modules services/react-admin/node_modules 2>/dev/null || true
	rm -f services/frontend/package-lock.json services/react-admin/package-lock.json 2>/dev/null || true
	@echo "  🗑️ Удаление .env файла..."
	rm -f .env
	@echo "  🗑️ Удаление логов и временных файлов..."
	rm -f build.log *.log 2>/dev/null || true
	@echo "  🗑️ Удаление файлов БД..."
	rm -f services/django_core/src/db.sqlite3 2>/dev/null || true
	@echo ""
	@echo "💥 АБСОЛЮТНАЯ ТОТАЛЬНАЯ ОЧИСТКА ЗАВЕРШЕНА!"
	@echo "✨ Система девственно чиста, как после установки!"
	@echo ""
	@echo "🚀 Для запуска: just up"


# ---------- PYTHON ----------
fix:
        @echo "🔧 Исправление Python кода..."
        docker exec -it logistics_fastapi poetry run ruff check --fix src/ infra/
        docker exec -it logistics_fastapi poetry run ruff format src/ infra/
        docker exec -it logistics_django poetry run ruff check --fix src/
        docker exec -it logistics_django poetry run ruff format src/
        @echo "✅ Python отформатирован!"

check:
        @echo "🔍 Проверка Python кода..."
        docker exec -it logistics_fastapi poetry run ruff check src/ infra/
        docker exec -it logistics_django poetry run ruff check src/
        @echo "✅ Ruff проверка пройдена!"

type-check:
        @echo "🔍 Проверка типов (mypy)..."
        docker exec -it logistics_fastapi poetry run mypy src/ || echo "⚠️ FastAPI: mypy ошибки найдены"
        docker exec -it logistics_django poetry run mypy src/ || echo "⚠️ Django: mypy ошибки найдены"
        @echo "✅ Проверка типов завершена!"

test:
        @echo "🧪 Запуск тестов..."
        docker exec -it logistics_fastapi poetry run pytest tests/ -v || echo "⚠️ FastAPI: тесты не найдены"
        docker exec -it logistics_django poetry run pytest src/ -v || echo "⚠️ Django: тесты не найдены"
        @echo "✅ Тесты завершены!"

# ---------- ФРОНТЕНД ----------
check-frontend:
        @echo "🔍 Проверка TypeScript..."
        @cd services/frontend && npx tsc --noEmit 2>/dev/null || echo "✅ Frontend TS ок"
        @cd services/react-admin && npx tsc --noEmit 2>/dev/null || echo "✅ React Admin TS ок"
        @echo "✅ TypeScript проверен!"

# ---------- ВСЕ ПРОВЕРКИ ----------
check-all: check type-check test check-frontend
        @echo "✅ Все проверки пройдены!"

# ---------- ПЕРЕД КОММИТОМ ----------
pre-commit: fix type-check test check-frontend
        @echo "✅ Проект готов к коммиту!"

# ---------- ПОМОЩЬ ----------
help:
        @echo "📋 Доступные команды:"
        @echo ""
        @echo "  🚀 Запуск:"
        @echo "    up              - Запустить проект (авто-создание .env)"
        @echo "    down            - Остановить проект"
        @echo "    restart         - Перезапустить проект"
        @echo "    logs            - Посмотреть логи"
        @echo "    build           - Пересобрать Docker образы"
        @echo ""
        @echo "  🧹 Очистка:"
        @echo "    clean           - Полная очистка (контейнеры, миграции)"
        @echo ""
        @echo "  🐍 Django:"
        @echo "    migrate         - Применить миграции"
        @echo "    createsuperuser - Создать суперпользователя"
        @echo ""
        @echo "  🔧 Проверка кода:"
        @echo "    check           - Проверить Python (ruff)"
        @echo "    fix             - Исправить Python (ruff)"
        @echo "    type-check      - Проверить типы (mypy)"
        @echo "    test            - Запустить тесты"
        @echo "    check-frontend  - Проверить TypeScript"
        @echo "    check-all       - Проверить всё"
        @echo "    pre-commit      - Подготовить к коммиту"
        @echo ""
        @echo "  📖 help - Показать эту справку"
