# payments/services/payment_gateway.py
import uuid
from datetime import datetime


class PaymentGateway:
    @staticmethod
    def create_payment(amount: float, currency: str = "RUB") -> dict:
        """Имитация создания платежа. Возвращает данные, как от реального шлюза."""
        # Здесь можно добавить задержку, чтобы имитировать реальный запрос
        return {
            "payment_id": str(uuid.uuid4()),
            "status": "pending",
            "payment_url": f"https://fake-payment.example.com/pay/{uuid.uuid4()}",
            "created_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def confirm_payment(payment_id: str) -> dict:
        """Имитация подтверждения оплаты."""
        # Здесь можно добавить случайную ошибку для имитации отказа (опционально)
        # import random
        # if random.random() < 0.1:
        #     return {"status": "failed", "error": "Ошибка шлюза"}
        return {
            "status": "paid",
            "paid_at": datetime.utcnow().isoformat(),
        }
