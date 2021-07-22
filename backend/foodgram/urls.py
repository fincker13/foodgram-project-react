from django.contrib import admin
from django.urls import include, path

api_urlpatterns = [
    path('users/', include('users.urls')),
    path('', include('api_v1.urls')),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
