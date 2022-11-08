from rest_framework import serializers
from src.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ Product serializer. """

    class Meta:
        model = Product
        fields = '__all__'
