from django.contrib import admin

from .models import Amount, Favorite, Follow, Ingredient, Recipes, Tag

EMPTY_VALUE = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipes')
    search_fields = ('user', )
    empty_value_display = EMPTY_VALUE


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name', )
    empty_value_display = EMPTY_VALUE


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author',
        'image', 'text', 'cooking_time')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = EMPTY_VALUE


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color')
    search_fields = ('name', )
    empty_value_display = EMPTY_VALUE


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipes', 'ingredient')
    search_fields = ('recipes', )
    empty_value_display = EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', )
    empty_value_display = EMPTY_VALUE
