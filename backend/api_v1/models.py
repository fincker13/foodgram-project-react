from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tags(models.Model):
    name = models.CharField(verbose_name='Teg', max_length=200)
    color = models.CharField(
        verbose_name='Color',
        max_length=200,
        blank=True,
        null=True
    )
    slug = models.SlugField(verbose_name='Slag', unique=True)
    objects = models.Manager()


class Ingredients(models.Model):
    name = models.CharField(verbose_name='ingredient', max_length=200)
    measurement_unit = models.CharField(
        verbose_name='measurement unit',
        max_length=200
    )
    objects = models.Manager()


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ingredients = models.ManyToManyField(
        Ingredients,
        through='Amount',
        through_fields=('recipes', 'ingredients')
    )
    tags = models.ManyToManyField(Tags)
    image = models.ImageField()
    name = models.CharField(verbose_name='Название', max_length=200)
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        default=None,
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    objects = models.Manager()

    def __str__(self):
        return (self.author, self.name, self.cooking_time)


class Amount(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Колличество')
    objects = models.Manager()


class Shopping_cart(models.Model):
    pass


class Favorit(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='castomer',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Рецепт',
        related_name='Favorit',
    )
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
