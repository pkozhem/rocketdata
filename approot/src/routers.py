from django.urls import path, include


urlpatterns = [
    path('users/', include('src.users.urls'))
]