from django.urls import path
from .views import TableListAPI, UpdateTableStatusAPI, CreateTableAPI, DeleteTableAPI

urlpatterns = [
    path('tables/', TableListAPI.as_view(), name='table-list'),
    path('tables/create/', CreateTableAPI.as_view(), name='table-create'),
    path('tables/<int:table_id>/status/', UpdateTableStatusAPI.as_view(), name='table-status'),
    path('tables/delete/<int:table_id>/', DeleteTableAPI.as_view(), name='table-delete'),
]