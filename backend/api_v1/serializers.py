from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.utils import model_meta

from .models import Amount, Favorit, Follow, Ingredient, Recipes, Tag, User


class UserSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        return Follow.objects.filter(user=request.user, author=obj).exists()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit', 'id',)

    def to_internal_value(self, data):
        return Ingredient.objects.get(id=data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


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
    image = serializers.ImageField()

    class Meta:
        model = Recipes
        fields = '__all__'


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


class FavoritSerializer(serializers.ModelSerializer):
    # TODO: переписать!!!!!
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    recipes = serializers.SlugRelatedField(
        slug_field='username',
        queryset=Recipes.objects.all()
    )

    class Meta:
        model = Favorit
        fields = ('user', 'recipes')
        validators = [UniqueTogetherValidator(
            queryset=Favorit.objects.all(),
            fields=['user', 'recipes']
        )
        ]

    def validate(self, attrs):
        if self.context['request'].user != attrs.get('author'):
            return attrs
        raise serializers.ValidationError(
            'Нльзя подписаться на самого себя!!!')


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
