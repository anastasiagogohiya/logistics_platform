import logging

from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

"""Используем generics от rest_framework так как
они больше подходят для работы с API,  сразу json
если еще короче код с ModelViewSet, но для большего контроля от него откажусь"""

"""Вюхи по пользователям"""

# api/login = api/token - он внутри библиотеки rest_framework_simplejwt


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""

    permission_classes = [permissions.AllowAny]  # разрешено всем регистрироваться
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, "message": "User registered successfully"}
        )


class UserListView(generics.ListAPIView):
    """Получение списка всех пользователей"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # только для авторизованных
    filter_backends = [OrderingFilter]  # сортировка для админки
    ordering_fields = "__all__"  # сортиврока по всем полям

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Получаем всех пользователей
        serializer = self.get_serializer(queryset, many=True)  # Преварщаем в json
        return Response({"users": serializer.data})


class UserIdView(generics.RetrieveAPIView):
    """Получение данных по id пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # только для авторизованных
    lookup_field = "id"
    # Возвращает одного пользователя


class UserUpdateView(generics.RetrieveUpdateAPIView):
    """Обновление данных пользователя по id"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # только для авторизованных
    lookup_field = "id"


class UserDeleteView(generics.DestroyAPIView):
    """Удаление пользователя по id"""

    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # только для авторизованных
    lookup_field = "id"
