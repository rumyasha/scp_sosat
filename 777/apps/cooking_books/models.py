from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.TextField(verbose_name="Ингредиенты")
    cooking_steps = models.TextField(verbose_name="Шаги приготовления")
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления (мин)")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Изображение")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'recipe_id': self.pk})

    @property
    def average_rating(self):
        return self.ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.recipe.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']


class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оценки")

    def __str__(self):
        return f"Оценка {self.rating} от {self.user.username} для {self.recipe.title}"

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        unique_together = ('recipe', 'user')
        ordering = ['-created_at']


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baskets')
    recipes = models.ManyToManyField(Recipe, related_name='in_baskets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipes = models.ManyToManyField(Recipe, related_name='in_favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Избранное пользователя {self.user.username}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные рецепты"


from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name='Аватар')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'