# utils.py
from django.core.mail import send_mail

def send_recipe_notification(user_email, recipe_name):
    send_mail(
        'Новый рецепт добавлен!',
        f'Ваш любимый рецепт "{recipe_name}" теперь доступен!',
        'from@example.com',  # твой email
        [user_email],  # email пользователя
        fail_silently=False,
    )
