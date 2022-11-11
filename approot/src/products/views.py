from rest_framework.generics import CreateAPIView
from src.core.views import UpdateDestroyAPIView
from src.products.models import Product
from src.products.serializers import ProductSerializer


class ProductCreateAPIView(CreateAPIView):
    """ Product create API View. """

    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects


class ProductUpdateDestroyAPIView(UpdateDestroyAPIView):
    """ Product UD API View. """

    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs['pk'])
