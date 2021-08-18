from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import filters, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)

from .models import Ingredient, Recipes, Tag, Follow, User
from .serializers import (
    FollowSerializer,
    IngredientSerializer,
    RecipesGetSerializer,
    RecipesPostSerializer,
    TagSerializer,
    FavoritSerializer
)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesGetSerializer
        return RecipesPostSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class IngrediensViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None


class TagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None


class FavoritViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritSerializer


class SubscribeViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, id):
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

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.get(user=user, author=author)
        follow.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Follow.objects.filter(user=user)
