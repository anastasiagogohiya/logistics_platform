from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('carriers', views.CarrierViewSet, basename='carrier')

urlpatterns = [
    path('', include(router.urls)),   # /api/carriers/ — список, /api/carriers/{id}/ — детали
]
