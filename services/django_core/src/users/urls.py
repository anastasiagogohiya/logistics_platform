from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    # REST-алиасы (сначала общие, потом детальные)
    path("users/", views.UserListView.as_view(), name="user-list"),          # список
    path("users/<int:id>/", views.UserIdView.as_view(), name="user-detail"), # детали

    # Оригинальные маршруты для FastAPI
    path("users/register/", views.RegisterView.as_view(), name="register"),
    path("users/list/", views.UserListView.as_view(), name="users-list"),
    # дублирующий путь с id убираем (оставляем только один)
    # path("users/<int:id>/", views.UserIdView.as_view(), name="user-get"),  # удаляем
    path("update/<int:id>/", views.UserUpdateView.as_view(), name="user-update"),
    path("delete/<int:id>/", views.UserDeleteView.as_view(), name="user-delete"),
]