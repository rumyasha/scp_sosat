# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.shortcuts import render

from Cook.cooking_book.models import Recipe
from Cook.cooking_book.utils import send_recipe_notification

# Устанавливаем настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cooking_book.settings')

# Создаем объект Celery
app = Celery('cooking_book')

# Загружаем настройки Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях Django
app.autodiscover_tasks()



def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    # Отправка уведомления на email пользователя
    send_recipe_notification(request.user.email, recipe.title)

    return render(request, 'recipe_detail.html', {'recipe': recipe})

# celery.py (добавление Beat для периодических задач)
from celery import Celery
from celery.schedules import crontab

app = Celery('your_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Периодические задачи
app.conf.beat_schedule = {
    'send-daily-recipes': {
        'task': 'recipes.tasks.send_daily_recipes',  # указываем путь к задаче
        'schedule': crontab(hour=7, minute=0),  # каждый день в 7 утра
    },
}
