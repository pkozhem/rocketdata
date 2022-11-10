from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from src.entities.models import Entity, Contacts, Address
from src.products.serializers import ProductSerializer
from src.users.serializers import UserPublicSerializer


class AddressSerializer(serializers.ModelSerializer):
    """ Address serializer. """

    class Meta:
        model = Address
        exclude = ('id', 'contacts')


class ContactsSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """ Contacts serializer. """

    email = serializers.EmailField(required=False)
    address = AddressSerializer(many=False, required=False)

    class Meta:
        model = Contacts
        exclude = ('entity',)


class EntitySerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """ Entity serializer. """

    type = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    debt = serializers.DecimalField(required=False, max_digits=9, decimal_places=2, read_only=True)
    date_created = serializers.DateTimeField(required=False, read_only=True)
    contacts = ContactsSerializer(many=False, required=False)
    products = ProductSerializer(many=True, required=False)
    user = UserPublicSerializer(many=True, required=False)

    class Meta:
        model = Entity
        fields = '__all__'
