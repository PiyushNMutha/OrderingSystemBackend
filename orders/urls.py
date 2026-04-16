from django.urls import path
from .views import CreateOrderAPI

urlpatterns = [
    path('order/create/', CreateOrderAPI.as_view()),
]