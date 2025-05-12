from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.news_view, name='index'),
    path('news_detail/<int:pk>/', views.news_detail, name='detail')
]
