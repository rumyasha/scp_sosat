from django.contrib import admin
from django.contrib.auth import views as auth_views  # Добавьте эту строку
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


