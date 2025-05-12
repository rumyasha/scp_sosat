from telegram import Bot
from celery import shared_task
from .utils import send_recipe_notification

@shared_task
def send_telegram_notification(user_id, recipe_name):
    bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")
    bot.send_message(user_id, f'Your favorite recipe "{recipe_name}" is now available!')



@shared_task
def send_daily_recipes():
    top_breakfast = Recipe.objects.filter(category="breakfast").order_by('-rating').first()
    top_lunch = Recipe.objects.filter(category="lunch").order_by('-rating').first()
    top_dinner = Recipe.objects.filter(category="dinner").order_by('-rating').first()

    # Отправка уведомлений через email
    send_recipe_notification(top_breakfast.author.email, top_breakfast.title)
    send_recipe_notification(top_lunch.author.email, top_lunch.title)
    send_recipe_notification(top_dinner.author.email, top_dinner.title)


from celery import shared_task
from django.core.mail import send_mail
from .models import Recipe


@shared_task
def send_new_recipe_notification(recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)  # Получаем рецепт по ID
    send_mail(
        'Новый рецепт на платформе!',
        f'Новый рецепт "{recipe.title}" только что был добавлен.',
        'from@example.com',  # Адрес отправителя
        ['user@example.com'],  # Сюда можно добавить адреса получателей
        fail_silently=False,
    )

