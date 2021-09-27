from django.shortcuts import HttpResponse, get_object_or_404
from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipesFilter
from .models import (Amount, Favorite, Follow, Ingredient, Recipes,
                     Shopping_cart, Tag, User)
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipesGetSerializer, RecipesPostSerializer,
                          RecipesSerializer, TagSerializer, UserSerializer)


class IngredientsViewSet(viewsets.ModelViewSet):
    """ View для игредиентов """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = [IngredientSearchFilter]
    search_fields = ['^name']
    pagination_class = None


class TagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ View для Тегов """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """ View для рецептов """
    queryset = Recipes.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesGetSerializer
        return RecipesPostSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if Favorite.objects.filter(user=user, recipes=recipe).exists():
            return Response(
                'Рецепт уже добавлен в избаранное',
                status=status.HTTP_400_BAD_REQUEST
            )
        obj = Favorite.objects.create(
            user=user, recipes=recipe
        )
        obj.save()
        serializer = RecipesSerializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        recipes = self.get_object()
        obj = Favorite.objects.get(user=user, recipes=recipes)
        obj.delete()
        serializer = RecipesSerializer(recipes)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if Shopping_cart.objects.filter(user=user, recipes=recipe).exists():
            return Response(
                'Рецепт уже добавлен в Список кокупок',
                status=status.HTTP_400_BAD_REQUEST
            )
        obj = Shopping_cart.objects.create(
            user=user, recipes=recipe
        )
        obj.save()
        serializer = RecipesSerializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        recipes = self.get_object()
        obj = Shopping_cart.objects.get(user=user, recipes=recipes)
        obj.delete()
        serializer = RecipesSerializer(recipes)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        shopping_list = {}
        user = request.user
        ingredients = Amount.objects.filter(recipes__shopping__user=user)

        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount

        wishlist = ([f" {item} - {value['amount']} "
                     f"{value['measurement_unit']} \n"
                     for item, value in shopping_list.items()])

        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response


class CastomUserViewSet(UserViewSet):
    """ View для реализации подписок на пользователей """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        context = {
            'request': request
        }
        if (Follow.objects.filter(user=user, author=author).exists()
                or author == user):
            return Response(
                'Вы уже подписаны на данного пользователя'
                'или вы пытаеть подписаться на себя',
                status=status.HTTP_400_BAD_REQUEST
            )
        obj = Follow.objects.create(user=user, author=author)
        obj.save()
        serializer = FollowSerializer(obj, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        obj = Follow.objects.get(user=user, author=author)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request, pk=None):
        user = request.user
        follow_list = Follow.objects.filter(user=user)
        context = {
            'request': request
        }
        paginete_list = self.paginate_queryset(follow_list)
        serializer = FollowSerializer(
            paginete_list, many=True,
            context=context
        )
        return self.get_paginated_response(serializer.data)
