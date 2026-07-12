from django.contrib.auth.models import AbstractUser
from django.db import models

"""Расширяем встроенную в Джанго Модель Пользователя с ролями
Потом создать модель для Юр лиц
"""

"""Модель для физ. лиц"""
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=13, blank=False, null=False) # обязательное поле
    avatar = models.URLField(blank=True, null=True) # ссылка

    """У пользователей разные роли"""
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Client'
        CARRIER = 'carrier', 'Carrier'
        MANAGER = 'manager', 'Manager'
        # добавлять новые роли можно здесь

    role = models.CharField(max_length=10,
                            choices=Role.choices,
                            default=Role.CLIENT, # клиент не должен заполнять поле роль
                            )

    def is_admin(self):
        return self.role == CustomUser.Role.ADMIN

    def is_client(self):
        return self.role == CustomUser.Role.CLIENT

    def is_carrier(self):
        return self.role == CustomUser.Role.CARRIER

    def is_manager(self):
        return self.role == CustomUser.Role.MANAGER