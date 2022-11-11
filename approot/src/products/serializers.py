from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from src.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ Product serializer. """

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            "name": {
                "required": True
            }
        }

    def validate(self, attrs):
        """ Validates or not incoming name length and release date. """

        if 'date_release' in attrs:
            if attrs['date_release'] > date.today() and len(attrs['name']) > 25:
                raise ValidationError({"detail": [
                    "Product's name should contains maximum 25 symbols.",
                    "Release date cannot be later than today."
                ]})

            elif attrs['date_release'] > date.today():
                raise ValidationError({"detail": "Release date cannot be later than today."})

        if len(attrs['name']) > 25:
            raise ValidationError({"detail": "Product's name should contains maximum 25 symbols."})

        return attrs
