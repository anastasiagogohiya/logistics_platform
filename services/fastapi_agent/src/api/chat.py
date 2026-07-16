# api/chat.py
import logging

from fastapi import APIRouter, Request

from src.agents.checkpointer import get_redis_checkpointer
from src.agents.middlewares import IntentRouter
from src.agents.order_agent import build_order_agent
from src.schemas.chat_schemas import ChatRequest, ChatResponse
from src.utils.auth import extract_token

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


@chat_router.post("/process", response_model=ChatResponse, summary="Обработка чата")
async def process_chat(request: Request, chat_req: ChatRequest):
    logger.info("=" * 60)
    logger.info(f"📩 Получен запрос: session_id={chat_req.session_id}")

    # === ШАГ 1: Предобработка через Middleware ===
    intent_result = IntentRouter.classify(chat_req.text)

    if intent_result and intent_result.get("skip_graph"):
        logger.info(f"⛔ Перехвачен интент '{intent_result['step']}'. В граф не идем.")

        # Обработка специальных действий без участия графа
        if intent_result.get("action") == "reset_graph_state":
            # Здесь можно принудительно очистить чекпоинт Redis для этой сессии
            pass

        return ChatResponse(
            parsed={"intent": intent_result.get("step")},
            offers=[],
            message=intent_result["response_message"],
            need_clarification=False,
        )

    logger.info(f"📝 Текст сообщения: {chat_req.text[:100]}...")

    try:
        agent = await get_agent()
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки агента: {e}", exc_info=True)
        return ChatResponse(
            parsed={}, offers=[], message="Сервис временно недоступен.", need_clarification=True
        )

    auth_token = extract_token(request)
    input_state = {
        "current_message": chat_req.text,
        "session_id": chat_req.session_id,
        "auth_token": auth_token,
    }
    config = {"configurable": {"thread_id": chat_req.session_id}}

    try:
        final_state = await agent.ainvoke(input_state, config=config)
    except Exception as e:
        logger.error(f"❌ Ошибка выполнения графа: {e}", exc_info=True)
        return ChatResponse(
            parsed={}, offers=[], message="Ошибка при обработке запроса.", need_clarification=True
        )

    response_message = final_state.get("response_message", "Сообщение не сгенерировано.")
    step = final_state.get("step", "init")
    need_clarification = step in ("collecting", "choosing", "confirming") and step != "done"

    logger.info("=" * 60)

    return ChatResponse(
        parsed=final_state,
        offers=final_state.get("offers", []),
        message=response_message,
        need_clarification=need_clarification,
    )
