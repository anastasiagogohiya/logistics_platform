from django.db import models

# Модель платежей (связь с заказом, статусом платежа, суммой, способом оплаты, с сервисом оплаты)

"""Модель можно расширить потом, для юр лиц пост оплата и т.д."""

class PaymentMethod(models.TextChoices):
    PREPAID = 'prepaid', 'Предоплата'
    POSTPAID = 'postpaid', 'Постоплата'


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает оплаты'
        PAID = 'paid', 'Оплачен'
        FAILED = 'failed', 'Ошибка'
        REFUNDED = 'refunded', 'Возврат'

    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.PROTECT,
        related_name='payment'
    )
    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.PREPAID # по умолчанию предоплата
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    # Для интеграции с платёжными системами
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_url = models.URLField(blank=True, null=True)  # ссылка на оплату

    def __str__(self):
        return f"Платёж #{self.id} - {self.order.order_number} ({self.status})"