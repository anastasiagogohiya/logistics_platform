"""Создание суперпользователя и ролей"""
from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = "Создание суперпользователя и ролей"

    def handle(self, *args, **kwargs):
        self.create_users_roles()

    def create_users_roles(self):
        self.stdout.write(self.style.SUCCESS("Создание ролей..."))
        users_data = [
            {
                'username': 'admin',
                'password': 'admin',
                'role': CustomUser.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
             },
            {
                'username': 'client',
                'password': 'client',
                'role': CustomUser.Role.CLIENT,
            },
            {
                'username': 'carrier',
                'password': 'carrier',
                'role': CustomUser.Role.CARRIER,
            },
            {
                'username': 'manager',
                'password': 'manager',
                'role': CustomUser.Role.MANAGER,
                'is_staff': True, # может заходить в админ панель
            },

        ]

        for user_data in users_data:
            username = user_data['username']
            if not CustomUser.objects.filter(username=username).exists():
                if user_data.get('is_superuser'):
                    CustomUser.objects.create_superuser(
                        username=user_data['username'],
                        password=user_data['password'],
                        role=user_data['role'],
                    )
                else:
                    user = CustomUser.objects.create_user(
                        username=user_data['username'],
                        password=user_data['password'],
                        role=user_data['role'],
                    )
                    # Если нужно дать доступ к админке
                    if user_data.get('is_staff'):
                        user.is_staff = True
                        user.save()
                self.stdout.write(self.style.SUCCESS(f'Создан: {username} ({user_data["role"]})'))
            else:
                self.stdout.write(f'Уже существует: {username}')
