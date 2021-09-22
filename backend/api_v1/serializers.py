from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.utils import model_meta
from rest_framework.validators import UniqueTogetherValidator

from .models import (Amount, Favorite, Follow, Ingredient, Recipes,
                     Shopping_cart, Tag, User)


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор модели User """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'id',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """ Метод для получения поля о подпики на пользователя """
        request = self.context.get('request')
        return Follow.objects.filter(user=request.user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Tag """
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для Ingredient """
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit', 'id',)

    def to_internal_value(self, data):
        """ пока не вспомнил зачем этот метод """
        return Ingredient.objects.get(id=data)


class AmountPostSerializer(serializers.ModelSerializer):
    id = IngredientSerializer()

    class Meta:
        model = Amount
        fields = ('id', 'amount')


class AmountGetSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')
    amount = serializers.IntegerField()

    class Meta:
        model = Amount
        fields = ('name', 'measurement_unit', 'id', 'amount')


class RecipesGetSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = AmountGetSerializer(source='amount_set', many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = '__all__'

    def get_is_favorited(self, obj):
        request_user = self.context.get('request').user
        return Favorite.objects.filter(user=request_user, recipes=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user
        return Shopping_cart.objects.filter(
            user=request_user, recipes=obj).exists()


class RecipesPostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = AmountPostSerializer(many=True)
    image = Base64ImageField(required=False)

    # TODO: катомная реализаыия работы с изображениями в BASE64

    class Meta:
        model = Recipes
        fields = '__all__'

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            Amount.objects.create(
                recipes=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        info = model_meta.get_field_info(instance)
        # понять как от этого избавится !!!
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        Amount.objects.filter(recipes=instance).delete()
        for ingredient in ingredients:
            Amount.objects.create(
                recipes=instance,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
        instance.save()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)
        return instance

    def to_representation(self, instance):
        data = RecipesGetSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
        return data


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class DetailUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'id',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(user=request.user, author=obj).exists()

    def get_recipes(self, obj):
        recipes = Recipes.objects.filter(author=obj)
        return RecipesSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        recipes_count = Recipes.objects.filter(author=obj).count()
        return recipes_count


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'author']
        )
        ]

    def validate(self, data):
        if data.get('user') != data.get('author'):
            return data
        raise serializers.ValidationError('Нельзя подписаться на самого себя')

    def to_representation(self, instance):
        data = DetailUserSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data
        return data
