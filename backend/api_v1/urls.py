
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesViewSet, SubscribeViewSet,
                    SubscriptionsViewSet, TagsViewSet)

router_v1 = DefaultRouter()

router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register(
    'users/subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)


urlpatterns = [
    path(
        'users/<int:id>/subscribe/',
        SubscribeViewSet.as_view(),
        name='subscribe'
    ),
    path('', include(router_v1.urls)),
]
