<p align="center">
  <img src="assets_readme/title.png" width="600" alt="Banner">
</p>

<h1 align="center" style="color: #3776AB; margin-top: 0px;">🚚 Logistics Platform</h1>
<p align="center" style="font-size: 16px; color: #666; margin-bottom: 20px;">
  Платформа для управления логистикой с AI-ассистентом
</p>

<p align="center">
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=F9DC24)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=FFD43B)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)](https://www.elastic.co/elasticsearch/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![React Admin](https://img.shields.io/badge/React_Admin-222222?style=for-the-badge&logo=react&logoColor=61DAFB)](https://marmelab.com/react-admin/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://docs.github.com/ru/actions)
[![Ruff](https://img.shields.io/badge/Ruff-000000?style=for-the-badge&logo=ruff&logoColor=white)](https://beta.ruff.rs/docs/)
[![MyPy](https://img.shields.io/badge/MyPy-1A1A1A?style=for-the-badge&logo=python&logoColor=white)](http://mypy-lang.org/)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-FAB040?style=for-the-badge&logo=pre-commit&logoColor=black)](https://pre-commit.com/)
[![Natasha](https://img.shields.io/badge/Natasha-4B0082?style=for-the-badge&logo=python&logoColor=white)](https://natasha.github.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/langgraph)
</p>




## ✨ Функционал

### 🤖 AI-Ассистент

- Обработка запросов на естественном языке (NER)
- Распознавание сущностей: города, даты, вес, тип груза
- Интеллектуальный поиск тарифов
- Оформление заказа в диалоговом режиме

### 📦 Логистика

- Поиск тарифов по маршруту и весу
- Фильтрация по типу груза и срочности
- Выбор перевозчика из нескольких вариантов
- Расчет стоимости и сроков доставки

### 🛠️ Администрирование

- Управление перевозчиками
- Создание и редактирование тарифов
- Управление заказами
- Административная панель (React Admin)

### 👤 Пользовательский функционал

- Регистрация и авторизация (JWT)
- Личный кабинет пользователя
- История заказов
- Статусы заказов

### 🔧 Технические возможности

- Автоматическое создание `.env` файла
- Автоматическая загрузка демо-данных
- Логирование всех запросов
- Проверка кода (ruff, mypy)

## 🖥 Интерфейс

<p align="center">
  <img src="assets_readme/actions.gif" width="800" alt="Работа на сайте">
</p>

<br>

---

---

## 🚀 Требования к запуску приложения через **Docker**

### 📦 Требования

Проверьте версии инструментов:

```bash
docker --version
docker compose version
```

### Приложение тестировалось на версиях:

Docker 29.1.5
Docker Compose 5.0.2

### Запуск проекта (ОДНА КОМАНДА!)

**Внимание! Команды just - из Justfile.**

1. Клонируем репозиторий

```bash
git clone 
cd logistics_platform

```

2. Запускаем проект (вручную ничего делать не нужно!)

```bash
just up
```

---

При выполнении команды just up автоматически:

- Создается .env файл с автогенерацией секретных ключей
- Создаются Docker образы всех сервисов
- Поднимается PostgreSQL и применяются миграции
- Запускается Redis (кэш + сессии)
- Запускается Elasticsearch (поиск тарифов)
- Запускается FastAPI (AI-агент)
- Запускается Django (бэкенд)
- Запускается Frontend (React + Vite)
- Загружаются демонстрационные данные (тарифы, перевозчики)
- Создается суперпользователь (admin/admin)

Доступные сервисы:
Сервис	URL	Назначение
🌐 Frontend	http://localhost:5173	Чат-интерфейс пользователя
🚀 FastAPI Docs	http://localhost:8000/docs	Документация API агента
🐍 Django Admin	http://localhost:8001/admin	Панель администратора
⚛️ React Admin	http://localhost:3001	Админ-панель логистики
📊 Redis Commander	http://localhost:8081	Управление Redis
📝 Swagger	http://localhost:8000/docs	OpenAPI документация
🔍 Elasticsearch  http://localhost:9200 Поисковый движок

👤 Доступ по умолчанию
Логин: admin
Пароль: admin

3. Чтобы остановить контейнер

```bash
just down
```

---

### Проверка работы приложения и ❗ Возможные проблемы

Если приложение не запускается, проверьте логи сервисов в реальном времени:

```bash
just logs
```

Предупреждение:
Убедитесь, что порты свободны:

- `5173` - Frontend
- `8000` - FastAPI
- `8001` - Django
- `3001` - React Admin
- `5432` - PostgreSQL
- `6378` - Redis Cache
- `6380` - Redis Storage
- `8081` - Redis Commander
- `9200` - Elasticsearch

Полная очистка и удаление
just clean-all

## Архитектура, слои проекта

Краткая структура проекта:

```text
 logistics_platform/
├── .github/                     # 🤖 CI/CD (GitHub Actions)
│   └── workflows/
│       └── ci.yml               # Автоматическая проверка при push
│
├── .pre-commit-config.yaml      # 🔒 Git хуки (проверка перед коммитом)
│
├── services/                    # Все сервисы
│   ├── fastapi_agent/          # 🤖 AI-агент (NER + диалоги)
│   │   ├── src/
│   │   │   ├── agents/         # Логика диалогов
│   │   │   ├── api/            # HTTP эндпоинты
│   │   │   ├── schemas/        # Pydantic схемы
│   │   │   ├── services/       # Бизнес-логика + NER
│   │   │   └── utils/          # Утилиты
│   │   └── Dockerfile
│   │
│   ├── django_core/            # 🐍 Бэкенд (тарифы, заказы, перевозчики, оплата, пользователи)
│   │   ├── src/
│   │   │   ├── carriers/       # Перевозчики
│   │   │   ├── orders/         # Заказы
│   │   │   ├── tariffs/        # Тарифы + Elasticsearch
│   │   │   ├── payments/       # Платежи
│   │   │   ├── users/          # Пользователи
│   │   │   └── config/         # Настройки Django
│   │   └── Dockerfile
│   │
│   ├── frontend/               # 💬 Чат-интерфейс (React + Vite)
│   │   ├── src/
│   │   │   ├── components/     # React компоненты
│   │   │   └── assets/         # Статика
│   │   └── Dockerfile
│   │
│   └── react-admin/            # ⚛️ Админ-панель (React Admin)
│       ├── src/
│       │   ├── authProvider.ts # Авторизация
│       │   └── dataProvider.ts # API клиент
│       └── package.json
│
├── infra/                      # 🔧 Инфраструктура
│   ├── logging/                # 📝 Логирование (общий пакет)
│   │   └── src/
│   │       └── infra_logging/  # Мидлвары для логов
│   └── redis/                  # 🗄️ Конфигурация Redis
│       ├── cache/              # Redis для кэширования
│       └── storage/            # Redis для сессий
│
├── docker-compose.yml          # 🐳 Оркестрация 9 сервисов
├── justfile                    # 📋 Команды для запуска
├── entrypoint.sh               # 🚀 Точка входа для контейнеров
├── .env.example                # 🔑 Шаблон переменных окружения
└── README.md                   # 📖 Документация проекта        
```

## 🛠 Технологии

### Backend

- **FastAPI** - AI-агент (обработка запросов, NER)
- **Django** - Основной бэкенд (API, админка)
- **PostgreSQL** - Основная база данных
- **Redis** - Кэширование и сессии
- **Elasticsearch** - Поиск тарифов

### AI

- **Natasha** - NER (извлечение сущностей)
- **pymystem3** - Морфологический анализ
- **LangGraph** - Управление диалогами

### Frontend

- **React + Vite** - Пользовательский интерфейс
- **React Admin** - Админ-панель

### DevOps

- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация
- **GitHub Actions** - CI/CD

### Качество кода

- **Ruff** - Линтер и форматтер
- **Mypy** - Проверка типов
- **Pre-commit** - Git хуки

---

👨‍💻 Автор
Anastasiya Gogokhiya
GitHub: @anastasiagogohiya

⭐ Благодарности
Natasha - NER библиотека
FastAPI - Современный веб-фреймворк
LangGraph - Управление диалогами
