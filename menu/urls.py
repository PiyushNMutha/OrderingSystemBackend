from django.urls import path
from .views import MenuCategoryByTableAPI, MenuItemByTableAPI

urlpatterns = [
    path(
        'menu/categories/<int:table_number>/',
        MenuCategoryByTableAPI.as_view(),
        name='menu-categories-by-table'
    ),
    path(
        'menu/items/<int:table_number>/',
        MenuItemByTableAPI.as_view(),
        name='menu-items-by-table'
        ),
]
