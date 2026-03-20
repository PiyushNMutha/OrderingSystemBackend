from django.contrib import admin
from django.urls import path, include
from .views import register, profile 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('profile/', profile),
    path('api/', include('cafeteria_tables.urls')),
    path('api/', include('menu.urls')),

]
