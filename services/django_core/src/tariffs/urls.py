from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('tariffs', views.TariffViewSet, basename='tariff')

urlpatterns = [
    path('tariffs/search/', views.search_tariff, name='search-tariff'),
    path('', include(router.urls)),  # создаёт /tariffs/ и /tariffs/{id}/
]

#GET /api/tariffs/ – список
#POST /api/tariffs/ – создание
#GET /api/tariffs/{id}/ – детали
#PUT /api/tariffs/{id}/ – полное обновление
#PATCH /api/tariffs/{id}/ – частичное обновление
#DELETE /api/tariffs/{id}/ – удаление
#POST /api/tariffs/search/ – кастомный поиск