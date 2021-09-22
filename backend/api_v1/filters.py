from django_filters import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipes


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'is_favorited', )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipes.objects.filter(favorites__user=user)
        return Recipes.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipes.objects.filter(shopping__user=user)
        return Recipes.objects.all()
