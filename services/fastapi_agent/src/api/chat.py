from fastapi import APIRouter, Request
from src.schemas.chat_schemas import ChatRequest, ChatResponse
from src.agents.order_agent import build_order_agent
from src.agents.checkpointer import get_redis_checkpointer
from src.utils.auth import extract_token
import logging

# Декоратор для обработчик ошибок здесь не нужен у нас есть другие внутри других

logger = logging.getLogger(__name__)
chat_router = APIRouter(prefix="/api/chat", tags=["Chat"])

_agent = None

async def get_agent():
    global _agent
    if _agent is None:
        logger.info("🔄 Инициализация агента LangGraph...")
        checkpointer = await get_redis_checkpointer()
        _agent = build_order_agent(checkpointer)
        logger.info("✅ Агент успешно создан")
    return _agent

@chat_router.post("/process", response_model=ChatResponse,
                  summary="Обработка чата")
async def process_chat(request: Request, chat_req: ChatRequest):
    """Обрабатывает сообщение пользователя в рамках диалогового агента.
        Функция принимает текст запроса и идентификатор сессии, передаёт их
        в агент LangGraph, который последовательно:
          1. Извлекает сущности (город отправления, город назначения, вес, дата и др.)
          2. Проверяет полноту обязательных полей
          3. Выполняет поиск тарифов через Django API (`/api/tariffs/search/`)
          4. Обрабатывает выбор пользователя (номер варианта)
          5. Запрашивает подтверждение заказа
          6. Создаёт заказ через Django API (`/api/orders/`) при подтверждении
    """
    logger.info("=" * 60)
    logger.info(f"📩 Получен запрос от пользователя: session_id={chat_req.session_id}")
    logger.info(f"📝 Текст сообщения: {chat_req.text[:100]}...")  # обрезаем для краткости

    # 1. Получаем агента
    try:
        agent = await get_agent()
        logger.info("✅ Агент загружен успешно")
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки агента: {e}", exc_info=True)
        return ChatResponse(
            parsed={},
            offers=[],
            message="Извините, не удалось инициализировать обработчик. Попробуйте позже.",
            need_clarification=True
        )

    # Получаем данные авторизации пользователя из заголовка
    auth_token = extract_token(request)

    # Формируем входные данные для графа
    input_state = {
        "current_message": chat_req.text,
        "session_id": chat_req.session_id,
        "auth_token": auth_token,
    }
    config = {"configurable": {"thread_id": chat_req.session_id}}
    logger.info(f"⚙️ Конфигурация графа: {config}")
    logger.info(f"🔧 Входное состояние: {input_state}")

    # 3. Запускаем граф
    try:
        logger.info("🚀 Запуск графа LangGraph...")
        final_state = await agent.ainvoke(input_state, config=config)
        logger.info("✅ Граф выполнен успешно")
        logger.info(f"📦 Финальное состояние: {final_state}")
    except Exception as e:
        logger.error(f"❌ Ошибка выполнения графа: {e}", exc_info=True)
        return ChatResponse(
            parsed={},
            offers=[],
            message="Извините, произошла ошибка при обработке запроса. Попробуйте позже.",
            need_clarification=True
        )

    # 4. Извлекаем ответ и дополнительную информацию
    response_message = final_state.get("response_message", "Сообщение не сгенерировано.")
    offers = final_state.get("offers", [])
    step = final_state.get("step", "init")
    need_clarification = step in ("collecting", "choosing", "confirming") and step != "done"

    logger.info(f"💬 Ответное сообщение: {response_message[:200]}...")
    logger.info(f"📊 Найдено предложений: {len(offers)}")
    logger.info(f"📍 Текущий шаг: {step}")
    logger.info(f"❓ Требуется уточнение: {need_clarification}")

    logger.info("=" * 60)

    return ChatResponse(
        parsed=final_state,
        offers=offers,
        message=response_message,
        need_clarification=need_clarification,
    )