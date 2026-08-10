# API Contract
## Logistics Platform — AI-ассистент для автоматизации логистических перевозок

---

| **Параметр** | **Значение** |
|--------------|--------------|
| **Документ** | API Contract |
| **Проект** | Logistics Platform |
| **Версия** | 2.0 |
| **Дата** | 30.07.2026 |
| **Автор** | Анастасия Гогохия |
| **Базовый URL** | `http://localhost:8000` |
| **Формат данных** | JSON |
| **Кодировка** | UTF-8 |
| **Авторизация** | JWT Bearer Token |

---

# Содержание

1. Общие принципы API
2. Аутентификация и авторизация
3. Эндпоинты по модулям
4. Общие структуры данных
5. Коды ошибок
6. Матрица покрытия требований

---

# 1. Общие принципы API

## 1.1. Формат запроса

Все запросы должны содержать заголовок:

```http
Content-Type: application/json
Authorization: Bearer <jwt_token>
```

## 1.2. Формат ответа

Успешный ответ:

```json
{
    "user": { ... },
    "users": [ ... ],
    "access": "...",
    "refresh": "..."
}
```

Ошибка (422 Validation Error):

```json
{
    "detail": [
        {
            "loc": ["body", "username"],
            "msg": "field required",
            "type": "missing"
        }
    ]
}
```

---

# 2. Аутентификация и авторизация

## 2.1. Регистрация пользователя

**POST** `/api/auth/register`

**Запрос:**

```json
{
    "username": "pipita",
    "email": "pipita@bk.ru",
    "password": "pipita123",
    "first_name": "Pipita",
    "last_name": "Ivanova",
    "phone": "89157655555"
}
```

| **Поле** | **Тип** | **Обязательное** | **Описание** | **Пример** |
|----------|---------|------------------|--------------|------------|
| username | string | ✅ Да | Имя пользователя | `"pipita"` |
| email | string | ❌ Нет | Email | `"pipita@bk.ru"` |
| password | string | ✅ Да | Пароль | `"pipita123"` |
| first_name | string | ✅ Да | Имя | `"Pipita"` |
| last_name | string | ✅ Да | Фамилия | `"Ivanova"` |
| phone | string | ✅ Да | Телефон | `"89157655555"` |
| avatar | string | ❌ Нет | Ссылка на аватар | `"https://example.com/avatar.jpg"` |

**Успешный ответ (200):**

```json
{
    "user": {
        "id": 1,
        "username": "pipita",
        "email": "pipita@bk.ru",
        "first_name": "Pipita",
        "last_name": "Ivanova",
        "phone": "89157655555",
        "avatar": null,
        "is_staff": null
    }
}
```

---

## 2.2. Получение токена (Login)

**POST** `/api/auth/token`

**Запрос:**

```json
{
    "username": "pipita",
    "password": "pipita123"
}
```

| **Поле** | **Тип** | **Обязательное** | **Описание** |
|----------|---------|------------------|--------------|
| username | string | ✅ Да | Имя пользователя |
| password | string | ✅ Да | Пароль |

**Успешный ответ (200):**

