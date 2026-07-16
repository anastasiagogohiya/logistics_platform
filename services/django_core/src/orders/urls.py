from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("orders", views.OrderViewSet, basename="order")

urlpatterns = [
    path("orders/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("", include(router.urls)),
]
