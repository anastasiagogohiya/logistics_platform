from django.db import models

# Тарифы транспортных компаний, с типами доставки и направлениями
# Направления пока по городам, для расширения более конкретные зоны


class Tariff(models.Model):
    class DeliveryType(models.TextChoices):
        STANDARD = "standard"
        EXPRESS = "express"

    # ссылка на перевозчика, все тарифы через связь related_name
    # Обратная связь: carrier.tariffs.all()
    carrier = models.ForeignKey(
        "carriers.Carrier", on_delete=models.CASCADE, related_name="tariffs"
    )

    # Направления
    ship_from = models.CharField(max_length=255, db_index=True)  # быстрый поиск
    ship_to = models.CharField(max_length=255, db_index=True)  # быстрый поиск

    # Какой тип груза перевозчик может перевозить в JSON (по разным напрвлениям может перевозить разные типы)
    cargo_type = models.JSONField(default=list, help_text="Список типов груза для перевозки")

    # Весовые диапазоны
    cargo_weight_from = models.FloatField(default=0)
    cargo_weight_to = models.FloatField(null=True, blank=True)

    # Объем не внедрен

    # Тип доставки
    delivery_type = models.CharField(
        max_length=20, choices=DeliveryType.choices, default=DeliveryType.STANDARD, db_index=True
    )

    # Цена
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Срок доставки как для экпресс так и для стандарта
    delivery_days_min = models.PositiveIntegerField(default=1, verbose_name="Мин. дней доставки")

    delivery_days_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Макс. дней доставки",
        help_text="Оставьте пустым, если срок фиксированный",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ["carrier", "ship_from", "ship_to", "delivery_type"]
        # Уникальная строка тарифа по маршруту
        unique_together = [
            [
                "carrier",
                "ship_from",
                "ship_to",
                "cargo_weight_from",
                "cargo_weight_to",
                "delivery_type",
            ]
        ]
