from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientSearchFilter, RecipesFilter
from .models import (Favorite, Follow, Ingredient, Recipes, Shopping_cart, Tag,
                     User)
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipesGetSerializer, RecipesPostSerializer,
                          RecipesSerializer, TagSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
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


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = [IngredientSearchFilter]
    search_fields = ['^name']
    pagination_class = None


class TagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None


class SubscribeViewSet(APIView):

    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request, id):
        user = get_object_or_404(User, username=request.user)
        author = get_object_or_404(User, id=id)
        context = {
            'request': request
        }
        data = {
            'user': user.username,
            'author': author.username
        }
        serializer = FollowSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.get(user=user, author=author)
        follow.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = FollowSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Follow.objects.filter(user=user)
