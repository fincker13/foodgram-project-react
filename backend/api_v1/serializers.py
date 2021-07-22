from rest_framework import serializers

from .models import Ingredients, Recipes, Tags


class RecipesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Recipes
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class TasgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
