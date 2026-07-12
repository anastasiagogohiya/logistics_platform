# src/agents/tools.py
import re
import os
import logging
import httpx
from src.services.ner_parser import extract_entities
from src.services.django_client import DjangoAPIClient
from src.agents.state import DialogState
from datetime import timedelta

logger = logging.getLogger(__name__)

DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://django:8001")
django_client = DjangoAPIClient(DJANGO_API_URL)


# ==================== Базовые узлы ====================

async def extract_entities_tool(state: DialogState) -> dict:
    """Извлекает сущности из текущего сообщения."""
    text = state.current_message
    if not text:
        return {"step": "error", "error_message": "Пустой запрос"}

    parsed = extract_entities(text)
    updates = {}
    for key in [
        "ship_from", "ship_to", "cargo_type", "delivery_type",
        "weight_kg", "quantity", "is_hazardous", "shipment_date"
    ]:
        val = parsed.get(key)
        if val not in (None, "", "other"):
            updates[key] = val

    updates["step"] = "collecting"
    return updates


async def validate_required_fields(state: DialogState) -> dict:
    """Проверяет наличие обязательных полей для поиска тарифов."""
    required = ["ship_from", "ship_to", "shipment_date", "weight_kg"]
    missing = [f for f in required if not getattr(state, f, None)]

    if missing:
        return {
            "step": "collecting",
            "response_message": f"Уточните: {', '.join(missing)}.",
        }
    return {"step": "searching"}


async def search_tariffs_tool(state: DialogState) -> dict:
    """Поиск тарифов через Django API."""
    params = {
        "ship_from": state.ship_from,
        "ship_to": state.ship_to,
        "cargo_type": state.cargo_type or "other",
        "weight_kg": state.weight_kg,
        "shipment_date": state.shipment_date.isoformat() if state.shipment_date else None,
        "delivery_type": state.delivery_type or "standard",
        "is_hazardous": state.is_hazardous or False,
        "quantity": state.quantity or 1,
    }
    # запрос через Класс Джанго клиент
    try:
        data = await django_client.search_tariffs(params, auth_token=state.auth_token)
    except httpx.HTTPStatusError as e:
        logger.error(f"Ошибка поиска тарифов: {e}")
        return {
            "step": "error",
            "error_message": "Сервис временно недоступен. Попробуйте позже."
        }

    offers = data.get("results", [])
    if offers:
        return {"offers": offers, "step": "choosing"}
    else:
        return {
            "step": "collecting",
            "response_message": "Тарифов не найдено. Попробуйте изменить параметры.",
        }


async def select_offer_tool(state: DialogState) -> dict:
    """Выбирает офер по номеру, введённому пользователем."""
    msg = state.current_message
    if not msg:
        return {"step": "error", "error_message": "Не указан номер варианта"}

    match = re.search(r"\b(\d+)\b", msg)
    if not match:
        return {"step": "error", "error_message": "Не удалось распознать номер"}

    idx = int(match.group(1)) - 1
    offers = state.offers or []
    if idx < 0 or idx >= len(offers):
        return {"step": "error", "error_message": f"Номер {idx+1} вне диапазона (1..{len(offers)})"}

    selected = offers[idx]
    return {
        "selected_offer": selected,
        "step": "confirming",
        "response_message": None,
    }


async def confirm_order_tool(state: DialogState) -> dict:
    """Обрабатывает ответ пользователя на подтверждение."""
    msg = state.current_message
    if not msg:
        return {
            "step": "confirming",
            "response_message": "Пожалуйста, ответьте 'да' или 'нет'.",
        }

    lower = msg.lower().strip()
    if lower in ("да", "yes", "подтверждаю", "ок", "ага", "конечно"):
        return {"step": "creating"}
    elif lower in ("нет", "no", "не надо", "отмена", "не подтверждаю"):
        return {
            "step": "init",
            "selected_offer": None,
            "offers": [],
            "response_message": "Вы отказались от оформления заказа. Если захотите перевезти груз, просто напишите новый запрос.",
        }
    else:
        return {
            "step": "confirming",
            "response_message": "Не понял ответ. Скажите 'да' или 'нет'.",
        }

