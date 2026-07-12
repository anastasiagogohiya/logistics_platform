from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

# Самый прагматичный путь для вас —
# использовать оба инструмента одновременно.
# Добавьте jazzmin для красивой админки, которой будут пользоваться люди,
# и django-admin-rest-api для того, чтобы ваш AI-клиент мог взаимодействовать
# с системой через API. Таким образом, вы получите и красивый интерфейс,
# и мощную программную интеграцию.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("avatar", "phone", "role") # поля в списке записей
    # какие поля будут ссылками на редактирование
    # поиск по полям
    # фильтры справа
    # сортировка по умолчанию
    # поля только для чтения

