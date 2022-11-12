from django.urls import path
from src.entities.views import (
    EntityListAPIView,
    EntityCountryAPIView,
    EntityDebtGreaterThanAverage,
    EntityByProductIDAPIView,
    EntityRetrieveAPIView,
    EntityCreateAPIView,
    EntityUpdateDestroyAPIView,
    ContactsQRCode
)


urlpatterns = [
    path('all', EntityListAPIView.as_view()),
    path('country', EntityCountryAPIView.as_view()),
    path('debt', EntityDebtGreaterThanAverage.as_view()),
    path('product', EntityByProductIDAPIView.as_view()),
    path('my', EntityRetrieveAPIView.as_view()),
    path('create', EntityCreateAPIView.as_view()),
    path('<int:pk>', EntityUpdateDestroyAPIView.as_view()),
    path('qrcode/<int:pk>', ContactsQRCode.as_view())
]