async def create_order_tool(state: DialogState) -> dict:
    selected = state.selected_offer
    if not selected:
        return {"step": "error", "error_message": "Не выбран тариф"}

    shipment_date = state.shipment_date
    expected_delivery_date = None
    if shipment_date and selected.get('delivery_days'):
        expected_delivery_date = (shipment_date + timedelta(days=selected['delivery_days'])).isoformat()

    payload = {
        "option_number": selected.get("option_number"),
        "weight_kg": state.weight_kg,
        "ship_from": state.ship_from,
        "ship_to": state.ship_to,
        "cargo_type": state.cargo_type,
        "shipment_date": shipment_date.isoformat() if shipment_date else None,
        "delivery_type": state.delivery_type,
        "quantity": state.quantity,
        "is_hazardous": state.is_hazardous,
        "price": selected["price"],
        "expected_delivery_date": expected_delivery_date,
    }

    logger.info(f"📤 Отправка заказа в Django: {payload}")

    # 1. Создаём заказ в Django
    order_result = await django_client.create_order(payload)
    order_id = order_result.get("id")
    order_number = order_result.get("order_number")

    # 2. Создаём платёж для заказа
    payment_payload = {
        "order": order_id,
        "method": state.payment_method,
        "amount": selected["price"],
    }
    payment_result = await django_client.create_payment(payment_payload, auth_token=state.auth_token)

    return {
        "step": "payment_pending",
        "order_created": True,
        "order_number": order_number,
        "payment_id": payment_result.get("id"),
        "payment_url": payment_result.get("payment_url"),
        "payment_status": payment_result.get("status"),
        "offers": [],
        "selected_offer": None,
    }


async def process_payment_tool(state: DialogState) -> dict:
    if not state.payment_id:
        return {"step": "error", "error_message": "Платёж не найден"}

    try:
        await django_client.pay_payment(state.payment_id, auth_token=state.auth_token)
        return {
            "step": "done",
            "payment_status": "paid",
            "response_message": "✅ Оплата успешно проведена! Спасибо за заказ."
        }
    except Exception as e:
        return {
            "step": "payment_pending",
            "response_message": "Ошибка оплаты. Попробуйте ещё раз."
        }



async def generate_response(state: DialogState) -> dict:
    """Генерирует финальное сообщение для пользователя."""
    step = state.step

    if step == "choosing":
        offers = state.offers or []
        if offers:
            lines = []
            for i, o in enumerate(offers[:5], 1):
                lines.append(f"{i}. {o['carrier_name']}: {o['price']} руб., {o['delivery_days']} дн.")
            text = (
                f"Найдено {len(offers)} вариантов:\n"
                + "\n".join(lines)
                + "\n\nВыберите номер для оформления заказа."
            )
        else:
            text = "Вариантов не найдено. Попробуйте изменить запрос."

    elif step == "confirming":
        selected = state.selected_offer
        if not selected:
            text = "Сначала выберите вариант."
        else:
            # Вычисляем ожидаемую дату доставки
            shipment_date = state.shipment_date
            if shipment_date and selected.get('delivery_days'):
                expected_date = shipment_date + timedelta(days=selected['delivery_days'])
                expected_date_str = expected_date.strftime('%Y-%m-%d')
            else:
                expected_date_str = "неизвестна"

            details = (
                f"📦 **Данные для оформления заказа:**\n"
                f"Откуда: {state.ship_from}\n"
                f"Куда: {state.ship_to}\n"
                f"Тип груза: {state.cargo_type}\n"
                f"Вес: {state.weight_kg} кг\n"
                f"Дата отправки: {state.shipment_date}\n"
                f"Перевозчик: {selected['carrier_name']}\n"
                f"Стоимость: {selected['price']} руб.\n"
                f"Срок доставки: {selected['delivery_days']} дн.\n"
                f"Ожидаемая дата доставки: {expected_date_str}\n\n"
                f"Подтвердите заказ? (да/нет)"
            )
            text = details

    elif step == "creating":
        text = "Заказ создаётся..."



    elif step == "done":
        order_number = state.order_number or "неизвестен"
        text = f"✅ Заказ {order_number} оформлен и оплачен! Спасибо!"

    elif step == "payment_pending":
        text = (
            f"✅ Заказ {state.order_number} создан.\n"
            "💳 Для оплаты введите номер карты или напишите 'оплатить'."
        )


    elif step == "cancelled":
        text = state.response_message or "Заказ отменён."

    elif step == "init":
        text = state.response_message or "Я вас слушаю."

    elif step == "error":
        text = state.error_message or "Произошла ошибка."

    else:
        text = state.response_message or "Я вас слушаю."

    return {"response_message": text}