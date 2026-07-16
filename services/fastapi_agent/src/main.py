from api.auth import auth_router
from api.chat import chat_router
from api.users import user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from infra_logging import FastAPIRequestIdMiddleware, configure_logging

configure_logging(service_name="fastapi_agent", human_readable=True)


"""Точка входа"""

app = FastAPI(
    title="FastAPI Agent",
    description="API для работы с сервисами",
)


# Глобальная настройка
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Logistics API",
        version="1.0.0",
        routes=app.routes,
    )
    # Добавляем схему безопасности для JWT
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Применяем авторизацию глобально ко всем эндпоинтам
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Добавляем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(FastAPIRequestIdMiddleware)
# http://127.0.0.1:8000/docs


@app.get("/")
async def root():
    return {"message": "FastAPI Agent welcoming you!"}


# Подключаем Роуты и CORS
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)
