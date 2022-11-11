from django.urls import path
from src.products.views import ProductCreateAPIView, ProductUpdateDestroyAPIView

urlpatterns = [
    path('create', ProductCreateAPIView.as_view()),
    path('<int:pk>', ProductUpdateDestroyAPIView.as_view())
]
