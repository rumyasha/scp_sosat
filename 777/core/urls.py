from django.contrib import admin
from django.contrib.admin import views
# Добавьте эту строку
from django.urls import path,include
# from .  import views
# from Cook.apps.cooking_books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.cooking_books.urls'))
]


