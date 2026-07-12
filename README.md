Проект Умная логистическая платформа
http://127.0.0.1:8001/admin/login/?next=/admin/  админка джанго жасмин
http://localhost:5173/  сайт бот
http://127.0.0.1:8000/docs#/ swagger
http://localhost:3001/#/  react adminka
http://localhost:8081  - просмотр данных Редис
docker exec -it logistics_fastapi python -m pytest tests/ -v



Внедрена Lagraf - для умного диалонга с пользователями
Есть пре хук 
рафф mypy 
pipx install pre-commit
pre-commit --version

git init

Это единая цифровая система, которая автоматизирует все этапы 
работы с заказом — от заявки до доставки.

В классической логистике (как у вас):

Клиент создает заказ на перевозку

Указывает: что везти, откуда, куда, вес, габариты

Перевозчик берет этот заказ

Доставляет

Товар как сущность здесь — это просто описание груза, а не полноценный товар с ценой, остатками, категориями и т.д.

Система, которая берет на себя всю рутинную работу по организации 
грузоперевозок, позволяя менеджеру (вам!) тратить время только 
на принятие стратегических решений, а клиентам — получать прозрачный и быстрый сервис.

Сценарий работы:
1. Клиент создает заказ через веб-интерфейс или Telegram-бота:

text
Клиент: "Мне нужно доставить 500 кг автозапчастей из Берлина в Москву за 4 дня"
2. Система (через AI-агента) автоматически:

Проверяет наличие товара на складе

Рассчитывает стоимость (вес + габариты + расстояние + таможенные пошлины)

Находит свободный транспорт

Бронирует машину

Отправляет клиенту счет и договор

Создает заказ в системе

3. Водитель (через мобильное приложение):

Получает уведомление о новом заказе

Подтверждает загрузку

Периодически обновляет статус (в пути, на таможне, доставлен)

4. Клиент в реальном времени видит:
Где находится его груз
Ожидаемое время доставки
Получает уведомления о любых изменениях

5. Вы как менеджер:
Видите дашборд со всеми заказами
Получаете оповещения о проблемах (задержка, поломка)
Можете быстро принять решение (найти замену транспорта)
Генерируете отчеты по эффективности





План реализации:
1) Обдумывание архитектуры проекта и какие технологии будут применены
для каждого сервиса будут отдельные зависимости,
а не один общий на весь проект.


🔄 Полный цикл обработки заказа
1. Пользователь вводит запрос (Frontend)
Клиент пишет: "Перевези диван из Москвы в Питер, вес 50 кг, завтра"

Frontend отправляет это сообщение в FastAPI Agent

2. FastAPI Agent (AI сервис) - ваша задача:
🔍 Парсит сообщение (извлекает: груз, откуда, куда, вес, дату)

🧠 Анализирует контекст (понимает, что это заказ, а не вопрос)

📦 Обогащает данные (добавляет ID клиента, время запроса)

🚀 Отправляет структурированные данные в Django Core

3. Django Core (основное приложение) - ваша задача:
✅ Принимает структурированные данные от AI Agent

💾 Сохраняет заказ в БД (модель Order)

📧 Генерирует ответ (статус, номер заказа, цену)

📤 Отправляет результат обратно в FastAPI Agent

4. FastAPI Agent - ваша задача:
📝 Форматирует ответ в человеческий вид

📨 Отправляет обратно во Frontend

🔄 Обновляет статус заказа в Django (подтверждение, оплата и т.д.)

5. Frontend показывает пользователю:
✅ "Заказ принят! Номер: ORD-12345"

📋 Детали заказа

💰 Стоимость

🚛 Перевозчик

Frontend (React)
    ↓ (отправляет данные пользователя)
FastAPI Agent (AI сервис)
    ↓ (парсит, обрабатывает, обогащает)
Django Core (основное приложение)
    ↓ (сохраняет в БД, управляет заказами)
PostgreSQL (база данных)

Использована современная крутая библиотека для логирования json-logify

logistics_platform
- services/ Здесь будут все сервисы
- docker-compose.yml
- .env
- django_core/ - джанго
- - src/
- - - config/ 
- - - users/  Приложение клиенты
- - - orders/ Заказы
- fastapi_agent/
- - - main.py - ТОчка входа
- - - api/
- - - - get_info_frontend.py
- - - - text_parsing.py
- - - - orders.py POST - отправка запросов в ДЖанго
- - - - schemas.py здесь? 
- frontend
свое окружение поетри + Docker
- infra/
- - logging/
- - - pyproject.toml
- - - - src/
- - - - - config.py
- - - - - middleware.py
- - - - - utils.py
- react/flask_admin/  Админка + метрики
свое окружение поетри + Docker
- workers/    CELERY + Kafka
свое окружение поетри + Docker

