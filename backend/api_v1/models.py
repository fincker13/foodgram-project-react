from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag', max_length=200)
    color = models.CharField(
        verbose_name='Color',
        max_length=200,
        blank=True,
        null=True
    )
    slug = models.SlugField(verbose_name='Slag', unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='ingredient', max_length=200)
    measurement_unit = models.CharField(
        verbose_name='Еденица измерения',
        max_length=200
    )
    objects = models.Manager()

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Amount',
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True
    )
    name = models.CharField(verbose_name='Название', max_length=200)
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        default=1,
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    is_favorit = models.BooleanField(
        verbose_name='Добавлено в избранное',
        default=False
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Добвленно в список покупок',
        default=False
    )
    objects = models.Manager()


class Amount(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='Колличество')
    objects = models.Manager()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )
    objects = models.Manager()


class Favorit(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='user',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Рецепт',
        related_name='favorit',
    )
    objects = models.Manager()
