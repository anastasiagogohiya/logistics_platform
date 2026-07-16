from django.db import models

"""Модель Заказ ЧТО ВЕЗЕМ с номером, датой, стоимостью, статусом"""


class OrderStatus(models.TextChoices):
    CREATED = "created"
    ASSIGNED = "assigned"  # назначен перевозчик
    IN_TRANSIT = "in_transit"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"


class CargoChoice(models.TextChoices):
    DOCUMENTS = "documents", "documents"
    PACKAGE = "package", "package"
    PALLET = "pallet", "pallet"
    FURNITURE = "furniture", "furniture"
    VEHICLE = "vehicle", "vehicle"
    HAZMAT = "hazmat", "hazmat"
    LIQUID = "liquid", "liquid"  # перевозка например силосами
    OTHER = "other", "other"


class DeliveryType(models.TextChoices):
    STANDARD = "standard"
    EXPRESS = "express"


class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # дата создания
    updated_at = models.DateTimeField(auto_now=True)  # дата обновления

    # сырые данные от клиента
    raw_data = models.TextField()

    # информация по грузу
    cargo_type = models.CharField(
        max_length=50, choices=CargoChoice.choices, default=CargoChoice.OTHER
    )
    weight_kg = models.FloatField(verbose_name="Вес (кг)")
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_hazardous = models.BooleanField(default=False)

    # Маршрут
    ship_from = models.CharField(max_length=100)  # откуда
    ship_to = models.CharField(max_length=100)  # куда
    shipment_date = models.DateTimeField()  # дата отгрузки
    # requested_delivery_date = models.DateTimeField() # ожидаемая дата доставки
    delivery_type = models.CharField(
        max_length=100, choices=DeliveryType.choices, default=DeliveryType.STANDARD
    )

    # ... результат подбора ...
    carrier = models.ForeignKey("carriers.Carrier", on_delete=models.PROTECT, null=True, blank=True)
    tariff = models.ForeignKey("tariffs.Tariff", on_delete=models.PROTECT, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # ... статус ...
    order_status = models.CharField(max_length=50, choices=OrderStatus.choices, default="created")
    expected_delivery_date = models.DateTimeField(
        null=True, blank=True, help_text="Ожидаемая дата доставки исходя из тарифа перевозчика"
    )
    factual_delivery_date = models.DateTimeField(
        null=True, blank=True, help_text="Фактическая дата доставки"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ {self.order_number} - {self.client}"
