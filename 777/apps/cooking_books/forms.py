from django.contrib.auth import models
from django import forms

from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment, Rating
from django.contrib import messages


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all().order_by('-created_at')  # Сортировка по дате
    ratings = recipe.ratings.all()

    if request.method == "POST":
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            messages.warning(request, 'Для добавления комментария или оценки необходимо войти в систему')
            return redirect('login')  # Перенаправляем на страницу входа

        # Обработка оценки
        rating_value = request.POST.get('rating')
        if rating_value:
            rating, created = Rating.objects.update_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'rating': rating_value}
            )
            messages.success(request, 'Ваша оценка сохранена!')

        # Обработка комментария
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(
                recipe=recipe,
                user=request.user,
                content=comment_text
            )
            messages.success(request, 'Ваш комментарий добавлен!')

        return redirect('recipe_detail', recipe_id=recipe.id)  # Редирект для предотвращения повторной отправки

    # Рассчитываем средний рейтинг
    average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] if ratings else None

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'ratings': ratings,
        'average_rating': average_rating,
        'user_rating': ratings.filter(user=request.user).first() if request.user.is_authenticated else None
    })

# Форма для добавления рецепта
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions']

# Форма для добавления комментариев
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
