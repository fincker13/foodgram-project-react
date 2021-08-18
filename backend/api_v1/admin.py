from django.contrib import admin

from .models import Follow, Amount, Favorit, Ingredient, Recipes, Tag


@admin.register(Favorit)
class FavoritAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipes')
    search_fields = ('user', )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author',
        'image', 'text', 'cooking_time')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color')
    search_fields = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipes', 'ingredient')
    search_fields = ('recipes', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
