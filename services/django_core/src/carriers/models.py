from django.db import models

"Общая информация о перевозчике с возможностью расширения"


class Carrier(models.Model):
    name = models.CharField(max_length=255)  # коммерческое название
    legal_name = models.CharField(max_length=255)
    country = models.CharField(
        max_length=100, blank=True, default="Россия", verbose_name="Страна регистрации"
    )
    inn = models.CharField(max_length=255)
    ogrn = models.CharField(max_length=255)
    reg_number = models.CharField(
        max_length=100, blank=True, verbose_name="Регистрационный номер в стране"
    )
    # contract_number = models.CharField(max_length=255) договор с платформой пока не нужно

    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    rating = models.IntegerField(default=0.0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # tariffs = models.ManyToManyField('tariffs.Tariff', related_name='carriers')

    class Meta:
        verbose_name = "Перевозчик"
        verbose_name_plural = "Перевозчики"
        ordering = ["-rating"]

    def __str__(self):
        return self.name
