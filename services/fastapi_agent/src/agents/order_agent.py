# src/agents/order_agent.py
import logging

from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from langgraph.graph import END, StateGraph

from .state import DialogState
from .tools import (
    confirm_order_tool,
    create_order_tool,
    extract_entities_tool,
    generate_response,
    process_payment_tool,
    search_tariffs_tool,
    select_offer_tool,
    validate_required_fields,
)

logger = logging.getLogger(__name__)


def build_order_agent(checkpointer: AsyncRedisSaver):
    workflow = StateGraph(DialogState)

    # Добавляем узлы (убедитесь, что все перечислены)
    workflow.add_node("extract_entities", extract_entities_tool)
    workflow.add_node("validate_fields", validate_required_fields)
    workflow.add_node("search_tariffs", search_tariffs_tool)
    workflow.add_node("select_offer", select_offer_tool)
    workflow.add_node("confirm_order", confirm_order_tool)
    workflow.add_node("create_order", create_order_tool)
    workflow.add_node("process_payment", process_payment_tool)  # <-- добавить
    workflow.add_node("generate_response", generate_response)

    # Начальный роутер
    def initial_router(state: DialogState) -> str:
        logger.info(
            f"🔀 initial_router: step={state.step}, current_message={state.current_message}"
        )
        step = state.step

        if step == "payment_pending":
            return "process_payment"

        if step in ("done", "cancelled"):
            return "generate_response"

        if step == "choosing" and state.current_message:
            if state.current_message.strip().isdigit():
                return "select_offer"
            else:
                return "generate_response"

        if step == "confirming":
            return "confirm_order"

        if step == "creating":
            return "create_order"

        return "extract_entities"

    workflow.set_conditional_entry_point(initial_router)

    # ---------- Переходы ----------
    workflow.add_edge("extract_entities", "validate_fields")

    def after_validate(state: DialogState) -> str:
        if state.step == "error":
            return "generate_response"
        if state.step == "searching":
            return "search_tariffs"
        return "generate_response"

    workflow.add_conditional_edges("validate_fields", after_validate)

    workflow.add_edge("search_tariffs", "generate_response")
    workflow.add_edge("select_offer", "generate_response")
    workflow.add_edge("create_order", "generate_response")
    workflow.add_edge("process_payment", "generate_response")

    def after_confirm(state: DialogState) -> str:
        if state.step == "creating":
            return "create_order"
        else:
            return "generate_response"

    workflow.add_conditional_edges("confirm_order", after_confirm)

    workflow.add_edge("create_order", "generate_response")
    workflow.add_edge("generate_response", END)

    logger.info("✅ StateGraph успешно скомпилирован")

    return workflow.compile(checkpointer=checkpointer)
