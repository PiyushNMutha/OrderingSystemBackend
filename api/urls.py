from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from .views import register, profile 

def home(request):
    return HttpResponse("API is running ✅")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('register/', register),
    path('profile/', profile),
    path('api/', include('cafeteria_tables.urls')),
    path('api/', include('menu.urls')),

]
