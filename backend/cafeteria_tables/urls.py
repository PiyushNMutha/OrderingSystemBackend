from django.urls import path
from .views import TableListAPI, UpdateTableStatusAPI

urlpatterns = [
    path('tables/', TableListAPI.as_view(), name='table-list'),
    path('tables/<int:table_id>/status/', UpdateTableStatusAPI.as_view(), name='table-status'),
]
