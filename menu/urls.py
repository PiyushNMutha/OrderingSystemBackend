from django.urls import path
from .views import (
    MenuCategoryByTableAPI, 
    MenuItemByTableAPI,
    CreateMenuItemAPI,
    UpdateMenuItemAPI,
    DeleteMenuItemAPI
)

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
    path(
        'menu/items/create/',
        CreateMenuItemAPI.as_view(),
        name='menu-item-create'
    ),
    path(
        'menu/items/update/<int:item_id>/',
        UpdateMenuItemAPI.as_view(),
        name='menu-item-update'
    ),
    path(
        'menu/items/delete/<int:item_id>/',
        DeleteMenuItemAPI.as_view(),
        name='menu-item-delete'
    ),
]
