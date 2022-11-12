from django.contrib import admin
from django.urls import path, include
from src.entities.view_js import EntityListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('src.routers')),
    path('entities', EntityListView.as_view())
]
