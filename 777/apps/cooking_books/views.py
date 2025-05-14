from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Исправленный импорт
from django.db import models  # Добавленный импорт
from django.contrib import messages

from .models import Recipe, Comment, Rating
from .forms import RecipeForm, CommentForm


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)

            # Обработка автора
            if request.user.is_authenticated:
                recipe.author = request.user
                # Отправка письма только авторизованным пользователям с email
                if request.user.email:
                    try:
                        send_mail(
                            'Новый рецепт добавлен!',
                            f'Ваш новый рецепт "{recipe.title}" был успешно добавлен.',
                            'azimkulovarita019@gmail.com',
                            [request.user.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        messages.warning(request, f'Не удалось отправить письмо: {str(e)}')
            else:
                # Создаем или получаем гостевого пользователя
                guest_user, created = User.objects.get_or_create(
                    username='guest',
                    defaults={'email': 'guest@example.com', 'password': 'unusablepassword'}
                )
                recipe.author = guest_user

            recipe.save()
            messages.success(request, 'Рецепт успешно добавлен!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})


def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')  # Сортировка по дате создания
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all().order_by('-created_at')  # Сортировка комментариев
    ratings = recipe.ratings.all()

    # Расчет среднего рейтинга
    average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] if ratings else None

    # Обработка комментариев и оценок
    if request.method == "POST":
        # Проверка аутентификации
        if not request.user.is_authenticated:
            messages.warning(request, 'Для добавления комментария или оценки необходимо войти в систему')
            return redirect('login')

        # Обработка оценки
        rating_value = request.POST.get('rating')
        if rating_value:
            Rating.objects.update_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'rating': rating_value}
            )
            messages.success(request, 'Ваша оценка сохранена!')

        # Обработка комментария через форму
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            Comment.objects.create(
                recipe=recipe,
                user=request.user,
                content=comment_form.cleaned_data['content']
            )
            messages.success(request, 'Ваш комментарий добавлен!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        comment_form = CommentForm()

    # Проверка, поставил ли текущий пользователь оценку
    user_rating = None
    if request.user.is_authenticated:
        user_rating = ratings.filter(user=request.user).first()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'ratings': ratings,
        'average_rating': average_rating,
        'comment_form': comment_form,
        'user_rating': user_rating,
    })


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('recipe_list')  # Перенаправление после успешной регистрации
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

