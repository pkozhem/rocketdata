from rest_framework import serializers
from src.entities.models import Entity, Contacts, Address
from src.products.serializers import ProductSerializer
from src.users.serializers import UserPublicSerializer


class AddressSerializer(serializers.ModelSerializer):
    """ Address serializer. """

    class Meta:
        model = Address
        fields = '__all__'


class ContactsSerializer(serializers.ModelSerializer):
    """ Contacts serializer with custom serializer for 'address' field. """

    address = AddressSerializer(many=False, required=False)

    class Meta:
        model = Contacts
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):
    """ Entity serializer with custom serializer for 'contacts' fields. """

    contacts = ContactsSerializer(many=False, required=False)
    product = ProductSerializer(many=True, required=False)
    user = UserPublicSerializer(many=True, required=False)

    class Meta:
        model = Entity
        fields = '__all__'
