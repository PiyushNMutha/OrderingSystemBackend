from django.urls import path
from .views import CreateOrderAPI, OrderListAPI, UpdateOrderStatusAPI

urlpatterns = [
    path('order/create/', CreateOrderAPI.as_view(), name='create-order'),
    path('orders/', OrderListAPI.as_view(), name='order-list'),
    path('order/<int:order_id>/status/', UpdateOrderStatusAPI.as_view(), name='update-order-status'),
]