в папке редис не нужен пайпроджект томл, так как это написано на языке C

3) Создание папок и окружения
mkdir -p services
poetry new django_core --name django_core   (poetry init это старый метод мы его не используем)
mkdir -p src


cd services/django-core
poetry add django djangorestframework django-cors-headers psycopg2-binary redis celery python-dotenv
cd services/django-core/src
poetry run django-admin startproject config .

cd src
poetry run python manage.py startapp users
poetry run python manage.py startapp orders

users и orders в INSTALLED_APPS
- не нужно активация окружения poetry env info, poetry shell/source /home/nastasiyaogokhiya/.cache/pypoetry/virtualenvs/logistics-platform-0O8KEvTd-py3.12/bin/activate


# Удалите старые миграции (если были)
rm -rf */migrations/__pycache__
rm -rf */migrations/0*.py

poetry add fastapi
poetry add --group dev uvicorn[standard]

poetry run uvicorn main:app --reload

3) Написание моделей, применение миграций
poetry run python manage.py makemigrations
poetry run python manage.py migrate

Установка библиотеки Pillow для поля avatar
Установка jazzmin для красивой админки

Настройка сеттингс AUTH_USER_MODEL, постресс, 
env файл библиотека python-dotenv




Создала сервис frontend REact внутри папки создать 
свое окружение
cd services/frontend
npm init -y   (это аналог pyproject toml)
npm install react react-dom
npm install -D vite @vitejs/plugin-react  # если будете использовать Vite для сборки  
npm install


Добавлена авториазция 
1) OAuth 2.1 + OpenID Connect (OIDC) — основа
OAuth 2.0 — это протокол авторизации (кто имеет доступ к чему). OpenID Connect — это надстройка над OAuth 2.0 для аутентификации (кто есть пользователь)
2) Короткоживущие access-токены + ротация refresh-токенов
Access token: 5–15 минут
Refresh token: одноразовый, при каждом обновлении выдаётся новый
3) PKCE (Proof Key for Code Exchange)
PKCE защищает от перехвата авторизационного кода в процессе обмена. В OAuth 2.1 его использование обязательно для всех клиентов
4) DPoP (Demonstration of Proof-of-Possession) — дополнительная защита
Это механизм, который привязывает токен к конкретному HTTP-запросу через криптографическую подпись. Даже если токен украден, злоумышленник не сможет его использовать с другого устройства.
5) Подпись JWT


Внедрение вышеперечисленного
poetry add djangorestframework-simplejwt
в settings добавили INSTALLED_APPS
REST_FRAMEWORK
SIMPLE_JWT
Добавлен в urls маршруты токенов
Добавлены вьхи
в env добавлены 
openssl ecparam -name prime256v1 -genkey -noout -out private.pem
openssl ec -in private.pem -pubout -out public.pem


8) Написание админки REACT admin чтобы проверить отображение моделей
и наглядно понять что мне нужно то
cd services
mkdir react-admin
cd react-admin
npm init -y
npm install react react-dom react-admin ra-data-simple-rest
создали vite.config.ts
создали tsconfig.json
создали tsconfig.node.json
создали index.html 
mkdir -p src
src/main.tsx
src/App.tsx
index
env
npm install -D vite @vitejs/plugin-react typescript @types/react @types/react-dom
добавили сервис в докеркомпос
http://localhost:3001



5) Настройка env
6) Настройка settings
7) Создание моделей данных 
















tree -I "__pycache__|*.pyc|*.pyo|.git|node_modules|.venv|media|static|__init__.py" -L 2


У меня вместо Makefile будет Just это более соврмененный аналог.
для установки   - это обязательно иначе у того кто 
будет разворачивать код не будут срабатывать команды
Нужна установка глобальная и он будет работать из любой папки
Linux (Ubuntu/Debian):

bash
sudo apt install just
macOS:

bash
brew install just
Windows:

bash
winget install Casey.Just
Cargo (если у вас установлен Rust):

bash
cargo install just



Бот (Telegram/Web) 
    ↓
FastAPI Agent (принимает запрос, валидирует)
    ↓
Django (получает запрос на заказ, бизнес-логика)
    ↓
Elasticsearch (поиск тарифов по индексу)
    ↓ (возвращает ID тарифов)
PostgreSQL (данные тарифов)
    ↓ (возвращает полные данные)
Elasticsearch → Django → FastAPI → Бот