```json
{
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

# 3. Эндпоинты по модулям

## 3.1. Пользователи

### 3.1.1. Получение списка пользователей

**GET** `/api/users/list`

**Заголовки:** `Authorization: Bearer <access_token>`

**Успешный ответ (200):**

```json
{
    "users": [
        {
            "id": 1,
            "username": "pipita",
            "email": "pipita@bk.ru",
            "first_name": "Pipita",
            "last_name": "Ivanova",
            "phone": "89157655555",
            "avatar": null,
            "is_staff": null
        },
        {
            "id": 2,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "Adminov",
            "phone": "89001234567",
            "avatar": null,
            "is_staff": true
        }
    ]
}
```

---

### 3.1.2. Получение пользователя по ID

**GET** `/api/users/{id}`

**Заголовки:** `Authorization: Bearer <access_token>`

**Параметры пути:**

| **Параметр** | **Тип** | **Описание** |
|--------------|---------|--------------|
| id | integer | ID пользователя |

**Успешный ответ (200):**

```json
{
    "user": {
        "id": 1,
        "username": "pipita",
        "email": "pipita@bk.ru",
        "first_name": "Pipita",
        "last_name": "Ivanova",
        "phone": "89157655555",
        "avatar": null,
        "is_staff": null
    }
}
```

**Ошибка (404):** Пользователь не найден

---

## 3.2. Чат (AI-агент)

### 3.2.1. Отправка сообщения в чат

**POST** `/api/chat/process`

**Заголовки:** `Authorization: Bearer <access_token>`

**Запрос:**

```json
{
    "message": "Нужно перевезти 500 кг оборудования из Москвы в Санкт-Петербург завтра",
    "session_id": "sess_123"
}
```

| **Поле** | **Тип** | **Обязательное** | **Описание** |
|----------|---------|------------------|--------------|
| message | string | ✅ Да | Текст запроса пользователя |
| session_id | string | ✅ Да | Уникальный идентификатор сессии |

**Успешный ответ (200) — когда данных достаточно:**

```json
{
    "parsed": {
        "current_message": "Нужно перевезти 500 кг оборудования из Москвы в Санкт-Петербург завтра",
        "session_id": "sess_123",
        "step": "collecting",
        "extracted_params": {
            "ship_from": "Москва",
            "ship_to": "Санкт-Петербург",
            "cargo_type": "equipment",
            "weight_kg": 500,
            "shipment_date": "2026-07-26"
        }
    },
    "offers": [
        {
            "option_number": 1,
            "tariff_id": 123,
            "carrier_name": "ЭкоЛогистик",
            "price": 9000.0,
            "delivery_days": 3,
            "is_express": false
        }
    ],
    "message": "Найдены варианты перевозки:",
    "need_clarification": false
}
```

**Успешный ответ (200) — когда данных недостаточно:**

```json
{
    "parsed": {
        "step": "collecting",
        "missing_params": ["ship_from", "ship_to", "weight_kg"]
    },
    "offers": [],
    "message": "Укажите, пожалуйста, откуда и куда нужно перевезти груз, а также его вес.",
    "need_clarification": true
}
```

---

# 4. Общие структуры данных

## 4.1. UserBase

```json
{
    "id": 1,
    "username": "pipita",
    "email": "pipita@bk.ru",
    "first_name": "Pipita",
    "last_name": "Ivanova",
    "phone": "89157655555",
    "avatar": null,
    "is_staff": null
}
```

| **Поле** | **Тип** | **Описание** |
|----------|---------|--------------|
| id | integer | ID пользователя |
| username | string | Имя пользователя |
| email | string/null | Email |
| first_name | string/null | Имя |
| last_name | string/null | Фамилия |
| phone | string/null | Телефон |
| avatar | string/null | Ссылка на аватар |
| is_staff | boolean/null | Администратор |

---

## 4.2. TariffOption

```json
{
    "option_number": 1,
    "tariff_id": 123,
    "carrier_name": "ЭкоЛогистик",
    "price": 9000.0,
    "delivery_days": 3,
    "is_express": false
}
```

| **Поле** | **Тип** | **Описание** |
|----------|---------|--------------|
| option_number | integer | Номер для выбора (1, 2, 3...) |
| tariff_id | integer | ID тарифа для создания заказа |
| carrier_name | string | Название перевозчика |
| price | number | Цена, ₽ |
| delivery_days | integer | Срок доставки, дней |
| is_express | boolean | Экспресс-доставка |

---

# 5. Коды ошибок

| **HTTP Код** | **Описание** |
|--------------|--------------|
| 200 | Успешно |
| 401 | Не авторизован |
| 404 | Ресурс не найден |
| 422 | Ошибка валидации |

**Формат ошибки 422:**

```json
{
    "detail": [
        {
            "loc": ["body", "username"],
            "msg": "field required",
            "type": "missing"
        }
    ]
}
```

---

# 6. Матрица покрытия требований API

| **TR ID** | **Требование** | **Endpoint** | **Метод** | **Статус** |
|-----------|----------------|--------------|-----------|------------|
| TR-001 | Регистрация пользователя | `/api/auth/register` | POST | ✅ |
| TR-002 | Авторизация пользователя | `/api/auth/token` | POST | ✅ |
| TR-003 | Чат для заявки | `/api/chat/process` | POST | ✅ |
| TR-009 | Список пользователей | `/api/users/list` | GET | ✅ |
| TR-010 | Пользователь по ID | `/api/users/{id}` | GET | ✅ |


---
